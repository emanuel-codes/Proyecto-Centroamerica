# Presentación del viernes: primer vistazo

## Antes del viernes (en este orden)

1. ~~Baja el ZIP nuevo y actualiza~~ **Listo:** Control en 🟢.
   - Para hablar de los errores del reporte actual, usa [`ERRORES_REPORTE_ACTUAL.md`](ERRORES_REPORTE_ACTUAL.md).
2. ~~Amazon, 10 meses completos~~ **Listo:** ya están en `Amazon/Sell out` y llegan con el ZIP.
3. ~~Walmart sell out, historial~~ **Listo:** del 01/10/2024 al 29/09/2026, sin huecos.
4. **El jueves, la rutina diaria** del manual (`MANUAL_OPERACION.md`). Así llegas al viernes con datos al día.
5. **El viernes temprano, guarda capturas** de cada página como respaldo, por si algo falla en vivo.
6. **Deja sin bajar el sell out de Walmart de ayer**, para descargarlo en vivo.

## Apertura (1 minuto)

> «Hoy les muestro la **primera versión** del reporte nuevo. Está completo para **Walmart y Amazon**. Falta el **sell in del ERP**, que es lo siguiente que voy a cargar en cuanto tenga el acceso.
>
> Para llegar aquí:
> - **Reconstruí el historial completo:** dos años de sell out de Walmart, desde octubre de 2024, en 11 consultas de Retail Link (casi 200 mil filas), y 32 meses de ventas de Amazon. Tuve que volver a bajar 10 meses de Amazon, porque los archivos que existían estaban armados a mano.
> - **Validé cada cifra contra los archivos originales:** cuadra **al peso**. Incluso encontré que Retail Link exporta las ventas sin decimales, y el reporte ahora lee el valor exacto.
> - **Comparé contra el reporte actual:** coincide exacto donde los datos estaban bien, y encontré los errores que explican las diferencias: días repetidos, días faltantes y meses incompletos.
>
> Lo más importante es que la actualización ya no depende de copiar y pegar: se guardan las descargas y el reporte se revisa solo antes de enviarse.»

## Guion (15 minutos)

| Min | Qué mostrar | Qué decir |
|---|---|---|
| 1 | — | Hoy el reporte toma unas 4 horas al día y se reenvía porque se corrigen errores. Casi todos vienen de pasos manuales. Ejemplo comprobado: en noviembre de 2025, el sell out de Walmart del reporte actual está inflado un 31 % por días pegados dos veces. |
| 2 | La carpeta `Nueva versión` | Cada descarga se guarda tal cual, en su carpeta. Sin copiar, pegar ni renombrar. Lo único que se edita a mano es el maestro. |
| 4 | **Carga en vivo:** bajar el sell out de Walmart de ayer, guardarlo en `Walmart/Sell out` y **Actualizar**. La actualización tarda unos 4 minutos: mientras corre, explica la carpeta y el maestro. | Cambia la fecha de «Datos al» y Control queda en 🟢. Toda la actualización, con dos años de historia, toma unos 4 minutos. |
| 1 | **Prueba de duplicado** (opcional, porque son otros 4 minutos): copiar y pegar ese mismo archivo en la carpeta (queda «… - copia») y actualizar | Las cifras no cambian. En «Archivos leídos», el repetido dice «No». |
| 5 | Páginas **Sell out**, **Inventario** y **Abasto** | El «Mes actual» se mueve solo. Comparación con los mismos días del año anterior. Cobertura por producto: el **Termómetro Koala** tiene 12 piezas en Walmart para una venta de 127 al mes (riesgo de quiebre), mientras Panda, Familiar y Elefante tienen entre 24 y 45 meses de inventario. Fill rate. |
| 1 | Página **Control** y el maestro | Si algo falta, o llega un producto nuevo, el semáforo lo dice antes de enviar. Un producto nuevo se da de alta en el maestro, en 2 filas. |
| 1 | — | Siguientes pasos (abajo). |

## Errores para mostrar en vivo

Están en [`ERRORES_REPORTE_ACTUAL.md`](ERRORES_REPORTE_ACTUAL.md), sección «Para mostrar en vivo».
- **Reporte actual:** página Sell Out → botón Walmart o Amazon → **Piezas** → pasa el mouse sobre el mes en «Tendencia de Venta por Mes». Para ver 2025, amplía el filtro «Rango de Fechas», por ejemplo a los últimos 13 meses.
- **Reporte nuevo:** página Sell out → Mes = ese mes → Cadena = Walmart o Amazon → tarjeta «Sell out (piezas)».

## Siguientes pasos que presentas

1. **Sell in del ERP:** falta el acceso para bajar la muestra.
2. **Aprobar las definiciones** (`DEFINICIONES_INDICADORES.md`) con el jefe: año anterior, cobertura, umbrales.
3. **Paralelo de 1 a 2 semanas** contra el reporte actual, explicando cada diferencia.
4. **Publicar** y dejar la rutina documentada para los dos analistas (`MANUAL_OPERACION.md`).
