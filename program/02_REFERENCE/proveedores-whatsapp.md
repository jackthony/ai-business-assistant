# Proveedores de WhatsApp: opciones, costos y plan mientras tanto

> **Estado:** borrador para decisión de Jack (dueño). Captura: **2026-10-14**.
> **Limitación de esta investigación:** el egress de la sesión bloqueó (HTTP 403 en CONNECT) los dominios oficiales de Meta, Kapso, Twilio, 360dialog, Gupshup, Bird, Infobip, Chatwoot, Telegram y gob.pe. Por eso **no se leyó ninguna página oficial de proveedor**. Lo que sigue sale de: (a) fragmentos de resultados de búsqueda, que citan la fuente original; (b) `meta-pricing.md` del repo (ya tenía tarifas de Meta, fuente secundaria). Todo lo no hallado está marcado **no confirmado**. Antes de decidir, repetir la verificación de las cifras marcadas en la sección 8.

> **Hechos confirmados por el dueño (2026-10-14, Centro de seguridad de Meta):** Hola Mujer **no es negocio verificado**; el límite de mensajería es el **estándar**; **no hay ningún proveedor/BSP conectado** y hoy atiende con la **app WhatsApp Business** (no con la API). Esto descarta la opción C tal como estaba redactada («reusar el número que ya opera en ManyChat»): ese número no está en la API. Lo que queda es A (provisional) o llevar el número a la API, y para eso la pieza clave es la **coexistencia** (sección 7).

> **Decisión del dueño (2026-10-14):** por ahora los practicantes trabajan con **datos sintéticos y fixtures**. El monitor configurará el proveedor/canal real de WhatsApp más adelante, cuando tenga tiempo.

## 1. Resumen y recomendación

- **Restricción del dueño (aplicada):** Hola Mujer **no tiene documentos** para la verificación de negocio de Meta y se quiere evitarla. NeuraCode queda **fuera del alcance** (proyecto posterior, tras validar y evaluar Hola Mujer): no es una vía para Hola Mujer. Las vías no oficiales (Baileys / WhatsApp Web) se **descartan**: riesgo de baneo del número, y ADR-003 ya las rechaza.
- **Hallazgo central:** la verificación no es un detalle de proveedor. Sin verificar, Meta parte de **250 conversaciones iniciadas por el negocio en 24 h** y no aprueba el nombre visible; según fuentes secundarias el tope puede escalar por calidad aun sin verificar, pero la verificación desbloquea nombre visible y límites mayores (sección 4). Esto aplica a **cualquier** ruta sobre la Cloud API, incluidos los BSP (Kapso, 360dialog, Twilio, Gupshup, Bird, Infobip, Chatwoot). Un BSP **no elimina** ese límite (no confirmado que alguno lo haga).
- **Recomendación para Hola Mujer:**
  1. **Ahora (S6–S8):** canal provisional. Telegram Bot API para practicantes + chat web propio, ambos detrás de un adapter (ADR-011). Costo de Meta: cero.
  2. **Producción WhatsApp:** no hay ruta que cumpla "sin verificación" **y** "escala". Si el dueño mantiene la restricción, WhatsApp real para Hola Mujer queda limitado a pruebas con número de prueba y 250 conversaciones iniciadas/24 h. Esto es decisión de Jack (sección 7).
  3. **Proveedor si se activa WhatsApp:** Meta Cloud API directa (ADR-003 vigente) por costo y sin markup. **Kapso** como alternativa si se prioriza DX para practicantes; exige revisar ADR-003 ("directa").
- **Alternativas que Jack debe decidir:** (A) canal provisional indefinido para Hola Mujer; (B) verificar Hola Mujer más adelante con documentos que hoy no existen; (C) **llevar el número actual (app WhatsApp Business) a la Cloud API en modo coexistencia**, para que la app y el agente convivan en el mismo número. Reemplaza a la antigua «usar NeuraCode», que ya no aplica. Viabilidad sin verificar el negocio: **pendiente de verificación en WhatsApp Manager** (no es «no viable»; ver sección 7).
- **Recomendación con los hechos de hoy:** seguir en **A** para S6–S8 (ya es el plan y no cuesta nada de Meta). La coexistencia (C) se evalúa **después**: primero se confirma en WhatsApp Manager que el número real es elegible y recién entonces se prueba el flujo técnico en un número de prueba; y solo si el requisito de verificación resulta no aplicar. No se toca el número en producción de Hola Mujer hasta entonces: conectarlo a la API sin coexistencia lo saca de la app WhatsApp Business.

