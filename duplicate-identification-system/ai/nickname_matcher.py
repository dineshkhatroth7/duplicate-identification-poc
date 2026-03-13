# ai/nickname_matcher.py

from difflib import SequenceMatcher


def nickname_match(name1: str, name2: str) -> float:
    """
    Simple nickname similarity using string matching
    """

    if not name1 or not name2:
        return 0.0

    name1 = name1.lower()
    name2 = name2.lower()

    similarity = SequenceMatcher(None, name1, name2).ratio()

    return round(similarity, 2)