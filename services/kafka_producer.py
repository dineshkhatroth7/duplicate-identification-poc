import json


def publish_candidate(data: dict):
    """
    Publish candidate to Kafka topic
    (Currently mocked for POC)
    """

    try:

        print("Sending to Kafka topic: candidate-verification")

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        raise Exception(f"Kafka publish failed: {str(e)}")