## 2. Requisitos

| Requisito | Fuente |
|---|---|
| Webhook HTTPS público al backend FastAPI (verificación GET + POST de eventos) | ADR-003; ADR-011 (`src/channels/`) |
| Plantillas aprobadas por Meta para mensajes fuera de la ventana de 24 h | `program/02_REFERENCE/meta-pricing.md` (sección Templates) |
| Costo por mensaje entregado, medible por canal (FinOps, S15) | ADR-011; `meta-pricing.md` |
| Un solo negocio (Hola Mujer); el campo `tenant` de `InboundEvent` queda por diseño del contrato, sin segundo tenant | ADR-011 (`InboundEvent.tenant`) |
| Datos de usuarios peruanos: Ley 29733 (tratamiento, transferencia, conservación) | Ley 29733 (ver sección 8: no verificado el texto aplicable) |
| Sin datos reales de clientes en ejemplos | AGENTS.md (reglas duras) |
| Salida de datos y lock-in controlables (migrar de proveedor sin reescribir agentes) | ADR-011 (contrato interno canónico) |

## 3. Matriz comparativa

Leyenda: **C** = confirmado en fuente consultada (secundaria salvo que se indique); **NC** = no confirmado.

| Proveedor | Markup sobre tarifa Meta | Tier gratis / plan mínimo | Webhook a FastAPI propio | Templates | Multitenant | Exige verificación Meta | Privacidad / retención | Lock-in |
|---|---|---|---|---|---|---|---|---|
| **Meta Cloud API directa** | 0 (es la tarifa) — C | 1.000 service/mes/número tras 1-oct-2026 (C, secundaria) | Sí, webhooks de la Cloud API — C (doc de Meta no abierta: NC en detalle) | Aprobación en WhatsApp Manager, <24 h típico — C (secundaria) | Varios números/WABA bajo un portfolio — NC | **Sí para producción** (límite 250 BI/24 h sin verificar) — C (secundaria) | Relación directa con Meta; DPA y retención — NC | Bajo en API estándar; plantillas y WABA atados a Meta |
| **Kapso** | Modo créditos: tarifa de lista de Meta sin recargo según docs actuales; un FAQ antiguo dice que Meta se cobra directo a la tarjeta del WABA — C parcial (docs.kapso.ai, vía búsqueda). Condiciones: todo el WABA en un proyecto Kapso; los envíos se pausan al agotar créditos; el uso de IA cuesta 4,4 % + 0,30 USD | Free: 2.000 msgs/mes, 1 número, 1 GB — C (docs.kapso.ai). Pro $25/mes (100k msgs, 3 números); Platform $299/mes (1M msgs, 50 números) — C (kapso.ai, su propio blog; verificar en su pricing page) | Sí; el plan Platform incluye webhooks — C | Sí — NC en detalle | Plan Platform pensado para "onboardear clientes" — C; aislamiento por tenant — NC | NC (Kapso no lo menciona en lo leído) | NC (no hay datos de retención en lo encontrado) | Medio: créditos y plataforma propia (API/CLI/MCP) |
| **Twilio (WhatsApp Senders)** | +0,005 USD por mensaje (cargo fijo, no %), sobre tarifa Meta; según Zoko y Landbot aplica también a mensajes entrantes (el cálculo de la sección 5 solo cuenta salientes y puede subestimar) — C (fuentes secundarias) | Sandbox — NC | Sí — NC en detalle | Sí — NC | Subcuentas — NC | Sí para sender de producción — NC | NC (Twilio es EE. UU.; transferencia internacional) | Medio |
| **360dialog** | 0 sobre tarifas de conversación de Meta — C (docs.360dialog.com, snippet oficial) | Licencia mensual por número; sin cifra oficial (docs piden contactar); terceros $15–49, se usa 49 como escenario conservador — NC | Sí — NC en detalle | Sí — NC | Modelo de partner con facturación por cliente — C (docs) | NC | NC | Bajo-medio |
| **Gupshup** | Markup de **+6 %** sobre la tarifa de **marketing** en Cloud API desde 1-ene-2026, solo para remitentes que no aceptaron MM Lite (evitable si es elegible) — C (support.gupshup.io, aviso oficial) + fee de plataforma ~0,001 USD — NC | NC | Sí — NC | Sí — NC | Sí — NC | NC | NC | Medio |
| **Bird** | NC (modelo: cargo de plataforma + markup por mensaje según terceros) | NC (pricing sin cifras publicadas) | NC | NC | NC | Tiene guía de verificación Meta — C (docs.bird.com, título de la página; contenido no leído) | NC | NC |
| **Infobip** | NC (sin datos de Perú) | NC | NC | NC | NC | NC | NC | NC |
| **Chatwoot sobre Cloud API** | No cobra Meta: se paga directo a Meta (si no hay BSP) — C (chatwoot.com docs, vía búsqueda) | Software: licencia NC; self-host en nuestra infraestructura | Chatwoot recibe el webhook de Meta; reenvío al backend propio — NC | Gestión de plantillas en Chatwoot — NC | Inboxes por cuenta — NC | Igual que Meta directa (usa su WABA) — C (lógica) | **Datos en nuestra infraestructura si es self-host** (ventaja para Ley 29733) — NC legal | Bajo (OSS), pero depende de la Cloud API |

