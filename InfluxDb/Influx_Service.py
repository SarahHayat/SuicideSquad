from Hardware import Collect_Hardware
from datetime import datetime
import yaml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "uedzs7JQSQUVspWLfKgd0d8U074AATtXyzRt9XZvBjI3hK4_4LpBmjZm1YTfpSLZMntiVdE79tAZmwhDJaFRLw=="
org = "Python_project"
bucket = "test"
client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


def send_dict_influxdb(user, pointName, mainObject, field=False):
    if field:
        toIterate = mainObject.get(field)
    else:
        toIterate = mainObject
    for key in toIterate:
        point = Point(pointName).tag("host", user)
        if field:
            point.tag("data", field)
        point.field(key, toIterate.get(key)).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, point)


def send_battery_influx(user, batteryData):
    print(user, batteryData)
    send_dict_influxdb(user, "battery", batteryData)


def send_disk_influx(user, disksData):
    print(user, disksData)
    partitions = disksData.get("partitions")
    io_stats = disksData.get("io_stats")
    for partition in partitions:
        tags = ("host", user)
        tagsPart = ("partition", partition.get("device"))
        for key in partition:
            if (type(partition.get(key)) == int) | (type(partition.get(key)) == float):
                point = Point("disk").tag(*tags).tag(*tagsPart).field(key, partition.get(key)).time(datetime.utcnow(),
                                                                                                    WritePrecision.NS)
                write_api.write(bucket, org, point)
    for stat in io_stats:
        point = Point("disk").tag("host", user).field(stat, io_stats.get(stat)).time(datetime.utcnow(),
                                                                                     WritePrecision.NS)
        write_api.write(bucket, org, point)


def send_network_influx(user, networks_data):
    print(user, networks_data)
    for infos in networks_data.get("incoming"):
        point = Point("networks").tag("host", user).tag("direction", "in").field(infos, networks_data.get(
            "incoming").get(infos)).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, point)
    for infos in networks_data.get("out"):
        point = Point("networks").tag("host", user).tag("direction", "out").field(infos, networks_data.get("out").get(
            infos)).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, point)


def send_cpu_influx(user, cpu_data):
    print(user, cpu_data)
    send_dict_influxdb(user, "cpus", cpu_data, "times_dict")
    send_dict_influxdb(user, "cpus", cpu_data, "stats")
    for index, percent in enumerate(cpu_data.get("percent")):
        point = Point("cpus").tag("host", user).tag("data", "cpu_percent").field(index, percent).time(datetime.utcnow(),
                                                                                                      WritePrecision.NS)
        write_api.write(bucket, org, point)


def send_data(component, user, data):
    send_component = {
        "battery": send_battery_influx,
        "network": send_network_influx,
        "disk": send_disk_influx,
        "cpu": send_cpu_influx

    }
    send_component.get(component)(user, data)

