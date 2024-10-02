import os

from dotenv import load_dotenv

load_dotenv()

SOURCE_ID_TO_NAME_MAP = {
    os.environ["ML_PAPER_NOTES_DB_ID"]: "ml_paper_notes",
}