**Lectura de la matriz:** el markup de BSP es pequeño frente a la tarifa de Meta (sección 5). La diferencia real entre proveedores está en DX (onboarding, UI de inbox, plantillas), en la verificación y en la privacidad, que no se pudo confirmar en ninguno.

## 4. Sin verificación vs con verificación

| Concepto | Sin verificación de negocio | Con verificación |
|---|---|---|
| Conversaciones iniciadas por el negocio | **250 por 24 h** (rolling); el conteo es por portfolio según 360dialog (cambio de oct-2025, fuente secundaria) y por número según Clickatell; sin doc oficial — **NC** | Límite sube (el tier 1 difiere entre fuentes; la cifra exacta es NC oficial). También escala por calidad aun sin verificar (fuentes secundarias, NC oficial) |
| Nombre visible del número | No se aprueba (C, secundaria) | Aprobación posible |
| Números por cuenta | Limitados (C, secundaria: "más de 2 números" requiere verificación) | Más números |
| Número de prueba | Límites relajados, sin cifra publicada — C (docs de Meta, vía búsqueda) | No aplica |
| Documentos necesarios | Ninguno | Razón social, dirección, teléfono, email, web oficial que coincidan con registros (C, secundaria). **Hola Mujer: no disponibles** (restricción del dueño) |
| Plazo de revisión | NC | NC |

**Para Hola Mujer con la restricción:** el camino compatible es número de prueba o número sin verificar, con 250 conversaciones iniciadas/24 h. Sirve para piloto y QA, no para escala. Si se quiere escala, hay que verificar (decisión del dueño) o usar un canal que no dependa de Meta.

## 5. Costos (USD/mes)

**Supuestos (de la función `tools/asignaciones/cost_scenarios.py`):**
- Tarifas Perú de `program/02_REFERENCE/meta-pricing.md`: service 0,033 (tras 1.000 gratis/número/mes); utility 0,033; marketing 0,07733. **Pendientes de confirmar en panel Billing del WABA.** Una verificación independiente (2026-10-14) **no pudo reproducir** estas cifras: terceros dan marketing 0,08–0,084 y utility 0,02–0,024 para Perú (Edna, Chatalog; la tabla de Salesforce no trae unidad). Tómalas como orden de magnitud. La cita de `meta-pricing.md` a `plivo.com/whatsapp/pricing/pe` no se reprodujo y debe revisarse.
- Un solo número. Escenarios: 500 / 3.000 / 10.000 mensajes service, con y sin 150 utility + 50 marketing.
- Fees de BSP: Kapso Pro $25 (markup 0 supuesto), Twilio +0,005/msg, 360dialog $49/número (cifra de fuente con conflicto), Gupshup +0,001/msg (NC). El +6 % de Gupshup no entra en la columna: sobre 50 marketing equivale a ~0,23 USD/mes (50 × 0,07733 × 6 %).

| Service | Utility | Marketing | Meta directa | Kapso Pro | Twilio | 360dialog | Gupshup |
|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0,00 | 25,00 | 2,50 | 49,00 | 0,50 |
| 500 | 150 | 50 | 8,82 | 33,82 | 12,32 | 57,82 | 9,52 |
| 3.000 | 0 | 0 | 66,00 | 91,00 | 81,00 | 115,00 | 69,00 |
| 3.000 | 150 | 50 | 74,82 | 99,82 | 90,82 | 123,82 | 78,02 |
| 10.000 | 0 | 0 | 297,00 | 322,00 | 347,00 | 346,00 | 307,00 |
| 10.000 | 150 | 50 | 305,82 | 330,82 | 356,82 | 354,82 | 316,02 |

