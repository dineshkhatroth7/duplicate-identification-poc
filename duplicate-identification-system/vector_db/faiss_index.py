# vector_db/faiss_index.py

import faiss
import numpy as np
from vector_db.embedding_service import create_embedding

# embedding size for sentence-transformers
index = faiss.IndexFlatL2(384)

candidate_store = []


class SearchResult:
    def __init__(self, candidate, score):
        self.candidate = candidate
        self.score = score


def add_candidate(candidate):
    """
    Add candidate vector to FAISS
    """

    vector = create_embedding(candidate["resume_text"])
    vector = np.array([vector]).astype("float32")

    index.add(vector)

    candidate_store.append(candidate)


def search_candidate(candidate, k=5):
    """
    Search similar candidates using FAISS
    """

    if len(candidate_store) == 0:
        return []

    vector = create_embedding(candidate["resume_text"])
    vector = np.array([vector]).astype("float32")

    distances, indices = index.search(vector, k)

    results = []

    for i, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        if idx < len(candidate_store):

            matched_candidate = candidate_store[idx]

            # convert L2 distance to similarity score
            distance = distances[0][i]

            similarity_score = 1 / (1 + distance)

            results.append(
                SearchResult(
                    candidate=matched_candidate,
                    score=similarity_score
                )
            )

    return results