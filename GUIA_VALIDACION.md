# Guía para validar las cifras

**Idea central:** el reporte no inventa números. Cada cifra sale de un archivo descargado. Validar es comprobar dos cosas:
1. que **el archivo es el correcto**, es decir, que la consulta descargó lo que debía;
2. que **el reporte suma lo mismo que el archivo**.

Si las dos se cumplen, la cifra es correcta, aunque no coincida con el reporte anterior. Las diferencias con el reporte anterior se explican en el paso 6.

Los valores de ejemplo de esta guía son los de las muestras de `Nueva versión/` (30/09/2026). Desde la v0.4 también está cargado el historial de Amazon de 2024 y 2025; donde eso cambia el resultado, se indica.

> **Regla de oro: valida sobre una copia, fuera de `Nueva versión`.**
> Copia el archivo a otra carpeta, por ejemplo `Documentos\Validaciones\`, y trabaja ahí.
> El reporte lee **todos** los Excel que hay dentro de `Nueva versión`. Si guardas ahí una copia, una tabla dinámica o un archivo de trabajo, el reporte lo tomará como otra descarga.

---

## Paso 1. Revisa que la descarga sea la correcta (2 minutos)

| Fuente | Dónde mirar | Qué debe decir |
|---|---|---|
| **Retail Link** (cualquier archivo) | Las primeras filas, antes de los encabezados de columna | El nombre del reporte («Sell Out Act.», «Inventario en Tiendas MX Act.», etc.). El proveedor: `Vendor Nbr ... Is One Of 164242`. El rango: `Pos Date ... Is Between 09-22-2026 and 09-29-2026`. **Ojo: Retail Link escribe las fechas como mes-día-año.** |
| **Retail Link, fill rate y Recship** | La lista de semanas (`Time Range 1 202549, ...`) | Que no falte ninguna semana. Hoy falta la **202618** en el fill rate (ver `GUIA_DESCARGAS.md`). |
| **Amazon** | La fila 1 | `Programa=[Retail]`, `Vista del distribuidor=[Fabricación]`, `Visto por=[ASIN]`, `Moneda=[MXN]` y el rango: `Rango de visualización=[01/09/26 - 28/09/26]`. **Amazon escribe las fechas como día/mes/año.** |
| **Power BI, página Control** | La tabla «Archivos leídos» | Cada archivo con su rango (Desde, Hasta). La columna **Usado** dice «Sí» en los archivos que cuentan. Si dice «No: hay uno más reciente», el reporte usa otro archivo: valida contra el que dice «Sí». |

---

## Paso 2. Cuadra los totales: archivo contra reporte (5 minutos)

**Cómo sumar una columna en Excel:** abre la copia, haz clic en la letra de la columna y mira **Suma** en la barra de abajo. Los encabezados de texto no estorban, porque Excel solo suma los números.

| Cifra del reporte | Archivo | Qué sumar | Muestras |
|---|---|---|---|
| Sell out Walmart, piezas y monto | `Walmart/Sell out` | `POS Qty` y `POS Sales` | 363 piezas · $87,070.21 |
| Sell out Amazon, piezas y monto | `Amazon/Sell out`, un archivo por mes | `Unidades pedidas` y `Ganancia por pedidos` | Agosto: 564 · $60,542.83<br>Septiembre: 692 · $60,111.75 |
| Tiendas de Walmart con venta | `Walmart/Sell out` | Tiendas (`Store Nbr`) con `POS Qty` mayor que 0, sin repetir (ver abajo) | 260 |
| Inventario Walmart | `Walmart/Inventario` | `Curr Str On Hand Qty` | 27,281 |
| Inventario Amazon | `Amazon/Inventarios` | `Unidades aptas para la venta disponibles` | 3,198 |
| Piezas ordenadas (fill rate) | `Walmart/Fill rate` | `Hist Eaches Str Ordered` + `Hist Eaches Whse Ordered` | 16,163 + 0 |
| Piezas recibidas (fill rate) | `Walmart/Fill rate` | `Hist Eaches Str Received` + `Hist Eaches Whse Received` | 15,126 + 0 |
| Pedidos planeados, piezas | `Walmart/Forecast` (el más reciente) | `Units` | 552 |
| Pedidos planeados, monto | `Walmart/Forecast` | Agrega una columna `= Units × VNPK Cost ÷ VNPK Qty` y súmala | $70,173.84 |

**Tiendas con venta, sin repetir.** En Excel 365 escribe, en una celda vacía:
`=CONTAR(UNICOS(FILTRAR(O25:O1732; S25:S1732>0)))`
En la muestra, `Store Nbr` está en la columna O, `POS Qty` en la S y los datos van de la fila 25 a la 1732. En otro archivo, cambia las letras y las filas por las que veas. Según la configuración de tu Excel, el separador puede ser `;` o `,`.

**Dónde ver la cifra en el reporte:**
- **Sell out:** tarjetas de la página Sell out. «Mes actual» suma las dos cadenas; para ver una sola, elígela en el filtro Cadena.
- **Inventario:** tarjeta de la página Inventario, con el filtro Cadena.
- **Fill rate y Recship:** tarjetas de la página Abasto, sin elegir mes.

**Cuánta diferencia se acepta:** ninguna. La única diferencia válida es el redondeo, porque las tarjetas no muestran centavos. Cualquier otra diferencia es un error: ve a «Si algo no cuadra».

**Si hay varios archivos del mismo periodo:**
- Walmart sell out: si dos archivos cubren el mismo día, el reporte usa el más reciente. Sumar los dos archivos contaría ese día dos veces. Compara **día por día** con la consulta 2 del paso 5.
- Amazon: el reporte usa un archivo por mes, el marcado «Usado = Sí» en la página Control.

---

## Paso 3. Revisa el detalle (una vez por semana, o cuando algo no cuadre)

### Por producto
En la copia del archivo, inserta una **tabla dinámica**:
- Walmart: filas = `Item Nbr`; valores = suma de `POS Qty` y de `POS Sales`.
- Amazon: filas = `ASIN`; valores = suma de `Unidades pedidas` y de `Ganancia por pedidos`.

Compárala con la página **Revisión de datos** (en Power BI Desktop aparece en las pestañas, aunque esté oculta) o con la consulta 3 del paso 5. Para saber qué producto es cada artículo, busca el `Item Nbr` o el `ASIN` en la hoja Equivalencias del maestro.

Con las muestras, Walmart del 22 al 29/09:

| Item Nbr | Producto (maestro) | Piezas | Monto |
|---|---|---|---|
| 101248318 | Nebulizador Adulto Walmart (14660) | 47 | $34,019.21 |
| 101248319 | Nebulizador Pediatrico Elefante Celeste (13471) | 34 | $23,237.47 |
| 101248322 | Termómetro Pediatrico Cute Animals Panda (13595) | 236 | $25,300.60 |
| 101248323 | Termómetro Pediatrico Cute Animals Koala (13594) | 4 | $17.02 |
| 101618069 | Termómetro Pediatrico Cute Animals Osito (13593) | 42 | $4,495.91 |

### Una fila al azar
Elige una fila del archivo y búscala en el reporte con la consulta 7 del paso 5.

Ejemplo de las muestras: el 23/09/2026, la tienda 5817 (Walmart Express Axomiatla) vendió 1 Termómetro Osito (artículo 101618069) por $108.62.

---

## Paso 4. Revisa los cálculos (con la calculadora)

Las fórmulas están en `DEFINICIONES_INDICADORES.md`. Con las cifras del reporte:

| Indicador | Cómo comprobarlo | Ejemplo |
|---|---|---|
| Sell out total | Walmart + Amazon | $87,070 + $60,112 = $147,182 |
| Fill rate | Recibidas ÷ ordenadas | 15,126 ÷ 16,163 = 93.6 % |
| Piezas no surtidas | Ordenadas − recibidas | 16,163 − 15,126 = 1,037 |
| Cobertura | Inventario ÷ venta promedio de los **3 últimos meses cerrados** | 480 piezas; venta de junio, julio y agosto: 150, 170 y 160; promedio 160 → 3.0 meses → 🟢 |
| Crecimiento | Venta actual ÷ venta del año anterior − 1, **mismos días** | Del 1 al 29/09/2026 contra el 1 al 29/09/2025 |
| Año anterior de Amazon, mes en curso | El mes del año anterior × días cubiertos ÷ días del mes | Septiembre 2025 completo: 600 piezas. Si el archivo de 2026 llega al día 28: 600 × 28 ÷ 30 = 560 |
| Participación | Venta del producto ÷ venta total de lo filtrado | |
| «Mes actual» | Es el mes del último día con sell out | Datos al 29/09 → septiembre |

---

## Paso 5. Consultas para cuadrar en un minuto

Power BI Desktop puede mostrar las cifras en una tabla, sin armar gráficos:
1. En la barra izquierda, abre la **Vista de consultas DAX** (el ícono de una tabla con «DAX»). Si no aparece, actívala en Archivo → Opciones y configuración → Opciones → Características en versión preliminar.
2. Pega una de las consultas de abajo y presiona **Ejecutar** (o F5).
3. El resultado sale abajo, con decimales, y se puede copiar a Excel.

**1. Sell out por cadena y mes**
```
EVALUATE
SUMMARIZECOLUMNS (
    dimCadena[Cadena],
    Calendario[Inicio_mes],
    "Piezas", [Sell out piezas],
    "Monto", [Sell out monto],
    "Datos hasta", [Último día sell out]
)
ORDER BY dimCadena[Cadena], Calendario[Inicio_mes]
```
Muestras (con el historial de Amazon salen también los meses de 2024 y 2025):

| Cadena | Mes | Piezas | Monto | Datos hasta |
|---|---|---|---|---|
| Amazon | agosto 2026 | 564 | $60,542.83 | 31/08 |
| Amazon | septiembre 2026 | 692 | $60,111.75 | 28/09 |
| Walmart | septiembre 2026 | 363 | $87,070.21 | 29/09 |

**2. Sell out de Walmart por día.** Compara con el archivo filtrando la columna `Daily`, que viene como texto `aaaa/mm/dd`.
```
EVALUATE
SUMMARIZECOLUMNS (
    Calendario[Fecha],
    TREATAS ( { "Walmart" }, dimCadena[Cadena] ),
    "Piezas", [Sell out piezas],
    "Monto", [Sell out monto]
)
ORDER BY Calendario[Fecha]
```
Muestras, piezas del 22 al 29/09: 43, 46, 40, 47, 50, 53, 41 y 43.

**3. Sell out por producto y cadena.** Si aparece una fila con el producto en blanco, hay un código sin homologar.
```
EVALUATE
SUMMARIZECOLUMNS (
    dimCadena[Cadena],
    dimProducto[Codigo_ERP],
    dimProducto[Producto],
    "Piezas", [Sell out piezas],
    "Monto", [Sell out monto]
)
ORDER BY dimCadena[Cadena], dimProducto[Producto]
```

**4. Inventario y cobertura por producto**
```
EVALUATE
SUMMARIZECOLUMNS (
    dimCadena[Cadena],
    dimProducto[Producto],
    "Fecha de la foto", [Fecha de inventario],
    "Inventario", [Inventario piezas],
    "Venta promedio", [Venta promedio mensual piezas],
    "Cobertura", [Cobertura meses],
    "Estado", [Clasificación cobertura]
)
ORDER BY dimCadena[Cadena], dimProducto[Producto]
```

**5. Fill rate por mes de la orden.** En el archivo, `PO Order Date` viene como texto mes/día/año: `01/07/2026` es el **7 de enero**. Para un mes, filtra con «Comienza por» `09/`.
```
EVALUATE
SUMMARIZECOLUMNS (
    Calendario[Inicio_mes],
    "Ordenadas", [Piezas ordenadas],
    "Recibidas", [Piezas recibidas],
    "Fill rate", [Fill rate]
)
ORDER BY Calendario[Inicio_mes]
```

**6. Todos los totales en una fila**
```
EVALUATE
ROW (
    "WM sell out piezas", CALCULATE ( [Sell out piezas], dimCadena[Cadena] = "Walmart" ),
    "WM sell out monto", CALCULATE ( [Sell out monto], dimCadena[Cadena] = "Walmart" ),
    "AMZ sell out piezas", CALCULATE ( [Sell out piezas], dimCadena[Cadena] = "Amazon" ),
    "AMZ sell out monto", CALCULATE ( [Sell out monto], dimCadena[Cadena] = "Amazon" ),
    "WM inventario", CALCULATE ( [Inventario piezas], dimCadena[Cadena] = "Walmart" ),
    "AMZ inventario", CALCULATE ( [Inventario piezas], dimCadena[Cadena] = "Amazon" ),
    "Piezas ordenadas", [Piezas ordenadas],
    "Piezas recibidas", [Piezas recibidas],
    "Recship piezas", [Pronóstico piezas],
    "Recship monto", [Pronóstico monto]
)
```
Muestras: 363 · 87,070.21 · 7,481 · 1,068,205.79 · 27,281 · 3,198 · 16,163 · 15,126 · 552 · 70,173.84. El total de Amazon suma todos los meses cargados: los 20 del historial más agosto y septiembre de 2026 (sin historial serían 1,256 · 120,654.58).

**7. Una fila de Walmart.** Cambia la tienda y la fecha por las de la fila que elegiste en el archivo.
```
EVALUATE
SUMMARIZECOLUMNS (
    fSellOut[Fecha],
    fSellOut[Tienda_Nbr],
    fSellOut[Codigo_cadena],
    fSellOut[Tipo_venta],
    TREATAS ( { 5817 }, fSellOut[Tienda_Nbr] ),
    TREATAS ( { DATE ( 2026, 9, 23 ) }, fSellOut[Fecha] ),
    "Piezas", [Sell out piezas],
    "Monto", [Sell out monto]
)
```
Muestras: artículo 101618069, Regular, 1 pieza, $108.62.

---

## Paso 6. Contra el reporte anterior (fase de paralelo)

**No esperes que cuadre:** el reporte anterior tiene errores medidos (ver `DIAGNOSTICO_REPORTE_ACTUAL.md`). La meta es **explicar cada diferencia**, no eliminarla.

Anota cada diferencia en una tabla: cifra, valor anterior, valor nuevo, causa. Causas conocidas:

| Diferencia | Causa probable | Diagnóstico |
|---|---|---|
| Sell out de Walmart más alto en el anterior | Días pegados dos veces en el Excel consolidado | Error 4 |
| Sell out de Walmart más bajo en el anterior | Días que nunca se pegaron | Error 4 |
| Crecimiento distinto | El anterior compara contra el año anterior completo; el nuevo, contra los mismos días | Error 3 |
| Cobertura o estado de Walmart distinto | El anterior usa piezas por tienda; el nuevo, meses de inventario | Error 5 |
| Un producto con venta o inventario distinto | Códigos escritos a mano en el anterior; en el nuevo, la hoja Equivalencias | Errores 7, 8 y 9 |
| Cumplimiento que cambia según el día | Metas y filtro de fechas por día en el anterior | Error 2 |

Si una diferencia no se explica con esta tabla, repite los pasos 2 y 3 para esa cifra. Si el reporte nuevo cuadra con el archivo, el anterior es el que está mal. Si no cuadra, avísame.

---

## Rutina diaria antes de enviar (5 minutos)

1. **Página Control:**
   - semáforo en 🟢;
   - «Días sin sell out Walmart» en 0;
   - «Meses sin ventas de Amazon» en «Ninguno»;
   - «Códigos sin homologar» en «Ninguno»;
   - fechas de «Datos al» de ayer.
2. **Archivos leídos:** los archivos de hoy aparecen con «Usado = Sí».
3. **Una suma:** `POS Qty` y `POS Sales` del archivo nuevo de Walmart contra la consulta 2, para esos días.
4. **Una mirada a los gráficos:** un día sin venta, o con el triple de lo normal, casi siempre es una descarga incompleta o repetida. Revísala antes de enviar.

---

## Si algo no cuadra

Revisa en este orden:
1. **¿Validaste contra el archivo que usa el reporte?** Mira «Usado» en la página Control, y si hay días repetidos entre archivos.
2. **¿Hay un código sin homologar?** Si la página Control lo muestra, agrega el código a la hoja Equivalencias del maestro y vuelve a actualizar.
3. **¿Actualizaste Power BI después de agregar el archivo?** Inicio → Actualizar.
4. **¿Se abrió y se guardó la descarga?** Guardarla puede cambiar formatos y fechas. Vuelve a descargarla.
5. **Si nada de eso lo explica,** mándame la cifra, el valor que esperabas y el archivo.
