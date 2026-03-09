 
from ai.verifier import DuplicateVerifier

verifier = DuplicateVerifier()


def test_exact_duplicate():

    payload = {
        "new_candidate": {
            "name": "John Smith",
            "email": "john@gmail.com",
            "phone": "9876543210"
        },
        "potential_matches_from_db": [
            {
                "candidate_id": 1,
                "name": "John Smith",
                "email": "john@gmail.com",
                "phone": "9876543210"
            }
        ]
    }

    result = verifier.verify(payload)

    assert "confidence" in result


def test_email_duplicate():

    payload = {
        "new_candidate": {"email": "john@gmail.com"},
        "potential_matches_from_db": [{"email": "john@gmail.com"}]
    }

    result = verifier.verify(payload)

    assert result


def test_phone_duplicate():

    payload = {
        "new_candidate": {"phone": "9999999999"},
        "potential_matches_from_db": [{"phone": "9999999999"}]
    }

    result = verifier.verify(payload)

    assert result


def test_fuzzy_name_duplicate():

    payload = {
        "new_candidate": {"name": "Jon Smith"},
        "potential_matches_from_db": [{"name": "John Smith"}]
    }

    result = verifier.verify(payload)

    assert result


def test_unique_candidate():

    payload = {
        "new_candidate": {"name": "Alice Cooper"},
        "potential_matches_from_db": []
    }

    result = verifier.verify(payload)

    assert result