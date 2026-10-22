"""Verificación de estilo de Hola Mujer: verifica, no corrige."""


def check_reply_style(text: str) -> list[str]:
    if not text.strip():
        return ["empty"]
    problems: list[str] = []
    if sum(1 for line in text.splitlines() if line.strip()) > 3:
        problems.append("too_many_lines")
    if text.count("?") > 1:
        problems.append("too_many_questions")
    return problems
