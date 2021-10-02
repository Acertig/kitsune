from asyncio.locks import Semaphore
from typing import Optional, Type, List, Dict, Any, Union
from bs4 import BeautifulSoup
from http import HTTPStatus
import re
import asyncio
import aiohttp

from constants import DEFAULT_HEADERS, BASE
from routes import APIRoute, SearchRoute

__all__ = ("HTTPHandler",)

class MediaNotFound(Exception): 
    pass

class HTTPHandler:

    __slots__ = ("loop", "session", "headers", "semaphore",)
   
    def __init__(self, loop: asyncio.AbstractEventLoop, headers: Optional[Dict[str, str]] = DEFAULT_HEADERS, session: Optional[Type[aiohttp.ClientSession]] = None):                             
        self.loop = loop                                                                                                                                                                                                                 
        self.headers = headers
        self.semaphore = Semaphore(3)

        self.session = session or None

    def _check_limit(self, soup: BeautifulSoup) -> int: 
        limit = soup.select("body > div[id=content] > section.pagination > a.last")[0]["href"]
        return int(re.search(r"\d+", limit).group(0))

    def _check_results(self, soup: BeautifulSoup) -> bool: 
        if not soup.select("body > div[id=content] > div.container > h2"): 
            return True
        return False

    def _scrape_codes(self, soup: BeautifulSoup) -> List[int]:  
        selection = soup.select("body > div[id=content] > div.container")[0].find_all("div", {"class": "gallery"})
        return [int(selected.find("a")["href"][3:-1]) for selected in selection]

    async def get(self, url: str) -> Union[Dict[str, Any], str]: 
        async with self.semaphore: 
            async with self.session.get(url) as response: 
                if response.status == HTTPStatus.OK:     
                    if response.headers["Content-Type"] == "application/json": 
                        return await response.json()
                    return await response.text()
                elif response.status == HTTPStatus.NOT_FOUND:  
                    raise MediaNotFound(f"Media could not be found at {url}")
        return await self.get(url) # Temporary solution
                    
    async def fetch_doujin_data(self, route: APIRoute) -> Dict[str, Any]:  
        return await self.get(route.url)

    async def fetch_search_data(self, route: SearchRoute, num: int) -> str:
        data = await self.get(route.get_url(num))
        soup = BeautifulSoup(data, features = "html5lib")

        return self._scrape_codes(soup)

    async def fetch_paginator_limit(self, route: SearchRoute) -> int: 
        data = await self.get(route.get_url(1))
        soup = BeautifulSoup(data, features = "html5lib")
        
        if self._check_results(soup): 
            return self._check_limit(soup)

    async def fetch_comments_data(self):
        ...

    async def fetch_bytes_data(self, url: str): 
        ...
