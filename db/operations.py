from mysql.connector import Error as MySQLError, MySQLConnection

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
        print(f"Inserted page {review_item.page_id} successfully.")
    except MySQLError as err:
        cnx.rollback()
        print(f"Error inserting page {review_item.page_id}: {err}.")
    except Exception as e:
        cnx.rollback()
        print(f"An unexpected error occurred: {e}")