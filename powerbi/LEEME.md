# Reporte Wellpro (versión nueva) — v0.5

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

  | Página | Para quién | Qué muestra |
  |---|---|---|
  | **Sell out** | Jefe | Panel ejecutivo: título que resume el mes («Octubre 2026: $88,971.48, ▼ 50% vs año anterior») y qué lo explica; tarjetas de monto, piezas, inventario en cadenas y tiendas de Walmart con venta, cada una contra el año anterior; gráfico de 12 meses con la variación %; «¿Qué explica la caída?» por familia; tabla por producto. |
  | **Inventario** | Jefe | Semáforo y prioridades: título con piezas y meses de cobertura, y la alerta del producto en riesgo; tarjetas de inventario contra el mes anterior, cobertura, productos por atender y tiendas de Walmart con inventario; cobertura por producto; tiendas de Walmart con inventario contra tiendas que venden; «Atender primero», ordenado por urgencia; tiendas que venden sin inventario. |
  | **Abasto** | Jefe | Fill rate de Walmart por mes y por producto, y los pedidos planeados del Recship. |
  | **Control** | Analistas | Semáforo con el motivo, fecha de los datos de cada fuente, días faltantes de Walmart, meses faltantes de Amazon, códigos sin homologar, lista de archivos leídos y sell out diario de Walmart. **Revísala antes de enviar.** |
  | Revisión de datos | Analistas | Para comprobar cifras por producto. |

  **Control y Revisión de datos están ocultas:** no aparecen en los botones ni en el reporte publicado, así que el jefe no las ve. En Power BI Desktop siguen en las pestañas de abajo (con un ícono de ojo tachado); ahí se abren con un clic.

Todavía **no** incluye el sell in ni el inventario del ERP (faltan sus muestras).

**Novedades de la v0.5** (del 3 al 9 de octubre de 2026; desde aquí la copia local de Manuel es la principal):
- **Sell out, panel ejecutivo:** título y subtítulo automáticos, tarjetas con su variación contra el año anterior y minigráfico de 12 meses, gráfico mensual con la línea de variación %, «¿Qué explica la caída?» por familia y tabla por producto nueva. Sale el filtro Producto de esta página.
- **Monto de sell out completo, con centavos**, en la tarjeta, en su referencia del año anterior y en el título, para cuadrar al centavo contra los archivos.
- **Sale la tarjeta «Precio promedio por pieza»:** el promedio se movía por la mezcla de productos, no por el precio (en octubre bajaba 39 % aunque los precios de los productos principales subieron). Entra «Inventario en cadenas» con sus meses de cobertura.
- **Inventario, semáforo y prioridades:** página nueva completa (ver la tabla de arriba). Sale el gráfico «Inventario al cierre de cada mes» hasta que haya unos 6 meses de historial de inventario.
- **Control oculta** y fuera de los botones; recibe el gráfico de sell out diario de Walmart.
- **El reporte abre con Cadena = Todas** en Sell out e Inventario.
- **Modelo:** 29 medidas en la carpeta «6. Panel ejecutivo» y 20 en «7. Panel inventario» (101 medidas en total). No cambió ninguna medida anterior, salvo el texto de «Título sell out» y «Ref año anterior monto» (ahora con la cifra completa).

## Cómo abrirlo

**En la computadora de Manuel:** abre `powerbi\Reporte Wellpro.pbip` desde la carpeta de siempre. **No vuelvas a extraer encima el ZIP de GitHub:** reemplazaría los archivos y se perderían los cambios hechos en Power BI Desktop. Para subir cambios a GitHub se usa el clon de Git en `C:\Users\mpalacios\gitpc` (ver `CLAUDE.md`).

**En otra computadora** (por ejemplo, el analista que cubre vacaciones):
1. **Descarga el proyecto como ZIP** (con tu sesión de GitHub abierta):
   https://github.com/emanuel-codes/Proyecto-Centroamerica/archive/refs/heads/claude/confident-dijkstra-apgh2d.zip

   Extráelo en una carpeta nueva.
