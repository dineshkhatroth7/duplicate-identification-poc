# tests/test_detect_duplicates_full.py
import pytest
from unittest.mock import patch, MagicMock

from backend.duplicate_detector import detect_duplicates

# -----------------------------
# Helper mocks
# -----------------------------
def mock_candidate_not_found(*args, **kwargs):
    return None

def mock_search_no_matches(candidate):
    return []

def mock_search_matches(score=0.85):
    class Match:
        def __init__(self, score):
            self.score = score
    return [Match(score)]

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def db_mock():
    return MagicMock()

candidate_base = {
    "candidate_id": "CAND123",
    "email": "test@example.com",
    "phone": "1234567890"
}

# -----------------------------
# Main Duplicate Detection Tests
# -----------------------------

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id")
@patch("backend.duplicate_detector.get_candidate_by_email")
@patch("backend.duplicate_detector.get_candidate_by_phone")
@patch("backend.duplicate_detector.search_candidate")
@patch("backend.duplicate_detector.calculate_duplicate_score")
def test_id_duplicate(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    mock_id.side_effect = lambda db, cid: {"candidate_id": cid}
    mock_email.side_effect = mock_candidate_not_found
    mock_phone.side_effect = mock_candidate_not_found
    mock_search.side_effect = mock_search_no_matches
    mock_score.side_effect = lambda **kwargs: 50

    result = detect_duplicates(candidate_base, db_mock)

    assert result["status"] == "ID_DUPLICATE"
    assert result["signals"]["id_match"] is True
    mock_log.assert_called_once()  # Log should be called

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id")
@patch("backend.duplicate_detector.get_candidate_by_email")
@patch("backend.duplicate_detector.get_candidate_by_phone")
@patch("backend.duplicate_detector.search_candidate")
@patch("backend.duplicate_detector.calculate_duplicate_score")
def test_email_duplicate_high_score(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    mock_id.side_effect = mock_candidate_not_found
    mock_email.side_effect = lambda db, email: {"email": email}
    mock_phone.side_effect = mock_candidate_not_found
    mock_search.side_effect = lambda candidate: mock_search_matches(score=0.95)
    mock_score.side_effect = lambda **kwargs: 95

    result = detect_duplicates(candidate_base, db_mock)
    assert result["status"] == "HIGH_DUPLICATE"
    assert result["signals"]["email_match"] is True
    assert result["signals"]["semantic_similarity"] == 0.95
    mock_log.assert_called_once()  # Log should be called

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id")
@patch("backend.duplicate_detector.get_candidate_by_email")
@patch("backend.duplicate_detector.get_candidate_by_phone")
@patch("backend.duplicate_detector.search_candidate")
@patch("backend.duplicate_detector.calculate_duplicate_score")
def test_possible_duplicate(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    mock_id.side_effect = mock_candidate_not_found
    mock_email.side_effect = mock_candidate_not_found
    mock_phone.side_effect = mock_candidate_not_found
    mock_search.side_effect = lambda candidate: mock_search_matches(score=0.75)
    mock_score.side_effect = lambda **kwargs: 75

    result = detect_duplicates(candidate_base, db_mock)
    assert result["status"] == "POSSIBLE_DUPLICATE"
    assert result["signals"]["semantic_similarity"] == 0.75
    mock_log.assert_called_once()

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_email", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_phone", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.search_candidate", side_effect=mock_search_no_matches)
@patch("backend.duplicate_detector.calculate_duplicate_score", side_effect=lambda **kwargs: 0)
def test_new_candidate(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    candidate = candidate_base.copy()
    result = detect_duplicates(candidate, db_mock)
    assert result["status"] == "NEW"
    # Log should NOT be called for new candidates
    mock_log.assert_not_called()

# -----------------------------
# Edge Case Tests
# -----------------------------

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_email", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_phone", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.search_candidate", side_effect=mock_search_no_matches)
@patch("backend.duplicate_detector.calculate_duplicate_score", side_effect=lambda **kwargs: 0)
def test_missing_email_and_phone(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    candidate = {"candidate_id": "CAND001"}
    result = detect_duplicates(candidate, db_mock)
    assert result["status"] == "NEW"
    mock_log.assert_not_called()

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_email", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_phone", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.search_candidate", side_effect=mock_search_no_matches)
@patch("backend.duplicate_detector.calculate_duplicate_score", side_effect=lambda **kwargs: 0)
def test_empty_candidate_dict(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    candidate = {}
    result = detect_duplicates(candidate, db_mock)
    assert result["status"] == "NEW"
    mock_log.assert_not_called()

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_email", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_phone", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.search_candidate", side_effect=lambda candidate: mock_search_matches(score=1.2))
@patch("backend.duplicate_detector.calculate_duplicate_score", side_effect=lambda **kwargs: 105)
def test_vector_score_over_1(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    candidate = {"candidate_id": "CAND002", "email": "test2@example.com"}
    result = detect_duplicates(candidate, db_mock)
    assert result["signals"]["semantic_similarity"] == 1.2
    assert result["status"] == "HIGH_DUPLICATE"
    mock_log.assert_called_once()

@patch("backend.duplicate_detector.create_duplicate_log")
@patch("backend.duplicate_detector.get_candidate_by_id", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_email", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.get_candidate_by_phone", side_effect=mock_candidate_not_found)
@patch("backend.duplicate_detector.search_candidate", side_effect=mock_search_no_matches)
@patch("backend.duplicate_detector.calculate_duplicate_score", side_effect=lambda **kwargs: 70)
def test_score_exact_threshold(mock_score, mock_search, mock_phone, mock_email, mock_id, mock_log, db_mock):
    candidate = {"candidate_id": "CAND003", "email": "test3@example.com"}
    result = detect_duplicates(candidate, db_mock)
    assert result["status"] == "POSSIBLE_DUPLICATE"
    mock_log.assert_called_once()