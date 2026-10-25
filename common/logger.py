"""Evidencia del flujo: una línea por acción, a consola y a logs/events.log."""
import os
from datetime import datetime, timezone

LOG_FILE = os.getenv("LOG_FILE", "/logs/events.log")


def log_action(service, action, event):
    """Formato: timestamp | service - action - event_type | event_id | order_id"""
    order_id = event.get("payload", {}).get("order_id", "-")
    line = (
        f"{datetime.now(timezone.utc).isoformat()} | "
        f"{service} - {action} - {event['event_type']} | "
        f"event_id={event['event_id']} | order_id={order_id}"
    )
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
