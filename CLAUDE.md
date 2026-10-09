# Proyecto Power BI — Reporte Wellpro (sell out Walmart y Amazon México)

Responsable: Manuel Palacios, analista contratado para rehacer el reporte «Análisis de Ventas Wellpro» (cliente VISION MEDICA S.A). Idioma: español. Manuel no conoce Git: explicar cada paso en términos sencillos y confirmar antes de hacer commit o push.

## Lee primero
- `README.md`: índice del repositorio.
- `MANUAL_OPERACION.md`: rutina de carga y mantenimiento.
- `powerbi/LEEME.md`: cómo está armado el modelo y las cifras esperadas.
- `DEFINICIONES_INDICADORES.md`: definición de cada indicador; las marcadas «Por decidir» están pendientes de aprobar.
- `ERRORES_REPORTE_ACTUAL.md` y `DIAGNOSTICO_REPORTE_ACTUAL.md`: errores del reporte anterior.

## Estructura
- Proyecto PBIP: `powerbi/Reporte Wellpro.pbip`. Modelo en TMDL (`Reporte Wellpro.SemanticModel/definition`) y reporte en PBIR (`Reporte Wellpro.Report/definition`).
- Datos: carpeta `Nueva versión/`, con las descargas tal como salen de Retail Link y Amazon, más `Maestros/Maestro_Wellpro.xlsx`. El parámetro `RutaDatos` apunta a esa carpeta en la computadora de Manuel y tiene que terminar en `\`.
- Páginas: Sell out (panel ejecutivo), Inventario (semáforo y prioridades), Abasto, Control y Revisión de datos. **Control y Revisión de datos están ocultas** (`"visibility": "HiddenInViewMode"`): el jefe no las ve; los analistas las abren desde las pestañas de Power BI Desktop.
- Maquetas de diseño de Sell out e Inventario (opciones A y B): https://claude.ai/artifact/5SBPrEgaZWJ8CRDzcqZmmy. En las dos páginas se implementó la opción A.

## Reglas críticas
1. **Un solo lugar de cambios.** Hasta ahora el proyecto se generaba completo con `analisis/herramientas/crear_pbip.py`, en una sesión de Claude en la nube.
   - **No ejecutes ese script:** borra y reescribe las carpetas del proyecto, y se perdería todo lo cambiado en Power BI Desktop o por MCP.
   - **Desde el 3/10/2026 la copia local de Manuel es la principal** (rediseño de Sell out e Inventario hecho en la sesión local). No hay que volver a extraer encima un ZIP de GitHub, porque reemplazaría los archivos.
2. **Cambios de modelo por MCP** (`powerbi-modeling`, conectado a la instancia abierta de Desktop). Quedan en memoria hasta que Manuel guarda con Ctrl+S.
   - Si se cambian el modelo y el reporte a la vez, el orden es: cambios por MCP → Manuel guarda con Ctrl+S → se editan los `visual.json` → `powerbi-desktop reload`. Si Manuel guarda **después** de editar los `visual.json`, Desktop los sobrescribe con su versión en memoria; si se recarga **antes** de que guarde, se pierden los cambios por MCP.
   - Antes de editar archivos o recargar, comprobar con `powerbi-desktop status` que `hasUnsavedChanges` sea `false`. Ojo: después de `powerbi-desktop reload` queda en `true` aunque no haya cambios; hay que pedir Ctrl+S antes de la siguiente ronda.
   - Un cambio por MCP no aparece en `powerbi-desktop screenshot` hasta guardar y recargar. Para revisar el resultado antes, usar una consulta DAX.
   - Validar el reporte con `powerbi-report-author validate`. El error `PBIR_THEME_FILE_NAME_MISMATCH` y los avisos de alto de los filtros ya existían: el tema carga bien y los filtros se ven completos.
3. **No actualizar datos por MCP/XMLA.** La actualización la hace Manuel con Inicio → Actualizar; tarda unos 4 minutos.
4. **Formato dinámico de medidas:** la línea `formatStringDefinition = ...` va **al final de la medida** en el TMDL. En medio rompe la apertura del proyecto. Por MCP, usar `formatStringExpression`.
5. **Las descargas no se editan ni se renombran.** Lo único que se edita a mano es el maestro; no se cambian los nombres de sus hojas, tablas ni columnas.
6. **Consultas DAX por MCP:** como máximo 100 filas.

## Decisiones de diseño que NO hay que «corregir» (están probadas)
- **`fnZipArchivo`, `fnColumnaExacta` y `fnXmlTexto` leen el XML del .xlsx directamente.** Retail Link guarda POS Sales con formato de moneda sin decimales, y `Excel.Workbook` lo entrega como texto redondeado («$109» en lugar de 108.62); se comprobó en Desktop. El monto exacto solo se usa si, redondeado al peso, coincide con el de Excel. Si no se puede leer, Control muestra «🟡 Montos de Walmart sin decimales».
- **`fnRetailLink` lee las opciones del reporte** (nombre, solicitud y rango) del principio del XML. Abrir la hoja con Excel para eso hacía la actualización muy lenta.
- **`Table.Buffer` antes de cada `Table.FromColumns`:** sin él, cada columna vuelve a evaluar la consulta completa. Eso era lento, y podía desalinear filas.
- **Sin duplicados:**
  - Walmart sell out: cada día se toma de un solo archivo, el de la solicitud más reciente (`WM_SellOut_Archivos`).
  - Amazon: un archivo por mes, el que llega más lejos.
  - Inventarios: una foto por día y, de cada mes, la última.
  - Fill rate: cada orden, de la descarga más reciente.
  - Recship: solo el archivo más reciente.
  - La subcarpeta `Respaldo` no se lee.
- **Calendario:** `Meses_atras` y `Periodo` se recalculan con el último día de sell out. El filtro guardado en «Mes actual» nunca se desactualiza.
- **Año anterior:** son los mismos días, por cadena. En el mes en curso de Amazon (que viene por mes) se toma en proporción a los días cubiertos. El crecimiento solo compara cadenas que tienen historial.
- **dimTienda sale de las fotos de inventario**, no del sell out, para no leer el sell out dos veces.
- **Sin tarjeta de precio promedio por pieza:** el promedio se mueve por la mezcla de productos y no por el precio (en octubre de 2026 bajaba 39 % aunque los precios subieron). Se cambió por «Inventario en cadenas».
- **«Atender primero» se ordena con la medida `Estado por urgencia`**: un número que ordena por urgencia y que, con formato dinámico, se muestra como el texto del estado (columna alineada a la izquierda). Un `RANKX` con `ALLSELECTED` daba bien en DAX, pero dentro de la tabla calculaba el lugar por separado para cada cadena.
- **Tarjetas `cardVisual`:** la etiqueta de referencia y su detalle usan el mismo `selector` (`dataViewWildcard` + `metadata` de la medida + `id`); el monto va sin unidades y con 2 decimales.

## Cifras validadas (datos al 07/10/2026 Walmart y 06/10/2026 Amazon)
Las dos descargas nuevas de Walmart se sumaron directo del archivo y cuadran al centavo:

| Qué | Valor |
|---|---|
| Sell out, «Mes actual» (octubre 2026) | $88,971.48 y 447 piezas |
| Sell out Walmart, del 1 al 7/10 | $76,000.15 y 324 piezas |
| Sell out Amazon, del 1 al 6/10 | $12,971.33 y 123 piezas |
| Sell out septiembre 2026 cerrado | Walmart $289,177.48 y 1,355 piezas · Amazon $67,898.91 y 757 piezas |
| Inventario | 31,550 piezas (Walmart 28,513 · Amazon 3,037), 16.7 meses de cobertura |
| Fill rate | 95.4 % (16,749 de 17,548 piezas) |
| Pedidos planeados (Recship del 09/10) | 66 piezas y $33,396.30 |

Después de cualquier cambio, comprobar que estas cifras no se muevan, salvo que haya datos nuevos. El procedimiento está en `GUIA_VALIDACION.md`; el detalle, en `powerbi/LEEME.md`.

## Pendientes
- **Sell in e inventario del ERP One Goal:** faltan las muestras (acceso en trámite).
- **Definiciones «Por decidir»:** año anterior de Amazon en el mes en curso (proporción, esperar al cierre o mismos días exactos), cobertura y umbrales (¿iguales para las dos cadenas?; con la regla anterior de Amazon, de 2 a 6 meses, sus 4.8 meses serían «Saludable»), tipo de cambio, productos nuevos («Sin rotación»). Manuel las lleva al jefe; las respuestas se anotan en `DEFINICIONES_INDICADORES.md` y después se ajusta el modelo.
- **Página Abasto** con el mismo estilo que Sell out e Inventario.
- **Arreglos del modelo de la auditoría del 2/10 (sin aprobar):** que el archivo de Amazon tenga que empezar el día 1 (un archivo parcial reemplaza el mes sin aviso), alerta en Control si el fill rate o el Recship están viejos, duplicados en Equivalencias, comprobar el nombre del reporte de Retail Link y el nombre exacto del maestro.
- **Limpieza del modelo:** 6 medidas del precio promedio quedaron sin uso, igual que las de las tarjetas viejas de Inventario (`Productos con sobre stock`, etc.). No estorban; borrarlas solo con el visto bueno de Manuel.
- **Maestro:** validar la hoja Pendientes con el cliente.
- **Entrega:** ver `PLAN_ENTREGA.md` (OneDrive o SharePoint de la empresa, Power BI Service y manual en PDF).

## Git
- Repositorio privado `github.com/emanuel-codes/Proyecto-Centroamerica`, rama `claude/confident-dijkstra-apgh2d`.
- La carpeta de trabajo de Manuel (en OneDrive) **no es un clon de Git**. Para subir cambios hay un clon en `C:\Users\mpalacios\gitpc`, con `core.longpaths` y `core.autocrlf` activados (las rutas del reporte son muy largas para la carpeta temporal).
- Cómo subir: copiar la carpeta de trabajo al clon con `robocopy /MIR`, **sin** `Nueva versión`, `.git`, `.claude` ni los `.pbi/cache.abf`; revisar `git status`; descartar los archivos que solo cambian en el salto de línea final (Power BI lo quita al guardar); hacer commit y push. En PowerShell 5.1 el mensaje va en un archivo: `git commit -F mensaje.txt`. Explicarle cada paso a Manuel y confirmar antes del commit y del push.
- **Datos:** los archivos de `Nueva versión` (ventas del cliente) no se suben desde la sesión de Claude: el sistema de permisos lo bloquea. Si Manuel los quiere en GitHub, los sube él. En GitHub están los datos al 2/10/2026.
