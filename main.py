import os

from dotenv import load_dotenv

from notion.extractor import NotionExtractor
from quiz.quiz_generator import QuizGenerator

def main() -> None:
    load_dotenv()
    
    extractor = NotionExtractor()
    contents = extractor.extract(os.environ["TEST_PAGE_ID"])

    with open(os.environ["QUIZ_GENERATION_SYSTEM_PROMPT_PATH"]) as f:
        system_prompt = f.readlines()
    f.close()
    with open(os.environ["QUIZ_GENERATION_USER_PROMPT_PATH"]) as f:
        user_prompt = f.readlines()
    f.close()
    
    generator = QuizGenerator(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    quiz = generator.generate_quiz(contents)
    print(quiz.title)
    for question in quiz.questions:
        print(question.question_text)

if __name__ == "__main__":
    main()