import pika
import json

from InfluxDb.Influx_Service import send_data


def callback(ch, method, properties, body):
    dict_body = (json.loads(body))
    print(f' [*] Job Received: {dict_body.get("user")}\'s  {dict_body.get("component")}')
    send_data(dict_body.get("component"), dict_body.get("user"), dict_body.get("data"))


def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logs', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('logs', callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    consumer()