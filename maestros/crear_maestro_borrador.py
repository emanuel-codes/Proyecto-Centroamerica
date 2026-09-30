import pandas as pd, openpyxl, warnings, datetime as dt
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
warnings.filterwarnings('ignore')
D='/tmp/claude-0/-home-user-Proyectos-Power-BI/69a65daa-6b0c-5b13-b1ac-f9fc6d488713/scratchpad/pbix/data/'
R='/home/user/proyecto-centroamerica/'
L=lambda t: pd.read_pickle(D+t+'.pkl')

def gtin_ok(s):
    s=str(s)
    if not (s.isdigit() and len(s)==13): return False
    tot=sum(int(x)*(1 if i%2==0 else 3) for i,x in enumerate(s[:12])); return (10-tot%10)%10==int(s[12])
def ean_desde_walmart(u):
    s=str(u).strip().lstrip('0')
    if len(s)!=12 or not s.isdigit(): return None
    tot=sum(int(x)*(1 if i%2==0 else 3) for i,x in enumerate(s)); return s+str((10-tot%10)%10)

# --- fuentes
wb=openpyxl.load_workbook(R+'Sell in/BD Sell In.xlsx', data_only=True)
def tab(ws, ref):
    rows=list(ws[ref]); h=[c.value for c in rows[0]]; return pd.DataFrame([[c.value for c in r] for r in rows[1:]], columns=h)
cat=tab(wb['Catalogo de Productos'],'A1:I35')
csi=tab(wb['Productos_Sell_In'],'A1:B49')
ccl=tab(wb['Catalogo Clientes'],'A1:C29')
met=tab(wb['Venta Objetivo'],'A1:G1320')
k=L('InventarioKardex'); aux=L('Inventario Auxiliar')
erp=pd.concat([k[['CodArticulo','Descripcion']].rename(columns={'CodArticulo':'cod','Descripcion':'nom'}),
               aux[['Código Pro.','Producto']].rename(columns={'Código Pro.':'cod','Producto':'nom'})]).dropna().drop_duplicates('cod')
erp_cat=dict(zip(aux['Código Pro.'],aux['Categoría']))
erp_nom=dict(zip(erp['cod'],erp['nom']))

# nombre del catálogo -> código ERP (revisado a mano)
cat2erp={
 'Báscula Digital de Vidrio Antideslizante':'13972','Báscula Digital de Vidrio Marmol':'13971','Báscula Digital de Vidrio Transparente':'13667',
 'Cojin Cuadrad Memory Foam':'14584','Inodoro Portatil con tapa y brazo':'13648','Nebulizador Adulto Compacto':'14806',
 'Nebulizador Adulto Moderno NBA-10WA':'F13644','Nebulizador Adulto Moderno Tapa Azul':'13644','Nebulizador Adulto Walmart':'14660',
 'Nebulizador Pediatrico Buho Blanco':'F13789','Nebulizador Pediatrico Buho Celeste':'F13791','Nebulizador Pediatrico Buho Rosado':'F13790',
 'Nebulizador Pediatrico Elefante Celeste':'13471','Nebulizador Pediatrico Elefante Rosa':'13470',
 'Pack Tarjetas Aromatizantes con Frases Motivacionales':'JH0006','Pack Tarjetas Aromatizantes con Frases Religiosas':'JH0005',
 'Pack Tarjetas Aromatizantes con Imagenes Religiosas':'JH0004','Prueba de Embarazo Wellpro Response Tipo Lápiz':'F09515',
 'Silla de Baño con Respaldo':'12993','Silla de Ruedas STD':'12982','Tarjeta Aromatizante con Frases Motivacionales':'JH0002',
 'Tarjeta Aromatizante con Frases Religiosas':'JH0003','Tarjeta Aromatizante con Imágenes Religiosas':'JH0001',
 'Termómetro Pediatrico Cute Animals Cerdito':'F13592','Termómetro Pediatrico Cute Animals Koala':'13594',
 'Termómetro Pediatrico Cute Animals Osito':'13593','Termómetro Pediatrico Cute Animals Panda':'13595',
 'Termómetro Pediatrico Cute Animals Ranita':'13597','Kit de Nebulización Adulto':'13259','Kit de Nebulización Pediátrico':'13260',
 'Nebulizador Pediátrico Penguin':'F00080',
}
sin_codigo={'Nebulizador Adulto Moderno Tapa Verde':'Sin código ERP. ¿Es el mismo producto que NBA-10WA (F13644)? En Amazon tiene el ASIN B0FPHCD4K3, y NBA-10WA tiene «BOFPHCD4K3» (con letra O).',
            'Nebulizador Pediatrico Animalitos':'Sin código ERP ni ventas. ¿Existe? ¿Es alguno de Kitty (F00073) o Panda (F52237)?'}
