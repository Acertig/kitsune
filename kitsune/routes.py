from enum import Enum
from typing import Any

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

    def __init__(self, path: str, *args): 
        self.path = path
        self.url = self.BASE + self.path
        
        for arg in args: 
            self.url = self.url.replace("{}", str(arg), 1)

    def insert_temporal_param(self, param: Any): 
        return self.url.replace("{}", param)
