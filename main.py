import os

from dotenv import load_dotenv

from db.connection import get_connection
from db.operations import add_review_item
from db.review_item import create_new_review_item

def main() -> None:
    load_dotenv()
    
    cnx = get_connection()
    
    review_item = create_new_review_item(
        page_id=os.environ["TEST_PAGE_ID"]
    )
    add_review_item(cnx, review_item)

if __name__ == "__main__":
    main()