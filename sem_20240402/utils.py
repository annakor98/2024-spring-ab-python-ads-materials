import json
import uuid
import redis
import pika
from prometheus_client import start_http_server, Gauge

#redis_instance = redis.Redis(host="redis-master.default.svc.cluster.local", port=6379, db=0)
redis_instance = redis.Redis(host="localhost", port=6379, db=0)

start_http_server(6000)

def publish_to_rabbitMQ(data):
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        #"hello-world.default.svc.cluster.local",
        "localhost",
        5672,
        credentials=credentials,
    ))
    channel = connection.channel()
    channel.queue_declare(queue='factorial_process', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='factorial_process',
        body=json.dumps(data)
    )
    connection.close()


def create_request(input):
    random_id = str(uuid.uuid4())
    redis_instance.set(
        random_id,
        json.dumps({
            'input': input,
            'status': 'processing',
            'output': ''
        })
    )
    publish_to_rabbitMQ({'request_id': random_id, 'input': input})
    return random_id


def get_request(request_id):
    request_data = redis_instance.get(request_id)
    if request_data:
        return json.loads(request_data)
    return None


def update_request(request_id, status, output):
    request_details = get_request(request_id)
    redis_instance.set(request_id, json.dumps({
        'input': request_details['input'],
        'status': status,
        'output': output,
    }))