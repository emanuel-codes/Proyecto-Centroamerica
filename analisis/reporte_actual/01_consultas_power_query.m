// Consultas de Power Query extraídas de "Analisis de Ventas Wellpro -V5.pbix respaldo.pbix" (30/09/2026).
// Código tal como está en el reporte actual; no se ha modificado.
// Parte 1: consultas que cargan una tabla al modelo. Parte 2: consultas auxiliares (funciones, archivos de ejemplo, parámetros, consultas sin cargar).

// ################################################################################################
// PARTE 1. CONSULTAS QUE CARGAN TABLAS AL MODELO (25)
// ################################################################################################

// ===== Consulta: Sell_Out_WM =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Walmart\Ventas Sell Out WM\Ventas Consolidadas WM.xlsx"), null, true),
    Sell_Out_WM_Table = Origen{[Item="Sell_Out_WM",Kind="Table"]}[Data],
    #"Tipo cambiado" = Table.TransformColumnTypes(Sell_Out_WM_Table,{{"UPC", Int64.Type}, {"Item Nbr", type text}, {"Signing Desc", type text}, {"Vendor Stk Nbr", Int64.Type}, {"Item Status", type text}, {"Item Type", Int64.Type}, {"Brand Desc", type text}, {"Dept Desc", type text}, {"Fineline", Int64.Type}, {"Fineline Desc", type text}, {"Financial Rpt Code", type text}, {"City", type text}, {"Street Address", type text}, {"Store Nbr", Int64.Type}, {"Store Name", type text}, {"Store Specific Retail", type number}, {"Store Specific Cost", type number}, {"POS Qty", Int64.Type}, {"POS Sales", type number}, {"POS Cost", type number}, {"VNPK Qty", Int64.Type}, {"WHPK Qty", Int64.Type}, {"VNPK Cost", type number}, {"WHPK Cost", type number}, {"Corp Cancel When Out Flag", type text}, {"Accounting Comp Flag", type text}, {"Order book Flag", type text}, {"Item Sub Type", Int64.Type}, {"Pallet Ti Qty", Int64.Type}, {"Pallet Hi Qty", Int64.Type}, {"Vndr Min Ord Qty", Int64.Type}, {"Max Str Order Qty", Int64.Type}, {"Acct Dept Nbr", Int64.Type}, {"Vendor Nbr", Int64.Type}, {"Vendor Name", type text}, {"Vendor Nbr Dept", Int64.Type}, {"Vendor Sequence Nbr", Int64.Type}, {"Sales Type", Int64.Type}, {"Sales Description", type text}, {"Daily", type date}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Tipo cambiado",743400255002,7434002550028,Replacer.ReplaceValue,{"UPC"}),
    #"Valor reemplazado1" = Table.ReplaceValue(#"Valor reemplazado",743400255149,7434002551490,Replacer.ReplaceValue,{"UPC"}),
    #"Valor reemplazado2" = Table.ReplaceValue(#"Valor reemplazado1",743100920749,7431009207498,Replacer.ReplaceValue,{"UPC"}),
    #"Valor reemplazado3" = Table.ReplaceValue(#"Valor reemplazado2",743100920750,7431009207504,Replacer.ReplaceValue,{"UPC"}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Valor reemplazado3",{"Brand Desc", "VNPK Qty", "WHPK Qty", "VNPK Cost", "WHPK Cost", "Pallet Ti Qty", "Pallet Hi Qty", "Vendor Nbr", "Vendor Name", "Identificador ", "Item Flags"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas quitadas",{{"UPC", type text}}),
    #"Filas filtradas" = Table.SelectRows(#"Tipo cambiado1", each ([Signing Desc] <> null)),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Filas filtradas",{{"Daily", type date}, {"mes", Int64.Type}})
in
    #"Tipo cambiado2"

// ===== Consulta: Catalogo de Tiendas =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\Reporterias WM\Wellpro Mexico\Bases PBI\SellOut Walmart.xlsx"), null, true),
    #"Catalogo de Tiendas_Sheet" = Origen{[Item="Catalogo de Tiendas",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Catalogo de Tiendas_Sheet", [PromoteAllScalars=true]),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos",{{"Store Nbr", Int64.Type}, {"Store Name", type text}, {"City", type text}, {"Estado", type text}, {"Formato Tienda", type text}, {"Codigo Estados", type text}}),
    #"Dividir columna por delimitador" = Table.SplitColumn(#"Tipo cambiado", "Formato Tienda", Splitter.SplitTextByEachDelimiter({" "}, QuoteStyle.Csv, true), {"Formato Tienda.1", "Formato Tienda.2"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Dividir columna por delimitador",{{"Formato Tienda.1", type text}, {"Formato Tienda.2", type text}}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Tipo cambiado1",{"Formato Tienda.1"}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columnas quitadas",{{"Formato Tienda.2", "Formato Tienda"}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Columnas con nombre cambiado","Superama","Walmart Expres",Replacer.ReplaceText,{"Formato Tienda"})
in
    #"Valor reemplazado"

// ===== Consulta: Catalogo_Clientes =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\BD Sell In.xlsx"), null, true),
    Catalogo_Clientes_Table = Origen{[Item="Catalogo_Clientes",Kind="Table"]}[Data],
    #"Tipo cambiado" = Table.TransformColumnTypes(Catalogo_Clientes_Table,{{"Clientes", type text}, {"Categoría 2", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: Catalogo_Estado =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\BD Sell In.xlsx"), null, true),
    #"Filas filtradas" = Table.SelectRows(Origen, each ([Name] = "Catalogo de Estados")),
    #"Se expandió Data" = Table.ExpandTableColumn(#"Filas filtradas", "Data", {"Column1"}, {"Data.Column1"}),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Se expandió Data",{"Data.Column1", "Name", "Item", "Kind", "Hidden"}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Columnas reordenadas",{"Data.Column1"}),
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Otras columnas quitadas", [PromoteAllScalars=true]),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos",{{"Codigo Estados", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: Catalogo_Producto_Wellpro =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\BD Sell In.xlsx"), null, true),
    Catalogo_Producto_Wellpro_Table = Origen{[Item="Catalogo_Producto_Wellpro",Kind="Table"]}[Data],
    #"Tipo cambiado" = Table.TransformColumnTypes(Catalogo_Producto_Wellpro_Table,{{"Nombre de Producto", type text}, {"Modelo", type text}, {"Costo CIF", type number}, {"Lead Time (meses)", Int64.Type}, {"Demanda Prom (mensual)", Int64.Type}, {"Familias", type text}, {"Stock Seguridad", Int64.Type}, {"UPC", type text}, {"ASIN", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: Metas =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\BD Sell In.xlsx"), null, true),
    Metas_Table = Origen{[Item="Metas",Kind="Table"]}[Data],
    #"Tipo cambiado" = Table.TransformColumnTypes(Metas_Table,{{"Fecha", type date}, {"Nombre Producto", type text}, {"Cliente", type text}, {"Cantidad Vendida", Int64.Type}, {"Precio de Venta", type number}, {"Total de Venta", type number}, {"categoria", type text}}),
    #"Consultas combinadas" = Table.NestedJoin(#"Tipo cambiado", {"Nombre Producto"}, Catalogo_Producto_Wellpro, {"Nombre de Producto"}, "Catalogo_Producto_Wellpro", JoinKind.LeftOuter),
    #"Se expandió Catalogo_Producto_Wellpro" = Table.ExpandTableColumn(#"Consultas combinadas", "Catalogo_Producto_Wellpro", {"UPC", "ASIN"}, {"UPC", "ASIN"}),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Se expandió Catalogo_Producto_Wellpro",{"UPC", "ASIN", "Fecha", "Nombre Producto", "categoria", "Cliente", "Cantidad Vendida", "Precio de Venta", "Total de Venta"}),
    #"Filas filtradas" = Table.SelectRows(#"Columnas reordenadas", each true)
in
    #"Filas filtradas"

// ===== Consulta: Ventas_Wellpro =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\BD Sell In.xlsx"), null, true),
    #"Filas filtradas" = Table.SelectRows(Origen, each ([Kind] = "Table")),
    Ventas_Wellpro_Table = #"Filas filtradas"{[Item="Ventas_Wellpro",Kind="Table"]}[Data],
    #"Tipo cambiado" = Table.TransformColumnTypes(Ventas_Wellpro_Table,{{"Mes", type text}, {"Año", type text}, {"Fecha", type date}, {"Producto", type text}, {"Cliente", type text}, {"Precio de Venta", type number}, {"Cantidad Vendida", Int64.Type}, {"IVA", type number}, {"Total de Venta sin IVA", type number}, {"Total de Venta con IVA", type number}, {"Día", Int64.Type}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Tipo cambiado",{"Fecha", "Producto", "Cliente", "Precio de Venta", "Cantidad Vendida", "IVA", "Total de Venta sin IVA"}),
    #"Consultas combinadas" = Table.NestedJoin(#"Otras columnas quitadas", {"Producto"}, Catalogo_Sell_In, {"Producto"}, "Catalogo_Sell_In", JoinKind.LeftOuter),
    #"Se expandió Catalogo_Sell_In" = Table.ExpandTableColumn(#"Consultas combinadas", "Catalogo_Sell_In", {"UPC"}, {"UPC"}),
    #"Reemplazo Nuevo WM - Walmart" = Table.ReplaceValue(#"Se expandió Catalogo_Sell_In","NUEVA WAL MART DE MEXICO ","Walmart",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo Wm linea Wm Marketplace" = Table.ReplaceValue(#"Reemplazo Nuevo WM - Walmart","WALMART EN LINEA","Walmart Marketplace",Replacer.ReplaceText,{"Cliente"}),
    #"Remmplazo Publico Gen-AP Dist" = Table.ReplaceValue(#"Reemplazo Wm linea Wm Marketplace","PUBLICO EN GENERAL","Market Place",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo Servicios Amazon-" = Table.ReplaceValue(#"Remmplazo Publico Gen-AP Dist","SERVICIOS COMERCIALES AMAZON MEXICO ","Amazon",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo coppel" = Table.ReplaceValue(#"Reemplazo Servicios Amazon-","COPPEL EN LINEA","Coppel Marketplace",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo Farma Sana -Farmacia Sana" = Table.ReplaceValue(#"Reemplazo coppel","FARMA SANA SANA","Farmacia Sana Sana",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo Claudia-Mercado libre" = Table.ReplaceValue(#"Reemplazo Farma Sana -Farmacia Sana","CLAUDIA LEMOINE GOMEZ","Mercado Libre",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo Int Seguridad-Mercado libre" = Table.ReplaceValue(#"Reemplazo Claudia-Mercado libre","INSTITUTO DE SEGURIDAD Y SERVICIOS SOCIALES DE LOS TRABAJADORES DEL ESTADO","Mercado Libre",Replacer.ReplaceText,{"Cliente"}),
    #"Reemplazo Pharma Plus-San Pablo" = Table.ReplaceValue(#"Reemplazo Int Seguridad-Mercado libre","PHARMA PLUS","Farmacia San Pablo",Replacer.ReplaceText,{"Cliente"}),
    #"Filas filtradas1" = Table.SelectRows(#"Reemplazo Pharma Plus-San Pablo", each true),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Filas filtradas1",{{"Cantidad Vendida", Int64.Type}}),
    #"Personalizada agregada" = Table.AddColumn(#"Tipo cambiado1", "Calcular IVA", each ([Precio de Venta]*0.16)*[Cantidad Vendida]),
    #"Personalizada agregada1" = Table.AddColumn(#"Personalizada agregada", "TOTAL VENTA SIN IVA", each [Precio de Venta]*[Cantidad Vendida]),
    #"Columnas quitadas" = Table.RemoveColumns(#"Personalizada agregada1",{"Total de Venta sin IVA", "IVA", "TOTAL VENTA SIN IVA"})
in
    #"Columnas quitadas"

// ===== Consulta: TipoVenta =====
let
    Origen = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8s3PK8lXitWJVgrITK1KLFaKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Tipo = _t]),
    #"Tipo cambiado" = Table.TransformColumnTypes(Origen,{{"Tipo", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: TipoSellOut =====
