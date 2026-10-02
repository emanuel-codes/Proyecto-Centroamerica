# Guía de descargas

Detalle de cada descarga: ajustes, consultas y carpetas. La rutina del día a día está en [`MANUAL_OPERACION.md`](MANUAL_OPERACION.md).

## Reglas

1. **Guardar el archivo tal como se descarga, en su carpeta.** No abrirlo para editarlo, no pegarlo en otro Excel y no convertirlo en tabla. Si lo abres para mirarlo, ciérralo **sin guardar**.
2. **No hace falta renombrar nada.** El reporte identifica cada archivo por lo que trae dentro:
   - Walmart: el título del reporte y las fechas de la consulta.
   - Amazon: el rango de fechas de la primera fila.
3. **Bajar dos veces el mismo periodo no duplica nada:**
   - Walmart sell out: cada día se toma de un solo archivo, el más reciente.
   - Amazon ventas: de cada mes se usa un solo archivo, el que llega más lejos.
   - Inventarios: una foto por día y, de cada mes, solo la última.
   - Fill rate: cada orden se toma de la descarga más reciente.
   - Recship: solo el archivo más reciente.
4. **Los archivos viejos no se borran.** Los que la página Control marca con «Usado = No» se mueven a la subcarpeta `Respaldo` de su carpeta, que el reporte no lee.

## Carpetas

```
Nueva versión/
├── Amazon/
│   ├── Sell out/
│   └── Inventarios/
├── Walmart/
│   ├── Sell out/
│   ├── Inventario/
│   ├── Forecast/          (Recship)
│   └── Fill rate/
├── ERP/
│   ├── Sell in/           (falta la muestra)
│   └── Inventario/        (falta la muestra)
└── Maestros/
    └── Maestro_Wellpro.xlsx
```

Cuando se decida dónde viven los datos (OneDrive o SharePoint de la empresa), se copia esta misma estructura. El reporte solo necesita saber dónde está la carpeta `Nueva versión`.

---

## Amazon Vendor Central

Ajustes de siempre: Programa *Retail*, Vista del distribuidor *Fabricación*, Visto por *ASIN*, *México*, Moneda *MXN*, rango *Personalizado*.

Amazon ya nombra los archivos con el rango de fechas, por ejemplo `Ventas_ASIN_Fabricación_Minorista_México_Personalizado_1-8-2026_31-8-2026.xlsx`.

| Descarga | Carpeta | Rango | Cada cuánto |
|---|---|---|---|
| **Ventas** | `Amazon/Sell out` | **Del día 1 al último día disponible**, dentro del mes de ese día. Amazon va 2 días atrás: si el último disponible es el 29/09, del 01/09 al 29/09; si es el 01/10, del 01/10 al 01/10. | Cada día |
| **Inventario** | `Amazon/Inventarios` | Un solo día: ayer | Cada día |
| Órdenes de compra (fill rate) | — | — | **Sin acceso.** Ver «Pendientes» |

**Comprobado:** la descarga de agosto completo trae las mismas 564 unidades que el archivo que el analista armó a mano con 31 descargas diarias. El monto difiere en 9 MXN porque el analista redondeaba las cifras. Por eso, **una descarga al mes reemplaza a las 30 diarias.**

**Mes en curso:** cada vez que bajas el mes en curso hasta el último día disponible, el reporte usa ese archivo y descarta los anteriores del mismo mes. Si Amazon todavía no tiene el último día cuando cambia el mes, la página Control avisa «meses de Amazon incompletos»: vuelve a bajar ese mes completo.

---

## Retail Link (Walmart México)

Retail Link nombra los archivos con el número de la solicitud, por ejemplo `1ug5pn1_114402242_171C28AE....xlsx`. **Se dejan así.**

Dentro del archivo, antes de los datos, vienen:
- el nombre del reporte;
- la fecha y hora de la solicitud;
- las columnas;
- los filtros, incluido el rango de fechas.

El reporte toma de ahí lo que necesita.

Aunque algunos terminan en `.xls`, por dentro son archivos de Excel modernos. Power BI los lee sin problema.

| Descarga | Nombre en Retail Link | Carpeta | Rango | Cada cuánto |
|---|---|---|---|---|
| **Sell out** | «Sell Out Act.» | `Walmart/Sell out` | Desde el día siguiente a la última descarga hasta ayer, con detalle diario (*Daily*). El primer día hábil del mes, además, el mes anterior completo en un archivo. | Cada día, y el mes completo una vez al mes |
| **Inventario en tiendas** | «Inventario en Tiendas MX Act.» | `Walmart/Inventario` | Un día (*Pos Date* = ayer). Es la foto del inventario. | Cada día |
| **Recship** | «Recship Proxima 5 Sem» | `Walmart/Forecast` | Las próximas 5 semanas de Walmart | Cada lunes. El reporte usa solo el más reciente. |
| **Fill rate** | «Fill rate 0.2.1» | `Walmart/Fill rate` | Las últimas 13 semanas de Walmart (la muestra trae de la 202549 a la 202634) | Cada lunes |

Lo que se vio en las muestras:
- **Sell out, del 22/09 al 29/09:**
  - 1,708 filas, 8 días, 363 piezas y 87,070 MXN;
  - incluye filas con venta 0 y ventas de liquidación (*Clearance Item*);
  - sin duplicados.