fake_asin=lambda a: (a is None) or (not str(a).startswith('B0')) or len(str(a))!=10
fam_marca=lambda n: 'Saint Ciel' if 'Tarjeta' in n else 'Wellpro'

prod=[]; vistos=set()
for _,r in cat.iterrows():
    n=r['Nombre de Producto']; cod=cat2erp.get(n)
    if cod in vistos:   # fila duplicada del Osito
        continue
    notas=[]; estado='OK'
    ean=str(r['UPC']) if r['UPC'] is not None else None
    asin=r['ASIN']
    if n in sin_codigo: notas.append(sin_codigo[n]); estado='Validar'
    if ean and not gtin_ok(ean): notas.append(f'EAN {ean} inválido (dígito verificador o provisional): confirmar el real.'); estado='Validar'
    if asin and fake_asin(asin):
        notas.append(f'ASIN «{asin}» no es real' + (' (letra O en vez de cero)' if str(asin).startswith('BO') else '') + '. Dejar vacío si no se vende en Amazon.'); estado='Validar'; asin=None
    if n=='Nebulizador Pediátrico Penguin': notas.append('El ASIN B0H356Y44X se parece mucho al del kit pediátrico (B0H356Y44V): confirmar que es real.')
    if n=='Termómetro Pediatrico Cute Animals Osito': notas.append('En el catálogo actual estaba dos veces; se dejó una sola fila (EAN 7431009207481).')
    if n in ('Tarjeta Aromatizante con Frases Motivacionales','Tarjeta Aromatizante con Frases Religiosas'): notas.append('En Productos_Sell_In estaba apuntando al EAN del Pack; corregido.')
    prod.append(dict(Codigo_ERP=cod, Producto=n, Nombre_ERP=erp_nom.get(cod), Familia=r['Familias'], Categoria_ERP=erp_cat.get(cod), Marca=fam_marca(n),
                     EAN=ean, ASIN=asin, Item_Walmart=None, Modelo=r['Modelo'], Costo_CIF=r['Costo CIF'], Lead_time_meses=r['Lead Time (meses)'],
                     Stock_seguridad=r['Stock Seguridad'], Demanda_prom_mensual=r['Demanda Prom (mensual)'], Activo='Sí', Estado=estado, Notas=' '.join(notas)))
    if cod: vistos.add(cod)
# productos del ERP que no están en el catálogo
extra={'F00073':('NEBULIZADORES','Nuevo en el ERP; falta EAN, ASIN y familia.'),'F52237':('NEBULIZADORES','Nuevo en el ERP; falta EAN, ASIN y familia.'),
       'JH0007':('AROMATIZANTES','En el ERP y en el inventario de Amazon (ASIN B0FCPW6FFL); falta en el catálogo. Confirmar EAN.'),
       'JHPM0001':(None,'Material promocional. ¿Se excluye del reporte?'),'JHPM0002':(None,'Material promocional. ¿Se excluye del reporte?'),
       '125536':(None,'Promocional Saint Ciel. ¿Se excluye del reporte?'),'125537':(None,'Promocional Saint Ciel. ¿Se excluye del reporte?'),'125538':(None,'Promocional Saint Ciel. ¿Se excluye del reporte?'),
       'PRUEBA':(None,'Código duplicado en el kardex para la prueba de embarazo (el correcto parece F09515). Confirmar con sistemas.')}
