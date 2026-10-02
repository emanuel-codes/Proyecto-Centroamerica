# Diagnóstico del reporte actual: «Análisis de Ventas Wellpro V5»

**Fecha del análisis:** 30/09/2026

**Archivos revisados:**
- `Analisis de Ventas Wellpro -V5.pbix respaldo.pbix`, con datos hasta el 18–20/09/2026.
- `Sell in/BD Sell In.xlsx`.
- `Inventario/Inventarios.xlsx`.
- `Ventas Amazon/`: los 32 archivos mensuales de ventas de Amazon (feb-2024 a sep-2026).

**Pendiente de revisar:** las descargas de inventario y fill rate de Amazon, y las de Walmart.

> **Cómo se hizo.** Del `.pbix` se extrajo todo el código y los datos que trae cargados:
> - 25 consultas de Power Query que cargan tablas y 34 auxiliares;
> - 107 medidas DAX;
> - las relaciones entre tablas;
> - las 5 páginas.
>
> Cada hallazgo de este documento se comprobó contra esos datos. Las cifras corresponden a lo que el reporte tenía cargado al 21/09/2026. El código extraído está en [`analisis/reporte_actual/`](analisis/reporte_actual/).

---

## 1. Resumen

El reporte funciona, pero sus cifras principales tienen errores medibles. Casi todos vienen del mismo origen: un proceso con muchos pasos manuales y reglas escritas a mano dentro de las consultas. Con este diseño, cualquier analista cometería errores.

**Errores que afectan cifras que ven los jefes**, todos verificados con los datos del `.pbix`:

| # | Qué pasa | Impacto medido |
|---|---|---|
| 1 | El Termómetro Osito aparece dos veces en los catálogos. El cruce por nombre duplica sus ventas y sus metas. | En el respaldo del 21/09: sell in inflado en **1.17 M MXN** (**+9 %** en 2026) y metas infladas en **2.72 M MXN**. En la versión publicada al 30/09 ya está corregido (ver A1). |
| 2 | Las metas están fechadas el último día de cada mes, y el filtro de fechas es "últimos 9 meses contados por día". | El % de cumplimiento cambia según el día en que se abre el reporte, aunque no entren datos nuevos: **46.4 %** el 21/09, **52.2 %** el 30/09 y **45.0 %** el 15/10. |
| 3 | El crecimiento compara el año en curso, incompleto, contra el año anterior completo. Además arrastra el duplicado del punto 1. | El 30/09 el reporte muestra **+42.7 %**. Comparando los mismos días y sin el duplicado, el crecimiento es **+40.0 %**. |
| 4 | En el Excel consolidado de sell out Walmart hay días pegados dos veces y días que nunca se pegaron. | **201,516 MXN** duplicados (del 1 al 10 de noviembre de 2025 y el 27 de agosto de 2026). **14 días de 2026** sin datos, unos 140–180 mil MXN faltantes. |
| 5 | La clasificación de cobertura de Walmart usa "piezas por tienda" como si fueran meses de inventario. | Nebulizadores con **28 y 50 meses** de inventario aparecen como "🟢 Saludable". |
| 6 | Dos gráficos tienen un filtro de meses fijo. | Desde octubre, «Inventario por mes» (Walmart) y el fill rate de Amazon dejan de mostrar los meses nuevos. |
| 7 | La homologación de códigos de Walmart está escrita a mano, producto por producto. | Los productos nuevos quedan sin asignar: el inventario del Osito en Walmart (**466 piezas** al 20/09) no aparece en ningún producto. |
| 8 | Dos tarjetas aromatizantes individuales están mapeadas al código del Pack. | **226 mil MXN** de venta de tarjetas individuales aparecen como venta de Packs. La tarjeta individual sale con meta y sin venta. |
| 9 | Hay un error de copiado en una consulta de Amazon. | Ventas del Nebulizador Elefante Rosa (**8,214 MXN**) aparecen como "Báscula de Vidrio Transparente" en la página de Amazon. |
| 10 | El tipo de cambio está fijo en 20 y escrito en 8 lugares del modelo. Además, "Recship (us$)" en realidad está en pesos. | Los montos en USD no usan el tipo de cambio real. En la página de Walmart se mezclan USD y MXN con la misma etiqueta. |

**Por qué la actualización toma horas:**
- El reporte lee **18 archivos y carpetas** distintos, todos en la computadora del analista anterior.
- Varias fuentes exigen preparar a mano cada archivo descargado: convertirlo en tabla con un nombre exacto y renombrar el archivo con la fecha.
- El sell out de Walmart se consolida copiando y pegando en un Excel de 315 mil filas.
- Algunas consultas hay que editarlas cada mes: cambiar la carpeta y cambiar la fecha escrita dentro de un paso.

