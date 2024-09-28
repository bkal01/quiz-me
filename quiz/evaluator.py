from copy import deepcopy
from typing import Dict, Tuple

from openai import OpenAI
from pydantic import BaseModel

from db.review_item import ReviewItem

class Evaluation(BaseModel):
    feedback: Dict[str, str]
    grade: int
    

class Evaluator:
    def __init__(self, system_prompt: str, user_prompt: str) -> None:
        self.client = OpenAI()
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
    
    def grade_quiz(self, notes: Dict[str, str], quiz: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """
        quiz: a dictionary mapping questions to user-generated answers.
        Asks an LLM to grade the quiz. Returns two outputs: a dictionary mapping questions to feedback, and an integer grade from 0 to 5.
        """
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": str(self.system_prompt)},
                {
                    "role": "user",
                    "content": f"{self.user_prompt}\n{quiz}",
                }
            ],
            response_format=Evaluation,
        )
        print(completion.choices[0].message.parsed)
        return dict(), 0

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