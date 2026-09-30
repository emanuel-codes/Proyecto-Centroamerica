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

| Fase | Qué se hace | Quién | Resultado |
|---|---|---|---|
| **1. Acuerdos** | Reunir los errores que el jefe suele marcar y definir cada indicador: fórmula, fechas, moneda y umbrales. Decidir la frecuencia de actualización y dónde se publica. | Manuel con el cliente. Claude prepara la propuesta de definiciones. | [`DEFINICIONES_INDICADORES.md`](DEFINICIONES_INDICADORES.md) aprobado |
| **2. Descargas** | Fijar la "receta" de cada descarga (sección 6) y hacer una descarga de prueba de cada fuente con tus usuarios. | Manuel descarga; Claude revisa las columnas. | `docs/guia_descargas.md` y un ejemplo de cada fuente |
| **3. Maestros** | Armar el archivo maestro con los códigos del ERP, EAN válidos, ASIN reales y artículos de Walmart. Sacar la lista de lo que falta validar. | Claude arma el borrador; el cliente valida. | [`maestros/Maestro_Wellpro_borrador.xlsx`](maestros/) validado |
| **4. Modelo** | Construir las consultas de Power Query, las tablas y las medidas en el proyecto `.pbip`. | Claude construye; Manuel abre y actualiza en Power BI Desktop. | Modelo que se actualiza sin pasos manuales |
| **5. Páginas** | Rehacer Sell In, Sell Out e Inventario con la lógica corregida, y agregar la página de control. | Claude y Manuel | Reporte completo |
| **6. Paralelo** | Correr el reporte viejo y el nuevo con los mismos datos durante 1 o 2 semanas. Explicar cada diferencia. | Manuel, con apoyo de Claude | Diferencias explicadas y aceptadas por el jefe |
| **7. Entrega** | Publicar, programar la actualización y escribir la guía paso a paso (meta: menos de 30 minutos). | Manuel | Reporte en producción |

---

## 3. Controles automáticos (página de control)

Cada control se muestra con semáforo verde, amarillo o rojo. **Si hay algo en rojo, no se envía.**

| Control | Qué revisa |
|---|---|
| Datos al día | La última fecha cargada de cada fuente frente a la esperada: ayer o la última semana. |
| Días faltantes | Días sin datos en el sell out y el inventario de Walmart y en las ventas y el inventario de Amazon. |
| Duplicados | Filas repetidas: misma fecha, tienda y artículo; o misma fecha y ASIN. |
| Códigos sin homologar | Artículos de Walmart, ASIN o códigos del ERP que no están en el maestro. También clientes del ERP sin clasificar. |
| Metas | Productos con venta y sin meta, y metas de productos que no existen. |
| Cuadre de totales | El sell in del mes contra el total del ERP, y el detalle de cada archivo contra su total. |
| Tipo de cambio | Que exista el tipo de cambio del mes. |
| Valores raros | Días con venta cero, o con más del triple del promedio. |

---

## 4. Carpetas de datos

Van en el OneDrive o SharePoint de la empresa, no en una computadora personal:

```
Wellpro Reporte/
├── 01 Descargas/              ← archivos tal como salen; nunca se editan
│   ├── Amazon Ventas/
│   ├── Amazon Inventario/
│   ├── Amazon Ordenes/
│   ├── Walmart Sell Out/
│   ├── Walmart Inventario Tiendas/
│   ├── Walmart Fill Rate/
│   ├── Walmart Recship/
│   ├── ERP Sell In/
│   └── ERP Inventario/
└── 02 Maestros/
    └── Maestro_Wellpro.xlsx   ← hojas: Productos, Equivalencias, Clientes, Metas, TipoCambio
```

**Nombres de archivo:** `Fuente_AAAA-MM-DD`, con la fecha de los datos. Por ejemplo, `WalmartSellOut_2026-09-29.csv` o `AmazonVentas_2026-09.csv`.

