"""Modelo guionado: devuelve respuestas fijas en orden (CI y pruebas, sin red)."""


class ScriptedModel:
    def __init__(self, *answers: str) -> None:
        self.answers = answers or ("",)
        self.calls = 0

    def complete(self, system: str, user: str) -> str:
        self.calls += 1
        return self.answers[min(self.calls, len(self.answers)) - 1]