**Lectura:**
- Meta directa es la opción más barata en todos los escenarios (sin markup ni licencia).
- A volumen bajo, la licencia del BSP domina; a volumen alto, la tarifa de Meta domina (297 USD de 300+ a 10.000 msgs).
- Con el tier gratis de 1.000 service/mes, los 500 msgs no pagan Meta. Esto depende de que el tier siga vigente (ver sección 8).
- Costo por conversación para FinOps (S15): (mensajes cobrados × tarifa) / conversaciones, por canal (ADR-011).
- **Proactivos:** 0,07733 (marketing) o 0,033 (utility) por mensaje entregado; diseñar con entrada por CTWA/FEP cuando sea posible (`meta-pricing.md`).

**Canales provisionales:** Telegram Bot API y chat web propio tienen costo de API nulo o de hosting. **Costo de API de Telegram: NC en fuente oficial consultada** (bots, sin cargo, según conocimiento general, no verificado).

## 6. Plan mientras tanto (HITO 1 fin de S6 con canal provisional)

**Objetivo:** que los practicantes avancen en la capa de agentes sin depender de WhatsApp real ni de verificación.

1. **Contrato interno primero** (ADR-011): `InboundEvent` y `OutboundReply` en `src/` antes de cualquier canal. Los agentes solo hablan ese contrato.
2. **Adapter 1: Telegram Bot API** (`src/channels/telegram.py`). Recibe por webhook HTTPS (puertos 443, 80, 88 u 8443) o por polling en desarrollo. Límites de envío: ~30 msgs/s para difusión; ~1 msg/s por chat como guía (C, secundaria; Telegram no publica cifras duras de forma clara — NC).
3. **Adapter 2: chat web propio** (`src/channels/web.py`, FastAPI + página simple). Sin terceros, sin costo de Meta, datos en nuestra infraestructura. Útil para demo y QA.
4. **Número de prueba de Meta** solo para validar el adapter de WhatsApp al final del HITO, no para producción.
5. **Criterio de HITO 1 (fin de S6):** un flujo E2E (entrada → agente → respuesta) funciona en Telegram **y** en chat web, con el mismo agente y sin cambios en `src/agents/`, `src/tools/`, `src/rag/` ni `src/memory/`.
6. **Qué NO hacer:** WhatsApp Business App o coexistencia como base de desarrollo (NC: no verificado en docs de Meta; no da webhook de forma confiable para este caso); Baileys/WhatsApp Web (descartado).

## 7. Cuándo pasar a WhatsApp real

**Trigger de paso:** cuando se cumpla una de estas condiciones, decide Jack:
- (a) Hola Mujer completa verificación de negocio de Meta (hoy no tiene documentos); o
- (b) la coexistencia (opción C) resulta viable para un negocio **sin verificar** en Perú y el dueño acepta sus límites.

**Coexistencia (app WhatsApp Business + Cloud API en el mismo número), solo fuentes secundarias leídas por resultados de búsqueda (fragmentos, no páginas abiertas); ninguna es doc oficial de Meta (egress bloqueado):** permite usar ambas a la vez; los chats 1 a 1 siguen en la app y la API automatiza; sincroniza ~6 meses de historial 1:1, sin grupos; el alta es por QR desde la app; la API queda con **20 msg/s** según Positus y Jelou (otras fuentes dicen 5 o 80→20: conflicto; **no usar estas cifras para dimensionar capacidad hasta confirmarlas con Meta**; la cifra de 20 msg/s, los ~6 meses de historial y la versión 2.24.17 de la app son **no confirmados** y Positus, que también cita los 20 msg/s, es otro proveedor comercial); no soporta en la API grupos, listas de difusión, estados ni llamadas. **Requisitos con conflicto:** Jelou exige app 2.24.17+, país soportado y **negocio verificado en Business Manager**; las demás no mencionan la verificación. Si la verificación es obligatoria, Hola Mujer no puede (restricción del dueño) y queda A. Consultadas el 2026-10-14; Jelou, Kapso, 360dialog y Chakra **venden** servicios sobre la Cloud API, así que pueden favorecer la opción de conectarse. Fuentes: https://docs.jelou.ai/en/coexistence · https://kapso.ai/blog/whatsapp-business-app-coexistence-cloud-api · https://docs.360dialog.com/docs/waba-management/embedded-signup/whatsapp-coexistence · https://chakrahq.com/article/whatsapp-coexistence-business-app-register-cloud-api/amp/

