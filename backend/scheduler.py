def calculate_next_interval(prev_int, recall, easiness=2.5):
    easiness_new = easiness + (0.1 - (5 - recall) * (0.08 + (5 - recall) * 0.02))
    easiness_new = max(1.3, easiness_new)
    return max(1, round(prev_int * easiness_new if recall > 2 else 1, 2))
