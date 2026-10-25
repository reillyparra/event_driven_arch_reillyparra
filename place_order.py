"""Order placement (initiating event): crea una orden y publica OrderPlaced.

Uso: docker compose run --rm app python place_order.py
"""
import os
import time
import uuid

from common.broker import connect, publish, setup_channel
from common.events import EMAIL_SENT, ORDER_PLACED, create_event
from common.logger import LOG_FILE, log_action

PRODUCER = "order-placement"
TIMEOUT = 20  # segundos que espera a que termine el flujo para mostrarlo


def main():
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    payload = {
        "order_id": order_id,
        "customer": "Reilly Parra",
        "email": "reill.parra@iteso.mx",
        "items": [
            {"sku": "LAPTOP-01", "quantity": 1, "price": 15000.00},
            {"sku": "MOUSE-02", "quantity": 2, "price": 350.00},
        ],
        "total": 15700.00,
    }

    connection = connect()
    channel = setup_channel(connection)
    event = create_event(ORDER_PLACED, PRODUCER, payload)
    publish(channel, event)
    log_action(PRODUCER, "produced", event)
    connection.close()

    print(f"\nOrden {order_id} enviada. Esperando el resto del flujo...\n")
    show_flow(order_id)


def show_flow(order_id):
    """Imprime las líneas del log de esta orden hasta que llegue EmailSent."""
    deadline = time.time() + TIMEOUT
    lines = []
    while time.time() < deadline:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, encoding="utf-8") as f:
                lines = [l.rstrip() for l in f if f"order_id={order_id}" in l]
            if any(EMAIL_SENT in l for l in lines):
                break
        time.sleep(0.5)
    print(f"--- Flujo de {order_id} ---")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
