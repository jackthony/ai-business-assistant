# Precios Meta WhatsApp Cloud API — archivo de referencia

> ⚠️ **Tarifas Perú: valores de referencia de la rate card 1-oct-2026 (vía BSPs), pendientes de confirmar contra el panel Billing del WABA (WhatsApp Manager → Configuración → Facturación).** Al confirmarlas ahí, eliminar esta nota.
>
> Captura: **2026-10-06**. Fuentes: [pricing oficial Meta](https://developers.facebook.com/docs/whatsapp/pricing) (act. 30-sep-2026), [platform pricing](https://business.whatsapp.com/products/platform-pricing), [authentication-international](https://developers.facebook.com/docs/whatsapp/pricing/authentication-international-rates), rate cards USD "effective October 1, 2026" y [resumen verificado del cambio 1-oct-2026](https://respond.io/blog/whatsapp-business-api-pricing) (respond.io, act. 2026-10-06 — fuente secundaria; gana la doc de Meta).
> Si algo cambia: Meta solo ajusta tarifas el 1er día del trimestre con preaviso. Revisar cada quincena en S13+ (FinOps).

## Modelo vigente (confirmado 1-oct-2026)

- **Por mensaje entregado** (per-message pricing, desde 1-jul-2025). Antes: por conversación de 24 h.
- Se cobra solo lo **delivered** (el webhook de estado lo confirma). Mensajes usuario→negocio: **nunca** se cobran. Paga la empresa, jamás el cliente.
- Categorías: **marketing**, **utility**, **authentication** (templates), **service** (free-form dentro de la ventana de 24 h) y *Meta Business Agent* (no aplica: usamos agente propio).
- **Cambio 1-oct-2026 (verificado):** los *service messages* (free-form en la ventana de 24 h) ahora cuestan: **1.000 gratis/mes por número**, después tarifa regional utility. El saldo **se resetea el 1.º de cada mes** (no se acumula) y es **por número**, no por WABA.
- **Cambio 1-oct-2026 (verificado):** los **utility templates enviados DENTRO de la ventana de 24 h ahora se cobran siempre** (antes gratis). Sin margen gratis.
- **FEP (free entry points):** CTWA ads → ventana gratis hasta **7 días**; botón de Facebook Page → **72 h**. Dentro de esa ventana, todo (incluso templates) es gratis.

## Límites de envío (messaging limits — desde 7-oct-2025)

- Se calculan **por portfolio de negocio** (no por número) y solo cuentan templates salientes (los mensajes dentro de la CSW no).
- Escala: **250** (inicio) → 2.000 → 10.000 → 100.000 → ilimitado, con subidas automáticas (~6 h) si se mantiene calidad.
- Error **131049**: máximo 2 templates marketing sin respuesta del usuario en 24 h; el 3.º falla (anti-spam).

## Templates (reglas verificadas — afecta #16)

- Solo se pueden usar **templates aprobados por Meta** fuera de la CSW (y utility dentro de la CSW, cobrados).
- Estructura: header (opcional) · **body ≤1.024 caracteres** · placeholders `{{1}}` **secuenciales** y con texto alrededor (nada de placeholders flotantes) · footer · botones.
- Categorías: utility (transaccional/citas), authentication (OTP), marketing (promocional). Contenido ambiguo → lo clasifican marketing (el más caro).
- **Aprobación:** normalmente <24 h. **Una vez aprobado no se puede editar** (se crea versión nueva). Rechazos típicos: pedir datos sensibles, categoría equivocada, idioma que no coincide, errores ortográficos, placeholders mal formados.
- **Quality rating:** si el usuario marca spam → template "flagged" → si no mejora en 7 días → **disabled**.
- Opt-in obligatorio: solo enviar a quien dio consentimiento activo.

## BSP opcional (Kapso — verificado 2026-10-06)

- Kapso es un BSP "dev-first" (API/CLI/MCP/agentes): Free $0 (2.000 msgs/mes, sandbox, 1 número), Pro $25/mes (100.000 msgs, 3 números), Platform $299/mes (1M msgs, 50 números).
- **Meta fees sin markup** (pass-through): útil como plan B si la integración directa Cloud API se complica. Decisión en S10 (B/B/I) — ver `kapso-n8n.md`.

## Reglas que afectan nuestro costo

1. **Ventana de servicio 24 h (CSW):** se abre/resetea con cada mensaje del usuario. Dentro: free-form (service) y/o templates. Fuera: **solo templates aprobados**.
2. **Proactivo = template:** toda reactivación (S13) y aviso sin respuesta previa del usuario necesita template aprobado (categoría marketing o utility) → **tiene costo**.
3. **1.000 mensajes service gratis/mes por número** (desde 1-oct-2026); el 1.001 en adelante se cobra. Sin método de pago registrado, Meta deja de entregar al agotarse el tier.
4. **Entry points gratuitos (FEP):** respuesta a click-to-WhatsApp (ads CTWA) o botón CTA de Facebook → gratis hasta 7 días (CTWA) / 72 h (Page).
5. **Utility en respuesta al usuario** (dentro de CSW): **desde 1-oct-2026 se cobra siempre** (antes gratis). ⚠️ Diseño: prefiere free-form para respuestas; reserva utility para confirmaciones formales.
6. **Volume tiers** (solo utility y authentication, a nivel portfolio, mensuales): descuentos de −5% a −25% según volumen.

## Tarifas PERÚ (mercado standalone desde 1-oct-2026; ya NO es "Rest of Latin America")

Valores de referencia tomados de la rate card vigente (1-oct-2026) vía BSPs que reenvían las tarifas oficiales de Meta (plivo.com/whatsapp/pricing/pe, formbeep.com/whatsapp-api-pricing — consultados 2026-10-06). **Confirmar contra el panel Billing del WABA antes de fijar presupuestos.**

| Categoría | USD / mensaje entregado |
|---|---|
| Marketing | **0,07733** (sin volume tiers) |
| Utility | 0,03300 (descuentos desde 100k/mes: −5% … −25%) |
| Authentication | 0,03300 (descuentos desde 120k/mes) |
| Service | 0,03300 (tras los 1.000 gratis/mes) |
| Authentication-International | no aplica a Perú |

Facturación: desde 1-abr-2026 se puede facturar en **PEN** (se elige al crear la Messaging account, no cambia después).

## Qué significa para nosotros (FinOps)

- Nuestro costo real = templates marketing/utility enviados + service tras el tier gratis. Un usuario que entra por CTWA y conversa dentro de la CSW cuesta **0**.
- La reactivación proactiva (S13) cuesta $0,07733 (marketing) o $0,03300 (utility) por mensaje entregado → diseñar con cierre por FEP/CTWA cuando sea posible.
- Medir desde S4: costo por conversación = (mensajes cobrados × tarifa) / conversaciones; registrar en `program/00_PROJECT/roi_metrics.md` (S15).
- Aviso trimestral: revisar esta página cada 1-ene/1-abr/1-jul/1-oct.
