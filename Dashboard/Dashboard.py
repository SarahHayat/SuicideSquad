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


def fetch_data_battery():
    """
            Get battery's data from Api.
    """
    req = requests.get(url=f"http://127.0.0.1:5000/api/?component=battery")
    return Helper.extract_list_of_value(json.loads(req.content), "charge")


def fetch_data_disk():
    """
                Get battery's disk from Api.
    """
    req = requests.get(url=f"http://127.0.0.1:5000/api/?component=disk&time=6h&tag=partition")
    return json.loads(req.content)


def fetch_data_network(filter):
    req = requests.get(url=f"http://127.0.0.1:5000/api/?component=networks&time=6h&filter=direction&filter={filter}")
    return Helper.extract_list_of_value(json.loads(req.content), "bytes")


df_disk = fetch_data_disk()
used = Helper.extract_list_of_value(df_disk, "used")
free = Helper.extract_list_of_value(df_disk, "free")
all_user_disk = Helper.extract_list_of_unique_value(used, "host")
all_partitions = Helper.extract_list_of_unique_value(df_disk, "partition")[:-2]

df = fetch_data_battery()
all_user = Helper.extract_list_of_unique_value(df, "host")

df_network_bytes_in = fetch_data_network("in")
df_network_bytes_out = fetch_data_network("out")
all_user_bytes_network = Helper.extract_list_of_unique_value(df, "host")

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
    html.P("Partition:"),
    dcc.Dropdown(
        id='partition',
        options=[{'value': partition, 'label': partition}
                 for partition in all_partitions],
        value=all_partitions[0],
        clearable=False
    ), dcc.Graph(id="pie-chart"),
    html.P("Network:"),
    dcc.Dropdown(
        id='network',
        options=[{'value': 'in', 'label': 'in'},
                 {'value': 'out', 'label': 'out'}],
        value='in',
        clearable=False
    ),
    dcc.Checklist(
        id="checklist-bytes-network",
        options=[{"label": user, "value": user}
                 for user in all_user],
        value=all_user_bytes_network,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart-bytes-network"),

])


@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value"), Input("partition", "value")])
def generate_chart(names, partition):
    usedValue = Helper.extract_data_where_is_value(used, names, "host")
    freeValue = Helper.extract_data_where_is_value(free, names, "host")
    usedValue = Helper.extract_data_where_is_value(usedValue, partition, "partition")
    freeValue = Helper.extract_data_where_is_value(freeValue, partition, "partition")
    if len(usedValue) == 0:
        usedValue = {"used": 0}
    else:
        usedValue = usedValue[-1]
    if len(freeValue) == 0:
        freeValue = {"free": 0}
    else:
        freeValue = freeValue[-1]

    value = {'values': [usedValue.get("used"), freeValue.get("free")], names: ["used", "free"]}

    fig = px.pie(value, values='values', names=names)
    return fig


@app.callback(
    dash.dependencies.Output('partition', 'options'),
    [dash.dependencies.Input('names', 'value')])
def update_output(names):
    usedValue = Helper.extract_data_where_is_value(used, names, "host")
    all_partitions = Helper.extract_list_of_unique_value(usedValue, "partition")[:-2]
    return [{'value': partition, 'label': partition}
            for partition in all_partitions]


@app.callback(
    Output("line-chart", "figure"),
    [Input("checklist", "value")])
def update_line_chart(users):
    df = fetch_data_battery()
    display = Helper.extract_data_where_is_value(df, users, "host")
    display = Helper.format_time_req(display)
    fig = px.line(display,
                  y="charge", x='time', color='host')
    return fig


@app.callback(
    Output("line-chart-bytes-network", "figure"),
    [Input("checklist-bytes-network", "value"), Input("network", "value")])
def update_line_chart_network(users, network):
    df_network_bytes = fetch_data_network(network)
    display = Helper.extract_data_where_is_value(df_network_bytes, users, "host")
    display = Helper.format_time_req(display)
    fig = px.line(display,
                  y="bytes", x="time", color='host')
    return fig


app.run_server(debug=True)