for cod,(fam,nota) in extra.items():
    prod.append(dict(Codigo_ERP=cod, Producto=erp_nom.get(cod), Nombre_ERP=erp_nom.get(cod), Familia=fam, Categoria_ERP=erp_cat.get(cod), Marca=('Saint Ciel' if cod.startswith(('JH','125')) else 'Wellpro'),
                     EAN=None, ASIN=('B0FCPW6FFL' if cod=='JH0007' else None), Item_Walmart=None, Modelo=None, Costo_CIF=None, Lead_time_meses=None, Stock_seguridad=None, Demanda_prom_mensual=None,
                     Activo=('No' if cod.startswith(('JHPM','125')) or cod=='PRUEBA' else 'Sí'), Estado='Validar', Notas=nota))
P=pd.DataFrame(prod)
# Walmart: Item Nbr por código ERP (Vendor Stk Nbr) y por EAN
so=L('Sell_Out_WM')
wm=so.groupby('Item Nbr').agg(vendor=('Vendor Stk Nbr','first'), desc=('Signing Desc','first')).reset_index()
wm_upc={'101248318':'0743400255002','101248319':'0743400255149','101248322':'0743100920749','101248323':'0743100920750','101618069':'0743100920748'}
ean2cod=dict(zip(P['EAN'],P['Codigo_ERP']))
eq=[]
for _,r in wm.iterrows():
    item=str(r['Item Nbr']); upc=wm_upc[item]; ean=ean_desde_walmart(upc)
    cod=str(int(r['vendor'])) if pd.notna(r['vendor']) else ean2cod.get(ean)
    via='Vendor Stk Nbr' if pd.notna(r['vendor']) else 'EAN calculado del UPC'
    P.loc[P['Codigo_ERP']==cod,'Item_Walmart']=item
    eq.append(dict(Cadena='Walmart', Codigo_en_cadena=item, Tipo_codigo='Item Nbr', Codigo_ERP=cod, Descripcion_en_cadena=r['desc'], Factor_piezas=1, Estado='OK', Notas=f'Asignado por {via}.'))
    eq.append(dict(Cadena='Walmart', Codigo_en_cadena=upc, Tipo_codigo='UPC Retail Link', Codigo_ERP=cod, Descripcion_en_cadena=r['desc'], Factor_piezas=1, Estado='OK', Notas=f'EAN equivalente: {ean} (se quita el 0 y se agrega el dígito verificador).'))
# Amazon
va=L('Ventas Amazon'); ia=L('Inventario Amazon')
tit=pd.concat([va[['ASIN','Nombre del Producto','Fecha']].rename(columns={'Nombre del Producto':'t'}), ia[['ASIN','Título del Producto','Fecha']].rename(columns={'Título del Producto':'t'})]).dropna(subset=['ASIN']).sort_values('Fecha').groupby('ASIN')['t'].last()
asin2cod=dict(zip(P['ASIN'],P['Codigo_ERP']))
for a,t in tit.items():
    cod=asin2cod.get(a); est='OK'; nota=''
    if a=='B0FPHCD4K3': est='Validar'; nota='Producto «Tapa Verde» sin código ERP (ver Productos).'
    if cod is None and a!='B0FPHCD4K3': est='Validar'; nota='ASIN sin producto en el maestro.'
    eq.append(dict(Cadena='Amazon', Codigo_en_cadena=a, Tipo_codigo='ASIN', Codigo_ERP=cod, Descripcion_en_cadena=t, Factor_piezas=1, Estado=est, Notas=nota))
# ERP: nombres de la exportación de sell in (transitorio, hasta que traiga el código)
cod_por_ean=dict(zip(P['EAN'],P['Codigo_ERP']))
fix_nombres={'Tarjeta Aromatizante con Frases Motivacionales':'JH0002','Tarjeta Aromatizante con Frases Religiosas':'JH0003','Tarjetas Aromatizantes con Imagenes Religiosas':'JH0004',
             'Termómetro Pediatrico Cute Animals Osito':'13593','Nebulizador Pediátrico Penguin':'F00080'}
