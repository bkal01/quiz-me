from typing import Any, Dict, List

from datetime import date
from mysql.connector import MySQLConnection
from openai import OpenAI
from pydantic import BaseModel

from db.operations import fetch_due_review_items
from db.review_item import ReviewItem

class Question(BaseModel):
    question_text: str

class Quiz(BaseModel):
    title: str
    questions: List[Question]

class QuizGenerator():
    def __init__(self, cnx: MySQLConnection, system_prompt: str, user_prompt: str) -> None:
        self.cnx = cnx
        self.client = OpenAI()
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        
    def get_review_items_due_today(self) -> List[ReviewItem]:
        due_review_items = fetch_due_review_items(
            cnx=self.cnx,
            due_date=date.today(),
        )
        if len(due_review_items) == 0:
            print("No items to review today.")
        return due_review_items
        
    def generate_quiz(self, content: Dict[str, Any]) -> Quiz:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": str(self.system_prompt)},
                {
                    "role": "user",
                    "content": f"{self.user_prompt}\n{content}",
                }
            ],
            response_format=Quiz,
        )
        quiz_data = completion.choices[0].message.parsed
        return quiz_data