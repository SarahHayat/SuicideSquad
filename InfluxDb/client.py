from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import json



# You can generate a Token from the "Tokens Tab" in the UI
token = "PtBVZKi-VDXbkoWYwSgAGatQzU5hMRSH4qzokhlKhBjcdkkaTCNTszrar9RM7MIeAO44MWvp_D10Cg3FKFaggA=="
org = "Python_project"
bucket = "Informations"

client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

# data = "mem,host=host1 used_percent=23.43234543"
# write_api.write(bucket, org, data)
#
# point = Point("mem").tag("host", "host1").field("used_percent", 23.43234543).time(datetime.utcnow(), WritePrecision.NS)
#
# write_api.write(bucket, org, point)
#

with open('data.json') as f:
  data = json.load(f)


sequence = []
for item in data["battery"]:
    sequence.append(f'battery,{item}={data["battery"][item]} {item}={data["battery"][item]}')

print(f'sequence : {sequence}')

write_api.write(bucket, org, sequence)

# query = f'from(bucket: \\"{bucket}\\") |> range(start: -1h)'
# tables = client.query_api().query(query, org=org)

