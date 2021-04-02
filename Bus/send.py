""" Module send.py
"""
import pika
import json
import yaml

from Hardware import Collect_Hardware




def send(component):
    """
    publish message to rabbitmq

    :param component: name of the hardware component
    :param data: data of the component
    """
    with open(r'config.yaml') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)

    USER = conf.get("user")
    data = Collect_Hardware.collect_data(component)
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
