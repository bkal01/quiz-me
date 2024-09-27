from copy import deepcopy
from db.review_item import ReviewItem

class Evaluator:
    def __init__(self) -> None:
        return

    def update_review_item(self, review_item: ReviewItem, grade: int) -> ReviewItem:
        """
        review_item: the review item which we want to apply the algorithm to.
        grade: score, from 0 to 5, with which we recalled this review item.
        Applies the SM-2 algorithm to the review item, updating its repetition number, ease factor, and review interval.
        """
        n = review_item.repetition_count
        ef = review_item.ease_factor
        i = review_item.review_interval
        
        n_new = -1
        ef_new = -1
        i_new = -1
        # correct response
        if grade > 3:
            if n == 0:
                i_new = 1
            elif n == 1:
                i_new = 6
            else:
                i_new = (i * ef) // 1
                if i_new == 0:
                    i_new = 1
            n_new = n + 1
        # incorrect response
        else:
            n_new = 0
            i_new = 1
        
        ef_new = round(ef + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)), 2)
        if ef_new < 1.3:
            ef_new = 1.3
        
        new_review_item = deepcopy(review_item)
        new_review_item.repetition_count = n_new
        new_review_item.ease_factor = ef_new
        new_review_item.review_interval = i_new
        
        return new_review_item