import json
from kafka import KafkaConsumer, KafkaProducer

from streaming.kafka_config import KAFKA_BROKER, CANDIDATE_TOPIC, DUPLICATE_RESULT_TOPIC

from backend.candidate_service import process_candidate
from database.connection import SessionLocal


consumer = KafkaConsumer(
    CANDIDATE_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="candidate-group"
)


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def start_consumer():

    print("Kafka consumer started...")

    for message in consumer:

        candidate = message.value

        print("Received candidate:", candidate)

        db = SessionLocal()

        try:

            result = process_candidate(candidate, db)

            print("Processing result:", result)

            # ✅ Send processed result to Kafka
            producer.send(DUPLICATE_RESULT_TOPIC, result)

            producer.flush()

        except Exception as e:

            print("Processing error:", e)

        finally:
            db.close()


if __name__ == "__main__":
    start_consumer()