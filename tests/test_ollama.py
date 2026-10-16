"""Adaptadores de Ollama contra un servidor simulado (sin red)."""

import httpx
import respx

from agents.config import load_tenant_config
from models.ollama import OllamaChat, OllamaEmbedder


@respx.mock
def test_chat_quita_el_razonamiento():
    respx.post("http://x/api/chat").mock(
        return_value=httpx.Response(
            200, json={"message": {"content": "<think>pienso…</think>Hola [1]"}}
        )
    )
    assert OllamaChat("m", "http://x").complete("sys", "usr") == "Hola [1]"


@respx.mock
def test_embed_devuelve_vectores():
    respx.post("http://x/api/embed").mock(
        return_value=httpx.Response(200, json={"embeddings": [[0.1, 0.2], [0.3, 0.4]]})
    )
    assert OllamaEmbedder("m", "http://x").embed(["a", "b"]) == [[0.1, 0.2], [0.3, 0.4]]


def test_config_del_tenant():
    cfg = load_tenant_config("hola_mujer")
    assert cfg.namespace == "hola_mujer"
    assert "<fragmentos>" in cfg.prompt and "[1]" in cfg.prompt
