# Páginas y visuales del reporte actual

Extraído del archivo de diseño del `.pbix`. Se omiten formas, imágenes y cuadros de texto decorativos.

- **Oculta, con botón**: la página no aparece en el menú, pero se llega con un botón.
- **Oculta, sin acceso**: no aparece y ningún botón lleva a ella.

## Página «Sell In» (Visible)

- **Segmentación** «Rango de Fechas» — Values: Calendario.Date — _filtro relativo: últimos 9 meses contados por día (la ventana se mueve cada día)_
- **Navegador de páginas**
- **Segmentación de botones** — Values: Moneda.Tipo
- **Segmentación de botones** — Values: TipoVenta.Tipo
- **Segmentación** — Values: Catalogo_Clientes.Clientes
- **Gráfico circular** «Participación por Categoría de Productos» — Category: Catalogo_Producto_Wellpro.Familias, Ventas_Wellpro.Producto; Y: Medidas Sell In.Real
- **Gráfico combinado (columnas y línea)** «Objetivo por Familia» — Category: Catalogo_Producto_Wellpro.Familias; Y: Medidas Sell_In.Real anterior, Medidas Sell_In.Real, Medidas Sell_In.ObjetivoV2
- **Tarjeta HTML (visual personalizado)** — content: Medidas Sell_In.arjeta Ventas Ejecutiva FINAL v2
- **Gráfico de anillo** «Participación por Cliente» — Category: Catalogo_Clientes.Categoría 2, Catalogo_Clientes.Clientes; Y: Medidas Sell In.Real
- **Gráfico combinado (columnas y línea)** «Tendencia de Venta por Mes» — Y: Medidas Sell_In.Real anterior, Medidas Sell_In.Real, Medidas Sell_In.ObjetivoV2; Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes

## Página «Sell Out» (Visible: vista Walmart)

- **Gráfico de columnas** «Tendencia de Sell Out» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Series: Catalogo_Clientes.Clientes — _sin ningún valor asignado: no muestra datos_
- **Segmentación** «Rango de Fechas» — Values: Calendario.Date — _filtro relativo: últimos 9 meses contados por día (la ventana se mueve cada día)_
- **Navegador de páginas**
- **Botón** «» — _navega a: «Sell Out»_
- **Botón** «» — _navega a: «Sell  Out»_
- **Segmentación de botones** — Values: Catalogo_Clientes.Clientes
- **Segmentación de botones** — Values: TipoSellOut.Tipo
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: Medida 2.Filtro_Sell_Out_WM 2
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: Medida 2.Filtro_Sell_Out_WM
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: MedidasInventarioWM.Cant.TiendasWM
- **Gráfico combinado (columnas y línea)** «Inventario por mes vs Promedio de Inventario por Piezas» — Y: Clasificacion_Cobertura.Filtro Inventario Unidades, MedidasInventarioWM.Cant.TiendasWM; Y2: MedidasInventarioWM.Inventario_Prom_Tienda; Tooltips: Min(Catalogo_Producto_Wellpro.Nombre de Producto); Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes — _**filtro fijo: excluye octubre, noviembre y diciembre**_
- **Gráfico combinado (columnas y línea)** «Tendencia de Venta por Mes» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Y: Clasificacion_Cobertura.Filtro_Sell_Out_Consolidado_Año_Anterior, Clasificacion_Cobertura.Filtro_Sell_Out_Consolidado
- **Gráfico de columnas** — Series: Catalogo_Clientes.Clientes; Y: MedidasFillRate.% Fill Rate Consolidado; Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes — _filtro con los 12 meses (sin efecto)_
- **Gráfico de área** «Pronostico de Compra» — Category: Recship WM.Plan Order Date.Variación.Jerarquía de fechas.Año, Recship WM.Plan Order Date.Variación.Jerarquía de fechas.Mes, Recship WM.Plan Order Date.Variación.Jerarquía de fechas.Día; Y: MedidasConsolidado.Filtro_RS_WM
- **Gráfico circular** — Category: Catalogo_Producto_Wellpro.Familias, Catalogo_Producto_Wellpro.Nombre de Producto; Y: MedidasConsolidado.Filtro_Sell_Out_Consolidado

## Página «Sell  Out» (Oculta, con botón: vista Amazon)