let
    Origen = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8s3PK8lXitWJVgrITK1KLFaKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Tipo = _t]),
    #"Tipo cambiado" = Table.TransformColumnTypes(Origen,{{"Tipo", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: Inventario en Tienda WM =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Walmart\Inventarios en Tiendas - copia"),
    #"Filas ordenadas" = Table.Sort(Origen,{{"Name", Order.Ascending}}),
    #"Filas filtradas3" = Table.SelectRows(#"Filas ordenadas", each ([Name] <> "01-01-2026.xlsx")),
    #"Filas filtradas" = Table.SelectRows(#"Filas filtradas3", each [Extension] = ".xlsx"),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Filas filtradas",{"Content", "Name"}),
    #"Personalizada agregada" = Table.AddColumn(#"Otras columnas quitadas", "Personalizado", each Excel.Workbook([Content],true)),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Personalizada agregada",{"Personalizado", "Name"}),
    #"Se expandió Personalizado" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Personalizado", {"Name", "Data", "Item", "Kind", "Hidden"}, {"Name.1", "Data", "Item", "Kind", "Hidden"}),
    #"Filas filtradas1" = Table.SelectRows(#"Se expandió Personalizado", each ([Kind] = "Table") and ([Name.1] = "Inventario_Tiendas_WM")),
    #"Otras columnas quitadas2" = Table.SelectColumns(#"Filas filtradas1",{"Data", "Name"}),
    #"Se expandió Data" = Table.ExpandTableColumn(#"Otras columnas quitadas2", "Data", {"Financial Rpt Code", "UPC", "Item Nbr", "Store Nbr", "Item Status", "Item Type", "Curr Traited Store/Item Comb.", "Curr Valid Store/Item Comb.", "VNPK Qty", "WHPK Qty", "Curr Str On Hand Qty", "Curr Str In Transit Qty", "Curr Str In Whse Qty", "Curr Str On Order Qty", "POS Qty", "Max Shelf Qty", "City", "Street Address", "Building Address"}, {"Financial Rpt Code", "UPC", "Item Nbr", "Store Nbr", "Item Status", "Item Type", "Curr Traited Store/Item Comb.", "Curr Valid Store/Item Comb.", "VNPK Qty", "WHPK Qty", "Curr Str On Hand Qty", "Curr Str In Transit Qty", "Curr Str In Whse Qty", "Curr Str On Order Qty", "POS Qty", "Max Shelf Qty", "City", "Street Address", "Building Address"}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Se expandió Data",".xlsx","",Replacer.ReplaceText,{"Name"}),
     #"Personalizada agregada1" = Table.AddColumn(#"Valor reemplazado", "UPC.", each
    if [UPC] = "0743400255002" then "7434002550028" 
    else if [UPC] = "0743400255149" then "7434002551490"
    else if [UPC] = "0743100920749" then "7431009207498"
    else if [UPC] = "0743100920750" then "7431009207504"
    else 0),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Personalizada agregada1",{{"Name", type date}, {"Building Address", type text}, {"Street Address", type text},{"UPC.", type text}, {"Financial Rpt Code", type text}, {"UPC", type text}, {"Item Nbr", type text}, {"Store Nbr", Int64.Type}, {"Item Status", type text}, {"Item Type", type text}, {"Curr Traited Store/Item Comb.", Int64.Type}, {"Curr Valid Store/Item Comb.", Int64.Type}, {"VNPK Qty", Int64.Type}, {"WHPK Qty", Int64.Type}, {"Curr Str On Hand Qty", Int64.Type}, {"Curr Str In Transit Qty", Int64.Type}, {"Curr Str In Whse Qty", Int64.Type}, {"Curr Str On Order Qty", Int64.Type}, {"POS Qty", Int64.Type}, {"Max Shelf Qty", Int64.Type}, {"City", type text}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado",{{"Name", "Fecha"}}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Columnas con nombre cambiado",{"UPC"}),
    #"Filas filtradas2" = Table.SelectRows(#"Columnas quitadas", each true)
   
in
    #"Filas filtradas2"

// ===== Consulta: Recship WM =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Walmart\Recship WM"),
    #"Filas filtradas" = Table.SelectRows(Origen, each [Extension] = ".xlsx"),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Filas filtradas",{"Content", "Name"}),
    #"Personalizada agregada" = Table.AddColumn(#"Otras columnas quitadas", "Personalizado", each Excel.Workbook([Content],true)),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Personalizada agregada",{"Name", "Personalizado"}),
    #"Se expandió Personalizado" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Personalizado", {"Name", "Data", "Item", "Kind", "Hidden"}, {"Name.1", "Data", "Item", "Kind", "Hidden"}),
    #"Filas filtradas1" = Table.SelectRows(#"Se expandió Personalizado", each ([Kind] = "Table")),
    #"Otras columnas quitadas2" = Table.SelectColumns(#"Filas filtradas1",{"Name", "Data"}),
    #"Se expandió Data" = Table.ExpandTableColumn(#"Otras columnas quitadas2", "Data", {"UPC", "Item Nbr", "VNPK Qty", "VNPK Cost", "Plan Order Date", "Units"}, {"UPC", "Item Nbr", "VNPK Qty", "VNPK Cost", "Plan Order Date", "Units"}),
    #"Personalizada agregada1" = Table.AddColumn(#"Se expandió Data", "Monto", each [Units]*([VNPK Cost]/[VNPK Qty])),
    #"Valor reemplazado" = Table.ReplaceValue(#"Personalizada agregada1",".xlsx","",Replacer.ReplaceText,{"Name"}),
      // Reemplazo de código de Barras //
     #"Personalizada agregada2" = Table.AddColumn(#"Valor reemplazado", "UPC.", each if [UPC] = "0743400255002" then 7434002550028 else if [UPC] = "0743400255149" then 7434002551490 else if [UPC] = "0743100920749" then 7431009207498 else if [UPC] = "0743100920750" then 7431009207504 else if [UPC] = "0743100920748" then 743100920748 else 0),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Personalizada agregada2",{{"Name", type date}, {"Item Nbr", type text}, {"UPC", type text},{"UPC.", type text},{"VNPK Qty", Int64.Type}, {"VNPK Cost", type number}, {"Units", Int64.Type}, {"Monto", type number}}),
    #"Tipo cambiado con configuración regional" = Table.TransformColumnTypes(#"Tipo cambiado", {{"Plan Order Date", type date}}, "en-US"),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado con configuración regional",{{"Name", "Fecha"}}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Columnas con nombre cambiado",{"UPC"}),
    #"Filas filtradas2" = Table.SelectRows(#"Columnas quitadas", each ([Item Nbr] <> null))
  
in
    #"Filas filtradas2"

// ===== Consulta: Inventarios Wellpro =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Wellpro y Jaime\2025\Inventarios Wellpro"),
    #"Filas filtradas" = Table.SelectRows(Origen, each ([Extension] = ".xlsx")),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Filas filtradas",{"Content"}),
    #"Personalizada agregada" = Table.AddColumn(#"Otras columnas quitadas", "Personalizado", each Excel.Workbook([Content],true)),
    #"Se expandió Personalizado" = Table.ExpandTableColumn(#"Personalizada agregada", "Personalizado", {"Name", "Data", "Item", "Kind", "Hidden"}, {"Name", "Data", "Item", "Kind", "Hidden"}),
    #"Filas filtradas1" = Table.SelectRows(#"Se expandió Personalizado", each ([Kind] = "Table")),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Filas filtradas1",{"Data"}),
    #"Se expandió Data" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Data", {"Producto", "Almacén", "Fecha", "Documento", "Cant. Mov.", "Udm. Mov.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Disp. Vta."}, {"Producto", "Almacén", "Fecha", "Documento", "Cant. Mov.", "Udm. Mov.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Disp. Vta."}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Se expandió Data",{{"Producto", type text}, {"Almacén", type text}, {"Fecha", type date}, {"Documento", type text}, {"Cant. Mov.", Int64.Type}, {"Udm. Mov.", type text}, {"Udm. Inv.", type text}, {"Entrada", Int64.Type}, {"Salida", Int64.Type}, {"Exist. Alm.", Int64.Type}, {"Cto. Uni.", type number}, {"Disp. Vta.", Int64.Type}}),
    #"Dividir columna por delimitador" = Table.SplitColumn(#"Tipo cambiado", "Producto", Splitter.SplitTextByEachDelimiter({"-"}, QuoteStyle.Csv, false), {"Producto.1", "Producto.2"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Dividir columna por delimitador",{{"Producto.1", type text}, {"Producto.2", type text}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado1",{{"Producto.1", "Código Producto"}, {"Producto.2", "Descripción Producto"}}),
    #"Dividir columna por delimitador1" = Table.SplitColumn(#"Columnas con nombre cambiado", "Almacén", Splitter.SplitTextByDelimiter("-", QuoteStyle.Csv), {"Almacén.1", "Almacén.2"}),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Dividir columna por delimitador1",{{"Almacén.1", Int64.Type}, {"Almacén.2", type text}}),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Tipo cambiado2",{{"Almacén.1", "Número Almacén"}, {"Almacén.2", "Descripción Almacén"}})
