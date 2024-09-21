from dotenv import load_dotenv
import json
import os

from notion_client import Client

load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])

paper_notes_page = notion.pages.retrieve(
    page_id=os.environ["PAPER_NOTES_PAGE_ID"]
)

ml_paper_notes_db = notion.databases.query(
    database_id=os.environ["ML_PAPER_NOTES_DB_ID"]
)

notes_page_id = ml_paper_notes_db["results"][0]["id"]

blocks = notion.blocks.children.list(
    block_id=notes_page_id,
)
print(blocks)