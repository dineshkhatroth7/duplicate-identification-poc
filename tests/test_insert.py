import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.queries import insert_staging_candidate, fetch_pending_candidates


candidate = insert_staging_candidate({
    "name": "Shiva Kumar",
    "email": "shiva@test.com",
    "phone": "9999999999",
    "experience": "3 years Python"
})

print("Inserted Candidate ID:", candidate.id)

pending = fetch_pending_candidates()

print("\nPending Candidates:")
for p in pending:
    print(p.id, p.name, p.email)