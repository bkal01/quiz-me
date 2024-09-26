import random
import string
import unittest

from datetime import date
from unittest.mock import patch, MagicMock

from db.operations import add_review_item, fetch_due_review_items
from db.review_item import create_new_review_item

class TestDBOperations(unittest.TestCase):
    
    @patch("db.connection.get_connection")
    def test_add_page(self, mock_get_connection):
        mock_cnx = mock_get_connection.return_value
        mock_cursor_context = MagicMock()
        mock_cursor = mock_cursor_context.__enter__.return_value
        mock_cnx.cursor.return_value = mock_cursor_context
        
        test_page_id = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        test_review_item = create_new_review_item(
            page_id=test_page_id,
        )
        add_review_item(mock_cnx, test_review_item)
        
        mock_cursor.execute.assert_called_once()
        mock_cnx.commit.assert_called_once()
        mock_cnx.rollback.assert_not_called()

    @patch("db.connection.get_connection")
    def test_fetch_due_review_items(self, mock_get_connection):
        mock_cnx = mock_get_connection.return_value
        mock_cursor_context = MagicMock()
        mock_cursor = mock_cursor_context.__enter__.return_value
        mock_cnx.cursor.return_value = mock_cursor_context
        
        fetch_due_review_items(mock_cnx, date.today())
        
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()

if __name__ == "__main__":
    unittest.main()