---

## 2. Qué muestra el reporte

| Página | Estado | Contenido |
|---|---|---|
| **Sell In** | Visible | Venta del ERP contra meta: tarjeta de venta, año anterior, crecimiento y cumplimiento; meta por familia; tendencia mensual; participación por cliente y por familia. Se puede ver en monto o piezas, y en MXN o USD. |
| **Sell Out** | Visible | Vista Walmart: sell out actual y del año anterior, tiendas con inventario, inventario por mes, tendencia de venta, fill rate, pronóstico de compra (Recship) y participación por familia. |
| **Sell  Out** (con dos espacios) | Oculta, se llega con un botón | Vista Amazon: sell out actual y del año anterior, tabla de cobertura por producto, tendencia, fill rate y participación. |
| **Inventario** | Visible | Inventario propio: existencia, meses de inventario, punto de reorden, entradas y salidas por mes, Top 10 de artículos. |
| **Inventario.** (con punto) | Oculta, sin acceso | Versión anterior de la página de inventario, basada en el kardex del ERP. Ningún botón lleva a ella. |

El detalle de cada gráfico, con sus campos y filtros, está en [`analisis/reporte_actual/05_paginas_y_visuales.md`](analisis/reporte_actual/05_paginas_y_visuales.md).

---

## 3. De dónde salen los datos

Todas las rutas apuntan a la computadora del analista anterior: `C:\Users\<analista anterior>\OneDrive - VISION MEDICA S.A\...`. Están repartidas en tres zonas distintas: `Documentos`, `Imágenes` y `Documentos\Escritorio\temp`.

Por eso el reporte **solo se puede actualizar desde esa computadora**. La actualización programada en Power BI Service no es posible sin una puerta de enlace instalada ahí.

| Fuente | Qué lee hoy | Tabla del modelo | Preparación manual que exige |
|---|---|---|---|
| Sell in (ERP One Goal) | `Imágenes\Reportes Mexico\BD Sell In.xlsx`, hoja «Venta», tabla `Ventas_Wellpro` (7,204 filas) | `Ventas_Wellpro` | Pegar lo exportado del ERP debajo de la marca «Aplicar aquí». Normalizar a mano los nombres de clientes y productos. Hay códigos de barras escritos a mano, según los comentarios del archivo. |
| Catálogos y metas | El mismo `BD Sell In.xlsx`: tablas `Catalogo_Producto_Wellpro`, `Catalogo_Sell_In`, `Catalogo_Clientes`, `Metas` y la hoja «Catalogo de Estados» | Tablas con esos nombres | Mantenerlos a mano. La homologación se hace **por nombre de producto**. |
| Sell out Walmart | `Walmart\Ventas Sell Out WM\Ventas Consolidadas WM.xlsx`, tabla `Sell_Out_WM` (314,747 filas) | `Sell_Out_WM` | Pegar cada descarga diaria de Retail Link en el consolidado. |
| Inventario en tiendas Walmart | Carpeta `Walmart\Inventarios en Tiendas - copia`, un Excel por día (239 archivos, 1.04 M filas) | `Inventario en Tienda WM` | Cada archivo debe tener una tabla llamada exactamente `Inventario_Tiendas_WM` y el nombre `dd-mm-aaaa.xlsx`. |
| Recship Walmart | Carpeta `Walmart\Recship WM` (1 archivo) | `Recship WM` | Nombrar el archivo con una fecha. |
| Fill rate Walmart | `Walmart\Fill rate.xlsx`, hoja «Fill_rate» | `Fill_rate` | Sobrescribir el archivo. |
| Tiendas Walmart | `Documentos\Reporterias WM\...\SellOut Walmart.xlsx` | `Catalogo de Tiendas` y su copia `TIENDAS` | No se usa en ningún gráfico. |
| Ventas Amazon (mensual) | Carpeta `Amazon\Ventas Amazon`, un archivo por mes (32 meses) | `Ventas Amazon` | Tabla llamada `Ventas_Amazon` y el nombre `... dd-mm-aaaa.xlsx`. Son exportaciones de **Amazon Vendor Central** (vista Fabricación, en MXN). Desde noviembre de 2025 el archivo del mes se arma a mano con las descargas diarias (ver B8). |
| Ventas Amazon (diario, mes en curso) | Carpeta `Documentos\Escritorio\temp\Enero 2026\Septiembre 2026`, un archivo por día | `Ventas Amazon mes actual` | No se usa en ningún gráfico. Su total coincide exactamente con el archivo mensual de septiembre (472 unidades, 40,777 MXN, 19 días), así que el mensual se arma con los diarios. La carpeta cambia cada mes. |
| Inventario Amazon | Carpeta `Amazon\Inventarios Amazon\2025`, un archivo por día (382 días) | `Inventario Amazon` | Tabla llamada `Inventario_Amazon` y la fecha en el nombre del archivo. |
| Fill rate Amazon | `Amazon\Fillrate AMAZON\POItemExport_2026-06-24.xls` | `Fillrate Amazon New` | El nombre del archivo está fijo: hay que sobrescribirlo conservando ese nombre. |
| Kardex ERP | Carpeta `Imágenes\Reportes Mexico\KARDEX` | `InventarioKardex` y `InventarioKardex (2)` | Se carga **dos veces**. Alimenta la página oculta y el Top 10. |
| Inventario auxiliar ERP | Carpeta `Imágenes\Reportes Mexico\Inventario Auxiliar` | `Inventario Auxiliar` | — |
| Inventario propio | `Imágenes\Reportes Mexico\Movimientos INV\Inventarios.xlsx`, hojas «Tbl» y «Costos» | `Tbl`, `Costos` | **Se escribe a mano cada mes**: 222 filas, 8 meses. Es la base de la página Inventario. |
| Tipo de cambio | Tabla escrita dentro del reporte | `Tipo de cambio` | Valor fijo: 20. |
| Sin uso | `Inventarios Wellpro` (datos hasta oct-2025), `CatalogoCuentas`, `Balanza de comprobacion` | — | Se cargan o se mantienen sin que ningún gráfico las use. |