- **Gráfico de columnas** «Tendencia de Sell Out» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Y: MedidasConsolidado.Filtro_Sell_Out_Consolidado; Series: Catalogo_Clientes.Clientes
- **Segmentación** «Rando de Fechas» — Values: Calendario.Date — _filtro relativo: últimos 9 meses contados por día (la ventana se mueve cada día)_
- **Navegador de páginas**
- **Botón** «» — _navega a: «Sell Out»_
- **Botón** «» — _navega a: «(sin destino)»_
- **Segmentación de botones** — Values: Catalogo_Clientes.Clientes
- **Segmentación de botones** — Values: TipoSellOut.Tipo
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: MedidasAmazon.Filtro Sell Out_Amazon 2
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: MedidasAmazon.Filtro Sell Out_Amazon
- **Matriz** — Rows: Catalogo_Producto_Wellpro.Nombre de Producto; Values: MedidasConsolidado.Filtro Inventario Unidades, MedidasConsolidado.FiltroVentasPromedio, MedidasConsolidado.Meses de Inventario, Clasificacion_Cobertura.Clasificación Cobertura
- **Gráfico combinado (columnas y línea)** «Tendencia de Venta por Mes» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Y: Clasificacion_Cobertura.Filtro_Sell_Out_Consolidado_Año_Anterior, Clasificacion_Cobertura.Filtro_Sell_Out_Consolidado
- **Gráfico de columnas** — Series: Catalogo_Clientes.Clientes; Y: MedidasFillRate.% Fill Rate Consolidado; Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes — _**filtro fijo: solo enero a septiembre**_
- **Gráfico circular** — Category: Catalogo_Producto_Wellpro.Familias, Ventas Amazon.Nombre del Producto; Y: MedidasConsolidado.Filtro_Sell_Out_Consolidado

## Página «Inventario.» (Oculta, sin acceso)

- **Segmentación** «Rando de Fechas» — Values: Calendario.Date — _filtro relativo: últimos 7 meses calendario completos_
- **Navegador de páginas**
- **Segmentación de botones** — Values: TipoSalida.Tipo
- **Segmentación** «Filtro por Artículo» — Values: Inventario Auxiliar.Producto — _excluye 4 valores fijos (BOLSA NO TEJIDA (SAINT CIEL), BOLSO BANDOLERO PARA HOMBRO (SAINT CIEL), COSMETIQUERA DE MANO (SAINT CIEL)...)_
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: InventarioKardex.Salidas Switch
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: InventarioKardex.Punto de Reorden
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: InventarioKardex.Promedio Salidas 2
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: InventarioKardex.MesesInventario
- **Gráfico combinado (columnas y línea)** «Tendencia de Inventario por Mes» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Y2: InventarioKardex.Debug Exist, InventarioKardex.Punto de Reorden; Series: InventarioKardex.Descripcion
- **Matriz** «Top 10 Articulos» — Rows: InventarioKardex.Descripcion; Values: InventarioKardex.Total Salidas
- **Gráfico de columnas agrupadas** «Salidas por Mes» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Y: InventarioKardex.EntradasConsolidada, InventarioKardex.SalidasConsolidada

## Página «Inventario» (Visible)

- **Segmentación** «Rando de Fechas» — Values: Calendario.Date — _filtro relativo: últimos 8 meses calendario completos_
- **Navegador de páginas**
- **Segmentación de botones** — Values: TipoSalida.Tipo
- **Segmentación** «Filtro por Artículo» — Values: Tbl.Descripcion — _excluye 4 valores fijos (BOLSA NO TEJIDA (SAINT CIEL), BOLSO BANDOLERO PARA HOMBRO (SAINT CIEL), COSMETIQUERA DE MANO (SAINT CIEL)...)_
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: Tbl.Inventario Último
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: Tbl.Promedio Mensual Salidas
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: Tbl.MesesInventario_V2
- **Tarjeta avanzada (visual personalizado)** — mainMeasure: Tbl.Punto de Reorden v2
- **Gráfico combinado (columnas y línea)** «Tendencia de Inventario por Mes» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Series: InventarioKardex.Descripcion; Y2: Sum(Tbl.Inventario Final), Tbl.Punto de Reorden v2
- **Matriz** «Top 10 Articulos» — Rows: InventarioKardex.Descripcion; Values: InventarioKardex.Total Salidas
- **Gráfico de columnas agrupadas** «Salidas por Mes» — Category: Calendario.Date.Variación.Jerarquía de fechas.Año, Calendario.Date.Variación.Jerarquía de fechas.Mes; Y: Sum(Tbl.Entrada dev), Sum(Tbl.Salida), Sum(Tbl.Salida Almacen)
