from datetime import date
from mysql.connector import Error as MySQLError, MySQLConnection
from typing import List

from db.review_item import ReviewItem

add_review_item_query = """
INSERT INTO review_items
(page_id, initial_learning_date, last_reviewed_date, next_review_date, ease_factor, review_interval, repetition_count, performance_score, priority_score, overdue_days, skip_counter)
VALUES (%(page_id)s, %(initial_learning_date)s, %(last_reviewed_date)s, %(next_review_date)s, %(ease_factor)s, %(review_interval)s, %(repetition_count)s, %(performance_score)s, %(priority_score)s, %(overdue_days)s, %(skip_counter)s)
"""

def add_review_item(cnx: MySQLConnection, review_item: ReviewItem) -> None:
    """
    cnx: MySQL connection.
    page_id: the 32 character string id of the page we want to add.
    Adds a review item for a page, along with default spaced repitition values, to the 'review_items' table.
    """
    try:
        with cnx.cursor() as cursor:
            cursor.execute(add_review_item_query, review_item.__dict__)
        cnx.commit()
        print(f"Inserted review item {review_item.page_id} successfully.")
    except MySQLError as err:
        cnx.rollback()
        print(f"Error inserting review item {review_item.page_id}: {err}.")
    except Exception as e:
        cnx.rollback()
        print(f"An unexpected error occurred: {e}")
        

fetch_due_review_items_query = """
SELECT * FROM review_items
WHERE next_review_date <= %(due_date)s
ORDER BY priority_score DESC, overdue_days DESC
"""
    
def fetch_due_review_items(cnx: MySQLConnection, due_date: date) -> List[ReviewItem]:
    """
    cnx: MySQL connection.
    date: the specific date from which we want to fetch the review items due.
    Gets all review items due on or before the given date.
    """
    data_due_review_items = {
        "due_date": due_date,
    }
    
    try:
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(fetch_due_review_items_query, data_due_review_items)
            rows = cursor.fetchall()
        print(f"Fetched {len(rows)} review item(s) due on {due_date} successfully.")
        review_items = [ReviewItem(**row) for row in rows]
        return review_items
    except MySQLError as err:
        print(f"Error getting review items due on {due_date}: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

batch_update_review_items_query = """
UPDATE review_items
SET
    last_reviewed_date = %s,
    next_review_date = %s,
    ease_factor = %s,
    review_interval = %s,
    repetition_count = %s,
    overdue_days = %s,
    skip_counter = %s,
    last_updated_at = %s
WHERE page_id = %s
"""

def batch_update_review_items(cnx: MySQLConnection, review_items: List[ReviewItem]) -> None:
    """
    cnx: MySQL connection.
    review_items: a list of review items that we need to update.
    """
    data_update_review_items = [
        (
            item.last_reviewed_date,
            item.next_review_date,
            item.ease_factor,
            item.review_interval,
            item.repetition_count,
            item.overdue_days,
            item.skip_counter,
            item.last_updated_at,
            item.page_id
        ) for item in review_items
    ]
    
    try:
        with cnx.cursor() as cursor:
            cursor.executemany(batch_update_review_items_query, data_update_review_items)
        cnx.commit()
        print(f"Batch updated {cursor.rowcount} review items succesfully.")
    except MySQLError as err:
        cnx.rollback()
        print(f"Error batch updating review items: {err}")
    except Exception as e:
        cnx.rollback()
        print(f"An unexpected error occurred: {e}")


delete_review_item_query = """
DELETE FROM review_items
WHERE page_id = %(page_id)s
"""

def delete_review_item(cnx: MySQLConnection, page_id: str) -> None:
    """
    cnx: MySQL connection.
    page_id: the page_id of the review item we want to delete.
    Deletes a review item from the db. Useful for testing/removing old records.
    """
    data_delete_review_item = {
        "page_id": page_id,
    }
    try:
        with cnx.cursor() as cursor:
            cursor.execute(delete_review_item_query, data_delete_review_item)
        cnx.commit()
        print(f"Deleted review item {page_id} successfully.")
    except MySQLError as err:
        cnx.rollback()
        print(f"Error deleting review item: {err}")
    except Exception as e:
        cnx.rollback()
        print(f"An unexpected error occurred: {e}")