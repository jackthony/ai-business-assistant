"""Bloque S7-A — una tool que NO acepta basura (Pydantic V2, errores tipados).

Idea (ADR-009, validación determinista primero): la tool valida SUS argumentos
antes de hacer nada. Si el modelo local manda algo raro, la tool devuelve un
error tipado que el agente puede explicar; nunca lanza una excepción cruda ni
inventa un precio. El catálogo de aquí es FALSO: en tu Issue sale del RAG/Excel.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

CATALOGO_FALSO = {
    "facial-basico": {
        "nombre": "Limpieza facial básica",
        "precio_soles": 80.0,
        "duracion_min": 45,
    },
    "depilacion-axilas": {
        "nombre": "Depilación de axilas",
        "precio_soles": 35.0,
        "duracion_min": 20,
    },
}


class ConsultaServicio(BaseModel):
    # extra="forbid": un argumento que no existe en el contrato es un error, no se ignora en silencio.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    service_id: str = Field(min_length=3, max_length=40, pattern=r"^[a-z0-9-]+$")


class ServicioOut(BaseModel):
    service_id: str
    nombre: str
    precio_soles: float = Field(gt=0)
    duracion_min: int = Field(gt=0)


class ErrorTool(BaseModel):
    codigo: Literal["argumentos_invalidos", "servicio_no_encontrado"]
    mensaje: str


def consultar_servicio(args: dict[str, object]) -> ServicioOut | ErrorTool:
    """Devuelve el servicio o un ErrorTool. Nunca lanza por argumentos malos."""
    try:
        consulta = ConsultaServicio.model_validate(args)
    except ValidationError as error:
        primero = error.errors()[0]
        campo = ".".join(str(parte) for parte in primero["loc"]) or "args"
        return ErrorTool(
            codigo="argumentos_invalidos", mensaje=f"{campo}: {primero['msg']}"
        )

    datos = CATALOGO_FALSO.get(consulta.service_id)
    if datos is None:
        return ErrorTool(codigo="servicio_no_encontrado", mensaje=consulta.service_id)
    return ServicioOut(service_id=consulta.service_id, **datos)  # type: ignore[arg-type]
