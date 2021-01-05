import plotly.graph_objects as go
from dash.dependencies import Input, Output

import lr_report_classes
from lr_report_init import app
from lr_report_dataset import colors, db_data, LRLC

# This callback updates the graphs visually based on new report selections.
@app.callback(
  Output('barG', 'figure'),
  [Input('compare_1','value'),
   Input('compare_2','value')]
)

def update_bar_graph(lr_report_1: str, lr_report_2:str):  # Called every time a new report is chosen.
  """Takes 2 loadrunner report names as args, returns a plotly bar object with 2 datasets."""
  bar = go.Figure()
  bar.add_trace(create_bar_plot(lr_report_1, colors[0]))
  bar.add_trace(create_bar_plot(lr_report_2, colors[1]))
  bar.update_layout(autosize=False, margin=go.layout.Margin(l=50, r=50, b=100, t=100, pad=4), 
                    title_text="Total Runtime 90th Percentile Comparison <span style='color:deeppink'><b>" 
                    + lr_report_1 + "</b></span> vs <span style='color:deepskyblue'><b>" 
                    + lr_report_2 + "</b></span>")
  return bar
 
def create_bar_plot(lr_report:str, color): # Creates a single bar object.  This is called by update_bar_graph().
  """Takes a loadrunner report names and a color, returns a single plotly bar object."""
  lr_report_data = {} # values = [(names,scores)]
  db_entry = []

  for report in db_data:
    if lr_report in report.lr_name:
      lr_report_data[report.lr_name] = []
      db_entry = report

  for i in range(len(db_entry.lr_moneymakers)):
    lr_report_data[report].append(db_entry.lr_moneymakers[i].transaction_name, 
                                  db_entry.lr_moneymakers[i].nintieth_percentile)

  bar_element = go.Bar(name="RELEASE: " + lr_report + " TOTAL",
                       x = lr_report_data.values()[0],
                       y = lr_report_data.keys(), text = lr_report_data.values(), 
                       textposition='auto', marker_color=color, marker_line_color=LRLC)
  return bar_element




# This callback updates the table object based on selection of a new lr report.
@app.callback(
  Output('compare_table', 'figure'),
  [Input('compare_1','value'),
   Input('compare_2','value')]
)

def update_comparison_table(lr_report_1:str , lr_report_2:str):
  """Takes two report names, returns a plotly table object"""
  lr_report_data_1 = {} # values = [(names,scores)]
  lr_report_data_2 = {}
  db_entry_1 = []
  db_entry_2 = []

  transaction_names = []
  extra_names = []
  extra_lr_1_ninety = []
  extra_lr_2_ninety = []
  diff = []
  
  for report in db_data:
    if lr_report_1 in report.lr_name:
      lr_report_data_1[report.lr_name] = []
      db_entry_1 = report
    if lr_report_2 in report.lr_name:
      lr_report_data_2[report.lr_name] = []
      db_entry_2 = report
  
  for transaction in db_entry_1.lr_transactions:
    lr_report_data_1[db_entry_1.lr_name].append((transaction.transaction_name, 
                                                 transaction.nintieth_percentile)
                                               )
  for transaction in db_entry_2.lr_transactions:
    lr_report_data_2[db_entry_2.lr_name].append((transaction.transaction_name, 
                                                 transaction.nintieth_percentile)
                                               )
  
  
  for transaction_1 in lr_report_data_1.values(): # This finds the transactions common between versions.
    for transaction_2 in lr_report_data_2.values():
      if transaction_1[0] == transaction_2[0] and transaction_1[0] not in transaction_names:
        transaction_names.append(transaction_1[0])
        diff.append(transaction_1[1] - transaction_2[1])
        transaction_1[1] = 0
        transaction_2[1] = 0
  
  ## all transactions which are NOT zeroes will be appended to their respective 'extra' arrays ##
  for transaction in lr_report_data_1.values():
    if transaction[1] !=0:
      extra_names.append(transaction[0])
      extra_lr_1_ninety.append(transaction[1])
      extra_lr_2_ninety.append('<b>N/A</b>') 

  for transaction in lr_report_data_2.values():
    if transaction[1] !=0:
      extra_names.append(transaction[0])
      extra_lr_2_ninety.append(transaction[1])
      extra_lr_1_ninety.append('<b>N/A</b>')


  ## apply color to diff corresponding to test that has higher runtime for runtimes greater than 1 second difference ##
  for i in range(len(diff)):
    if float(diff[i]) > 1.0:
      diff[i] = "<span style='color:deeppink'><b>%s</b></span>" %str(round(diff[i], 3))
    elif float(diff[i]) < -1.0:
      diff[i] = "<span style='color:blue'><b>%s</b></span>" %str(round(diff[i], 3))
    else:
      diff[i] = str(round(diff[i], 3))

  ## CREATE THE TABLE
  table = go.Figure(data =[go.Table(columnwidth = [150, 70, 70, 70], 
                                    header = dict(values = ("Transaction Name", "R1 :Ninetieth Percentile " 
                                                            + lr_report_1, "R2: Ninetieth Percentile " 
                                                            + lr_report_2, "Diff (R1 - R2)"
                                                          ), 
                                                  fill_color = ['lightgray', colors[0], colors[1], 'lightgray'], 
                                                  font_color = ['black', 'black', 'black', 'black'] , align ='left'
                                                  ),
                                    cells = dict(values = [transaction_names + extra_names, 
                                                           lr_report_data_1.values()[0] + lr_report_data_1.values()[1], 
                                                           lr_report_data_2.values()[0] + lr_report_data_2.values()[1], diff
                                                          ], 
                                                  align = 'left')
                                    )
  ])

  return table

