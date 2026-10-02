# Herramienta interna (Claude): genera desde cero el proyecto powerbi/Reporte Wellpro.*
# (modelo TMDL y reporte PBIR). NO la ejecutes a mano: borra y vuelve a escribir esas carpetas,
# así que cualquier cambio hecho en Power BI Desktop se perdería. Requiere Python 3.
import os, json, uuid, shutil, textwrap

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '..', '..', 'powerbi'))
NOMBRE = 'Reporte Wellpro'
SM = f'{RAIZ}/{NOMBRE}.SemanticModel'
RP = f'{RAIZ}/{NOMBRE}.Report'
TEMA_BASE = os.path.join(AQUI, 'recursos', 'Fluent2-CY26SU08.json')

IDS = {}
for _k, _p in (('SM', f'{SM}/.platform'), ('RP', f'{RP}/.platform')):
    if os.path.exists(_p):
        IDS[_k] = json.load(open(_p, encoding='utf-8'))['config']['logicalId']
# se regeneran solo las carpetas del proyecto; LEEME.md y otros archivos sueltos se conservan
for _d in (SM, RP):
    if os.path.exists(_d):
        shutil.rmtree(_d)

def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
        f.write(texto)

def jdump(ruta, obj):
    escribir(ruta, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def bloque(m, tabs):
    """Indenta código M/DAX con tabulaciones para TMDL."""
    m = textwrap.dedent(m).strip('\n')
    return '\n'.join(('\t' * tabs + l) if l.strip() else '' for l in m.split('\n'))

# ---------------------------------------------------------------- consultas M
M = {}

M['Archivos'] = '''
let
    // Todos los archivos de Excel dentro de la carpeta de datos (parámetro RutaDatos)
    Origen = Folder.Files(RutaDatos),
    Validos = Table.SelectRows(Origen, each not Text.StartsWith([Name], "~$")
        and List.Contains({".xlsx", ".xls"}, Text.Lower([Extension]))
        and [Attributes]?[Hidden]? <> true),
    // Carpeta relativa en minúsculas, por ejemplo "walmart\\sell out"
    ConCarpeta = Table.AddColumn(Validos, "Carpeta",
        each Text.Trim(Text.Replace(Text.Lower([Folder Path]), Text.Lower(RutaDatos), ""), "\\"), type text),
    Columnas = Table.SelectColumns(ConCarpeta, {"Content", "Name", "Carpeta"})
in
    Columnas
'''

M['fnFechaMDA'] = '''
// Convierte "mm-dd-aaaa" o "mm/dd/aaaa" (formato de Retail Link) en fecha, sin depender de la configuración regional
(valor as any) as nullable date =>
    if valor = null then null
    else if Value.Is(valor, type date) then valor
    else if Value.Is(valor, type datetime) then Date.From(valor)
    else
        let
            Texto = Text.Trim(Text.From(valor)),
            Partes = Text.SplitAny(Texto, "-/")
        in
            if Texto = "" then null
            else #date(Number.From(Partes{2}), Number.From(Partes{0}), Number.From(Partes{1}))
'''

M['fnFechaAMD'] = '''
// Convierte "aaaa/mm/dd" (columna Daily de Retail Link) en fecha
(valor as any) as nullable date =>
    if valor = null then null
    else if Value.Is(valor, type date) then valor
    else if Value.Is(valor, type datetime) then Date.From(valor)
    else
        let
            Texto = Text.Trim(Text.From(valor)),
            Partes = Text.SplitAny(Texto, "-/")
        in
            if Texto = "" then null
            else #date(Number.From(Partes{0}), Number.From(Partes{1}), Number.From(Partes{2}))
'''

M['fnNumero'] = '''
// Convierte números que vienen como texto con punto decimal ("18635.76") sin depender de la configuración regional
(valor as any) as nullable number =>
    if valor = null then null
    else if Value.Is(valor, type number) then valor
    else
        let
            Texto = Text.Trim(Text.From(valor))
        in
            if Texto = "" then null else Number.FromText(Text.Remove(Texto, ","), "en-US")
'''

M['fnRetailLink'] = '''
// Lee un archivo de Retail Link tal como se descarga.
// Devuelve el nombre del reporte, la fecha y hora de la solicitud, el rango de fechas consultado y la tabla de datos.
(contenido as binary) as record =>
let
    Libro = Excel.Workbook(contenido, null, true),
    // Primera hoja del libro (algunos archivos no traen la columna Kind en la lista de hojas)
    Hojas = if Table.HasColumns(Libro, "Kind") then Table.SelectRows(Libro, each [Kind] = "Sheet") else Libro,
    Hoja = Hojas{0}[Data],
    // Solo las primeras filas: ahí están las opciones y los encabezados (no se recorre todo el archivo)
    Filas = Table.ToRows(Table.FirstN(Hoja, 200)),
    // La fila de encabezados es la primera con 5 o más celdas llenas; antes vienen las opciones del reporte
    PosEncabezado = List.PositionOf(List.Transform(Filas, each List.Count(List.RemoveNulls(_)) >= 5), true),
    TextosPrevios = List.Transform(List.RemoveNulls(List.Combine(List.FirstN(Filas, PosEncabezado))), Text.From),
    Reporte = Text.Trim(TextosPrevios{0}),
    // "Requested 114402242: (MX)  2026 09 30, 16:42"
    TextoSolicitud = List.First(List.Select(TextosPrevios, each Text.Contains(_, "Requested")), null),
    Solicitado =
        if TextoSolicitud = null then null
        else
            let
                Resto = Text.Trim(Text.AfterDelimiter(TextoSolicitud, ")")),
                F = List.Select(Text.Split(Text.BeforeDelimiter(Resto, ","), " "), each _ <> ""),
                H = Text.Split(Text.Trim(Text.AfterDelimiter(Resto, ",")), ":")
            in
                #datetime(Number.From(F{0}), Number.From(F{1}), Number.From(F{2}), Number.From(H{0}), Number.From(H{1}), 0),
    // "... Time Range 1 Is Between  09-22-2026 and 09-29-2026 And"
    TextoRango = List.First(List.Select(TextosPrevios, each Text.Contains(_, "Between")), null),
    Rango = if TextoRango = null then null else Text.Trim(Text.BetweenDelimiters(TextoRango, "Between", " And")),
    Desde = if Rango = null then null else fnFechaMDA(Text.BeforeDelimiter(Rango, " and ")),
    Hasta = if Rango = null then null else fnFechaMDA(Text.AfterDelimiter(Rango, " and ")),
    Datos = Table.PromoteHeaders(Table.Skip(Hoja, PosEncabezado), [PromoteAllScalars = true])
in
    [Reporte = Reporte, Solicitado = Solicitado, Desde = Desde, Hasta = Hasta, Datos = Datos]
'''

M['fnAmazon'] = '''
// Lee un archivo de Amazon Vendor Central tal como se descarga.
// La primera fila trae el rango de fechas ("Rango de visualización=[01/08/26 - 31/08/26]"); la segunda, los encabezados.
(contenido as binary) as record =>
let
    Libro = Excel.Workbook(contenido, null, true),
    // Primera hoja del libro (algunos archivos no traen la columna Kind en la lista de hojas)
    Hojas = if Table.HasColumns(Libro, "Kind") then Table.SelectRows(Libro, each [Kind] = "Sheet") else Libro,
    Hoja = Hojas{0}[Data],
    Meta = Text.Combine(List.Transform(List.RemoveNulls(Record.FieldValues(Hoja{0})), Text.From), "|"),
    FechaDMA = (t as text) as date =>
        let
            P = Text.Split(Text.Trim(t), "/"),
            Anio = Number.From(P{2})
        in
            #date(if Anio < 100 then 2000 + Anio else Anio, Number.From(P{1}), Number.From(P{0})),
    Rango = Text.AfterDelimiter(Text.BeforeDelimiter(Text.AfterDelimiter(Meta, "Rango de visualizaci"), "]"), "["),
    Desde = FechaDMA(Text.BeforeDelimiter(Rango, " - ")),
    Hasta = FechaDMA(Text.AfterDelimiter(Rango, " - ")),
    Actualizado = try FechaDMA(Text.BeforeDelimiter(Text.AfterDelimiter(Meta, "Informe actualizado=["), "]")) otherwise null,
    Datos = Table.PromoteHeaders(Table.Skip(Hoja, 1), [PromoteAllScalars = true])
in
    [Desde = Desde, Hasta = Hasta, Actualizado = Actualizado, Datos = Datos]
'''

M['Maestro'] = '''
let
    // Maestro_Wellpro.xlsx, dentro de la carpeta Maestros de RutaDatos
    Archivo = Table.SelectRows(Archivos, each [Carpeta] = "maestros" and Text.StartsWith(Text.Lower([Name]), "maestro_wellpro")),
    Libro = Excel.Workbook(Archivo{0}[Content], null, true)
in
    Libro
'''

M['fnTablaMaestro'] = '''
// Devuelve una tabla del maestro por su nombre (por ejemplo "tProductos").
// Si el libro no la muestra como tabla, usa la hoja del mismo contenido (por ejemplo "Productos").
(tabla as text, hoja as text) as table =>
let
    PorTabla = Table.SelectRows(Maestro, each [Name] = tabla),
    PorHoja = Table.SelectRows(Maestro, each [Name] = hoja)
in
    if Table.RowCount(PorTabla) > 0 then PorTabla{0}[Data]
    else Table.PromoteHeaders(PorHoja{0}[Data], [PromoteAllScalars = true])
'''

M['Productos'] = '''
let
    Origen = fnTablaMaestro("tProductos", "Productos"),
    ComoTexto = (v) => if v = null then null else Text.Trim(Text.From(v)),
    Texto = Table.TransformColumns(Origen, {
        {"Codigo_ERP", ComoTexto, type nullable text}, {"EAN", ComoTexto, type nullable text},
        {"ASIN", ComoTexto, type nullable text}, {"Item_Walmart", ComoTexto, type nullable text},
        {"Producto", ComoTexto, type nullable text}, {"Familia", ComoTexto, type nullable text},
        {"Marca", ComoTexto, type nullable text}, {"Activo", ComoTexto, type nullable text}, {"Estado", ComoTexto, type nullable text}}),
    Numeros = Table.TransformColumnTypes(Texto, {{"Lead_time_meses", type number}, {"Stock_seguridad", type number}}),
    ConCodigo = Table.SelectRows(Numeros, each [Codigo_ERP] <> null),
    Unicos = Table.Distinct(ConCodigo, {"Codigo_ERP"}),
    Columnas = Table.SelectColumns(Unicos, {"Codigo_ERP", "Producto", "Familia", "Marca", "EAN", "ASIN", "Item_Walmart", "Lead_time_meses", "Stock_seguridad", "Activo", "Estado"})
in
    Columnas
'''

M['Equivalencias'] = '''
let
    Origen = fnTablaMaestro("tEquivalencias", "Equivalencias"),
    ComoTexto = (v) => if v = null then null else Text.Trim(Text.From(v)),
    Texto = Table.TransformColumns(Origen, {
        {"Cadena", ComoTexto, type nullable text}, {"Codigo_en_cadena", ComoTexto, type nullable text},
        {"Tipo_codigo", ComoTexto, type nullable text}, {"Codigo_ERP", ComoTexto, type nullable text}}),
    Columnas = Table.SelectColumns(Texto, {"Cadena", "Codigo_en_cadena", "Tipo_codigo", "Codigo_ERP"})
in
    Columnas
'''

M['WM_SellOut_Archivos'] = '''
let
    Lista = Table.SelectRows(Archivos, each [Carpeta] = "walmart\\sell out"),
    Leidos = Table.AddColumn(Lista, "R", each fnRetailLink([Content])),
    ConSolicitud = Table.AddColumn(Leidos, "Solicitado", each [R][Solicitado], type nullable datetime),
    // Días que cubre cada archivo: el rango de Pos Date del encabezado (no hace falta leer los datos).
    // Solo si el archivo no trae el rango, se toman de la columna Daily.
    ConDias = Table.AddColumn(ConSolicitud, "Dias", each
        let d = [R][Desde], h = [R][Hasta] in
            if d <> null and h <> null and h >= d then List.Dates(d, Duration.Days(h - d) + 1, #duration(1, 0, 0, 0))
            else if Table.HasColumns([R][Datos], "Daily")
            then List.Distinct(List.RemoveNulls(List.Transform([R][Datos][Daily], fnFechaAMD)))
            else {}, type list),
    // Cada día se toma de UN solo archivo: el de la solicitud más reciente (si empatan, el último por nombre).
    // Así, bajar dos veces el mismo día, o el mes completo encima de los diarios, nunca duplica.
    Pares = Table.SelectRows(Table.ExpandListColumn(Table.SelectColumns(ConDias, {"Name", "Solicitado", "Dias"}), "Dias"), each [Dias] <> null),
    PorDia = Table.Buffer(Table.Group(Pares, {"Dias"}, {{"Elegido", each Table.First(Table.Sort(_, {{"Solicitado", Order.Descending}, {"Name", Order.Descending}}))[Name], type text}})),
    ConUsados = Table.AddColumn(ConDias, "Dias_usados", (a) => Table.SelectRows(PorDia, each [Elegido] = a[Name])[Dias], type list),
    ConUso = Table.AddColumn(ConUsados, "Usado", each
        let n = List.Count([Dias]), u = List.Count([Dias_usados]) in
            if n = 0 then "No: no trae datos"
            else if u = n then "Sí"
            else if u = 0 then "No: sus días están en un archivo más reciente"
            else "Parcial: usa " & Text.From(u) & " de " & Text.From(n) & " días", type text),
    ConRango = Table.AddColumn(Table.AddColumn(ConUso,
        "Desde", each if List.IsEmpty([Dias]) then [R][Desde] else List.Min([Dias]), type nullable date),
        "Hasta", each if List.IsEmpty([Dias]) then [R][Hasta] else List.Max([Dias]), type nullable date)
in
    ConRango
'''

M['WM_SellOut_Filas'] = '''
let
    Usados = Table.SelectRows(WM_SellOut_Archivos, each not List.IsEmpty([Dias_usados])),
    // De cada archivo, solo los días que le tocan
    Filas = Table.Combine(List.Transform(Table.ToRecords(Usados), (a) =>
        let
            Dias = List.Buffer(a[Dias_usados]),
            Columnas = Table.SelectColumns(a[R][Datos], {"Daily", "Item Nbr", "Store Nbr", "Vendor Stk Nbr", "Signing Desc",
                "Sales Description", "POS Qty", "POS Sales", "POS Cost"}, MissingField.UseNull),
            Datos = Table.TransformColumns(Columnas, {{"Daily", fnFechaAMD, type nullable date}})
        in
            Table.SelectRows(Datos, each List.Contains(Dias, [Daily])))),
    Validas = Table.SelectRows(Filas, each [Item Nbr] <> null and [Daily] <> null),
    Tipado = Table.TransformColumns(Validas, {
        {"Item Nbr", each Text.From(Int64.From(_)), type text},
        {"Store Nbr", each Int64.From(_), Int64.Type},
        {"Vendor Stk Nbr", each if _ = null then null else Text.Trim(Text.From(_)), type nullable text},
        {"Signing Desc", each Text.From(_), type text},
        {"Sales Description", each Text.From(_), type text},
        {"POS Qty", fnNumero, type number},
        {"POS Sales", fnNumero, type number},
        {"POS Cost", fnNumero, type number}})
in
    Tipado
'''

M['WM_SellOut'] = '''
let
    // Cada día ya viene de un solo archivo (ver WM_SellOut_Archivos)
    ConMovimiento = Table.SelectRows(WM_SellOut_Filas, each [POS Qty] <> 0 or [POS Sales] <> 0),
    // Homologación: número de artículo de Walmart -> código del ERP (hoja Equivalencias del maestro).
    // Si no está, se usa Vendor Stk Nbr cuando coincide con un código del ERP.
    Eq = Table.Distinct(Table.SelectRows(Equivalencias, each [Cadena] = "Walmart" and [Tipo_codigo] = "Item Nbr"), {"Codigo_en_cadena"}),
    Codigos = List.Buffer(Productos[Codigo_ERP]),
    Unido = Table.ExpandTableColumn(Table.NestedJoin(ConMovimiento, {"Item Nbr"}, Eq, {"Codigo_en_cadena"}, "Eq", JoinKind.LeftOuter), "Eq", {"Codigo_ERP"}, {"Codigo_eq"}),
    ConCodigo = Table.AddColumn(Unido, "Codigo_ERP",
        each if [Codigo_eq] <> null then [Codigo_eq] else if List.Contains(Codigos, [Vendor Stk Nbr]) then [Vendor Stk Nbr] else null, type nullable text),
    // Se guarda en memoria: armar la tabla columna por columna volvería a leer todos los archivos por cada columna
    B = Table.Buffer(Table.SelectColumns(ConCodigo, {"Daily", "Codigo_ERP", "Item Nbr", "Signing Desc", "Store Nbr", "Sales Description", "POS Qty", "POS Sales", "POS Cost"})),
    Salida = Table.FromColumns({
        B[Daily], B[Daily], List.Repeat({"Walmart"}, Table.RowCount(B)), B[Codigo_ERP],
        B[Item Nbr], B[Signing Desc], B[Store Nbr], B[Sales Description],
        B[POS Qty], B[POS Sales], B[POS Cost]},
        type table [Fecha = date, Datos_hasta = date, Cadena = text, Codigo_ERP = nullable text, Codigo_cadena = text,
            Descripcion_cadena = text, Tienda_Nbr = nullable Int64.Type, Tipo_venta = text, Piezas = number, Monto = number, Costo = nullable number])
in
    Salida
'''

M['AMZ_SellOut_Archivos'] = '''
let
    Lista = Table.SelectRows(Archivos, each [Carpeta] = "amazon\\sell out"),
    Leidos = Table.AddColumn(Lista, "R", each fnAmazon([Content])),
    ConMeta = Table.AddColumn(Table.AddColumn(Table.AddColumn(Leidos,
        "Desde", each [R][Desde], type date),
        // Último día con datos: el fin del rango, o la fecha de actualización de Amazon si es anterior
        "Hasta", each if [R][Actualizado] <> null and [R][Actualizado] < [R][Hasta] then [R][Actualizado] else [R][Hasta], type date),
        "Actualizado", each [R][Actualizado], type nullable date),
    ConMes = Table.AddColumn(ConMeta, "Mes", each Date.StartOfMonth([Desde]), type date),
    // Solo sirven archivos de un solo mes. Por cada mes se usa el que llega más lejos; si empatan, el actualizado más reciente.
    DeUnMes = Table.SelectRows(ConMes, each Date.StartOfMonth([Hasta]) = [Mes]),
    Elegidos = Table.Group(DeUnMes, {"Mes"}, {{"Nombre", each Table.First(Table.Sort(_, {{"Hasta", Order.Descending}, {"Actualizado", Order.Descending}, {"Name", Order.Descending}}))[Name], type text}}),
    ConUso = Table.AddColumn(ConMes, "Usado", each if List.Contains(Elegidos[Nombre], [Name]) then "Sí" else if Date.StartOfMonth([Hasta]) <> [Mes] then "No: abarca más de un mes" else "No: hay uno más reciente del mismo mes", type text)
in
    ConUso
'''

M['AMZ_SellOut'] = '''
let
    Usados = Table.SelectRows(AMZ_SellOut_Archivos, each [Usado] = "Sí"),
    Filas = Table.Combine(List.Transform(Table.ToRecords(Usados),
        (a) => Table.AddColumn(Table.AddColumn(a[R][Datos], "Mes", each a[Mes], type date), "Datos_hasta", each a[Hasta], type date))),
    Validas = Table.SelectRows(Filas, each [ASIN] <> null and Text.Trim(Text.From([ASIN])) <> ""),
    Tipado = Table.TransformColumns(Validas, {
        {"ASIN", each Text.Trim(Text.From(_)), type text},
        {"Título del Producto", each Text.From(_), type text},
        {"Unidades pedidas", fnNumero, type number},
        {"Ganancia por pedidos", fnNumero, type number}}),
    // Homologación: ASIN -> código del ERP (hoja Equivalencias del maestro)
    Eq = Table.Distinct(Table.SelectRows(Equivalencias, each [Cadena] = "Amazon"), {"Codigo_en_cadena"}),
    Unido = Table.ExpandTableColumn(Table.NestedJoin(Tipado, {"ASIN"}, Eq, {"Codigo_en_cadena"}, "Eq", JoinKind.LeftOuter), "Eq", {"Codigo_ERP"}),
    // Se guarda en memoria: armar la tabla columna por columna volvería a leer todos los archivos por cada columna
    UnidoB = Table.Buffer(Unido),
    N = Table.RowCount(UnidoB),
    Salida = Table.FromColumns({
        UnidoB[Mes], UnidoB[Datos_hasta], List.Repeat({"Amazon"}, N), UnidoB[Codigo_ERP],
        UnidoB[ASIN], UnidoB[#"Título del Producto"], List.Repeat({null}, N), List.Repeat({"Regular"}, N),
        UnidoB[Unidades pedidas], UnidoB[Ganancia por pedidos], List.Repeat({null}, N)},
        type table [Fecha = date, Datos_hasta = date, Cadena = text, Codigo_ERP = nullable text, Codigo_cadena = text,
            Descripcion_cadena = text, Tienda_Nbr = nullable Int64.Type, Tipo_venta = text, Piezas = number, Monto = number, Costo = nullable number])
in
    Salida
'''

M['WM_Inventario_Archivos'] = '''
let
    Lista = Table.SelectRows(Archivos, each [Carpeta] = "walmart\\inventario"),
    Leidos = Table.AddColumn(Lista, "R", each fnRetailLink([Content])),
    ConSolicitud = Table.AddColumn(Leidos, "Solicitado", each [R][Solicitado], type nullable datetime),
    // La foto corresponde al día consultado (Pos Date); si no viene, al día anterior a la solicitud
    ConFecha = Table.AddColumn(ConSolicitud, "Fecha", each
        if [R][Hasta] <> null then [R][Hasta]
        else if [Solicitado] = null then null
        else Date.AddDays(Date.From([Solicitado]), -1), type nullable date),
    // Una foto por día: la de la solicitud más reciente (si empatan, la última por nombre)
    PorDia = Table.Buffer(Table.Group(Table.SelectRows(ConFecha, each [Fecha] <> null), {"Fecha"},
        {{"Elegido", each Table.First(Table.Sort(_, {{"Solicitado", Order.Descending}, {"Name", Order.Descending}}))[Name], type text}})),
    Elegidos = List.Buffer(PorDia[Elegido]),
    // De cada mes solo cuenta la última foto: la más reciente es el inventario actual y las de cierre de mes, el historial
    UltimasDelMes = List.Buffer(Table.Group(Table.AddColumn(PorDia, "Mes", each Date.StartOfMonth([Fecha])), {"Mes"},
        {{"Ultima", each List.Max([Fecha]), type date}})[Ultima]),
    ConUso = Table.AddColumn(ConFecha, "Usado", each
        if [Fecha] = null then "No: no se pudo leer la fecha"
        else if not List.Contains(Elegidos, [Name]) then "No: hay uno más reciente del mismo día"
        else if not List.Contains(UltimasDelMes, [Fecha]) then "No: no es la última foto del mes"
        else "Sí", type text)
in
    ConUso
'''

M['WM_Inventario_Filas'] = '''
let
    Usados = Table.SelectRows(WM_Inventario_Archivos, each [Usado] = "Sí"),
    Filas = Table.Combine(List.Transform(Table.ToRecords(Usados),
        (a) => Table.AddColumn(a[R][Datos], "Fecha", each a[Fecha], type date))),
    Validas = Table.SelectRows(Filas, each [Item Nbr] <> null and [Store Nbr] <> null),
    Tipado = Table.TransformColumns(Validas, {
        {"Item Nbr", each Text.From(Int64.From(_)), type text},
        {"Store Nbr", each Int64.From(_), Int64.Type},
        {"Signing Desc", each Text.From(_), type text},
        {"Store Name", each Text.From(_), type text},
        {"City", each Text.From(_), type text},
        {"Curr Str On Hand Qty", fnNumero, type number},
        {"Curr Str In Transit Qty", fnNumero, type number},
        {"Curr Str In Whse Qty", fnNumero, type number},
        {"Curr Str On Order Qty", fnNumero, type number}})
in
    Tipado
'''

M['WM_Inventario'] = '''
let
    // Cada día ya viene de un solo archivo (ver WM_Inventario_Archivos)
    Eq = Table.Distinct(Table.SelectRows(Equivalencias, each [Cadena] = "Walmart" and [Tipo_codigo] = "Item Nbr"), {"Codigo_en_cadena"}),
    Unido = Table.ExpandTableColumn(Table.NestedJoin(WM_Inventario_Filas, {"Item Nbr"}, Eq, {"Codigo_en_cadena"}, "Eq", JoinKind.LeftOuter), "Eq", {"Codigo_ERP"}),
    // Se guarda en memoria: armar la tabla columna por columna volvería a leer todos los archivos por cada columna
    UnidoB = Table.Buffer(Unido),
    N = Table.RowCount(UnidoB),
    Salida = Table.FromColumns({
        UnidoB[Fecha], List.Repeat({"Walmart"}, N), UnidoB[Codigo_ERP], UnidoB[Item Nbr], UnidoB[Store Nbr],
        UnidoB[Curr Str On Hand Qty], UnidoB[Curr Str In Transit Qty], UnidoB[Curr Str In Whse Qty], UnidoB[Curr Str On Order Qty],
        List.Repeat({null}, N), List.Repeat({null}, N)},
        type table [Fecha = date, Cadena = text, Codigo_ERP = nullable text, Codigo_cadena = text, Tienda_Nbr = nullable Int64.Type,
            Piezas_disponibles = nullable number, Piezas_transito = nullable number, Piezas_CEDIS = nullable number,
            Piezas_en_pedido = nullable number, Piezas_no_aptas = nullable number, Monto_disponible = nullable number])
in
    Salida
'''

M['AMZ_Inventario_Archivos'] = '''
let
    // Carpeta exacta (las subcarpetas, como Respaldo, no se leen)
    Lista = Table.SelectRows(Archivos, each List.Contains({"amazon\\inventario", "amazon\\inventarios"}, [Carpeta])),
    Leidos = Table.AddColumn(Lista, "R", each fnAmazon([Content])),
    ConMeta = Table.AddColumn(Table.AddColumn(Table.AddColumn(Leidos,
        "Desde", each [R][Desde], type date),
        "Hasta", each [R][Hasta], type date),
        "Actualizado", each [R][Actualizado], type nullable date),
    // Una foto por día: la actualizada más recientemente (si empatan, la última por nombre)
    PorDia = Table.Buffer(Table.Group(ConMeta, {"Hasta"},
        {{"Nombre", each Table.First(Table.Sort(_, {{"Actualizado", Order.Descending}, {"Name", Order.Descending}}))[Name], type text}})),
    Elegidos = List.Buffer(PorDia[Nombre]),
    // De cada mes solo cuenta la última foto
    UltimasDelMes = List.Buffer(Table.Group(Table.AddColumn(PorDia, "Mes", each Date.StartOfMonth([Hasta])), {"Mes"},
        {{"Ultima", each List.Max([Hasta]), type date}})[Ultima]),
    ConUso = Table.AddColumn(ConMeta, "Usado", each
        if not List.Contains(Elegidos, [Name]) then "No: hay uno más reciente del mismo día"
        else if not List.Contains(UltimasDelMes, [Hasta]) then "No: no es la última foto del mes"
        else "Sí", type text)
in
    ConUso
'''

M['AMZ_Inventario'] = '''
let
    Usados = Table.SelectRows(AMZ_Inventario_Archivos, each [Usado] = "Sí"),
    Filas = Table.Combine(List.Transform(Table.ToRecords(Usados),
        (a) => Table.AddColumn(a[R][Datos], "Fecha", each a[Hasta], type date))),
    Validas = Table.SelectRows(Filas, each [ASIN] <> null and Text.Trim(Text.From([ASIN])) <> ""),
    Tipado = Table.TransformColumns(Validas, {
        {"ASIN", each Text.Trim(Text.From(_)), type text},
        {"Unidades aptas para la venta disponibles", fnNumero, type number},
        {"Inventario apto para la venta disponible", fnNumero, type number},
        {"Unidades no aptas para la venta disponibles", fnNumero, type number},
        {"Cantidad de órdenes de compra abiertas", fnNumero, type number}}),
    Eq = Table.Distinct(Table.SelectRows(Equivalencias, each [Cadena] = "Amazon"), {"Codigo_en_cadena"}),
    Unido = Table.ExpandTableColumn(Table.NestedJoin(Tipado, {"ASIN"}, Eq, {"Codigo_en_cadena"}, "Eq", JoinKind.LeftOuter), "Eq", {"Codigo_ERP"}),
    // Se guarda en memoria: armar la tabla columna por columna volvería a leer todos los archivos por cada columna
    UnidoB = Table.Buffer(Unido),
    N = Table.RowCount(UnidoB),
    Salida = Table.FromColumns({
        UnidoB[Fecha], List.Repeat({"Amazon"}, N), UnidoB[Codigo_ERP], UnidoB[ASIN], List.Repeat({null}, N),
        UnidoB[Unidades aptas para la venta disponibles], List.Repeat({null}, N), List.Repeat({null}, N),
        UnidoB[#"Cantidad de órdenes de compra abiertas"], UnidoB[Unidades no aptas para la venta disponibles],
        UnidoB[Inventario apto para la venta disponible]},
        type table [Fecha = date, Cadena = text, Codigo_ERP = nullable text, Codigo_cadena = text, Tienda_Nbr = nullable Int64.Type,
            Piezas_disponibles = nullable number, Piezas_transito = nullable number, Piezas_CEDIS = nullable number,
            Piezas_en_pedido = nullable number, Piezas_no_aptas = nullable number, Monto_disponible = nullable number])
in
    Salida
'''

M['WM_FillRate_Archivos'] = '''
let
    Lista = Table.SelectRows(Archivos, each [Carpeta] = "walmart\\fill rate"),
    Leidos = Table.AddColumn(Lista, "R", each fnRetailLink([Content])),
    ConSolicitud = Table.AddColumn(Leidos, "Solicitado", each [R][Solicitado], type nullable datetime)
in
    ConSolicitud
'''

M['WM_FillRate_Lineas'] = '''
let
    Filas = Table.Combine(List.Transform(Table.ToRecords(WM_FillRate_Archivos),
        (a) => Table.AddColumn(Table.AddColumn(a[R][Datos], "Solicitado", each a[Solicitado], type nullable datetime), "Archivo", each a[Name], type text))),
    Validas = Table.SelectRows(Filas, each [PO Number] <> null and [Item Nbr] <> null),
    Tipado = Table.TransformColumns(Validas, {
        {"PO Number", each Text.From(Int64.From(_)), type text},
        {"Item Nbr", each Text.From(Int64.From(_)), type text},
        {"PO Order Date", fnFechaMDA, type date},
        {"PO Ship Date", fnFechaMDA, type nullable date},
        {"PO Cancel Date", fnFechaMDA, type nullable date},
        {"Unit Cost", fnNumero, type nullable number},
        {"Hist Eaches Str Ordered", fnNumero, type number},
        {"Hist Eaches Str Received", fnNumero, type number},
        {"Hist Eaches Whse Ordered", fnNumero, type number},
        {"Hist Eaches Whse Received", fnNumero, type number}}),
    // Una orden se actualiza cuando llega la mercancía: cada línea (orden + artículo) se toma de la descarga más reciente
    Ordenado = Table.Buffer(Table.Sort(Tipado, {{"Solicitado", Order.Descending}, {"Archivo", Order.Descending}})),
    SinRepetidos = Table.Distinct(Ordenado, {"PO Number", "Item Nbr"})
in
    SinRepetidos
'''

M['WM_FillRate'] = '''
let
    Eq = Table.Distinct(Table.SelectRows(Equivalencias, each [Cadena] = "Walmart" and [Tipo_codigo] = "Item Nbr"), {"Codigo_en_cadena"}),
    Unido = Table.ExpandTableColumn(Table.NestedJoin(WM_FillRate_Lineas, {"Item Nbr"}, Eq, {"Codigo_en_cadena"}, "Eq", JoinKind.LeftOuter), "Eq", {"Codigo_ERP"}),
    ConPiezas = Table.AddColumn(Table.AddColumn(Unido,
        "Ordenadas", each List.Sum({[Hist Eaches Str Ordered], [Hist Eaches Whse Ordered]}), type number),
        "Recibidas", each List.Sum({[Hist Eaches Str Received], [Hist Eaches Whse Received]}), type number),
    // Se guarda en memoria: armar la tabla columna por columna volvería a leer todos los archivos por cada columna
    ConPiezasB = Table.Buffer(ConPiezas),
    N = Table.RowCount(ConPiezasB),
    Salida = Table.FromColumns({
        List.Repeat({"Walmart"}, N), ConPiezasB[PO Number], ConPiezasB[Codigo_ERP], ConPiezasB[Item Nbr],
        ConPiezasB[PO Order Date], ConPiezasB[PO Ship Date], ConPiezasB[PO Cancel Date],
        ConPiezasB[Ordenadas], ConPiezasB[Recibidas], ConPiezasB[Unit Cost]},
        type table [Cadena = text, Orden = text, Codigo_ERP = nullable text, Codigo_cadena = text,
            Fecha_orden = date, Fecha_envio = nullable date, Fecha_cancelacion = nullable date,
            Piezas_ordenadas = number, Piezas_recibidas = number, Costo_unitario = nullable number])
in
    Salida
'''

M['WM_Recship_Archivos'] = '''
let
    Lista = Table.SelectRows(Archivos, each [Carpeta] = "walmart\\forecast"),
    Leidos = Table.AddColumn(Lista, "R", each fnRetailLink([Content])),
    ConSolicitud = Table.AddColumn(Leidos, "Solicitado", each [R][Solicitado], type nullable datetime),
    Elegido = Table.First(Table.Sort(ConSolicitud, {{"Solicitado", Order.Descending}, {"Name", Order.Descending}}))[Name],
    ConUso = Table.AddColumn(ConSolicitud, "Usado", each if [Name] = Elegido then "Sí" else "No: hay uno más reciente", type text)
in
    ConUso
'''

M['WM_Recship'] = '''
let
    // Solo cuenta el pronóstico más reciente
    Ultimo = Table.First(Table.SelectRows(WM_Recship_Archivos, each [Usado] = "Sí")),
    Datos = Ultimo[R][Datos],
    Validas = Table.SelectRows(Datos, each [Item Nbr] <> null and [Units] <> null),
    Tipado = Table.TransformColumns(Validas, {
        {"Item Nbr", each Text.From(Int64.From(_)), type text},
        {"Whse Name", each Text.From(_), type text},
        {"Plan Create Date", fnFechaMDA, type nullable date},
        {"Plan Order Date", fnFechaMDA, type date},
        {"Plan Recieve Date", fnFechaMDA, type nullable date},
        {"Units", fnNumero, type number},
        {"VNPK Qty", fnNumero, type number},
        {"VNPK Cost", fnNumero, type number}}),
    Eq = Table.Distinct(Table.SelectRows(Equivalencias, each [Cadena] = "Walmart" and [Tipo_codigo] = "Item Nbr"), {"Codigo_en_cadena"}),
    Unido = Table.ExpandTableColumn(Table.NestedJoin(Tipado, {"Item Nbr"}, Eq, {"Codigo_en_cadena"}, "Eq", JoinKind.LeftOuter), "Eq", {"Codigo_ERP"}),
    // Costo por pieza = costo de la caja / piezas por caja (Retail Link lo da en pesos)
    ConCosto = Table.AddColumn(Unido, "Costo_pieza", each if [VNPK Qty] = null or [VNPK Qty] = 0 then null else [VNPK Cost] / [VNPK Qty], type nullable number),
    // Se guarda en memoria: armar la tabla columna por columna volvería a leer todos los archivos por cada columna
    ConCostoB = Table.Buffer(ConCosto),
    N = Table.RowCount(ConCostoB),
    Salida = Table.FromColumns({
        List.Repeat({"Walmart"}, N), ConCostoB[Codigo_ERP], ConCostoB[Item Nbr], ConCostoB[Whse Name],
        ConCostoB[Plan Create Date], ConCostoB[Plan Order Date], ConCostoB[Plan Recieve Date],
        ConCostoB[Units], ConCostoB[Costo_pieza], List.Transform(List.Zip({ConCostoB[Units], ConCostoB[Costo_pieza]}), each if _{1} = null then null else _{0} * _{1})},
        type table [Cadena = text, Codigo_ERP = nullable text, Codigo_cadena = text, CEDIS = text,
            Fecha_creacion = nullable date, Fecha_pedido = date, Fecha_recepcion = nullable date,
            Piezas = number, Costo_pieza = nullable number, Monto = nullable number])
in
    Salida
'''

PARAM_RUTA = r'C:\Users\mpalacios\OneDrive - VISION MEDICA S.A\Documentos\Proyecto-Centroamerica-claude-confident-dijkstra-apgh2d\Nueva versión' + '\\'

# ---------------------------------------------------------------- particiones de tablas
P = {}
P['Calendario'] = '''
let
    Inicio = #date(2024, 1, 1),
    Fin = Date.EndOfYear(Date.AddMonths(DateTime.Date(DateTime.LocalNow()), 6)),
    Fechas = List.Dates(Inicio, Duration.Days(Fin - Inicio) + 1, #duration(1, 0, 0, 0)),
    Tabla = Table.FromList(Fechas, Splitter.SplitByNothing(), type table [Fecha = date]),
    Anio = Table.AddColumn(Tabla, "Año", each Date.Year([Fecha]), Int64.Type),
    NumMes = Table.AddColumn(Anio, "Num_mes", each Date.Month([Fecha]), Int64.Type),
    Mes = Table.AddColumn(NumMes, "Mes", each Text.Proper(Date.MonthName([Fecha], "es-MX")), type text),
    AnioMes = Table.AddColumn(Mes, "Año_mes", each Date.ToText([Fecha], "yyyy-MM"), type text),
    InicioMes = Table.AddColumn(AnioMes, "Inicio_mes", each Date.StartOfMonth([Fecha]), type date),
    Trimestre = Table.AddColumn(InicioMes, "Trimestre", each "T" & Text.From(Date.QuarterOfYear([Fecha])), type text),
    // Etiqueta corta para los ejes, por ejemplo "Sep 2026"
    MesAnio = Table.AddColumn(Trimestre, "Mes_año", each
        {"Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"}{Date.Month([Fecha]) - 1}
        & " " & Text.From(Date.Year([Fecha])), type text)
in
    MesAnio
'''
P['dimCadena'] = '''
#table(type table [Cadena = text, Orden = Int64.Type], {{"Walmart", 1}, {"Amazon", 2}})
'''
P['dimProducto'] = '''
Productos
'''
P['dimTienda'] = '''
let
    // Las tiendas salen de las fotos de inventario, que son pocas y pequeñas. Así no se vuelve a leer todo el sell out.
    Filas = Table.SelectColumns(WM_Inventario_Filas, {"Store Nbr", "Store Name", "City"}),
    Unicas = Table.Distinct(Table.SelectRows(Filas, each [Store Nbr] <> null), {"Store Nbr"}),
    Renombrado = Table.RenameColumns(Unicas, {{"Store Nbr", "Tienda_Nbr"}, {"Store Name", "Tienda"}, {"City", "Ciudad"}}),
    Etiqueta = Table.AddColumn(Renombrado, "Tienda_etiqueta", each Text.From([Tienda_Nbr]) & " - " & [Tienda], type text)
in
    Etiqueta
'''
P['fSellOut'] = '''
Table.Combine({WM_SellOut, AMZ_SellOut})
'''
P['fInventarioCadena'] = '''
Table.Combine({WM_Inventario, AMZ_Inventario})
'''
P['fFillRate'] = '''
WM_FillRate
'''
P['fRecship'] = '''
WM_Recship
'''
P['Metas'] = '''
let
    Origen = fnTablaMaestro("tMetas", "Metas"),
    Tipado = Table.TransformColumns(Origen, {
        {"Mes", each Date.StartOfMonth(Date.From(_)), type date},
        {"Codigo_ERP", each if _ = null then null else Text.Trim(Text.From(_)), type nullable text},
        {"Producto", each Text.From(_), type text},
        {"Cliente_reporte", each Text.From(_), type text},
        {"Cantidad", each Number.From(_), type number},
        {"Precio", each Number.From(_), type number},
        {"Monto", each Number.From(_), type number}}),
    Columnas = Table.SelectColumns(Tipado, {"Mes", "Codigo_ERP", "Producto", "Cliente_reporte", "Cantidad", "Precio", "Monto"})
in
    Columnas
'''
P['ctlArchivos'] = '''
let
    // Qué archivos leyó el reporte, de qué fechas y si se usan. Los que dicen "No" pueden pasar a la subcarpeta Respaldo.
    DeWM = (fuente as text, t as table) as table =>
        Table.FromRecords(List.Transform(Table.ToRecords(t), (a) => [
            Fuente = fuente, Archivo = a[Name], Reporte = a[R][Reporte],
            Desde = if Record.HasFields(a, "Desde") then a[Desde] else if Record.HasFields(a, "Fecha") then a[Fecha] else a[R][Desde],
            Hasta = if Record.HasFields(a, "Hasta") then a[Hasta] else if Record.HasFields(a, "Fecha") then a[Fecha] else a[R][Hasta],
            Generado = a[Solicitado], Usado = a[Usado]])),
    DeAMZ = (fuente as text, t as table) as table =>
        Table.FromRecords(List.Transform(Table.ToRecords(t), (a) => [
            Fuente = fuente, Archivo = a[Name], Reporte = fuente, Desde = a[Desde], Hasta = a[Hasta],
            Generado = if a[Actualizado] = null then null else DateTime.From(a[Actualizado]),
            Usado = a[Usado]])),
    UsadosFR = List.Buffer(List.Distinct(WM_FillRate_Lineas[Archivo])),
    FillRate = Table.AddColumn(WM_FillRate_Archivos, "Usado", each
        if List.Contains(UsadosFR, [Name]) then "Sí" else "No: todas sus órdenes están en un archivo más reciente", type text),
    Todas = Table.Combine({
        DeWM("Walmart - Sell out", WM_SellOut_Archivos),
        DeWM("Walmart - Inventario", WM_Inventario_Archivos),
        DeWM("Walmart - Fill rate", FillRate),
        DeWM("Walmart - Forecast (Recship)", WM_Recship_Archivos),
        DeAMZ("Amazon - Sell out", AMZ_SellOut_Archivos),
        DeAMZ("Amazon - Inventario", AMZ_Inventario_Archivos)}),
    Tipado = Table.TransformColumnTypes(Todas, {{"Fuente", type text}, {"Archivo", type text}, {"Reporte", type text},
        {"Desde", type date}, {"Hasta", type date}, {"Generado", type datetime}, {"Usado", type text}})
in
    Tipado
'''
P['sMetrica'] = '''
#table(type table [Metrica = text, Orden = Int64.Type], {{"Monto", 1}, {"Piezas", 2}})
'''
P['_Medidas'] = '''
#table(type table [Columna = text], {})
'''

# ---------------------------------------------------------------- columnas por tabla
S, I, D, DT, B = 'string', 'int64', 'double', 'dateTime', 'boolean'
FMT_FECHA = 'dd/mm/yyyy'
COLS = {
 'Calendario': [('Fecha', DT, 'key'), ('Año', I, None), ('Num_mes', I, None), ('Mes', S, 'sortNum_mes'), ('Año_mes', S, None), ('Inicio_mes', DT, None), ('Trimestre', S, None), ('Mes_año', S, 'sortInicio_mes')],
 'dimCadena': [('Cadena', S, 'sortOrden'), ('Orden', I, 'hidden')],
 'sMetrica': [('Metrica', S, 'sortOrden'), ('Orden', I, 'hidden')],
 'dimProducto': [('Codigo_ERP', S, None), ('Producto', S, None), ('Familia', S, None), ('Marca', S, None), ('EAN', S, None), ('ASIN', S, None), ('Item_Walmart', S, None), ('Lead_time_meses', D, 'nosum'), ('Stock_seguridad', D, 'nosum'), ('Activo', S, None), ('Estado', S, None)],
 'dimTienda': [('Tienda_Nbr', I, 'nosum'), ('Tienda', S, None), ('Ciudad', S, None), ('Tienda_etiqueta', S, None)],
 'fSellOut': [('Fecha', DT, None), ('Datos_hasta', DT, None), ('Cadena', S, None), ('Codigo_ERP', S, None), ('Codigo_cadena', S, None), ('Descripcion_cadena', S, None), ('Tienda_Nbr', I, 'nosum'), ('Tipo_venta', S, None), ('Piezas', D, 'sum'), ('Monto', D, 'sum'), ('Costo', D, 'sum')],
 'fInventarioCadena': [('Fecha', DT, None), ('Cadena', S, None), ('Codigo_ERP', S, None), ('Codigo_cadena', S, None), ('Tienda_Nbr', I, 'nosum'), ('Piezas_disponibles', D, 'nosum'), ('Piezas_transito', D, 'nosum'), ('Piezas_CEDIS', D, 'nosum'), ('Piezas_en_pedido', D, 'nosum'), ('Piezas_no_aptas', D, 'nosum'), ('Monto_disponible', D, 'nosum')],
 'fFillRate': [('Cadena', S, None), ('Orden', S, None), ('Codigo_ERP', S, None), ('Codigo_cadena', S, None), ('Fecha_orden', DT, None), ('Fecha_envio', DT, None), ('Fecha_cancelacion', DT, None), ('Piezas_ordenadas', D, 'sum'), ('Piezas_recibidas', D, 'sum'), ('Costo_unitario', D, 'nosum')],
 'fRecship': [('Cadena', S, None), ('Codigo_ERP', S, None), ('Codigo_cadena', S, None), ('CEDIS', S, None), ('Fecha_creacion', DT, None), ('Fecha_pedido', DT, None), ('Fecha_recepcion', DT, None), ('Piezas', D, 'sum'), ('Costo_pieza', D, 'nosum'), ('Monto', D, 'sum')],
 'Metas': [('Mes', DT, None), ('Codigo_ERP', S, None), ('Producto', S, None), ('Cliente_reporte', S, None), ('Cantidad', D, 'sum'), ('Precio', D, 'nosum'), ('Monto', D, 'sum')],
 'ctlArchivos': [('Fuente', S, None), ('Archivo', S, None), ('Reporte', S, None), ('Desde', DT, None), ('Hasta', DT, None), ('Generado', DT, 'fechahora'), ('Usado', S, None)],
 '_Medidas': [('Columna', S, 'hidden')],
}
DESC_TABLA = {
 'Calendario': 'Calendario del reporte (desde enero de 2024).',
 'dimCadena': 'Cadenas con sell out: Walmart y Amazon.',
 'dimProducto': 'Productos del maestro (hoja Productos). La llave es el código del ERP.',
 'dimTienda': 'Tiendas de Walmart que aparecen en las fotos de inventario.',
 'fSellOut': 'Venta de las cadenas al consumidor. Walmart por día, tienda y artículo; Amazon por mes y ASIN (Fecha = primer día del mes; Datos_hasta = último día que cubre el archivo).',
 'fInventarioCadena': 'Fotos del inventario en las cadenas. Walmart por día, tienda y artículo; Amazon por día y ASIN.',
 'fFillRate': 'Órdenes de compra de Walmart: piezas ordenadas y recibidas (tienda + centro de distribución).',
 'fRecship': 'Pronóstico de pedidos de Walmart (Recship); solo el archivo más reciente.',
 'Metas': 'Metas mensuales de sell in por producto y cliente (hoja Metas del maestro).',
 'ctlArchivos': 'Control: archivos leídos por el reporte, sus fechas y si se usaron.',
 'sMetrica': 'Selector de la página Sell out: ver los gráficos en monto o en piezas. No se relaciona con otras tablas.',
 '_Medidas': 'Tabla para las medidas del reporte.',
}

def columna(tabla, nombre, tipo, extra):
    q = f"'{nombre}'" if any(c in nombre for c in ' ñáéíóú') else nombre
    out = [f'\tcolumn {q}', f'\t\tdataType: {tipo}']
    if tipo == DT:
        out.append(f'\t\tformatString: {"dd/mm/yyyy hh:nn" if extra == "fechahora" else FMT_FECHA}')
    if tipo == D and extra != 'nosum':
        out.append('\t\tformatString: #,0')
    if tipo == D and extra == 'nosum':
        out.append('\t\tformatString: #,0.##')
    if extra == 'key':
        out.append('\t\tisKey')
    if extra == 'hidden':
        out.append('\t\tisHidden')
    summ = 'sum' if extra == 'sum' else 'none'
    out.append(f'\t\tsummarizeBy: {summ}')
    out.append(f'\t\tsourceColumn: {nombre}')
    if extra and extra.startswith('sort'):
        out.append(f'\t\tsortByColumn: {extra[4:]}')
    if tipo == DT and extra != 'fechahora':
        out += ['', '\t\tannotation UnderlyingDateTimeDataType = Date']
    return '\n'.join(out)

# columnas calculadas (DAX): se recalculan en cada actualización con el último dato de sell out
CALC = {
 'Calendario': [
  ('Meses_atras', 'DATEDIFF ( Calendario[Inicio_mes], DATE ( YEAR ( MAX ( fSellOut[Datos_hasta] ) ), MONTH ( MAX ( fSellOut[Datos_hasta] ) ), 1 ), MONTH )',
   I, None, 'Meses entre este mes y el último mes con sell out: 0 = mes actual, 1 = mes anterior; negativo = meses futuros.'),
  ('Periodo', 'IF ( Calendario[Meses_atras] = 0, "Mes actual", Calendario[Mes_año] )',
   S, 'sortInicio_mes', 'Mes para los filtros: el último mes con sell out se llama "Mes actual", así el filtro guardado no se desactualiza.'),
 ],
}

def columna_calc(nombre, expr, tipo, extra, desc):
    q = f"'{nombre}'" if any(c in nombre for c in ' ñáéíóú') else nombre
    out = [f'\t/// {desc}', f'\tcolumn {q} = {expr}', f'\t\tdataType: {tipo}']
    if tipo == I:
        out.append('\t\tformatString: 0')
    out.append('\t\tsummarizeBy: none')
    if extra and extra.startswith('sort'):
        out.append(f'\t\tsortByColumn: {extra[4:]}')
    return '\n'.join(out)

# ---------------------------------------------------------------- medidas
MED = []
FORMATO_DINAMICO = {}
def med(nombre, expr, fmt, carpeta, desc, formato_dinamico=None):
    MED.append((nombre, expr, fmt, carpeta, desc))
    if formato_dinamico:
        FORMATO_DINAMICO[nombre] = formato_dinamico

med('Sell out piezas', 'SUM ( fSellOut[Piezas] )', '#,0', '1. Sell out', 'Piezas vendidas al consumidor. Walmart: POS Qty. Amazon: unidades pedidas.')
med('Sell out monto', 'SUM ( fSellOut[Monto] )', '"$"#,0', '1. Sell out', 'Venta al consumidor en MXN, a precio de la cadena. Walmart: POS Sales. Amazon: ganancia por pedidos.')
med('Último día sell out', 'MAX ( fSellOut[Datos_hasta] )', 'dd/mm/yyyy', '1. Sell out', 'Último día con datos de sell out en el contexto.')
def dax_anio_anterior(base):
    # Mismos días del año anterior, por cadena, hasta el último día con datos de esa cadena.
    # Amazon viene por mes: si su último archivo no cubre el mes completo, el mes del año anterior
    # se toma en proporción a los días cubiertos (por ejemplo, 28 de 30 días).
    return f'''
SUMX (
    VALUES ( dimCadena[Cadena] ),
    VAR _ultimo = CALCULATE ( MAX ( fSellOut[Datos_hasta] ), REMOVEFILTERS ( Calendario ), REMOVEFILTERS ( dimProducto ), REMOVEFILTERS ( dimTienda ) )
    VAR _aa = CALCULATE ( [{base}], SAMEPERIODLASTYEAR ( Calendario[Fecha] ), Calendario[Fecha] <= EDATE ( _ultimo, -12 ) )
    VAR _mesParcial = CALCULATE ( [{base}], SAMEPERIODLASTYEAR ( Calendario[Fecha] ), Calendario[Fecha] = DATE ( YEAR ( _ultimo ) - 1, MONTH ( _ultimo ), 1 ) )
    VAR _proporcion = DIVIDE ( DAY ( _ultimo ), DAY ( EOMONTH ( _ultimo, 0 ) ) )
    RETURN
        IF (
            ISBLANK ( _ultimo ), BLANK (),
            IF ( dimCadena[Cadena] = "Amazon", _aa - _mesParcial * ( 1 - _proporcion ), _aa )
        )
)'''

med('Sell out piezas año anterior', dax_anio_anterior('Sell out piezas'), '#,0', '1. Sell out',
    'Piezas de los mismos días del año anterior, hasta el último día con datos de cada cadena. Amazon (mensual): el mes en curso se compara en proporción a los días cubiertos.')
med('Sell out monto año anterior', dax_anio_anterior('Sell out monto'), '"$"#,0', '1. Sell out',
    'Monto de los mismos días del año anterior, hasta el último día con datos de cada cadena. Amazon (mensual): el mes en curso se compara en proporción a los días cubiertos.')
med('Hay historial año anterior', '''
VAR _ultimo = CALCULATE ( MAX ( fSellOut[Datos_hasta] ), REMOVEFILTERS ( Calendario ), REMOVEFILTERS ( dimProducto ), REMOVEFILTERS ( dimTienda ) )
RETURN
    NOT ISBLANK ( _ultimo )
        && CALCULATE (
            COUNTROWS ( fSellOut ),
            SAMEPERIODLASTYEAR ( Calendario[Fecha] ),
            Calendario[Fecha] <= EDATE ( _ultimo, -12 ),
            REMOVEFILTERS ( dimProducto ),
            REMOVEFILTERS ( dimTienda )
        ) > 0''', None, '1. Sell out',
    'Verdadero si la cadena tiene datos cargados en los mismos días del año anterior (de cualquier producto). Sirve para no comparar una cadena que todavía no tiene historial.')
for _base in ('piezas', 'monto'):
    med(f'Sell out {_base} comparable', f'''
SUMX (
    VALUES ( dimCadena[Cadena] ),
    IF ( [Hay historial año anterior], [Sell out {_base}] )
)''', '#,0' if _base == 'piezas' else '"$"#,0', '1. Sell out',
        f'Sell out en {_base} solo de las cadenas que tienen historial del año anterior. Es la base del crecimiento, para comparar lo mismo contra lo mismo.')
FMT_CREC = '"▲ "0.0%;"▼ "0.0%;0.0%'
med('Crecimiento sell out piezas', 'DIVIDE ( [Sell out piezas comparable] - [Sell out piezas año anterior], [Sell out piezas año anterior] )', FMT_CREC, '1. Sell out', 'Crecimiento en piezas contra los mismos días del año anterior, solo con las cadenas que tienen historial.')
med('Crecimiento sell out monto', 'DIVIDE ( [Sell out monto comparable] - [Sell out monto año anterior], [Sell out monto año anterior] )', FMT_CREC, '1. Sell out', 'Crecimiento en monto contra los mismos días del año anterior, solo con las cadenas que tienen historial.')
med('Participación sell out monto', 'DIVIDE ( [Sell out monto], CALCULATE ( [Sell out monto], ALLSELECTED ( dimProducto ) ) )', '0.0%', '1. Sell out', 'Parte del monto de sell out que aporta cada producto, dentro de lo filtrado.')
for _base in ('monto', 'piezas'):
    med(f'Texto vs año anterior {_base}', f'''
VAR _aa = [Sell out {_base} año anterior]
VAR _crec = [Crecimiento sell out {_base}]
VAR _conVenta = FILTER ( VALUES ( dimCadena[Cadena] ), NOT ISBLANK ( [Sell out {_base}] ) )
VAR _sinHistorial = FILTER ( _conVenta, NOT [Hay historial año anterior] )
VAR _comparadas = CONCATENATEX ( FILTER ( _conVenta, [Hay historial año anterior] ), dimCadena[Cadena], " y " )
RETURN
    IF (
        ISBLANK ( _aa ) || _aa = 0, "Sin año anterior",
        IF ( _crec >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( _crec ), "0.0%" )
            & IF ( COUNTROWS ( _sinHistorial ) > 0, " (solo " & _comparadas & ")" )
    )''', None, '1. Sell out',
        f'Tarjeta: crecimiento en {_base} contra los mismos días del año anterior, con flecha. Si una cadena todavía no tiene historial, dice qué cadenas se compararon. "Sin año anterior" si no hay datos para comparar.')
med('Tiendas con venta', 'CALCULATE ( DISTINCTCOUNT ( fSellOut[Tienda_Nbr] ), fSellOut[Cadena] = "Walmart", fSellOut[Piezas] > 0 ) + 0', '#,0', '1. Sell out', 'Tiendas de Walmart que vendieron al menos una pieza en el periodo.')
_METRICA = 'SELECTEDVALUE ( sMetrica[Metrica], "Monto" ) = "Piezas"'
med('Sell out', f'IF ( {_METRICA}, [Sell out piezas], [Sell out monto] )', None, '1. Sell out',
    'Sell out en monto o en piezas, según el selector "Ver gráficos en" de la página Sell out (por omisión, monto).',
    f'IF ( {_METRICA}, "#,0", "$#,0" )')
med('Sell out año anterior', f'IF ( {_METRICA}, [Sell out piezas año anterior], [Sell out monto año anterior] )', None, '1. Sell out',
    'Sell out del año anterior en monto o en piezas, según el selector "Ver gráficos en".',
    f'IF ( {_METRICA}, "#,0", "$#,0" )')
med('Venta 28 días Walmart', '''
VAR _ultimo = CALCULATE ( MAX ( fSellOut[Datos_hasta] ), REMOVEFILTERS ( Calendario ), REMOVEFILTERS ( dimProducto ), REMOVEFILTERS ( dimTienda ), fSellOut[Cadena] = "Walmart" )
RETURN
    CALCULATE ( [Sell out piezas], DATESBETWEEN ( Calendario[Fecha], _ultimo - 27, _ultimo ), fSellOut[Cadena] = "Walmart" )''', '#,0', '1. Sell out',
    'Piezas vendidas en Walmart en los últimos 28 días con datos.')
med('Inventario piezas', '''
SUMX (
    VALUES ( dimCadena[Cadena] ),
    VAR _f = CALCULATE ( MAX ( fInventarioCadena[Fecha] ), REMOVEFILTERS ( dimProducto ), REMOVEFILTERS ( dimTienda ) )
    RETURN
        CALCULATE ( SUM ( fInventarioCadena[Piezas_disponibles] ), fInventarioCadena[Fecha] = _f )
)''', '#,0', '2. Inventario en cadenas', 'Piezas disponibles en la última foto de cada cadena (Walmart: en tienda; Amazon: aptas para la venta). La fecha de la foto es la última de la cadena, aunque un producto o una tienda ya no aparezca en ella.')
med('Fecha de inventario', 'MAX ( fInventarioCadena[Fecha] )', 'dd/mm/yyyy', '2. Inventario en cadenas', 'Fecha de la foto de inventario más reciente en el contexto.')
med('Tiendas con inventario', '''
VAR _f = CALCULATE ( MAX ( fInventarioCadena[Fecha] ), dimCadena[Cadena] = "Walmart", REMOVEFILTERS ( dimProducto ), REMOVEFILTERS ( dimTienda ) )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( fInventarioCadena[Tienda_Nbr] ),
        dimCadena[Cadena] = "Walmart",
        fInventarioCadena[Fecha] = _f,
        fInventarioCadena[Piezas_disponibles] > 0
    )''', '#,0', '2. Inventario en cadenas', 'Tiendas de Walmart con más de 0 piezas en la última foto.')
med('Venta promedio mensual piezas', '''
SUMX (
    VALUES ( dimCadena[Cadena] ),
    VAR _ultimo = CALCULATE ( MAX ( fSellOut[Datos_hasta] ), REMOVEFILTERS ( dimProducto ), REMOVEFILTERS ( dimTienda ) )
    VAR _fin = IF ( _ultimo = EOMONTH ( _ultimo, 0 ), _ultimo, EOMONTH ( _ultimo, -1 ) )
    VAR _ini = EOMONTH ( _fin, -3 ) + 1
    RETURN
        IF ( ISBLANK ( _ultimo ), BLANK (), DIVIDE ( CALCULATE ( [Sell out piezas], DATESBETWEEN ( Calendario[Fecha], _ini, _fin ) ), 3 ) )
)''', '#,0', '2. Inventario en cadenas', 'Promedio de piezas vendidas en los últimos 3 meses cerrados de cada cadena (propuesta; ver DEFINICIONES_INDICADORES.md).')
med('Cobertura meses', 'DIVIDE ( [Inventario piezas], [Venta promedio mensual piezas] )', '0.0', '2. Inventario en cadenas', 'Meses de inventario: inventario / venta promedio mensual. Misma fórmula para las dos cadenas.')
med('Clasificación cobertura', '''
VAR _inv = [Inventario piezas]
VAR _vta = [Venta promedio mensual piezas]
VAR _cob = DIVIDE ( _inv, _vta )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( _inv ) && ISBLANK ( _vta ), BLANK (),
        _inv <= 0, "⚫ Sin inventario",
        ISBLANK ( _vta ) || _vta <= 0, "⚪ Sin rotación",
        _cob < 1, "🔴 Riesgo de quiebre",
        _cob <= 3, "🟢 Saludable",
        "🟡 Sobre stock"
    )''', None, '2. Inventario en cadenas', 'Umbrales provisionales: menos de 1 mes riesgo, de 1 a 3 saludable, más de 3 sobre stock. Pendientes de aprobar.')
for _nombre, _estado, _desc in (
        ('Productos en riesgo de quiebre', '🔴 Riesgo de quiebre', 'menos de 1 mes de cobertura'),
        ('Productos sin inventario', '⚫ Sin inventario', 'venta en los últimos 3 meses y 0 piezas en la última foto'),
        ('Productos con sobre stock', '🟡 Sobre stock', 'más de 3 meses de cobertura')):
    med(_nombre, f'''
COUNTROWS (
    FILTER (
        CROSSJOIN ( VALUES ( dimProducto[Codigo_ERP] ), VALUES ( dimCadena[Cadena] ) ),
        [Clasificación cobertura] = "{_estado}"
    )
) + 0''', '#,0', '2. Inventario en cadenas', f'Productos con {_desc}. Se cuenta cada producto en cada cadena: si le pasa en Walmart y en Amazon, cuenta 2.')
med('Alerta tienda sin inventario', 'IF ( [Venta 28 días Walmart] > 0 && [Inventario piezas] + 0 <= 0, 1 )', '0', '2. Inventario en cadenas',
    'Vale 1 cuando una tienda de Walmart vendió el producto en los últimos 28 días y hoy tiene 0 piezas. Filtra la tabla de tiendas sin inventario.')
med('Piezas ordenadas', 'SUM ( fFillRate[Piezas_ordenadas] )', '#,0', '3. Fill rate', 'Piezas pedidas por Walmart en sus órdenes de compra.')
med('Piezas recibidas', 'SUM ( fFillRate[Piezas_recibidas] )', '#,0', '3. Fill rate', 'Piezas que Walmart recibió de esas órdenes.')
med('Fill rate', 'DIVIDE ( [Piezas recibidas], [Piezas ordenadas] )', '0.0%', '3. Fill rate', 'Piezas recibidas / piezas ordenadas, por mes de la fecha de la orden (propuesta).')
med('Piezas no surtidas', '[Piezas ordenadas] - [Piezas recibidas]', '#,0', '3. Fill rate', 'Piezas ordenadas que Walmart no recibió.')
med('Pronóstico piezas', 'SUM ( fRecship[Piezas] )', '#,0', '4. Pronóstico', 'Piezas que Walmart planea pedir (Recship más reciente).')
med('Pronóstico monto', 'SUM ( fRecship[Monto] )', '"$"#,0', '4. Pronóstico', 'Piezas planeadas por costo por pieza, en MXN.')
med('Meta monto', 'SUM ( Metas[Monto] )', '"$"#,0', '5. Metas', 'Meta mensual de sell in en MXN (hoja Metas del maestro).')
med('Meta piezas', 'SUM ( Metas[Cantidad] )', '#,0', '5. Metas', 'Meta mensual de sell in en piezas.')
# control
med('Datos al - sell out Walmart', 'CALCULATE ( MAX ( fSellOut[Datos_hasta] ), fSellOut[Cadena] = "Walmart", REMOVEFILTERS () )', 'dd/mm/yyyy', '9. Control', 'Último día con sell out de Walmart.')
med('Datos al - sell out Amazon', 'CALCULATE ( MAX ( fSellOut[Datos_hasta] ), fSellOut[Cadena] = "Amazon", REMOVEFILTERS () )', 'dd/mm/yyyy', '9. Control', 'Último día que cubre el archivo de ventas de Amazon más reciente.')
med('Datos al - inventario Walmart', 'CALCULATE ( MAX ( fInventarioCadena[Fecha] ), fInventarioCadena[Cadena] = "Walmart", REMOVEFILTERS () )', 'dd/mm/yyyy', '9. Control', 'Fecha de la última foto de inventario de Walmart.')
med('Datos al - inventario Amazon', 'CALCULATE ( MAX ( fInventarioCadena[Fecha] ), fInventarioCadena[Cadena] = "Amazon", REMOVEFILTERS () )', 'dd/mm/yyyy', '9. Control', 'Fecha de la última foto de inventario de Amazon.')
med('Datos al - fill rate Walmart', 'CALCULATE ( MAX ( fFillRate[Fecha_orden] ), REMOVEFILTERS () )', 'dd/mm/yyyy', '9. Control', 'Fecha de la orden más reciente en el fill rate.')
med('Días sin sell out Walmart', '''
VAR _dias = CALCULATETABLE ( VALUES ( fSellOut[Fecha] ), fSellOut[Cadena] = "Walmart", REMOVEFILTERS () )
VAR _ini = MINX ( _dias, fSellOut[Fecha] )
VAR _fin = MAXX ( _dias, fSellOut[Fecha] )
RETURN
    IF ( ISBLANK ( _ini ), BLANK (), COUNTROWS ( EXCEPT ( CALENDAR ( _ini, _fin ), _dias ) ) + 0 )''', '#,0', '9. Control', 'Días entre el primero y el último con datos en los que no hay sell out de Walmart (descargas faltantes).')
med('Meses sin sell out Amazon', '''
VAR _meses = CALCULATETABLE ( VALUES ( fSellOut[Fecha] ), fSellOut[Cadena] = "Amazon", REMOVEFILTERS () )
VAR _ini = MINX ( _meses, fSellOut[Fecha] )
VAR _fin = MAXX ( _meses, fSellOut[Fecha] )
RETURN
    IF ( ISBLANK ( _ini ), BLANK (), COUNTROWS ( EXCEPT ( FILTER ( CALENDAR ( _ini, _fin ), DAY ( [Date] ) = 1 ), _meses ) ) + 0 )''', '#,0', '9. Control',
    'Meses sin archivo de ventas de Amazon entre el primero y el último cargados.')
med('Meses incompletos Amazon', '''
VAR _meses = CALCULATETABLE (
    ADDCOLUMNS ( VALUES ( fSellOut[Fecha] ), "@Hasta", CALCULATE ( MAX ( fSellOut[Datos_hasta] ) ) ),
    fSellOut[Cadena] = "Amazon", REMOVEFILTERS ()
)
VAR _ultimo = MAXX ( _meses, fSellOut[Fecha] )
RETURN
    IF ( ISBLANK ( _ultimo ), BLANK (), COUNTROWS ( FILTER ( _meses, fSellOut[Fecha] < _ultimo && [@Hasta] < EOMONTH ( fSellOut[Fecha], 0 ) ) ) + 0 )''', '#,0', '9. Control',
    'Meses ya cerrados cuyo archivo de Amazon no llega al último día del mes (por ejemplo, porque Amazon todavía no tenía el último día al descargarlo).')
med('Meses faltantes Amazon', '''
VAR _meses = CALCULATETABLE (
    ADDCOLUMNS ( VALUES ( fSellOut[Fecha] ), "@Hasta", CALCULATE ( MAX ( fSellOut[Datos_hasta] ) ) ),
    fSellOut[Cadena] = "Amazon", REMOVEFILTERS ()
)
VAR _ini = MINX ( _meses, fSellOut[Fecha] )
VAR _fin = MAXX ( _meses, fSellOut[Fecha] )
VAR _faltan = EXCEPT ( FILTER ( CALENDAR ( _ini, _fin ), DAY ( [Date] ) = 1 ), SELECTCOLUMNS ( _meses, "Date", fSellOut[Fecha] ) )
VAR _incompletos = FILTER ( _meses, fSellOut[Fecha] < _fin && [@Hasta] < EOMONTH ( fSellOut[Fecha], 0 ) )
VAR _txtFaltan = CONCATENATEX ( _faltan, LOOKUPVALUE ( Calendario[Mes_año], Calendario[Fecha], [Date] ), ", ", [Date], ASC )
VAR _txtIncompletos = CONCATENATEX ( _incompletos, LOOKUPVALUE ( Calendario[Mes_año], Calendario[Fecha], fSellOut[Fecha] ), ", ", fSellOut[Fecha], ASC )
RETURN
    IF (
        ISBLANK ( _ini ), BLANK (),
        IF ( _txtFaltan = "" && _txtIncompletos = "", "Ninguno",
            IF ( _txtFaltan <> "", "Faltan: " & _txtFaltan )
                & IF ( _txtFaltan <> "" && _txtIncompletos <> "", " · " )
                & IF ( _txtIncompletos <> "", "Incompletos: " & _txtIncompletos )
        )
    )''', None, '9. Control',
    'Meses de Amazon por descargar: los que faltan y los cerrados que quedaron incompletos.')
med('Filas sin homologar', '''
CALCULATE ( COUNTROWS ( fSellOut ), REMOVEFILTERS (), ISBLANK ( fSellOut[Codigo_ERP] ) ) + 0
    + CALCULATE ( COUNTROWS ( fInventarioCadena ), REMOVEFILTERS (), ISBLANK ( fInventarioCadena[Codigo_ERP] ) ) + 0
    + CALCULATE ( COUNTROWS ( fFillRate ), REMOVEFILTERS (), ISBLANK ( fFillRate[Codigo_ERP] ) ) + 0
    + CALCULATE ( COUNTROWS ( fRecship ), REMOVEFILTERS (), ISBLANK ( fRecship[Codigo_ERP] ) ) + 0''', '#,0', '9. Control', 'Filas cuyo código de cadena no está en la hoja Equivalencias del maestro.')
med('Códigos sin homologar', '''
VAR _t =
    UNION (
        SELECTCOLUMNS ( CALCULATETABLE ( VALUES ( fSellOut[Codigo_cadena] ), REMOVEFILTERS (), ISBLANK ( fSellOut[Codigo_ERP] ) ), "Codigo", fSellOut[Codigo_cadena] ),
        SELECTCOLUMNS ( CALCULATETABLE ( VALUES ( fInventarioCadena[Codigo_cadena] ), REMOVEFILTERS (), ISBLANK ( fInventarioCadena[Codigo_ERP] ) ), "Codigo", fInventarioCadena[Codigo_cadena] ),
        SELECTCOLUMNS ( CALCULATETABLE ( VALUES ( fFillRate[Codigo_cadena] ), REMOVEFILTERS (), ISBLANK ( fFillRate[Codigo_ERP] ) ), "Codigo", fFillRate[Codigo_cadena] ),
        SELECTCOLUMNS ( CALCULATETABLE ( VALUES ( fRecship[Codigo_cadena] ), REMOVEFILTERS (), ISBLANK ( fRecship[Codigo_ERP] ) ), "Codigo", fRecship[Codigo_cadena] )
    )
VAR _lista = CONCATENATEX ( DISTINCT ( _t ), [Codigo], ", " )
RETURN
    IF ( _lista = "", "Ninguno", _lista )''', None, '9. Control', 'Lista de códigos (artículo de Walmart o ASIN) que faltan en la hoja Equivalencias.')
def _fecha_txt(m):
    return f'IF ( ISBLANK ( [{m}] ), "sin datos", FORMAT ( [{m}], "dd/mm/yyyy" ) )'
med('Texto datos sell out', f'"Sell out · Walmart al " & {_fecha_txt("Datos al - sell out Walmart")} & "  ·  Amazon al " & {_fecha_txt("Datos al - sell out Amazon")}',
    None, '9. Control', 'Encabezado de la página Sell out: último día con datos de cada cadena.')
med('Texto datos inventario', f'"Inventario · Walmart al " & {_fecha_txt("Datos al - inventario Walmart")} & "  ·  Amazon al " & {_fecha_txt("Datos al - inventario Amazon")}',
    None, '9. Control', 'Encabezado de la página Inventario: fecha de la última foto de cada cadena.')
med('Fecha del Recship', 'CALCULATE ( MAX ( fRecship[Fecha_creacion] ), REMOVEFILTERS () )', 'dd/mm/yyyy', '9. Control', 'Fecha en que Walmart generó el Recship más reciente.')
med('Texto datos abasto', f'"Walmart · órdenes hasta el " & {_fecha_txt("Datos al - fill rate Walmart")} & "  ·  Recship del " & {_fecha_txt("Fecha del Recship")}',
    None, '9. Control', 'Encabezado de la página Abasto: orden más reciente del fill rate y fecha del Recship.')
med('Estado del reporte', '''
VAR _hoy = TODAY ()
VAR _atrasoWM = IF ( ISBLANK ( [Datos al - sell out Walmart] ), 999, DATEDIFF ( [Datos al - sell out Walmart], _hoy, DAY ) )
VAR _atrasoAMZ = IF ( ISBLANK ( [Datos al - sell out Amazon] ), 999, DATEDIFF ( [Datos al - sell out Amazon], _hoy, DAY ) )
VAR _atrasoInvWM = IF ( ISBLANK ( [Datos al - inventario Walmart] ), 999, DATEDIFF ( [Datos al - inventario Walmart], _hoy, DAY ) )
VAR _atrasoInvAMZ = IF ( ISBLANK ( [Datos al - inventario Amazon] ), 999, DATEDIFF ( [Datos al - inventario Amazon], _hoy, DAY ) )
RETURN
    SWITCH (
        TRUE (),
        [Días sin sell out Walmart] > 0, "🔴 Faltan días de sell out de Walmart",
        [Meses sin sell out Amazon] > 0, "🔴 Faltan meses de ventas de Amazon",
        [Meses incompletos Amazon] > 0, "🔴 Hay meses de Amazon incompletos",
        [Filas sin homologar] > 0, "🔴 Hay códigos sin homologar",
        _atrasoWM > 3, "🟡 Sell out de Walmart atrasado",
        _atrasoAMZ > 3, "🟡 Ventas de Amazon atrasadas",
        _atrasoInvWM > 3, "🟡 Inventario de Walmart atrasado",
        _atrasoInvAMZ > 3, "🟡 Inventario de Amazon atrasado",
        "🟢 Listo para enviar"
    )''', None, '9. Control',
    'Semáforo general con el motivo. Rojo: faltan días de Walmart, faltan o están incompletos meses de Amazon, o hay códigos sin homologar. Amarillo: el sell out o el inventario de Walmart o de Amazon tiene más de 3 días.')

# ---------------------------------------------------------------- escribir TMDL
def tabla_tmdl(nombre):
    lines = [f'/// {DESC_TABLA[nombre]}', f'table {nombre}']
    if nombre == 'Calendario':
        lines.append('\tdataCategory: Time')
    lines.append('')
    if nombre == '_Medidas':
        for (n, e, fmt, carpeta, desc) in MED:
            q = f"'{n}'"
            e = textwrap.dedent(e).strip('\n')
            lines.append(f'\t/// {desc}')
            if '\n' in e:
                lines.append(f'\tmeasure {q} =')
                lines.append(bloque(e, 3))
            else:
                lines.append(f'\tmeasure {q} = {e}')
            if fmt:
                lines.append(f'\t\tformatString: {fmt}')
            lines.append(f'\t\tdisplayFolder: {carpeta}')
            lines.append('')
            if n in FORMATO_DINAMICO:
                # siempre al final de la medida, después de una línea en blanco
                lines.append(f'\t\tformatStringDefinition = {FORMATO_DINAMICO[n]}')
                lines.append('')
    for (c, t, x) in COLS[nombre]:
        lines.append(columna(nombre, c, t, x))
        lines.append('')
    for (c, e, t, x, desc) in CALC.get(nombre, []):
        lines.append(columna_calc(c, e, t, x, desc))
        lines.append('')
    lines.append(f'\tpartition {nombre} = m')
    lines.append('\t\tmode: import')
    src = textwrap.dedent(P[nombre]).strip('\n')
    lines.append('\t\tsource =')
    lines.append(bloque(src, 4))
    lines.append('')
    lines.append('\tannotation PBI_ResultType = Table')
    lines.append('')
    return '\n'.join(lines)

TABLAS = ['Calendario', 'dimCadena', 'dimProducto', 'dimTienda', 'fSellOut', 'fInventarioCadena', 'fFillRate', 'fRecship', 'Metas', 'ctlArchivos', 'sMetrica', '_Medidas']
for t in TABLAS:
    escribir(f'{SM}/definition/tables/{t}.tmdl', tabla_tmdl(t))

# expresiones (consultas que no se cargan, funciones y parámetro)
exp = []
exp.append('/// Carpeta donde están los datos (Amazon, Walmart, ERP y Maestros). Debe terminar en \\.')
exp.append(f'expression RutaDatos = "{PARAM_RUTA}" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]')
exp.append('')
exp.append('\tannotation PBI_ResultType = Text')
exp.append('')
DESC_EXP = {
 'Archivos': 'Lista de todos los archivos de Excel de la carpeta de datos, con su carpeta relativa.',
 'fnFechaMDA': 'Función: texto mm-dd-aaaa o mm/dd/aaaa a fecha.',
 'fnFechaAMD': 'Función: texto aaaa/mm/dd a fecha.',
 'fnNumero': 'Función: número en texto con punto decimal a número.',
 'fnRetailLink': 'Función: lee un archivo de Retail Link tal como se descarga.',
 'fnAmazon': 'Función: lee un archivo de Amazon Vendor Central tal como se descarga.',
 'Maestro': 'Libro Maestro_Wellpro.xlsx.',
 'fnTablaMaestro': 'Función: devuelve una tabla del maestro por su nombre.',
 'Productos': 'Hoja Productos del maestro.',
 'Equivalencias': 'Hoja Equivalencias del maestro: código de cada cadena -> código del ERP.',
 'WM_SellOut_Archivos': 'Archivos de sell out de Walmart y qué días se toman de cada uno (cada día, del más reciente).',
 'WM_SellOut_Filas': 'Filas de sell out de Walmart: de cada archivo, solo los días que le tocan.',
 'WM_SellOut': 'Sell out de Walmart depurado y homologado.',
 'AMZ_SellOut_Archivos': 'Archivos de ventas de Amazon y cuál se usa por mes.',
 'AMZ_SellOut': 'Sell out de Amazon homologado.',
 'WM_Inventario_Archivos': 'Archivos de inventario de Walmart y cuáles se usan (una foto por día; de cada mes, la última).',
 'WM_Inventario_Filas': 'Filas de los archivos de inventario de Walmart que se usan.',
 'WM_Inventario': 'Inventario en tiendas de Walmart depurado y homologado.',
 'AMZ_Inventario_Archivos': 'Archivos de inventario de Amazon y cuáles se usan (una foto por día; de cada mes, la última).',
 'AMZ_Inventario': 'Inventario de Amazon homologado.',
 'WM_FillRate_Archivos': 'Archivos de fill rate de Walmart.',
 'WM_FillRate_Lineas': 'Líneas de órdenes de Walmart: cada orden y artículo, de la descarga más reciente.',
 'WM_FillRate': 'Órdenes de compra de Walmart homologadas.',
 'WM_Recship_Archivos': 'Archivos de Recship de Walmart y cuál es el más reciente.',
 'WM_Recship': 'Pronóstico de pedidos de Walmart (archivo más reciente).',
}
for nombre, m in M.items():
    exp.append(f'/// {DESC_EXP[nombre]}')
    exp.append(f'expression {nombre} =')
    exp.append(bloque(m, 2))
    exp.append('')
    tipo = 'Function' if nombre.startswith('fn') else ('Binary' if False else 'Table')
    if nombre == 'Maestro':
        tipo = 'Table'
    exp.append(f'\tannotation PBI_ResultType = {tipo}')
    exp.append('')
escribir(f'{SM}/definition/expressions.tmdl', '\n'.join(exp))

# relaciones
REL = [
 ('fSellOut', 'Fecha', 'Calendario', 'Fecha'), ('fSellOut', 'Codigo_ERP', 'dimProducto', 'Codigo_ERP'),
 ('fSellOut', 'Cadena', 'dimCadena', 'Cadena'), ('fSellOut', 'Tienda_Nbr', 'dimTienda', 'Tienda_Nbr'),
 ('fInventarioCadena', 'Fecha', 'Calendario', 'Fecha'), ('fInventarioCadena', 'Codigo_ERP', 'dimProducto', 'Codigo_ERP'),
 ('fInventarioCadena', 'Cadena', 'dimCadena', 'Cadena'), ('fInventarioCadena', 'Tienda_Nbr', 'dimTienda', 'Tienda_Nbr'),
 ('fFillRate', 'Fecha_orden', 'Calendario', 'Fecha'), ('fFillRate', 'Codigo_ERP', 'dimProducto', 'Codigo_ERP'),
 ('fFillRate', 'Cadena', 'dimCadena', 'Cadena'),
 ('fRecship', 'Fecha_pedido', 'Calendario', 'Fecha'), ('fRecship', 'Codigo_ERP', 'dimProducto', 'Codigo_ERP'),
 ('fRecship', 'Cadena', 'dimCadena', 'Cadena'),
 ('Metas', 'Mes', 'Calendario', 'Fecha'), ('Metas', 'Codigo_ERP', 'dimProducto', 'Codigo_ERP'),
]
rel = []
for a, ca, b, cb in REL:
    rel.append(f'relationship {a}_{ca}_{b}')
    rel.append(f'\tfromColumn: {a}.{ca}')
    rel.append(f'\ttoColumn: {b}.{cb}')
    rel.append('')
escribir(f'{SM}/definition/relationships.tmdl', '\n'.join(rel))

orden = ['RutaDatos'] + list(M.keys()) + TABLAS
modelo = ['model Model', '\tculture: es-MX', '\tdefaultPowerBIDataSourceVersion: powerBI_V3', '\tsourceQueryCulture: es-MX',
          '\tdataAccessOptions', '\t\tlegacyRedirects', '\t\treturnErrorValuesAsNull', '',
          'annotation __PBI_TimeIntelligenceEnabled = 0', '',
          'annotation PBI_QueryOrder = ' + json.dumps(orden, ensure_ascii=False), '']
modelo += [f'ref table {t}' for t in TABLAS]
modelo.append('')
escribir(f'{SM}/definition/model.tmdl', '\n'.join(modelo))
escribir(f'{SM}/definition/database.tmdl', 'database\n\tcompatibilityLevel: 1606\n\n')
jdump(f'{SM}/definition.pbism', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json", "version": "4.2", "settings": {}})
jdump(f'{SM}/.platform', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
      "metadata": {"type": "SemanticModel", "displayName": NOMBRE}, "config": {"version": "2.0", "logicalId": IDS.get('SM', str(uuid.uuid4()))}})

# ---------------------------------------------------------------- reporte (PBIR)
LOGO = os.path.join(AQUI, 'recursos', 'LogoWellpro.png')
VC_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json"
PAGE_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"

# Colores (paleta validada con el validador de dataviz: rojo Wellpro, azul Walmart, ámbar Amazon)
ROJO, AZUL_WM, AMBAR_AMZ, GRIS_AA = '#E31E26', '#2A78D6', '#EDA100', '#B8BFC7'
TXT, TXT2, TXT3 = '#1F2933', '#52606D', '#7B8794'
FONDO, BORDE, GRILLA = '#F4F5F7', '#E4E7EB', '#EEF0F3'
COLOR_CADENA = {'Walmart': AZUL_WM, 'Amazon': AMBAR_AMZ}

jdump(f'{RAIZ}/{NOMBRE}.pbip', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
      "version": "1.0", "artifacts": [{"report": {"path": f"{NOMBRE}.Report"}}], "settings": {"enableAutoRecovery": True}})