in
    #"Columnas con nombre cambiado1"

// ===== Consulta: Inventario Amazon =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Amazon\Inventarios Amazon\2025"),
    #"Columna duplicada" = Table.DuplicateColumn(Origen, "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas reordenadas", {{"Name - Copia", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Name - Copia"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Name - Copia", type date}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado",{{"Name - Copia", "Fecha"}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Columnas con nombre cambiado",{"Content", "Name", "Fecha"}),
    #"Archivos ocultos filtrados1" = Table.SelectRows(#"Otras columnas quitadas", each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados1", "Transformar archivo (6)", each #"Transformar archivo (6)"([Content])),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Invocar función personalizada1", {"Transformar archivo (6)","Fecha"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo (6)", Table.ColumnNames(#"Transformar archivo (6)"(#"Archivo de ejemplo (6)"))),
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Columna de tabla expandida1", [PromoteAllScalars=true]),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Encabezados promovidos",{{"1/4/2026", "Fecha"}}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas con nombre cambiado1",{{"Unidades no aptas para la venta disponibles", Int64.Type}, {"ASIN", type text}, {"Título del Producto", type text}, {"Marca", type text}, {"Porcentaje de producto tercerizable no disponible temporalmente", type number}, {"Porcentaje de confirmación del proveedor", type number}, {"Recibido neto", type number}, {"Unidades netas recibidas", Int64.Type}, {"Cantidad de órdenes de compra abiertas", Int64.Type}, {"Porcentaje de cumplimiento de recepción", type number}, {"Tiempo total de entrega del proveedor (días)", Int64.Type}, {"Unidades pedidas por clientes no surtidas", Int64.Type}, {"Inventario apto para la venta de más de 90 días", type number}, {"Unidades aptas para la venta de más de 90 días", Int64.Type}, {"Inventario apto para la venta disponible", type number}, {"Unidades aptas para la venta disponibles", Int64.Type}, {"Inventario no apto para la venta disponible", type number}}),
    #"Filas filtradas" = Table.SelectRows(#"Tipo cambiado1", each ([ASIN] <> "ASIN") and ([Marca] <> "Marca")),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Filas filtradas",{{"Fecha", type date}}),
    #"Filas filtradas1" = Table.SelectRows(#"Tipo cambiado2", each true)
in
    #"Filas filtradas1"

// ===== Consulta: Catalogo_Sell_In =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\BD Sell In.xlsx"), null, true),
    Catalogo_Sell_In_Table = Origen{[Item="Catalogo_Sell_In",Kind="Table"]}[Data],
    #"Tipo cambiado" = Table.TransformColumnTypes(Catalogo_Sell_In_Table,{{"Producto", type text}, {"UPC", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: Fill_rate =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Walmart\Fill rate.xlsx"), null, true),
    Fill_rate_Sheet = Origen{[Item="Fill_rate",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(Fill_rate_Sheet, [PromoteAllScalars=true]),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Encabezados promovidos",{{"PO Number", Int64.Type}, {"PO Type", Int64.Type}, {"PO Event", type text}, {"PO Order Date", type text}, {"PO Cancel Date", type text}, {"PO Ship Date", type text}, {"UPC", Int64.Type}, {"Item Nbr", Int64.Type}, {"Item Flags", type any}, {"Signing Desc", type text}, {"Vendor Stk Nbr", Int64.Type}, {"Brand Desc", type text}, {"Item Type", Int64.Type}, {"Item Status", type text}, {"Unit Cost", type number}, {"VNPK Qty", Int64.Type}, {"VNPK Cost", type number}, {"WHPK Qty", Int64.Type}, {"WHPK Cost", type number}, {"Hist Eaches Str Ordered", Int64.Type}, {"Hist Eaches Str Received", Int64.Type}, {"Hist Eaches Whse Ordered", Int64.Type}, {"Hist Eaches Whse Received", Int64.Type}}),
    #"Tipo cambiado con configuración regional" = Table.TransformColumnTypes(#"Tipo cambiado2", {{"PO Cancel Date", type date}}, "en-US"),
    #"Tipo cambiado con configuración regional1" = Table.TransformColumnTypes(#"Tipo cambiado con configuración regional", {{"PO Order Date", type date}}, "en-US"),
    #"Tipo cambiado con configuración regional2" = Table.TransformColumnTypes(#"Tipo cambiado con configuración regional1", {{"PO Ship Date", type date}}, "en-US"),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Tipo cambiado con configuración regional2",{{"PO Number", type text}, {"PO Type", type text}, {"PO Event", type text}, {"PO Order Date", type date}, {"PO Cancel Date", type date}, {"PO Ship Date", type date}, {"UPC", Int64.Type}, {"Item Nbr", Int64.Type}, {"Item Flags", type any}, {"Signing Desc", type text}, {"Vendor Stk Nbr", Int64.Type}, {"Brand Desc", type text}, {"Item Type", Int64.Type}, {"Item Status", type text}, {"Unit Cost", type number}, {"VNPK Qty", Int64.Type}, {"VNPK Cost", type number}, {"WHPK Qty", Int64.Type}, {"WHPK Cost", type number}, {"Hist Eaches Str Ordered", Int64.Type}, {"Hist Eaches Str Received", Int64.Type}, {"Hist Eaches Whse Ordered", Int64.Type}, {"Hist Eaches Whse Received", Int64.Type}}),
    #"Remp Neb Familiar" = Table.ReplaceValue(#"Tipo cambiado",743400255002,7434002550028,Replacer.ReplaceValue,{"UPC"}),
    #"Remp Neb Elefante" = Table.ReplaceValue(#"Remp Neb Familiar",743400255149,7434002551490,Replacer.ReplaceValue,{"UPC"}),
    #"Remp Termtro Panda" = Table.ReplaceValue(#"Remp Neb Elefante",743100920749,7431009207498,Replacer.ReplaceValue,{"UPC"}),
    #"Remp Termtro Koala" = Table.ReplaceValue(#"Remp Termtro Panda",743100920750,7431009207504,Replacer.ReplaceValue,{"UPC"}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Remp Termtro Koala",{"Item Flags"}),

    #"No Entregado en Und" = Table.AddColumn(#"Columnas quitadas", "Und no Entregado", each [Hist Eaches Str Ordered]-[Hist Eaches Str Received]),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"No Entregado en Und",{{"Hist Eaches Str Ordered", "Ordenado en Und"}, {"Hist Eaches Str Received", "Entregado en Und"}}),
    #"Personalizada agregada" = Table.AddColumn(#"Columnas con nombre cambiado", "Cajas Ordenadas", each [Ordenado en Und]/[VNPK Qty]),
    #"Personalizada agregada1" = Table.AddColumn(#"Personalizada agregada", "Cajas Entregadas", each [Entregado en Und]/[VNPK Qty]),
    #"Personalizada agregada2" = Table.AddColumn(#"Personalizada agregada1", "Cajas no Entregadas", each [Cajas Ordenadas]-[Cajas Entregadas]),
    #"Personalizada agregada3" = Table.AddColumn(#"Personalizada agregada2", "Ordenado en $MX", each [Ordenado en Und]*[VNPK Cost]),
    #"Personalizada agregada4" = Table.AddColumn(#"Personalizada agregada3", "Entregado en $MX", each [Entregado en Und]*[VNPK Cost]),
    #"Personalizada agregada5" = Table.AddColumn(#"Personalizada agregada4", "No Entregado en $MX", each [#"Ordenado en $MX"]-[#"Entregado en $MX"]),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Personalizada agregada5",{{"No Entregado en $MX", type number}, {"Entregado en $MX", type number}, {"Ordenado en $MX", type number}, {"Cajas no Entregadas", Int64.Type}, {"Cajas Entregadas", Int64.Type}, {"Cajas Ordenadas", Int64.Type}, {"Und no Entregado", Int64.Type}}),
    #"Filas filtradas" = Table.SelectRows(#"Tipo cambiado1", each ([PO Number] <> null))
in
    #"Filas filtradas"

// ===== Consulta: Ventas Amazon mes actual =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\Escritorio\temp\Enero 2026\Septiembre 2026"),
    #"Filas filtradas" = Table.SelectRows(Origen, each ([Extension] = ".xlsx")),
    #"Columna duplicada" = Table.DuplicateColumn(#"Filas filtradas", "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columnas reordenadas",{{"Name - Copia", "Fecha"}}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas con nombre cambiado", {{"Fecha", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Fecha"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Fecha", type date}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Tipo cambiado",{"Content", "Name", "Fecha"}),
    #"Archivos ocultos filtrados1" = Table.SelectRows(#"Otras columnas quitadas", each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados1", "Transformar archivo", each #"Transformar archivo"([Content])),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Invocar función personalizada1", {"Transformar archivo","Fecha"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo", Table.ColumnNames(#"Transformar archivo"(#"Archivo de ejemplo"))),
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Columna de tabla expandida1", [PromoteAllScalars=true]),
    #"Filas filtradas1" = Table.SelectRows(#"Encabezados promovidos", each ([ASIN] <> "ASIN")),
    #"Errores quitados" = Table.RemoveRowsWithErrors(#"Filas filtradas1", {"Column9"}),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Errores quitados",{{"Column9", "Devoluciones del cliente"}}),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Columnas con nombre cambiado1",{{"ASIN", type text}, {"Título del Producto", type text}, {"Marca", type text}, {"Ganancia por envíos", type number}, {"COGS por envíos", type number}, {"Unidades enviadas", Int64.Type}, {"Devoluciones del cliente", Int64.Type}}),
    #"Columnas con nombre cambiado3" = Table.RenameColumns(#"Tipo cambiado2",{{"1/9/2026", "Fecha"}}),
    #"Filas filtradas3" = Table.SelectRows(#"Columnas con nombre cambiado3", each true),
    #"Filas filtradas2" = Table.SelectRows(#"Filas filtradas3", each true),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Filas filtradas2",{{"Ganancia por pedidos", Int64.Type}, {"Unidades pedidas", Int64.Type}, {"Ganancia por envíos", Int64.Type}, {"COGS por envíos", Int64.Type}, {"Unidades enviadas", Int64.Type}, {"Devoluciones del cliente", Int64.Type}})
in
    #"Tipo cambiado1"

// ===== Consulta: Tipo de cambio =====
let
    Origen = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMjJQio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Tipo_de_cambio = _t]),
    #"Tipo cambiado" = Table.TransformColumnTypes(Origen,{{"Tipo_de_cambio", Int64.Type}})
