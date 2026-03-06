import json

def publish_candidate(data):
    print("Sending to Kafka topic: candidate-verification")
    print(json.dumps(data, indent=2)) 