import aiohttp, asyncio
from doujin import Doujin
from bs4 import BeautifulSoup

class NhentaiScraper:

    URL = "https://nhentai.net"
    
    def __init__(self, **kwargs): 
        self.cache = kwargs.get("cache", True)
        if self.cache: 
            self._doujin_cache = {}

    async def _get_soup(self, code : int) -> BeautifulSoup: 
        async with aiohttp.ClientSession() as session: 
            async with session.get(__class__.URL + f"/g/{code}/") as response: 
                text = await response.read()
        return BeautifulSoup(text.decode("utf-8"), "html5lib")
        
    async def _arrange_soup(self, soup : BeautifulSoup, code : int) -> dict: 
        name, _ = soup.title.string.split(" »")
        content = [img["src"] for img in soup.find_all("img") if img["src"][-4:] in [".png", ".jpeg", ".jpg"]]
        content_cover, content_pages, content_recommended = content[0], content[1:-5], content[-5:]
        content_pages = [page_url[:page_url.rindex("t")] + page_url[page_url.rindex("."):] for page_url in content_pages]
        info = soup.find("div", {"id" : "content"}).find("div").find("div", {"id" : "info-block"}).find("div")
        pages = info.find("section").find_all("div")[-2].find("span").text

        return {
            "name" : name, 
            "pages" : pages,
            "code" : code, 
            "content_cover":  content_cover, 
            "content_pages" : content_pages,
            "content_recommended" : content_recommended
            }

    async def get_doujin(self, code : int) -> Doujin: 
        try: 
            return self._doujin_cache[str(code)]
        except:
            print("Not found in cache / Cache disabled")

        soup = await self._get_soup(code)
        elements = await self._arrange_soup(soup, code)
        doujin = Doujin(**elements)

        if self.cache: 
            self._doujin_cache[str(doujin.code)] = doujin 
        return doujin

# Example of usage

# async def main():
#    scraper = NhentaiScraper()
#    doujin = await scraper.get_doujin(4203)
    
# asyncio.get_event_loop().run_until_complete(main())