in
    #"Tipo cambiado"

// ===== Consulta: Ventas Amazon =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Amazon\Ventas Amazon"),
    #"Filas filtradas" = Table.SelectRows(Origen, each ([Extension] = ".xlsx")),
    #"Columna duplicada" = Table.DuplicateColumn(#"Filas filtradas", "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columnas reordenadas",{{"Name - Copia", "Fecha"}}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas con nombre cambiado", {{"Fecha", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Fecha"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Fecha", type date}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Tipo cambiado",{"Content", "Name", "Fecha"}),
    #"Archivos ocultos filtrados1" = Table.SelectRows(#"Otras columnas quitadas", each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados1", "Transformar archivo", each #"Transformar archivo"([Content])),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Invocar función personalizada1", {"Transformar archivo","Fecha"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo", Table.ColumnNames(#"Transformar archivo"(#"Archivo de ejemplo"))),
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Columna de tabla expandida1", [PromoteAllScalars=true]),
    #"Filas filtradas1" = Table.SelectRows(#"Encabezados promovidos", each ([ASIN] <> "ASIN")),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Filas filtradas1",{{"ASIN", type text}, {"Título del Producto", type text}, {"Marca", type text}, {"Ganancia por envíos", type number}, {"COGS por envíos", type number}, {"Unidades enviadas", Int64.Type}, {"Devoluciones del cliente", Int64.Type}}),
    #"Filas filtradas2" = Table.SelectRows(#"Tipo cambiado2", each ([ASIN] <> null)),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Filas filtradas2",{{"1/1/2025", "1/2/2024"}}),
    #"Columnas con nombre cambiado3" = Table.RenameColumns(#"Columnas con nombre cambiado1",{{"1/2/2024", "Fecha"}}),
    #"Tipo cambiado3" = Table.TransformColumnTypes(#"Columnas con nombre cambiado3",{{"Fecha", type date}, {"Ganancia por pedidos", type number}, {"Unidades pedidas", type number}}),
    #"Filas filtradas4" = Table.SelectRows(#"Tipo cambiado3", each true),
    #"Consultas combinadas" = Table.NestedJoin(#"Filas filtradas4", {"ASIN"}, Catalogo_Producto_Wellpro, {"ASIN"}, "Catalogo_Producto_Wellpro", JoinKind.LeftOuter),
    #"Se expandió Catalogo_Producto_Wellpro" = Table.ExpandTableColumn(#"Consultas combinadas", "Catalogo_Producto_Wellpro", {"UPC"}, {"Catalogo_Producto_Wellpro.UPC"}),
    #"Filas filtradas3" = Table.SelectRows(#"Se expandió Catalogo_Producto_Wellpro", each true),
    #"Columnas reordenadas1" = Table.ReorderColumns(#"Filas filtradas3",{"Catalogo_Producto_Wellpro.UPC", "ASIN", "Título del Producto", "Marca", "Ganancia por envíos", "COGS por envíos", "Unidades enviadas", "Devoluciones del cliente", "Fecha"}),
    #"Columnas con nombre cambiado2" = Table.RenameColumns(#"Columnas reordenadas1",{{"Catalogo_Producto_Wellpro.UPC", "UPC"}, {"Título del Producto", "Nombre del Producto"}, {"Ganancia por envíos", "Ingresos enviados"}, {"COGS por envíos", "COGS enviados"}}),
    #"Filas filtradas5" = Table.SelectRows(#"Columnas con nombre cambiado2", each true),
    #"Valor reemplazado1" = Table.ReplaceValue(#"Filas filtradas5","Prueba de Embarazo Wellpro Response Tipo Lápiz, 99.9% Precisión, Resultados en 5 Minutos, Detección Temprana de hormona, Fácil de Usar, No Invasiva","Prueba de Embarazo Wellpro Response Tipo Lápiz",Replacer.ReplaceValue,{"Nombre del Producto"}),
    #"Valor reemplazado2" = Table.ReplaceValue(#"Valor reemplazado1","Wellpro Kit de Nebulización Universal pediátrico Para Niños, Sin Látex","Wellpro Kit de Nebulización Universal pediátrico",Replacer.ReplaceValue,{"Nombre del Producto"}),
    #"Valor reemplazado3" = Table.ReplaceValue(#"Valor reemplazado2","Wellpro Cojín Cuadrado Memory Foam, con Funda Extraíble Lavable, Apoyo Terapéutico para Silla, Alivia Ciática así como Dolores en Cuello, Mejora Postura","Wellpro Cojín Cuadrado Memory Foam",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado4" = Table.ReplaceValue(#"Valor reemplazado3","Wellpro Silla de Baño con Respaldo, Altura Ajustable, Plástico Sin Látex, Soporta 113 Kg, Segura y cómoda para Adultos Mayores, Antideslizante","Wellpro Silla de Baño con Respaldo",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado5" = Table.ReplaceValue(#"Valor reemplazado4","Wellpro Inodoro Portátil con Tapa y Apoya Brazos, Diseño práctico, cómodo y muy seguro, Plástico Sin Látex, Soporta 110 Kg, con 2 Años Garantía","Wellpro Inodoro Portátil con Tapa y Apoya Brazos",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado6" = Table.ReplaceValue(#"Valor reemplazado5","Wellpro báscula Digital de vidrio transparente, altamente resistente, Pantalla LCD, sensor de Alta Precisión, diseño moderno y muy práctico","Wellpro báscula Digital de vidrio transparente",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado7" = Table.ReplaceValue(#"Valor reemplazado6","Wellpro Nebulizador pediátrico de Elefante Rosa, Compacto y Práctico para el Hogar, Silencioso, con diseño creativo y precisión clínica, 2 Años de Garantía","Wellpro báscula Digital de vidrio transparente",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado8" = Table.ReplaceValue(#"Valor reemplazado7","Wellpro Nebulizador pediátrico de Elefante Rosa, Compacto y Práctico para el Hogar, Silencioso, con diseño creativo y precisión clínica, 2 Años de Garantía","Wellpro Nebulizador pediátrico de Elefante Ros",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado9" = Table.ReplaceValue(#"Valor reemplazado8","Wellpro Termómetro Pediátrico Digital Diseño de Panda, Anatómico creado especialmente para Bebés y Niños, Lectura Rápida en 30 Segundos, Diseño práctico","Wellpro Termómetro Pediátrico Digital Diseño de Panda",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado10" = Table.ReplaceValue(#"Valor reemplazado9","Wellpro Termómetro Pediátrico Digital Diseño de Ranita, Anatómico creado especialmente para Bebés y Niños, Lectura Rápida en 30 Segundos, Diseño práctico","Wellpro Termómetro Pediátrico Digital Diseño de Ranita",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado11" = Table.ReplaceValue(#"Valor reemplazado10","Wellpro Termómetro Pediátrico Digital Diseño de Osito, Anatómico creado especialmente para Bebés y Niños, Lectura Rápida en 30 Segundos, Diseño práctico","Wellpro Termómetro Pediátrico Digital Diseño de Osito",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado12" = Table.ReplaceValue(#"Valor reemplazado11","Wellpro Termómetro Pediátrico Digital Diseño de Koala, Anatómico creado especialmente para Bebés y Niños, Lectura Rápida en 30 Segundos, Diseño práctico","Wellpro Termómetro Pediátrico Digital Diseño de Koala",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado13" = Table.ReplaceValue(#"Valor reemplazado12","Wellpro Nebulizador pediátrico de Búho Rosado, Compacto y Práctico para el Hogar, Silencioso, con diseño creativo y precisión clínica, 2 Años de Garantía","Wellpro Nebulizador pediátrico de Búho Rosado, Compacto y Práctico para el Hogar, Silencioso, con diseño creativo y precisión clínica, 2 Años de Garantía",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado14" = Table.ReplaceValue(#"Valor reemplazado13","Wellpro Nebulizador pediátrico de Búho Azul, Compacto y Práctico para el Hogar, Silencioso, con diseño creativo y precisión clínica, 2 Años de Garantía","Wellpro Nebulizador pediátrico de Búho Azul",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado15" = Table.ReplaceValue(#"Valor reemplazado14","Wellpro Nebulizador Familiar con tapa Verde, Compacto y Práctico para el Hogar, Silencioso y con precisión clínica, Compartimiento para Accesorios, 2 Años de Garantía","Wellpro Nebulizador Familiar con tapa Verde",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado16" = Table.ReplaceValue(#"Valor reemplazado15","Wellpro Nebulizador para Toda la Familia, Silencioso y Compacto con Precisión Clínica, Compartimiento para Accesorios, 2 Años de Garantía","Wellpro Nebulizador para Toda la Familia",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado17" = Table.ReplaceValue(#"Valor reemplazado16","Wellpro Nebulizador pediátrico de Búho Rosado, Compacto y Práctico para el Hogar, Silencioso, con diseño creativo y precisión clínica, 2 Años de Garantía","Wellpro Nebulizador pediátrico de Búho Rosado",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado18" = Table.ReplaceValue(#"Valor reemplazado17","Wellpro báscula Digital de vidrio,Superficie Antideslizante, Pantalla LCD, sensor de Alta Precisión, encendido y apagado Automático, diseño moderno","Wellpro báscula Digital de vidrio",Replacer.ReplaceText,{"Nombre del Producto"}),
    #"Valor reemplazado19" = Table.ReplaceValue(#"Valor reemplazado18","Wellpro báscula Digital de vidrio, muy práctica y resistente, Pantalla LCD, sensor de Alta Precisión, encendido y apagado Automático, diseño marmoleado","Wellpro báscula Digital de vidrio",Replacer.ReplaceText,{"Nombre del Producto"})
