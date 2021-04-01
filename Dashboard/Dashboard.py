""" Module Dashboard
The dashboard
"""
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
from dash.dependencies import Output, Input
from flask import jsonify
from pandas import json_normalize

import Helpers_Pie

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cpu = requests.get(url="http://127.0.0.1:5000/api/v1/cpus/")
cpu_data = json.loads(cpu.content)
# print(cpu_data)

disk = requests.get(url="http://127.0.0.1:5000/api/v1/disk/")
disk_data = json.loads(disk.content)
# print(disk_data)

network = requests.get(url="http://127.0.0.1:5000/api/v1/networks/")
network_data = json.loads(network.content)
# print(network_data)

battery = requests.get(url="http://127.0.0.1:5000/api/v1/battery/")
battery_data = json.loads(battery.content)


# print(battery_data)


# df1 = json_normalize(disk_data)
# df_csv = df1.to_csv()


def fetch_data_pie():
    req = requests.get(url="http://127.0.0.1:5000/api/v1/disk/")
    return Helpers_Pie.extract_list_of_value(json.loads(req.content), "used", "free")


df = fetch_data_pie()
alluser = Helpers_Pie.extract_list_of_host(df)
app = dash.Dash(__name__)

# ---------------------------------------------------------------

app.layout = html.Div([
    html.P("Names:"),
    dcc.Dropdown(
        id='names',
        value='day',
        options=[{'value': x, 'label': x}
                 for x in ['smoker', 'day', 'time', 'sex']],
        clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(
        id='values',
        value='total_bill',
        options=[{'value': x, 'label': x}
                 for x in ['total_bill', 'tip', 'size']],
        clearable=False
    ),
    dcc.Graph(id="pie-chart"),
])

@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value"),
     Input("values", "value")])
def generate_chart(names, values):
    fig = px.pie(df, values=values, names=names)
    return fig

app.run_server(debug=True)

# df = pd.DataFrame(cpu_data["percent"])
#
# fig = px.bar(df, x=0, y=0, color=0, barmode="group")
#
# app.layout = html.Div(children=[
#     html.H1(children='CPU Dashboard'),
#
#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),
#
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])
#
# app.run_server(debug=True)