**Para cerrar la duda (la responde Meta, no nosotros):** en WhatsApp Manager, ¿aparece la opción de conectar la app Business a una plataforma (coexistencia) para el número de Hola Mujer? Si el flujo de *Embedded Signup* o el proveedor rechaza el alta por falta de verificación, la respuesta es no. Ojo: una prueba con un número de prueba valida el **flujo técnico** (webhook, plantillas, sincronización), no que el **número real** de Hola Mujer sea elegible; la elegibilidad real solo la muestra WhatsApp Manager para ese número.

**Implementación (cuando se active):**
- Un adapter nuevo: `src/channels/whatsapp.py`, con verificación GET, parseo POST de eventos y envío. Solo este módulo importa SDK o HTTP de Meta/BSP (ADR-011).
- **Proveedor:** si es Meta directa, sin cambios de ADR. Si es BSP (Kapso, 360dialog, etc.), **ADR-003 dice "Cloud API directa"**: hay que escribir un ADR nuevo que la modifique antes de implementar. Ver `program/03_ARCHITECTURE/decisions/ADR-003-whatsapp-cloud-api.md`.
- **Plantillas:** registrar en el repo los `template_id` aprobados y su categoría (`OutboundReply.template_id`).
- **Ventana de 24 h:** el adapter debe rastrear la última entrada del usuario por `(tenant, user_id)` para decidir free-form o template.
- **Antes de producción:** revisar Ley 29733 con el texto oficial (sección 8) y mapear la retención de cada proveedor.

## 8. Por confirmar

| # | Tema | Por qué importa | Cómo confirmar |
|---|---|---|---|
| 1 | Tarifas Perú (0,07733 marketing; 0,033 utility/service) | Base de todos los costos | Panel Billing del WABA (WhatsApp Manager → Configuración → Facturación); la nota de `meta-pricing.md` ya lo pide |
| 2 | Cobro de service tras 1.000 gratis desde 1-oct-2026 | Cambia el costo a partir de 1.000 msgs/mes | Doc oficial de pricing de Meta (no accesible en esta sesión); `meta-pricing.md` lo atribuye a respond.io (secundaria) |
| 3 | Utility dentro de la ventana de 24 h cobrado desde 1-oct-2026 | Cambia el diseño de respuestas | Igual que #2. Las fuentes de Twilio y de `meta-pricing.md` coinciden, pero ninguna es oficial |
| 4 | Límite de 250 conversaciones iniciadas/24 h sin verificar, y si es por portfolio o por número | Define si el piloto de Hola Mujer es viable | Doc oficial de límites de mensajería de Meta |
| 5 | Si Kapso, 360dialog u otro BSP elimina el límite de 250 con verificación compartida | Podría cambiar la decisión de la sección 1 | Preguntar al proveedor por escrito. Fuentes secundarias indican que el 250 es de Meta y ningún BSP lo evita; sin evidencia en contra |
| 6 | Licencia de 360dialog ($25 / $49 / €49) | Conflicto entre fuentes | Pricing page oficial de 360dialog |
| 7 | Markup de Kapso sobre tarifas Meta en modo créditos (cero según docs.kapso.ai; no leído en página completa) | Afecta el ranking de BSP | docs.kapso.ai, página completa de pricing-faq |
| 8 | Retención, ubicación de datos y DPA de cada proveedor (Meta, Kapso, Twilio, 360dialog, Gupshup, Bird, Infobip, Chatwoot) | Ley 29733; transferencia internacional | Términos y DPA de cada proveedor |
| 9 | Texto vigente de la Ley 29733 y su Reglamento (consentimiento para transferencia, plazos de conservación). Búsqueda no lo leyó; el reglamento vigente aparece citado como D.S. 016-2024-JUS (NC: no verificado) | Requisito legal para datos de usuarios | Texto oficial en gob.pe / ANPD |
| 10 | Precios y markup de Bird, Infobip, Twilio para Perú | Sin cifras encontradas | Cotización formal o pricing page oficial |
| 11 | Chatwoot: licencia y ruta de webhook al backend propio | Afecta si entra como inbox o como BSP | chatwoot.com docs (no accesible en esta sesión) |
| 12 | Coexistencia de WhatsApp Business App con Cloud API: ¿exige negocio verificado? ¿está disponible en Perú? ¿límites exactos de mensajes por segundo? | Decide si Hola Mujer puede tener agente en su número actual sin verificar | Doc oficial de Meta (no accesible) o prueba real en un número de prueba; hoy solo fuentes secundarias en conflicto (sección 7) |
| 13 | Costo y límites de Telegram Bot API | Canal provisional | core.telegram.org/bots/api (no accesible en esta sesión) |
| 14 | Unidad de la tabla de Salesforce (86,8 / 24,7 / 24,7) | Fuente de tarifa, no usada en cálculos | Descartada hasta confirmar la unidad |

