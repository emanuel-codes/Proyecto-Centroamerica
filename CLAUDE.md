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
- Páginas: Sell out, Inventario, Abasto, Control y Revisión de datos (oculta).

## Reglas críticas
1. **Un solo lugar de cambios.** Hasta ahora el proyecto se generaba completo con `analisis/herramientas/crear_pbip.py`, en una sesión de Claude en la nube.
   - **No ejecutes ese script:** borra y reescribe las carpetas del proyecto, y se perdería todo lo cambiado en Power BI Desktop o por MCP.
   - Si en la sesión local se hacen cambios al modelo o al reporte, **avísale a Manuel**: desde ese momento la copia local es la principal. Tampoco hay que volver a extraer encima un ZIP de GitHub, porque reemplazaría los archivos.
2. **Cambios de modelo por MCP** (`powerbi-modeling`, conectado a la instancia abierta de Desktop). Quedan en memoria hasta que Manuel guarda con Ctrl+S.
   - Si se cambian el modelo y el reporte a la vez: primero MCP, Manuel guarda, recién ahí se editan los `visual.json`, y Manuel usa «Aplicar cambios externos».
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

## Cifras validadas (datos al 29/09/2026 Walmart y 28/09/2026 Amazon)
Cuadran al peso contra los archivos:

| Qué | Valor |
|---|---|
| Sell out, «Mes actual» (septiembre 2026) | $335,146 y 1,982 piezas |
| Sell out Walmart, septiembre 2026 | $275,034 y 1,290 piezas |
| Sell out Amazon, septiembre 2026 | $60,112 y 692 piezas |
| Inventario | 30,479 piezas |
| Fill rate | 93.6 % |
| Pedidos planeados (Recship) | 552 piezas y $70,174 |

Después de cualquier cambio, comprobar que estas cifras no se muevan, salvo que haya datos nuevos. El procedimiento está en `GUIA_VALIDACION.md`.

## Pendientes
- **Sell in e inventario del ERP One Goal:** faltan las muestras (acceso en trámite).
- **Definiciones «Por decidir»:** año anterior de Amazon, cobertura y umbrales, tipo de cambio, productos nuevos («Sin rotación»).
- **Maestro:** validar la hoja Pendientes con el cliente.
- **Entrega:** ver `PLAN_ENTREGA.md` (OneDrive o SharePoint de la empresa, Power BI Service y manual en PDF).

## Git
- Repositorio privado `github.com/emanuel-codes/Proyecto-Centroamerica`, rama `claude/confident-dijkstra-apgh2d`.
- Manuel trabaja con la carpeta extraída del ZIP de esa rama, **que no es un clon de Git**. Para subir cambios desde la sesión local, primero hay que clonar el repositorio y explicarle cada paso.
