from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .connection import Base


class CandidateStaging(Base):
    __tablename__ = "candidates_staging"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    experience = Column(String)
    status = Column(String, default="PENDING", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CandidateMain(Base):
    __tablename__ = "candidates_main"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    experience = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class MergeAuditLog(Base):
    __tablename__ = "merge_audit_log"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer)
    target_id = Column(Integer)
    confidence_score = Column(Integer)
    action = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)