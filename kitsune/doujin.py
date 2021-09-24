from typing import Dict, Any, List

from query import Query

__all__ = ("Tag", "Page", "Doujinshi", "Shelf",)

class Tag: 

    """
    Class for storing doujinshi tag data. 
    """

    def __init__(self, code: int, filtering: str, name: str, url: str, count: int): 
        self.code = code
        self.filtering = filtering
        self.name = name
        self.url = url
        self.count = count

class Page: 

    """
    Class for storing doujinshi page data.
    """

    def __init__(self, media_id: int, page_num: int, pages: int): 
        self.media_id = media_id
        self.page_num = page_num
        self.pages = pages
    
    @property
    def url(self): 
        return f"https://i.nhentai.net/galleries/{self.media_id}/{self.page_num}.jpg"

class Doujinshi: 

    """
    Doujinshi base class. With iterator functionality to retrieve its pages
    and contains all the data received from the GET request to the API.
    """

    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data

        for key, value in self.raw_data.items(): 
            setattr(self, key, value)

        self.code = self.id
        self.pages = [Page(self.media_id, i + 1, self.num_pages) for i in range(self.num_pages)]
        self.tags = [Tag(*tag.values()) for tag in self.tags]

    def __iter__(self): 
        self._counter = 0
        return self

    def __next__(self):
        if self._counter < len(self.pages):
            self._counter += 1
            return self.pages[self._counter - 1]
        raise StopIteration

    def get_page(self, page: int) -> Page: 
        return self.pages[page]

    def download(self, directory: str) -> bool: 
        ...

class Gallery: 

    """
    Gallery base class. Iterator functionality to retrieve its doujinshi codes.
    """

    def __init__(self, codes: List[int], gallery_num: int, galleries: int): 
        self.codes = codes
        self.gallery_num = gallery_num
        self.galleries = galleries
    
    def __iter__(self): 
        self._counter = 0
        return self
    
    def __next__(self): 
        if self._counter < len(self.codes): 
            self._counter += 1
            return self.codes[self._counter - 1]
        raise StopIteration

class Shelf: 

    """
    Shelf base class. Iterator functionality to retrieve its galleries.
    It contains all the data scraped from the HTML code related to the doujins found. 
    """
    
    def __init__(self, codes: List[int], query: Query): 
        self.galleries = [Gallery(code, codes.index(code) + 1, len(codes)) for code in codes]
        self.query = query

    def __iter__(self): 
        self._counter = 0
        return self
    
    def __next__(self): 
        if self._counter < len(self.galleries): 
            self._counter += 1
            return self.galleries[self._counter - 1]
        raise StopIteration
    ...