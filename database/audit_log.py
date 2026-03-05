from sqlalchemy.exc import SQLAlchemyError
from .connection import SessionLocal
from .models import MergeAuditLog


def log_merge_action(source_id, target_id, score, action):
    db = SessionLocal()

    try:
        log = MergeAuditLog(
            source_id=source_id,
            target_id=target_id,
            confidence_score=score,
            action=action
        )

        db.add(log)
        db.commit()

        return "Audit logged successfully"

    except SQLAlchemyError as e:
        db.rollback()
        return f"Audit log failed: {str(e)}"

    finally:
        db.close()