# Reporte Wellpro (versión nueva) — v0.1

Proyecto de Power BI (`.pbip`) de la versión nueva. En esta primera entrega:

- **Lee directo de las carpetas**, sin pasos manuales:
  - Walmart: sell out, inventario en tiendas, fill rate y forecast (Recship);
  - Amazon: ventas e inventario;
  - el archivo maestro.
- **Aplica solo las reglas de `GUIA_DESCARGAS.md`:**
  - no importa el nombre del archivo;
  - si dos descargas cubren los mismos días, usa la más reciente;
  - los códigos se homologan con la hoja Equivalencias del maestro.
- **Trae dos páginas:**
  - **Control:** semáforo, fecha de los datos de cada fuente, días faltantes, códigos sin homologar y lista de archivos leídos.
  - **Revisión de datos:** sell out, inventario y cobertura por producto y cadena, para comprobar las cifras.

Todavía **no** incluye el sell in ni el inventario del ERP (faltan sus muestras), ni las páginas finales del reporte.

## Cómo abrirlo

1. **Baja el repositorio a tu computadora** (solo la primera vez). En PowerShell, dentro de la carpeta donde lo quieras guardar:
   ```powershell
   git clone -b claude/confident-dijkstra-apgh2d https://github.com/emanuel-codes/Proyecto-Centroamerica.git
   ```
   Para traer cambios nuevos más adelante, entra a la carpeta `Proyecto-Centroamerica` y ejecuta `git pull`.
2. **Abre** `Proyecto-Centroamerica\powerbi\Reporte Wellpro.pbip` con Power BI Desktop.
3. **Indica dónde están los datos.** Ve a **Inicio → Transformar datos → Editar parámetros** y en **RutaDatos** escribe la ruta completa de la carpeta `Nueva versión`, terminada en `\`. Por ejemplo:
   `C:\Users\TuUsuario\Documents\Proyecto-Centroamerica\Nueva versión\`
4. **Actualiza** con Inicio → Actualizar.
5. **Revisa la página Control** y compara con las cifras de abajo.

Si aparece un error, copia el mensaje completo, o toma una captura, y mándamelo.

## Cifras esperadas con las muestras actuales

| Qué | Valor esperado |
|---|---|
| Estado del reporte | 🟢 Listo para enviar (con datos al 29/09) |
| Sell out Walmart, del 22 al 29/09 | 363 piezas · $87,070 |
| Sell out Amazon, agosto 2026 | 564 piezas · $60,543 |
| Sell out Amazon, del 1 al 28/09/2026 | 692 piezas · $60,112 |
| Inventario Walmart al 29/09 | 27,281 piezas en 1,449 tiendas |
| Inventario Amazon al 28/09 | 3,198 unidades aptas para la venta |
| Fill rate Walmart (órdenes de enero a septiembre de 2026) | 93.6 % (15,126 de 16,163 piezas) |
| Pronóstico Recship (creado el 30/09) | 552 piezas · $70,174 |
| Metas (todas) | $110,714,326 |
| Días sin sell out Walmart | 0 |
| Filas sin homologar | 0 |

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
  | Medidas | `_Medidas` |

- **Medidas:** en `_Medidas`, por carpeta: Sell out, Inventario en cadenas, Fill rate, Pronóstico, Metas y Control. Siguen la propuesta de `DEFINICIONES_INDICADORES.md` y se ajustan cuando el jefe la apruebe.
