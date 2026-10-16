"""Configuración por tenant (`configs/<tenant>/`): el núcleo no tiene `if tenant == ...`."""

from pathlib import Path

from pydantic import BaseModel

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
        prompt=(base / "prompt.md").read_text(encoding="utf-8"),
        namespace=(base / "rag.namespace").read_text(encoding="utf-8").strip(),
        booking_prompt=(base / "booking_prompt.md").read_text(encoding="utf-8"),
        schedule=load_schedule(base / "schedule.json"),
    )
