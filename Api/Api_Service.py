""" Module Api_Service
APi
"""
import flask
from pytz import timezone as timez
from flask import jsonify, request
from datetime import timezone

from InfluxDb.Influx_Service import client, org

app = flask.Flask(__name__)
app.config["DEBUG"] = True

tz = timez('Europe/Paris')


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=tz)


def get_data(client, measurement, host=None):
    results = []
    if host:
        query = f'query = from(bucket: "python_week")\
        |> range(start: -10m)\
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")\
        |> filter(fn: (r) => r["host"] == "{host}")\
        |> yield(name: "mean")'


        print(f'query = {query}')
        result = client.query_api().query(org=org, query=query)

        for table in result:
            for record in table.records:
                results.append(dict({record.get_field(): record.get_value(),
                                     "time": utc_to_local(record.get_time()),
                                     "host": record.values.get("host")}))
    else:
        query = f'from(bucket: "python_week")\
                    |> range(start: -10m)\
                    |> filter(fn: (r) => r["_measurement"] == "{measurement}")'

        print(f'query = {query}')
        result = client.query_api().query(org=org, query=query)

        for table in result:
            for record in table.records:
                results.append(dict({record.get_field(): record.get_value(),
                                     "time": utc_to_local(record.get_time()),
                                     "host": record.values.get("host")}))

    return results


@app.route('/api/v1/cpus/', methods=['GET'])
def api_cpu():
    if 'host' in request.args:
        host = str(request.args['host'])
        return jsonify(get_data(client, "cpus", host))
    else:
        return jsonify(get_data(client, "cpus"))


@app.route('/api/v1/disk/', methods=['GET'])
def api_disk():
    if 'host' in request.args:
        host = str(request.args['host'])
        return jsonify(get_data(client, "disk", host))
    else:
        return jsonify(get_data(client, "disk"))


@app.route('/api/v1/networks/', methods=['GET'])
def api_network():
    if 'host' in request.args:
        host = str(request.args['host'])
        return jsonify(get_data(client, "networks", host))
    else:
        return jsonify(get_data(client, "networks"))


@app.route('/api/v1/battery/', methods=['GET'])
def api_battery():
    if 'host' in request.args:
        host = str(request.args['host'])
        return jsonify(get_data(client, "battery", host))
    else:
        return jsonify(get_data(client, "battery"))


app.run()
