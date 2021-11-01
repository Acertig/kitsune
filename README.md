[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
# Kitsune: An asynchronous nhentai.net API wrapper and scraper

Only contributions I allow will be accepted. This will be worked on only in my free time. 

### Current capabilities: 

- nhentai.net API endpoints data requesting 
- Searching and filtering with webscraping
- Ratelimit handling
- Downloading done via threads

### Pre-release: 

- Extra polishing, some extra refactoring and last touches.
- Licensing, uploading the package and guide on how to use.

### Post-release: 
- Even more refactoring. 
- Tweaks and changes for the http handler.

## How-to-use Guide

The main way to instantiate the wrapper class is via an async context manager which takes care of creating and closing the HTTP session internally.

```py
import asyncio

from kitsune import Kitsune

async def main():
    async with Kitsune() as client: 
        ...
    
```

You can also opt to pass your own HTTP session.

```py
import aiohttp

from kitsune import Kitsune

async def main():
    session = aiohttp.ClientSession()
    async with Kitsune.from_session(session) as client: 
        ...
   
```

Now that you have your instance of the wrapper, using it is fairly simple. Some examples below.

```py
import aiohttp

from kitsune import Kitsune, Tag, Artist

async def main():
    async with Kitsune(loop = your_loop) as client: # You can also pass your own loop, which will handle the ratelimits  
        
        gallery = await client.fetch_gallery(312781) # Fetching a gallery/doujinshi
        
        shelf = await client.search([Tag["futanari"], Tag["kitsune"], pages = [1, 10], popularity = Popularity.ALL_TIME) # Searching based on query or filter
        
        comments = await client.fetch_comments(gallery.id) # Fetching the comments from a doujin
   
```
More examples and explanations can be found on the documentation. 

Special thanks to hentai-chan for sharing the API endpoints. They were necessary for this async version of the wrapper to work.
