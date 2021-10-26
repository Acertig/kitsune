from enum import Enum

__all__ = ("Popularity",)

class Popularity(Enum): 
    RECENT = ""
    TODAY = "popular-today"
    WEEK = "popular-week"
    MONTH = "popular-month"
    YEAR = "popular-year"
    ALL_TIME = "popular"

class Route: 
    
    BASE = "http://nhentai.net"

    def __init__(self, path: str = ""): 
        self.path = path
        self.url = self.BASE + path if not "https" in path else path
