import plotly.graph_objects as go

import lr_report_classes
from lr_report_dataset import db_official_report_count, db_official_report_list, colors



def create_release_scatter(db_data):
  scatter = go.Figure()
  clrStrt = 0
  most_money_makers = 0
  moneymakers = []
  moneymakers_per_report =[]
  totals = []
  
  ## find highest count of moneymakers ##
  for report in db_data:
    if report.lr_money_maker_count > most_money_makers:
      most_money_makers = report.lr_money_maker_count
      moneymakers = report.lr_moneymakers

  ## find all _Totals ##
  mmc = 0

  for report in db_data:
    for scenario in report.lr_transactions:
      if "_Total" in scenario.transaction_name:
        totals.append(scenario)
    
    moneymakers_per_report.append(mmc)

  ## Fill # of moneymaker lists of # of report entries ex. if 5 moneymakers and 10 reports it will be 5 lists each with 10 elements.
  scenario_percentiles = [[] for i in range (most_money_makers)]
  for i in range(most_money_makers):
    for j in range(db_official_report_count):
      scenario_percentiles[i].append(db_official_report_list[j])
  report_num = 0
  scenario_num = 0
  partition = totals[0].partition_0
  

  for i in range(len(totals)):
    
    ## if partition changes to another official partition ##
    if totals[i].partition_0 != partition:
      partition = totals[i].partition_0
      report_num += 1
      scenario_num = 0

    ## if the scenario is found
    if totals[i].transaction_name in moneymakers[scenario_num].transaction_name:
      scenario_percentiles[scenario_num][report_num] = totals[i].nintieth_percentile
  
    scenario_num+=1

  ## CREATE EACH LINE IN THE GRAPH
  for i in range(len(moneymakers)):
    scatter.add_trace(go.Scatter(name=moneymakers[i].transaction_name + " TOTAL ", mode = 'lines+markers', x=db_official_report_list, y=scenario_percentiles[i], line_width = 7, marker_size=15, line_color=colors[clrStrt]))
    clrStrt+=1

  scatter.update_layout(title = "90th Percentile of each MoneyMaker from release to release", margin=go.layout.Margin(l = 50, r= 50, b= 100, t=100, pad = 4))

  return scatter
