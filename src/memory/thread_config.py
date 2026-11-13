import re

from langchain_core.runnables import RunnableConfig

# Solo letras, números y _ . : - (de 1 a 64 caracteres)
_ALLOWED_THREAD_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,64}$")


def config_for_phone(phone: str) -> RunnableConfig:
    """Arma la configuración del hilo de conversación para un teléfono."""

    # TODO 1: validar que el teléfono no esté vacío ni contenga solo espacios
    if not phone or not phone.strip():
        raise ValueError("El teléfono no puede estar vacío.")

    # TODO 2: validar que solo contenga caracteres permitidos
    if not _ALLOWED_THREAD_ID.fullmatch(phone):
        raise ValueError("El teléfono contiene caracteres no permitidos.")

    # Devolver la configuración del hilo de conversación
    return {"configurable": {"thread_id": phone}}
