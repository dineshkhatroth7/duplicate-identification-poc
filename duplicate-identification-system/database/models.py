from sqlalchemy import Column, Integer, String, Text,Float,DateTime
from datetime import datetime
from database.connection import Base

class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, unique=True, index=True)

    first_name = Column(String)
    last_name = Column(String)

    email = Column(String, index=True)
    phone = Column(String)

    resume_text = Column(Text)

class DuplicateAuditLog(Base):

    __tablename__ = "duplicate_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer)
    matched_candidate_id = Column(Integer)
    match_type = Column(String)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)