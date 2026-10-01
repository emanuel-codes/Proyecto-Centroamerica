# Manual de operación — Reporte Wellpro

Para quien actualiza el reporte: Manuel y el analista que lo reemplaza en vacaciones.
El detalle de cada descarga (ajustes de Amazon y consultas de Retail Link) está en [`GUIA_DESCARGAS.md`](GUIA_DESCARGAS.md).

## Las 4 reglas

1. **Las descargas se guardan tal cual**, en su carpeta. No se abren para editar, no se renombran y no se copian a otro Excel.
2. **El único archivo que se edita a mano es el maestro**: `Maestros/Maestro_Wellpro.xlsx`.
3. **No se borra nada.** Lo que sobra va a la subcarpeta `Respaldo` de su carpeta, porque el reporte no lee esa subcarpeta.
4. **Si la página Control no está en 🟢, no se envía.** Primero se corrige con la tabla de abajo.

---

## Cada día (unos 10 minutos)

| # | Qué | Rango | Carpeta |
|---|---|---|---|
| 1 | Walmart sell out («Sell Out Act.») | Del día siguiente al último que bajaste hasta ayer. Normalmente es solo ayer; el lunes, de viernes a domingo. | `Walmart/Sell out` |
| 2 | Walmart inventario («Inventario en Tiendas MX Act.») | Ayer | `Walmart/Inventario` |
| 3 | Amazon ventas | Del día 1 del mes hasta ayer. El día 1 de cada mes, eso es el mes anterior completo. | `Amazon/Sell out` |
| 4 | Amazon inventario | Ayer | `Amazon/Inventarios` |

5. Abre el reporte → **Inicio → Actualizar**.
6. Revisa la página **Control**: semáforo en 🟢 y fechas de «Datos al» de ayer.
7. Envía o publica.

**No te preocupes por repetir:**
- si bajas un día dos veces, o un rango que se cruza con otro archivo, el reporte toma cada día del archivo más reciente;
- nada se duplica;
- si te falta un día, Control se pone en 🔴 y te dice qué falta.

## Cada lunes

| Qué | Rango | Carpeta |
|---|---|---|
| Walmart fill rate («Fill rate 0.2.1») | Las últimas 13 semanas de Walmart | `Walmart/Fill rate` |
| Walmart Recship («Recship Proxima 5 Sem») | Las próximas 5 semanas | `Walmart/Forecast` |

## El primer día hábil de cada mes (5 minutos más)

1. **Walmart:** baja el **mes anterior completo** en un solo archivo, a `Walmart/Sell out`.
2. **Actualiza** el reporte.
3. **Ordena:** en la página Control, tabla «Archivos leídos», los archivos que dicen **Usado = No** muévelos a la subcarpeta `Respaldo` de su carpeta. Son los diarios que reemplazó el archivo del mes y las fotos de inventario que no son de cierre de mes.

Si un mes no haces el paso 3, no pasa nada grave: el reporte sigue correcto, solo tarda más en actualizar.

---

## Qué hacer según la página Control

| Mensaje | Qué pasó | Qué hacer |
|---|---|---|
| 🟢 Listo para enviar | Todo bien | Enviar |
| 🔴 Faltan días de sell out de Walmart | Hay días sin archivo entre el primero y el último | Mira «Archivos leídos» y baja los días que faltan |
| 🔴 Faltan meses de ventas de Amazon | Hay meses sin archivo | La tarjeta «Meses de Amazon por descargar» dice cuáles. Bájalos completos. |
| 🔴 Hay meses de Amazon incompletos | Un mes cerrado no llega a su último día. Pasa cuando Amazon todavía no tenía el último día al descargar. | Baja ese mes completo otra vez |
| 🔴 Hay códigos sin homologar | Llegó un artículo o ASIN que no está en el maestro, casi siempre un **producto nuevo** | Sigue «Producto nuevo», abajo |
| 🟡 … atrasado | Una fuente tiene más de 3 días sin datos | Baja lo que falta de esa fuente |

---

## Mantenimiento

### Producto nuevo
Te enteras porque Control dice **«🔴 Hay códigos sin homologar»** y lista el código: un número de artículo de Walmart (por ejemplo, 101999999) o un ASIN de Amazon (por ejemplo, B0XXXXXXXX).

1. **Identifica el producto.** Busca el código en la descarga:
   - Walmart: columna `Signing Desc`. La columna `Vendor Stk Nbr` muchas veces trae el código del ERP.
   - Amazon: columna `Título del Producto`.
2. Abre el maestro y, si el producto **no existe** en la hoja **Productos**, agrega una fila:
   - `Codigo_ERP`: el código del ERP;
   - `Producto`: el nombre oficial;
   - `Familia` y `Marca`;
   - `EAN`;
   - `Activo` = `Sí`.
3. En la hoja **Equivalencias**, agrega una fila por cada código de cadena:

   | Cadena | Codigo_en_cadena | Tipo_codigo | Codigo_ERP |
   |---|---|---|---|
   | Walmart | el número de artículo (`Item Nbr`) | Item Nbr | el código del ERP |
   | Amazon | el ASIN | ASIN | el código del ERP |

4. Si tiene meta, agrégala en la hoja **Metas**.
5. **Guarda y cierra el maestro**, espera a que OneDrive sincronice (el visto verde) y **actualiza** el reporte. Control debe volver a 🟢.

**Cómo agregar filas:** escribe en la **primera fila vacía debajo de la tabla**. Excel agranda la tabla solo. No cambies el nombre de las hojas, de las tablas ni de las columnas.

### Otros casos

| Caso | Qué hacer |
|---|---|
| Un producto ya existente cambia de número de artículo o de ASIN | Agrega el código nuevo en Equivalencias. No borres el viejo: sirve para el historial. |
| Un producto se descontinúa | En Productos, `Activo` = `No`. Su historial se mantiene y deja de aparecer en los filtros. |
| Tienda nueva de Walmart | Nada: el reporte la toma sola de las descargas. |
| Metas del año nuevo | Hoja Metas: una fila por mes, producto y cliente. `Mes` = primer día del mes. |
| Otra persona abre el reporte en su computadora | **Inicio → Transformar datos → Editar parámetros → RutaDatos**: la carpeta `Nueva versión` en su equipo, terminada en `\`. |
| Retail Link o Amazon cambian columnas o nombres de reporte | Si Power BI marca un error al actualizar, no edites las consultas: manda la captura del error y el archivo nuevo. |

---

## Lo que nunca se hace

- Editar, renombrar o «limpiar» una descarga.
- Guardar copias, tablas dinámicas o archivos de trabajo dentro de `Nueva versión`, porque el reporte los leería.
- Borrar archivos: van a `Respaldo`.
- Corregir cifras a mano en Power BI. Si una cifra está mal, se corrige la fuente o el maestro.

Para comprobar cifras contra los archivos: [`GUIA_VALIDACION.md`](GUIA_VALIDACION.md).
