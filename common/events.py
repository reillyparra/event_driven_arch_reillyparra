"""Definición de eventos: tipos y fábrica con la estructura estándar."""
import uuid
from datetime import datetime, timezone

# Tipos de evento del flujo
ORDER_PLACED = "OrderPlaced"
PAYMENT_APPLIED = "PaymentApplied"
ORDER_FULFILLED = "OrderFulfilled"
EMAIL_SENT = "EmailSent"


def create_event(event_type, producer, payload):
    """Crea un evento con la estructura estándar."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "producer": producer,
        "payload": payload,
    }
