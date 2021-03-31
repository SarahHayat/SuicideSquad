""" Module send.py
"""
import pika
import json
import yaml

with open(r'config.yaml') as file:
    yaml = yaml.load(file, Loader=yaml.FullLoader)

USER = yaml.get("user")


def send(component, data):
    """
    :param component:
    :param data:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logs', durable=True)

    body = {"user": USER, "component": component, "data": data}

    channel.basic_publish(exchange='', routing_key='logs', body=json.dumps(body),
                          properties=pika.BasicProperties(
                              delivery_mode=2
                          ))
    connection.close()
    print(f'Data from {USER}\'s {component} send')