---

## 4. El proceso de actualización, según el código

Esto se deduce de lo que exigen las consultas. **Hay que confirmarlo con el cliente.**

**Cada día:**
1. **Amazon, ventas.** Descargar el día, abrir el archivo, convertirlo en tabla llamada `Ventas_Amazon` y guardarlo como `Ventas Amazon dd-mm-aaaa.xlsx` en la carpeta temporal del mes.
2. **Amazon, inventario.** Lo mismo, con una tabla llamada `Inventario_Amazon`.
3. **Walmart, sell out.** Descargar de Retail Link y pegar en `Ventas Consolidadas WM.xlsx`.
4. **Walmart, inventario en tiendas.** Descargar, convertir en tabla `Inventario_Tiendas_WM` y guardar como `dd-mm-aaaa.xlsx`.

**Periódicamente:**

5. **Sell in.** Exportar del ERP, pegar en `BD Sell In.xlsx` y corregir nombres y códigos.
6. **Amazon, cada mes:**
   - armar el archivo mensual a partir de los diarios;
   - crear una carpeta nueva para el mes;
   - cambiar la ruta de la consulta «Ventas Amazon mes actual»;
   - cambiar el paso que dice `"1/9/2026"` (ver B2).
7. **Inventario propio, cada mes.** Escribir a mano la tabla `Tbl`.
8. **Fill rates.** Sobrescribir los archivos, conservando el nombre fijo en el caso de Amazon.
9. **Cierre.** Actualizar, que es lento porque abre cientos de Excel; revisar y publicar.

Cada paso es una oportunidad de error. Varios de los errores de la sección 5 son justamente eso: días pegados dos veces, días sin descargar y archivos duplicados.

---

## 5. Errores encontrados (detalle)

### A. Errores que afectan las cifras

**A1. Termómetro Osito duplicado: infla el sell in y las metas.**
- El catálogo de productos tiene **dos filas** llamadas «Termómetro Pediatrico Cute Animals Osito»: una con UPC `7431009207481` y otra con UPC `743100920748`. `Catalogo_Sell_In` también lo tiene dos veces.
- Las consultas `Ventas_Wellpro` y `Metas` cruzan **por nombre de producto**, así que cada fila del Osito se multiplica por dos.
- Prueba: el Excel tiene 7,204 filas de venta y el modelo 8,385. La diferencia, 1,181 filas, son todas del Osito. En metas, el Excel tiene 1,319 filas y el modelo 1,425: hay 106 duplicadas.
- Impacto en el sell in: **+1,169,551 MXN** (121 mil en 2024, 272 mil en 2025 y 776 mil en 2026). En 2026 el reporte muestra 9.18 M, cuando el dato correcto es 8.40 M.
- Impacto en las metas: **+2,721,454 MXN**.
- **Actualización del 30/09:** en las capturas del reporte publicado, la meta (17,036,534) y el año anterior (6,290,482) coinciden exactamente con las cifras corregidas de este análisis. El duplicado ya se quitó en la versión actual, pero la causa, el cruce por nombre, sigue en el diseño.
- **Corrección:** homologar por código, no por nombre, y dejar una sola fila por producto en el catálogo.

