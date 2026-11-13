"""Exercise the WhatsApp HTTP endpoint with a fully synthetic catalog and transport."""

import hashlib
import hmac
import inspect
import json
import socket
import threading
import time

import httpx
import uvicorn
from langgraph.checkpoint.memory import InMemorySaver

from agents.graph import build_graph
from api.chat_app import create_chat_app
from rag.documents import Document
from rag.embedding import LexicalEmbedder
from rag.store import ChromaStore
from services.notifier_memory import InMemoryNotifier

TOKEN = "verify-senati-fake"
SECRET = b"secret-senati-fake"
PHONE = "51900000000"
ANSWER = "El taller de prueba Senati cuesta S/ 42.00 [1]."


class FakeModel:
    def complete(self, system: str, user: str) -> str:
        return ANSWER


def main() -> None:
    if "whatsapp_send" not in inspect.signature(create_chat_app).parameters:
        raise SystemExit("El webhook de #3 aún no está implementado en esta rama.")
    store = ChromaStore(LexicalEmbedder(), "senati-fake-whatsapp")
    store.ingest(
        [
            Document(
                doc_id="fake-1",
                text="El taller de prueba Senati cuesta S/ 42.00.",
                label="Catálogo ficticio SENATI",
                source="fixture:fake-1",
                kind="servicio",
            )
        ]
    )
    graph = build_graph(
        store,
        FakeModel(),
        "Solo datos de prueba",
        InMemoryNotifier(),
        None,
        InMemorySaver(),
    )
    sent: list[tuple[str, str]] = []
    got_reply = threading.Event()

    def fake_send(phone: str, text: str) -> None:
        sent.append((phone, text))
        got_reply.set()

    app = create_chat_app(
        graph,
        whatsapp_verify_token=TOKEN,
        whatsapp_app_secret=SECRET.decode(),
        whatsapp_send=fake_send,
    )
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen()
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning"))
    thread = threading.Thread(
        target=server.run, kwargs={"sockets": [sock]}, daemon=True
    )
    thread.start()

    def payload(**value: object) -> bytes:
        return json.dumps({"entry": [{"changes": [{"value": value}]}]}).encode()

    def sign(body: bytes) -> str:
        return "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()

    try:
        deadline = time.monotonic() + 10
        while not server.started and time.monotonic() < deadline:
            time.sleep(0.02)
        assert server.started
        with httpx.Client(
            base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=5
        ) as client:
            assert client.get("/health").json() == {"status": "ok"}
            url = "/whatsapp/webhook"
            q = {
                "hub.mode": "subscribe",
                "hub.verify_token": TOKEN,
                "hub.challenge": "senati-987",
            }
            ok = client.get(url, params=q)
            assert (ok.status_code, ok.text) == (200, "senati-987")
            assert (
                client.get(
                    url, params={**q, "hub.verify_token": "incorrecto"}
                ).status_code
                == 403
            )
            msg = payload(
                messages=[
                    {
                        "from": PHONE,
                        "type": "text",
                        "text": {"body": "¿Cuánto cuesta el taller de prueba Senati?"},
                    }
                ]
            )
            assert client.post(url, content=msg).status_code == 403
            assert (
                client.post(
                    url, content=msg + b" ", headers={"X-Hub-Signature-256": sign(msg)}
                ).status_code
                == 403
            )
            for ignored in (payload(statuses=[{"id": "estado-falso"}]), b"{"):
                assert (
                    client.post(
                        url,
                        content=ignored,
                        headers={"X-Hub-Signature-256": sign(ignored)},
                    ).status_code
                    == 200
                )
            assert not got_reply.is_set()
            reply = client.post(
                url, content=msg, headers={"X-Hub-Signature-256": sign(msg)}
            )
            assert (reply.status_code, reply.json()) == (200, {"ok": True})
            assert got_reply.wait(3) and len(sent) == 1
            assert (
                sent[0][0] == PHONE
                and "S/ 42.00" in sent[0][1]
                and "Catálogo ficticio" in sent[0][1]
            )
        print(
            "HTTP real por loopback: GET correcto/incorrecto, firma ausente/adulterada, estado, JSON inválido y un envío simulado con RAG ficticio: OK."
        )
    finally:
        server.should_exit = True
        thread.join(5)
        sock.close()


if __name__ == "__main__":
    main()
