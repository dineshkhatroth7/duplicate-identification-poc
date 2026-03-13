
def decide(score):
    if score>0.85: return "DUPLICATE"
    if score>0.65: return "REVIEW"
    return "NEW"