**A2. El cumplimiento de meta cambia según el día en que se abre el reporte.**
- Las metas son mensuales y están fechadas el último día del mes (31/01, 28/02, ...). El filtro de fechas de las páginas es relativo: "últimos 9 meses", contados por día.
- Salvo el último día de cada mes, la ventana empieza a mitad de un mes. Por eso incluye la meta **completa** de ese mes, pero solo unos días de su venta.
- Ejemplo con los mismos datos: el 21/09 la tarjeta muestra **46.4 %**, el 30/09 muestra **52.2 %** y el 15/10, sin cargar nada nuevo, mostraría **45.0 %**.
- Con el duplicado del Osito corregido y solo meses cerrados (enero a agosto de 2026), el cumplimiento es **46.6 %**.
- **Corrección:** comparar por meses completos y tratar el mes en curso aparte, con la meta prorrateada o como "mes a la fecha".

**A3. El crecimiento contra el año anterior compara periodos distintos.**
- La venta del año en curso llega hasta el 18/09, pero el "año anterior" toma el periodo completo, hasta el 30/09/2025. A eso se suma el duplicado del Osito, que pesa más en 2026.
- El 30/09 el reporte muestra **+42.7 %**. Sin el duplicado y comparando los mismos días (del 1/1 al 18/9), el crecimiento es **+40.0 %**.
- El mismo problema afecta las tarjetas "año anterior" de las páginas de sell out, que usan `SAMEPERIODLASTYEAR` y `DATEADD`.
- **Corrección:** limitar el año anterior al último día con datos.

**A4. Sell out Walmart con días duplicados y días faltantes.**
- Hay 2,113 filas idénticas, es decir, mismo día, tienda, artículo y valores: **465 piezas y 201,516 MXN contados dos veces**.
  - Del 3 al 7 de noviembre de 2025, prácticamente el día completo está dos veces.
  - Del 1 al 2 y del 8 al 10 de noviembre, entre el 30 % y el 42 % del día está repetido.
  - El 27 de agosto de 2026, el 84 %.
- Faltan **14 días de 2026**: 06/01, 15/01, 03/02, 23/03, 14/04, 27/04, 28/04, 20/05, 25/05, 28/05, 11/06, 12/06, 16/06 y 12/08. Con una venta diaria típica de 10–13 mil MXN, faltan unos **140–180 mil MXN**, alrededor del 5 % de 2026.
- **Corrección:** leer las descargas directamente de una carpeta, sin consolidado manual, y eliminar duplicados por llave (día + tienda + artículo). Agregar una alerta de días faltantes.
- **Comprobado con las descargas nuevas (02/10/2026)**, del 01/10/2024 al 20/09/2026, el último día del reporte actual:
  - de octubre de 2024 a agosto de 2025, el reporte actual coincide exactamente, al peso;
  - **de más:** 203,270 MXN y 471 piezas en 12 días (del 1 al 10 de noviembre de 2025, y el 27 y 30 de agosto de 2026);
  - **días completos faltantes:** 191,566 MXN y 540 piezas en los 14 días de 2026 ya listados;
  - **días incompletos:** 129,981 MXN y 517 piezas en 120 días, de septiembre de 2025 a septiembre de 2026. Todo septiembre de 2025 trae menos venta (−31,170 MXN) y el 21/12/2025 solo tiene un artículo (−34,747 MXN);
  - **neto:** el reporte actual muestra 118,278 MXN y 586 piezas menos de lo real. Por mes el error es mayor: +31 % en noviembre de 2025, −8.6 % en enero de 2026 y −6.2 % en septiembre de 2025.

**A5. La clasificación de cobertura se contradice con los meses de inventario.**

Esto aparece en la tabla de la página de Amazon cuando se elige Walmart. Para Walmart, la medida «Clasificación Cobertura» no usa los meses de inventario: usa `Inventario_Prom_Tienda`, que son **piezas promedio por tienda**, y le aplica los mismos umbrales de meses.

| Producto (Walmart) | Inventario | Venta promedio mensual (4 meses) | Meses de inventario | Piezas por tienda | Clasificación en el reporte |
|---|---|---|---|---|---|
| Nebulizador Familiar | 3,576 | 125 | 28 | 2 | 🟢 Saludable |
| Nebulizador Elefante Azul | 3,676 | 72 | 50 | 2 | 🟢 Saludable |
| Termómetro Panda | 18,524 | 754 | 24 | 17 | 🟡 Sobre stock |

