from typing import Optional, List, Union
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from random import randint
from PIL import Image, UnidentifiedImageError

import asyncio
import aiohttp
import io
import os

from kitsune.constants import DEFAULT_HEADERS
from kitsune.doujin import Comment, Shelf, Gallery, User, HomePage
from kitsune.http_handler import HTTPHandler
from kitsune.routes import Popularity

__all__ = ("Kitsune",)

class Kitsune: 

    """
    Wrapper class.

    Attributes
    ----------
    loop: asyncio.AbstractEventLoop
        The event loop in which the wrapper instance will run on. 
    http: http_handler.HTTPHandler
        The http handler which implements ratelimits to GET requests
        and returns the data from API endpoints. 
    cache: Dict[str, Gallery]
        A dictionary that holds pre-requested Gallery instances
        to avoid making unnecessary requests for existing data.
    """

    __slots__ = ("loop", "http", "cache",)
        
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):

        """
        Parameters
        ----------
        loop: Optional[asyncio.AbstractEventLoop], defaults to None
        """

        self.loop = loop or asyncio.get_running_loop()
        self.http: HTTPHandler

        self.cache = {}

    async def __aenter__(self):
        session = aiohttp.ClientSession(loop = self.loop, headers = DEFAULT_HEADERS)
        self.http = HTTPHandler(self.loop, session)
        return self

    async def __aexit__(self, *args): 
        await self.http.session.close()

    def save_bytes_to_file(self, bytes_l: List[bytes], path: str, gallery: Gallery): 
        for i, __bytes in enumerate(bytes_l): 
            try: 
                img = Image.open(io.BytesIO(__bytes))
                img.save(f"{path}/{i if i != 0 else 'cover'}.{gallery.pages[i-1].extension if i != 0 else gallery.cover_extension}")
            except UnidentifiedImageError: 
                print(f"Page {i} was corrupted.")

    @classmethod
    @asynccontextmanager
    async def from_session(cls, session: aiohttp.ClientSession):
        
        """
        Async context manager to instantiate the wrapper with a custom session. 

        Parameters 
        ----------
        session: aiohttp.ClientSession
            Used by the http handler to request data.
        loop: Optional[asyncio.AbstractEventLoop], defaults to None

        Returns
        ----------
        Kitsune 
        """

        loop = asyncio.get_running_loop()

        try: 
            instance = cls(loop, session)
            yield instance
        except Exception as e: 
            await instance.__aexit__(type(e), e, e.__traceback__)
        else: 
            await instance.__aexit__(*([None]*3))

    async def fetch_gallery(self, __id: int) -> Gallery: 

        """
        Async function. Fetches the data from the /api/gallery/ endpoint and wraps it into a Gallery instance.

        Parameters 
        ----------
        __id: int
            Identifier used to fetch Gallery data. 
        
        Returns 
        ----------
        Gallery
        """

        if gallery := self.cache.get(str(__id)):
            return gallery

        payload = await self.http.fetch_gallery_data(__id)
        gallery = Gallery(payload)
        self.cache[gallery.id] = gallery
       
        return gallery

    async def fetch_galleries(self, ids: List[int]) -> List[Gallery]:

        """
        Async function. Multiple ids variant of Kitsune.fetch_gallery.

        Parameters 
        ----------
        ids: List[int]
            List of identifiers, multiple id variant of Kitsune.fetch_gallery. 

        Returns 
        ----------
        List[Gallery]
        """

        return await asyncio.gather(*(self.fetch_gallery(__id) for __id in ids))

    async def fetch_related(self, gallery = Union[int, Gallery]) -> List[Gallery]:
        
        """
        Async function. Relation variant of fetch_galleries. 

        Parameters 
        ----------
        gallery: Gallery
            Gallery from which to retrieve the related galleries.  
        """

        try: 
            __id = gallery.id
        except AttributeError: 
            __id = gallery

        ids = await self.http.fetch_related_data(__id)
        galleries = await self.fetch_galleries(ids)

        return galleries

    async def fetch_random(self) -> Gallery: 

        """
        Async function. Random id variant of Kitsune.fetch_gallery.
        
        Returns 
        ----------
        Gallery
        """ 

        return await self.fetch_gallery(randint(1, 335000))

    async def fetch_homepage(self) -> HomePage: 
        
        """
        Async function. Scrapes the data from the homepage and wraps it into a HomePage instance. 
        
        Returns 
        ----------
        HomePage
        """ 
        
        ids = await self.http.fetch_homepage_data()
        galleries = await self.fetch_galleries(ids)

        homepage = HomePage(galleries[0:5], galleries[5:])

        return homepage

    async def search(self, query: Union[str, List[str]], page: Optional[Union[int, List[int]]] = 1, popularity: Optional[Popularity] = Popularity.RECENT) -> Shelf:
        
        """
        Async function. Fetches the data from the /api/galleries/ endpoint and wraps it into a Shelf instance. 

        Parameters
        ----------
        query: Union[str, List[str]]
            A string or a list of category:query if given. 
        page: Optional[Union[int, List[int]]], defaults to 1. 
            The paginator number, or a list of start and end of an inclusive range if given.
        popularity: Optional[Popularity], defaults to Popularity.RECENT
            Used to filter the popularity of the galleries.  

        Returns
        ----------
        Shelf
        """

        if isinstance(query, list): 
            query = "+".join(query)
        
        if isinstance(page, int): 
            payload = await self.http.fetch_search_data(query, page, popularity)
            payload["result"] = [Gallery(data) for data in payload["result"]]
            
            shelf = Shelf(*(payload.values()))

            return shelf
        
        payload = await self.http.fetch_search_data(query, 1, popularity)
        paginator_max = payload["num_pages"]
        
        pages = [end if end < paginator_max else paginator_max for end in page]

        results = await asyncio.gather(*(self.http.fetch_search_data(query, page, popularity) for page in range(*pages)), return_exceptions = True)
        payloads = [result for result in results if isinstance(result, dict)]

        for payload in payloads: 
            payload["result"] = [Gallery(data) for data in payload["result"]]

        shelves = [Shelf(*(payload.values())) for payload in payloads]

        return shelves

    async def fetch_comments(self, gallery: Union[int, Gallery]) -> Comment: 

        """
        Async function. Fetches the data from the /api/gallery/{id}/comments endpoint and wraps it into a list of Comment instances.

        Parameters 
        ----------
        gallery: Union[int, Gallery] 
            The gallery whose comments' data is getting fetched. 
        
        Returns
        ----------
        Comment
        """

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

    async def download(self, container: Union[Gallery, List[Gallery], Shelf], path: str, directory: Optional[bool] = True): 
        
        """
        Async function. Fetches the bytes from the containers' media, and downloads it via threads in the path given and creates a directory if specified. 

        Parameters
        ----------
        container: Union[Gallery, List[Gallery], Shelf]
            A Gallery, list of galleries or Shelf instance to retrieve the media data from. 
        path: str
            Path in which the downloaded media will be saved to.  
        directory: Optional[bool], defaults to True. 
            Creates a directory if set to True. Else it will save the media without creating a directory. 
        """

        if isinstance(container, Shelf): 
            galleries = [gallery for gallery in container.galleries]
        else: 
            if isinstance(container, list): 
                galleries = [*container]
            else: 
                galleries = [container]
        
        bytes_l = [await self.http.fetch_media_bytes([gallery.cover, *gallery.pages]) for gallery in galleries]
        media = list(zip(galleries, bytes_l))

        with ThreadPoolExecutor() as executor: 
            for gallery, bytes_l in media: 
                if directory: 
                    temp = f"{path}/{gallery.id}"
                    try: 
                        os.mkdir(temp)
                    except FileExistsError: 
                        print(f"Directory {temp} couldn't be created because it already exists.")
                else: 
                    temp = path
                    
                executor.submit(self.save_bytes_to_file(bytes_l, temp, gallery))
