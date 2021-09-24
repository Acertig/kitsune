from enum import Enum

__all__ = ("Popularity", "Filtering",)

# Exception subclassing

class FieldsNotValid(Exception): 
    pass

# Filter constants

class Popularity(Enum): 
    RECENT = ""
    TODAY = "popular-today"
    WEEK = "popular-week"
    ALL_TIME = "popular"

class Filtering(Enum): 
    DOUJIN = "g"
    TAGS = "tags"
    ARTISTS = "artists"
    CHARACTERS = "characters"
    PARODIES = "parodies"
    GROUPS = "groups"
    LANGUAGE = "language"

# Main objects

class Query: 
    
    __slots__ = ("query", "page", "pages", "filtering", "popularity",)

    def __init__(self, query: str, pages: int, popularity: Popularity, filtering: Filtering):
        self.query = query
        self.page = 1
        self.pages = pages
        self.popularity = popularity
        self.filtering = filtering

        if self.popularity != Popularity.RECENT: 
            if not isinstance(self.popularity, Popularity): 
                raise FieldsNotValid("Popularity field should be of type: enum Popularity.")

        if self.filtering is not None: 
            if not isinstance(self.filtering, Filtering): 
                raise FieldsNotValid("Filtering field should be of type: enum Filtering.") 

    @property
    def built(self) -> str: 
        if self.filtering is None: 
            return f"/search/?q={self.query}&sort={self.popularity.value}&page={self.page}"

        return f"/{self.filtering.value}/{self.query}/{self.popularity.value}?page={self.page}"


