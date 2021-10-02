from enum import Enum

from constants import BASE

__all__ = ("Popularity", "Filtering",)

class FieldsNotValid(Exception): 
    pass


class Popularity(Enum): 
    RECENT = ""
    TODAY = "popular-today"
    WEEK = "popular-week"
    ALL_TIME = "popular"

class Category(Enum): 
    TAGS = "tags"
    ARTISTS = "artists"
    CHARACTERS = "characters"
    PARODIES = "parodies"
    GROUPS = "groups"
    LANGUAGE = "language"

# Main objects

class APIRoute:

    __slots__ = ("id",)

    def __init__(self, id: int): 
        self.id = id
    
    @property
    def url(self): 
        return BASE + f"/api/gallery/{self.id}"

class SearchRoute: 
    
    __slots__ = ("query", "popularity", "category",)

    def __init__(self, query: str, popularity: Popularity, category: Category):
        self.query = query
        self.popularity = popularity
        self.category = category

        if self.popularity != Popularity.RECENT and not isinstance(self.popularity, Popularity): 
            raise FieldsNotValid("Popularity field should be of type: enum Popularity.")

        if self.category is not None and not isinstance(self.category, Category):  
            raise FieldsNotValid("Category field should be of type: enum Category.") 

    def get_url(self, page: int) -> str: 
        if self.category is None: 
            return BASE + f"/search/?q={self.query}&sort={self.popularity.value}&page={page}"

        return BASE + f"/{self.category.value}/{self.query}/{self.popularity.value}?page={page}"


