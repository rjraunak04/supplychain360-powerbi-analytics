import os, json, hashlib, shutil, re, zipfile, glob

ROOT='/mnt/data/final_work/SupplyChain360'
REPORT=os.path.join(ROOT,'SupplyChain360.Report','definition','pages')
MEAS=os.path.join(ROOT,'SupplyChain360.SemanticModel','definition','tables','_Measures.tmdl')
SCHEMA_VISUAL='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json'
SCHEMA_PAGE='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json'

def uid(seed): return hashlib.md5(seed.encode()).hexdigest()[:20]
def lit(v): return {'expr':{'Literal':{'Value':v}}}
def solid(c): return {'solid':{'color':{'expr':{'Literal':{'Value':f"'{c}'"}}}}}
def col(t,c,n=None):
    return {'field':{'Column':{'Expression':{'SourceRef':{'Entity':t}},'Property':c}},'queryRef':f'{t}.{c}','nativeQueryRef':n or c}
def measure(t,m,n=None):
    return {'field':{'Measure':{'Expression':{'SourceRef':{'Entity':t}},'Property':m}},'queryRef':f'{t}.{m}','nativeQueryRef':n or m}
def visual(name,x,y,w,h,vtype,qs=None,objects=None,vc=None,z=1000,tab=3000):
    d={'$schema':SCHEMA_VISUAL,'name':uid(name),'position':{'x':x,'y':y,'z':z,'height':h,'width':w,'tabOrder':tab},'visual':{'visualType':vtype,'drillFilterOtherVisuals':True}}
    if qs: d['visual']['query']={'queryState':qs}
    if objects: d['visual']['objects']=objects
    if vc: d['visual']['visualContainerObjects']=vc
    return d

