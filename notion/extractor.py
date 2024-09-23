import os
import typing
import queue

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()         

class NotionExtractor():
    def __init__(self):
        self.client = Client(auth=os.environ["NOTION_TOKEN"])
        
    def get_base_text(self, block: typing.Dict[str, typing.Any]) -> str:
        """
        block (dict): a Notion block.
        Helper function to get the base text of a block according to its type.
        """
        block_type = block["type"]
        if block_type == "child_page":
            return block["child_page"]["title"]
        else:
            rich_text = block[block_type]["rich_text"][0]
            if rich_text["href"] is None:
                return rich_text["plain_text"]
            else:
                return f'{rich_text["plain_text"]} ({rich_text["href"]})'
        
    def get_parent_id(self, block: typing.Dict[str, typing.Any]) -> str:
        """
        block (dict): a Notion block.
        Helper function to get the parent id of a block according to the parent type.
        """
        parent = block["parent"]
        parent_type = parent["type"]
        return parent[parent_type]
            
    
    def extract(self, block_id: str) -> typing.Dict[str, typing.Any]:
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
    
    
if __name__ == "__main__":
    extractor = NotionExtractor()
    contents = extractor.extract(os.environ["TEST_PAGE_ID"])
    print(contents)