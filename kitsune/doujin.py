from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

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
    def post_date(self) -> datetime:
        return datetime.fromtimestamp(self._post_date)

@dataclass(frozen = True)
class Title: 

    english: str
    japanese: str
    pretty: str

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
    extension: str
    
    @property
    def url(self) -> str: 
        return f"https://i.nhentai.net/galleries/{self.media_id}/{self.page_num}.{self.extension}"

class Cover(Page): 

    @property
    def url(self) -> str:  
        return f"https://t.nhentai.net/galleries/{self.media_id}/cover.{self.extension}"

class Gallery: 

    EXTENSIONS = {"j": "jpg", "p": "png", "g": "gif"}

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

        self.title = Title(*(self.payload["title"].values()))
        self.cover = Cover(self.media_id, 0, self.num_pages, self.EXTENSIONS[self.payload["images"]["cover"]["t"]])
        self.pages = [Page(self.media_id, i + 1, self.num_pages, self.EXTENSIONS[self.payload["images"]["pages"][i]["t"]]) for i in range(self.num_pages)]
        self.tags = [Tag(*tag.values()) for tag in self.payload["tags"]]

    def __iter__(self): 
        return iter([self])

    def __str__(self): 
        return f"[{self.id}] {self.title.pretty}"

    def __repr__(self): 
        return f"Gallery(id={self.id}, media_id={self.media_id}, title={self.title}, num_pages={self.num_pages}, cover={self.cover}, pages={self.pages}, tags={self.tags})"

    @property
    def id(self) -> int: 
        return self.payload["id"]
    
    @property
    def media_id(self) -> int: 
        return self.payload["media_id"]

    @property
    def num_pages(self) -> int: 
        return self.payload["num_pages"]

    def get_page(self, page: int) -> Page: 
        return self.pages[page + 1]

@dataclass(frozen = True)
class HomePage: 

    popular_now: List[Gallery]
    new_uploads: List[Gallery]

@dataclass(frozen = True)
class Shelf: 

    galleries: List[Gallery]
    num_pages: int
    per_page: int

    def __iter__(self): 
        return iter(self.galleries)