2. **Abre** `powerbi\Reporte Wellpro.pbip` con Power BI Desktop.
3. **Ruta de los datos.** El parámetro **RutaDatos** viene con la ruta de Manuel:
   `C:\Users\mpalacios\OneDrive - VISION MEDICA S.A\Documentos\Proyecto-Centroamerica-claude-confident-dijkstra-apgh2d\Nueva versión\`

   Cámbiala a tu carpeta `Nueva versión` en **Inicio → Transformar datos → Editar parámetros**. Tiene que terminar en `\`.
4. **Actualiza** con Inicio → Actualizar.
5. **Revisa la página Control** y compara con las cifras de abajo.

Si aparece un error, copia el mensaje completo, o toma una captura, y mándamelo.

Para comprobar cada cifra por tu cuenta contra los archivos descargados, sigue [`GUIA_VALIDACION.md`](../GUIA_VALIDACION.md).

## Cómo se usan las páginas

- **Filtro Mes (página Sell out):** el reporte abre en **«Mes actual»**, que es el último mes con sell out. No hay que cambiarlo cada día: cuando llegan datos de un mes nuevo, «Mes actual» pasa a ser ese mes. Para ver otro mes, elígelo en el filtro; con Ctrl puedes elegir varios.
- **Ver gráficos en:** cambia los gráficos de la página Sell out entre monto (MXN) y piezas. Las tarjetas y la tabla siempre muestran las dos cosas.
- **Cadena y Familia** se mantienen al pasar de una página a otra. **Producto** está en Inventario y Abasto.
- **Sell out por mes** y los minigráficos de las tarjetas muestran siempre los últimos 12 meses, sin importar el mes elegido. El último punto es el mes en curso, todavía incompleto.
- **Inventario** no tiene filtro de mes: siempre es la última foto de cada cadena. La tarjeta de inventario se compara con la última foto del mes anterior.
- **Tiendas de Walmart** (tarjeta y gráfico de Inventario, tabla de tiendas sin inventario): con Cadena = Amazon dicen «Solo aplica a Walmart».
- **Abasto:** el filtro «Mes de la orden» solo afecta al fill rate. Sin elegir ninguno, usa todas las órdenes descargadas. Los pedidos planeados (Recship) no se filtran por mes.

## Cifras esperadas con los datos actuales

Datos al **07/10/2026 de Walmart** y al **06/10/2026 de Amazon**. Si ya bajaste días más recientes, tus cifras del mes actual serán mayores.

| Página | Qué | Valor esperado |
|---|---|---|
| Control | Estado del reporte | 🟢 Listo para enviar (mientras los datos tengan 3 días o menos) |
| Control | Días sin sell out Walmart · Meses de Amazon por descargar · Códigos sin homologar | 0 · Ninguno · Ninguno |
| Sell out («Mes actual» = octubre 2026) | Sell out (MXN) | $88,971.48 (Walmart $76,000.15 del 1 al 7/10 + Amazon $12,971.33 del 1 al 6/10) |
| Sell out («Mes actual») | Sell out (piezas) | 447 (Walmart 324 + Amazon 123) |
| Sell out («Mes actual») | Tiendas de Walmart con venta | 239 (vs 348 año anterior) |
| Sell out («Mes actual») | Monto vs año anterior | ▼ 49.5 % (vs $176,204.53) |
| Sell out («Mes actual») | Piezas vs año anterior | ▼ 17.5 % (vs 542) |
| Sell out (filtro Mes = septiembre 2026) | Sell out cerrado | Walmart $289,177.48 y 1,355 piezas · Amazon $67,898.91 y 757 piezas |
| Inventario | Inventario (piezas) | 31,550 (Walmart 28,513 al 07/10 + Amazon 3,037 al 06/10), ▲ 3.6 % vs 30,449 al cierre de septiembre |
| Inventario | Venta promedio mensual (piezas) | 1,893 (Walmart 1,261 + Amazon 632; julio a septiembre de 2026) |
| Inventario | Cobertura (meses) | 16.7, sobre stock (Walmart 22.6 · Amazon 4.8) |
| Inventario | Productos por atender | 4 (1 en riesgo: Termómetro Koala en Walmart · 3 sin inventario en Amazon) |
| Inventario | Tiendas de Walmart con inventario | 1,451; 596 vendieron en los últimos 28 días (41 %) |
| Inventario | Tiendas que venden sin inventario | 31 casos |
| Abasto (sin elegir mes) | Fill rate | 95.4 % (16,749 de 17,548 piezas; 799 no surtidas) |
| Abasto | Pedidos planeados (Recship del 09/10) | 66 piezas · $33,396.30 (solo nebulizadores) |

Las dos descargas nuevas de Walmart (del 1 al 7/10 y septiembre completo) se sumaron directo del archivo y cuadran al centavo con el reporte.

**Montos de Walmart con centavos:** Retail Link guarda POS Sales con formato de moneda sin decimales, y Power BI lo recibe como texto redondeado ($108.62 llega como «$109»). Por eso el reporte lee el monto exacto directo del archivo y lo comprueba fila por fila: solo lo usa si, redondeado al peso, da lo mismo que el valor de Power BI. Si algún monto no se puede leer exacto, la página Control se pone en 🟡 «Montos de Walmart sin decimales».

**De dónde sale la comparación con el año anterior (octubre):**
- Walmart: del 1 al 7 de octubre de 2025 fueron 457 piezas y $163,941.22.
- Amazon: octubre de 2025 en proporción a 6 de 31 días, 84.8 piezas y $12,263.31.
- Total: 541.8 piezas y $176,204.53. Contra eso, octubre de 2026 da ▼ 17.5 % en piezas y ▼ 49.5 % en monto.

**Cobertura de Walmart por producto** (inventario al 07/10 ÷ venta promedio de julio a septiembre):

| Producto | Inventario | Venta promedio | Cobertura | Tiendas con inventario · que vendieron en 28 días |
|---|---|---|---|---|
| Termómetro Koala | 10 | 72 | **0.1 meses: riesgo de quiebre** | 7 · 9 |
| Termómetro Panda | 19,117 | 953 | 20.1 meses | 1,078 · 445 |
| Nebulizador Adulto Walmart | 3,586 | 135 | 26.6 meses | 1,435 · 150 |
| Nebulizador Elefante Celeste | 3,659 | 71 | 51.8 meses | 1,417 · 91 |
| Termómetro Osito | 2,141 | 31 | 69.1 meses | 351 · 106 |

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
- **Medidas:** en `_Medidas`, por carpeta: 1. Sell out, 2. Inventario en cadenas, 3. Fill rate, 4. Pronóstico, 5. Metas, 6. Panel ejecutivo (textos, colores y referencias de la página Sell out), 7. Panel inventario (lo mismo para la página Inventario) y 9. Control. Siguen la propuesta de `DEFINICIONES_INDICADORES.md` y se ajustan cuando el jefe la apruebe.
- **Orden de «Atender primero»:** la columna Estado es la medida `Estado por urgencia`, un número que ordena por urgencia (riesgo de quiebre, sin inventario, sobre stock de mayor a menor cobertura, sin rotación y saludable) y que, con un formato dinámico, se muestra como el texto del estado.
- **Diseño:** tema `TemaWellpro.json` (rojo Wellpro para el año actual, gris para el año anterior, azul para Walmart y ámbar para Amazon) y logo en `StaticResources/RegisteredResources`.
