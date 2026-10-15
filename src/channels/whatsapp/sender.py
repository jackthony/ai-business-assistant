import logging
import time

import httpx

# Configuramos un logger para registrar eventos, advertencias o errores del sender
logger = logging.getLogger(__name__)

# URL base oficial de la Graph API de Meta para WhatsApp (versión 17.0)
BASE_URL = "https://graph.facebook.com/v17.0"


class WhatsAppSender:
    """Envía mensajes a través de la API oficial de WhatsApp Cloud."""

    def __init__(
        self,
        phone_number_id: str,
        access_token: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Inicializa el sender con las credenciales necesarias.

        Args:
            phone_number_id (str): El ID del número de teléfono asignado en Meta Business.
            access_token (str): Token de acceso permanente o temporal de la API de Meta.
            transport (httpx.AsyncBaseTransport, optional): Útil para inyectar un transporte
                mockeado (como MockTransport) y realizar pruebas unitarias sin llamadas reales a internet.
        """
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.transport = transport

    async def send_text(self, to_wa_id: str, text: str) -> dict:
        """Envía un mensaje de texto libre a un usuario de WhatsApp.
        Nota: Solo permitido dentro de la ventana de atención de 24 horas.
        """
        # 1. Construimos la URL del endpoint de mensajes usando el ID del teléfono
        url = f"{BASE_URL}/{self.phone_number_id}/messages"

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
        async with httpx.AsyncClient(transport=self.transport) as client:
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

        # 7. Registramos la latencia
        latency_ms = (time.perf_counter() - start) * 1000
        logger.info("whatsapp_send ok latency_ms=%.1f", latency_ms)

        return response.json()

        async with httpx.AsyncClient(transport=self.transport) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            return response.json()