in
    #"Valor reemplazado19"

// ===== Consulta: Fillrate Amazon New =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Amazon\Fillrate AMAZON\POItemExport_2026-06-24.xls"), null, true),
    #"Líneas de artículos" = Origen{[Name="Líneas de artículos"]}[Data],
    #"Encabezados promovidos1" = Table.PromoteHeaders(#"Líneas de artículos", [PromoteAllScalars=true]),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Encabezados promovidos1",{{"Fecha del pedido", type date}, {"Fecha límite de cancelación", type date}, {"Fecha esperada", type date}, {"Fin del plazo", type date}, {"Inicio del plazo", type date}}),
    #"Filas filtradas1" = Table.SelectRows(#"Tipo cambiado2", each true),
    #"Tipo cambiado3" = Table.TransformColumnTypes(#"Filas filtradas1",{{"Fecha del pedido", type date}}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Tipo cambiado3",{{"Fecha del pedido", type date}, {"Fecha límite de cancelación", type date}, {"Cantidad solicitada", Int64.Type}, {"Cantidad aceptada", Int64.Type}, {"Cantidad ASN", Int64.Type}, {"Cantidad recibida", Int64.Type}, {"Cantidad cancelada", Int64.Type}, {"Cantidad restante", Int64.Type}}),
    #"Filas filtradas" = Table.SelectRows(#"Tipo cambiado1", each true),
    #"Tipo cambiado4" = Table.TransformColumnTypes(#"Filas filtradas",{{"Fecha del pedido", type date}})
in
    #"Tipo cambiado4"

// ===== Consulta: InventarioKardex =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\KARDEX"),
    #"Archivos ocultos filtrados1" = Table.SelectRows(Origen, each [Attributes]?[Hidden]? <> true),
    #"Archivos ocultos filtrados2" = Table.SelectRows(#"Archivos ocultos filtrados1", each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados2", "Transformar archivo (4)", each #"Transformar archivo (4)"([Content])),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Invocar función personalizada1", {"Name", "Source.Name"}),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Columnas con nombre cambiado1", {"Source.Name", "Transformar archivo (4)"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo (4)", Table.ColumnNames(#"Transformar archivo (4)"(#"Archivo de ejemplo (4)"))),
    #"Rellenar hacia abajo" = Table.FillDown(#"Columna de tabla expandida1",{"Fecha Registro", "Column2"}),
    #"Filas filtradas" = Table.SelectRows(#"Rellenar hacia abajo", each ([Column3] <> null)),
    #"Dividir columna por delimitador" = Table.SplitColumn(#"Filas filtradas", "Fecha Registro", Splitter.SplitTextByEachDelimiter({"-"}, QuoteStyle.Csv, false), {"Fecha Registro.1", "Fecha Registro.2"}),
    #"Tipo cambiado7" = Table.TransformColumnTypes(#"Dividir columna por delimitador",{{"Fecha", type date}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Tipo cambiado7",{{"Fecha Registro.1", type text}, {"Fecha Registro.2", type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Tipo cambiado","Producto:","",Replacer.ReplaceText,{"Fecha Registro.1"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Fecha", type date}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado1",{{"Fecha Registro.2", "Descripcion"}}),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"Exist. Alm.", Int64.Type}, {"Salida", Int64.Type}, {"Fecha", type date}}),
    #"Columna duplicada" = Table.DuplicateColumn(#"Tipo cambiado2", "Fecha", "Fecha - Copia"),
    #"Mes extraído" = Table.TransformColumns(#"Columna duplicada",{{"Fecha - Copia", Date.Month, Int64.Type}}),
    #"Columnas con nombre cambiado2" = Table.RenameColumns(#"Mes extraído",{{"Fecha - Copia", "MES"}}),
    #"Tipo cambiado3" = Table.TransformColumnTypes(#"Columnas con nombre cambiado2",{{"Entrada", Int64.Type}, {"MES", type number}}),
    #"Tipo cambiado4" = Table.TransformColumnTypes(#"Tipo cambiado3",{{"MES", Int64.Type}}),
    #"Personalizada agregada" = Table.AddColumn(#"Tipo cambiado4", "CostoEntradas", each [Entrada]*[#"Cto. Uni."]),
    #"Personalizada agregada1" = Table.AddColumn(#"Personalizada agregada", "SumSalidas", each [Salida]*[#"Cto. Uni."]),
    #"Columnas con nombre cambiado3" = Table.RenameColumns(#"Personalizada agregada1",{{"SumSalidas", "CostoSalidas"}}),
    #"Tipo cambiado5" = Table.TransformColumnTypes(#"Columnas con nombre cambiado3",{{"CostoSalidas", Int64.Type}, {"CostoEntradas", Int64.Type}}),
    #"Filas filtradas2" = Table.SelectRows(#"Tipo cambiado5", each true),
    #"Columnas con nombre cambiado4" = Table.RenameColumns(#"Filas filtradas2",{{"Fecha Registro.1", "CodArticulo"}}),
    #"Texto recortado" = Table.TransformColumns(#"Columnas con nombre cambiado4",{{"CodArticulo", Text.Trim, type text}}),
    #"Filas filtradas1" = Table.SelectRows(#"Texto recortado", each ([Fecha] <> #date(2025, 1, 31) and [Fecha] <> #date(2025, 3, 31))),
    #"Tipo cambiado6" = Table.TransformColumnTypes(#"Filas filtradas1",{{"Fecha", type date}}),
    #"Tipo cambiado con configuración regional" = Table.TransformColumnTypes(#"Tipo cambiado6", {{"Fecha", type date}}, "es-NI"),
    #"Personalizada agregada2" = Table.AddColumn(#"Tipo cambiado con configuración regional", "AÑO", each Date.AddYears([Fecha], 1)),
    #"Columnas quitadas2" = Table.RemoveColumns(#"Personalizada agregada2",{"AÑO"}),
    #"Filas filtradas5" = Table.SelectRows(#"Columnas quitadas2", each true),
    #"Personalizada agregada3" = Table.AddColumn(#"Filas filtradas5", "AÑO", each Date.Year([Fecha])),
    #"Personalizada agregada4" = Table.AddColumn(#"Personalizada agregada3", "MES.1", each Date.Month([Fecha])),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Personalizada agregada4",{"CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "CostoEntradas", "CostoSalidas", "AÑO", "MES", "MES.1"}),
    #"Columnas quitadas3" = Table.RemoveColumns(#"Columnas reordenadas",{"MES.1"}),
    #"Tipo cambiado8" = Table.TransformColumnTypes(#"Columnas quitadas3",{{"Fecha", type date}}),
    #"Filas filtradas3" = Table.SelectRows(#"Tipo cambiado8", each true),
    #"Tipo cambiado9" = Table.TransformColumnTypes(#"Filas filtradas3",{{"Cto. Mov.", Int64.Type}, {"Cto. Inv.", type number}, {"Cto. Uni.", Int64.Type}}),
    #"Filas filtradas4" = Table.SelectRows(#"Tipo cambiado9", each true),
    #"Tipo cambiado10" = Table.TransformColumnTypes(#"Filas filtradas4",{{"Cto. Prom.", type number}, {"Cto. Mov.", type number}}),
    #"Columnas con nombre cambiado5" = Table.RenameColumns(#"Tipo cambiado10",{{"Column2", "Almacen"}}),
    #"Tipo cambiado11" = Table.TransformColumnTypes(#"Columnas con nombre cambiado5",{{"Fecha", type date}}),
    #"Columnas con nombre cambiado6" = Table.RenameColumns(#"Tipo cambiado11",{{"Column3", "fecha2"}}),
    #"Tipo cambiado12" = Table.TransformColumnTypes(#"Columnas con nombre cambiado6",{{"fecha2", type date}, {"Disp. Vta.", Int64.Type}})
in
    #"Tipo cambiado12"

// ===== Consulta: CatalogoCuentas =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\CtalogoCuentasMX"),
    #"Archivos ocultos filtrados1" = Table.SelectRows(Origen, each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados1", "Transformar archivo (7)", each #"Transformar archivo (7)"([Content])),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Invocar función personalizada1", {"Name", "Source.Name"}),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Columnas con nombre cambiado1", {"Source.Name", "Transformar archivo (7)"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo (7)", Table.ColumnNames(#"Transformar archivo (7)"(#"Archivo de ejemplo (7)"))),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Columna de tabla expandida1",{{"Source.Name", type text}, {"CUENTAS", Int64.Type}, {"DESCRICION_CUENTAS", type text}, {"CATEGORÍA", type text}, {"SUBCATEGORÍA", type text}}),
    #"Filas filtradas" = Table.SelectRows(#"Tipo cambiado", each ([CUENTAS] <> null))
in
    #"Filas filtradas"

