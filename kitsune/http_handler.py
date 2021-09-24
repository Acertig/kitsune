from typing import Optional, Type, List, Dict, Any
from bs4 import BeautifulSoup
import asyncio
import aiohttp

from constants import API_ENDPOINT, DEFAULT_HEADERS, ROUTE
from query import Query

__all__ = ("HTTPHandler",)

class HTTPHandler:

    __slots__ = ("loop", "session", "headers", "semaphore")
   
    def __init__(self, loop: asyncio.AbstractEventLoop, headers: Optional[Dict[str, str]] = DEFAULT_HEADERS, session: Optional[Type[aiohttp.ClientSession]] = None):                             
        self.loop = loop                                                                                                                                                                                                                 
        self.headers = headers

        if session is None: 
            async def create_session(): 
                self.session = aiohttp.ClientSession(loop = self.loop, headers = headers)
            
            self.loop.run_until_complete(create_session())
        
        else: 
            self.session = session
            
    def __del__(self): 
        async def close_session(): 
            await self.session.close()

        self.loop.run_until_complete(close_session())

    def _check_results(self, soup) -> bool: 
        if not soup.select("body > div[id=content] > div.container > h2"): 
            return True
        return False

    def _scrape_codes(self, soup) -> List[int]: 
        selection = soup.select("body > div[id=content] > div.container")[0].find_all("div", {"class": "gallery"})
        return [int(selected.find("a")["href"][3:-1]) for selected in selection]

    async def fetch_doujin_data(self, code: int) -> Dict[str, Any]:  
        async with self.session.get(f"{ROUTE}{API_ENDPOINT}{code}") as response:  
            return await response.json()

    async def fetch_search_data(self, query: Query) -> str:
        codes = []
        while query.page <= query.pages: 
            async with self.session.get(f"{ROUTE}{query.built}") as response: 
                soup = BeautifulSoup(await response.text(), features = "html5lib")
                if self._check_results(soup): 
                    codes.append(self._scrape_codes(soup))
                else: 
                    break
            
            query.page += 1

        return codes

    async def fetch_comments_data(self):
        ...

    async def fetch_bytes_data(self, url: str) -> bytearray: 
        ...


