from Hardware import Collect_Hardware
from datetime import datetime
import yaml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "uedzs7JQSQUVspWLfKgd0d8U074AATtXyzRt9XZvBjI3hK4_4LpBmjZm1YTfpSLZMntiVdE79tAZmwhDJaFRLw=="
org = "Python_project"
bucket = "python_week"
client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

with open(r'config.yaml') as file:
    yaml = yaml.load(file, Loader=yaml.FullLoader)

HOST = yaml.get("user")


def send_dict_influxdb(pointName, mainObject, field=False):
    if field:
        toIterate = mainObject.get(field)
    else:
        toIterate = mainObject
    for key in toIterate:
        point = Point(pointName).tag("host", HOST)
        if field:
            point.tag("data", field)
        point.field(key, toIterate.get(key)).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, point)


def send_battery_influx():
    battery = Collect_Hardware.get_battery_data()
    send_dict_influxdb("battery", battery)
    print("battery send")


def send_disk_influx():
    disks = Collect_Hardware.get_all_partition_all_usage()
    partitions = disks.get("partitions")
    io_stats = disks.get("io_stats")
    for partition in partitions:
        tags = ("host", HOST)
        tagsPart = ("partition", partition.get("device"))
        for key in partition:
            if (type(partition.get(key)) == int) | (type(partition.get(key)) == float):
                point = Point("disk").tag(*tags).tag(*tagsPart).field(key, partition.get(key)).time(datetime.utcnow(),
                                                                                                    WritePrecision.NS)
                write_api.write(bucket, org, point)
    for stat in io_stats:
        point = Point("disk").tag("host", HOST).field(stat, io_stats.get(stat)).time(datetime.utcnow(),
                                                                                     WritePrecision.NS)
        write_api.write(bucket, org, point)
    print("disk send")


# networks

def send_network_influx():
    networks = Collect_Hardware.get_net_io_sent_recv()
    tags = ("host", HOST)
    for infos in networks.get("incoming"):
        point = Point("networks").tag("host", HOST).tag("direction", "in").field(infos, networks.get(
            "incoming").get(infos)).time(
            datetime.utcnow(),
            WritePrecision.NS)
        write_api.write(bucket, org, point)
    for infos in networks.get("out"):
        point = Point("networks").tag("host", HOST).tag("direction", "out").field(infos,
                                                                                  networks.get("out").get(
                                                                                      infos)).time(
            datetime.utcnow(),
            WritePrecision.NS)
        write_api.write(bucket, org, point)


print("network send")


def send_cpu_influx():
    cpus = Collect_Hardware.get_cpu_informations()
    send_dict_influxdb("cpus", cpus, "times_dict")
    send_dict_influxdb("cpus", cpus, "stats")
    for index, percent in enumerate(cpus.get("percent")):
        point = Point("cpus").tag("host", HOST).tag("data", "cpu_percent").field(index, percent).time(datetime.utcnow(),
                                                                                                      WritePrecision.NS)
        write_api.write(bucket, org, point)
    print("cpu send")
