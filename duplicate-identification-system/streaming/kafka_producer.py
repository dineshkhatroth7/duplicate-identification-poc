
import json
from kafka import KafkaProducer
from streaming.kafka_config import KAFKA_BROKER, CANDIDATE_TOPIC


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def send_candidate_event(candidate: dict):

    producer.send(CANDIDATE_TOPIC, candidate)

    producer.flush()

    print("Candidate event sent to Kafka")