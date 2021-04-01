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
    req = requests.get(url=f"http://127.0.0.1:5000/api/?component=battery")
    return Helper.extract_list_of_value(json.loads(req.content), "charge")


def fetch_data_disk():
    req = requests.get(url=f"http://127.0.0.1:5000/api/?component=disk&time=6h")
    return json.loads(req.content)


df_disk = fetch_data_disk()
print(df_disk)
used = Helper.extract_list_of_value(df_disk, "used")
free = Helper.extract_list_of_value(df_disk, "free")
all_user_disk = Helper.extract_list_of_host(used)

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
    html.P("Names:"),
    dcc.Dropdown(
        id='names',
        options=[{'value': user, 'label': user}
                 for user in all_user_disk],
        value=all_user_disk[0],
        clearable=False
    ),
    dcc.Graph(id="pie-chart"),
])


@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value")])
def generate_chart(names):
    usedValue = Helper.extract_data_where_users(used, names)[-1]
    freeValue = Helper.extract_data_where_users(free, names)[-1]
    value = {'values': [usedValue.get("used"), freeValue.get("free")], names: ["used", "free"]}

    fig = px.pie(value, values='values', names=names)
    return fig


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