Otros problemas de la misma tabla:
- Para Walmart nunca se asigna "Riesgo de quiebre".
- Los umbrales de Walmart y de Amazon son distintos.
- El promedio de 4 meses incluye el mes en curso incompleto, así que subestima la venta y exagera la cobertura.

**Corrección:** una sola definición de cobertura en meses, igual para las dos cadenas, calculada con meses completos.

**A6. Filtros de meses fijos en dos gráficos.**
- «Inventario por mes vs Promedio de Inventario por Piezas» (página Walmart) tiene un filtro que **excluye octubre, noviembre y diciembre**.
- El gráfico de fill rate de la página Amazon tiene un filtro que **solo incluye de enero a septiembre**.
- Desde el 1 de octubre, esos gráficos dejan de mostrar los meses nuevos, y octubre a diciembre nunca aparecen, de ningún año.
- **Corrección:** quitar esos filtros. La ventana de fechas ya la controla el filtro relativo.

**A7. Homologación de Walmart escrita a mano; los productos nuevos se pierden.**
- Retail Link reporta el UPC sin dígito verificador y con un 0 adelante. Cuatro consultas (`Sell_Out_WM`, `Inventario en Tienda WM`, `Recship WM` y `Fill_rate`) traducen el código de **4 productos** a mano, uno por uno.
- En `Inventario en Tienda WM` la regla es "si no es uno de estos 4, poner 0". Por eso el Osito, que Walmart empezó a manejar a fines de agosto de 2026, tiene su inventario (**466 piezas en 214 tiendas**) asignado al código «0», que no corresponde a ningún producto.
- En `Recship WM`, el Osito se traduce a `743100920748`, un código de 12 dígitos que no existe. Probablemente por eso se agregó al catálogo la segunda fila del Osito, que es la causa del duplicado del punto A1. El código correcto es `7431009207481`.
- **Walmart ya trae el código del ERP.** La columna `Vendor Stk Nbr` de Retail Link es el código de producto del ERP en 4 de los 5 artículos: 14660, 13471, 13595 y 13594. La homologación puede hacerse directo por ese código, y usar el número de artículo o la regla del UPC cuando traiga otra cosa. En los datos del reporte el Osito lo trae vacío, y en la descarga del 30/09 trae «MTB132FA».
- **La regla es fija y se puede automatizar.** Se quita el 0 inicial y se agrega el dígito verificador. Por ejemplo, `0743400255002` → `743400255002` → `7434002550028` (Nebulizador Familiar). Se comprobó con los 5 artículos que maneja Walmart.

**A8. Tarjetas aromatizantes individuales asignadas al Pack.**
- En `Catalogo_Sell_In`, «Tarjeta Aromatizante con Frases Motivacionales» y «... con Frases Religiosas» apuntan al UPC del **Pack de 24** (`7431009209737` y `7431009209713`). Sus códigos propios son `7431009209706` y `7431009209690`.
- Los precios confirman que son tarjetas individuales: se venden a unos 14 MXN por unidad, contra unos 341 MXN del pack.
- Resultado: **226 mil MXN** de venta de tarjetas individuales aparecen como venta de Packs. Las tarjetas individuales muestran meta (909 mil y 120 mil MXN) sin venta.

**A9. Nombres de producto en Amazon.**
- La consulta `Ventas Amazon` acorta los títulos con **19 reemplazos escritos a mano**.
- Uno tiene un error de copiado: el título del «Nebulizador pediátrico de Elefante Rosa» se reemplaza por «Wellpro báscula Digital de vidrio transparente». Por eso **12 unidades y 8,214 MXN** del nebulizador aparecen como báscula en el gráfico circular de la página Amazon.
- Además, Amazon cambia los títulos con el tiempo: **17 de los 25 ASIN tienen 2 o 3 títulos distintos**. En ese gráfico un mismo producto sale partido en varias porciones.
- **Corrección:** tomar siempre el nombre del catálogo a partir del ASIN, nunca el título de Amazon.

**A10. Tipo de cambio y monedas.**
- El tipo de cambio es un valor fijo de **20** en la tabla `Tipo de cambio`, y además está escrito como `/20` 7 veces en 6 medidas y en una hoja del Excel de sell in. No cambia por mes.
- La medida «Recship (us$)» suma `Unidades × Costo por caja ÷ Piezas por caja`. Ese costo viene de Retail Link en **pesos**, y no se divide entre el tipo de cambio.
- Resultado: en la página de Walmart, con "Monto" seleccionado, las tarjetas muestran USD y el «Pronóstico de Compra» muestra MXN.
- **Corrección:** una tabla de tipo de cambio por mes y una sola medida de conversión.

