from typing import Awaitable, Optional, Type, List, Union
import asyncio
import aiohttp

from doujin import Comment, Doujinshi, Shelf, Gallery, User
from http_handler import HTTPHandler
from routes import Category, SearchRoute, APIRoute, Popularity

__all__ = ("Kitsune",)

class Kitsune: 

    slots = ("loop", "client", "options", "cache",)
        
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
        return await asyncio.gather(*(self.get_doujinshi(code) for code in codes))

    async def fetch_doujinshi(self, code: int) -> Doujinshi: 
        if doujin := self.cache.get(str(code)):
            return doujin

        route = APIRoute(code)

        data = await self.http.fetch_doujin_data(route)
        doujin = Doujinshi(data)
        self.cache[doujin.id] = doujin
       
        return doujin

    async def fetch_gallery(self, shelf: Shelf, num: int) -> Gallery: 
        data = await self.http.fetch_search_data(shelf.route, num)
        doujins = await self._distribute(data)

        return Gallery(doujins, num, shelf.galleries)

    async def fetch_user(self, id: int) -> User: 
        ...

    async def fetch_comment(self, target: Union[Doujinshi, User]) -> Comment: 
        ...

    async def search(self, query: str, popularity: Popularity, category: Optional[Category] = None) -> Union[Shelf, List[List[Doujinshi]]]: 
        route = SearchRoute(query.replace(" ", "+"), popularity, category)

        limit = await self.http.fetch_paginator_limit(route)

        return Shelf(limit, route)