jdump(f'{RP}/.platform', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
      "metadata": {"type": "Report", "displayName": NOMBRE}, "config": {"version": "2.0", "logicalId": IDS.get('RP', str(uuid.uuid4()))}})
jdump(f'{RP}/definition.pbir', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
      "version": "4.0", "datasetReference": {"byPath": {"path": f"../{NOMBRE}.SemanticModel"}}})
jdump(f'{RP}/definition/version.json', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
os.makedirs(f'{RP}/StaticResources/SharedResources/BaseThemes', exist_ok=True)
shutil.copy(TEMA_BASE, f'{RP}/StaticResources/SharedResources/BaseThemes/Fluent2-CY26SU08.json')
os.makedirs(f'{RP}/StaticResources/RegisteredResources', exist_ok=True)
shutil.copy(LOGO, f'{RP}/StaticResources/RegisteredResources/LogoWellpro.png')

sc = lambda c: {"solid": {"color": c}}
TEMA = {
 "name": "Wellpro",
 "dataColors": ["#E31E26", "#2A78D6", "#1BAF7A", "#EDA100", "#E87BA4", "#008300", "#4A3AA7", "#EB6834"],
 "foreground": TXT, "foregroundNeutralSecondary": TXT2, "foregroundNeutralTertiary": TXT3,
 "background": "#FFFFFF", "backgroundLight": FONDO, "backgroundNeutral": BORDE,
 "tableAccent": ROJO, "good": "#1E8E3E", "neutral": "#B26A00", "bad": "#C62828",
 "maximum": ROJO, "center": "#F29A9E", "minimum": "#FDECEC", "hyperlink": AZUL_WM, "visitedHyperlink": "#1B5FAE",
 "textClasses": {
   "title": {"fontFace": "Segoe UI Semibold", "fontSize": 11, "color": TXT},
   "header": {"fontFace": "Segoe UI Semibold", "fontSize": 10, "color": TXT},
   "label": {"fontFace": "Segoe UI", "fontSize": 9, "color": TXT2},
   "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 22, "color": TXT}},
 "visualStyles": {
   "*": {"*": {
     "background": [{"show": True, "color": sc("#FFFFFF"), "transparency": 0}],
     "border": [{"show": True, "color": sc(BORDE), "radius": 10}],
     "dropShadow": [{"show": False}],
     "title": [{"fontColor": sc(TXT), "fontSize": 11, "bold": True}],
     "subTitle": [{"fontColor": sc(TXT3), "fontSize": 9}],
     "categoryAxis": [{"labelColor": sc(TXT2), "gridlineShow": False, "showAxisTitle": False}],
     "valueAxis": [{"labelColor": sc(TXT3), "gridlineColor": sc(GRILLA), "showAxisTitle": False}],
     "legend": [{"labelColor": sc(TXT2)}]}},
   "page": {"*": {"background": [{"color": sc(FONDO), "transparency": 0}], "outspace": [{"color": sc(FONDO)}]}},
   "tableEx": {"*": {
     "columnHeaders": [{"fontColor": sc(TXT), "backColor": sc(FONDO), "fontFamily": "Segoe UI Semibold"}],
     "values": [{"fontColorPrimary": sc(TXT), "backColorPrimary": sc("#FFFFFF"), "fontColorSecondary": sc(TXT), "backColorSecondary": sc("#FAFBFC")}],
     "total": [{"fontColor": sc(TXT), "backColor": sc(FONDO), "fontFamily": "Segoe UI Semibold"}],
     "grid": [{"gridHorizontalColor": sc(GRILLA), "outlineColor": sc(BORDE)}]}},
   "pivotTable": {"*": {
     "columnHeaders": [{"fontColor": sc(TXT), "backColor": sc(FONDO), "fontFamily": "Segoe UI Semibold"}],
     "rowHeaders": [{"fontColor": sc(TXT)}],
     "total": [{"fontColor": sc(TXT), "backColor": sc(FONDO), "fontFamily": "Segoe UI Semibold"}],
     "grid": [{"gridHorizontalColor": sc(GRILLA), "outlineColor": sc(BORDE)}]}},
   "slicer": {"*": {"header": [{"fontColor": sc(TXT3), "textSize": 9}], "items": [{"fontColor": sc(TXT), "textSize": 10}]}}}}
jdump(f'{RP}/StaticResources/RegisteredResources/TemaWellpro.json', TEMA)

lit = lambda v: {"expr": {"Literal": {"Value": v}}}
L = lit
C = lambda c: {"solid": {"color": lit(f"'{c}'")}}
def props(**kw):
    return [{"properties": kw}]
def txt(s):
    return "'" + s.replace("'", "''") + "'"
VERSIONES = {"visual": "2.12.0", "report": "3.4.0", "page": "2.3.1"}
jdump(f'{RP}/definition/report.json', {
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json",
  "themeCollection": {"baseTheme": {"name": "Fluent2-CY26SU08", "reportVersionAtImport": VERSIONES, "type": "SharedResources"},
                      "customTheme": {"name": "TemaWellpro.json", "reportVersionAtImport": VERSIONES, "type": "RegisteredResources"}},
  "objects": {"section": [{"properties": {"verticalAlignment": lit("'Top'")}}], "outspacePane": [{"properties": {"expanded": lit("false")}}]},
  "resourcePackages": [
    {"name": "SharedResources", "type": "SharedResources", "items": [{"name": "Fluent2-CY26SU08", "path": "BaseThemes/Fluent2-CY26SU08.json", "type": "BaseTheme"}]},
    {"name": "RegisteredResources", "type": "RegisteredResources", "items": [
        {"name": "TemaWellpro.json", "path": "TemaWellpro.json", "type": "CustomTheme"},
        {"name": "LogoWellpro.png", "path": "LogoWellpro.png", "type": "Image"}]}],
  "settings": {"useStylableVisualContainerHeader": True, "exportDataMode": "AllowSummarized", "defaultDrillFilterOtherVisuals": True,
               "allowChangeFilterTypes": True, "useEnhancedTooltips": True, "useDefaultAggregateDisplayName": True}})

# ---- campos
def ref_medida(m):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Medidas"}}, "Property": m}}
def ref_col(t, c):
    return {"Column": {"Expression": {"SourceRef": {"Entity": t}}, "Property": c}}
def campo_medida(m, alias=None):
    d = {"field": ref_medida(m), "queryRef": f"_Medidas.{m}", "nativeQueryRef": m}
    if alias: d["displayName"] = alias
    return d
def campo_col(t, c, alias=None, activo=False):
    d = {"field": ref_col(t, c), "queryRef": f"{t}.{c}", "nativeQueryRef": c}
    if activo: d["active"] = True
    if alias: d["displayName"] = alias
    return d
def consulta(orden=None, **roles):
    q = {"queryState": {rol: {"projections": proys} for rol, proys in roles.items()}}
    if orden:
        q["sortDefinition"] = {"sort": [{"field": f, "direction": d} for f, d in orden]}
    return q

# ---- filtros
def _where(tabla, cond):
    return {"Version": 2, "From": [{"Name": "t", "Entity": tabla, "Type": 0}], "Where": [{"Condition": cond}]}
def _col_src(c):
    return {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": c}}
def cond_in(c, valores):
    return {"In": {"Expressions": [_col_src(c)], "Values": [[{"Literal": {"Value": txt(v)}}] for v in valores]}}
def cond_rango(c, minimo, maximo):
    izq = {"Comparison": {"ComparisonKind": 2, "Left": _col_src(c), "Right": {"Literal": {"Value": f"{minimo}L"}}}}
    der = {"Comparison": {"ComparisonKind": 4, "Left": _col_src(c), "Right": {"Literal": {"Value": f"{maximo}L"}}}}
    return {"And": {"Left": izq, "Right": der}}
def filtro_valores(nombre, tabla, col, valores):
    return {"name": nombre, "field": ref_col(tabla, col), "type": "Categorical", "filter": _where(tabla, cond_in(col, valores)), "howCreated": "User"}
def filtro_meses(nombre, desde, hasta):
    return {"name": nombre, "field": ref_col('Calendario', 'Meses_atras'), "type": "Advanced",
            "filter": _where('Calendario', cond_rango('Meses_atras', desde, hasta)), "howCreated": "User"}
def filtro_medida_igual(nombre, medida, valor):
    cond = {"Comparison": {"ComparisonKind": 0, "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": medida}},
                           "Right": {"Literal": {"Value": f"{valor}L"}}}}
    return {"name": nombre, "field": ref_medida(medida), "type": "Advanced", "filter": _where('_Medidas', cond), "howCreated": "User"}

# ---- contenedores
def contenedor(titulo=None, subtitulo=None, fondo=True, borde=True, pad=10, encabezado=True, color_fondo='#FFFFFF',
               titulo_tam=11, titulo_color=TXT, titulo_negrita=True):
    o = {}
    if titulo:
        o["title"] = props(show=L('true'), text=L(txt(titulo)), fontColor=C(titulo_color), fontSize=L(f'{titulo_tam}D'),
                           bold=L('true' if titulo_negrita else 'false'))
    else:
        o["title"] = props(show=L('false'))
    if subtitulo:
        o["subTitle"] = props(show=L('true'), text=L(txt(subtitulo)), fontColor=C(TXT3), fontSize=L('9D'))
    o["background"] = props(show=L('true' if fondo else 'false'), color=C(color_fondo), transparency=L('0D'))
    o["border"] = props(show=L('true' if borde else 'false'), color=C(BORDE), radius=L('10D'))
    o["dropShadow"] = props(show=L('false'))
    o["padding"] = props(top=L(f'{pad}D'), bottom=L(f'{pad}D'), left=L(f'{pad}D'), right=L(f'{pad}D'))
    if not encabezado:
        o["visualHeader"] = props(show=L('false'))
    return o

_z = [0]
def visual(nombre, pos, vtype, query=None, objetos=None, cont=None, filtros=None, sync=None):
    _z[0] += 100
    x, y, w, h = pos
    v = {"visualType": vtype}
    if query: v["query"] = query
    if objetos: v["objects"] = objetos
    v["visualContainerObjects"] = cont if cont is not None else contenedor()
    if sync: v["syncGroup"] = {"groupName": sync, "fieldChanges": True, "filterChanges": True}
    v["drillFilterOtherVisuals"] = True
    d = {"$schema": VC_SCHEMA, "name": nombre,
         "position": {"x": x, "y": y, "z": _z[0], "height": h, "width": w, "tabOrder": _z[0]}, "visual": v}
    if filtros: d["filterConfig"] = {"filters": filtros}
    return d

# ---- piezas del encabezado
def caja(nombre, pos, color):
    return visual(nombre, pos, 'textbox', objetos={"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": " "}]}]}}]},
                  cont=contenedor(borde=False, pad=0, encabezado=False, color_fondo=color))