def title_box(name,x,y,w,h,text,size=14,bg='#1E293B',z=9000,tab=1000):
    return visual(name,x,y,w,h,'textbox',objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':text,'textStyle':{'fontFamily':'Segoe UI Semibold','fontSize':f'{size}px','color':'#FFFFFF'}}]}]}}]},vc={'visualHeader':[{'properties':{'show':lit('false')}}],'background':[{'properties':{'show':lit('true'),'color':solid(bg),'transparency':lit('0D')}}]},z=z,tab=tab)

def subtitle(name,x,y,w,h,text):
    # white background, gray text
    return visual(name,x,y,w,h,'textbox',objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':text,'textStyle':{'fontFamily':'Segoe UI','fontSize':'10px','color':'#64748B'}}]}]}}]},vc={'visualHeader':[{'properties':{'show':lit('false')}}]},z=8500,tab=1000)

def card_obj():
    return {'layout':[{'properties':{'style':lit("'Table'"),'orientation':lit('1D'),'rowCount':lit('5L'),'contentOrder':lit("'referenceLabel_callout_image'")}}, {'properties':{'rectangleRoundedCurve':lit('10L'),'paddingUniform':lit('10L'),'backgroundTransparency':lit('0D')},'selector':{'id':'default'}}], 'accentBar':[{'properties':{'show':lit('true')},'selector':{'id':'default'}}], 'shadowCustom':[{'properties':{'show':lit('true')},'selector':{'id':'default'}}], 'shapeCustomRectangle':[{'properties':{'tileShape':lit("'rectangleRoundedByPixel'")},'selector':{'id':'default'}}]}

def card(name,x,y,w,h,m,tab): return visual(name,x,y,w,h,'cardVisual',{'Data':{'projections':[measure('_Measures',m)]}},card_obj(),tab=tab)
def slicer(name,x,y,w,h,t,c,n,tab): return visual(name,x,y,w,h,'slicer',{'Values':{'projections':[col(t,c,n)]}},tab=tab,z=1500)
def chart_obj(labels=False):
    o={'categoryAxis':[{'properties':{'fontSize':lit('10L'),'showAxisTitle':lit('false')}}], 'valueAxis':[{'properties':{'fontSize':lit('10L'),'showAxisTitle':lit('false'),'gridlineStyle':lit("'dashed'"),'gridlineColor':solid('#E2E8F0')}}]}
    if labels:o['labels']=[{'properties':{'show':lit('true'),'fontSize':lit('9L')}}]
    return o

def bar(name,x,y,w,h,ct,cc,mt,mm,catname=None,measname=None,tab=3000):
    qs={'Category':{'projections':[col(ct,cc,catname)]},'Y':{'projections':[measure(mt,mm,measname)]}}
    qs['sortDefinition']={'sort':[{'field':{'Measure':{'Expression':{'SourceRef':{'Entity':mt}},'Property':mm}},'direction':'Descending'}],'isDefaultSort':True}
    return visual(name,x,y,w,h,'clusteredBarChart',qs,chart_obj(True),tab=tab)
def line(name,x,y,w,h,ct,cc,measures,catname=None,tab=3000):
    qs={'Category':{'projections':[col(ct,cc,catname)]},'Y':{'projections':[measure(t,m,n) for t,m,n in measures]}}
    return visual(name,x,y,w,h,'lineChart',qs,chart_obj(False),tab=tab)
def donut(name,x,y,w,h,ct,cc,mt,mm,tab=3000):
    return visual(name,x,y,w,h,'donutChart',{'Category':{'projections':[col(ct,cc)]},'Y':{'projections':[measure(mt,mm)]}},tab=tab)
def table(name,x,y,w,h,fields,tab=3000):
    proj=[]
    for t,c,is_m,n in fields:
        proj.append(measure(t,c,n) if is_m else col(t,c,n))
    obj={'columnHeaders':[{'properties':{'bold':lit('true'),'fontSize':lit('10L'),'fontColor':solid('#FFFFFF'),'backColor':solid('#1E293B')}}], 'values':[{'properties':{'fontSize':lit('9L'),'backColor':solid('#FFFFFF'),'backColorAlternate':solid('#F8FAFC')}}], 'grid':[{'properties':{'gridHorizontal':lit('true'),'gridHorizontalColor':solid('#E2E8F0'),'gridVertical':lit('false'),'rowPadding':lit('4L')}}]}
    return visual(name,x,y,w,h,'tableEx',{'Values':{'projections':proj}},obj,tab=tab)

def write_page(page_id,display,visuals):
    pdir=os.path.join(REPORT,page_id)
    if os.path.exists(pdir): shutil.rmtree(pdir)
    os.makedirs(os.path.join(pdir,'visuals'),exist_ok=True)
    page={'$schema':SCHEMA_PAGE,'name':page_id,'displayName':display,'displayOption':'FitToPage','height':1080,'width':1920,'objects':{'background':[{'properties':{'color':solid('#F8FAFC'),'transparency':lit('0D')}}]}}
    json.dump(page,open(os.path.join(pdir,'page.json'),'w',encoding='utf-8'),indent=2)
    for v in visuals:
        vd=os.path.join(pdir,'visuals',v['name']);os.makedirs(vd,exist_ok=True)
        json.dump(v,open(os.path.join(vd,'visual.json'),'w',encoding='utf-8'),indent=2)


def column_chart(name,x,y,w,h,ct,cc,mt,mm,catname=None,measname=None,tab=3000):
    qs={'Category':{'projections':[col(ct,cc,catname)]},'Y':{'projections':[measure(mt,mm,measname)]}}
    return visual(name,x,y,w,h,'clusteredColumnChart',qs,chart_obj(True),tab=tab)

# ---------------------------------------------------------------------------
# 1. Make Order Fulfillment robust: source raw Fact.Order and derive metrics
# ---------------------------------------------------------------------------
ORDER_TMDL=os.path.join(ROOT,'SupplyChain360.SemanticModel','definition','tables','Fact Order Fulfillment.tmdl')
REL=os.path.join(ROOT,'SupplyChain360.SemanticModel','definition','relationships.tmdl')
order_txt=open(ORDER_TMDL,encoding='utf-8').read()

# Add missing role keys if not already present.
if "column 'City Key'" not in order_txt:
    insert="""
\tcolumn 'City Key'
\t\tdataType: int64
\t\tisHidden
\t\tformatString: 0
\t\tsummarizeBy: none
\t\tsourceColumn: City Key

\t\tannotation SummarizationSetBy = Automatic

\tcolumn 'Salesperson Key'
\t\tdataType: int64
\t\tisHidden
\t\tformatString: 0
\t\tsummarizeBy: none
\t\tsourceColumn: Salesperson Key

\t\tannotation SummarizationSetBy = Automatic

\tcolumn 'Picker Key'
\t\tdataType: int64
\t\tisHidden
\t\tformatString: 0
\t\tsummarizeBy: none
\t\tsourceColumn: Picker Key

\t\tannotation SummarizationSetBy = Automatic

"""
    order_txt=order_txt.replace("\n\tcolumn 'Order Date Key'",insert+"\n\tcolumn 'Order Date Key'")

if "column 'Backordered Quantity'" not in order_txt:
    insert="""
\tcolumn 'Backordered Quantity'
\t\tdataType: int64
\t\tformatString: 0
\t\tsummarizeBy: sum
\t\tsourceColumn: Backordered Quantity

\t\tannotation SummarizationSetBy = Automatic

\tcolumn 'Is Picked'
\t\tdataType: int64
\t\tformatString: 0
\t\tsummarizeBy: sum
\t\tsourceColumn: Is Picked

\t\tannotation SummarizationSetBy = Automatic

"""
    order_txt=order_txt.replace("\n\tcolumn 'Days To Pick'",insert+"\n\tcolumn 'Days To Pick'")

if "column 'Picking Speed Category'" not in order_txt:
    insert="""
\tcolumn 'Picking Speed Category'
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Picking Speed Category

\t\tannotation SummarizationSetBy = Automatic

"""
    order_txt=order_txt.replace("\n\tpartition 'Fact Order Fulfillment' = m",insert+"\n\tpartition 'Fact Order Fulfillment' = m")

prefix=order_txt.split("\n\tpartition 'Fact Order Fulfillment' = m")[0]
partition="""
\tpartition 'Fact Order Fulfillment' = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Sql.Database("localhost", "WideWorldImportersDW"),
\t\t\t\t    Data = Source{[Schema="Fact",Item="Order"]}[Data],
\t\t\t\t    SelectedColumns = Table.SelectColumns(Data, {"Order Key", "City Key", "Customer Key", "Stock Item Key", "Salesperson Key", "Picker Key", "Order Date Key", "Picked Date Key", "WWI Order ID", "WWI Backorder ID", "Quantity", "Unit Price", "Tax Rate", "Total Excluding Tax", "Tax Amount", "Total Including Tax"}),
\t\t\t\t    AddedBackordered = Table.AddColumn(SelectedColumns, "Is Backordered", each if [WWI Backorder ID] = null then 0 else 1, Int64.Type),
\t\t\t\t    AddedBackorderedQty = Table.AddColumn(AddedBackordered, "Backordered Quantity", each if [WWI Backorder ID] = null then 0 else [Quantity], Int64.Type),
\t\t\t\t    AddedPicked = Table.AddColumn(AddedBackorderedQty, "Is Picked", each if [Picked Date Key] = null then 0 else 1, Int64.Type),
\t\t\t\t    AddedDaysToPick = Table.AddColumn(AddedPicked, "Days To Pick", each if [Picked Date Key] = null or [Order Date Key] = null then null else Duration.Days(Date.From([Picked Date Key]) - Date.From([Order Date Key])), Int64.Type),
\t\t\t\t    AddedStatus = Table.AddColumn(AddedDaysToPick, "Fulfillment Status", each if [WWI Backorder ID] <> null then "Backordered" else if [Picked Date Key] = null then "Pending Pick" else "Picked", type text),
\t\t\t\t    AddedSpeed = Table.AddColumn(AddedStatus, "Picking Speed Category", each if [Picked Date Key] = null then "Not Completed" else if [Days To Pick] = 0 then "Same Day" else if [Days To Pick] = 1 then "Next Day" else "2+ Days", type text)
\t\t\t\tin
\t\t\t\t    AddedSpeed

\tannotation PBI_NavigationStepName = Navigation

\tannotation PBI_ResultType = Table
"""
open(ORDER_TMDL,'w',encoding='utf-8').write(prefix+partition)

# Add order role-playing / conformed relationships.
rel_txt=open(REL,encoding='utf-8').read()
rels=[
("order_city_rel","'Fact Order Fulfillment'.'City Key'","'Dim City'.'City Key'",True),
("order_salesperson_rel","'Fact Order Fulfillment'.'Salesperson Key'","'Dim Employee'.'Employee Key'",True),
("order_picker_rel","'Fact Order Fulfillment'.'Picker Key'","'Dim Employee'.'Employee Key'",False),
]
for seed,fc,tc,active in rels:
    if fc not in rel_txt:
        rid=uid(seed)
        block=f"\nrelationship {rid}\n"
        if not active: block+="\tisActive: false\n"
        block+=f"\tfromColumn: {fc}\n\ttoColumn: {tc}\n"
        rel_txt+=block
open(REL,'w',encoding='utf-8').write(rel_txt)

# ---------------------------------------------------------------------------
# 2. Add final-domain DAX measures
# ---------------------------------------------------------------------------
text=open(MEAS,encoding='utf-8').read()
new_measures=r'''
	measure 'Picked Lines' = SUM('Fact Order Fulfillment'[Is Picked])
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Pick Completion %' = DIVIDE([Picked Lines], [Order Lines])
		formatString: 0.0%
		displayFolder: 10 Fulfillment Intelligence

	measure 'Backordered Units' = SUM('Fact Order Fulfillment'[Backordered Quantity])
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Backordered Orders' = CALCULATE(DISTINCTCOUNT('Fact Order Fulfillment'[WWI Order ID]), 'Fact Order Fulfillment'[Is Backordered] = 1)
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Backordered Order %' = DIVIDE([Backordered Orders], [Total Orders])
		formatString: 0.0%
		displayFolder: 10 Fulfillment Intelligence

	measure 'Backorder Unit Rate %' = DIVIDE([Backordered Units], [Ordered Units])
		formatString: 0.0%
		displayFolder: 10 Fulfillment Intelligence

	measure 'Same Day Pick Lines' = CALCULATE([Order Lines], 'Fact Order Fulfillment'[Picking Speed Category] = "Same Day")
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Next Day Pick Lines' = CALCULATE([Order Lines], 'Fact Order Fulfillment'[Picking Speed Category] = "Next Day")
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure '2+ Day Pick Lines' = CALCULATE([Order Lines], 'Fact Order Fulfillment'[Picking Speed Category] = "2+ Days")
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Same Day Pick %' = DIVIDE([Same Day Pick Lines], [Picked Lines])
		formatString: 0.0%
		displayFolder: 10 Fulfillment Intelligence

	measure 'Picked Orders by Picker' = CALCULATE([Total Orders], USERELATIONSHIP('Dim Employee'[Employee Key], 'Fact Order Fulfillment'[Picker Key]))
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Top 10 Product Backordered Units' = VAR Rnk = RANKX(ALLSELECTED('Dim Stock Item'[SKU Label]), [Backordered Units], , DESC, DENSE) RETURN IF(Rnk <= 10 && [Backordered Units] > 0, [Backordered Units])
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Top 10 Customer Backordered Units' = VAR Rnk = RANKX(ALLSELECTED('Dim Customer'[Customer]), [Backordered Units], , DESC, DENSE) RETURN IF(Rnk <= 10 && [Backordered Units] > 0, [Backordered Units])
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Top 10 City Backordered Units' = VAR Rnk = RANKX(ALLSELECTED('Dim City'[City]), [Backordered Units], , DESC, DENSE) RETURN IF(Rnk <= 10 && [Backordered Units] > 0, [Backordered Units])
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Top 10 Picker Orders' = VAR Rnk = RANKX(ALLSELECTED('Dim Employee'[Employee]), [Picked Orders by Picker], , DESC, DENSE) RETURN IF(Rnk <= 10, [Picked Orders by Picker])
		formatString: #,##0
		displayFolder: 10 Fulfillment Intelligence

	measure 'Average Revenue per Invoice' = DIVIDE([Total Revenue], [Total Invoices])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Revenue per Unit' = DIVIDE([Total Revenue], [Units Sold])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Profit per Unit' = DIVIDE([Total Profit], [Units Sold])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Sales Lines' = COUNTROWS('Fact Sales Demand')
		formatString: #,##0
		displayFolder: 11 Sales & Profitability

	measure 'Loss Making Lines' = CALCULATE([Sales Lines], 'Fact Sales Demand'[Is Loss Making] = TRUE())
		formatString: #,##0
		displayFolder: 11 Sales & Profitability

	measure 'Loss Making Line %' = DIVIDE([Loss Making Lines], [Sales Lines])
		formatString: 0.0%
		displayFolder: 11 Sales & Profitability

	measure 'Loss Making Revenue' = CALCULATE([Total Revenue], 'Fact Sales Demand'[Is Loss Making] = TRUE())
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Top 10 Product Revenue' = VAR Rnk = RANKX(ALLSELECTED('Dim Stock Item'[SKU Label]), [Total Revenue], , DESC, DENSE) RETURN IF(Rnk <= 10, [Total Revenue])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Top 10 Product Profit' = VAR Rnk = RANKX(ALLSELECTED('Dim Stock Item'[SKU Label]), [Total Profit], , DESC, DENSE) RETURN IF(Rnk <= 10, [Total Profit])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Top 10 Customer Revenue' = VAR Rnk = RANKX(ALLSELECTED('Dim Customer'[Customer]), [Total Revenue], , DESC, DENSE) RETURN IF(Rnk <= 10, [Total Revenue])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Top 10 Customer Profit' = VAR Rnk = RANKX(ALLSELECTED('Dim Customer'[Customer]), [Total Profit], , DESC, DENSE) RETURN IF(Rnk <= 10, [Total Profit])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Top 10 State Profit' = VAR Rnk = RANKX(ALLSELECTED('Dim City'[State Province]), [Total Profit], , DESC, DENSE) RETURN IF(Rnk <= 10, [Total Profit])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Top 10 Salesperson Revenue' = VAR Rnk = RANKX(ALLSELECTED('Dim Employee'[Employee]), [Total Revenue], , DESC, DENSE) RETURN IF(Rnk <= 10, [Total Revenue])
		formatString: $#,##0.00
		displayFolder: 11 Sales & Profitability

	measure 'Stock In %' = DIVIDE([Stock In Quantity], [Stock Movement Volume])
		formatString: 0.0%
		displayFolder: 12 Stock Movement Intelligence

	measure 'Stock Out %' = DIVIDE([Stock Out Quantity], [Stock Movement Volume])
		formatString: 0.0%
		displayFolder: 12 Stock Movement Intelligence

	measure 'Net Outflow Quantity' = MAX([Stock Out Quantity] - [Stock In Quantity], 0)
		formatString: #,##0
		displayFolder: 12 Stock Movement Intelligence

	measure 'Top 10 Product Net Outflow' = VAR Rnk = RANKX(ALLSELECTED('Dim Stock Item'[SKU Label]), [Net Outflow Quantity], , DESC, DENSE) RETURN IF(Rnk <= 10 && [Net Outflow Quantity] > 0, [Net Outflow Quantity])
		formatString: #,##0
		displayFolder: 12 Stock Movement Intelligence

	measure 'Top 10 Transaction Type Volume' = VAR Rnk = RANKX(ALLSELECTED('Dim Transaction Type'[Transaction Type]), [Stock Movement Volume], , DESC, DENSE) RETURN IF(Rnk <= 10, [Stock Movement Volume])
		formatString: #,##0
		displayFolder: 12 Stock Movement Intelligence

	measure 'Top 10 Supplier Stock In' = VAR Rnk = RANKX(ALLSELECTED('Dim Supplier'[Supplier]), [Stock In Quantity], , DESC, DENSE) RETURN IF(Rnk <= 10 && [Stock In Quantity] > 0, [Stock In Quantity])
		formatString: #,##0
		displayFolder: 12 Stock Movement Intelligence

	measure 'Top 10 Customer Stock Out' = VAR Rnk = RANKX(ALLSELECTED('Dim Customer'[Customer]), [Stock Out Quantity], , DESC, DENSE) RETURN IF(Rnk <= 10 && [Stock Out Quantity] > 0, [Stock Out Quantity])
		formatString: #,##0
		displayFolder: 12 Stock Movement Intelligence

	measure 'Latest Sales Date' = MAX('Fact Sales Demand'[Invoice Date Key])
		formatString: yyyy-mm-dd
		displayFolder: 13 Model QA

	measure 'Latest Order Date' = MAX('Fact Order Fulfillment'[Order Date Key])
		formatString: yyyy-mm-dd
		displayFolder: 13 Model QA

	measure 'Latest Movement Date' = MAX('Fact Stock Movement'[Date Key])
		formatString: yyyy-mm-dd
		displayFolder: 13 Model QA
'''
if "measure 'Picked Lines'" not in text:
    marker='\n\tcolumn Dummy\n'
    text=text.replace(marker,'\n'+new_measures+marker)
    open(MEAS,'w',encoding='utf-8').write(text)

# ---------------------------------------------------------------------------
# 3. Build remaining dashboard pages 06-14
# ---------------------------------------------------------------------------

def add_common_slicers(v,prefix,items,tab):
    x=30
    for width,t,c,label in items:
        v.append(slicer(prefix+'_'+label.replace(' ','_'),x,110,width,62,t,c,label,tab)); tab+=1; x+=width+20
    return tab

# 06 Order Fulfillment & Backorders
p6=uid('final_order_fulfillment')
v=[];tab=3000
v.append(title_box('p6_title',0,0,1920,72,'SupplyChain360 — Order Fulfillment & Backorders',20,bg='#0F172A'))
v.append(subtitle('p6_sub',30,76,1700,28,'Order volume • backorder exposure • picking completion • customer and product fulfillment performance'))
tab=add_common_slicers(v,'p6',[(280,'Dim Date','Calendar Year','Year'),(420,'Dim Customer','Customer','Customer'),(520,'Dim Stock Item','SKU Label','Product'),(300,'Dim City','State Province','State'),(300,'Dim Employee','Employee','Salesperson')],tab)
for i,(m,x,y) in enumerate([
('Total Orders',30,190),('Ordered Units',495,190),('Backordered Orders',960,190),('Backordered Units',1425,190),
('Backordered Order %',30,310),('Pick Completion %',495,310),('Average Days to Pick',960,310),('Same Day Pick %',1425,310)]):
    v.append(card(f'p6_card{i}',x,y,435,105,m,tab));tab+=1
v.append(title_box('p6_sec1',30,440,900,30,'Monthly Orders & Backordered Orders',11));v.append(title_box('p6_sec2',950,440,940,30,'Backordered Units — Top 10 Products',11))
v.append(line('p6_monthly',30,475,900,245,'Dim Date','Year Month',[('_Measures','Total Orders','Orders'),('_Measures','Backordered Orders','Backordered Orders')],'Year Month',tab));tab+=1
v.append(bar('p6_prod_backorder',950,475,940,245,'Dim Stock Item','SKU Label','_Measures','Top 10 Product Backordered Units','SKU','Backordered Units',tab));tab+=1
v.append(title_box('p6_sec3',30,740,600,30,'Picking Speed Mix',11));v.append(title_box('p6_sec4',650,740,620,30,'Backorder Exposure — Top Customers',11));v.append(title_box('p6_sec5',1290,740,600,30,'Picker Throughput — Top 10',11))
v.append(donut('p6_speed',30,775,600,270,'Fact Order Fulfillment','Picking Speed Category','_Measures','Order Lines',tab));tab+=1
v.append(bar('p6_customer',650,775,620,270,'Dim Customer','Customer','_Measures','Top 10 Customer Backordered Units','Customer','Backordered Units',tab));tab+=1
v.append(bar('p6_picker',1290,775,600,270,'Dim Employee','Employee','_Measures','Top 10 Picker Orders','Picker','Orders Picked',tab));tab+=1
write_page(p6,'06 Order Fulfillment & Backorders',v)

# 07 Fulfillment Exceptions
p7=uid('final_fulfillment_exceptions')
v=[];tab=3000
v.append(title_box('p7_title',0,0,1920,72,'SupplyChain360 — Fulfillment Exceptions',20,bg='#0F172A'))
v.append(subtitle('p7_sub',30,76,1700,28,'Exception-led order monitoring • pending picks • backorders • slow picking • customer and SKU hotspots'))
tab=add_common_slicers(v,'p7',[(430,'Dim Customer','Customer','Customer'),(560,'Dim Stock Item','SKU Label','Product'),(330,'Fact Order Fulfillment','Fulfillment Status','Status'),(330,'Fact Order Fulfillment','Picking Speed Category','Pick Speed')],tab)
for i,(m,x) in enumerate([('Pending Pick Lines',30),('Backordered Orders',400),('Backordered Units',770),('2+ Day Pick Lines',1140),('Average Days to Pick',1510)]):
    v.append(card(f'p7_card{i}',x,190,350,105,m,tab));tab+=1
v.append(title_box('p7_sec1',30,330,900,30,'Backordered Units — Top 10 Customers',11));v.append(title_box('p7_sec2',950,330,940,30,'Backordered Units — Top 10 Cities',11))
v.append(bar('p7_customer',30,365,900,260,'Dim Customer','Customer','_Measures','Top 10 Customer Backordered Units','Customer','Backordered Units',tab));tab+=1
v.append(bar('p7_city',950,365,940,260,'Dim City','City','_Measures','Top 10 City Backordered Units','City','Backordered Units',tab));tab+=1
v.append(title_box('p7_sec3',30,645,1860,30,'Fulfillment Exception Register',11))
v.append(table('p7_table',30,680,1860,365,[
('Dim Customer','Customer',False,'Customer'),('Dim Stock Item','SKU Label',False,'SKU'),('Dim City','State Province',False,'State'),('Fact Order Fulfillment','Fulfillment Status',False,'Status'),('Fact Order Fulfillment','Picking Speed Category',False,'Pick Speed'),('_Measures','Total Orders',True,'Orders'),('_Measures','Ordered Units',True,'Units'),('_Measures','Backordered Units',True,'Backordered Units'),('_Measures','Average Days to Pick',True,'Avg Days to Pick'),('_Measures','Order Value',True,'Order Value')],tab));tab+=1
write_page(p7,'07 Fulfillment Exceptions',v)

# 08 Sales & Demand Intelligence
p8=uid('final_sales_demand')
v=[];tab=3000
v.append(title_box('p8_title',0,0,1920,72,'SupplyChain360 — Sales & Demand Intelligence',20,bg='#0F172A'))
v.append(subtitle('p8_sub',30,76,1700,28,'Revenue • demand • profitability • customer concentration • geography • delivery performance'))
tab=add_common_slicers(v,'p8',[(280,'Dim Date','Calendar Year','Year'),(520,'Dim Stock Item','SKU Label','Product'),(420,'Dim Customer','Customer','Customer'),(300,'Dim City','State Province','State'),(300,'Dim Employee','Employee','Salesperson')],tab)
for i,(m,x,y) in enumerate([
('Total Revenue',30,190),('Total Profit',495,190),('Profit Margin %',960,190),('Units Sold',1425,190),
('Total Invoices',30,310),('Average Revenue per Invoice',495,310),('Revenue YoY %',960,310),('Average Delivery Days',1425,310)]):
    v.append(card(f'p8_card{i}',x,y,435,105,m,tab));tab+=1
v.append(title_box('p8_sec1',30,440,900,30,'Monthly Revenue & Profit',11));v.append(title_box('p8_sec2',950,440,940,30,'Revenue — Top 10 Products',11))
v.append(line('p8_monthly',30,475,900,245,'Dim Date','Year Month',[('_Measures','Total Revenue','Revenue'),('_Measures','Total Profit','Profit')],'Year Month',tab));tab+=1
v.append(bar('p8_prod',950,475,940,245,'Dim Stock Item','SKU Label','_Measures','Top 10 Product Revenue','SKU','Revenue',tab));tab+=1
v.append(title_box('p8_sec3',30,740,600,30,'Delivery Speed Mix',11));v.append(title_box('p8_sec4',650,740,620,30,'Revenue — Top Customers',11));v.append(title_box('p8_sec5',1290,740,600,30,'Profit — Top States',11))
v.append(donut('p8_delivery',30,775,600,270,'Fact Sales Demand','Delivery Speed Category','_Measures','Total Revenue',tab));tab+=1
v.append(bar('p8_customer',650,775,620,270,'Dim Customer','Customer','_Measures','Top 10 Customer Revenue','Customer','Revenue',tab));tab+=1
v.append(bar('p8_state',1290,775,600,270,'Dim City','State Province','_Measures','Top 10 State Profit','State','Profit',tab));tab+=1
write_page(p8,'08 Sales & Demand Intelligence',v)

# 09 Profitability & Customer Insights
p9=uid('final_profitability')
v=[];tab=3000
v.append(title_box('p9_title',0,0,1920,72,'SupplyChain360 — Profitability & Customer Insights',20,bg='#0F172A'))
v.append(subtitle('p9_sub',30,76,1700,28,'Margin quality • loss-making exposure • customer profitability • product economics • salesperson contribution'))
tab=add_common_slicers(v,'p9',[(500,'Dim Customer','Customer','Customer'),(600,'Dim Stock Item','SKU Label','Product'),(350,'Fact Sales Demand','Profitability Status','Profitability'),(350,'Dim City','State Province','State')],tab)
for i,(m,x,y) in enumerate([
('Total Profit',30,190),('Profit Margin %',495,190),('Profit per Unit',960,190),('Loss Making Lines',1425,190),
('Loss Making Revenue',30,310),('Loss Making Line %',495,310),('Revenue YTD',960,310),('Profit YTD',1425,310)]):
    v.append(card(f'p9_card{i}',x,y,435,105,m,tab));tab+=1
v.append(title_box('p9_sec1',30,440,900,30,'Profit — Top 10 Products',11));v.append(title_box('p9_sec2',950,440,940,30,'Profit — Top 10 Customers',11))
v.append(bar('p9_prod_profit',30,475,900,245,'Dim Stock Item','SKU Label','_Measures','Top 10 Product Profit','SKU','Profit',tab));tab+=1
v.append(bar('p9_cust_profit',950,475,940,245,'Dim Customer','Customer','_Measures','Top 10 Customer Profit','Customer','Profit',tab));tab+=1
v.append(title_box('p9_sec3',30,740,600,30,'Profitability Status',11));v.append(title_box('p9_sec4',650,740,620,30,'Revenue — Top Salespeople',11));v.append(title_box('p9_sec5',1290,740,600,30,'Customer Profitability Detail',11))
v.append(donut('p9_status',30,775,600,270,'Fact Sales Demand','Profitability Status','_Measures','Total Revenue',tab));tab+=1
v.append(bar('p9_salesperson',650,775,620,270,'Dim Employee','Employee','_Measures','Top 10 Salesperson Revenue','Salesperson','Revenue',tab));tab+=1
v.append(table('p9_table',1290,775,600,270,[('Dim Customer','Customer',False,'Customer'),('_Measures','Total Revenue',True,'Revenue'),('_Measures','Total Profit',True,'Profit'),('_Measures','Profit Margin %',True,'Margin %'),('_Measures','Units Sold',True,'Units')],tab));tab+=1
write_page(p9,'09 Profitability & Customer Insights',v)

# 10 Stock Movement & Operations
p10=uid('final_stock_movement')
v=[];tab=3000
v.append(title_box('p10_title',0,0,1920,72,'SupplyChain360 — Stock Movement & Operations',20,bg='#0F172A'))
v.append(subtitle('p10_sub',30,76,1700,28,'Inventory flow • stock receipts/issues • movement mix • product velocity • supplier and customer operational flows'))
tab=add_common_slicers(v,'p10',[(280,'Dim Date','Calendar Year','Year'),(520,'Dim Stock Item','SKU Label','Product'),(390,'Dim Transaction Type','Transaction Type','Transaction Type'),(330,'Fact Stock Movement','Flow Direction','Flow'),(330,'Fact Stock Movement','Movement Source','Source')],tab)
for i,(m,x,y) in enumerate([
('Stock In Quantity',30,190),('Stock Out Quantity',495,190),('Net Stock Movement',960,190),('Movement Events',1425,190),
('Stock Movement Volume',30,310),('Stock In %',495,310),('Stock Out %',960,310),('Quantity On Hand',1425,310)]):
    v.append(card(f'p10_card{i}',x,y,435,105,m,tab));tab+=1
v.append(title_box('p10_sec1',30,440,900,30,'Monthly Stock In vs Stock Out',11));v.append(title_box('p10_sec2',950,440,940,30,'Movement Volume — Top Transaction Types',11))
v.append(line('p10_monthly',30,475,900,245,'Dim Date','Year Month',[('_Measures','Stock In Quantity','Stock In'),('_Measures','Stock Out Quantity','Stock Out')],'Year Month',tab));tab+=1
v.append(bar('p10_type',950,475,940,245,'Dim Transaction Type','Transaction Type','_Measures','Top 10 Transaction Type Volume','Transaction Type','Movement Volume',tab));tab+=1
v.append(title_box('p10_sec3',30,740,600,30,'Movement Source Mix',11));v.append(title_box('p10_sec4',650,740,620,30,'Supplier Stock In — Top 10',11));v.append(title_box('p10_sec5',1290,740,600,30,'Customer Stock Out — Top 10',11))
v.append(donut('p10_source',30,775,600,270,'Fact Stock Movement','Movement Source','_Measures','Stock Movement Volume',tab));tab+=1
v.append(bar('p10_supplier',650,775,620,270,'Dim Supplier','Supplier','_Measures','Top 10 Supplier Stock In','Supplier','Stock In',tab));tab+=1
v.append(bar('p10_customer',1290,775,600,270,'Dim Customer','Customer','_Measures','Top 10 Customer Stock Out','Customer','Stock Out',tab));tab+=1
write_page(p10,'10 Stock Movement & Operations',v)

# 11 Movement Exceptions
p11=uid('final_movement_exceptions')
v=[];tab=3000
v.append(title_box('p11_title',0,0,1920,72,'SupplyChain360 — Movement Exceptions & Net Outflow Risk',20,bg='#0F172A'))
v.append(subtitle('p11_sub',30,76,1700,28,'Net-outflow hotspots • operational transaction mix • high-velocity SKU monitoring • detailed movement exception register'))
tab=add_common_slicers(v,'p11',[(580,'Dim Stock Item','SKU Label','Product'),(430,'Dim Transaction Type','Transaction Type','Transaction Type'),(400,'Fact Stock Movement','Flow Direction','Flow Direction'),(400,'Fact Stock Movement','Movement Source','Source')],tab)
for i,(m,x) in enumerate([('Net Stock Movement',30),('Net Outflow Quantity',400),('Stock Movement Volume',770),('Movement Events',1140),('Stock Out Quantity',1510)]):
    v.append(card(f'p11_card{i}',x,190,350,105,m,tab));tab+=1
v.append(title_box('p11_sec1',30,330,900,30,'Net Outflow — Top 10 Products',11));v.append(title_box('p11_sec2',950,330,940,30,'Movement Volume — Top 10 Products',11))
v.append(bar('p11_outflow',30,365,900,270,'Dim Stock Item','SKU Label','_Measures','Top 10 Product Net Outflow','SKU','Net Outflow',tab));tab+=1
v.append(bar('p11_volume',950,365,940,270,'Dim Stock Item','SKU Label','_Measures','Top 10 Movement Volume','SKU','Movement Volume',tab));tab+=1
v.append(title_box('p11_sec3',30,655,1860,30,'Movement Exception Register',11))
v.append(table('p11_table',30,690,1860,355,[('Dim Stock Item','SKU Label',False,'SKU'),('Dim Transaction Type','Transaction Type',False,'Transaction Type'),('Fact Stock Movement','Flow Direction',False,'Flow'),('Fact Stock Movement','Movement Source',False,'Source'),('_Measures','Stock In Quantity',True,'Stock In'),('_Measures','Stock Out Quantity',True,'Stock Out'),('_Measures','Net Stock Movement',True,'Net'),('_Measures','Stock Movement Volume',True,'Volume'),('_Measures','Movement Events',True,'Events')],tab));tab+=1
write_page(p11,'11 Movement Exceptions',v)

# 12 Product 360
p12=uid('final_product360')
v=[];tab=3000
v.append(title_box('p12_title',0,0,1920,72,'SupplyChain360 — Product 360',20,bg='#0F172A'))
v.append(subtitle('p12_sub',30,76,1700,28,'One-product view across inventory • procurement • demand • profitability • fulfillment • stock movement'))
v.append(slicer('p12_product',30,110,1200,62,'Dim Stock Item','SKU Label','Product',tab));tab+=1
v.append(slicer('p12_year',1250,110,300,62,'Dim Date','Calendar Year','Year',tab));tab+=1
v.append(slicer('p12_chiller',1570,110,320,62,'Dim Stock Item','Is Chiller Stock','Chiller Stock',tab));tab+=1
cards=[('Total Inventory Value',30,190),('Quantity On Hand',400,190),('Units Sold',770,190),('Total Revenue',1140,190),('Total Profit',1510,190),('Ordered Quantity',30,310),('Outstanding Quantity',400,310),('Backordered Units',770,310),('Stock Movement Volume',1140,310),('Average Days to Pick',1510,310)]
for i,(m,x,y) in enumerate(cards):v.append(card(f'p12_card{i}',x,y,350,105,m,tab));tab+=1
v.append(title_box('p12_sec1',30,440,900,30,'Monthly Revenue & Profit',11));v.append(title_box('p12_sec2',950,440,940,30,'Monthly Stock In & Stock Out',11))
v.append(line('p12_salestrend',30,475,900,245,'Dim Date','Year Month',[('_Measures','Total Revenue','Revenue'),('_Measures','Total Profit','Profit')],'Year Month',tab));tab+=1
v.append(line('p12_movetrend',950,475,940,245,'Dim Date','Year Month',[('_Measures','Stock In Quantity','Stock In'),('_Measures','Stock Out Quantity','Stock Out')],'Year Month',tab));tab+=1
v.append(title_box('p12_sec3',30,740,1860,30,'Product Operational Snapshot',11))
v.append(table('p12_table',30,775,1860,270,[('Dim Stock Item','SKU Label',False,'SKU'),('Dim Stock Item','Brand',False,'Brand'),('Dim Stock Item','Lead Time Days',False,'Lead Time'),('_Measures','Total Inventory Value',True,'Inventory Value'),('_Measures','Quantity On Hand',True,'On Hand'),('_Measures','Reorder Gap Units',True,'Reorder Gap'),('_Measures','Excess Inventory Value',True,'Excess Value'),('_Measures','Procurement Fulfillment %',True,'Procurement Fill'),('_Measures','Backorder Rate %',True,'Backorder Rate'),('_Measures','Profit Margin %',True,'Margin')],tab));tab+=1
write_page(p12,'12 Product 360',v)

# 13 Supplier 360
p13=uid('final_supplier360')
v=[];tab=3000
v.append(title_box('p13_title',0,0,1920,72,'SupplyChain360 — Supplier 360',20,bg='#0F172A'))
v.append(subtitle('p13_sub',30,76,1700,28,'One-supplier procurement profile • purchase-order completion • receipt exposure • product mix • inbound stock movement'))
v.append(slicer('p13_supplier',30,110,1100,62,'Dim Supplier','Supplier','Supplier',tab));tab+=1
v.append(slicer('p13_category',1150,110,400,62,'Dim Supplier','Category','Category',tab));tab+=1
v.append(slicer('p13_year',1570,110,320,62,'Dim Date','Calendar Year','Year',tab));tab+=1
cards=[('Purchase Orders',30,190),('Ordered Quantity',400,190),('Received Quantity',770,190),('Outstanding Quantity',1140,190),('Procurement Fulfillment %',1510,190),('Open Purchase Orders',30,310),('Purchase Order Completion %',400,310),('Average Expected Lead Time Days',770,310),('Stock In Quantity',1140,310),('Receipt Shortfall Lines',1510,310)]
for i,(m,x,y) in enumerate(cards):v.append(card(f'p13_card{i}',x,y,350,105,m,tab));tab+=1
v.append(title_box('p13_sec1',30,440,900,30,'Monthly Ordered vs Received',11));v.append(title_box('p13_sec2',950,440,940,30,'Outstanding Quantity — Top Products',11))
v.append(line('p13_monthly',30,475,900,245,'Dim Date','Year Month',[('_Measures','Ordered Quantity','Ordered'),('_Measures','Received Quantity','Received')],'Year Month',tab));tab+=1
v.append(bar('p13_products',950,475,940,245,'Dim Stock Item','SKU Label','_Measures','Top 10 Product Outstanding Quantity','SKU','Outstanding',tab));tab+=1
v.append(title_box('p13_sec3',30,740,1860,30,'Supplier Product Scorecard',11))
v.append(table('p13_table',30,775,1860,270,[('Dim Supplier','Supplier',False,'Supplier'),('Dim Stock Item','SKU Label',False,'SKU'),('_Measures','Purchase Orders',True,'POs'),('_Measures','Ordered Quantity',True,'Ordered'),('_Measures','Received Quantity',True,'Received'),('_Measures','Outstanding Quantity',True,'Outstanding'),('_Measures','Procurement Fulfillment %',True,'Fill %'),('_Measures','Stock In Quantity',True,'Stock In')],tab));tab+=1
write_page(p13,'13 Supplier 360',v)

# 14 Data Quality & Model QA
p14=uid('final_model_qa')
v=[];tab=3000
v.append(title_box('p14_title',0,0,1920,72,'SupplyChain360 — Data Quality & Model QA',20,bg='#0F172A'))
v.append(subtitle('p14_sub',30,76,1700,28,'Semantic-model acceptance checks • inventory uniqueness • data coverage • reconciliation readiness'))
for i,(m,x,y) in enumerate([
('Inventory QA Status',30,150),('Inventory Key QA',495,150),('Inventory SKUs',960,150),('Supplier Count',1425,150),
('Latest Sales Date',30,280),('Latest Order Date',495,280),('Latest Movement Date',960,280),('Purchase Orders',1425,280)]):
    v.append(card(f'p14_card{i}',x,y,435,110,m,tab));tab+=1
v.append(title_box('p14_sec1',30,430,900,30,'Inventory Status Distribution',11));v.append(title_box('p14_sec2',950,430,940,30,'Core KPI Reconciliation Snapshot',11))
v.append(donut('p14_status',30,465,900,300,'Fact Inventory','Inventory Status','_Measures','Inventory SKUs',tab));tab+=1
v.append(table('p14_kpis',950,465,940,300,[('_Measures','Total Inventory Value',True,'Inventory Value'),('_Measures','Total Revenue',True,'Revenue'),('_Measures','Total Profit',True,'Profit'),('_Measures','Procurement Fulfillment %',True,'Procurement Fill'),('_Measures','Backorder Rate %',True,'Backorder Rate'),('_Measures','Net Stock Movement',True,'Net Movement')],tab));tab+=1
v.append(title_box('p14_sec3',30,790,1860,30,'QA Acceptance Criteria',11))
v.append(subtitle('p14_note',30,830,1860,160,'PASS criteria: Inventory QA Status = PASS; Inventory Key QA = 0; refresh completes without query errors; SQL validation scripts 01–08 reconcile headline KPIs; no broken relationships or visual field references.'))
write_page(p14,'14 Data Quality & Model QA',v)

# Update page metadata
pp=os.path.join(REPORT,'pages.json')
pages=json.load(open(pp,encoding='utf-8'))
for pid in [p6,p7,p8,p9,p10,p11,p12,p13,p14]:
    if pid not in pages['pageOrder']: pages['pageOrder'].append(pid)
json.dump(pages,open(pp,'w',encoding='utf-8'),indent=2)

# ---------------------------------------------------------------------------
# 4. Documentation inside PBIP package
# ---------------------------------------------------------------------------
notes={
'STAGE_11_FULFILLMENT.md':'''# Stage 11 — Order Fulfillment & Backorder Intelligence\n\nPages 06–07 add order, backorder, picking-speed, customer/SKU hotspot and exception analysis. Fact Order Fulfillment now sources raw Fact.Order and derives Days To Pick in Power Query, removing dependency on an older analytics-view schema.\n''',
'STAGE_12_SALES_DEMAND.md':'''# Stage 12 — Sales, Demand & Profitability\n\nPages 08–09 add revenue, profit, demand, customer concentration, loss-making exposure, delivery-speed and salesperson analysis.\n''',
'STAGE_13_STOCK_MOVEMENT.md':'''# Stage 13 — Stock Movement & Operations\n\nPages 10–11 add stock in/out, net flow, transaction-type, product velocity, supplier inbound, customer outbound and net-outflow exception analysis.\n''',
'STAGE_14_360_VIEWS.md':'''# Stage 14 — 360 Views\n\nPages 12–13 provide Product 360 and Supplier 360 cross-domain analytical views using conformed dimensions across inventory, procurement, fulfillment, sales and movement facts.\n''',
'FINAL_QA_AND_DEPLOYMENT.md':'''# Final QA & Deployment\n\nPage 14 provides model QA visibility. Before publication: run SQL validation scripts, refresh the PBIP locally, verify Inventory QA Status = PASS, then publish to Power BI Service and configure gateway/credentials and scheduled refresh as required.\n'''
}
for fn,c in notes.items(): open(os.path.join(ROOT,fn),'w',encoding='utf-8').write(c)

# ---------------------------------------------------------------------------
# 5. Static QA
# ---------------------------------------------------------------------------
# Parse all report JSON
errors=[]
for dirpath,_,files in os.walk(os.path.join(ROOT,'SupplyChain360.Report')):
    for fn in files:
        if fn.endswith('.json'):
            p=os.path.join(dirpath,fn)
            try: json.load(open(p,encoding='utf-8'))
            except Exception as e: errors.append((p,str(e)))
if errors: raise RuntimeError(f'JSON errors: {errors[:5]}')

# TMDL model inventory
base_tables=os.path.join(ROOT,'SupplyChain360.SemanticModel','definition','tables')
table_cols={}; table_measures={}
for fn in os.listdir(base_tables):
    if not fn.endswith('.tmdl'): continue
    t=fn[:-5]; s=open(os.path.join(base_tables,fn),encoding='utf-8').read()
    cs=[]
    for a,b in re.findall(r"\n\tcolumn (?:'([^']+)'|([^\n\t]+))",s): cs.append(a or b.strip())
    table_cols[t]=set(cs); table_measures[t]=set(re.findall(r"\n\tmeasure '([^']+)'",s))

# Validate visual field and measure references
bad=[]
for p in glob.glob(os.path.join(REPORT,'*','visuals','*','visual.json')):
    d=json.load(open(p,encoding='utf-8'))
    raw=json.dumps(d)
    # targeted extractor for SourceRef Entity / Property pairs
    for entity,prop in re.findall(r'"SourceRef": \{"Entity": "([^"]+)"\}[^\}]*?"Property": "([^"]+)"',raw):
        if prop not in table_cols.get(entity,set()) and prop not in table_measures.get(entity,set()):
            bad.append((os.path.relpath(p,ROOT),entity,prop))
if bad: raise RuntimeError(f'Broken visual refs: {bad[:20]}')

# Validate relationship refs exist
rtext=open(REL,encoding='utf-8').read()
for t,c in re.findall(r"(?:fromColumn|toColumn): '([^']+)'\.'([^']+)'",rtext):
    if c not in table_cols.get(t,set()): raise RuntimeError(f'Broken relationship {t}.{c}')

# Validate all measure table/column DAX refs (simple direct refs)
mtxt=open(MEAS,encoding='utf-8').read()
for t,c in re.findall(r"'([^']+)'\[([^\]]+)\]",mtxt):
    if t in table_cols and c not in table_cols[t] and c not in table_measures.get(t,set()):
        raise RuntimeError(f'Broken DAX ref {t}[{c}]')

# Validate page order and files
pages=json.load(open(pp,encoding='utf-8'))
for pid in pages['pageOrder']:
    if not os.path.exists(os.path.join(REPORT,pid,'page.json')): raise RuntimeError(f'Missing page {pid}')

# Write QA report
qa=f'''# SupplyChain360 — Final Static QA PASS\n\n- Report pages registered: {len(pages['pageOrder'])}\n- Report JSON parse errors: 0\n- Broken visual field/measure references: 0\n- Broken relationship references: 0\n- Broken direct DAX table/column references: 0\n- Order Fulfillment refresh hardening: raw Fact.Order source + Power Query-derived Days To Pick\n- Runtime SQL refresh still requires local SQL Server database WideWorldImportersDW.\n'''
open(os.path.join(ROOT,'FINAL_STATIC_QA_PASS.md'),'w',encoding='utf-8').write(qa)

# Zip final project
out='/mnt/data/SupplyChain360-FINAL-COMPLETE.zip'
if os.path.exists(out): os.remove(out)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    parent=os.path.dirname(ROOT)
    for dirpath,_,files in os.walk(ROOT):
        for fn in files:
            p=os.path.join(dirpath,fn)
            z.write(p,os.path.relpath(p,parent))
print(out)
print('pages',len(pages['pageOrder']))
print('measures',len(table_measures.get('_Measures',[])))
