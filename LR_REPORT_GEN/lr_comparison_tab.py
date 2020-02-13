### GENERATES THE BAR GRAPH AND THE TABLE IN THE COMPARISON TAB ###

import plotly.graph_objects as go
from dash.dependencies import Input, Output

from lr_report_dataset import colors, db_data, LRLC
import lr_report_classes
from lr_report_init import app



## CALLBACK TO UPDATE THE BAR GRAPH BASED ON THE DROPDOWN MENUS
@app.callback(
  Output('barG', 'figure'),
  [Input('compare_1','value'),
   Input('compare_2','value')])

def update_bar_graph(lr_report_1, lr_report_2):  
  clrStrt = 0
  bar = go.Figure()
  bar.add_trace(create_bar_plot(lr_report_1, colors[clrStrt]))
  clrStrt += 1
  bar.add_trace(create_bar_plot(lr_report_2, colors[clrStrt]))
  
  bar.update_layout(autosize=False, margin=go.layout.Margin(l = 50, r= 50, b= 100, t=100, pad = 4), title_text="Total Runtime 90th Percentile Comparison <span style='color:deeppink'><b>" + lr_report_1 + "</b></span> vs <span style='color:deepskyblue'><b>" + lr_report_2 + "</b></span>")
  return bar

## HELPER METHOD - CREATES EACH SET OF BARS TO ADD TO THE GRAPH
def create_bar_plot(lr_report, color):
  lr_report_names = []
  lr_report_data = []
  lr_report_scores = []

  for report in db_data:
    if lr_report in report.lr_name:
      lr_report_data=report
  for i in range(len(lr_report_data.lr_moneymakers)):
    lr_report_names.append(lr_report_data.lr_moneymakers[i].transaction_name)
    lr_report_scores.append(lr_report_data.lr_moneymakers[i].nintieth_percentile)

  bar_element = go.Bar(name="RELEASE: " + lr_report + " TOTAL", x = lr_report_names, y = lr_report_scores, text = lr_report_scores, textposition='auto',marker_color=color, marker_line_color=LRLC)

  return bar_element

## CALLBACK TO UPDATE THE TABLE BASED ON THE DROPDOWN MENUS
@app.callback(
  Output('compare_table', 'figure'),
  [Input('compare_1','value'),
   Input('compare_2','value')]
)
def update_comparison_table(lr_report_1 , lr_report_2):
  clrStrt = 0
  
  lr_report_data_1 = []
  lr_report_data_2 = []
  lr_report_transaction_names_1 =[]
  lr_ninety_1 = []
  lr_report_transaction_names_2 =[]
  lr_ninety_2 = []
  transaction_names =[]
  extra_names = []
  extra_lr_1_ninety = []
  extra_lr_2_ninety = []
  diff = []
  
  for report in db_data:
    if lr_report_1 in report.lr_name:
      lr_report_data_1 = report
    if lr_report_2 in report.lr_name:
      lr_report_data_2 = report
  
  for i in range(len(lr_report_data_1.lr_transactions)):
    lr_report_transaction_names_1.append(lr_report_data_1.lr_transactions[i].transaction_name)
  for i in range(len(lr_report_data_2.lr_transactions)):
    lr_report_transaction_names_2.append(lr_report_data_2.lr_transactions[i].transaction_name)
  
  ## FIND ALL TRANSACTIONS THAT PERSIST BETWEEN VERSIONS ##
  
  for i in range(len(lr_report_transaction_names_1)):
    for j in range(len(lr_report_transaction_names_2)):
      if lr_report_transaction_names_1[i] == lr_report_transaction_names_2[j] and lr_report_transaction_names_1[i] not in transaction_names:
        transaction_names.append(lr_report_transaction_names_1[i])
        lr_report_transaction_names_1[i] = 0
        lr_report_transaction_names_2[j] = 0
        lr_ninety_1.append(lr_report_data_1.lr_transactions[i].nintieth_percentile)
        lr_ninety_2.append(lr_report_data_2.lr_transactions[j].nintieth_percentile)
        diff.append(lr_report_data_1.lr_transactions[i].nintieth_percentile - lr_report_data_2.lr_transactions[j].nintieth_percentile)
        continue
  
  ## all transactions which are NOT zeroes will be appended to their respective 'extra' arrays ##
  for i in range(len(lr_report_transaction_names_1)):
    if lr_report_transaction_names_1[i] !=0:
      extra_names.append(lr_report_transaction_names_1[i])
      extra_lr_1_ninety.append(lr_report_data_1.lr_transactions[i].nintieth_percentile)
      extra_lr_2_ninety.append('<b>N/A</b>')
  for i in range(len(lr_report_transaction_names_2)):
    if lr_report_transaction_names_2[i] !=0:
      extra_names.append(lr_report_transaction_names_2[i])
      extra_lr_2_ninety.append(lr_report_data_2.lr_transactions[i].nintieth_percentile)
      extra_lr_1_ninety.append('<b>N/A</b>')


  ## apply color to diff corresponding to test that has higher runtime for runtimes greater than 1 second difference ##
  for i in range(len(diff)):
    if float(diff[i]) > 1.0:
      diff[i] = "<span style='color:deeppink'><b>%s</b></span>" %str(round(diff[i], 3))
    elif float(diff[i]) < -1.0:
      diff[i] = "<span style='color:blue'><b>%s</b></span>" %str(round(diff[i],3))
    else:
      diff[i] = str(round(diff[i], 3))

  ## CREATE THE TABLE
  table = go.Figure( data =[go.Table(columnwidth = [150, 70, 70, 70], header = dict(values = ("Transaction Name", "R1 :Ninetieth Percentile " + lr_report_1, "R2: Ninetieth Percentile " + lr_report_2, "Diff (R1 - R2)"), fill_color = ['lightgray', colors[clrStrt], colors[clrStrt+1], 'lightgray'], font_color = ['black', 'black', 'black', 'black'] , align ='left'),
                                     cells = dict(values = [transaction_names + extra_names , lr_ninety_1 + extra_lr_1_ninety, lr_ninety_2+extra_lr_2_ninety, diff], align = 'left'))
  ])


  return table

