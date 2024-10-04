import os

from argparse import ArgumentParser, Namespace
from datetime import date
from dotenv import load_dotenv
from tqdm import tqdm

from db.connection import get_connection
from notion.extractor import NotionExtractor
from quiz.quiz_generator import QuizGenerator

def generate(args: Namespace):
    load_dotenv()
    cnx = get_connection()
    
    extractor = NotionExtractor(
        cnx=cnx,
        sources=[os.environ["ML_PAPER_NOTES_DB_ID"]]
    )
    print("Fetching any new pages from Notion to add for review...")
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
    print("Getting review items due today...")
    due_review_items = generator.get_review_items_due_today()
    
    quiz_save_dir = f"generated_quizzes/{date.today().strftime('%m_%d_%Y')}"
    os.makedirs(
        name=quiz_save_dir,
        exist_ok=True
    )
    for item in tqdm(due_review_items):
        print(f"Fetching content for {item.page_id}...")
        content = extractor.extract(
            block_id=item.page_id,
        )
        
        print(f"Generating quiz for {item.page_id}")
        quiz = generator.generate_quiz(
            content=content,
        )
        
        print(f"Saving quiz for {item.page_id}...")
        with open(f"{quiz_save_dir}/{item.page_id}.txt", "w") as f:
            f.write(f"{quiz.title}\n\n")
            for question in quiz.questions:
                f.write(f"Q: {question.question_text}\n\n")
                f.write("A: \n\n")

def evaluate(args: Namespace):
    print("Not implemented yet.")

def parse_arguments()-> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    quiz_generation_subparser = subparsers.add_parser("gen", help="generate your quizzes due today")
    quiz_generation_subparser.set_defaults(func=generate)
    quiz_evaluation_subparser = subparsers.add_parser("eval", help="grade your completed quizzes for today")
    quiz_evaluation_subparser.set_defaults(func=evaluate)
    
    return parser.parse_args()

def main(args: Namespace) -> None:
    args.func(args)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)