**A11. La página Inventario mezcla tablas que no están relacionadas.**
- Las tarjetas y los gráficos salen de la tabla manual `Tbl`, pero el «Top 10 Articulos» sale del kardex del ERP.
- No hay relación entre las dos tablas. Por eso el filtro «Filtro por Artículo» no cambia el Top 10: en la captura del 30/09, con la báscula antideslizante filtrada, el Top 10 sigue mostrando todos los artículos.
- Los botones «Monto» y «Piezas» de esta página no cambian nada, porque ninguna medida de la página los usa. En la captura, con «Monto» seleccionado, las cifras siguen en piezas.
- Además, el «Punto de Reorden» es el promedio de salidas × 7, un número fijo, aunque el catálogo ya tiene el tiempo de entrega y el stock de seguridad de cada producto.

**A12. Metas con el cliente mal escrito.**
- En la hoja de metas, 60 filas de 2025 tienen el cliente «Walmar Marketplace», sin la t.
- Ese nombre no existe en el catálogo de clientes. Por eso, al filtrar por cliente, esas metas (361,696 MXN) no aparecen en ningún cliente.

### B. Riesgos que hacen fallar la actualización o que dependen de pasos manuales

- **B1. Rutas personales.** Son 18 rutas en la computadora del analista anterior, incluidas las carpetas `Imágenes` y `Escritorio\temp`. En otra computadora, ninguna consulta encuentra sus archivos.
- **B2. Pasos atados al primer archivo de la carpeta.**
  - Al combinar archivos, la columna de fecha toma como nombre la fecha del primer archivo, y luego un paso la renombra usando ese texto: `"1/1/2025"` → `"1/2/2024"` → `"Fecha"` en Ventas Amazon, `"1/4/2026"` en Inventario Amazon y `"1/9/2026"` en Ventas Amazon mes actual.
  - Si cambia el primer archivo (llega un mes nuevo, se agrega o se borra un archivo), **la actualización falla**. La consulta del mes en curso hay que editarla cada mes.
  - Pasa lo mismo con `"Column9"`, una columna sin título en el primer archivo.
- **B3. Fecha tomada del nombre del archivo.**
  - Se toman los últimos 15 caracteres del nombre (por ejemplo, `01-09-2026.xlsx`) y se convierten a fecha con la configuración regional de la computadora.
  - Un nombre mal escrito o una computadora en inglés cambian o rompen las fechas. El archivo de Recship tiene fecha **12/12/2026**, en el futuro.
- **B4. Cada descarga debe convertirse a mano en una tabla con nombre exacto**: `Ventas_Amazon`, `Inventario_Amazon` o `Inventario_Tiendas_WM`. Si la tabla tiene otro nombre, ese archivo no se carga.
- **B5. Excepciones escritas a mano en el código.**
  - Un archivo excluido por nombre: `01-01-2026.xlsx`.
  - Fechas del kardex excluidas: 31/01/2025 y 31/03/2025.
  - Salidas de exactamente 6,000 unidades y artículos con "tarjeta" en el nombre, excluidos del Top 10.
  - Filtros con el texto `"de ABR a ABR"` y `"de AGO a AGO"` en la balanza.
  - Una lista fija de productos promocionales excluidos del filtro de artículos.
- **B6. Consolidado manual de Walmart:** un Excel de 315 mil filas que crece cada día y que es la causa de los errores del punto A4.
- **B7. Archivos faltantes o incompletos.**
  - Inventario en tiendas Walmart:
    - hay archivo en 239 de 385 días;
    - **abril de 2026 no tiene ningún archivo**, así que el gráfico mensual no tiene abril;
    - los archivos del 12/12/2025 y del 09/09/2026 vienen casi vacíos, con inventario 0.
  - Inventario Amazon:
    - el 12/12/2025 está cargado dos veces, lo que duplica ese día;
    - el 02/11/2025 trae 2,391 unidades sin ASIN;
    - faltan el 12/11/2025 y el 31/03/2026.
