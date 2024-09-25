import os

from dotenv import load_dotenv

from db.connection import get_connection
from db.operations import add_page

def main() -> None:
    load_dotenv()
    
    cnx = get_connection()
    add_page(cnx, os.environ["TEST_PAGE_ID"])

if __name__ == "__main__":
    main()