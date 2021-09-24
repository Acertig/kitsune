from asyncio.coroutines import coroutine
from typing import Awaitable, Optional, Type, List, Callable
from doujin import Doujinshi, Shelf
from http_handler import HTTPHandler
from query import Filtering, Query, Popularity
from time import time
import asyncio

__all__ = ("Kitsune",)

class CacheError(Exception): 
    pass

class Kitsune: 

    slots = ("loop", "client", "options", "cache",)

    def __new__(cls, *args, **kwargs): 
        for value in globals().values():
            if isinstance(value, cls): 
                raise CacheError("The cache won't work properly if there are 2 instances of the wrapper or its subclass.")
        return super().__new__(cls)
        
    def __init__(self, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(), custom_client: Optional[Type[HTTPHandler]] = None):
        self.loop = loop 
        self.http = custom_client or HTTPHandler(self.loop)
        self.cache = {}

    async def _distribute(self, async_fn: Callable[[int], Doujinshi], *args) -> List[Awaitable]: 
        return await asyncio.gather(*(async_fn(arg) for arg in args))

    async def get_doujinshi(self, code: int) -> Doujinshi: 
        if doujin := self.cache.get(str(code)):
            return doujin

        data = await self.http.fetch_doujin_data(312781)
        doujin = Doujinshi(data)
        self.cache[doujin.id] = doujin
       
        return doujin

    async def search(self, query: str, pages: int, popularity: Popularity, filtering: Optional[Filtering] = None) -> Shelf: 
        query = Query(query, pages, popularity, filtering)

        data = await self.http.fetch_search_data(query)

        return Shelf(data, query)