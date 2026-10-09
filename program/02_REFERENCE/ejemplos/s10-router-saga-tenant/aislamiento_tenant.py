"""Bloque S10-C — aislamiento por tenant (multitenant sin mezclar negocios).

Un tenant = un negocio (hola_mujer, neuracode). Regla: NINGÚN acceso a datos
(colección RAG, memoria, tools) se arma con un tenant que venga "tal cual" del
mensaje. Se resuelve contra una lista cerrada que sale de `configs/` y de ahí
sale el nombre del recurso. Un tenant desconocido es un error, no un valor por defecto.
Cubre el riesgo de contaminar el RAG entre negocios (OWASP ASI06, ADR-009).
"""

import re

PATRON_TENANT = re.compile(r"^[a-z][a-z0-9_]{2,30}$")


class TenantDesconocido(ValueError):
    pass


def resolver_tenant(candidato: str, permitidos: frozenset[str]) -> str:
    if not PATRON_TENANT.fullmatch(candidato) or candidato not in permitidos:
        raise TenantDesconocido(
            "tenant no permitido"
        )  # no eco del valor: puede ser un ataque
    return candidato


def coleccion_rag(tenant: str, permitidos: frozenset[str]) -> str:
    """Nombre de colección Chroma por tenant: nunca compartida entre negocios."""
    return f"{resolver_tenant(tenant, permitidos)}__servicios"
