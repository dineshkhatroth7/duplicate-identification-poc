from pydantic import BaseModel, field_validator
from typing import Optional


class CandidateRequest(BaseModel):
    candidate_id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    phone: str
    resume_text: str

    @field_validator("candidate_id")
    def validate_candidate_id(cls, value):

        # Allow None (optional field)
        if value is None:
            return value

        # Must be positive
        if value <= 0:
            raise ValueError("candidate_id must be a positive number")

        # Max length check (convert to string)
        if len(str(value)) > 6:
            raise ValueError("candidate_id length should be <= 6 digits")

        return value