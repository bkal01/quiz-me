import os
import random
import string

from datetime import date, timedelta
from dotenv import load_dotenv

from db.connection import get_connection
from db.operations import add_review_item, delete_review_item, fetch_last_creation_date
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
    
    last_creation_date = fetch_last_creation_date(
        cnx=cnx
    )
    print(last_creation_date)
    
    delete_review_item(
        cnx=cnx,
        page_id=review_item.page_id,
    )
    

if __name__ == "__main__":
    main()