for _,r in csi.drop_duplicates('Producto').iterrows():
    n=r['Producto']; cod=fix_nombres.get(n) or cod_por_ean.get(str(r['UPC'])); nota=''
    if n in fix_nombres and n.startswith('Tarjeta A'): nota='Antes apuntaba al Pack; corregido a la tarjeta individual.'
    if n=='Tarjetas Aromatizantes con Imagenes Religiosas': nota='Nombre del ERP para el Pack (JH0004). Confirmar.'
    eq.append(dict(Cadena='ERP (nombre)', Codigo_en_cadena=n, Tipo_codigo='Nombre en exportación de sell in', Codigo_ERP=cod, Descripcion_en_cadena=n, Factor_piezas=1,
                   Estado='OK' if cod else 'Validar', Notas=(nota+' Transitorio: se elimina cuando la exportación traiga el código.').strip()))
E=pd.DataFrame(eq)
# Clientes
cli=[]
reglas={'NUEVA WAL MART DE MEXICO':'WALMART','WALMART EN LINEA':'WALMART MARKETPLACE','PUBLICO EN GENERAL':'MARKET PLACE','SERVICIOS COMERCIALES AMAZON MEXICO':'AMAZON',
        'COPPEL EN LINEA':'COPPEL MARKETPLACE','FARMA SANA SANA':'FARMACIA SANA SANA','CLAUDIA LEMOINE GOMEZ':'MERCADO LIBRE',
        'INSTITUTO DE SEGURIDAD Y SERVICIOS SOCIALES DE LOS TRABAJADORES DEL ESTADO':'MERCADO LIBRE','PHARMA PLUS':'FARMACIA SAN PABLO'}
catcli=dict(zip(ccl['Clientes'],ccl['Categoría 2']))
for n,c in catcli.items():
    if n in ('PUBLICO EN GENERAL','PHARMA PLUS'): continue
    cli.append(dict(Cliente_ERP=n, Cliente_reporte=n, Categoria=c, Cadena_sell_out={'WALMART':'Walmart','AMAZON':'Amazon'}.get(n), Estado='OK', Notas=''))
val={'INSTITUTO DE SEGURIDAD Y SERVICIOS SOCIALES DE LOS TRABAJADORES DEL ESTADO':'El ISSSTE es una institución de gobierno: ¿de verdad se agrupa como Mercado Libre?',
     'PHARMA PLUS':'¿Pharma Plus se reporta como Farmacia San Pablo?','PUBLICO EN GENERAL':'¿Público en general se reporta como Market Place?','CLAUDIA LEMOINE GOMEZ':'¿Esta persona vende por Mercado Libre?'}
for n,dest in reglas.items():
    cli.append(dict(Cliente_ERP=n, Cliente_reporte=dest, Categoria=catcli.get(dest), Cadena_sell_out={'WALMART':'Walmart','AMAZON':'Amazon'}.get(dest),
                    Estado='Validar' if n in val else 'OK', Notas=val.get(n,'Regla que hoy está escrita dentro de la consulta de Power Query.')))
