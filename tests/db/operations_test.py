import random
import string
import unittest

from datetime import date
from unittest.mock import patch, MagicMock

from db.operations import add_review_item, batch_update_review_items, delete_review_item, fetch_due_review_items, fetch_last_creation_date
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
        
    @patch("db.connection.get_connection")
    def test_batch_update_review_items(self, mock_get_connection):
        mock_cnx = mock_get_connection.return_value
        mock_cursor_context = MagicMock()
        mock_cursor = mock_cursor_context.__enter__.return_value
        mock_cnx.cursor.return_value = mock_cursor_context
        
        test_page_id_1 = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        test_review_item_1 = create_new_review_item(
            page_id=test_page_id_1,
        )
        
        test_page_id_2 = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        test_review_item_2 = create_new_review_item(
            page_id=test_page_id_2,
        )
        
        batch_update_review_items(mock_cnx, [test_review_item_1, test_review_item_2])
        
        mock_cursor.executemany.assert_called_once()
        mock_cnx.commit.assert_called_once()
        mock_cnx.rollback.assert_not_called()
    
    @patch("db.connection.get_connection")
    def test_delete_review_item(self, mock_get_connection):
        mock_cnx = mock_get_connection.return_value
        mock_cursor_context = MagicMock()
        mock_cursor = mock_cursor_context.__enter__.return_value
        mock_cnx.cursor.return_value = mock_cursor_context
        
        test_page_id = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        delete_review_item(mock_cnx, test_page_id)
        
        mock_cursor.execute.assert_called_once()
        mock_cnx.commit.assert_called_once()
        mock_cnx.rollback.assert_not_called()
        
    @patch("db.connection.get_connection")
    def test_fetch_last_creation_date(self, mock_get_connection):
        mock_cnx = mock_get_connection.return_value
        mock_cursor_context = MagicMock()
        mock_cursor = mock_cursor_context.__enter__.return_value
        mock_cnx.cursor.return_value = mock_cursor_context
        
        fetch_last_creation_date(mock_cnx)
        
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        

if __name__ == "__main__":
    unittest.main()