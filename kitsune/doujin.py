from typing import Dict, Any, List
from dataclasses import dataclass

from routes import SearchRoute

__all__ = ("Tag", "Doujinshi", "Shelf",)

@dataclass(frozen = True)
class User: 

    id: int
    name: str
    about: str
    favorite_tags: str
    recent_favorites: List[int]

@dataclass(frozen = True)
class Comment:
    
    doujin_id: int
    id: int
    content: str
    user: User

@dataclass(frozen = True)
class Tag: 

    id: int
    category: str
    name: str
    url: str
    count: int

@dataclass(frozen = True)
class Page: 

    media_id: int
    page_num: int
    pages: int
    
    @property
    def url(self) -> str: 
        return f"https://i.nhentai.net/galleries/{self.media_id}/{self.page_num}.jpg"

class Cover(Page): 

    @property
    def url(self) -> str:  
        return f"https://t.nhentai.net/galleries/{self.media_id}/cover.jpg"

class Doujinshi: 

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.cover = Cover(self.media_id, 0, self.num_pages)
        self.pages = [Page(self.media_id, i + 1, self.num_pages) for i in range(self.num_pages)]
        self.tags = [Tag(*tag.values()) for tag in self.data["tags"]]

    def __iter__(self): 
        self._counter = 0
        return self

    def __next__(self):
        if self._counter < len(self.pages):
            self._counter += 1
            return self.pages[self._counter - 1]
        raise StopIteration

    @property
    def id(self) -> int: 
        return self.data["id"]
    
    @property
    def media_id(self) -> int: 
        return self.data["media_id"]

    @property
    def title(self) -> Dict[str, str]: 
        return self.data["title"]

    @property
    def num_pages(self) -> int: 
        return self.data["num_pages"]

    def get_page(self, page: int) -> Page: 
        return self.pages[page]

    def download(self, directory: str) -> bool: 
        ...

class Gallery: 

    __slots__ = ("doujins", "gallery_num", "galleries",)

    def __init__(self, doujins: List[Doujinshi], gallery_num: int, galleries: int): 
        self.doujins = doujins
        self.gallery_num = gallery_num
        self.galleries = galleries
    
    def __iter__(self): 
        self._counter = 0
        return self
    
    def __next__(self): 
        if self._counter < len(self.ids): 
            self._counter += 1
            return self.ids[self._counter - 1]
        raise StopIteration

class Shelf: 

    __slots__ = ("galleries", "route")
    
    def __init__(self, galleries: int, route: SearchRoute): 
        self.galleries = galleries
        self.route = route
