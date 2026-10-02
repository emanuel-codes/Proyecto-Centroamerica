# Proyecto-Centroamerica

Rediseño del reporte de Power BI «Análisis de Ventas Wellpro»: sell in del ERP One Goal, sell out e inventario de Amazon México y Walmart México (Retail Link), metas, fill rate e inventario propio.

Objetivo: una versión nueva que se actualice con menos pasos manuales y sin los errores del reporte actual.

## Contenido

**Para operar el reporte, empieza por [`MANUAL_OPERACION.md`](MANUAL_OPERACION.md).**

| Archivo o carpeta | Qué es |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Contexto y reglas para trabajar el proyecto con Claude Code en la computadora local (MCP de Power BI). |
| [`MANUAL_OPERACION.md`](MANUAL_OPERACION.md) | Rutina diaria, semanal y mensual; qué hacer según la página Control; cómo dar de alta un producto nuevo. Para Manuel y el analista que lo reemplaza. |
| [`DEMO_VIERNES.md`](DEMO_VIERNES.md) | Qué preparar y guion de la presentación del primer vistazo. |
| [`ERRORES_REPORTE_ACTUAL.md`](ERRORES_REPORTE_ACTUAL.md) | Resumen para presentar: errores del reporte actual, su impacto, su causa y cómo los evita la versión nueva. |
| [`PLAN_ENTREGA.md`](PLAN_ENTREGA.md) | Cómo se entrega: carpeta compartida en OneDrive o SharePoint, actualización programada, alertas y cómo reparar si algo se daña. |
| [`powerbi/`](powerbi/) | **Proyecto nuevo de Power BI** (v0.4): páginas Sell out, Inventario, Abasto y Control con el diseño Wellpro. Lee Walmart, Amazon (con historial desde febrero de 2024) y el maestro. La v0.3 ya se probó en Power BI Desktop. Cómo abrirlo: [`powerbi/LEEME.md`](powerbi/LEEME.md). |
| [`PLAN_VERSION_NUEVA.md`](PLAN_VERSION_NUEVA.md) | Plan de trabajo: reglas, fases con su estado, controles y decisiones pendientes. |
| [`GUIA_DESCARGAS.md`](GUIA_DESCARGAS.md) | Qué se descarga de Amazon, Retail Link y el ERP, cada cuánto y en qué carpeta. |
| [`GUIA_VALIDACION.md`](GUIA_VALIDACION.md) | Cómo comprobar por tu cuenta cada cifra del reporte contra los archivos descargados, y la rutina diaria antes de enviar. |
| `Nueva versión/` | Carpeta de datos de la versión nueva: descargas por fuente (con su subcarpeta `Respaldo`) y `Maestros/Maestro_Wellpro.xlsx` (borrador del maestro). |
| [`DEFINICIONES_INDICADORES.md`](DEFINICIONES_INDICADORES.md) | Propuesta de definición de cada indicador, para aprobar con el jefe. |
| [`DIAGNOSTICO_REPORTE_ACTUAL.md`](DIAGNOSTICO_REPORTE_ACTUAL.md) | Cómo funciona el reporte actual, qué pasos manuales exige y qué errores tiene, con cifras. |
| [`analisis/reporte_actual/`](analisis/reporte_actual/) | Código extraído del `.pbix` actual: consultas de Power Query, medidas DAX, relaciones y páginas. |
| `analisis/herramientas/` | Herramientas internas de Claude que generan el proyecto y el maestro. **No se ejecutan:** reescriben el proyecto completo y borrarían los cambios hechos en Power BI Desktop. |
| `Analisis de Ventas Wellpro -V5.pbix respaldo.pbix` | Reporte actual, tal como lo entregó el cliente. |
| `Sell in/BD Sell In.xlsx` | Base de sell in y catálogos: productos, clientes y metas. |
| `Inventario/Inventarios.xlsx` | Tabla de inventario que se llena a mano cada mes. |
| `Ventas Amazon/` | Archivos mensuales de ventas de Amazon Vendor Central que lee el reporte actual (feb-2024 a sep-2026). Los 20 que son descargas completas del mes ya se copiaron a `Nueva versión/Amazon/Sell out`. |
