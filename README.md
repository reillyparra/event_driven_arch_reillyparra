# Event Driven Architecture – Flujo de una orden

Simulación del flujo de una orden con arquitectura orientada a eventos usando
**RabbitMQ** (`pika`) y **Docker Compose**. Cada servicio y el broker corren en
un contenedor separado. No se implementan cobros ni envío de correos reales:
solo se generan los eventos.

## Flujo

```
Order placement (place_order.py) ──▶ OrderPlaced
                                        │
                                payment-service ──▶ PaymentApplied
                                                        │
                                          fulfillment-service ──▶ OrderFulfilled
                                                                      │
                                                        notification-service ──▶ EmailSent
```

| Servicio             | Consume        | Produce        |
|----------------------|----------------|----------------|
| order-placement      | –              | OrderPlaced    |
| payment-service      | OrderPlaced    | PaymentApplied |
| fulfillment-service  | PaymentApplied | OrderFulfilled |
| notification-service | OrderFulfilled | EmailSent      |

## Estructura

```
.
├── docker-compose.yml
├── Dockerfile               # imagen compartida por todos los servicios
├── requirements.txt
├── place_order.py           # order placement: evento inicial (OrderPlaced)
├── common/
│   ├── events.py            # tipos de evento y estructura estándar
│   ├── broker.py            # conexión y publicación en RabbitMQ
│   ├── logger.py            # evidencia (consola + logs/events.log)
│   └── service.py           # runner genérico de servicios
├── services/
│   ├── payment_service.py
│   ├── fulfillment_service.py
│   └── notification_service.py
└── logs/                    # events.log se genera al ejecutar
```

## Estructura de un evento

```json
{
  "event_id": "uuid",
  "event_type": "OrderPlaced",
  "timestamp": "2026-10-25T17:55:00+00:00",
  "producer": "order-placement",
  "payload": { "order_id": "ORD-1A2B3C4D", "customer": "...", "items": [], "total": 15700.0 }
}
```

## Cómo ejecutar

Requiere Docker Desktop corriendo.

```bash
docker compose run --rm app python place_order.py
```

Este comando construye la imagen, levanta RabbitMQ y los 3 servicios, espera a
que estén listos, publica la orden e imprime el flujo completo en consola.

Ejemplo de salida:

```
... | order-placement - produced - OrderPlaced | event_id=... | order_id=ORD-1A2B3C4D
... | payment-service - consumed - OrderPlaced | ...
... | payment-service - produced - PaymentApplied | ...
... | fulfillment-service - consumed - PaymentApplied | ...
... | fulfillment-service - produced - OrderFulfilled | ...
... | notification-service - consumed - OrderFulfilled | ...
... | notification-service - produced - EmailSent | ...
```

## Evidencia

- Consola: la imprime `place_order.py` y `docker compose logs`.
- Archivo: `logs/events.log` (se crea y se llena dinámicamente; está en `.gitignore`).
- Formato de línea: `timestamp | service - action - event_type | event_id | order_id`.
- Opcional: UI de RabbitMQ en http://localhost:15672 (guest / guest) mientras los contenedores estén arriba.

## Limpieza

```bash
docker compose down
```

## Cómo extender

- **Nuevo evento:** agregar la constante en `common/events.py`.
- **Nuevo servicio:** crear `services/x_service.py` con un `handle(event)` y llamar a
  `run_service(...)`; añadir su bloque en `docker-compose.yml`.

## Uso de IA

Para esta tarea utilicé **Claude** como herramienta de apoyo. Lo usé para:

- Generar la estructura inicial del proyecto y le di la organización de modulos (`common/`, `services/`).
- Escribir el código de los servicios, la conexión a RabbitMQ con `pika` y el registro de eventos en el log.
- Redactar el `Dockerfile`, el `docker-compose.yml` y este README.

Yo definí los requisitos y el flujo a simular (OrderPlaced, PaymentApplied, OrderFulfilled, EmailSent), y moldée la solución a una implementación simple, claramente con bajo acoplamiento y pues la facilidad de modificar. Después revisé el funcionamiento del sistema para poder explicarlo y probé la ejecución con:
`docker compose run --rm app python place_order.py`.