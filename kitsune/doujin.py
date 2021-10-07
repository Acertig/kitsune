from types import prepare_class
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass(frozen = True)
class User: 

    id: int
    username: str
    slug: str
    avatar_url: str
    is_superuser: bool
    is_staff: bool

@dataclass(frozen = True)
class Comment:
    
    id: int
    gallery_id: int
    poster: User
    _post_date: int
    body: str

    @property
    def post_date(self):
        return self._post_date

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

class Gallery: 

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

    @property
    def payload(self) -> Dict[str, Any]: 
        return self.data

    def get_page(self, page: int) -> Page: 
        return self.pages[page]

    def download(self, directory: str) -> bool: 
        ...

class HomePage: 

    __slots__ = ("popular_now", "new_uploads",)

    def __init__(self, popular_now: List[Gallery], new_uploads: List[Gallery]): 
        self.popular_now = popular_now
        self.new_uploads = new_uploads

class Shelf: 

    __slots__ = ("galleries", "num_pages", "per_page",)

    def __init__(self, galleries: List[Gallery], num_pages: int, per_page: int): 
        self.galleries = galleries
        self.num_pages = num_pages
        self.per_page = per_page
