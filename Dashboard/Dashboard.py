""" Module Dashboard
The dashboard
"""
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import Helper


def fetch_data():
    req = requests.get(url=f"http://127.0.0.1:5000/api/v1/battery/")
    return Helper.extract_list_of_value(json.loads(req.content), "charge")


df = fetch_data()
all_user = Helper.extract_list_of_host(df)
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(
        id="checklist",
        options=[{"label": user, "value": user}
                 for user in all_user],
        value=all_user,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart"),
])


@app.callback(
    Output("line-chart", "figure"),
    [Input("checklist", "value")])
def update_line_chart(users):
    df = fetch_data()
    display = Helper.extract_data_where_users(df, users)
    fig = px.line(display,
                  y="charge", x="time", color='user')
    return fig


app.run_server(debug=True)
