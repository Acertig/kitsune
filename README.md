# Kitsune

An asynchronous nhentai.net API wrapper and scraper

As of now the wrapper has most of the functionality the API has to offer, except for the endpoint for filtering galleries by tag which I didn't include in the wrapper due to the fact that the search endpoint can already do that. The only thing left to do is to improve the quality of the code, implement GIF downloading which, according to how they are distributed across nhentai image repositories, will be quite troublesome and writing the documentation. 

On hiatus/possibly discontinued: the way the API stores the media (e.g. images and gifs) and their different types of file extensions is unclear and I've tried some workarounds to is problem but the issue persists. Everything is so mixed up it's impossible to pack it all into a single doujin object without making a request for every piece of media individually, and this is without taking into account the failed attemps since some start with i.nhentai, i3.nhentai or even t.nhentai, and the payload doesn't contain any info regarding the respective media associated with each. This is the reason the wrapper looks so ugly aside from it being my first attempt of a proper wrapper, which I persoanlly am not fond of. At the end of the day it's my fault since I decided to keep working on it despite these limitations. If this eventually changes I will be happy to come back to this project and maybe even refactor everything, until then, this it it.

### Current capabilities: 

- nhentai.net API endpoints data requesting 
- Searching and filtering with webscraping
- Ratelimit handling
- Downloading done via threads

### Post-release:
- Polishing the README.md
- Documenting all class models
- Fix the async mess
- GIF downloading support
- Pathlib support
- Tweaks and changes for the http handler
- Logging
- CLI probably
- Even more refactoring and annotation changes

## Installation

Python 3.8+

```
pip install kitsune-nh
```
Dependencies: aiohttp v3.8.0, Pillow v8.4.0

## How-to-use guide

The main way to instantiate the wrapper class is via an async context manager which takes care of creating and closing the HTTP session internally.

```py
from kitsune import Kitsune

async def main():
    async with Kitsune() as client: 
        ...
    
```

You can also opt to pass your own HTTP session.

```py
from kitsune import Kitsune

import aiohttp

async def main():

    session = aiohttp.ClientSession()
    
    async with Kitsune.from_session(session) as client: 
        ...
   
```
And for those who want to keep the client instance static, you can use it like this: 
Not yet implemented lol

Now that you have your instance of the wrapper, using it is fairly simple. Some examples below.

```py
from kitsune import Kitsune, Popularity, Tag, Artist, Character, Parody, Group 

async def main():
    async with Kitsune(loop = your_loop) as client: # Passing your own loop 
    
    	# Wrapper methods
        
        gallery = await client.fetch_gallery(312781)
        
        galleries = await client.fetch_galleries([312781, 31286, 9294])
        
        related = await client.fetch_related(312781)
        
        random_gallery = await client.fetch_random()
        
        comments = await client.fetch_comments(gallery.id)
        
        homepage = await client.fetch_homepage()
        
        shelf = await client.search(Tag["kitsune"], popularity = Popularity.ALL_TIME)
        
        await client.download(shelf, "/home/acertig/Pictures")
     
```

More examples and explanations can be found on the yet to come (lol) documentation. 
