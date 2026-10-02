# Errores del reporte actual y cómo los evita la versión nueva

Resumen para presentar. El detalle y la forma de comprobar cada cifra están en [`DIAGNOSTICO_REPORTE_ACTUAL.md`](DIAGNOSTICO_REPORTE_ACTUAL.md).

> **Prueba de que el proceso nuevo funciona:** de octubre de 2024 a agosto de 2025, cuando el consolidado del reporte actual estaba bien armado, sus cifras de Walmart coinciden **al peso** con las descargas nuevas. Las diferencias empiezan cuando aparecen los días repetidos, faltantes o incompletos.

> **El mensaje principal:** los errores no son de la persona, son del proceso. El reporte exige copiar, pegar, renombrar y escribir reglas a mano todos los días. Así, cualquier analista se equivoca y nada avisa antes de enviar.

## Para mostrar en vivo (en piezas)

Compáralo en **piezas**: el reporte actual muestra el monto en dólares con tipo de cambio fijo de 20, y el nuevo en pesos.

| Qué | Mes | Reporte actual | Reporte nuevo | Diferencia | Causa |
|---|---|---|---|---|---|
| Walmart | Noviembre 2025 | 1,827 | **1,391** | +436 (+31 %) | Del 1 al 10 de noviembre se pegaron dos veces |
| Walmart | Septiembre 2025 | 1,429 | **1,701** | −272 (−16 %) | Los 30 días están incompletos. Además es el «año anterior» de septiembre 2026, así que el crecimiento actual sale inflado. |
| Amazon | Diciembre 2025 | 489 | **577** | −88 (−15 %) | El mes se armó a mano y solo llega al 27/12 |
| Walmart | Abril 2026 | 726 | **815** | −89 (−11 %) | Faltan el 14, el 27 y el 28 de abril |

En pesos: noviembre 2025 de Walmart, $825,629 contra $629,395; diciembre 2025 de Amazon, $56,792 contra $69,879.

**El filtro de fechas del reporte actual:** viene en «Último 9 Meses», contados por día desde hoy. Por eso enero empieza el día 3 y aparece una barra de «octubre» con solo 3 días del año anterior. Las tarjetas «Total Anterior» y «Total Actual» comparan periodos de distinto largo y arrastran los días faltantes:
- **Reporte actual:** 10,258 contra 10,270, es decir, Walmart va **igual que el año pasado** (+0.1 %).
- **Reporte nuevo:** con los datos completos y los mismos días (del 1 de enero al 29 de septiembre), son 10,467 contra 11,046, es decir, **+5.5 %**. Para verlo: Mes = de Ene 2026 a «Mes actual» (con Ctrl) y Cadena = Walmart; la tarjeta «Piezas vs año anterior» da ▲ 5.5 %.
- **Para ver 2025 en el reporte actual:** cambia el filtro a «Último 13 Meses (calendario)». Muestra de septiembre 2025 a septiembre 2026, con meses completos.

Las cifras del reporte actual salen del respaldo del 21/09/2026.

## 1. Errores en las cifras

Todos se comprobaron con los datos que tenía cargados el reporte (21/09/2026) o con descargas nuevas.