// ===== Consulta: Inventario Auxiliar =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\Inventario Auxiliar"),
    #"Archivos ocultos filtrados1" = Table.SelectRows(Origen, each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados1", "Transformar archivo (8)", each #"Transformar archivo (8)"([Content])),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Invocar función personalizada1", {"Name", "Source.Name"}),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Columnas con nombre cambiado1", {"Source.Name", "Transformar archivo (8)"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo (8)", Table.ColumnNames(#"Transformar archivo (8)"(#"Archivo de ejemplo (8)"))),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Columna de tabla expandida1",{{"Source.Name", type text}, {"Último Proveedor", type text}, {"Reorden", Int64.Type}, {"Mínimo", Int64.Type}, {"Máximo", Int64.Type}, {"Código Alm.", Int64.Type}, {"Código Pro.", type text}, {"Producto", type text}, {"Último Precio Vta.", type number}, {"Lote", Int64.Type}, {"UDM Inv.", type text}, {"Existencias", Int64.Type}, {"Costo Prom.", type number}, {"Costo Tot. Alm.", type number}, {"Último Costo ", type number}, {"En Pedido", Int64.Type}, {"Disponible", Int64.Type}, {"En Req.", Int64.Type}, {"En OC Inv.", Int64.Type}, {"UDM Comp.", type text}, {"Cant. Comp.", Int64.Type}, {"Categoría", type text}, {"Sub Categoría", type text}, {"Clasif. Gral.", type text}, {"Clasif. Contable", type text}, {"Cuenta", Int64.Type}, {"Nombre Cta.", type any}, {"Moneda Movimiento", type text}, {"Costo Moneda Movi", type number}, {"Tc Moneda Movi", Int64.Type}}),
    #"Filas filtradas2" = Table.SelectRows(#"Tipo cambiado", each ([Último Proveedor] <> null and [Último Proveedor] <> "Almacén: PRODUCTOS PROMOCIONALES - 3 ")),
    #"Columnas quitadas" = Table.RemoveColumns(#"Filas filtradas2",{"Reorden", "Mínimo", "Máximo"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas quitadas",{{"Disponible", Int64.Type}, {"Código Pro.", type text}}),
    #"Texto recortado" = Table.TransformColumns(#"Tipo cambiado1",{{"Código Pro.", Text.Trim, type text}}),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Texto recortado",{{"Existencias", Int64.Type}}),
    #"Filas filtradas1" = Table.SelectRows(#"Tipo cambiado2", each ([#"Código Alm."] <> null))
in
    #"Filas filtradas1"

// ===== Consulta: InventarioKardex (2) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\KARDEX"),
    #"Archivos ocultos filtrados1" = Table.SelectRows(Origen, each [Attributes]?[Hidden]? <> true),
    #"Archivos ocultos filtrados2" = Table.SelectRows(#"Archivos ocultos filtrados1", each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada1" = Table.AddColumn(#"Archivos ocultos filtrados2", "Transformar archivo (4)", each #"Transformar archivo (4)"([Content])),
    #"Columnas con nombre cambiado1" = Table.RenameColumns(#"Invocar función personalizada1", {"Name", "Source.Name"}),
    #"Otras columnas quitadas1" = Table.SelectColumns(#"Columnas con nombre cambiado1", {"Source.Name", "Transformar archivo (4)"}),
    #"Columna de tabla expandida1" = Table.ExpandTableColumn(#"Otras columnas quitadas1", "Transformar archivo (4)", Table.ColumnNames(#"Transformar archivo (4)"(#"Archivo de ejemplo (4)"))),
    #"Rellenar hacia abajo" = Table.FillDown(#"Columna de tabla expandida1",{"Fecha Registro", "Column2"}),
    #"Filas filtradas" = Table.SelectRows(#"Rellenar hacia abajo", each ([Column3] <> null)),
    #"Dividir columna por delimitador" = Table.SplitColumn(#"Filas filtradas", "Fecha Registro", Splitter.SplitTextByEachDelimiter({"-"}, QuoteStyle.Csv, false), {"Fecha Registro.1", "Fecha Registro.2"}),
    #"Tipo cambiado7" = Table.TransformColumnTypes(#"Dividir columna por delimitador",{{"Fecha", type date}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Tipo cambiado7",{{"Fecha Registro.1", type text}, {"Fecha Registro.2", type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Tipo cambiado","Producto:","",Replacer.ReplaceText,{"Fecha Registro.1"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Fecha", type date}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado1",{{"Fecha Registro.2", "Descripcion"}}),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"Exist. Alm.", Int64.Type}, {"Salida", Int64.Type}, {"Fecha", type date}}),
    #"Columna duplicada" = Table.DuplicateColumn(#"Tipo cambiado2", "Fecha", "Fecha - Copia"),
    #"Mes extraído" = Table.TransformColumns(#"Columna duplicada",{{"Fecha - Copia", Date.Month, Int64.Type}}),
    #"Columnas con nombre cambiado2" = Table.RenameColumns(#"Mes extraído",{{"Fecha - Copia", "MES"}}),
    #"Tipo cambiado3" = Table.TransformColumnTypes(#"Columnas con nombre cambiado2",{{"Entrada", Int64.Type}, {"MES", type number}}),
    #"Tipo cambiado4" = Table.TransformColumnTypes(#"Tipo cambiado3",{{"MES", Int64.Type}}),
    #"Personalizada agregada" = Table.AddColumn(#"Tipo cambiado4", "CostoEntradas", each [Entrada]*[#"Cto. Uni."]),
    #"Personalizada agregada1" = Table.AddColumn(#"Personalizada agregada", "SumSalidas", each [Salida]*[#"Cto. Uni."]),
    #"Columnas con nombre cambiado3" = Table.RenameColumns(#"Personalizada agregada1",{{"SumSalidas", "CostoSalidas"}}),
    #"Tipo cambiado5" = Table.TransformColumnTypes(#"Columnas con nombre cambiado3",{{"CostoSalidas", Int64.Type}, {"CostoEntradas", Int64.Type}}),
    #"Filas filtradas2" = Table.SelectRows(#"Tipo cambiado5", each true),
    #"Columnas con nombre cambiado4" = Table.RenameColumns(#"Filas filtradas2",{{"Fecha Registro.1", "CodArticulo"}}),
    #"Texto recortado" = Table.TransformColumns(#"Columnas con nombre cambiado4",{{"CodArticulo", Text.Trim, type text}}),
    #"Filas filtradas1" = Table.SelectRows(#"Texto recortado", each ([Fecha] <> #date(2025, 1, 31) and [Fecha] <> #date(2025, 3, 31))),
    #"Tipo cambiado6" = Table.TransformColumnTypes(#"Filas filtradas1",{{"Fecha", type date}}),
    #"Tipo cambiado con configuración regional" = Table.TransformColumnTypes(#"Tipo cambiado6", {{"Fecha", type date}}, "es-NI"),
    #"Personalizada agregada2" = Table.AddColumn(#"Tipo cambiado con configuración regional", "AÑO", each Date.AddYears([Fecha], 1)),
    #"Columnas quitadas2" = Table.RemoveColumns(#"Personalizada agregada2",{"AÑO"}),
    #"Filas filtradas5" = Table.SelectRows(#"Columnas quitadas2", each true),
    #"Personalizada agregada3" = Table.AddColumn(#"Filas filtradas5", "AÑO", each Date.Year([Fecha])),
    #"Personalizada agregada4" = Table.AddColumn(#"Personalizada agregada3", "MES.1", each Date.Month([Fecha])),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Personalizada agregada4",{"CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "CostoEntradas", "CostoSalidas", "AÑO", "MES", "MES.1"}),
    #"Columnas quitadas3" = Table.RemoveColumns(#"Columnas reordenadas",{"MES.1"}),
    #"Tipo cambiado8" = Table.TransformColumnTypes(#"Columnas quitadas3",{{"Fecha", type date}}),
    #"Filas filtradas3" = Table.SelectRows(#"Tipo cambiado8", each true),
    #"Tipo cambiado9" = Table.TransformColumnTypes(#"Filas filtradas3",{{"Cto. Mov.", Int64.Type}, {"Cto. Inv.", type number}, {"Cto. Uni.", Int64.Type}}),
    #"Tipo cambiado10" = Table.TransformColumnTypes(#"Tipo cambiado9",{{"Cto. Prom.", type number}, {"Cto. Mov.", type number}}),
    #"Columnas con nombre cambiado5" = Table.RenameColumns(#"Tipo cambiado10",{{"Column2", "Almacen"}}),
    #"Tipo cambiado11" = Table.TransformColumnTypes(#"Columnas con nombre cambiado5",{{"Fecha", type date}}),
    #"Columnas con nombre cambiado6" = Table.RenameColumns(#"Tipo cambiado11",{{"Column3", "fecha2"}}),
    #"Tipo cambiado12" = Table.TransformColumnTypes(#"Columnas con nombre cambiado6",{{"fecha2", type date}, {"Disp. Vta.", Int64.Type}})
in
    #"Tipo cambiado12"

