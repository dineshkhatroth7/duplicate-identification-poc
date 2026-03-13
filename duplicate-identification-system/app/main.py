from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from schemas.candidate_schema import CandidateRequest

from database.connection import get_db, engine
from database.models import Base

# Kafka Producer
from streaming.kafka_producer import send_candidate_event

app = FastAPI(title="Duplicate Candidate Detection System")

# Create tables automatically
Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "Duplicate Detection API Running"}


@app.post("/duplicate-check")
def duplicate_check(candidate: CandidateRequest):

    # Convert Pydantic model to dict
    candidate_data = candidate.dict()

    # Send event to Kafka
    send_candidate_event(candidate_data)

    return {
        "message": "Candidate sent to Kafka for processing"
    }