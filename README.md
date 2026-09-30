# Proyecto-Centroamerica

Rediseño del reporte de Power BI «Análisis de Ventas Wellpro»: sell in del ERP One Goal, sell out e inventario de Amazon México y Walmart México (Retail Link), metas, fill rate e inventario propio.

Objetivo: una versión nueva que se actualice con menos pasos manuales y sin los errores del reporte actual.

## Contenido

| Archivo o carpeta | Qué es |
|---|---|
| [`PLAN_VERSION_NUEVA.md`](PLAN_VERSION_NUEVA.md) | Plan de trabajo de la versión nueva: reglas, fases, controles, carpetas y recetas de descarga. |
| [`DIAGNOSTICO_REPORTE_ACTUAL.md`](DIAGNOSTICO_REPORTE_ACTUAL.md) | Cómo funciona el reporte actual, qué pasos manuales exige y qué errores tiene, con cifras. |
| [`analisis/reporte_actual/`](analisis/reporte_actual/) | Código extraído del `.pbix` actual: consultas de Power Query, medidas DAX, relaciones y páginas. |
| `Analisis de Ventas Wellpro -V5.pbix respaldo.pbix` | Reporte actual, tal como lo entregó el cliente. |
| `Sell in/BD Sell In.xlsx` | Base de sell in y catálogos: productos, clientes y metas. |
| `Inventario/Inventarios.xlsx` | Tabla de inventario que se llena a mano cada mes. |
| `Ventas Amazon/` | Archivos mensuales de ventas de Amazon Vendor Central que lee el reporte actual (feb-2024 a sep-2026). |
