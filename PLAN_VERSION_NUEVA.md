# Plan de la versión nueva

**Objetivo:** que el reporte salga bien a la primera.

Hoy el reporte se reenvía unas tres veces al día porque el jefe encuentra errores. La versión nueva debe cumplir tres cosas:
- **Actualización corta, sin tocar los datos a mano.** Sin copiar, pegar ni renombrar.
- **Controles automáticos** que detecten los errores antes de enviar el reporte, no después.
- **Indicadores con definiciones acordadas por escrito**, para que el jefe y el reporte midan lo mismo.

El reporte actual no es complejo por lo que muestra. Los errores vienen del proceso: cada paso manual es una oportunidad de equivocarse, y no hay nada que avise cuando algo salió mal. El detalle está en [`DIAGNOSTICO_REPORTE_ACTUAL.md`](DIAGNOSTICO_REPORTE_ACTUAL.md).

---

## 1. Reglas del proyecto

1. **Las descargas no se editan.** Cada archivo se guarda tal como sale de Amazon, Retail Link o el ERP, en su carpeta. No se pega en otro Excel, no se convierte en tabla y no se renombra por dentro.
2. **Cada dato se mantiene en un solo lugar.** Productos y equivalencias, clientes, metas y tipo de cambio viven en un solo archivo maestro.
3. **La homologación se hace por código, nunca por nombre.**
4. **Nada que editar en Power Query al actualizar.**
   - La ruta de los datos está en un solo parámetro.
   - Las fechas se toman del contenido del archivo, o de un nombre con formato `AAAA-MM-DD`.
5. **El reporte se revisa solo.** Tiene una página de control con semáforo. Si hay algo en rojo, no se envía: se corrige la fuente.
6. **Cada indicador tiene una definición escrita** y aprobada por el jefe antes de construirlo.
7. **Todo cambio queda registrado en GitHub.** El reporte se guarda como proyecto de Power BI (`.pbip`).

---

## 2. Fases

| Fase | Qué se hace | Estado (01/10/2026) |
|---|---|---|
| **1. Acuerdos** | Definir cada indicador: fórmula, fechas, moneda y umbrales. | Propuesta lista en [`DEFINICIONES_INDICADORES.md`](DEFINICIONES_INDICADORES.md); **falta que el jefe la apruebe**. |
| **2. Descargas** | Fijar la receta de cada descarga y probarla. | **Listo** para Amazon y Walmart ([`GUIA_DESCARGAS.md`](GUIA_DESCARGAS.md)). **Falta el ERP** (sin acceso todavía). |
| **3. Maestros** | Archivo maestro con productos, códigos, clientes, metas y tipo de cambio. | Borrador listo; **falta validar** la hoja Pendientes con el cliente. |
| **4. Modelo** | Consultas, tablas y medidas en el proyecto `.pbip`. | **Listo** para Amazon y Walmart, a prueba de duplicados. **Falta el ERP.** |
| **5. Páginas** | Páginas del reporte y página de control. | **Sell out, Inventario, Abasto y Control listas.** Falta **Sell in** (depende del ERP). |
| **6. Paralelo** | Correr el reporte viejo y el nuevo con los mismos datos 1 o 2 semanas y explicar cada diferencia. | Pendiente; necesita el historial de Walmart. Resumen de errores ya encontrados: [`ERRORES_REPORTE_ACTUAL.md`](ERRORES_REPORTE_ACTUAL.md). |
| **7. Entrega** | Publicar, programar la actualización y documentar la rutina. | Manual listo ([`MANUAL_OPERACION.md`](MANUAL_OPERACION.md)); plan en [`PLAN_ENTREGA.md`](PLAN_ENTREGA.md). |

---

## 3. Controles automáticos (página de control)

Cada control se muestra con semáforo verde, amarillo o rojo. **Si hay algo en rojo, no se envía.**

| Control | Qué revisa | Estado |
|---|---|---|
| Datos al día | La última fecha de cada fuente: amarillo si tiene más de 3 días | Listo |
| Días faltantes | Días sin sell out de Walmart; meses de Amazon que faltan o quedaron incompletos | Listo |
| Duplicados | Cada día se toma de un solo archivo, así que no puede haber duplicados | Listo, por diseño |
| Códigos sin homologar | Artículos de Walmart o ASIN que no están en el maestro | Listo |
| Metas | Productos con venta y sin meta, y metas de productos que no existen | Pendiente (página Sell in) |
| Cuadre de totales | El sell in del mes contra el total del ERP | Pendiente (ERP) |
| Tipo de cambio | Que exista el tipo de cambio del mes | Pendiente (falta definirlo) |
| Valores raros | Días con venta cero, o con más del triple del promedio | Pendiente |

---

## 4. Carpetas de datos

```
Nueva versión/
├── Amazon/      Sell out, Inventarios
├── Walmart/     Sell out, Inventario, Fill rate, Forecast
├── ERP/         Sell in, Inventario   (faltan las muestras)
└── Maestros/    Maestro_Wellpro.xlsx
```

- Los archivos se guardan **con el nombre con que se descargan**. El reporte saca las fechas del contenido.
- Cada carpeta tiene una subcarpeta `Respaldo` para los archivos que la página Control marca con «Usado = No». El reporte no la lee.
- En la entrega, esta carpeta pasa al OneDrive o SharePoint de la empresa ([`PLAN_ENTREGA.md`](PLAN_ENTREGA.md)).

---

## 5. Estructura del repositorio

```
Proyecto-Centroamerica/
├── README.md                       índice
├── MANUAL_OPERACION.md             rutina y mantenimiento (para los dos analistas)
├── GUIA_DESCARGAS.md, GUIA_VALIDACION.md
├── DEFINICIONES_INDICADORES.md, PLAN_VERSION_NUEVA.md, PLAN_ENTREGA.md
├── DIAGNOSTICO_REPORTE_ACTUAL.md, ERRORES_REPORTE_ACTUAL.md, DEMO_VIERNES.md
├── powerbi/          el proyecto nuevo (.pbip)
├── Nueva versión/    datos de la versión nueva
├── analisis/         código extraído del reporte actual y herramientas internas
└── (raíz)            reporte actual (.pbix) y Excel que entregó el cliente, como referencia
```

---

## 6. Recetas de descarga

Confirmadas con las descargas de prueba. Están en [`GUIA_DESCARGAS.md`](GUIA_DESCARGAS.md), y la rutina diaria en [`MANUAL_OPERACION.md`](MANUAL_OPERACION.md).

---

## 7. Decisiones pendientes

1. **Dónde viven los datos y dónde se publica el reporte:** propuesta en [`PLAN_ENTREGA.md`](PLAN_ENTREGA.md). Falta confirmar las licencias de Power BI y la carpeta de la empresa.
2. **Definiciones de los indicadores:** las marcadas «Por decidir» en [`DEFINICIONES_INDICADORES.md`](DEFINICIONES_INDICADORES.md).
3. **Exportación del ERP con código de producto:** si sistemas la puede hacer.
4. **Resueltas:**
   - la frecuencia es diaria;
   - el diseño usa los colores y el logo de Wellpro.
