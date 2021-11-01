from enum import Enum

__all__ = ("Popularity", "Tag", "Artist", "Character", "Parody", "Group",)

class Popularity(Enum): 
    RECENT = ""
    TODAY = "popular-today"
    WEEK = "popular-week"
    MONTH = "popular-month"
    YEAR = "popular-year"
    ALL_TIME = "popular"

class MetaCategory(type): 
    
    def __getitem__(self, i: str): 
        return f"{self.__name__.lower()}:{i.lower()}"

class Tag(metaclass = MetaCategory): 
    pass

class Artist(metaclass = MetaCategory): 
    pass

class Character(metaclass = MetaCategory): 
    pass

class Parody(metaclass = MetaCategory): 
    pass

class Group(metaclass = MetaCategory): 
    pass
