# Precios Meta WhatsApp Cloud API — archivo de referencia

> Captura: **2026-10-06**. Fuentes: [pricing oficial Meta](https://developers.facebook.com/docs/whatsapp/pricing) (act. 30-sep-2026), [platform pricing](https://business.whatsapp.com/products/platform-pricing), [authentication-international](https://developers.facebook.com/docs/whatsapp/pricing/authentication-international-rates) y rate cards USD "effective October 1, 2026".
> Si algo cambia: Meta solo ajusta tarifas el 1er día del trimestre con preaviso. Revisar cada quincena en S13+ (FinOps).

## Modelo vigente

- **Por mensaje entregado** (per-message pricing, desde 1-jul-2025). Antes: por conversación de 24 h.
- Se cobra solo lo **delivered** (el webhook de estado lo confirma). Mensajes usuario→negocio: **nunca** se cobran. Paga la empresa, jamás el cliente.
- Categorías: **marketing** (template promocional), **utility** (template transaccional), **authentication** (template OTP), **service** (free-form dentro de la ventana de 24 h), y *Meta Business Agent* (plataforma de Meta — **no aplica a nuestro proyecto**, que usa agente propio).

## Reglas que afectan nuestro costo

1. **Ventana de servicio 24 h (CSW):** se abre/resetea con cada mensaje del usuario. Dentro: free-form (service) y/o templates. Fuera: **solo templates aprobados**.
2. **Proactivo = template:** toda reactivación (S13) y aviso sin respuesta previa del usuario necesita template aprobado (categoría marketing o utility) → **tiene costo**.
3. **1.000 mensajes service gratis/mes por número** (desde 1-oct-2026); el 1.001 en adelante se cobra. Sin método de pago registrado, Meta deja de entregar al agotarse el tier.
4. **Entry points gratuitos (FEP):** respuesta a click-to-WhatsApp (ads CTWA) o botón CTA de Facebook dentro de la CSW → marketing/utility/service **gratis** (duración: docs dicen 7 días; la página comercial, 72 h — verificar en el panel).
5. **Utility en respuesta al usuario** (dentro de CSW): gratis hasta sep-2026; **desde 1-oct-2026 vuelve a cobrarse**.
6. **Volume tiers** (solo utility y authentication, a nivel portfolio, mensuales): descuentos de −5% a −25% según volumen.

## Tarifas PERÚ (mercado standalone desde 1-oct-2026; ya NO es "Rest of Latin America")

| Categoría | USD / mensaje entregado |
|---|---|
| Marketing | **0,0703** (sin volume tiers) |
| Utility | 0,03 (descuentos desde 100k/mes: −5% … −25%) |
| Authentication | 0,03 (descuentos desde 120k/mes) |
| Service | 0,03 (tras los 1.000 gratis/mes) |
| Authentication-International | no aplica a Perú |

Facturación: desde 1-abr-2026 se puede facturar en **PEN** (se elige al crear la Messaging account, no cambia después).

## Qué significa para nosotros (FinOps)

- Nuestro costo real = templates marketing/utility enviados + service tras el tier gratis. Un usuario que entra por CTWA y conversa dentro de la CSW cuesta **0**.
- La reactivación proactiva (S13) cuesta $0,0703 (marketing) o $0,03 (utility) por mensaje entregado → diseñar con cierre por FEP/CTWA cuando sea posible.
- Medir desde S4: costo por conversación = (mensajes cobrados × tarifa) / conversaciones; registrar en `program/00_PROJECT/roi_metrics.md` (S15).
- Aviso trimestral: revisar esta página cada 1-ene/1-abr/1-jul/1-oct.
