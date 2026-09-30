# Definiciones de los indicadores (propuesta para aprobar)

**Para qué sirve este documento:** que el jefe y el reporte midan lo mismo. Muchos de los "errores" que se corrigen hoy varias veces al día son diferencias de definición. Por ejemplo:
- un cumplimiento que cambia según el día en que se abre el reporte;
- un crecimiento que compara periodos de distinto largo;
- una cobertura que mezcla meses con piezas por tienda.

**Cómo usarlo:**
1. Revisa cada indicador con el jefe.
2. Marca la opción elegida en «Por decidir».
3. Con eso se construye el reporte. Si después se quiere cambiar una definición, se cambia aquí primero.

Cada indicador trae tres cosas: la **definición propuesta**, **cómo lo calcula hoy** el reporte actual y lo que queda **por decidir**.

---

## 0. Reglas generales

| Tema | Propuesta |
|---|---|
| **Fecha de corte** | Cada página muestra «Datos al dd/mm/aaaa» por fuente. El periodo termina en el último día con datos, no en la fecha de hoy. |
| **Periodo** | Se analiza por **meses completos**. El reporte abre en el **«Mes actual»**, que es el último mes con sell out (mes a la fecha). Los meses anteriores se eligen en el filtro Mes. |
| **Comparación con el año anterior** | Siempre los mismos días: si hay datos del 1 al 18 de septiembre de 2026, se compara con el 1 al 18 de septiembre de 2025. |
| **Moneda** | Pesos (MXN) por defecto. Los dólares (USD) se calculan con el tipo de cambio **del mes** de cada venta, de la hoja TipoCambio del maestro. |
| **Montos** | Sin IVA. |
| **Producto** | Todo se agrupa por el código del ERP y el nombre oficial del maestro, sin importar cómo lo llame cada cadena. |

**Por decidir:** ¿qué tipo de cambio se usa? Por ejemplo, el promedio mensual FIX de Banxico, o uno fijo de presupuesto por año.

---

## 1. Sell In (ventas del ERP a clientes)

### Venta real (monto y piezas)
- **Propuesta:** la suma de precio × cantidad, sin IVA, de las facturas del ERP, por fecha de factura. En piezas, la suma de la cantidad facturada.
- **Hoy:** igual, pero el producto se identifica por nombre. Eso causó que el Osito se contara dos veces.
- **Por decidir:** ¿se restan las devoluciones y notas de crédito? Hoy no aparecen en la base.

### Meta
- **Propuesta:** meta mensual por producto y cliente, tomada de la hoja Metas del maestro.
- **Hoy:** está fechada el último día de cada mes. Con el filtro de "últimos 9 meses contados por día", entra la meta completa de un mes con solo unos días de su venta.

### % de cumplimiento
- **Propuesta:**
  - Meses cerrados: venta real ÷ meta de esos meses.
  - Mes en curso: venta a la fecha ÷ meta prorrateada.
- **Hoy:** venta ÷ meta dentro de una ventana móvil. Cambia según el día en que se abre el reporte: 46.4 %, 52.2 % o 45.0 % con los mismos datos.
- **Por decidir:** para prorratear la meta del mes en curso, ¿se usan días calendario o días hábiles?

### Venta del año anterior y crecimiento
- **Propuesta:** la venta de los mismos días del año anterior. Crecimiento = venta real ÷ venta del año anterior − 1.
- **Hoy:** compara el año en curso, que llega hasta el último dato, contra el año anterior completo hasta la fecha de hoy.

### Semáforo de cumplimiento
- **Propuesta:** verde desde 100 %, amarillo de 90 % a 99 %, rojo por debajo de 90 %. Son los umbrales del reporte actual.
- **Por decidir:** confirmar los umbrales.

### Participación
- **Propuesta:** % de la venta por cliente, por categoría de cliente y por familia de producto. Los clientes se agrupan según la hoja Clientes del maestro.
- **Por decidir:** las reglas de agrupación pendientes (ISSSTE, Pharma Plus, Público en general...).

---

## 2. Sell Out (venta de las cadenas al consumidor)

### Sell out Walmart
- **Propuesta:**
  - Piezas: POS Qty de Retail Link.
  - Monto: POS Sales, a precio de venta de Walmart, en MXN.
  - Por día, tienda y artículo.
- **Hoy:** igual, pero desde un Excel consolidado a mano, con días duplicados y días faltantes.
- **Por decidir:** ¿se incluyen todos los tipos de venta (Regular, Clearance, Store Tab) o solo la regular?

### Sell out Amazon
- **Propuesta:**
  - Piezas: *Unidades pedidas*.
  - Monto: *Ganancia por pedidos*, que es el ingreso de lo pedido a precio de Amazon, en MXN.
  - Por mes y ASIN.
- **Hoy:** igual.
- **Por decidir:** ¿se mide lo **pedido** por los clientes o lo **enviado**? Amazon trae las dos cosas; hoy se usa lo pedido.

### Sell out del año anterior
- **Propuesta:** los mismos días del año anterior, igual que en Sell In. El corte es el último día con datos **de cada cadena**: si Walmart llega al 29/09 y Amazon al 28/09, Walmart se compara hasta el 29/09 del año anterior y Amazon hasta el 28/09.
- **Amazon viene por mes.** Si el mes en curso está incompleto (por ejemplo, del 1 al 28 de septiembre), el mismo mes del año anterior se toma **en proporción a los días**: 28 de 30. Así no se compara un mes parcial contra uno completo, que haría ver una caída que no existe.
- **Por decidir:** si se acepta la proporción para Amazon, o si el mes en curso de Amazon no se compara hasta que cierre.

