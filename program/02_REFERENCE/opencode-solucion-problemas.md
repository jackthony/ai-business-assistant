# OpenCode en Windows: guía de solución de problemas

> Para practicantes del programa HealthTech Software & AI (SENATI 2026). Úsala cuando OpenCode no responde, carga sin fin o muestra un error.
>
> - **Fuentes revisadas el 2026-10-13.** Cada afirmación lleva su enlace. Lo que no está confirmado en la documentación oficial o en reportes verificables va marcado **no confirmado**.
> - Los reportes de GitHub que no son del mantenedor van marcados **reporte de usuario (no oficial)**.
> - Esta guía no se probó en un PC del aula. Describe lo documentado.
> - Si un paso pide algo que no está aquí, pregunta en el grupo antes de hacerlo.

## Antes de empezar: tres reglas

1. **No pegues secretos.** Claves API, tokens, cabeceras de autorización, prompts, contenido de archivos y el contenido de `auth.json` no van al Issue, al repo ni al chat. La doc v2 pide quitarlos de cualquier reporte ([troubleshooting v2](https://opencode.ai/v2/docs/troubleshooting/)). La carpeta de datos de v1 contiene `auth.json`, con claves y tokens ([troubleshooting v1](https://opencode.ai/docs/troubleshooting/)).
2. **Copia antes de borrar.** Cualquier carpeta de OpenCode que vayas a borrar o renombrar, cópiala primero a otro sitio. La doc v2 advierte de no borrar ni editar archivos de servicio ni la base de datos mientras diagnosticas ([troubleshooting v2](https://opencode.ai/v2/docs/troubleshooting/)). Criterio de esta guía: cuando un paso dice "borrar", envía la carpeta a la Papelera de reciclaje y no la vacíes hasta confirmar que todo funciona.
3. **Sin datos reales y sin gastos.** No pegues datos reales de clientas en modelos gratis. El aviso de Nemotron pide no enviar datos personales ni confidenciales, y durante su periodo gratis Big Pickle puede usar lo recogido para mejorar el modelo ([Zen](https://opencode.ai/docs/zen/)). OpenCode Go es una suscripción mensual de pago ([Zen](https://opencode.ai/docs/zen/)). Que el prefijo `opencode-go/` de algunos modelos corresponda a esa suscripción es **no confirmado** en la doc. No actives planes ni compres créditos sin aprobación del monitor.

## Paso 0. Identifica la versión

Ejecuta en la terminal:

```
opencode --version
```

- Resultado `1.x`: OpenCode 1 (v1). Resultado `2.x`: OpenCode 2 (v2).
- La doc v2 pide incluir este comando en los reportes ([troubleshooting v2](https://opencode.ai/v2/docs/troubleshooting/)). Que funcione igual en v1: **no confirmado**, porque las páginas v1 revisadas no lo documentan.
- Por qué importa: rutas, claves de config y comandos cambian entre versiones. Por ejemplo, la clave de proveedor se llama `provider` en v1 y `providers` en v2 ([config v2](https://opencode.ai/v2/docs/config/)).
- OpenCode 2 ya salió. El mantenedor cerró como "not planned" los issues contra v1 porque el desarrollo se centra en v2 ([#31119](https://github.com/anomalyco/opencode/issues/31119)). Por eso muchos issues de v1 se cierran sin fix.
- Dos instalaciones pueden chocar: los métodos de instalación de v1 pueden entrar en conflicto con una instalación de v2 o reemplazarla ([docs](https://opencode.ai/docs/)). Ten una sola.

Anota también cómo lo usas:

- **TUI en la terminal** (la interfaz normal): esta guía aplica completa.
- **`opencode run`**: hay reportes de que se queda sin salida ([#38723](https://github.com/anomalyco/opencode/issues/38723), [#49030](https://github.com/anomalyco/opencode/issues/49030)). **Reporte de usuario (no oficial).**
- **App de escritorio**: ver Paso 8.

### Qué síntoma tienes

| Síntoma | Pasos |
|---|---|
| Carga sin fin o sin respuesta | 1, 2, 3 |
| Error `429 FreeUsageLimitError` | 1 |
| Error `503 Endpoint is unavailable` | 1 |
| `ProviderInitError` en el log | 2, 7 |
| `AI_APICallError` | 2, 5 |
| `Event stream stalled` en el log | 2, 1, 3 (el 8 solo como alternativa) |
| "Restarting service" en bucle | 3, 8 |
| Enter o Shift+Tab no responden (v2, reporte) | 4 |
| `no such column: name` tras actualizar | 6 |
| Sesión que se reinicia sin respuesta (CLI o escritorio) | 2, 8 |
| Ventana en blanco (app de escritorio) | 8 |

## Orden de los pasos (de más barato a más costoso)

| Paso | Qué haces | Coste | ¿Puedes perder algo? |
|---|---|---|---|
| 0 | Ver versión y tipo de uso | nulo | no |
| 1 | Cambiar de modelo; entender los timeouts | bajo | no |
| 2 | Leer el log | bajo | no |
| 3 | Revisar proxy y red | bajo | no |
| 4 | Revisar config del proyecto y plugins | medio | sí, si editas sin copia |
| 5 | Limpiar la caché | medio | no documentado (va a la Papelera) |
| 6 | Actualizar | alto | sí: la base de datos (copia antes) |
| 7 | Borrar la carpeta de datos | alto | puedes perder credenciales guardadas (no confirmado) |
| 8 | WSL2 o app de escritorio | muy alto | no borra nada, pero la config y las sesiones de WSL quedan separadas |

## Paso 1. Cambia de modelo y entiende los timeouts (coste bajo)

Úsalo si el modelo da error 429 o 503, o si no responde.

- **Tiempos de espera.** La doc de config (v1) lista timeouts por proveedor ([config](https://opencode.ai/docs/config/)):
  - `timeout`, 300000 ms: tiempo máximo de la solicitud.
  - `headerTimeout`, 300000 ms: espera de las cabeceras; se detiene al llegar y no limita el cuerpo.
  - `chunkTimeout`, 900000 ms: si no llega ningún fragmento a tiempo, la solicitud se aborta.
  - Cada uno se desactiva con `false`. La doc no dice si esos son los valores por defecto: **no confirmado**.
  - No hay atajo documentado para cancelar una solicitud en curso ([TUI](https://opencode.ai/docs/tui/)).
- **Ver y elegir modelo.** En la TUI escribe `/models`, o pulsa Ctrl+X y después M ([TUI](https://opencode.ai/docs/tui/)). La tecla líder Ctrl+X espera 2000 ms por defecto. Desde la terminal, `opencode models` lista los modelos como `provider/model`, y `opencode models --refresh` actualiza la lista desde models.dev ([CLI](https://opencode.ai/docs/cli/)).
- **Qué modelo arranca.** El orden es: flag `--model` o `-m`, después la clave `model` de la config, después el último modelo usado y, por último, uno interno ([models](https://opencode.ai/docs/models/)). Si la config fija un modelo que falla, cambiarlo en la TUI puede no bastar. Revisa la config (Paso 4).
- **429 `FreeUsageLimitError`.** Es un límite de uso de un modelo gratis. Un reporte describe que algunos modelos gratis respondían y otros daban 429 desde la misma IP al mismo tiempo ([#42977](https://github.com/anomalyco/opencode/issues/42977), **reporte de usuario (no oficial)**). Prueba otro modelo gratis. La doc no publica límites ni horas de reinicio ([Zen](https://opencode.ai/docs/zen/)).
- **Respuesta lenta tras un 429.** Un reporte dice que el agente de títulos reintenta tres veces (unos 90 s) y bloquea la respuesta principal si comparten hilo ([#31042](https://github.com/anomalyco/opencode/issues/31042), **reporte de usuario (no oficial)**). El mismo reporte dice que `small_model` se ignora. Que `small_model` evite el problema: **no confirmado**.
- **503 `Endpoint is unavailable`.** Un reporte en Windows lo vio con un modelo `opencode-go/...`, con reintentos silenciosos cada unos 7 s ([#49030](https://github.com/anomalyco/opencode/issues/49030), **reporte de usuario (no oficial)**). Cambia de modelo. **No** pases a modelos `opencode-go/...` como solución: OpenCode Go es de pago y el prefijo no está confirmado en la doc.
- **Disponibilidad de los modelos gratis.** La doc los presenta como gratis "for a limited time", sin fechas ([Zen](https://opencode.ai/docs/zen/)). Si siguen disponibles hoy: **no confirmado**.

## Paso 2. Lee el log (coste bajo)

- **Windows (v1).** Pulsa WIN+R, pega `%USERPROFILE%\.local\share\opencode\log` y pulsa Enter. Los archivos llevan fecha y hora, y se conservan los 10 más recientes ([troubleshooting](https://opencode.ai/docs/troubleshooting/)).
- **v2.** `opencode debug paths log` imprime la ruta exacta ([CLI v2](https://opencode.ai/v2/docs/cli/)). La ruta de los logs en Windows para v2 no está documentada: **no confirmado**.
- **Más detalle en la terminal.** `opencode --print-logs` manda los logs a la salida de error (stderr). `opencode --log-level DEBUG` sube el nivel; los valores son DEBUG, INFO, WARN y ERROR ([CLI](https://opencode.ai/docs/cli/)). El nivel por defecto y un comando para seguir el log en vivo no están documentados: **no confirmado**.
- **Qué buscar** (son nombres que aparecen en la doc o en reportes):
  - `ProviderInitError`: la doc lo asocia "probablemente" con una configuración inválida o corrupta. Ve al Paso 7 ([troubleshooting](https://opencode.ai/docs/troubleshooting/)).
  - `AI_APICallError`: la doc lo asocia a paquetes de proveedor desactualizados. Ve al Paso 5 ([troubleshooting](https://opencode.ai/docs/troubleshooting/)).
  - `FreeUsageLimitError` o 429: Paso 1.
  - `Event stream stalled`: un reporte describe un watchdog de 45 s en la CLI de Windows ([#52049](https://github.com/anomalyco/opencode/issues/52049), **reporte de usuario (no oficial)**; causa **no confirmada**). Ve a los Pasos 1 y 3. El Paso 8 solo como alternativa.

## Paso 3. Revisa proxy y red (coste bajo)

Hazlo solo si tu equipo o tu red usa proxy.

- OpenCode respeta `HTTPS_PROXY`, `HTTP_PROXY` y `NO_PROXY`. Con proxy hay que excluir el servidor local: la doc de red marca `NO_PROXY=localhost,127.0.0.1` como necesario ([network](https://opencode.ai/docs/network/)). Ese ejemplo usa sintaxis de bash. Cómo definir variables de entorno en Windows no está documentado en las fuentes revisadas: **no confirmado**. Pide ayuda al monitor para hacerlo en el equipo.
- Si hay proxy y no se excluye el loopback, un reporte describe la TUI con "Restarting service" en bucle ([#52054](https://github.com/anomalyco/opencode/issues/52054), **reporte de usuario (no oficial)**). El mismo reporte sugiere añadir `::1` a `NO_PROXY`. Sin fix confirmado.
- Certificados corporativos: `NODE_EXTRA_CA_CERTS` apunta a un archivo de CA personalizado ([network](https://opencode.ai/docs/network/)).

## Paso 4. Revisa la config del proyecto y los plugins (coste medio)

Antes de editar cualquier archivo, copia el original.

- La config va en `opencode.json` u `opencode.jsonc` en la raíz del proyecto. JSONC admite comentarios. Se busca hasta el directorio Git más cercano, y las configs se **fusionan** en lugar de reemplazarse ([config](https://opencode.ai/docs/config/)).
- **La ruta de la config global en Windows se contradice entre páginas.** La troubleshooting da `%USERPROFILE%\.config\opencode\opencode.jsonc`. La página de config da `~/.config/opencode/opencode.json` y no da ruta de Windows ([troubleshooting](https://opencode.ai/docs/troubleshooting/), [config](https://opencode.ai/docs/config/)). Cuál aplica: **no confirmado**. No edites la global sin el monitor; revisa la del proyecto.
- Claves que más influyen: `model` (formato `provider_id/model_id`), `small_model` (modelo ligero para tareas como los títulos), `enabled_providers` y `disabled_providers`. `disabled_providers` tiene prioridad sobre `enabled_providers` ([config](https://opencode.ai/docs/config/)).
- **Plugins.** La clave `plugin` admite una lista de nombres de plugins npm ([config](https://opencode.ai/docs/config/)). Un reporte en v2 dice que Enter y Shift+Tab dejaron de responder, con sospecha de plugins de v1 ([#55162](https://github.com/anomalyco/opencode/issues/55162), **reporte de usuario (no oficial)**; causa **no confirmada**). Si lo quieres probar, quita los plugins de uno en uno, anota cuál es y restaura el resto. Avisa al monitor antes.
- `snapshot: false` desactiva los snapshots y, con ellos, el rollback de cambios del agente desde la interfaz ([config](https://opencode.ai/docs/config/)). Algunos usuarios lo usan como workaround en #52049 (**reporte de usuario, no oficial**). No lo cambies sin aprobación del monitor.
- Si tienes un `.git` suelto en tu carpeta de usuario (`%USERPROFILE%`), un reporte lo relaciona con sesiones que se cortan. Causa **no confirmada** ([#52049](https://github.com/anomalyco/opencode/issues/52049)). **No lo borres**: puede contener historial de Git. Avisa al monitor.

## Paso 5. Limpia la caché (coste medio)

Para `AI_APICallError`, la doc indica borrar la caché y reiniciar OpenCode, para que reinstale los paquetes del proveedor ([troubleshooting](https://opencode.ai/docs/troubleshooting/)).

1. Cierra OpenCode.
2. Pulsa WIN+R y pega `%USERPROFILE%\.cache\opencode`.
3. Envía esa carpeta a la Papelera de reciclaje. No la vacíes todavía. La doc no detalla qué guarda la caché (**no confirmado**), por eso no se borra a secas.
4. Abre OpenCode de nuevo.

## Paso 6. Actualiza OpenCode (coste alto; copia antes)

1. **Copia la carpeta de datos** `%USERPROFILE%\.local\share\opencode` a otra carpeta. Un reporte en Windows 11 con v1.16.2 describe un arranque fatal con el error `no such column: name` después de actualizar. El issue se cerró como "not planned" sin causa confirmada ([#31119](https://github.com/anomalyco/opencode/issues/31119)). Hay workarounds de usuarios que borran `opencode.db` y pierden el historial ([#31119](https://github.com/anomalyco/opencode/issues/31119), **reporte de usuario, no oficial**). No los hagas sin el monitor.
2. **Actualiza.**
   - `opencode upgrade` actualiza a la última versión. `--method` (`-m`) acepta `curl`, `npm`, `pnpm`, `bun` o `brew` ([CLI](https://opencode.ai/docs/cli/)). `choco` y `scoop` no aparecen en esa lista. El método por defecto no está documentado: **no confirmado**.
   - En la TUI, `/update` instala actualizaciones o pasa a OpenCode 2. Las actualizaciones ya no se instalan solas ([notas de v1.19.0](https://github.com/anomalyco/opencode/releases/tag/v1.19.0)).
3. **Para pasar a OpenCode 2.** Las notas oficiales de v1.19.0 indican `opencode upgrade --major` ([notas de v1.19.0](https://github.com/anomalyco/opencode/releases/tag/v1.19.0)). La página de CLI v1 no documenta `--major` ([CLI](https://opencode.ai/docs/cli/)). **Confirma el comando con el monitor antes.** Después revisa la config: la clave pasa de `provider` a `providers` ([config v2](https://opencode.ai/v2/docs/config/)). Para Windows, la doc v2 ofrece un binario zip independiente y dice: "Windows package managers are not supported" ([v2](https://opencode.ai/v2/docs/)).
4. Comprueba la versión con `opencode --version` (Paso 0).

## Paso 7. Borra la carpeta de datos (coste alto; puedes perder credenciales)

Hazlo solo si el log muestra `ProviderInitError`, y con el monitor. La troubleshooting indica borrar la carpeta de datos y volver a autenticar con `/connect` ([troubleshooting](https://opencode.ai/docs/troubleshooting/)). La misma página dice que ese error suele deberse a una configuración inválida o corrupta.

1. Cierra OpenCode.
2. Copia `%USERPROFILE%\.local\share\opencode` a otra carpeta. No la compartas: contiene `auth.json` ([troubleshooting](https://opencode.ai/docs/troubleshooting/)).
3. Pulsa WIN+R, pega `%USERPROFILE%\.local\share\opencode` y envía la carpeta a la Papelera de reciclaje.
4. Abre OpenCode y ejecuta `/connect` para volver a configurar el proveedor. La clave la pegas en OpenCode, nunca en el chat ni en el Issue ([providers](https://opencode.ai/docs/providers/)).

**Sobre las credenciales.** La doc no dice que se pierdan al borrar la carpeta: **no confirmado**. Es probable, porque las credenciales de `/connect` se guardan en `~/.local/share/opencode/auth.json` ([providers](https://opencode.ai/docs/providers/)) y la doc sitúa `auth.json` en la carpeta de datos ([troubleshooting](https://opencode.ai/docs/troubleshooting/)). La ruta de Windows de esa carpeta no está escrita explícitamente; se deduce de la ruta de logs (`%USERPROFILE%\.local\share\opencode\log`). Si algo no se recupera, la copia del paso 2 es tu respaldo. No la borres hasta que OpenCode funcione.

## Paso 8. WSL2 o app de escritorio (coste muy alto)

### WSL2: la alternativa que recomienda la doc

La doc oficial recomienda WSL para usar OpenCode en Windows, por rendimiento del sistema de archivos, terminal completa y compatibilidad con herramientas ([WSL](https://opencode.ai/docs/windows-wsl)). Un reporte en Windows 11 indica que, en Ubuntu bajo WSL2 en la misma máquina, funciona cuando la app nativa falla ([#55220](https://github.com/anomalyco/opencode/issues/55220), **reporte de usuario (no oficial)**).

Pasos:

1. Instala WSL con la guía de Microsoft: [learn.microsoft.com/en-us/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install) (enlazada desde [WSL](https://opencode.ai/docs/windows-wsl)). Pide permiso al monitor antes de instalar nada. Los requisitos de tu PC (virtualización, espacio en disco, RAM) no están documentados en las fuentes revisadas: **no confirmado**.
2. Dentro de WSL, en su terminal bash y no en PowerShell, ejecuta `curl -fsSL https://opencode.ai/install | bash` ([WSL](https://opencode.ai/docs/windows-wsl)). Ese comando es la instalación de v1. La doc v2 lista `curl -fsSL https://opencode.ai/v2/install | bash` ([v2](https://opencode.ai/v2/docs/)). No instales las dos: ten una sola versión, la que acuerdes con el monitor.
3. Trabaja dentro del sistema de archivos de WSL, por ejemplo en `~/code/`. Las unidades de Windows aparecen como `/mnt/c/`, pero la doc recomienda clonar o copiar los repos dentro de WSL ([WSL](https://opencode.ai/docs/windows-wsl)).
4. La config y las sesiones quedan dentro de WSL, en `~/.local/share/opencode/` ([WSL](https://opencode.ai/docs/windows-wsl)). **No se comparten** con la instalación de Windows. Copiar la carpeta de Windows no sirve dentro de WSL.
5. Si usas la interfaz web (`opencode web --hostname 0.0.0.0`, desde la terminal de WSL): la doc advierte que `0.0.0.0` expone el servidor y recomienda `OPENCODE_SERVER_PASSWORD` ([WSL](https://opencode.ai/docs/windows-wsl)). En el aula, no lo uses sin contraseña.

### Reinstalar o desinstalar

- No hay comando documentado para reinstalar.
- `opencode uninstall` tiene las opciones `--keep-config` (`-c`), `--keep-data` (`-d`), `--dry-run` y `--force` (`-f`). La doc no dice qué borra por defecto: **no confirmado** ([CLI](https://opencode.ai/docs/cli/)). Usa `--dry-run` primero y pide permiso al monitor antes de quitar nada.

### App de escritorio en Windows

- Requiere Microsoft Edge WebView2 Runtime. Si abre en blanco o no inicia, instala o actualiza WebView2 ([troubleshooting](https://opencode.ai/docs/troubleshooting/)). Esto no aplica a la CLI.
- **Sesiones y servicios que se reinician en Windows.** Son reportes de usuario (no oficiales), sin causa confirmada:
  - [#55220](https://github.com/anomalyco/opencode/issues/55220), abierto el 13 oct 2026, con el título "bug(windows): CLI and Desktop repeatedly restart/expire sessions without AI responses; WSL2 works". Afecta a la CLI y al escritorio. Solo ha respondido un bot. Workaround reportado: WSL2 (arriba).
  - [#53849](https://github.com/anomalyco/opencode/issues/53849): app de escritorio v2. El servicio compartido se reinicia cada 66–82 s y termina las sesiones. El bot lo cerró como duplicado de #51216. Un usuario dice que `opencode run` funciona en ese caso: **no confirmado** por el mantenedor.
  - [#52049](https://github.com/anomalyco/opencode/issues/52049): es de la **CLI** (título "cli(win): 45s event-stream idle watchdog restarts the managed service, aborting all sessions/subagents"). Sigue abierto y sin comentarios del mantenedor. Ve a los Pasos 2 y 3.
- Con v2, `opencode --standalone` arranca un servidor privado, y `opencode --server http://localhost:4096` conecta a un servidor concreto ([CLI v2](https://opencode.ai/v2/docs/cli/)). Solo v2.
- Un reporte recomienda no usar la TUI mientras la app de escritorio está abierta ([#52049](https://github.com/anomalyco/opencode/issues/52049), **reporte de usuario, no oficial**).
- En v2, la troubleshooting documenta `opencode service status` y `opencode service restart`, pero la página de CLI v2 no los incluye: **no confirmado** en la ayuda de la CLI ([troubleshooting v2](https://opencode.ai/v2/docs/troubleshooting/)).
- Para el "Restarting service" en bucle (Paso 3), un workaround de usuarios es `opencode service set disabled true`. La CLI v2 lo documenta, y `opencode service unset disabled` lo deshace ([CLI v2](https://opencode.ai/v2/docs/cli/)). Desactiva el servicio compartido: pide permiso al monitor.

## Qué pegar en el Issue si no se arregla

Copia esta plantilla al Issue y rellénala. Quita lo que no aplique.

```markdown
**Versión de OpenCode:** (salida de `opencode --version`)
**Sistema operativo:** Windows 10 o Windows 11 (y la compilación, si la sabes)
**Cómo lo usas:** TUI en terminal / `opencode run` / app de escritorio / WSL2
**Modelo:** provider/model (indica si es gratis)
**Qué esperaba / qué pasó:**
**Pasos para repetirlo:** 1) ... 2) ...
**Alcance:** ¿pasa en todos los proyectos o en uno? ¿con todos los modelos o con uno?
**Pasos de la guía probados:** 0 a 8, con el resultado de cada uno
**Últimas líneas del log más reciente** (unas 30 o las que quepan; sin claves, tokens, prompts ni contenido de archivos):
(pegar aquí)
**Solo v2:** salida de `opencode service status` (no confirmado en la ayuda de la CLI)
```

- La doc v2 pide estos datos en un reporte: versión, salida de `opencode service status`, pasos para repetirlo, si afecta al servicio compartido, a un cliente o a un proyecto, y las líneas del log con los campos `run` y `role` ([troubleshooting v2](https://opencode.ai/v2/docs/troubleshooting/)).
- Quita de las rutas tu nombre de usuario de Windows antes de pegarlas. Criterio del curso; OpenCode no lo pide.
- Antes de reportar, busca si el problema ya existe en el repositorio oficial, [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode). Ejemplos: [#55220](https://github.com/anomalyco/opencode/issues/55220), [#52049](https://github.com/anomalyco/opencode/issues/52049), [#52054](https://github.com/anomalyco/opencode/issues/52054), [#53849](https://github.com/anomalyco/opencode/issues/53849) y [#49030](https://github.com/anomalyco/opencode/issues/49030).
- Si parece un bug de OpenCode, el monitor decide si se reporta en GitHub Issues ([troubleshooting v2](https://opencode.ai/v2/docs/troubleshooting/)).

## Alternativa de respaldo: DeepSeek web

Si OpenCode no funciona y necesitas seguir con tu Issue, usa las alternativas de [deepseek-local.md](deepseek-local.md):

1. Modelo chico en tu PC, según tu RAM. La lista está en ese archivo: con 8 GB de RAM o menos, `qwen2.5-coder:1.5b` o `deepseek-r1:1.5b`; con 16 GB, `qwen2.5-coder:3b` o `deepseek-r1:7b`.
2. **DeepSeek web** (chat.deepseek.com): gratis y sin API key ([deepseek-local.md](deepseek-local.md)).

Reglas para usarlo:

- Para dudas puntuales, no para reescribir el proyecto. El stack lo define así ([stack-versiones.md](stack-versiones.md)).
- Carga solo el Issue y 2 o 3 archivos de la tarea, no el repo completo ([deepseek-local.md](deepseek-local.md)).
- Pega el error y unas líneas del log, sin claves, sin `auth.json` y sin datos reales.
- Respeta el presupuesto de interacciones de [pack_contexto.md](../01_CURRICULUM/pack_contexto.md): unas 10 a 15 por sesión. Ver también [current_status.md](../00_PROJECT/current_status.md).

## Fuentes oficiales revisadas

- Documentación general: https://opencode.ai/docs/
- Troubleshooting v1: https://opencode.ai/docs/troubleshooting/
- Config: https://opencode.ai/docs/config/
- CLI: https://opencode.ai/docs/cli/
- Red y proxy: https://opencode.ai/docs/network/
- Proveedores: https://opencode.ai/docs/providers/
- WSL: https://opencode.ai/docs/windows-wsl
- Modelos, Zen y TUI: https://opencode.ai/docs/models/ · https://opencode.ai/docs/zen/ · https://opencode.ai/docs/tui/
- v2 (documentación, troubleshooting, CLI y config): https://opencode.ai/v2/docs/ · https://opencode.ai/v2/docs/troubleshooting/ · https://opencode.ai/v2/docs/cli/ · https://opencode.ai/v2/docs/config/
- Repositorio y notas de release: https://github.com/anomalyco/opencode · https://github.com/anomalyco/opencode/releases/tag/v1.19.0
