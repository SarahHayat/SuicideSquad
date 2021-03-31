import argparse
from pprint import pprint

import yaml


def execute():
    pprint(parse_args(create_parser()))


def create_parser():
    parser = argparse.ArgumentParser(description="""Python Week project collect data on your hardware send it to 
influxDbCloud via rabbitmq queuebeautify them in grafana and a dash powered website and hack the nasa""")

    g = parser.add_argument_group('Config Value')
    g.add_argument('--user', default=str, help='user name to find data in db')
    g.add_argument('--timer', type=int, help='timer value for cpu collection if 0 no collection')
    return parser


def parse_args(parser):
    args = parser.parse_args()
    with open(r'config.yaml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    arg_dict = args.__dict__
    for key, value in arg_dict.items():
        if value:
            data[key] = value
    with open('config.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


execute()
