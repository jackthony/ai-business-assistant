"""Adaptadores de Ollama (HTTP): implementan los puertos `ChatModel` y `Embedder`."""

import re

import httpx

_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


class OllamaChat:
    def __init__(
        self,
        model: str = "deepseek-r1:14b",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        self._model = model
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def complete(self, system: str, user: str) -> str:
        r = self._client.post(
            "/api/chat",
            json={
                "model": self._model,
                "stream": False,
                "options": {"temperature": 0},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
        )
        r.raise_for_status()
        return _THINK.sub("", str(r.json()["message"]["content"])).strip()


class OllamaEmbedder:
    def __init__(
        self,
        model: str = "bge-m3",
        base_url: str = "http://localhost:11434",
        timeout: float = 60.0,
    ) -> None:
        self._model = model
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def embed(self, texts: list[str]) -> list[list[float]]:
        r = self._client.post("/api/embed", json={"model": self._model, "input": texts})
        r.raise_for_status()
        vectors: list[list[float]] = r.json()["embeddings"]
        return vectors