def logo(nombre, pos):
    return visual(nombre, pos, 'image', objetos={
        "general": [{"properties": {"imageUrl": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": "LogoWellpro.png"}}}}}],
        "imageScaling": props(imageScalingType=L("'Fit'"))}, cont=contenedor(fondo=False, borde=False, pad=0, encabezado=False))
def navegador(nombre, pos):
    estados = {'default': (TXT2, FONDO, 'false'), 'hover': (TXT, BORDE, 'false'), 'press': (TXT, BORDE, 'true'), 'selected': ('#FFFFFF', ROJO, 'true')}
    return visual(nombre, pos, 'pageNavigator', objetos={
        "text": [{"properties": {"show": L('true'), "fontColor": C(t), "fontSize": L('11D'), "bold": L(b)}, "selector": {"id": k}} for k, (t, f, b) in estados.items()],
        "fill": [{"properties": {"show": L('true'), "fillColor": C(f), "transparency": L('0D')}, "selector": {"id": k}} for k, (t, f, b) in estados.items()],
        "outline": [{"properties": {"show": L('false')}, "selector": {"id": k}} for k in estados],
        "shape": props(tileShape=L("'rectangleRounded'"), rectangleRoundedCurve=L('8L')),
        "pages": props(showHiddenPages=L('false'), showTooltipPages=L('false'))},
        cont=contenedor(fondo=False, borde=False, pad=0, encabezado=False))
def tarjeta(nombre, pos, medida, titulo, fuente=20, unidades=True, ajustar=False):
    lab = {"fontSize": L(f'{fuente}D'), "color": C(TXT)}
    if unidades: lab["labelDisplayUnits"] = L('1D')
    obj = {"categoryLabels": props(show=L('false')), "labels": [{"properties": lab}]}
    if ajustar: obj["wordWrap"] = props(show=L('true'))
    return visual(nombre, pos, 'card', consulta(Values=[campo_medida(medida)]), obj,
                  contenedor(titulo, pad=8, encabezado=False, titulo_tam=10, titulo_color=TXT2, titulo_negrita=False))
def texto_datos(nombre, pos, medida):
    return visual(nombre, pos, 'card', consulta(Values=[campo_medida(medida)]),
                  {"categoryLabels": props(show=L('false')), "labels": props(fontSize=L('10D'), color=C(TXT2))},
                  contenedor(fondo=False, borde=False, pad=0, encabezado=False))
def encabezado(medida_texto):
    return [caja('hdrFondo', (0, 0, 1280, 60), '#FFFFFF'),
            caja('hdrLinea', (0, 60, 1280, 3), ROJO),
            logo('hdrLogo', (20, 9, 116, 43)),
            navegador('hdrPaginas', (168, 14, 560, 32)),
            texto_datos('hdrDatos', (744, 12, 520, 36), medida_texto)]

# ---- segmentaciones
def segmentacion(nombre, pos, tabla, col, etiqueta, modo='Dropdown', sync=None, multi=True, defecto=None,
                 filtros=None, descendente=False, buscar=False, horizontal=False):
    obj = {"data": props(mode=L(f"'{modo}'")),
           "header": props(show=L('true'), fontColor=C(TXT3), textSize=L('9D')),
           "items": props(fontColor=C(TXT), textSize=L('10D')),
           "selection": props(selectAllCheckboxEnabled=L('true' if multi else 'false'), singleSelect=L('false' if multi else 'true'))}
    gen = {}
    if defecto:
        gen["filter"] = {"filter": _where(tabla, cond_in(col, defecto))}
    if horizontal:
        gen["orientation"] = L('1D')
    if buscar:
        gen["selfFilterEnabled"] = L('true')
    if gen:
        obj["general"] = [{"properties": gen}]
    orden = [(ref_col(tabla, col), 'Descending')] if descendente else None
    return visual(nombre, pos, 'slicer', consulta(orden, Values=[campo_col(tabla, col, etiqueta, activo=True)]), obj,
                  contenedor(pad=4, encabezado=False), filtros, sync)
def seg_cadena(pos):
    return segmentacion('sltCadena', pos, 'dimCadena', 'Cadena', 'Cadena', sync='Cadena')
def seg_familia(pos):
    return segmentacion('sltFamilia', pos, 'dimProducto', 'Familia', 'Familia', sync='Familia',
                        filtros=[filtro_valores('fActivoFamilia', 'dimProducto', 'Activo', ['Sí'])])
def seg_producto(pos):
    return segmentacion('sltProducto', pos, 'dimProducto', 'Producto', 'Producto', sync='Producto', buscar=True,
                        filtros=[filtro_valores('fActivoProducto', 'dimProducto', 'Activo', ['Sí'])])

# ---- gráficos
def ejes(fmt_categoria=None):
    cat = {"showAxisTitle": L('false'), "labelColor": C(TXT2), "fontSize": L('9D'), "gridlineShow": L('false')}
    if fmt_categoria: cat["axisType"] = L("'Categorical'")
    return {"categoryAxis": [{"properties": cat}],
            "valueAxis": props(showAxisTitle=L('false'), labelColor=C(TXT3), fontSize=L('9D'), gridlineColor=C(GRILLA))}
def leyenda(mostrar=True):
    if not mostrar:
        return {"legend": props(show=L('false'))}
    return {"legend": props(show=L('true'), position=L("'Top'"), labelColor=C(TXT2), fontSize=L('9D'), showTitle=L('false'))}
def etiquetas(mostrar=True):
    return {"labels": props(show=L('true' if mostrar else 'false'), color=C(TXT2), fontSize=L('9D'))}
def color_medida(medida, color):
    return {"properties": {"fill": C(color)}, "selector": {"metadata": f"_Medidas.{medida}"}}
def color_cadena(cadena):
    return {"properties": {"fill": C(COLOR_CADENA[cadena])},
            "selector": {"data": [{"scopeId": {"Comparison": {"ComparisonKind": 0, "Left": ref_col('dimCadena', 'Cadena'),
                                                             "Right": {"Literal": {"Value": txt(cadena)}}}}}]}}
def colores_cadena():
    return {"dataPoint": [color_cadena(c) for c in COLOR_CADENA]}
def tabla(nombre, pos, columnas, titulo, subtitulo=None, orden=None, filtros=None, vtype='tableEx', **roles):
    q = consulta(orden, Values=columnas, **roles) if vtype == 'tableEx' else consulta(orden, **roles)
    obj = {"values": props(fontSize=L('10D')), "columnHeaders": props(fontSize=L('10D'), wordWrap=L('true')),
           "total": props(fontSize=L('10D'))}
    return visual(nombre, pos, vtype, q, obj, contenedor(titulo, subtitulo), filtros)

MES = campo_col('Calendario', 'Mes_año', 'Mes')
ORDEN_MES = [(ref_col('Calendario', 'Mes_año'), 'Ascending')]
ULT12 = lambda n: [filtro_meses(n, 0, 11)]
KPI_Y, KPI_H = 134, 78
def kpis(lista):
    n = len(lista)
    w = (1248 - 12 * (n - 1)) // n
    return [tarjeta(nom, (16 + i * (w + 12), KPI_Y, w, KPI_H), m, t, *extra) for i, (nom, m, t, *extra) in enumerate(lista)]

paginas = {}

# ================= Sell out
_z[0] = 0
v_sellout = encabezado('Texto datos sell out') + [
    segmentacion('sltMes', (16, 74, 180, 50), 'Calendario', 'Periodo', 'Mes', defecto=['Mes actual'], descendente=True,
                 filtros=[filtro_meses('fMesesSlicer', 0, 23)]),
    seg_cadena((206, 74, 160, 50)),
    seg_familia((376, 74, 220, 50)),
    seg_producto((606, 74, 330, 50)),
    segmentacion('sltMetrica', (1024, 74, 240, 50), 'sMetrica', 'Metrica', 'Ver gráficos en', modo='Basic', multi=False,
                 defecto=['Monto'], horizontal=True),
] + kpis([('kpiMonto', 'Sell out monto', 'Sell out (MXN)'),
          ('kpiPiezas', 'Sell out piezas', 'Sell out (piezas)'),
          ('kpiCrecMonto', 'Texto vs año anterior monto', 'Monto vs año anterior', 15),
          ('kpiCrecPiezas', 'Texto vs año anterior piezas', 'Piezas vs año anterior', 15),
          ('kpiTiendas', 'Tiendas con venta', 'Tiendas de Walmart con venta')]) + [
    visual('chrMensual', (16, 224, 740, 236), 'clusteredColumnChart',
           consulta(ORDEN_MES, Category=[MES], Y=[campo_medida('Sell out', 'Año actual'), campo_medida('Sell out año anterior', 'Año anterior')]),
           {**ejes(), **leyenda(), **etiquetas(False), "dataPoint": [color_medida('Sell out', ROJO), color_medida('Sell out año anterior', GRIS_AA)]},
           contenedor('Sell out por mes', 'Últimos 12 meses, sin importar el mes elegido · gris: mismos días del año anterior'),
           filtros=ULT12('fUlt12Mensual')),
    visual('chrFamilia', (768, 224, 496, 236), 'barChart',
           consulta([(ref_medida('Sell out'), 'Descending')], Category=[campo_col('dimProducto', 'Familia')],
                    Series=[campo_col('dimCadena', 'Cadena')], Y=[campo_medida('Sell out')]),
           {**ejes(), **leyenda(), **etiquetas(), **colores_cadena()},
           contenedor('Sell out por familia y cadena', 'Mes elegido')),
    tabla('mtxProductos', (16, 472, 740, 232), None, 'Sell out por producto', 'Mes elegido · crecimiento contra los mismos días del año anterior',
          orden=[(ref_medida('Sell out monto'), 'Descending')], vtype='pivotTable',
          Rows=[campo_col('dimProducto', 'Producto')],
          Values=[campo_medida('Sell out piezas', 'Piezas'), campo_medida('Sell out piezas año anterior', 'Piezas año ant.'),
                  campo_medida('Crecimiento sell out piezas', 'Crec. piezas'), campo_medida('Sell out monto', 'Monto'),
                  campo_medida('Crecimiento sell out monto', 'Crec. monto'), campo_medida('Participación sell out monto', 'Part. monto')]),
    visual('chrDiario', (768, 472, 496, 232), 'lineChart',
           consulta([(ref_col('Calendario', 'Fecha'), 'Ascending')], Category=[campo_col('Calendario', 'Fecha', 'Día')], Y=[campo_medida('Sell out')]),
           {**ejes(), **leyenda(False), "dataPoint": [color_medida('Sell out', AZUL_WM)],
            "lineStyles": props(strokeWidth=L('2D'), showMarker=L('true'))},
           contenedor('Sell out diario de Walmart', 'Mes elegido · Amazon solo reporta por mes'),
           filtros=[filtro_valores('fSoloWalmartDiario', 'dimCadena', 'Cadena', ['Walmart'])]),
]
paginas['sellout'] = ('Sell out', v_sellout, [('sltMes', 'chrMensual')], None)

# ================= Inventario
_z[0] = 0
v_inv = encabezado('Texto datos inventario') + [
    seg_cadena((16, 74, 180, 50)),
    seg_familia((206, 74, 220, 50)),
    seg_producto((436, 74, 330, 50)),
] + kpis([('kpiInventario', 'Inventario piezas', 'Inventario (piezas)'),
          ('kpiVentaProm', 'Venta promedio mensual piezas', 'Venta prom. mensual (piezas)'),
          ('kpiCobertura', 'Cobertura meses', 'Cobertura (meses)'),
          ('kpiRiesgo', 'Productos en riesgo de quiebre', 'Riesgo de quiebre (productos)'),
          ('kpiSinInv', 'Productos sin inventario', 'Sin inventario (productos)'),
          ('kpiSobre', 'Productos con sobre stock', 'Sobre stock (productos)')]) + [
    tabla('tblInventario', (16, 224, 700, 480),
          [campo_col('dimCadena', 'Cadena'), campo_col('dimProducto', 'Producto'),
           campo_medida('Inventario piezas', 'Inventario (piezas)'), campo_medida('Venta promedio mensual piezas', 'Venta prom. mensual'),
           campo_medida('Cobertura meses', 'Cobertura (meses)'), campo_medida('Clasificación cobertura', 'Estado')],
          'Inventario y cobertura por producto',
          'Cobertura = inventario ÷ venta promedio de los últimos 3 meses cerrados · 🔴 menos de 1 mes · 🟢 de 1 a 3 · 🟡 más de 3',
          orden=[(ref_col('dimCadena', 'Cadena'), 'Ascending'), (ref_medida('Cobertura meses'), 'Ascending')]),
    visual('chrInvMes', (728, 224, 536, 234), 'clusteredColumnChart',
           consulta(ORDEN_MES, Category=[MES], Series=[campo_col('dimCadena', 'Cadena')], Y=[campo_medida('Inventario piezas', 'Inventario')]),
           {**ejes(), **leyenda(), **etiquetas(), **colores_cadena()},
           contenedor('Inventario al cierre de cada mes', 'Última foto de cada mes, en piezas · últimos 12 meses'),
           filtros=ULT12('fUlt12Inv')),
    tabla('tblSinInventario', (728, 470, 536, 234),
          [campo_col('dimTienda', 'Tienda_etiqueta', 'Tienda'), campo_col('dimTienda', 'Ciudad'), campo_col('dimProducto', 'Producto'),
           campo_medida('Venta 28 días Walmart', 'Venta 28 días')],
          'Tiendas de Walmart sin inventario que sí venden', 'Vendieron en los últimos 28 días y hoy tienen 0 piezas',
          orden=[(ref_medida('Venta 28 días Walmart'), 'Descending')],
          filtros=[filtro_medida_igual('fAlertaSinInv', 'Alerta tienda sin inventario', 1)]),
]
paginas['inventario'] = ('Inventario', v_inv, [], None)

# ================= Abasto (Walmart)
_z[0] = 0
v_abasto = encabezado('Texto datos abasto') + [
    segmentacion('sltMesOrden', (16, 74, 180, 50), 'Calendario', 'Periodo', 'Mes de la orden', descendente=True,
                 filtros=[filtro_meses('fMesesOrden', 0, 23)]),
    seg_familia((206, 74, 220, 50)),
    seg_producto((436, 74, 330, 50)),
] + kpis([('kpiFillRate', 'Fill rate', 'Fill rate'),
          ('kpiOrdenadas', 'Piezas ordenadas', 'Piezas ordenadas'),
          ('kpiRecibidas', 'Piezas recibidas', 'Piezas recibidas'),
          ('kpiNoSurtidas', 'Piezas no surtidas', 'Piezas no surtidas'),
          ('kpiRecshipPzas', 'Pronóstico piezas', 'Pedidos planeados (piezas)'),
          ('kpiRecshipMonto', 'Pronóstico monto', 'Pedidos planeados (MXN)')]) + [
    visual('chrFillRate', (16, 224, 620, 234), 'clusteredColumnChart',
           consulta(ORDEN_MES, Category=[MES], Y=[campo_medida('Fill rate')]),
           {**ejes(), **leyenda(False), **etiquetas(), "dataPoint": [color_medida('Fill rate', AZUL_WM)]},
           contenedor('Fill rate por mes de la orden', 'Walmart · piezas recibidas ÷ piezas ordenadas · últimos 12 meses'),
           filtros=ULT12('fUlt12FillRate')),
    tabla('tblFillRate', (16, 470, 620, 234),
          [campo_col('dimProducto', 'Producto'), campo_medida('Piezas ordenadas', 'Ordenadas'), campo_medida('Piezas recibidas', 'Recibidas'),
           campo_medida('Piezas no surtidas', 'No surtidas'), campo_medida('Fill rate')],
          'Fill rate por producto', 'Órdenes del mes elegido (todas si no eliges ninguno)',
          orden=[(ref_medida('Piezas no surtidas'), 'Descending')]),
    visual('chrRecship', (648, 224, 616, 234), 'clusteredColumnChart',
           consulta([(ref_col('Calendario', 'Fecha'), 'Ascending')], Category=[campo_col('Calendario', 'Fecha', 'Fecha de pedido')],
                    Y=[campo_medida('Pronóstico piezas', 'Piezas')]),
           {**ejes(True), **leyenda(False), **etiquetas(), "dataPoint": [color_medida('Pronóstico piezas', AZUL_WM)]},
           contenedor('Pedidos planeados por Walmart (Recship)', 'Piezas por fecha de pedido planeada · Recship más reciente')),
    tabla('tblRecship', (648, 470, 616, 234),
          [campo_col('fRecship', 'CEDIS'), campo_col('dimProducto', 'Producto'), campo_col('fRecship', 'Fecha_pedido', 'Pedido'),
           campo_col('fRecship', 'Fecha_recepcion', 'Recepción'), campo_medida('Pronóstico piezas', 'Piezas'), campo_medida('Pronóstico monto', 'Monto')],
          'Detalle de los pedidos planeados', 'Por centro de distribución (CEDIS)',
          orden=[(ref_col('fRecship', 'Fecha_pedido'), 'Ascending')]),
]
_sin_mes = ['kpiRecshipPzas', 'kpiRecshipMonto', 'chrRecship', 'tblRecship', 'chrFillRate']
paginas['abasto'] = ('Abasto', v_abasto, [('sltMesOrden', t) for t in _sin_mes], None)

# ================= Control
_z[0] = 0
v_control = encabezado('Texto datos sell out') + [
    tarjeta('crdEstado', (16, 76, 400, 86), 'Estado del reporte', 'Estado del reporte', 14),
    tarjeta('crdWMSO', (428, 76, 200, 86), 'Datos al - sell out Walmart', 'Sell out Walmart al', unidades=False),
    tarjeta('crdAMZSO', (640, 76, 200, 86), 'Datos al - sell out Amazon', 'Sell out Amazon al', unidades=False),
    tarjeta('crdWMInv', (852, 76, 200, 86), 'Datos al - inventario Walmart', 'Inventario Walmart al', unidades=False),
    tarjeta('crdAMZInv', (1064, 76, 200, 86), 'Datos al - inventario Amazon', 'Inventario Amazon al', unidades=False),
    tarjeta('crdDiasWM', (16, 174, 190, 86), 'Días sin sell out Walmart', 'Días sin sell out Walmart'),
    tarjeta('crdFilasSH', (218, 174, 190, 86), 'Filas sin homologar', 'Filas sin homologar'),
    tarjeta('crdMesesAMZ', (420, 174, 450, 86), 'Meses faltantes Amazon', 'Meses de Amazon por descargar', 11, ajustar=True),
    tarjeta('crdCodSH', (882, 174, 382, 86), 'Códigos sin homologar', 'Códigos sin homologar', 11, ajustar=True),
    tabla('tblArchivos', (16, 272, 1248, 432),
          [campo_col('ctlArchivos', 'Fuente'), campo_col('ctlArchivos', 'Archivo'), campo_col('ctlArchivos', 'Reporte'),
           campo_col('ctlArchivos', 'Desde'), campo_col('ctlArchivos', 'Hasta'), campo_col('ctlArchivos', 'Generado'),
           campo_col('ctlArchivos', 'Usado')],
          'Archivos leídos', 'Cada día se toma del archivo más reciente · los que dicen «No» pueden pasar a la subcarpeta Respaldo'),
]
paginas['control'] = ('Control', v_control, [], None)

# ================= Revisión de datos (oculta: solo para comprobar cifras en Power BI Desktop)
_z[0] = 0
v_revision = encabezado('Texto datos sell out') + [
    tabla('mtxSellOut', (16, 76, 624, 628), None, 'Sell out por producto y cadena', vtype='pivotTable',
          Rows=[campo_col('dimProducto', 'Producto')], Columns=[campo_col('dimCadena', 'Cadena')],
          Values=[campo_medida('Sell out piezas', 'Piezas'), campo_medida('Sell out monto', 'Monto')]),
    tabla('mtxInventario', (652, 76, 612, 628), None, 'Inventario y cobertura por producto y cadena', vtype='pivotTable',
          Rows=[campo_col('dimProducto', 'Producto')], Columns=[campo_col('dimCadena', 'Cadena')],
          Values=[campo_medida('Inventario piezas', 'Inventario'), campo_medida('Cobertura meses', 'Cobertura'),
                  campo_medida('Clasificación cobertura', 'Estado')]),
]
paginas['revision'] = ('Revisión de datos', v_revision, [], 'HiddenInViewMode')

for pid, (titulo_p, visuales, sin_filtro, visibilidad) in paginas.items():
    pg = {"$schema": PAGE_SCHEMA, "name": pid, "displayName": titulo_p, "displayOption": "FitToPage", "height": 720, "width": 1280,
          "objects": {"background": props(color=C(FONDO), transparency=L('0D')), "outspace": props(color=C(FONDO), transparency=L('0D'))}}
    if visibilidad:
        pg["visibility"] = visibilidad
    if sin_filtro:
        pg["visualInteractions"] = [{"source": a, "target": b, "type": "NoFilter"} for a, b in sin_filtro]
    jdump(f'{RP}/definition/pages/{pid}/page.json', pg)
    nombres = [v["name"] for v in visuales]
    assert len(nombres) == len(set(nombres)), pid
    for a, b in sin_filtro:
        assert a in nombres and b in nombres, (pid, a, b)
    for v in visuales:
        jdump(f'{RP}/definition/pages/{pid}/visuals/{v["name"]}/visual.json', v)
jdump(f'{RP}/definition/pages/pages.json', {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
      "pageOrder": list(paginas.keys()), "activePageName": "sellout"})
print('listo')
