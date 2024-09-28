import random
import string
import unittest

from datetime import date, timedelta

from db.review_item import ReviewItem
from quiz.evaluator import Evaluator

class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator(
            system_prompt="",
            user_prompt="",
        )
        self.review_item_old = ReviewItem(
            page_id="".join(random.choices(string.ascii_letters + string.digits, k=32)),
            initial_learning_date=date.today() - timedelta(1),
            last_reviewed_date=date.today() ,
            next_review_date= date.today() + timedelta(1),
            ease_factor=3,
            review_interval=1,
            # This item has been repeated many times.
            repetition_count=5,
        )

        self.review_item_new = ReviewItem(
            page_id="".join(random.choices(string.ascii_letters + string.digits, k=32)),
            initial_learning_date=date.today() - timedelta(1),
            last_reviewed_date=date.today() ,
            next_review_date= date.today() + timedelta(1),
            ease_factor=3,
            review_interval=1,
            # This item has been repeated just once.
            repetition_count=1,
        )
        
        self.review_item_easy = ReviewItem(
            page_id="".join(random.choices(string.ascii_letters + string.digits, k=32)),
            initial_learning_date=date.today() - timedelta(1),
            last_reviewed_date=date.today() ,
            next_review_date= date.today() + timedelta(1),
            # Easy review item.
            ease_factor=10,
            review_interval=1,
            repetition_count=1,
        )
        
        self.review_item_hard = ReviewItem(
            page_id="".join(random.choices(string.ascii_letters + string.digits, k=32)),
            initial_learning_date=date.today() - timedelta(1),
            last_reviewed_date=date.today() ,
            next_review_date= date.today() + timedelta(1),
            # Hard review item.
            ease_factor=1.3,
            review_interval=1,
            repetition_count=1,
        )
    
    def test_update_review_item_age(self):
        # If we do poorly on an old review item, we expect the repetition/review interval to refresh.
        updated_review_item = self.evaluator.update_review_item(self.review_item_old, 0)
        self.assertEqual(updated_review_item.repetition_count, 0)
        self.assertEqual(updated_review_item.review_interval, 1)
        
        # If we do well on an old review_item, we expect the repetition/review interval to increase.
        updated_review_item = self.evaluator.update_review_item(self.review_item_old, 5)
        self.assertEqual(updated_review_item.repetition_count, 6) # increment repetition count
        self.assertEqual(updated_review_item.review_interval, 3)  # multiply old interval by ease factor
        
        # If we do poorly on a new review item, we expect the repetition/review interval to refresh.
        updated_review_item = self.evaluator.update_review_item(self.review_item_new, 0)
        self.assertEqual(updated_review_item.repetition_count, 0)
        self.assertEqual(updated_review_item.review_interval, 1)
        
        # If we do well on an old review_item, we expect the repetition/review interval to increase.
        updated_review_item = self.evaluator.update_review_item(self.review_item_new, 5)
        self.assertEqual(updated_review_item.repetition_count, 2) # increment repetition count
        self.assertEqual(updated_review_item.review_interval, 6)  # set to 6
        
    def test_update_review_item_ease(self):
        # If we do poorly on an easy review item, then ease factor should drop and review interval/repetition count should refresh.
        updated_review_item = self.evaluator.update_review_item(self.review_item_easy, 0)
        self.assertEqual(updated_review_item.repetition_count, 0)
        self.assertEqual(updated_review_item.review_interval, 1)
        self.assertEqual(updated_review_item.ease_factor, 9.2)
        
        # If we do well on an easy review item, then ease factor should increase and review interval/repetition count should increase.
        updated_review_item = self.evaluator.update_review_item(self.review_item_easy, 5)
        self.assertEqual(updated_review_item.repetition_count, 2) # increment repetition count
        self.assertEqual(updated_review_item.review_interval, 6)  # set to 6
        self.assertEqual(updated_review_item.ease_factor, 10.1)
        
        # If we do poorly on an hard review item, then ease factor should drop and review interval/repetition count should refresh.
        updated_review_item = self.evaluator.update_review_item(self.review_item_hard, 0)
        self.assertEqual(updated_review_item.repetition_count, 0)
        self.assertEqual(updated_review_item.review_interval, 1)
        self.assertEqual(updated_review_item.ease_factor, 1.3)
        
        # If we do well on an hard review_item, then ease factor should increase and review interval/repetition count should increase.
        updated_review_item = self.evaluator.update_review_item(self.review_item_hard, 5)
        self.assertEqual(updated_review_item.repetition_count, 2) # increment repetition count
        self.assertEqual(updated_review_item.review_interval, 6)  # set to 6
        self.assertEqual(updated_review_item.ease_factor, 1.4)
        
        
if __name__ == "__main__":
    unittest.main()