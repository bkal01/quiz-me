from datetime import date, timedelta
from mysql.connector import MySQLConnection

add_page_query = """
INSERT INTO pages
(page_id, initial_learning_date, last_reviewed_date, next_review_date, ease_factor, review_interval, repetition_count, performance_score, priority_score, overdue_days, skip_counter)
VALUES (%(page_id)s, %(initial_learning_date)s, %(last_reviewed_date)s, %(next_review_date)s, %(ease_factor)s, %(review_interval)s, %(repetition_count)s, %(performance_score)s, %(priority_score)s, %(overdue_days)s, %(skip_counter)s)
"""

def add_page(cnx: MySQLConnection, page_id: str):
    """
    cnx: MySQL connection.
    page_id: the 32 character string id of the page we want to add.
    Adds a page, along with default spaced repitition values, to the 'pages' table.
    """
    today = date.today()
    next_review_date = today + timedelta(days=1)
    data_page = {
        "page_id": page_id,
        "initial_learning_date": today,
        "last_reviewed_date": today,
        "next_review_date": next_review_date,
        # Default values
        "ease_factor":2.5,
        "review_interval": 1,
        "repetition_count": 0,
        "performance_score": 0,
        "priority_score": 0,
        "overdue_days": 0,
        "skip_counter": 0,
    }
    
    cursor = cnx.cursor()
    cursor.execute(add_page_query, data_page)
    cnx.commit()
    cursor.close()
    
    print(f"Inserted page {page_id} successfully.")