// ===== Consulta: Tbl =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\Movimientos INV\Inventarios.xlsx"), null, true),
    Tbl_Sheet = Origen{[Item="Tbl",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(Tbl_Sheet, [PromoteAllScalars=true]),
    #"Columnas quitadas1" = Table.RemoveColumns(#"Encabezados promovidos",{"COSTO", "Column11", "Column12", "Column13", "Column14", "Column15"}),
    #"Filas filtradas" = Table.SelectRows(#"Columnas quitadas1", each ([Fecha] <> null)),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Filas filtradas",{{"Fecha", type date}, {"COSTOS", type number}, {"Inventario Inicial", Int64.Type}, {"Compra", Int64.Type}, {"Entrada dev", Int64.Type}, {"Salida", Int64.Type}, {"Salida Almacen", Int64.Type}, {"Inventario Final", Currency.Type}, {"Descripcion", type text}})
in
    #"Tipo cambiado"

// ===== Consulta: Costos =====
let
    Origen = Excel.Workbook(File.Contents("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\Movimientos INV\Inventarios.xlsx"), null, true),
    Costos_Sheet = Origen{[Item="Costos",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(Costos_Sheet, [PromoteAllScalars=true]),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos",{{"PRODUCTO", type text}, {"COSTO", type number}, {"Column3", type any}, {"Column4", type any}}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Tipo cambiado",{"Column3", "Column4"})
in
    #"Columnas quitadas"

// ################################################################################################
// PARTE 2. CONSULTAS AUXILIARES Y SIN CARGAR (34)
// ################################################################################################

// ===== Consulta: Archivo de ejemplo =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Amazon\Ventas Amazon"),
    #"Filas filtradas" = Table.SelectRows(Origen, each ([Extension] = ".xlsx")),
    #"Columna duplicada" = Table.DuplicateColumn(#"Filas filtradas", "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columnas reordenadas",{{"Name - Copia", "Fecha"}}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas con nombre cambiado", {{"Fecha", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Fecha"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Fecha", type date}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Tipo cambiado",{"Content", "Name", "Fecha"}),
    Navegación1 = #"Otras columnas quitadas"{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo =====
let
    Origen = (Parámetro1 as binary) => let
    Origen = Excel.Workbook(Parámetro1, null, true),
    Ventas_Amazon_Table = Origen{[Item="Ventas_Amazon",Kind="Table"]}[Data]
in
    Ventas_Amazon_Table
in
    Origen

// ===== Consulta: Archivo de ejemplo (6) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Documentos\IMFORME WELLPRO Y JAIME MX\Amazon\Inventarios Amazon\2025"),
    #"Columna duplicada" = Table.DuplicateColumn(Origen, "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas reordenadas", {{"Name - Copia", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Name - Copia"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Valor reemplazado",{{"Name - Copia", type date}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado",{{"Name - Copia", "Fecha"}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Columnas con nombre cambiado",{"Content", "Name", "Fecha"}),
    Navegación1 = #"Otras columnas quitadas"{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo (6) =====
let
    Origen = (Parámetro6 as binary) => let
    Origen = Excel.Workbook(Parámetro6, null, true),
    Inventario_Amazon_Table = Origen{[Item="Inventario_Amazon",Kind="Table"]}[Data]
in
    Inventario_Amazon_Table
in
    Origen

// ===== Consulta: Archivo de ejemplo (3) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\ER -ONE GOAL"),
    #"Columna duplicada" = Table.DuplicateColumn(Origen, "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columnas reordenadas",{{"Name - Copia", "Fecha"}}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas con nombre cambiado", {{"Fecha", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Fecha"}),
    #"Primeros caracteres extraídos1" = Table.TransformColumns(#"Valor reemplazado", {{"Fecha", each Text.Start(_, 11), type text}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Primeros caracteres extraídos1",{{"Fecha", type date}}),
    #"Primeros caracteres extraídos" = Table.TransformColumns(#"Tipo cambiado", {{"Fecha", each Text.Start(Text.From(_, "es-NI"), 11), type text}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Primeros caracteres extraídos",{"Content", "Name", "Fecha"}),
    #"Archivos ocultos filtrados1" = Table.SelectRows(#"Otras columnas quitadas", each [Attributes]?[Hidden]? <> true),
    Navegación1 = #"Archivos ocultos filtrados1"{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo (3) =====
let
    Source = (Parámetro3 as binary) => let
    Origen = Excel.Workbook(Parámetro3, null, true),
    Sheet2 = Origen{[Name="Sheet1"]}[Data]
in
    Sheet2
in
    Source

// ===== Consulta: Balanza de comprobacion =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\ER -ONE GOAL"),
    #"Columna duplicada" = Table.DuplicateColumn(Origen, "Name", "Name - Copia"),
    #"Columnas reordenadas" = Table.ReorderColumns(#"Columna duplicada",{"Content", "Name", "Name - Copia", "Extension", "Date accessed", "Date modified", "Date created", "Attributes", "Folder Path"}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columnas reordenadas",{{"Name - Copia", "Fecha"}}),
    #"Últimos caracteres extraídos" = Table.TransformColumns(#"Columnas con nombre cambiado", {{"Fecha", each Text.End(_, 15), type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Últimos caracteres extraídos",".xlsx","",Replacer.ReplaceText,{"Fecha"}),
    #"Primeros caracteres extraídos1" = Table.TransformColumns(#"Valor reemplazado", {{"Fecha", each Text.Start(_, 11), type text}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Primeros caracteres extraídos1",{{"Fecha", type date}}),
    #"Primeros caracteres extraídos" = Table.TransformColumns(#"Tipo cambiado", {{"Fecha", each Text.Start(Text.From(_, "es-NI"), 11), type text}}),
    #"Otras columnas quitadas" = Table.SelectColumns(#"Primeros caracteres extraídos",{"Content", "Name", "Fecha"}),
    #"Archivos ocultos filtrados1" = Table.SelectRows(#"Otras columnas quitadas", each [Attributes]?[Hidden]? <> true),
    #"Archivos ocultos filtrados2" = Table.SelectRows(#"Archivos ocultos filtrados1", each [Attributes]?[Hidden]? <> true),
    #"Invocar función personalizada2" = Table.AddColumn(#"Archivos ocultos filtrados2", "Transformar archivo (3)", each #"Transformar archivo (3)"([Content])),
    #"Otras columnas quitadas2" = Table.SelectColumns(#"Invocar función personalizada2", {"Transformar archivo (3)"}),
    #"Columna de tabla expandida2" = Table.ExpandTableColumn(#"Otras columnas quitadas2", "Transformar archivo (3)", Table.ColumnNames(#"Transformar archivo (3)"(#"Archivo de ejemplo (3)"))),
    #"Invocar función personalizada1" = Table.AddColumn(#"Columna de tabla expandida2", "Transformar archivo", each #"Transformar archivo"([Content])),
    #"Filas filtradas" = Table.SelectRows(#"Invocar función personalizada1", each ([Column1] <> null and [Column1] <> "-" and [Column1] <> "Balanza de Comprobación" and [Column1] <> "Ejercicio: 2025#(lf)Período: de ABR a ABR#(lf)Nivel: Todas las Cuentas" and [Column1] <> "Ejercicio: 2025#(lf)Período: de AGO a AGO#(lf)Nivel: Todas las Cuentas")),
    #"Columnas quitadas2" = Table.RemoveColumns(#"Filas filtradas",{"Transformar archivo", "Column18"}),
    #"Encabezados promovidos1" = Table.PromoteHeaders(#"Columnas quitadas2", [PromoteAllScalars=true]),
    #"Columnas quitadas1" = Table.RemoveColumns(#"Encabezados promovidos1",{"Columna1", "Columna2", "Columna3", "Columna4", "Columna5", "Columna6", "Columna7", "Columna8", "Columna9"}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas quitadas1",{{"Saldo Inicial", type number}, {"Cargos", type number}, {"Abonos", type number}, {"Cambio Neto", type number}, {"Saldo Final", type number}, {"MES", type text}})
in
    #"Tipo cambiado1"

// ===== Consulta: Parámetro1 =====
#"Archivo de ejemplo (2)" meta [IsParameterQuery=true, BinaryIdentifier=#"Archivo de ejemplo (2)", Type="Binary", IsParameterQueryRequired=true]

// ===== Consulta: Archivo de ejemplo (2) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\Inventario MX"),
    #"Conservar errores" = Table.SelectRowsWithErrors(Origen)
in
    #"Conservar errores"

// ===== Consulta: Transformar archivo (2) =====
let
    Origen = (Parámetro1 as binary) => let
    Origen = Excel.Workbook(Parámetro1, null, true),
    Sheet1 = Origen{[Name="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(Sheet1, [PromoteAllScalars=true])
in
    #"Encabezados promovidos"
in
    Origen

// ===== Consulta: Parámetro2 =====
#"Archivo de ejemplo (4)" meta [IsParameterQuery=true, BinaryIdentifier=#"Archivo de ejemplo (4)", Type="Binary", IsParameterQueryRequired=true]

// ===== Consulta: Transformar archivo de ejemplo (2) =====
let
    Origen = Excel.Workbook(Parámetro2, null, true),
    #"Hoja 1_Sheet" = Origen{[Item="Hoja 1",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Hoja 1_Sheet", [PromoteAllScalars=true])
in
    #"Encabezados promovidos"

// ===== Consulta: Archivo de ejemplo (4) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\KARDEX"),
    #"Archivos ocultos filtrados1" = Table.SelectRows(Origen, each [Attributes]?[Hidden]? <> true),
    Navegación1 = #"Archivos ocultos filtrados1"{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo (4) =====
let
    Origen = (Parámetro2 as binary) => let
    Origen = Excel.Workbook(Parámetro2, null, true),
    #"Hoja 1_Sheet" = Origen{[Item="Hoja 1",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Hoja 1_Sheet", [PromoteAllScalars=true])
in
    #"Encabezados promovidos"
in
    Origen

// ===== Consulta: Parámetro3 =====
#"Archivo de ejemplo (5)" meta [IsParameterQuery=true, BinaryIdentifier=#"Archivo de ejemplo (5)", Type="Binary", IsParameterQueryRequired=true]

// ===== Consulta: Transformar archivo de ejemplo (3) =====
let
    Origen = Excel.Workbook(Parámetro3, null, true),
    Sheet2 = Origen{[Name="Sheet1"]}[Data]
in
    Sheet2

// ===== Consulta: Archivo de ejemplo (5) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\Balanza de comprobación"),
    Navegación1 = Origen{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo (5) =====
let
    Origen = (Parámetro3 as binary) => let
    Origen = Excel.Workbook(Parámetro3, null, true),
    Sheet2 = Origen{[Name="Sheet1"]}[Data]
in
    Sheet2
in
    Origen

// ===== Consulta: Parámetro4 =====
#"Archivo de ejemplo (7)" meta [IsParameterQuery=true, BinaryIdentifier=#"Archivo de ejemplo (7)", Type="Binary", IsParameterQueryRequired=true]

// ===== Consulta: Transformar archivo de ejemplo (4) =====
let
    Origen = Excel.Workbook(Parámetro4, null, true),
    #"Table 3_Sheet" = Origen{[Item="Table 3",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Table 3_Sheet", [PromoteAllScalars=true])
in
    #"Encabezados promovidos"

// ===== Consulta: Archivo de ejemplo (7) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\CtalogoCuentasMX"),
    Navegación1 = Origen{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo (7) =====
let
    Origen = (Parámetro4 as binary) => let
    Origen = Excel.Workbook(Parámetro4, null, true),
    #"Table 3_Sheet" = Origen{[Item="Table 3",Kind="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(#"Table 3_Sheet", [PromoteAllScalars=true])
in
    #"Encabezados promovidos"
in
    Origen

// ===== Consulta: Parámetro5 =====
#"Archivo de ejemplo (8)" meta [IsParameterQuery=true, BinaryIdentifier=#"Archivo de ejemplo (8)", Type="Binary", IsParameterQueryRequired=true]

// ===== Consulta: Transformar archivo de ejemplo (5) =====
let
    Origen = Excel.Workbook(Parámetro5, null, true),
    Sheet1 = Origen{[Name="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(Sheet1, [PromoteAllScalars=true])
in
    #"Encabezados promovidos"

// ===== Consulta: Archivo de ejemplo (8) =====
let
    Origen = Folder.Files("C:\Users\jolivas\OneDrive - VISION MEDICA S.A\Imágenes\Reportes Mexico\Inventario Auxiliar"),
    Navegación1 = Origen{0}[Content]
in
    Navegación1

// ===== Consulta: Transformar archivo (8) =====
let
    Origen = (Parámetro5 as binary) => let
    Origen = Excel.Workbook(Parámetro5, null, true),
    Sheet1 = Origen{[Name="Sheet"]}[Data],
    #"Encabezados promovidos" = Table.PromoteHeaders(Sheet1, [PromoteAllScalars=true])
in
    #"Encabezados promovidos"
in
    Origen

// ===== Consulta: Errores en InventarioKardex =====
let
Origen = InventarioKardex,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"})
in
  #"Columnas reordenadas"

// ===== Consulta: Errores en InventarioKardex (2) =====
let
Origen = InventarioKardex,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"}),
    #"Conservar errores1" = Table.SelectRowsWithErrors(#"Columnas reordenadas")
in
  #"Conservar errores1"

// ===== Consulta: Errores en InventarioKardex (3) =====
let
Origen = InventarioKardex,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"})
in
  #"Columnas reordenadas"

// ===== Consulta: Errores en InventarioKardex (4) =====
let
Origen = InventarioKardex,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "CodArticulo", "Descripcion", "Fecha", "Código Doc.", "Documento", "Tipo", "Cant. Mov.", "Udm. Mov.", "Factor. Inv.", "Udm. Inv.", "Entrada", "Salida", "Exist. Alm.", "Cto. Uni.", "Cto. Prom.", "Cto. Mov.", "Cto. Inv.", "Disp. Vta.", "Categoria", "Cód. Trabajo", "CostoEntradas", "CostoSalidas", "AÑO", "MES"}),
    #"Filas filtradas" = Table.SelectRows(#"Columnas reordenadas", each ([Descripcion] = "Termometro Pediatrico Cerdito "))
in
    #"Filas filtradas"

// ===== Consulta: Errores en Sell_Out_WM =====
let
Origen = Sell_Out_WM,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Item Status", "Item Type", "Dept Desc", "Fineline", "Fineline Desc", "Financial Rpt Code", "City", "Street Address", "Store Nbr", "Store Name", "Store Specific Retail", "Store Specific Cost", "POS Qty", "POS Sales", "POS Cost", "Corp Cancel When Out Flag", "Accounting Comp Flag", "Order book Flag", "Item Sub Type", "Vndr Min Ord Qty", "Max Str Order Qty", "Acct Dept Nbr", "Vendor Nbr Dept", "Vendor Sequence Nbr", "Sales Type", "Sales Description", "Daily", "año", "mes"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Item Status", "Item Type", "Dept Desc", "Fineline", "Fineline Desc", "Financial Rpt Code", "City", "Street Address", "Store Nbr", "Store Name", "Store Specific Retail", "Store Specific Cost", "POS Qty", "POS Sales", "POS Cost", "Corp Cancel When Out Flag", "Accounting Comp Flag", "Order book Flag", "Item Sub Type", "Vndr Min Ord Qty", "Max Str Order Qty", "Acct Dept Nbr", "Vendor Nbr Dept", "Vendor Sequence Nbr", "Sales Type", "Sales Description", "Daily", "año", "mes"})
in
  #"Columnas reordenadas"

// ===== Consulta: Errores en Fill_rate =====
let
Origen = Fill_rate,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"PO Number", "PO Type", "PO Event", "PO Order Date", "PO Cancel Date", "PO Ship Date", "UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Brand Desc", "Item Type", "Item Status", "Unit Cost", "VNPK Qty", "VNPK Cost", "WHPK Qty", "WHPK Cost", "Ordenado en Und", "Entregado en Und", "Hist Eaches Whse Ordered", "Hist Eaches Whse Received", "Und no Entregado", "Cajas Ordenadas", "Cajas Entregadas", "Cajas no Entregadas", "Ordenado en $MX", "Entregado en $MX", "No Entregado en $MX"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "PO Number", "PO Type", "PO Event", "PO Order Date", "PO Cancel Date", "PO Ship Date", "UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Brand Desc", "Item Type", "Item Status", "Unit Cost", "VNPK Qty", "VNPK Cost", "WHPK Qty", "WHPK Cost", "Ordenado en Und", "Entregado en Und", "Hist Eaches Whse Ordered", "Hist Eaches Whse Received", "Und no Entregado", "Cajas Ordenadas", "Cajas Entregadas", "Cajas no Entregadas", "Ordenado en $MX", "Entregado en $MX", "No Entregado en $MX"})
in
  #"Columnas reordenadas"

// ===== Consulta: Errores en Sell_Out_WM (2) =====
let
Origen = Sell_Out_WM,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Item Status", "Item Type", "Dept Desc", "Fineline", "Fineline Desc", "Financial Rpt Code", "City", "Street Address", "Store Nbr", "Store Name", "Store Specific Retail", "Store Specific Cost", "POS Qty", "POS Sales", "POS Cost", "Corp Cancel When Out Flag", "Accounting Comp Flag", "Order book Flag", "Item Sub Type", "Vndr Min Ord Qty", "Max Str Order Qty", "Acct Dept Nbr", "Vendor Nbr Dept", "Vendor Sequence Nbr", "Sales Type", "Sales Description", "Daily", "año", "mes"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Item Status", "Item Type", "Dept Desc", "Fineline", "Fineline Desc", "Financial Rpt Code", "City", "Street Address", "Store Nbr", "Store Name", "Store Specific Retail", "Store Specific Cost", "POS Qty", "POS Sales", "POS Cost", "Corp Cancel When Out Flag", "Accounting Comp Flag", "Order book Flag", "Item Sub Type", "Vndr Min Ord Qty", "Max Str Order Qty", "Acct Dept Nbr", "Vendor Nbr Dept", "Vendor Sequence Nbr", "Sales Type", "Sales Description", "Daily", "año", "mes"})
in
  #"Columnas reordenadas"

// ===== Consulta: Errores en Fill_rate (2) =====
let
Origen = Fill_rate,
  #"Errores de coincidencia detectados" = let
    tableWithOnlyPrimitiveTypes = Table.SelectColumns(Origen, Table.ColumnsOfType(Origen, {type nullable number, type nullable text, type nullable logical, type nullable date, type nullable datetime, type nullable datetimezone, type nullable time, type nullable duration})),
    recordTypeFields = Type.RecordFields(Type.TableRow(Value.Type(tableWithOnlyPrimitiveTypes))),
    fieldNames = Record.FieldNames(recordTypeFields),
    fieldTypes = List.Transform(Record.ToList(recordTypeFields), each [Type]),
    pairs = List.Transform(List.Positions(fieldNames), (i) => {fieldNames{i}, (v) => if v = null or Value.Is(v, fieldTypes{i}) then v else error [Message = "El tipo del valor no coincide con el tipo de la columna.", Detail = v], fieldTypes{i}})
in
    Table.TransformColumns(Origen, pairs),
  #"Índice agregado" = Table.AddIndexColumn(#"Errores de coincidencia detectados", "Número de fila" ,1),
  #"Conservar errores" = Table.SelectRowsWithErrors(#"Índice agregado", {"PO Number", "PO Type", "PO Event", "PO Order Date", "PO Cancel Date", "PO Ship Date", "UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Brand Desc", "Item Type", "Item Status", "Unit Cost", "VNPK Qty", "VNPK Cost", "WHPK Qty", "WHPK Cost", "Ordenado en Und", "Entregado en Und", "Hist Eaches Whse Ordered", "Hist Eaches Whse Received", "Und no Entregado", "Cajas Ordenadas", "Cajas Entregadas", "Cajas no Entregadas", "Ordenado en $MX", "Entregado en $MX", "No Entregado en $MX"}),
  #"Columnas reordenadas" = Table.ReorderColumns(#"Conservar errores", {"Número de fila", "PO Number", "PO Type", "PO Event", "PO Order Date", "PO Cancel Date", "PO Ship Date", "UPC", "Item Nbr", "Signing Desc", "Vendor Stk Nbr", "Brand Desc", "Item Type", "Item Status", "Unit Cost", "VNPK Qty", "VNPK Cost", "WHPK Qty", "WHPK Cost", "Ordenado en Und", "Entregado en Und", "Hist Eaches Whse Ordered", "Hist Eaches Whse Received", "Und no Entregado", "Cajas Ordenadas", "Cajas Entregadas", "Cajas no Entregadas", "Ordenado en $MX", "Entregado en $MX", "No Entregado en $MX"}),
    #"Conservar errores1" = Table.SelectRowsWithErrors(#"Columnas reordenadas")
in
  #"Conservar errores1"

