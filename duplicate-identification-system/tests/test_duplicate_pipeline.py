from schemas.candidate_schema import CandidateRequest
import pytest


def test_valid_candidate_id():

    data = {
        "candidate_id": "15",
        "name": "John",
        "email": "john@test.com",
        "phone": "9876543210",
        "resume_text": "Python developer"
    }

    obj = CandidateRequest(**data)

    assert obj.candidate_id == "15"


def test_empty_candidate_id():

    data = {
        "candidate_id": "",
        "name": "John",
        "email": "john@test.com",
        "phone": "9876543210",
        "resume_text": "Python developer"
    }

    with pytest.raises(ValueError):
        CandidateRequest(**data)


def test_invalid_candidate_id_string():

    data = {
        "candidate_id": "abchakuh",
        "name": "John",
        "email": "john@test.com",
        "phone": "9876543210",
        "resume_text": "Python developer"
    }

    with pytest.raises(ValueError):
        CandidateRequest(**data)


def test_candidate_id_too_long():

    data = {
        "candidate_id": "123456789",
        "name": "John",
        "email": "john@test.com",
        "phone": "9876543210",
        "resume_text": "Python developer"
    }

    with pytest.raises(ValueError):
        CandidateRequest(**data)