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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cpu = requests.get(url="http://127.0.0.1:5000/api/v1/cpu/all")
cpu_data = json.loads(cpu.content)
print(cpu_data)

disk = requests.get(url="http://127.0.0.1:5000/api/v1/disk/all")
disk_data = json.loads(cpu.content)
print(disk_data)

network = requests.get(url="http://127.0.0.1:5000/api/v1/network/all")
network_data = json.loads(cpu.content)
print(network_data)

battery = requests.get(url="http://127.0.0.1:5000/api/v1/battery/all")
battery_data = json.loads(cpu.content)
print(battery_data)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(cpu_data["percent"])

fig = px.bar(df, x=0, y=0, color=0, barmode="group")

app.layout = html.Div(children=[
    html.H1(children='CPU Dashboard'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

app.run_server(debug=True)