- **B8. Desde noviembre de 2025, los archivos mensuales de Amazon se arman a mano.**
  - Los 32 archivos coinciden exactamente con lo que muestra el reporte: Power BI los lee bien.
  - Cada archivo trae en la primera fila el rango de fechas que Amazon usó al generarlo.
  - **Hasta octubre de 2025**, el rango es el mes completo (por ejemplo, `01/03/24 - 31/03/24`). Es decir, cada archivo era **una sola descarga del mes**.
  - **Desde noviembre de 2025**, el rango ya no corresponde a los datos:
    - nov-2025, dic-2025, ene-2026 y sep-2026 dicen un solo día (el 1 del mes);
    - de feb-2026 a may-2026 dicen `01/01/26 - 01/01/26`;
    - de jun-2026 a ago-2026 dicen `01/06/25 - 30/06/25`, un mes de otro año.

    Todo indica que se usa un archivo viejo como plantilla y se pegan encima los totales del mes, sumados a partir de las descargas diarias.
  - El archivo de dic-2025 lo muestra: tiene 6 hojas, con los datos diarios del 1 al 27 de diciembre, una tabla dinámica que los suma y dos versiones anteriores con cifras distintas.
  - El archivo de ene-2025 también trae un rango que no le corresponde: `01/02/25 - 28/02/25`, que es febrero.
  - **Conclusión:** la cuenta de Amazon sí permite bajar el mes completo en un archivo, porque así se hizo hasta octubre de 2025. Volver a eso pasa de unas 30 descargas al mes a una.
  - **Comprobado con las descargas nuevas del mes completo (30/09/2026):**
    - **Noviembre y diciembre de 2025 están incompletos en el reporte actual:** le faltan **112 piezas y 16,928 MXN**. Noviembre: −24 piezas y −3,841 MXN. Diciembre: −88 piezas y −13,087 MXN, porque solo llega al día 27.
    - **De enero a agosto de 2026**, las piezas coinciden y el monto difiere menos de 25 MXN al mes, por el redondeo de las sumas a mano.
    - **Enero de 2025** coincide: el contenido era correcto, solo traía mal el rango de fechas.

### C. Catálogo de productos con códigos inválidos

El catálogo es la base de toda la homologación. Tiene estos problemas:

| Problema | Productos |
|---|---|
| ASIN inventados para cumplir la relación | Nebulizador Adulto Walmart (`abcdefghi1`), Nebulizador Adulto Compacto (`abcdefghi2`), Nebulizador Pediátrico Elefante Celeste (`abcdefghi3`), Nebulizador Pediátrico Búho Blanco (`ABCDEFG910`) |
| ASIN escrito con letra O en lugar de cero | Nebulizador Adulto Moderno NBA-10WA (`BOFPHCD4K3`). Parece ser el mismo ASIN de «Tapa Verde» (`B0FPHCD4K3`). |
| UPC provisionales | Nebulizador Pediátrico Animalitos, Kit de Nebulización Adulto y Kit de Nebulización Pediátrico (`7770000000053/54/55`) |
| UPC con dígito verificador inválido | Nebulizador Adulto Compacto (`7434002550000`), Nebulizador Pediátrico Penguin (`7743100920748`) y Nebulizador Adulto Moderno Tapa Verde (`7431009209318`). En este último, el código válido más cercano, `…9317`, está asignado al Búho Blanco: hay que verificarlo. |
| Producto duplicado | Termómetro Osito (dos filas); ver A1 |
| Homologación del ERP por nombre | `Catalogo_Sell_In` tiene 48 nombres para 30 productos, por ejemplo «Bascula» y «Báscula», o «Termometro Pediatrico Panda» y «Termómetro Pediatrico Cute Animals Panda». |

### D. Limpieza y rendimiento

- **D1. Tablas cargadas que ningún gráfico ni medida usa (8):** `Catalogo de Tiendas`, `TIENDAS`, `Catalogo_Estado`, `CatalogoCuentas`, `Costos`, `Inventarios Wellpro`, `Ventas Amazon mes actual` e `InventarioKardex (2)`. Todas se actualizan cada vez.
- **D2. Medidas sin uso: 46 de 107.** Algunas tienen errores, pero no se ven en el reporte:
  - «DOH AMAZON» divide el inventario de Amazon entre la venta de **Walmart**;
  - «Promedio_Ventas_Diarias» divide dos veces entre la cantidad de días.
- **D3.** La página «Inventario.» está oculta y ningún botón lleva a ella.
- **D4. Fecha automática activada.** El modelo tiene 14 tablas de fecha ocultas y el calendario se genera con `CALENDARAUTO()`.
- **D5. La tabla más grande es el inventario diario por tienda de Walmart (1.04 M filas).** El reporte solo usa la última fecha de cada mes y la última disponible. Guardar una foto semanal o mensual bajaría mucho el tiempo de actualización.
- **D6. Fill rate Walmart.**
  - Se relaciona con el calendario por la **fecha de cancelación** de la orden, no por la de pedido ni la de envío. Hay que confirmarlo con el cliente.
  - Su selector de unidades espera "$MX", "Cajas" y "Unidades", pero la segmentación ofrece "Monto" y "Piezas". Por eso siempre calcula en unidades.
  - La columna «Ordenado en $MX» multiplica unidades por el costo de la **caja** completa. Hoy no se usa, pero está mal.
  - La relación de producto une un número (`Fill_rate[UPC]`) con un texto (el UPC del catálogo).
