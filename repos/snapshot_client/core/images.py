__author__ = 'Jeff.Bell'

class Image(object):
    def __init__(self, pk, url, name, filepath, assets, width, height, created, modified):
        self.pk = pk
        self.url = url
        self.name = name
        self.filepath = filepath
        self.assets = assets
        self.created = created
        self.modified = modified
        self.width = width
        self.height = height

    def __str__(self):
        return ("%s > %s > %s.%s" (self.name, self.filepath, self.width, self.height))
