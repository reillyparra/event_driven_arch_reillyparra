"""Conexión y publicación en RabbitMQ (pika)."""
import json
import os
import time

import pika

EXCHANGE = "events"


def connect(retries=30, delay=2):
    """Conecta a RabbitMQ reintentando hasta que el broker esté listo."""
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    for _ in range(retries):
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=host, heartbeat=60)
            )
        except pika.exceptions.AMQPConnectionError:
            time.sleep(delay)
    raise RuntimeError(f"No se pudo conectar a RabbitMQ en {host}")


def setup_channel(connection):
    """Abre un canal y declara el exchange (tipo topic, routing key = event_type)."""
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    return channel


def publish(channel, event):
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=event["event_type"],
        body=json.dumps(event),
        properties=pika.BasicProperties(
            delivery_mode=2, content_type="application/json"
        ),
    )
