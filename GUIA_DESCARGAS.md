# Guía de descargas

Qué se descarga de cada fuente, cada cuánto y dónde se guarda. Está confirmado con las muestras de `Nueva versión/` (30/09/2026).

## Reglas

1. **Guardar el archivo tal como se descarga, en su carpeta.** No abrirlo para editarlo, no pegarlo en otro Excel y no convertirlo en tabla. Si lo abres para mirarlo, ciérralo **sin guardar**.
2. **No hace falta renombrar nada.** El reporte identifica cada archivo por lo que trae dentro:
   - Walmart: el título del reporte y las fechas de la consulta.
   - Amazon: el rango de fechas de la primera fila.
3. **Bajar dos veces el mismo periodo no genera errores.** Si dos archivos cubren los mismos días, el reporte se queda con el más reciente. Así, una descarga repetida no duplica ventas.
4. **Los archivos viejos no se borran.** Son el historial.

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
| **Ventas** | `Amazon/Sell out` | **El mes cerrado completo**, una vez al inicio del mes siguiente; y **el mes en curso hasta ayer**, en cada actualización. | Mes cerrado: una vez al mes. Mes en curso: en cada actualización. |
| **Inventario** | `Amazon/Inventarios` | Un solo día: el último disponible | En cada actualización |
| Órdenes de compra (fill rate) | — | — | **Sin acceso.** Ver «Pendientes» |

**Comprobado:** la descarga de agosto completo trae las mismas 564 unidades que el archivo que el analista armó a mano con 31 descargas diarias. El monto difiere en 9 MXN porque el analista redondeaba las cifras. Por eso, **una descarga al mes reemplaza a las 30 diarias.**

**Mes en curso:** cada vez que bajas el mes en curso hasta ayer, el reporte usa ese archivo y descarta los anteriores del mismo mes. No hace falta borrarlos.

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
| **Sell out** | «Sell Out Act.» | `Walmart/Sell out` | Desde el día siguiente a la última descarga hasta ayer, con detalle diario (*Daily*). Puede ser una semana en un solo archivo. | En cada actualización |
| **Inventario en tiendas** | «Inventario en Tiendas MX Act.» | `Walmart/Inventario` | Un día (*Pos Date* = ayer). Es la foto del inventario. | En cada actualización |
| **Recship** | «Recship Proxima 5 Sem» | `Walmart/Forecast` | Las próximas 5 semanas de Walmart | En cada actualización. El reporte usa solo el más reciente. |
| **Fill rate** | «Fill rate 0.2.1» | `Walmart/Fill rate` | Las semanas de Walmart que interesan; la muestra trae de la 202549 a la 202634 | Semanal |

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

### Amazon: faltan 10 meses
- **Ya están en `Amazon/Sell out`** los 20 meses que el analista anterior descargó completos: de febrero a diciembre de 2024 y de febrero a octubre de 2025.
- **Hay que bajar de nuevo:** enero de 2025, noviembre y diciembre de 2025, y de enero a julio de 2026. Para cada uno:
  - el **mes completo**, del día 1 al último;
  - los ajustes de siempre;
  - a la carpeta `Amazon/Sell out`.
- **Por qué no sirven los archivos del analista para esos meses:** traen por dentro un rango de fechas que no corresponde al mes, porque se armaron a mano sobre un archivo viejo (ver B8 en `DIAGNOSTICO_REPORTE_ACTUAL.md`). El reporte los pondría en el mes equivocado.
- **Cómo saber cuáles faltan:** la página Control los lista en «Meses sin ventas de Amazon». Cada mes que descargas desaparece de la lista; cuando queda en «Ninguno», terminaste.

### Walmart: sell out desde enero de 2025
- **Consulta:** la misma «Sell Out Act.», con detalle diario (*Daily*). Solo cambia el rango de *Pos Date*.
- **Rango:**
  - del **01/01/2025 al 21/09/2026**, porque la muestra ya cubre del 22 al 29/09;
  - si Retail Link lo permite, empieza en el **01/10/2024**. Así el gráfico de 12 meses también tiene año anterior en todos sus meses.
- **Un archivo por mes**, o por trimestre si Retail Link lo deja. Al reporte le da igual: junta todos y, si dos archivos repiten días, usa el más reciente. Por mes es más fácil repetir una descarga que falle.
- **No uses el Excel consolidado del analista anterior:** tiene días pegados dos veces y días faltantes (error 4 del diagnóstico).
- **Cómo comprobarlo:** en la página Control, «Días sin sell out Walmart» debe quedar en 0. Para cuadrar cada archivo, sigue el paso 2 de `GUIA_VALIDACION.md`.

### Inventario: no descargues fechas pasadas por ahora
- **Walmart:** la consulta «Inventario en Tiendas MX Act.» trae columnas *Curr* (*current*, es decir, actual). Con una fecha pasada, lo más probable es que traiga **el inventario de hoy con la fecha vieja**, y el reporte lo tomaría como si fuera de esa fecha.
  - Si el jefe quiere el historial de cierres de mes, prueba primero: baja el 31/08/2026 y compáralo con el archivo del 29/09.
  - Si las piezas son iguales, la consulta no sirve para historial y hay que buscar en Retail Link una columna de inventario histórico.
- **Amazon:** es opcional. Si quieres llenar el gráfico «Inventario al cierre de cada mes», baja el inventario del **último día de cada mes**, de octubre de 2025 a agosto de 2026.

### Orden sugerido
1. Los 10 meses de Amazon: son 10 descargas.
2. El sell out de Walmart, mes por mes.
3. Opcional: los cierres de mes del inventario de Amazon.

Con eso, el reporte queda listo para la fase de paralelo: comparar contra el reporte anterior y explicar cada diferencia (paso 6 de `GUIA_VALIDACION.md`).

---

## Pendientes

1. **Muestras del ERP:** sell in y kardex o inventario auxiliar.
2. **Fill rate de Amazon:** no tienes acceso a las órdenes de compra. Hay que decidir con el jefe entre:
   - quitar el indicador;
   - que alguien con acceso deje cada mes el export `POItemExport` en una carpeta `Amazon/Ordenes`.
3. **Semana 202618 del fill rate de Walmart:** agregarla a la consulta, o cambiarla a un rango relativo.
