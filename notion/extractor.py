import os
import queue

from mysql.connector import MySQLConnection
from notion_client import Client
from typing import Any, Dict, List

from db.operations import add_review_item, fetch_last_creation_date
from db.review_item import create_new_review_item_from_source, ReviewItem
from notion.consts import SOURCE_ID_TO_NAME_MAP


class NotionExtractor():
    def __init__(self, cnx: MySQLConnection, sources: List[str]):
        """
        cnx: MySQLConnection.
        sources: a list of notion source ids we want to pull new pages from.
        """
        self.cnx = cnx
        self.sources = sources
        self.client = Client(auth=os.environ["NOTION_TOKEN"])
        
    def get_base_text(self, block: Dict[str, Any]) -> str:
        """
        block (dict): a Notion block.
        Helper function to get the base text of a block according to its type.
        """
        block_type = block["type"]
        if block_type == "child_page":
            return block["child_page"]["title"]
        elif block_type == "image":
            # Will support images in the future.
            return ""
        else:
            rich_text = block[block_type]["rich_text"]
            if len(rich_text) == 0:
                return ""
            rich_text = rich_text[0]
            if rich_text["href"] is None:
                return rich_text["plain_text"]
            else:
                return f'{rich_text["plain_text"]} ({rich_text["href"]})'
        
    def get_parent_id(self, block: Dict[str, Any]) -> str:
        """
        block (dict): a Notion block.
        Helper function to get the parent id of a block according to the parent type.
        """
        parent = block["parent"]
        parent_type = parent["type"]
        return parent[parent_type]
            
    
    def extract(self, block_id: str) -> Dict[str, Any]:
        """
        block_id (str): the 32 character id of the block whose content we want to extract.
        Uses BFS to extract content from a block and all of its sub-blocks.
        Importantly, block_id can also be the id of an entire page.
        """
        contents = dict()
        id_to_children = dict()
        q = queue.Queue()
        starter_block = self.client.blocks.retrieve(block_id)
        q.put(starter_block)
        while not q.empty():
            block = q.get()
            id = block["id"]
            base_text = self.get_base_text(block)
            
            # Initially, we add to the base contents dict.
            target_contents = contents
            # If we've seen the parent though, we should add to the dict that the parent key maps to.
            parent_id = self.get_parent_id(block)
            if parent_id in id_to_children:
                target_contents = id_to_children[parent_id]
                
            # Add text to the contents dict, and also maintain a mapping of id->child dict.
            target_contents[base_text] = dict()
            id_to_children[id] = target_contents[base_text]
            
            # If the current block has children, add them to the queue.
            if block["has_children"]:
                children = self.client.blocks.children.list(block["id"])["results"]
                for child_block in children:
                    q.put(child_block)
        return contents
    
    def pull_new_pages_from_source(self, source_id: str) -> List[ReviewItem]:
        """
        source_id: the id of the database/page we want to pull pages from. could be a database of papers, a page with lecture notes, etc.
        Checks to see what pages have been added in the given source since the last scan.
        Creates ReviewItems for each of those pages and stores them in the db.
        """
        last_creation_date = fetch_last_creation_date(
            cnx=self.cnx,
            source=SOURCE_ID_TO_NAME_MAP[source_id],
        )
        
        resp = self.client.databases.query(source_id, filter={
            "property": "Created time",
            "date": {
                "after": str(last_creation_date),
            },
        })
        
        new_review_items = []
        if len(resp["results"]) == 0:
            print("No new pages to review.")
            return []
        for result in resp["results"]:
            new_review_item = create_new_review_item_from_source(
                page_id=result["id"],
                source=SOURCE_ID_TO_NAME_MAP[source_id],
            )
            add_review_item(
                cnx=self.cnx,
                review_item=new_review_item
            )
            new_review_items.append(new_review_item)
            
        return new_review_items
    
if __name__ == "__main__":
    extractor = NotionExtractor()
    contents = extractor.extract(os.environ["TEST_PAGE_ID"])
    print(contents)