### Tiendas con venta (Walmart)
- **Propuesta:** tiendas que vendieron al menos una pieza en el periodo elegido.

### Tiendas sin inventario que sí venden (Walmart)
- **Propuesta:** tienda y producto con venta en los **últimos 28 días** y **0 piezas** en la última foto de inventario. Es la lista de venta que se está perdiendo.
- **Por decidir:** ¿28 días está bien, o se prefiere otra ventana?

---

## 3. Inventario en las cadenas y cobertura

### Inventario Walmart
- **Propuesta:** las piezas en tienda (*Curr Str On Hand Qty*) en la última foto disponible.
- **Hoy:** igual.
- **Por decidir:** ¿se suma lo que viene en tránsito y lo que está en el centro de distribución (*In Transit*, *In Whse*)?

### Inventario Amazon
- **Propuesta:** *Unidades aptas para la venta disponibles* en la última foto disponible.
- **Hoy:** igual.

**Qué es «la última foto»:** la fecha más reciente de cada cadena, la misma para todos sus productos y tiendas. Si un producto ya no aparece en la foto más reciente, cuenta con 0 piezas, no con lo que tenía en una foto anterior.

### Tiendas con inventario (Walmart)
- **Propuesta:** tiendas con más de 0 piezas **en la última foto**.
- **Hoy:** tiendas que tuvieron inventario en cualquier momento del periodo.

### Venta promedio mensual
- **Propuesta:** el promedio de los **últimos 3 meses cerrados**, en piezas.
- **Hoy:** 4 meses incluyendo el mes en curso, que está incompleto. Eso baja el promedio y exagera la cobertura.
- **Por decidir:** ¿3 o 4 meses?

### Cobertura (meses de inventario)
- **Propuesta:** inventario ÷ venta promedio mensual. Es **la misma fórmula para Walmart y Amazon**.
- **Hoy:** para Walmart, la clasificación usa piezas por tienda en lugar de meses. Por eso nebulizadores con 28 y 50 meses de inventario salen «Saludable».

### Clasificación de cobertura

Propuesta de umbrales, a confirmar:

| Estado | Condición |
|---|---|
| ⚫ Sin inventario | Inventario = 0 |
| 🔴 Riesgo de quiebre | Menos de 1 mes |
| 🟢 Saludable | De 1 a 3 meses |
| 🟡 Sobre stock | Más de 3 meses |
| ⚪ Sin rotación | Hay inventario, pero no hubo venta en los últimos 3 meses |

**Hoy:** Amazon usa 1 mes como riesgo, de 2 a 6 como saludable y más de 6 como sobre stock. Walmart usa otra escala, en piezas por tienda.

**Por decidir:** los umbrales, y si son iguales para las dos cadenas.

**Conteos de la página Inventario** (productos en riesgo, sin inventario y con sobre stock): se cuenta cada producto **en cada cadena**. Un producto en riesgo en Walmart y en Amazon cuenta 2, igual que en la tabla, donde aparece una vez por cadena.

---

## 4. Fill rate (nivel de servicio a las cadenas)

### Fill rate Walmart
- **Propuesta:** piezas recibidas ÷ piezas ordenadas (*Hist Eaches Str Received* ÷ *Hist Eaches Str Ordered*), por mes de la **fecha de la orden**.
- **Hoy:** usa esa fórmula, pero asigna el mes por la **fecha de cancelación** de la orden.
- **Por decidir:**
  - ¿El mes va por fecha de orden, de envío o de cancelación?
  - ¿Se incluyen las órdenes a centro de distribución (*Whse*) o solo las de tienda?

### Fill rate Amazon
- **Propuesta:** cantidad recibida ÷ cantidad solicitada, por mes de la fecha del pedido.
- **Hoy:** igual.
- **Por decidir:** ¿se divide entre lo **solicitado** o entre lo **aceptado**?

---

## 5. Pronóstico de compra (Recship Walmart)

- **Propuesta:**
  - Piezas planeadas por fecha de pedido planeada (*Plan Order Date*).
  - Monto en MXN = piezas × costo por pieza, que es el costo de la caja ÷ las piezas por caja.
- **Hoy:** el monto está en pesos pero se muestra como "us$", junto a cifras que sí están en dólares.

---

## 6. Inventario propio (ERP)

### Existencia
- **Propuesta:** el disponible por producto al cierre, desde el inventario auxiliar o el kardex del ERP.
- **Hoy:** sale de una tabla que se escribe a mano cada mes.
- **Por decidir:** ¿qué almacenes cuentan? Por ejemplo, ¿se excluyen los promocionales?

### Salidas mensuales
- **Propuesta:** las salidas por venta más las salidas de almacén, sin traspasos entre almacenes.
- **Por decidir:** qué tipos de documento del ERP cuentan como salida.

### Promedio mensual de salidas y meses de inventario
- **Propuesta:** el promedio de los últimos 3 meses cerrados. Meses de inventario = existencia ÷ promedio.

### Punto de reorden
- **Propuesta:** demanda mensual promedio × tiempo de entrega (meses) + stock de seguridad. El tiempo de entrega y el stock de seguridad de cada producto salen del maestro.
- **Hoy:** promedio de salidas × 7, fijo para todos los productos.
- **Por decidir:** confirmar la fórmula.

### Monto de inventario
- **Propuesta:** piezas × costo promedio del ERP, en MXN, y en USD con el tipo de cambio del mes.
- **Hoy:** los botones Monto/Piezas de la página no hacen nada, y donde se convierte a dólares se divide entre 20 fijo.
