import os

from datetime import date
from dotenv import load_dotenv

from db.connection import get_connection
from notion.extractor import NotionExtractor
from quiz.quiz_generator import QuizGenerator

def main() -> None:
    load_dotenv()
    
    cnx = get_connection()
    
    extractor = NotionExtractor(
        cnx=cnx,
        sources=[os.environ["ML_PAPER_NOTES_DB_ID"]]
    )
    
    extractor.pull_new_pages_from_source(extractor.sources[0])
    
    with open(os.environ["QUIZ_GENERATION_SYSTEM_PROMPT_PATH"]) as f:
        quiz_generator_system_prompt = f.readlines()
    with open(os.environ["QUIZ_GENERATION_USER_PROMPT_PATH"]) as f:
        quiz_generator_user_prompt = f.readlines()
    generator = QuizGenerator(
        cnx=cnx,
        system_prompt=quiz_generator_system_prompt,
        user_prompt=quiz_generator_user_prompt,
    )
    due_review_items = generator.get_review_items_due_today()
    
    quiz_save_dir = f"generated_quizzes/{date.today().strftime('%m_%d_%Y')}"
    os.makedirs(
        name=quiz_save_dir,
        exist_ok=True
    )
    responses_save_dir = f"quiz_responses/{date.today().strftime('%m_%d_%Y')}"
    os.makedirs(
        name=responses_save_dir,
        exist_ok=True
    )
    for item in due_review_items:
        print(f"Processing {item.page_id}")
        content = extractor.extract(
            block_id=item.page_id,
        )
        
        quiz = generator.generate_quiz(
            content=content,
        )
        with open(f"{quiz_save_dir}/{item.page_id}.txt", "w") as f:
            f.write(quiz.title)
            f.write("\n\n")
            for question in quiz.questions:
                f.write(question.question_text)
                f.write("\n\n")

        open(f"{responses_save_dir}/{item.page_id}.txt", "w")
if __name__ == "__main__":
    main()