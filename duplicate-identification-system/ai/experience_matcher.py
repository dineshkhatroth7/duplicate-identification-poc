# ai/experience_matcher.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def experience_similarity(exp1: str, exp2: str) -> float:
    """
    Resume experience semantic similarity
    """

    if not exp1 or not exp2:
        return 0.0

    emb1 = model.encode([exp1])
    emb2 = model.encode([exp2])

    similarity = cosine_similarity(emb1, emb2)[0][0]

    return round(float(similarity), 2)