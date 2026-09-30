# Reporte Wellpro (versión nueva) — v0.3

Proyecto de Power BI (`.pbip`) de la versión nueva.

- **Lee directo de las carpetas**, sin pasos manuales:
  - Walmart: sell out, inventario en tiendas, fill rate y forecast (Recship);
  - Amazon: ventas e inventario;
  - el archivo maestro.
- **Aplica solo las reglas de `GUIA_DESCARGAS.md`:**
  - no importa el nombre del archivo;
  - si dos descargas cubren los mismos días, usa la más reciente;
  - los códigos se homologan con la hoja Equivalencias del maestro.
- **Páginas** (con los colores y el logo de Wellpro):

  | Página | Qué muestra |
  |---|---|
  | **Sell out** | Venta de Walmart y Amazon en monto y piezas, contra el año anterior. Por mes, por familia y cadena, por producto, y el diario de Walmart. |
  | **Inventario** | Inventario en las cadenas, venta promedio, cobertura y estado de cada producto; inventario al cierre de cada mes; tiendas de Walmart sin inventario que sí venden. |
  | **Abasto** | Fill rate de Walmart por mes y por producto, y los pedidos planeados del Recship. |
  | **Control** | Semáforo, fecha de los datos de cada fuente, días faltantes, códigos sin homologar y lista de archivos leídos. **Revísala antes de enviar.** |
  | Revisión de datos | Oculta. Sirve para comprobar cifras en Power BI Desktop; no aparece en el reporte publicado. |

Todavía **no** incluye el sell in ni el inventario del ERP (faltan sus muestras).

## Cómo abrirlo

1. **Descarga el proyecto como ZIP** (con tu sesión de GitHub abierta):
   https://github.com/emanuel-codes/Proyecto-Centroamerica/archive/refs/heads/claude/confident-dijkstra-apgh2d.zip

   Extráelo siempre en `Documentos` (clic derecho → **Extraer todo**) y, si ya existía, acepta reemplazar los archivos. Así la ruta de los datos no cambia.
2. **Abre** `powerbi\Reporte Wellpro.pbip` con Power BI Desktop.
3. **Ruta de los datos.** El parámetro **RutaDatos** ya viene con la ruta de Manuel:
   `C:\Users\mpalacios\OneDrive - VISION MEDICA S.A\Documentos\Proyecto-Centroamerica-claude-confident-dijkstra-apgh2d\Nueva versión\`

   Si extraes el ZIP en otro lugar, cámbiala en **Inicio → Transformar datos → Editar parámetros**. Tiene que terminar en `\`.
4. **Actualiza** con Inicio → Actualizar. Hazlo aunque ya lo hayas actualizado antes: la v0.3 agrega columnas nuevas al calendario.
5. **Revisa la página Control** y compara con las cifras de abajo.

Si aparece un error, copia el mensaje completo, o toma una captura, y mándamelo.

Para comprobar cada cifra por tu cuenta contra los archivos descargados, sigue [`GUIA_VALIDACION.md`](../GUIA_VALIDACION.md).

## Cómo se usan las páginas

- **Filtro Mes (página Sell out):** el reporte abre en **«Mes actual»**, que es el último mes con sell out. No hay que cambiarlo cada día: cuando llegan datos de un mes nuevo, «Mes actual» pasa a ser ese mes. Para ver otro mes, elígelo en el filtro; con Ctrl puedes elegir varios.
- **Ver gráficos en:** cambia los gráficos de la página Sell out entre monto (MXN) y piezas. Las tarjetas y la tabla siempre muestran las dos cosas.
- **Cadena, Familia y Producto** se mantienen al pasar de una página a otra.
- **Sell out por mes** muestra siempre los últimos 12 meses, sin importar el mes elegido.
- **Abasto:** el filtro «Mes de la orden» solo afecta al fill rate. Sin elegir ninguno, usa todas las órdenes descargadas. Los pedidos planeados (Recship) no se filtran por mes.

## Cifras esperadas con las muestras actuales

| Página | Qué | Valor esperado |
|---|---|---|
| Control | Estado del reporte | 🟢 Listo para enviar (con datos al 29/09) |
| Control | Días sin sell out Walmart · Filas sin homologar | 0 · 0 |
| Sell out («Mes actual» = septiembre 2026) | Sell out (MXN) | $147,182 (Walmart $87,070 del 22 al 29/09 + Amazon $60,112 del 1 al 28/09) |
| Sell out («Mes actual») | Sell out (piezas) | 1,055 (Walmart 363 + Amazon 692) |
| Sell out («Mes actual») | Tiendas de Walmart con venta | 260 |
| Sell out | Monto y piezas vs año anterior | «Sin año anterior» hasta que se descargue el historial |
| Sell out, eligiendo «Ago 2026» | Sell out | Amazon: 564 piezas · $60,543 |
| Inventario | Inventario (piezas) | 30,479 (Walmart 27,281 al 29/09 + Amazon 3,198 al 28/09) |
| Abasto (sin elegir mes) | Fill rate | 93.6 % (15,126 de 16,163 piezas; 1,037 no surtidas) |
| Abasto | Pedidos planeados | 552 piezas · $70,174 |

**Con las muestras actuales es normal que:**
- los gráficos por mes tengan solo agosto y septiembre, y el diario de Walmart solo del 22 al 29/09;
- la venta promedio y la cobertura salgan en blanco o bajas: se calculan con los 3 últimos meses cerrados y todavía no hay historial;
- no haya comparación con el año anterior.

Todo eso se llena solo cuando se descargue el historial (sell out de Walmart y ventas de Amazon desde enero de 2025).

## Cómo está armado

- **Parámetro `RutaDatos`:** la carpeta con las subcarpetas `Amazon`, `Walmart`, `ERP` y `Maestros`. Cuando los datos pasen a SharePoint, solo cambia la consulta `Archivos`.
- **Funciones:**
  - `fnRetailLink` lee el encabezado de Retail Link (nombre del reporte, fecha de solicitud y rango consultado) y los datos.
  - `fnAmazon` lee la primera fila de Amazon (rango de fechas y fecha de actualización) y los datos.
- **Tablas:**

  | Tipo | Tablas |
  |---|---|
  | Hechos | `fSellOut` (Walmart por día y tienda, Amazon por mes), `fInventarioCadena`, `fFillRate`, `fRecship`, `Metas` |
  | Dimensiones | `Calendario`, `dimProducto`, `dimCadena`, `dimTienda` |
  | Control | `ctlArchivos` |
  | Selector | `sMetrica` (monto o piezas en los gráficos de Sell out) |
  | Medidas | `_Medidas` |

- **Calendario:** las columnas `Meses_atras` y `Periodo` se recalculan en cada actualización con el último día de sell out. Por eso el filtro guardado en «Mes actual» nunca se desactualiza.
- **Medidas:** en `_Medidas`, por carpeta: Sell out, Inventario en cadenas, Fill rate, Pronóstico, Metas y Control. Siguen la propuesta de `DEFINICIONES_INDICADORES.md` y se ajustan cuando el jefe la apruebe.
- **Diseño:** tema `TemaWellpro.json` (rojo Wellpro para el año actual, gris para el año anterior, azul para Walmart y ámbar para Amazon) y logo en `StaticResources/RegisteredResources`.
