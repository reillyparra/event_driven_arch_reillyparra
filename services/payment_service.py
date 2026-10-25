"""Payment Service: OrderPlaced -> PaymentApplied (no cobra nada real)."""
from common.events import ORDER_PLACED, PAYMENT_APPLIED, create_event
from common.service import run_service

NAME = "payment-service"


def handle(event):
    payload = {**event["payload"], "payment_status": "applied"}
    return [create_event(PAYMENT_APPLIED, NAME, payload)]


if __name__ == "__main__":
    run_service(NAME, [ORDER_PLACED], handle)