- **Inventario al 29/09:** 4,491 filas, por tienda y artículo.
- **Recship, creado el 30/09:** es por centro de distribución, no por tienda, con las fechas de pedido y de recepción planeadas.
- **Fill rate (enero a septiembre de 2026):**
  - 540 líneas de órdenes, todas de reabastecimiento a tienda (*POS REPLEN*);
  - 16,163 piezas ordenadas y 15,126 recibidas, un **93.6 %**.
- **Cuidado con las semanas escritas a mano:** las consultas de fill rate y Recship tienen las semanas de Walmart escritas una por una.
  - En la de fill rate **falta la semana 202618** (principios de mayo de 2026), así que esas órdenes nunca se descargan.
  - Si Retail Link lo permite, conviene cambiarlas a un rango relativo, por ejemplo "últimas 13 semanas" o "próximas 5 semanas", para no editarlas en cada descarga.
- **`Vendor Stk Nbr`:** trae el código del ERP en 4 artículos (14660, 13471, 13595, 13594). El Osito trae otro código, «MTB132FA». Por eso la llave para Walmart es el **número de artículo** (*Item Nbr*), que ya está en la hoja Equivalencias del maestro.

---

## ERP One Goal

| Descarga | Carpeta | Qué pedir | Cada cuánto |
|---|---|---|---|
| **Sell in** | `ERP/Sell in` | Las facturas del periodo, con **código de producto**, cliente, fecha, cantidad, precio y, si se puede, número de factura. | En cada actualización (el mes en curso) |
| **Inventario** | `ERP/Inventario` | El kardex o el inventario auxiliar, con código de producto y almacén | En cada actualización |

**Faltan las muestras.** Súbelas tal como las exportas hoy, aunque todavía no traigan el código.

---

## Carga del historial (una sola vez)

Para comparar con el año anterior, calcular la cobertura y mostrar la tendencia de 12 meses, el reporte necesita **historial de ventas**. El inventario no necesita historial: se acumula solo con las descargas de cada actualización.

### Amazon: completo
- `Amazon/Sell out` tiene los 32 meses, de febrero de 2024 a septiembre de 2026, sin huecos.
- 20 meses vienen del analista anterior: son los que había descargado completos.
- Los otros 12 se volvieron a descargar, porque los del analista se habían armado a mano y su rango de fechas no correspondía al mes (ver B8 en `DIAGNOSTICO_REPORTE_ACTUAL.md`).

### Walmart: sell out desde octubre de 2024
- **Consulta:** la misma «Sell Out Act.», con detalle diario (*Daily*). Solo cambia el rango de *Pos Date*.
- **Rango:**
  - del **01/10/2024 al 21/09/2026**, porque la muestra ya cubre del 22 al 29/09. Así el gráfico de 12 meses tiene año anterior en todos sus meses;
  - como mínimo, desde el **01/09/2025**, sin huecos.
- **Un archivo por mes**, o por trimestre si Retail Link lo deja. Al reporte le da igual: junta todos y, si dos archivos repiten días, usa el más reciente. Por mes es más fácil repetir una descarga que falle.
- **No uses el Excel consolidado del analista anterior:** tiene días pegados dos veces y días faltantes (error 4 del diagnóstico).
- **Cómo comprobarlo:** en la página Control, «Días sin sell out Walmart» debe quedar en 0. Para cuadrar cada archivo, sigue el paso 2 de `GUIA_VALIDACION.md`.

### Inventario: no descargues fechas pasadas por ahora
- **Walmart:** la consulta «Inventario en Tiendas MX Act.» trae columnas *Curr* (*current*, es decir, actual). Con una fecha pasada, lo más probable es que traiga **el inventario de hoy con la fecha vieja**, y el reporte lo tomaría como si fuera de esa fecha.
  - Si el jefe quiere el historial de cierres de mes, prueba primero: baja el 31/08/2026 y compáralo con el archivo del 29/09.
  - Si las piezas son iguales, la consulta no sirve para historial y hay que buscar en Retail Link una columna de inventario histórico.
- **Amazon:** es opcional. Si quieres llenar el gráfico «Inventario al cierre de cada mes», baja el inventario del **último día de cada mes**, de octubre de 2025 a agosto de 2026.

### Orden sugerido
1. ~~Los 10 meses de Amazon~~ (listo).
2. El sell out de Walmart, por mes o por trimestre.
3. Opcional: los cierres de mes del inventario de Amazon.

Con eso, el reporte queda listo para la fase de paralelo: comparar contra el reporte anterior y explicar cada diferencia (paso 6 de `GUIA_VALIDACION.md`).

---

## Pendientes

1. **Muestras del ERP:** sell in y kardex o inventario auxiliar.
2. **Fill rate de Amazon:** no tienes acceso a las órdenes de compra. Hay que decidir con el jefe entre:
   - quitar el indicador;
   - que alguien con acceso deje cada mes el export `POItemExport` en una carpeta `Amazon/Ordenes`.
3. **Semana 202618 del fill rate de Walmart:** agregarla a la consulta, o cambiarla a un rango relativo.
4. ~~Montos de Walmart redondeados~~ **Resuelto:** el reporte lee POS Sales exacto directo del archivo, porque Retail Link lo guarda con formato sin decimales.
