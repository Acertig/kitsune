
class Doujin: 
    def __init__(self, **kwargs): 
        self.name = kwargs.get("name", None)
        self.artists = kwargs.get("artists", None)
        self.favorite = kwargs.get("favorites", None)
        self.tags = kwargs.get("tag", None)
        self.languages = kwargs.get("languages", None)
        self.uploaded = kwargs.get("uploaded", None)
        self.pages = kwargs.get("pages", None)
        self.code = kwargs.get("code", None)
        self.content_cover = kwargs.get("content_cover", None)
        self.content_pages = kwargs.get("content_pages", None)
        self.content_recommended = kwargs.get("content_recommended", None)

