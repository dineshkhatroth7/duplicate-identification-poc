import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.queries import insert_staging_candidate
from database.merge_logic import merge_candidates
from database.audit_log import log_merge_action
from database.connection import SessionLocal
from database.models import CandidateMain


db = SessionLocal()

main_candidate = CandidateMain(
    name="Test User",
    email="test@main.com",
    phone="8888888888",
    experience="5 years"
)

db.add(main_candidate)
db.commit()
db.refresh(main_candidate)
db.close()


staging_candidate = insert_staging_candidate({
    "name": "Test User",
    "email": "test@main.com",
    "phone": "8888888888",
    "experience": "5 years"
})


merge_result = merge_candidates(staging_candidate.id, main_candidate.id)
print("Merge Result:", merge_result)


audit_result = log_merge_action(
    staging_candidate.id,
    main_candidate.id,
    85,
    "AUTO_MERGE"
)

print("Audit Result:", audit_result)


print("\nTesting rollback with wrong IDs")

fail_result = merge_candidates(9999, 9999)

print("Failure Test Result:", fail_result)