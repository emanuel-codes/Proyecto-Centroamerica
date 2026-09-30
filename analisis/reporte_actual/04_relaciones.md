# Relaciones del modelo actual

Se omiten las relaciones con las tablas de fecha automáticas (`LocalDateTable_*`). "Ambas" = filtro en las dos direcciones.

| Desde (tabla[columna]) | Hacia (tabla[columna]) | Cardinalidad | Dirección del filtro | Activa |
|---|---|---|---|---|
| Sell_Out_WM[Store Nbr] | Catalogo de Tiendas[Store Nbr] | *:1 | Ambas | Sí |
| Sell_Out_WM[UPC] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Ventas_Wellpro[Cliente] | Catalogo_Clientes[Clientes] | *:1 | Una | Sí |
| Metas[Cliente] | Catalogo_Clientes[Clientes] | *:1 | Una | Sí |
| Catalogo de Tiendas[Codigo Estados] | Catalogo_Estado[Codigo Estados] | *:1 | Una | Sí |
| Inventario en Tienda WM[Store Nbr] | Catalogo de Tiendas[Store Nbr] | *:1 | Una | Sí |
| Inventario en Tienda WM[UPC.] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Recship WM[UPC.] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Ventas_Wellpro[UPC] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Metas[UPC] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Inventario Amazon[ASIN] | Catalogo_Producto_Wellpro[ASIN] | *:1 | Una | Sí |
| Fill_rate[UPC] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Metas[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| Ventas_Wellpro[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| Ventas Amazon[UPC] | Catalogo_Producto_Wellpro[UPC] | *:1 | Una | Sí |
| Ventas Amazon[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| Sell_Out_WM[Daily] | Calendario[Date] | *:1 | Una | Sí |
| Fillrate Amazon New[ASIN] | Catalogo_Producto_Wellpro[ASIN] | *:1 | Una | Sí |
| Fillrate Amazon New[Fecha del pedido] | Calendario[Date] | *:1 | Una | Sí |
| Fill_rate[PO Cancel Date] | Calendario[Date] | *:1 | Una | Sí |
| Inventario en Tienda WM[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| InventarioKardex[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| Inventario Amazon[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| InventarioKardex[CodArticulo] | Inventario Auxiliar[Código Pro.] | *:* | Una | Sí |
| Tbl[Fecha] | Calendario[Date] | *:1 | Una | Sí |
| InventarioKardex (2)[Descripcion] | Costos[PRODUCTO] | *:* | Ambas | Sí |
