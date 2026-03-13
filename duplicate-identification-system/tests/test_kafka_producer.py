from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

candidate = {
    "candidate_id": "200",
    "email": "test@test.com",
    "phone": "9999999999"
}

producer.send("candidate-topic", candidate)

print("Event sent to Kafka")