C=pd.DataFrame(cli)
# Metas (sin duplicados; producto por código; cliente normalizado)
m=met.copy()
m['Mes']=pd.to_datetime(m['Fecha']).dt.to_period('M').dt.to_timestamp().dt.date
m['Codigo_ERP']=m['Nombre Producto'].map(cat2erp)
norm={'WALMART':'WALMART','WALMAR MARKETPLACE':'WALMART MARKETPLACE'}
m['Cliente_reporte']=m['Cliente'].str.upper().str.strip().map(lambda x: norm.get(x,x))
M=m[['Mes','Codigo_ERP','Nombre Producto','Cliente_reporte','Cantidad Vendida','Precio de Venta','Total de Venta']].rename(columns={'Nombre Producto':'Producto','Cantidad Vendida':'Cantidad','Precio de Venta':'Precio','Total de Venta':'Monto'})
assert set(M.loc[M['Codigo_ERP'].isna(),'Producto'])<= {'Nebulizador Pediatrico Animalitos'}
M['Estado']=['Validar' if pd.isna(c) or cl=='WALMART MARKETPLACE' and orig=='WALMAR MARKETPLACE' else 'OK' for c,cl,orig in zip(M['Codigo_ERP'],M['Cliente_reporte'],m['Cliente'].str.upper().str.strip())]
M['Notas']=['Producto sin código ERP (ver Productos).' if pd.isna(c) else ('Cliente venía como «Walmar Marketplace».' if orig=='WALMAR MARKETPLACE' else '') for c,orig in zip(M['Codigo_ERP'],m['Cliente'].str.upper().str.strip())]
# Tipo de cambio
T=pd.DataFrame({'Mes':pd.period_range('2024-01','2026-12',freq='M').to_timestamp().date,'TC_MXN_por_USD':None,'Fuente':None})
# Pendientes
pend=[
 ('Productos','Confirmar el nombre oficial de cada producto para el reporte (columna Producto).','Cliente'),
 ('Productos','«Nebulizador Adulto Moderno Tapa Verde»: ¿es el NBA-10WA (F13644)? Tiene EAN inválido.','Cliente'),
 ('Productos','«Nebulizador Pediatrico Animalitos»: sin código ERP ni ventas, pero tiene metas (4 filas). ¿Existe?','Cliente'),
 ('Productos','EAN y ASIN reales de los productos marcados «Validar» (provisionales 7770000000053/54/55, 7434002550000, 7743100920748).','Cliente'),
 ('Productos','Nuevos en el ERP sin catálogo: Nebulizador Kitty (F00073), Nebulizador Panda (F52237), Pack Mix Religioso (JH0007).','Cliente'),
 ('Productos','Material promocional (JHPM0001, JHPM0002, 125536–125538): ¿se excluye del reporte?','Cliente'),
 ('Productos','Código «PRUEBA» en el kardex: ¿es la misma prueba de embarazo que F09515?','Sistemas'),
 ('Clientes','Reglas de agrupación: ISSSTE → Mercado Libre, Claudia Lemoine → Mercado Libre, Pharma Plus → Farmacia San Pablo, Público en general → Market Place.','Cliente'),
 ('Metas','60 filas de 2025 tenían el cliente «Walmar Marketplace» (sin t); se corrigió a WALMART MARKETPLACE. Confirmar.','Cliente'),
 ('Metas','Confirmar que las metas de 2026 están completas y vigentes (se tomaron del Excel de sell in).','Cliente'),
 ('Tipo de cambio','Definir qué tipo de cambio usar por mes (por ejemplo, el promedio mensual FIX de Banxico) y llenar la hoja TipoCambio. Hoy el reporte usa 20 fijo.','Cliente'),
 ('ERP','Pedir que la exportación de sell in traiga el código de producto; con eso se elimina la tabla transitoria de nombres.','Sistemas'),
]
PE=pd.DataFrame(pend, columns=['Tema','Pendiente','Quién valida']); PE.insert(0,'N',range(1,len(PE)+1))

# --- escribir Excel
out=R+'maestros/Maestro_Wellpro_borrador.xlsx'
with pd.ExcelWriter(out, engine='openpyxl') as w:
    pd.DataFrame({'x':[]}).to_excel(w, sheet_name='LEEME', index=False)
    for name,df in [('Productos',P),('Equivalencias',E),('Clientes',C),('Metas',M),('TipoCambio',T),('Pendientes',PE)]:
        df.to_excel(w, sheet_name=name, index=False)
