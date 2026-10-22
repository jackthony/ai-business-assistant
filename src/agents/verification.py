import re

from pydantic import BaseModel


class VerificationResult(BaseModel):
    ok: bool
    reasons: list[str]


def verify_response(text: str) -> VerificationResult:
    reasons: list[str] = []

    # empty: texto solo con espacios en blanco
    if text.strip() == "":
        return VerificationResult(ok=False, reasons=["empty"])

    # too_many_lines: más de 3 líneas no vacías
    lineas_no_vacias = [l for l in text.splitlines() if l.strip()]
    if len(lineas_no_vacias) > 3:
        reasons.append("too_many_lines")

    # too_many_questions: más de 1 signo ?
    if text.count("?") > 1:
        reasons.append("too_many_questions")

    # invented_price
    if _tiene_precio(text):
        reasons.append("invented_price")

    return VerificationResult(ok=(len(reasons) == 0), reasons=reasons)


def _tiene_precio(text: str) -> bool:
    # (a) S/ seguido de punto opcional, espacios opcionales y un dígito
    if re.search(r"S/\.?\s*\d", text):
        return True
    # (b) $ seguido de espacios opcionales y un dígito
    if re.search(r"\$\s*\d", text):
        return True
    # (c) PEN en mayúsculas seguida de espacios opcionales y un dígito
    if re.search(r"PEN\s*\d", text):
        return True
    # (d) número (con parte decimal opcional con punto o coma) seguido de espacios y soles/nuevos soles
    return bool(
        re.search(r"\d+[.,]?\d*\s+soles", text, re.IGNORECASE)
        or re.search(r"\d+[.,]?\d*\s+nuevos soles", text, re.IGNORECASE)
    )
