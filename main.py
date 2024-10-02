import os

from dotenv import load_dotenv

from db.connection import get_connection
from db.operations import add_review_item, delete_review_item
from db.review_item import create_new_review_item_from_source
from notion.extractor import NotionExtractor

def main() -> None:
    load_dotenv()
    
    cnx = get_connection()
    
    review_item = create_new_review_item_from_source(
        page_id=os.environ["TEST_PAGE_ID"],
        source="ml_paper_notes",
    )
    add_review_item(
        cnx=cnx, 
        review_item=review_item,
    )
    
    extractor = NotionExtractor(
        cnx=cnx,
        sources=[os.environ["ML_PAPER_NOTES_DB_ID"]]
    )
    
    new_review_items = extractor.pull_new_pages_from_source(extractor.sources[0])
    for new_review_item in new_review_items:
        print(new_review_item.page_id)
    
    delete_review_item(
        cnx=cnx,
        page_id=review_item.page_id,
    )
    

if __name__ == "__main__":
    main()