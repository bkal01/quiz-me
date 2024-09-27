import os
import random
import string

from datetime import date, timedelta
from dotenv import load_dotenv

from db.connection import get_connection
from db.operations import add_review_item, batch_update_review_items, delete_review_item, fetch_due_review_items
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
    
    another_review_item = create_new_review_item(
        page_id="".join(random.choices(string.ascii_letters + string.digits, k=32))
    )
    add_review_item(
        cnx=cnx,
        review_item=another_review_item
    )
    
    due_date = date.today() + timedelta(1)
    due_review_items = fetch_due_review_items(
        cnx=cnx,
        due_date=due_date,
    )
    assert len(due_review_items) == 2
    print(f"Original ease factors: {due_review_items[0].ease_factor}, {due_review_items[1].ease_factor}")
    
    
    modified_review_item = review_item
    modified_review_item.ease_factor = 1
    
    another_modified_review_item = another_review_item
    another_modified_review_item.ease_factor = 3
    
    batch_update_review_items(
        cnx=cnx,
        review_items=[modified_review_item, another_modified_review_item],
    )
    
    due_review_items = fetch_due_review_items(
        cnx=cnx,
        due_date=due_date,
    )
    assert len(due_review_items) == 2
    print(f"New ease factors: {due_review_items[0].ease_factor}, {due_review_items[1].ease_factor}")
    
    delete_review_item(
        cnx=cnx,
        page_id=another_modified_review_item.page_id,
    )
    
    due_review_items = fetch_due_review_items(
        cnx=cnx,
        due_date=due_date,
    )
    assert len(due_review_items) == 1
    print(f"Remaining page_id: {due_review_items[0].page_id}")
    

if __name__ == "__main__":
    main()