
from vector_db.embedding_service import create_embedding
def test_embedding():
    emb=create_embedding("Python developer")
    assert len(emb)>0
