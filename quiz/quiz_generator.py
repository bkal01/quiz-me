from typing import Any, Dict, List

from openai import OpenAI
from pydantic import BaseModel

class Question(BaseModel):
    question_text: str

class Quiz(BaseModel):
    title: str
    questions: List[Question]

class QuizGenerator():
    def __init__(self, system_prompt: str, user_prompt: str) -> None:
        self.client = OpenAI()
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        
    def generate_quiz(self, content: Dict[str, Any]) -> str:
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
        return completion.choices[0].message.parsed