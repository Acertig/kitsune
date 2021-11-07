from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.7"
DESCRIPTION = "nhentai.net API wrapper for doujins"
LONG_DESCRIPTION = """
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
# Kitsune

An asynchronous nhentai.net API wrapper and scraper

As of now the wrapper has most of the functionality the API has to offer, except for the endpoint for filtering galleries by tag which I didn't include in the wrapper due to the fact that the search endpoint can already do that. The only thing left to do is to improve the quality of the code, implement GIF downloading which, according to how they are distributed across nhentai image repositories, will be quite troublesome and writing the documentation. 

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
- GIF downloading support.
- Even more refactoring. 
- Tweaks and changes for the http handler.

## Installation

Python 3.8+

```
pip install kitsune-nh
```

## How-to-use guide

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
More examples and explanations can be found on the documentation. 

Special thanks to hentai-chan for sharing the API endpoints. They were necessary for this async version of the wrapper to work. 
You can check his own sync wrapper here: https://github.com/hentai-chan/hentai
"""

setup(
    name="kitsune-nh",
    version=VERSION,
    author="https://github.com/Acertig",
    author_email="<acertig04@gmail.com>",
    license_files=("LICENSE.txt",),
    description=DESCRIPTION, 
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["aiohttp", "Pillow"],
    keywords=["python", "wrapper", "scraper", "nhentai", "anime", "manga"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix", 
        "Operating System :: Microsoft :: Windows"
    ]
)
