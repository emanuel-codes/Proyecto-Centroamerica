# Reporte Wellpro (versión nueva) — v0.4

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
  | **Control** | Semáforo con el motivo, fecha de los datos de cada fuente, días faltantes de Walmart, meses faltantes de Amazon, códigos sin homologar y lista de archivos leídos. **Revísala antes de enviar.** |
  | Revisión de datos | Oculta. Sirve para comprobar cifras en Power BI Desktop; no aparece en el reporte publicado. |

Todavía **no** incluye el sell in ni el inventario del ERP (faltan sus muestras).

**Novedades de la v0.4** (la v0.3 ya se probó en Power BI Desktop y sus cifras coinciden):
- **Historial de Amazon:** se copiaron a `Nueva versión/Amazon/Sell out` los 20 meses que el analista anterior descargó completos (de febrero a diciembre de 2024 y de febrero a octubre de 2025). Los demás meses hay que bajarlos de nuevo: ver «Carga del historial» en `GUIA_DESCARGAS.md`.
- **Crecimiento comparable:** el crecimiento contra el año anterior solo toma las cadenas que tienen historial. Mientras falte el de Walmart, la tarjeta dice «(solo Amazon)».
- **Página Control:** avisa qué meses de ventas de Amazon faltan o quedaron incompletos, y el semáforo dice el motivo.
- **A prueba de duplicados:** cada día de Walmart se toma de un solo archivo, el más reciente, aunque lo bajes dos veces. De cada mes se guarda solo la última foto de inventario. Los archivos que sobran salen con «Usado = No» en la página Control y se pueden mover a la subcarpeta `Respaldo`, que el reporte no lee.

## Cómo abrirlo

1. **Descarga el proyecto como ZIP** (con tu sesión de GitHub abierta):
   https://github.com/emanuel-codes/Proyecto-Centroamerica/archive/refs/heads/claude/confident-dijkstra-apgh2d.zip

   Extráelo siempre en `Documentos` (clic derecho → **Extraer todo**) y, si ya existía, acepta reemplazar los archivos. Así la ruta de los datos no cambia.
2. **Abre** `powerbi\Reporte Wellpro.pbip` con Power BI Desktop.
3. **Ruta de los datos.** El parámetro **RutaDatos** ya viene con la ruta de Manuel:
   `C:\Users\mpalacios\OneDrive - VISION MEDICA S.A\Documentos\Proyecto-Centroamerica-claude-confident-dijkstra-apgh2d\Nueva versión\`

   Si extraes el ZIP en otro lugar, cámbiala en **Inicio → Transformar datos → Editar parámetros**. Tiene que terminar en `\`.
4. **Actualiza** con Inicio → Actualizar.
5. **Revisa la página Control** y compara con las cifras de abajo.

Si aparece un error, copia el mensaje completo, o toma una captura, y mándamelo.

Para comprobar cada cifra por tu cuenta contra los archivos descargados, sigue [`GUIA_VALIDACION.md`](../GUIA_VALIDACION.md).

## Cómo se usan las páginas

- **Filtro Mes (página Sell out):** el reporte abre en **«Mes actual»**, que es el último mes con sell out. No hay que cambiarlo cada día: cuando llegan datos de un mes nuevo, «Mes actual» pasa a ser ese mes. Para ver otro mes, elígelo en el filtro; con Ctrl puedes elegir varios.
- **Ver gráficos en:** cambia los gráficos de la página Sell out entre monto (MXN) y piezas. Las tarjetas y la tabla siempre muestran las dos cosas.
- **Cadena, Familia y Producto** se mantienen al pasar de una página a otra.
- **Sell out por mes** muestra siempre los últimos 12 meses, sin importar el mes elegido.
- **Abasto:** el filtro «Mes de la orden» solo afecta al fill rate. Sin elegir ninguno, usa todas las órdenes descargadas. Los pedidos planeados (Recship) no se filtran por mes.

## Cifras esperadas con los datos actuales

Datos del repositorio: el historial completo de Walmart (del 01/10/2024 al 29/09/2026) y de Amazon (de febrero de 2024 al 28/09/2026). Si ya bajaste días más recientes, tus cifras del mes actual serán mayores.

| Página | Qué | Valor esperado |
|---|---|---|
| Control | Estado del reporte | 🟢 Listo para enviar (mientras los datos tengan 3 días o menos) |
| Control | Días sin sell out Walmart · Meses de Amazon por descargar · Códigos sin homologar | 0 · Ninguno · Ninguno |
| Sell out («Mes actual» = septiembre 2026) | Sell out (MXN) | $335,146 (Walmart $275,034 del 1 al 29/09 + Amazon $60,112 del 1 al 28/09) |
| Sell out («Mes actual») | Sell out (piezas) | 1,982 (Walmart 1,290 + Amazon 692) |
| Sell out («Mes actual») | Tiendas de Walmart con venta | 576 |
| Sell out («Mes actual») | Monto vs año anterior | ▼ 38.9 % |
| Sell out («Mes actual») | Piezas vs año anterior | ▼ 9.5 % |
| Inventario | Inventario (piezas) | 30,479 (Walmart 27,281 al 29/09 + Amazon 3,198 al 28/09) |
| Inventario | Venta promedio mensual (piezas) | 1,690 (Walmart 1,149 + Amazon 541; junio a agosto de 2026) |
| Inventario | Cobertura (meses) | 18.0 (Walmart 23.7 · Amazon 5.9) |
| Abasto (sin elegir mes) | Fill rate | 93.6 % (15,126 de 16,163 piezas; 1,037 no surtidas) |
| Abasto | Pedidos planeados | 552 piezas · $70,174 |

**Montos de Walmart con centavos:** Retail Link guarda POS Sales con formato de moneda sin decimales, y Power BI lo recibe como texto redondeado ($108.62 llega como «$109»). Por eso el reporte lee el monto exacto directo del archivo y lo comprueba fila por fila: solo lo usa si, redondeado al peso, da lo mismo que el valor de Power BI. Si algún monto no se puede leer exacto, la página Control se pone en 🟡 «Montos de Walmart sin decimales».

**De dónde sale la comparación con el año anterior:**
- Walmart: del 1 al 29 de septiembre de 2025 fueron 1,629 piezas y $482,042.
- Amazon: septiembre de 2025 en proporción a 28 de 30 días, 561.9 piezas y $66,628.
- Total: 2,190.9 piezas y $548,670. Contra eso, septiembre de 2026 da ▼ 9.5 % en piezas y ▼ 38.9 % en monto.

**Cobertura de Walmart por producto** (inventario al 29/09 ÷ venta promedio de junio a agosto):

| Producto | Inventario | Venta promedio | Cobertura |
|---|---|---|---|
| Termómetro Koala | 12 | 127 | **0.1 meses: riesgo de quiebre** |
| Termómetro Panda | 18,846 | 796 | 23.7 meses |
| Nebulizador Familiar | 3,573 | 143 | 24.9 meses |
| Nebulizador Elefante Azul | 3,660 | 82 | 44.5 meses |
| Termómetro Osito | 1,190 | — | Sin venta de junio a agosto: empezó a venderse en septiembre |

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