- **D7. Reglas de clientes escondidas en el código.**
  - «PUBLICO EN GENERAL» → Market Place.
  - «PHARMA PLUS» → Farmacia San Pablo.
  - «CLAUDIA LEMOINE GOMEZ» → Mercado Libre.
  - «ISSSTE» → Mercado Libre. Esta última parece un error, aunque hoy no tiene filas.

  Estas reglas deberían estar en una tabla visible y validada por el cliente.
- **D8.** En la tarjeta de venta de Sell In, el crecimiento siempre se muestra en rojo, aunque sea positivo.

---

## 6. Qué conviene conservar

- **El filtro de fechas relativo.** Se actualiza solo, pero hay que alinearlo con metas mensuales (ver A2).
- **La lectura por carpeta.** Algunas fuentes ya combinan todos los archivos de una carpeta; es la base del esquema nuevo.
- **El catálogo de productos.** Ya tiene UPC, ASIN, familia, tiempo de entrega y stock de seguridad. Limpio, es la tabla de homologación.
- **Los indicadores que el cliente ya usa:** sell in contra meta, crecimiento, participación, sell out por cadena, fill rate, cobertura, punto de reorden y pronóstico de compra.
- **El diseño de las tarjetas HTML**, si al cliente le gusta.

---

## 7. Propuesta para la versión nueva (resumen)

1. **Maestro de productos único y limpio.** El ID del ERP es la llave. Cada producto con un EAN válido, su ASIN real y su artículo de Walmart.
2. **Tabla de equivalencias** con las columnas Cadena, Código en la cadena, ID ERP y Factor de piezas. La conversión del UPC de Walmart se hace con la regla automática.
3. **Una carpeta por fuente en el OneDrive o SharePoint de la empresa.**
   - Los archivos se guardan tal como se descargan.
   - Power Query toma la fecha del contenido o de un nombre con formato fijo.
   - No hay tablas con nombre ni pasos que haya que editar cada mes.
4. **Sin consolidados manuales.** El sell out de Walmart se lee de la carpeta y los duplicados se eliminan por llave.
5. **Amazon: menos descargas.** Bajar el mes, o el mes hasta la fecha, en un solo archivo en vez de 30 diarios. La cuenta lo permite: así se hizo hasta octubre de 2025 (ver B8).
6. **Inventario desde el ERP**, usando el kardex o el inventario auxiliar, en lugar de la tabla manual.
7. **Metas por mes completo.** El mes en curso se muestra con la meta prorrateada.
8. **Tipo de cambio mensual** en una tabla.
9. **Página de control** con:
   - la última fecha cargada de cada fuente;
   - los días faltantes;
   - los duplicados;
   - los códigos sin homologar.
10. **Modelo limpio.**
    - Quitar tablas, medidas y páginas sin uso.
    - Apagar la fecha automática.
    - Una sola tabla de sell out con una columna "Cadena".
    - Una sola definición de cobertura.
11. **Actualización sin depender de una computadora.** Los Excel en SharePoint no necesitan puerta de enlace. Si el ERP es una base de datos interna, esa fuente sí la necesita.

---

## 8. Preguntas para el cliente

- **Amazon:** las ventas salen de Vendor Central. ¿Por qué desde noviembre de 2025 se descargan día por día, si antes se bajaba el mes completo? ¿Se necesita el dato diario para algo?
- **Walmart:** ¿qué consulta de Retail Link se usa? ¿Se puede guardar y programar?
- **Tipo de cambio:** ¿cuál se debe usar? Por ejemplo, el mensual real o uno fijo de presupuesto.
- **Reglas de clientes:** ¿son correctas? Sobre todo ISSSTE → Mercado Libre, Claudia Lemoine → Mercado Libre, Pharma Plus → Farmacia San Pablo y Público en general → Market Place.
- **Cobertura:** ¿cuántos meses se consideran riesgo, óptimo y sobre stock? ¿Son iguales para Walmart y Amazon?
- **Fill rate Walmart:** ¿se mide por fecha de pedido, de envío o de cancelación?
- **Inventario:** ¿por qué la página pasó del kardex del ERP a una tabla escrita a mano?
- **Códigos:** ¿cuáles son los ASIN y UPC reales de los productos con códigos provisionales (sección C)?
- **Proceso:** ¿el proceso de la sección 4 coincide con lo que se hace hoy? ¿Cuánto tiempo toma cada paso?
