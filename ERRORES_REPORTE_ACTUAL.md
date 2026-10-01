# Errores del reporte actual y cómo los evita la versión nueva

Resumen para presentar. El detalle y la forma de comprobar cada cifra están en [`DIAGNOSTICO_REPORTE_ACTUAL.md`](DIAGNOSTICO_REPORTE_ACTUAL.md).

> **El mensaje principal:** los errores no son de la persona, son del proceso. El reporte exige copiar, pegar, renombrar y escribir reglas a mano todos los días. Así, cualquier analista se equivoca y nada avisa antes de enviar.

## 1. Errores en las cifras

Todos se comprobaron con los datos que tenía cargados el reporte (21/09/2026) o con descargas nuevas.

| # | Qué pasa | Impacto | Causa | Cómo lo evita la versión nueva |
|---|---|---|---|---|
| 1 | Días de sell out de Walmart pegados dos veces, y días que nunca se pegaron | **201,516 MXN contados dos veces** (noviembre de 2025 y 27/08/2026). **14 días de 2026 sin datos**: entre 140 y 180 mil MXN faltantes, cerca del 5 % del año. | Consolidado manual: cada día se pega en un Excel de 315 mil filas | Lee las descargas directo de la carpeta. Cada día se toma de un solo archivo. Si falta un día, Control se pone en 🔴. |
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
