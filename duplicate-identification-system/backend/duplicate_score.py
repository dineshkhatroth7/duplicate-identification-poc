def calculate_duplicate_score(email_match, phone_match, vector_score):

    score = 0

    if email_match:
        score += 100

    if phone_match:
        score += 90

    if vector_score:
        score += int(vector_score * 100)

    return min(score, 100)