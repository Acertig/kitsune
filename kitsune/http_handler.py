from typing import Optional, Type, List, Dict, Any, Union, Tuple
import re
import asyncio
import aiohttp

from constants import DEFAULT_HEADERS, TBR
from routes import Popularity, Route

__all__ = ("HTTPHandler",)

class HTTPHandler:

    __slots__ = ("loop", "session", "headers", "lock",)
   
    def __init__(self, loop: asyncio.AbstractEventLoop, headers: Optional[Dict[str, str]] = DEFAULT_HEADERS, session: Optional[Type[aiohttp.ClientSession]] = None):                             
        self.loop = loop                                                                                                                                                                                                                 
        self.headers = headers
        self.lock = asyncio.Lock()

        self.session = session or None

    def ratelimit(async_func):
        async def wrapper(*args): 
            self = args[0]
            await self.lock.acquire()
            self.loop.call_later(TBR, self.lock.release)
            return await async_func(*args)
        return wrapper 

    @ratelimit
    async def get(self, url: str) -> Union[Dict[str, Any], str, None]: 
        async with self.session.get(url) as response: 
            if 200 <= response.status < 300:    
                if response.headers["Content-Type"] == "application/json": 
                    return await response.json()
                return await response.text()
            elif response.status == 429: 
                return await self.get(url) 
            else: 
                return None
                    
    async def fetch_gallery_data(self, __id: int) -> Dict[str, Any]:  
        route = Route("/api/gallery/{}", __id)
        payload = await self.get(route.url)

        return payload

    async def fetch_homepage_data(self) -> List[List[int]]: 
        route = Route("")
        html = await self.get(route.url)

        ids = re.findall(r"/g/(\d+)/", html)

        return ids

    async def fetch_search_data(self, query: str, page: int, popularity: Popularity) -> Dict[str, Any]:
        route = Route("/api/galleries/search?query={}&page={}&sort={}", query, page, popularity.value)     
        payload = await self.get(route.url)

        return payload

    async def fetch_comment_data(self, __id: int) -> Dict[str, Any]:
        route = Route("/api/gallery/{}/comments", __id)
        payload = await self.get(route.url)

        return payload
