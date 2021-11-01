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

The main way to create the wrapper instance is via an async context manager which takes care of creating and closing the HTTP session internally.

```py
import asyncio
from kitsune import Kitsune

async def main():
  async with Kitsune() as client: 
    ...

asyncio.run(main())
```

Special thanks to hentai-chan for sharing the API endpoints. They were necessary for this async version of the wrapper to work.
