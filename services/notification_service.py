"""Notification Service: OrderFulfilled -> EmailSent (no envía correo real)."""
from common.events import EMAIL_SENT, ORDER_FULFILLED, create_event
from common.service import run_service

NAME = "notification-service"


def handle(event):
    payload = {**event["payload"], "channel": "email"}
    return [create_event(EMAIL_SENT, NAME, payload)]


if __name__ == "__main__":
    run_service(NAME, [ORDER_FULFILLED], handle)
