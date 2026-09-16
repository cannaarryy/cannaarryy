# README-ASSETS.md — Sistema visual del perfil (`cannaarryy`)

7 SVG hechos a medida, un solo sistema de diseño. Sin JavaScript, sin
recursos externos, sin CSS externo. Funcionan como `<img>` en GitHub
(incluida la animación de cursor: SMIL declarativo, degrada a estático).

## Sistema de diseño compartido

| Elemento | Valor |
|---|---|
| Fondos | `#0A0A0A` (base), `#0D0D0D` (paneles), `#111111` (inputs) |
| Bordes | `#222222`, `#333333` (pills) |
| Texto | `#FFFFFF` (títulos), `#F5F5F5` (contenido), `#8A8A8A` (muted) |
| Acento único | `#38BDF8` (cyan: prompts, estados, nodos) |
| Tipografía | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` |
| Formato | `viewBox` + `width/height` fijos (1200 base) — GitHub los escala con `max-width:100%` |
| Accesibilidad | Cada SVG lleva `<title>` + `<desc>`; el README añade `alt` bilingüe |

## Archivos

### 1. `assets/hero.svg` (1200×560) — Cabecera
Nombre, rol, 4 líneas de terminal (`whoami`, `education`, `building`,
`focus`), cursor con blink, barra de estado (`SYSTEM ONLINE · BUILD 2026 · v2.0`)
y pill decorativa `ES / EN` (el toggle real está en el Markdown, debajo).
**Editar:** textos en etiquetas `<text>` (nombre, rol, outputs).

### 2. `assets/terminal.svg` (1200×420) — Perfil en terminal
Sesión `bash — profile.sh` con 6 comandos y salidas universales
(sin idioma). Va en la sección TERMINAL.
**Editar:** comandos y salidas en `<text>`.

### 3. `assets/system-status.svg` (1200×430) — Dashboard 2×2
Tarjetas EDUCATION / BUILDING / FOCUS / STATUS con textos
bilingües inline (`DAW · 2º YEAR`, `ClientFlow [active_project]`…).
**Editar:** cambia `ClientFlow` o el estado cuando evolucionen.

### 4. `assets/stats-frame.svg` (1200×150) — Marco de actividad
Cabecera de sección, SIN números (prohibido hardcodear stats).
Los datos reales viven en `generated/overview.svg` y
`generated/languages.svg` (GitHub Action diaria). No tocar.

### 5. `assets/debug-developer.svg` (1200×430) — Easter egg
Consola `SYS_ERROR // DEVELOPER_NOT_FOUND` con las 4 opciones.
No ejecuta nada: en el README va envuelta en `<a>` hacia
`issues/new` y las opciones enlazan a anchors internos.
**Editar:** textos de opciones (mantén `[1]`–`[4]`).

### 6. `assets/section-divider.svg` (1200×24) — Separador
Regla con degradado + nodo central de acento. Reutilizado entre
secciones. `alt=""` (decorativo).

### 7. `assets/footer.svg` (1200×140) — Cierre
Filosofía bilingüe + metadata (`cannaarryy · 2026 · v2.0`).
El `©` legal vive como texto en el README (seleccionable).

## Mantenimiento

- **Textos:** busca el `<text>` correspondiente y edítalo. Respeta los
  anchos (fuente monoespaciada ≈ 0.6× el tamaño por carácter).
- **Acento:** buscar/reemplazar `#38BDF8`. Para quitarlo: `#8A8A8A`.
- **Añadir sección:** reutiliza `section-divider.svg`; no crees divisores nuevos.
- **No hacer:** filtros pesados, fuentes externas, `<script>`, links
  dentro del SVG (en GitHub se renderiza como imagen sin interacción).

## GIFs animados (nativos en GitHub, sin JS)

Generados con `assets/make_gifs.py` (Pillow + Consolas del sistema).
Solo 2 archivos: calidad sobre cantidad.

| Archivo | Tamaño | Duración | Función |
|---|---|---|---|
| `boot.gif` | 880×330 · ~94 KB · 34 frames @10fps | ~3.4 s loop | Secuencia de arranque tras el hero (`boot profile`, 6× `[ OK ]`, barra, `SYSTEM ONLINE`) |
| `online.gif` | 32×32 · ~1 KB · 8 frames | loop | Punto de estado pulsante (fondo transparente). Reutilizado en ClientFlow y footer |

Reglas: 2–6 s, loop infinito, paleta del perfil, texto Consolas.
Para regenerar: `python assets/make_gifs.py`. No añadir más GIFs
sin eliminar antes algo (presupuesto: <150 KB en animación).
