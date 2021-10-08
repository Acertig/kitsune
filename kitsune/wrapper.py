from typing import Awaitable, Optional, Type, List, Union
from random import randint
import asyncio
import aiohttp

from doujin import Comment, Shelf, Gallery, User, HomePage
from http_handler import HTTPHandler
from routes import Popularity

__all__ = ("Kitsune",)

class Kitsune: 

    slots = ("loop", "http", "cache",)
        
    def __init__(self, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(), subcls_handler: Optional[Type[HTTPHandler]] = None):
        self.loop = loop 
        self.http = subcls_handler or HTTPHandler(self.loop)
        self.cache = {}

    async def __aenter__(self):
        self.http.session = aiohttp.ClientSession(loop = self.loop, headers = self.http.headers)
        return self

    async def __aexit__(self, *args): 
        await self.http.session.__aexit__(*args)

    async def _distribute(self, codes: List[int]) -> List[Awaitable]: 
        return await asyncio.gather(*(self.fetch_gallery(code) for code in codes))

    async def fetch_gallery(self, code: int) -> Gallery: 
        if gallery := self.cache.get(str(code)):
            return gallery

        payload = await self.http.fetch_gallery_data(code)
        gallery = Gallery(payload)
        self.cache[gallery.id] = gallery
       
        return gallery

    async def fetch_random(self) -> Gallery: 
        return await self.fetch_gallery(randint(1, 335000))

    async def fetch_homepage(self) -> HomePage: 
        ids = await self.http.fetch_homepage_data()
        galleries = await self._distribute(ids)

        homepage = HomePage(galleries[0:5], galleries[5:])

        return homepage

    async def fetch_comments(self, gallery: Union[int, Gallery]) -> Comment: 
        try: 
            __id = gallery.id
        except AttributeError: 
            __id = gallery

        payload = await self.http.fetch_comment_data(__id)

        comments = []

        for data in payload: 
            data["poster"] = User(*(data.get("poster").values()))           
            comment = Comment(*data.values())
            comments.append(comment)

        return comments

    async def search(self, query: Union[str, List[str]], page: Union[int, List[int]], popularity: Popularity = Popularity.RECENT) -> Shelf: 
        if isinstance(query, list): 
            query = "+".join(query)
        
        payload = await self.http.fetch_search_data(query, page, popularity)

        payload["result"] = [Gallery(data) for data in payload["result"]]
        
        shelf = Shelf(*(payload.values()))

        return shelf

