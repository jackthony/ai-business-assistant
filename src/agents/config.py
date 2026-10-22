"""Configuración por tenant (`configs/<tenant>/`): el núcleo no tiene `if tenant == ...`."""

from pathlib import Path

from pydantic import BaseModel

from agents.prompt import compose_system_prompt, load_prompt_pieces
from tools.schedule import Schedule, load_schedule

CONFIGS_DIR = Path(__file__).resolve().parents[2] / "configs"


class TenantConfig(BaseModel):
    prompt: str
    namespace: str
    booking_prompt: str
    schedule: Schedule


def load_tenant_config(tenant: str, root: Path = CONFIGS_DIR) -> TenantConfig:
    base = root / tenant
    return TenantConfig(
        prompt=compose_system_prompt(load_prompt_pieces(base / "prompt_v1.md")),
        namespace=(base / "rag.namespace").read_text(encoding="utf-8").strip(),
        booking_prompt=(base / "booking_prompt.md").read_text(encoding="utf-8"),
        schedule=load_schedule(base / "schedule.json"),
    )
