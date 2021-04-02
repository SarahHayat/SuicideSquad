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


def get_data(client, measurement, host=None, time=None, additionalTag=None, tagFilter=None):
    results = []
    query = f'query = from(bucket: "python_week")'
    if time:
        query += f'|> range(start: -{time})'
    else:
        query += f'|> range(start: -1d)'
    query += f'|> filter(fn: (r) => r["_measurement"] == "{measurement}") '
    if tagFilter:
        query += f'|> filter(fn: (r) => r["{tagFilter[0]}"] == "{tagFilter[1]}") '
    if host:
        query += f'|> filter(fn: (r) => r["host"] == "{host}")'
    query += '|> yield(name: "mean")'

    result = client.query_api().query(org=org, query=query)
    for table in result:
        for record in table.records:
            return_value = dict({record.get_field(): record.get_value(),
                                 "time": utc_to_local(record.get_time()),
                                 "host": record.values.get("host")})
            if additionalTag:
                return_value[additionalTag] = record.values.get(additionalTag)
            results.append(return_value)
    return results


@app.route('/api/', methods=['GET'])
def api():

    measurement, host, time, additionalTag, tagFilter = None, None, None, None, None
    if 'host' in request.args:
        host = str(request.args['host'])
    if 'component' in request.args:
        measurement = str(request.args['component'])
    if 'time' in request.args:
        time = str(request.args['time'])
    if 'tag' in request.args:
        additionalTag = str(request.args['tag'])
    if 'filter' in request.args:

        tagFilter = request.args.getlist("filter")

    return jsonify(get_data(client, measurement, host, time, additionalTag, tagFilter))


app.run()

