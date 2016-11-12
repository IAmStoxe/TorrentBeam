import json


class SearchResult:
    def __init__(self, title, link, added, seeds):
        self.title = title
        self.link = link
        self.added = added
        self.seeds = seeds

    def toJSON(self):
        return {"title": str(self.title), "link": str(self.link), "added": str(self.added), "seeds": str(self.seeds)}
