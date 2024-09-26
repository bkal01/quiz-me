import os

from datetime import date, timedelta
from dotenv import load_dotenv

from db.connection import get_connection
from db.operations import add_review_item, fetch_due_review_items
from db.review_item import create_new_review_item

def main() -> None:
    load_dotenv()
    
    cnx = get_connection()
    
    review_item = create_new_review_item(
        page_id=os.environ["TEST_PAGE_ID"]
    )
    add_review_item(
        cnx=cnx, 
        review_item=review_item,
    )
    
    due_date = date.today() + timedelta(1)
    review_items = fetch_due_review_items(
        cnx=cnx,
        due_date=due_date,
    )
    assert len(review_items) == 1
    print(f"Original page_id: {os.environ['TEST_PAGE_ID']}")
    print(f"page_id in db: {review_items[0].page_id}")
    

if __name__ == "__main__":
    main()