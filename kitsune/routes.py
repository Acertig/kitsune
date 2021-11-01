class Route: 
    
    BASE = "http://nhentai.net"

    def __init__(self, path: str = ""): 
        self.path = path
        self.url = self.BASE + path if not "https" in path else path