Así los archivos se ordenan solos y la fecha no depende de la configuración de la computadora. Si el archivo ya trae la fecha por dentro, el nombre solo sirve para ordenar.

---

## 5. Estructura del repositorio (propuesta)

```
Proyecto-Centroamerica/
├── README.md
├── docs/          diagnóstico, plan, definiciones, guía de descargas, guía de actualización
├── powerbi/       el proyecto nuevo (.pbip)
├── maestros/      plantilla del archivo maestro
├── muestras/      uno o dos archivos de ejemplo por fuente, para probar las consultas
├── referencia/    reporte actual (.pbix) y Excel que entregó el cliente
└── analisis/      código extraído del reporte actual
```

---

## 6. Recetas de descarga (primera versión)

Hay que confirmarlas con las descargas de prueba. La idea es que cada descarga tenga siempre las mismas columnas y la menor cantidad de archivos posible.

### Amazon Vendor Central

Los archivos actuales muestran los ajustes que se usan: Programa *Retail*, Vista del distribuidor *Fabricación*, Visto por *ASIN*, Moneda *MXN* y rango *Personalizado*.

| Descarga | Rango | Para qué |
|---|---|---|
| Ventas | Mes anterior completo, y mes en curso hasta ayer, **en un archivo cada uno** | Sell out Amazon |
| Inventario | Último día disponible | Inventario y cobertura en Amazon |
| Órdenes de compra, líneas de artículos (`POItemExport`) | Últimos 3 meses | Fill rate Amazon |

Hasta octubre de 2025 las ventas se bajaban así, por mes, en un solo archivo. Por eso no hacen falta 30 descargas diarias.

### Retail Link (Walmart México)

Pídele al analista actual los parámetros de sus consultas guardadas: las columnas, los filtros y el nivel de detalle. Con eso armas las tuyas iguales.

| Descarga | Detalle | Columnas mínimas |
|---|---|---|
| Sell out | Diario, por tienda y artículo. Idealmente **una semana en un solo archivo**. | Fecha (Daily), Store Nbr, Item Nbr, UPC, Vendor Stk Nbr, Signing Desc, POS Qty, POS Sales, POS Cost, Sales Type |
| Inventario en tiendas | Foto del día, por tienda y artículo | Store Nbr, Item Nbr, UPC, Vendor Stk Nbr, Curr Str On Hand Qty, Curr Str In Transit Qty, Curr Str In Whse Qty, Curr Str On Order Qty, Max Shelf Qty |
| Fill rate | Órdenes de compra | PO Number, PO Type, PO Order Date, PO Ship Date, PO Cancel Date, Item Nbr, UPC, VNPK Qty, VNPK Cost, Hist Eaches Str Ordered, Hist Eaches Str Received |
| Recship | Pedidos planeados | Item Nbr, UPC, Store Nbr, Plan Order Date, Units, VNPK Qty, VNPK Cost |

`Vendor Stk Nbr` es importante: en Retail Link trae el **código de producto del ERP** (14660, 13471, 13595...). Con esa columna la homologación con Walmart es directa.

### ERP One Goal

| Descarga | Pedido |
|---|---|
| Sell in | Que la exportación incluya el **código de producto** (por ejemplo 13595 o JH0002), el cliente, la fecha, la cantidad, el precio y, si se puede, el número de factura. Hoy solo trae nombres. |
| Inventario | El kardex o el inventario auxiliar, que ya traen el código. Reemplazan la tabla de inventario que hoy se escribe a mano. |

---

## 7. Decisiones pendientes

1. **Dónde viven los datos y dónde se publica el reporte:** en la cuenta de Microsoft de la empresa del cliente o en la tuya, mientras tanto.
2. **Frecuencia de actualización** que esperan los jefes: diaria o semanal.
3. **Diseño visual:** si se mantiene el actual, con los colores Wellpro, o se renueva.
4. **Exportación del ERP con código de producto:** si sistemas la puede hacer, o si hay acceso de solo lectura a la base de datos.
