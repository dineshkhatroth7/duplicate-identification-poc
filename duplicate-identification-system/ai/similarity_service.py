# ai/similarity_service.py

from ai.nickname_matcher import nickname_match
from ai.experience_matcher import experience_similarity


def ai_duplicate_check(candidate, matched_candidate):

    # Convert SQLAlchemy object to values safely
    name1 = f"{candidate.get('first_name','')} {candidate.get('last_name','')}".strip()

    name2 = f"{matched_candidate.first_name} {matched_candidate.last_name}".strip()

    nickname_score = nickname_match(name1, name2)

    exp1 = candidate.get("resume_text", "")
    exp2 = matched_candidate.resume_text or ""

    exp_score = experience_similarity(exp1, exp2)

    ai_score = (nickname_score + exp_score) / 2

    return {
        "nickname_score": nickname_score,
        "experience_score": exp_score,
        "ai_score": ai_score
    }