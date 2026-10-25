"""Runner genérico: cada servicio solo define qué eventos consume y un handler."""
import json

from common.broker import EXCHANGE, connect, publish, setup_channel
from common.logger import log_action

READY_FILE = "/tmp/ready"  # lo usa el healthcheck de docker compose


def run_service(name, consumes, handler):
    """
    name:     nombre del servicio (aparece en el log)
    consumes: lista de event_type a los que se suscribe
    handler:  función(event) -> lista de eventos nuevos a publicar (o None)
    """
    connection = connect()
    channel = setup_channel(connection)

    queue = f"{name}.queue"
    channel.queue_declare(queue=queue, durable=True)
    for event_type in consumes:
        channel.queue_bind(queue=queue, exchange=EXCHANGE, routing_key=event_type)

    def on_message(ch, method, properties, body):
        event = json.loads(body)
        log_action(name, "consumed", event)
        for new_event in handler(event) or []:
            publish(ch, new_event)
            log_action(name, "produced", new_event)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=on_message)

    open(READY_FILE, "w").close()  # ya estamos suscritos: listo para recibir
    print(f"[{name}] esperando eventos: {consumes}", flush=True)
    channel.start_consuming()
