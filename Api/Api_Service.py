""" Module Api_Service
APi
"""
import flask
from flask import jsonify

from Hardware.Collect_Hardware import get_cpu_informations, get_all_partition_all_usage, get_net_io_sent_recv, \
    get_battery_data, collect_all_data

app = flask.Flask(__name__)
app.config["DEBUG"] = True

all = collect_all_data()
cpu = get_cpu_informations()
disk = get_all_partition_all_usage()
network = get_net_io_sent_recv()
battery = get_battery_data()

@app.route('/api/v1/all', methods=['GET'])
def api_all():
    return jsonify(all)

@app.route('/api/v1/cpu/all', methods=['GET'])
def api_cpu():
    return jsonify(cpu)


@app.route('/api/v1/disk/all', methods=['GET'])
def api_disk():
    return jsonify(disk)


@app.route('/api/v1/network/all', methods=['GET'])
def api_network():
    return jsonify(network)


@app.route('/api/v1/battery/all', methods=['GET'])
def api_battery():
    return jsonify(battery)
app.run()