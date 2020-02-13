## INITIALIZE THE DASH (flask) APPLICATION ##
## SETS THE LAYOUT ##



import dash
from lr_report_dataset import external_stylesheets
from lr_report_layout import layout

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout
application = app.server #must be called 'application' for AWS wsgl detection
app.config.suppress_callback_exceptions = True