| # | Qué pasa | Impacto | Causa | Cómo lo evita la versión nueva |
|---|---|---|---|---|
| 1 | Sell out de Walmart con días pegados dos veces, días que nunca se pegaron y días incompletos | Comprobado contra la descarga completa de octubre de 2024 a septiembre de 2026:<br>• **203,270 MXN contados dos veces** (del 1 al 10 de noviembre de 2025 y el 27 y 30 de agosto de 2026).<br>• **14 días sin datos**: faltan 191,566 MXN.<br>• **120 días incompletos**, entre ellos todo septiembre de 2025: faltan 129,981 MXN.<br>Por mes, el error llega a **+31 %** en noviembre de 2025 y a **−8.6 %** en enero de 2026. | Consolidado manual: cada día se pega en un Excel de 315 mil filas | Lee las descargas directo de la carpeta. Cada día se toma de un solo archivo. Si falta un día, Control se pone en 🔴. |
| 2 | Amazon noviembre y diciembre de 2025 incompletos | **Faltan 112 piezas y 16,928 MXN.** Diciembre solo llega al día 27. | Desde noviembre de 2025, el mes se arma a mano sumando unas 30 descargas diarias | Una descarga por mes. Control avisa si falta un mes o si quedó incompleto. |
| 3 | El crecimiento contra el año anterior compara periodos distintos | El 30/09 mostraba **+42.7 %**. Con los mismos días, **+40.0 %**. | El año en curso llega al último dato y el anterior se toma completo | Siempre los mismos días, por cadena. Solo compara cadenas con historial. |
| 4 | El cumplimiento de meta cambia según el día en que se abre el reporte, sin datos nuevos | **46.4 %** el 21/09, **52.2 %** el 30/09 y **45.0 %** el 15/10 | Metas mensuales contra un filtro de «últimos 9 meses» contado por día | Meses completos, más un «Mes actual» aparte (se aplica en la página de Sell in, pendiente del ERP) |
| 5 | Termómetro Osito duplicado | Sell in inflado en **1.17 M MXN** y metas en **2.72 M MXN**. Ya se corrigió a mano en la versión publicada, pero la causa sigue. | El cruce entre tablas se hace por nombre de producto | Todo se cruza por código del ERP, con una sola fila por producto en el maestro |
| 6 | Productos nuevos de Walmart se pierden | El inventario del Osito en Walmart (**466 piezas en 214 tiendas**) no aparece en ningún producto | La traducción de códigos de Walmart está escrita a mano, producto por producto | Hoja Equivalencias del maestro. Un código desconocido pone Control en 🔴 y lo lista. |
| 7 | Cobertura de Walmart mal clasificada | Nebulizadores con **28 y 50 meses** de inventario salen «🟢 Saludable» | Usa piezas por tienda como si fueran meses, y promedia con el mes en curso incompleto | La misma fórmula en meses para las dos cadenas, con los 3 últimos meses cerrados |
| 8 | Tarjetas aromatizantes individuales registradas como Pack | **226 mil MXN** de tarjetas aparecen como Packs | Código equivocado en el catálogo | El maestro tiene un código propio por producto |
| 9 | Ventas de un nebulizador mostradas como báscula | **8,214 MXN** mal asignados en la página Amazon | 19 reemplazos de nombres escritos a mano, uno mal copiado | El nombre sale del maestro a partir del ASIN, nunca del título de Amazon |
| 10 | Dos gráficos dejan de mostrar meses nuevos | Desde octubre, «Inventario por mes» y el fill rate de Amazon no muestran octubre a diciembre | Filtros de meses fijos | Ventana móvil de 12 meses, según el último dato |
| 11 | Montos en dólares con tipo de cambio fijo, y pesos con etiqueta de dólares | Tipo de cambio fijo de **20**, escrito en 7 lugares. «Recship (us$)» en realidad está en pesos. | Valores escritos dentro de las fórmulas | Montos en MXN con su etiqueta. El tipo de cambio por mes va en el maestro (pendiente de definir cuál). |
| 12 | Metas sin cliente | **361,696 MXN** de metas no aparecen en ningún cliente | El cliente está mal escrito: «Walmar Marketplace» | El maestro ya está corregido; los clientes salen de una sola lista |

## 2. Por qué el proceso actual genera errores

| Paso manual de hoy | Riesgo | En la versión nueva |
|---|---|---|
| Pegar cada día el sell out de Walmart en un Excel consolidado | Días repetidos o faltantes (error 1) | Se guarda la descarga tal cual |
| Convertir cada descarga en tabla con nombre exacto y renombrar el archivo con la fecha | Si el nombre está mal, el archivo no carga o queda en otra fecha | No se renombra nada. La fecha sale del contenido del archivo. |
| Armar a mano el mes de Amazon con unas 30 descargas diarias | Meses incompletos y redondeos (error 2) | 1 descarga al mes |
| Editar consultas cada mes (rutas y pasos atados al primer archivo) | Si cambia un archivo, la actualización falla | Nada que editar en Power BI |
| 18 rutas a carpetas personales del analista anterior | En otra computadora no funciona | Una sola ruta, en un parámetro |
| Reglas y excepciones escritas dentro del código | Nadie las ve; los productos nuevos se pierden (error 6) | Todo en el maestro, a la vista |
| Sin ningún control antes de enviar | El jefe encuentra los errores después | Página Control con semáforo: si no está en 🟢, no se envía |

## 3. Qué ya está resuelto y qué falta

- **Resuelto:**
  - Sell out, inventario, fill rate y Recship de Walmart, y ventas e inventario de Amazon, se cargan sin pasos manuales.
  - Historial de Amazon completo, de febrero de 2024 a septiembre de 2026.
  - Página Control y manual de operación para los dos analistas.
- **Falta:**
  - Sell in e inventario del ERP: se necesita el acceso para bajar la muestra.
  - Historial de sell out de Walmart.
  - Aprobar las definiciones de los indicadores con el jefe.
  - Paralelo de 1 a 2 semanas contra el reporte actual.
