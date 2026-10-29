"""Configuración por tenant (`configs/<tenant>/`): el núcleo no tiene `if tenant == ...`."""

from pathlib import Path

from pydantic import BaseModel

from agents.fewshot import load_fewshots, render_fewshots
from agents.prompt import compose_system_prompt, load_prompt_pieces
from tools.schedule import Schedule, load_schedule

CONFIGS_DIR = Path(__file__).resolve().parents[2] / "configs"


class TenantConfig(BaseModel):
    prompt: str
    prompt_v2: str
    namespace: str
    booking_prompt: str
    schedule: Schedule


def load_tenant_config(tenant: str, root: Path = CONFIGS_DIR) -> TenantConfig:
    base = root / tenant

    # Corregido: pasar el archivo exacto "prompt_v1.md"
    pieces = load_prompt_pieces(base / "prompt_v1.md")
    prompt = compose_system_prompt(pieces)

    # Cálculo de prompt_v2 usando la fórmula del contrato §5.3
    ruta_json_fewshots = base / "fewshot_objeciones.json"
    prompt_v2 = prompt + "\n\n" + render_fewshots(load_fewshots(ruta_json_fewshots))

    return TenantConfig(
        prompt=prompt,
        prompt_v2=prompt_v2,
        namespace=(base / "rag.namespace").read_text(encoding="utf-8").strip(),
        booking_prompt=(base / "booking_prompt.md").read_text(encoding="utf-8"),
        schedule=load_schedule(base / "schedule.json"),
    )
