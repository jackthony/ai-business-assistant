import logging
import os
import time

import httpx

# Configuramos un logger para registrar eventos, advertencias o errores del sender
logger = logging.getLogger(__name__)

# Versión de la Graph API de Meta para WhatsApp.
# Configurable por constructor o variable de entorno WHATSAPP_GRAPH_VERSION.
# Verificar versión vigente en https://developers.facebook.com/docs/whatsapp (por definir al cerrar S4).
DEFAULT_GRAPH_VERSION = os.getenv("WHATSAPP_GRAPH_VERSION", "v26.0")


class WhatsAppSender:
    """Envía mensajes a través de la API oficial de WhatsApp Cloud."""

    def __init__(
        self,
        phone_number_id: str,
        access_token: str,
        transport: httpx.AsyncBaseTransport | None = None,
        graph_version: str | None = None,
    ) -> None:
        """Inicializa el sender con las credenciales necesarias.

        Args:
            phone_number_id (str): El ID del número de teléfono asignado en Meta Business.
            access_token (str): Token de acceso permanente o temporal de la API de Meta.
            transport (httpx.AsyncBaseTransport, optional): Útil para inyectar un transporte
                mockeado (como MockTransport) y realizar pruebas unitarias sin llamadas reales a internet.
            graph_version (str, optional): Versión de la Graph API (p.ej. "v21.0"). Por defecto usa
                WHATSAPP_GRAPH_VERSION o "v26.0".
        """
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.transport = transport
        self.graph_version = graph_version or DEFAULT_GRAPH_VERSION

    @property
    def base_url(self) -> str:
        return f"https://graph.facebook.com/{self.graph_version}"

    async def send_text(
        self,
        to_wa_id: str,
        text: str,
        received_at: float | None = None,
    ) -> dict:
        """Envía un mensaje de texto libre a un usuario de WhatsApp.
        Nota: Solo permitido dentro de la ventana de atención de 24 horas.

        Args:
            to_wa_id (str): Número de destino del usuario (ej. 51999999999).
            text (str): Contenido del mensaje.
            received_at (float, optional): Marca de tiempo (perf_counter) en que llegó el webhook
                entrante. Si se pasa, se loguea `first_response_ms` (webhook receipt → start del envío).
                La medición completa webhook→send se cierra en el orquestador cuando se integre con #3.
        """
        # 1. Construimos la URL del endpoint de mensajes usando el ID del teléfono
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        # 2. Preparamos los headers de autenticación requeridos por Meta
        headers = {"Authorization": f"Bearer {self.access_token}"}

        # 3. Armamos el cuerpo (payload) con el formato JSON que exige la API de Meta
        body = {
            "messaging_product": "whatsapp",
            "to": to_wa_id,  # Número de destino del usuario (ej. 51999999999)
            "type": "text",  # Indicamos que es un mensaje de texto plano
            "text": {"body": text},  # Contenido del mensaje
        }

        # 4. Medimos el tiempo desde que empezamos a enviar
        start = time.perf_counter()

        # 5. Enviamos con un reintento ante fallos de red (no ante errores de Meta)
        async with httpx.AsyncClient(transport=self.transport, timeout=10.0) as client:
            for attempt in (1, 2):
                try:
                    response = await client.post(url, headers=headers, json=body)
                    break
                except httpx.TransportError:
                    logger.warning("whatsapp_send network error, attempt=%d", attempt)
                    if attempt == 2:
                        raise

        # 6. Si Meta respondió con error (401, 400...), lanzamos la excepción
        response.raise_for_status()

        # 7. Registramos la latencia del POST a Meta
        latency_ms = (time.perf_counter() - start) * 1000
        logger.info("whatsapp_send ok latency_ms=%.1f", latency_ms)

        # 8. Si conocemos el timestamp de entrada (webhook), logueamos tiempo de primera respuesta
        if received_at is not None:
            first_response_ms = (start - received_at) * 1000
            logger.info("whatsapp_first_response_ms=%.1f", first_response_ms)

        return response.json()
