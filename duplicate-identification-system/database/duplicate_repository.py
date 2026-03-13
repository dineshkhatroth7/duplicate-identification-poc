from sqlalchemy.orm import Session
from database.models import DuplicateAuditLog


def create_duplicate_log(db: Session, log_data: dict):

    log = DuplicateAuditLog(
        candidate_id=log_data.get("candidate_id"),
        matched_candidate_id=log_data.get("matched_candidate_id"),
        match_type=log_data.get("match_type"),
        confidence_score=log_data.get("confidence_score"),
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log