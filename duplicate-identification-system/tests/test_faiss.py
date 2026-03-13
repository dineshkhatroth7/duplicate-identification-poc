
from vector_db.faiss_index import add_candidate,search_candidate
def test_vector_search():
    c={"name":"John","email":"john@gmail.com","phone":"999","resume_text":"Python Dev"}
    add_candidate(c)
    r=search_candidate(c)
    assert len(r)>0