**Verificación independiente (2026-10-14, solo fuentes secundarias; ningún dominio oficial fue accesible):** confirmó 250 inicial, 1.000 service gratis/número desde 1-oct-2026, Kapso Free (2.000 msgs) y Pro ($25), y el +6 % de Gupshup; no reprodujo las tarifas de Perú ni el plan Platform de Kapso ($299) ni el fee de Gupshup (~0,001); corrigió el alcance de «sin markup» de Kapso y la licencia de 360dialog.

**Cifras más frágiles (en orden):** cargo de service tras 1.000 gratis (#2), límite de 250 y su alcance (#4), tarifa de marketing Perú (#1: fuentes de 2025 dan 0,08 y 0,0703; la de 2026 usada es 0,07733), y licencias de BSP (#6).

## 9. Fuentes

**Oficiales intentadas y no accesibles en esta sesión (403 del egress):**
- https://developers.facebook.com/docs/whatsapp/pricing
- https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
- https://business.whatsapp.com/products/platform-pricing
- https://docs.kapso.ai · https://kapso.ai/pricing
- https://www.twilio.com/en-us/whatsapp/pricing
- https://www.360dialog.com/pricing
- https://www.gupshup.io/whatsapp/pricing · https://bird.com/pricing/whatsapp · https://www.infobip.com
- https://www.chatwoot.com/docs
- https://core.telegram.org/bots/api
- https://www.gob.pe (Ley 29733)

**Fuentes consultadas por resultados de búsqueda (no abiertas completas; fragmento citado):**
- Kapso, FAQ de precios: https://docs.kapso.ai/docs/whatsapp/pricing-faq (planes, créditos, Meta sin markup en modo créditos)
- Kapso, blog: https://kapso.ai/blog/whatsapp-api-pricing-2026 (fuente propia, no independiente)
- 360dialog, precios y planes (docs): https://docs.360dialog.com/docs/360dialog/prices-plans-and-payment-options (sin markup sobre Meta; mensajes de sesión gratis)
- Gupshup, aviso de cambio: https://support.gupshup.io/hc/en-us/articles/53700207494169-Gupshup-fee-changes-to-Cloud-API-marketing-w-e-f-1st-Jan-2026 (+6 % marketing desde 1-ene-2026)
- Twilio: https://landbot.io/blog/twilio-whatsapp-pricing (+0,005/msg; tercero)
- Bird, verificación Meta: https://docs.bird.com/applications/channels/channels/supported-channels/whatsapp/concepts/accounts-and-verification-levels/meta-business-account-verification-for-whatsapp (solo título leído)
- Chatwoot, canal WhatsApp: https://chatwoot.com/docs/product/channels/whatsapp/twilio (sección Cloud, vía búsqueda)
- Meta, límites de mensajería (secundaria): https://learn.doubletick.io/whatsapp-business-api/messaging-limits-in-whatsapp-api
- Meta, verificación (secundaria): https://help.chatdaddy.tech/article/how-to-verify-your-business-on-meta-required-for-official-whatsapp-business-api
- Telegram, webhooks y límites (secundaria): https://airbyte.com/data-engineering-resources/telegram-webhooks · https://rollout.com/integration-guides/telegram/api-essentials
- Ley 29733, texto de referencia (secundaria): https://lpderecho.pe/ley-proteccion-datos-personales-ley-29733-actualizada/

**Fuentes del repo (internas):**
- `program/02_REFERENCE/meta-pricing.md` (tarifas Perú, reglas de templates, cambios 1-oct-2026)
- `program/03_ARCHITECTURE/decisions/ADR-003-whatsapp-cloud-api.md`
- `program/03_ARCHITECTURE/decisions/ADR-011-canal-agnostico.md`
- `tools/asignaciones/cost_scenarios.py` (cálculo de la sección 5)
