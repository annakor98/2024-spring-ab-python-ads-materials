import pika
import json
from utils import update_request


def calculate_factorial(n):
    result = 1
    if n > 1:
        for i in range(1, n+1):
            result = result * i
    return result


def callback(ch, method, properties, body):
    body = json.loads(body)
    request_id = body["request_id"]
    print(f'Received request with ID: {request_id}')
    input = body['input']
    output = calculate_factorial(input)
    update_request(
        request_id,
        'done',
        output
    )


def start_consumer():
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        #"hello-world.default.svc.cluster.local",
        "localhost",
        5672,
        credentials=credentials,
    ))

    channel = connection.channel()
    channel.queue_declare(queue='factorial_process', durable=True)
    channel.basic_consume(queue='factorial_process', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer()