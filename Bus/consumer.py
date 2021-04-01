import pika
import json

from pika.exchange_type import ExchangeType

from InfluxDb.Influx_Service import send_data


def callback(ch, method, properties, body):
    """
            function to execute when publication 'logs' get consume

            send body to influxDb

    """
    dict_body = (json.loads(body))

    print(f'Publication Received: {dict_body.get("user")}\'s  {dict_body.get("component")}')
    send_data(dict_body.get("component"), dict_body.get("user"), dict_body.get("data"))


def consumer():
    """
             run consumer
             listen on 'logs'
             use function callback()

     """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(
        exchange="test_exchange",
        exchange_type=ExchangeType.direct,
        passive=False,
        durable=True,
        auto_delete=False)
    channel.queue_declare(queue='logs', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('logs', callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    consumer()
