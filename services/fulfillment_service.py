"""Order Fulfillment Service: PaymentApplied -> OrderFulfilled."""
from common.events import ORDER_FULFILLED, PAYMENT_APPLIED, create_event
from common.service import run_service

NAME = "fulfillment-service"


def handle(event):
    payload = {**event["payload"], "status": "fulfilled"}
    return [create_event(ORDER_FULFILLED, NAME, payload)]


if __name__ == "__main__":
    run_service(NAME, [PAYMENT_APPLIED], handle)