wb=openpyxl.load_workbook(out)
hdr_fill=PatternFill('solid', fgColor='C00000'); warn=PatternFill('solid', fgColor='FFF2CC')
tnames={'Productos':'tProductos','Equivalencias':'tEquivalencias','Clientes':'tClientes','Metas':'tMetas','TipoCambio':'tTipoCambio','Pendientes':'tPendientes'}
for ws in wb.worksheets:
    if ws.title=='LEEME': continue
    ref=f"A1:{get_column_letter(ws.max_column)}{max(ws.max_row,2)}"
    t=Table(displayName=tnames[ws.title], ref=ref); t.tableStyleInfo=TableStyleInfo(name='TableStyleMedium2', showRowStripes=True); ws.add_table(t)
    ws.freeze_panes='A2'
    for c in ws[1]: c.font=Font(bold=True, color='FFFFFF'); c.fill=hdr_fill; c.alignment=Alignment(vertical='center', wrap_text=True)
    for i,col in enumerate(ws.columns,1):
        width=max(len(str(c.value)) if c.value is not None else 0 for c in col)
        ws.column_dimensions[get_column_letter(i)].width=min(max(10,width+2),60)
    heads=[c.value for c in ws[1]]
    if 'Estado' in heads:
        j=heads.index('Estado')+1
        for row in ws.iter_rows(min_row=2):
            if row[j-1].value=='Validar':
                for c in row: c.fill=warn
    for col in ('Notas','Pendiente'):
        if col in heads:
            j=heads.index(col)+1
            ws.column_dimensions[get_column_letter(j)].width=80
            for row in ws.iter_rows(min_row=2): row[j-1].alignment=Alignment(wrap_text=True, vertical='top')
    if 'Mes' in heads:
        j=heads.index('Mes')+1
        for row in ws.iter_rows(min_row=2): row[j-1].number_format='yyyy-mm'
ws=wb['LEEME']; ws.delete_rows(1,2)
lineas=[('Maestro Wellpro (BORRADOR)',True),('',False),
 ('Único lugar donde se mantienen productos, códigos, clientes, metas y tipo de cambio. El reporte lee estas tablas; no se edita nada en Power BI.',False),('',False),
 ('Hojas',True),
 ('Productos: una fila por producto. La llave es el código del ERP (Codigo_ERP).',False),
 ('Equivalencias: traduce los códigos de cada cadena (ASIN de Amazon, artículo y UPC de Walmart, nombres del ERP) al código del ERP.',False),
 ('Clientes: traduce el nombre del cliente del ERP al cliente y la categoría del reporte.',False),
 ('Metas: meta mensual por producto y cliente (Mes = primer día del mes).',False),
 ('TipoCambio: tipo de cambio por mes (pesos por dólar). Falta llenarlo.',False),
 ('Pendientes: lo que hay que validar con el cliente o con sistemas.',False),('',False),
 ('Reglas',True),
 ('1. Las filas en amarillo (Estado = Validar) tienen algo por confirmar; la columna Notas explica qué.',False),
 ('2. Un producto nuevo se agrega una sola vez en Productos, y sus códigos en Equivalencias.',False),
 ('3. No se cambia el nombre de las tablas (tProductos, tEquivalencias, etc.) ni de las columnas: el reporte las busca por nombre.',False),
 ('4. Este borrador se armó con el catálogo, el kardex y los datos del reporte actual (30/09/2026).',False)]
for i,(txt,bold) in enumerate(lineas,1):
    c=ws.cell(i,1,txt); c.font=Font(bold=bold, size=14 if i==1 else 11)
ws.column_dimensions['A'].width=130
wb.move_sheet('LEEME', offset=-wb.index(wb['LEEME']))
wb.save(out)
print('Productos', len(P), 'validar', (P.Estado=='Validar').sum()); print('Equivalencias', len(E), E.groupby('Cadena').size().to_dict(), 'validar', (E.Estado=='Validar').sum())
print('Clientes', len(C), 'Metas', len(M), 'monto', round(M['Monto'].sum()), 'Pendientes', len(PE))
print(P[['Codigo_ERP','Producto','EAN','ASIN','Item_Walmart','Estado']].to_string())
