### LAYOUT FOR WEBAPP PAGE ###

import dash_core_components as dcc
import dash_html_components as html

from lr_report_dataset import db_data, db_report_dict, db_official_data
from lr_scatter_tab import create_release_scatter

### Application complete UI layout
layout = html.Div([
               dcc.Tabs(id='tabs', children= [
                 dcc.Tab(label="Comparison Tab" , children = [ ## Tab with Bar Chart and Table
                   html.H1(children="MoneyMakers Comparison Report"),
                   dcc.Dropdown(
                       id = 'compare_1',
                       options = db_report_dict,
                       placeholder="Select Report 1 (PINK)",
                       searchable=True
                     ),
                   dcc.Dropdown(
                     id = 'compare_2',
                     options = db_report_dict,
                     placeholder = "Select Report 2 (BLUE)",
                     searchable=True
                     ),
                   ## BAR GRAPH
                   dcc.Graph (
                     id = 'barG'
                   ),
                   ## TABLE
                   dcc.Graph(
                     id = 'compare_table'
                   )
                 ]),
                 dcc.Tab(label="Release Scatter Plot", children = [ # Tab with line graph data
                   html.H1(children="Release to Release MoneyMaker Comparison"),
                   dcc.Graph(
                     id = 'scatG',
                     figure = create_release_scatter(db_official_data)
                   )
                 ])
               ])
             ])

