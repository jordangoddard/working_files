# Class wrapper for snapshot show objects
from core import connections

class Show():
    def __init__(self, pk, url, code, name, created, modified, assets=None):
        self.pk = pk
        self.url = url
        self.code = code
        self.name = name
        self.created = created
        self.modified = modified

        # Caches for related items
        self._assets = []

        # Snapshot connector to get data
        self.snapshot = connections.Connector()

    def __str__(self):
        return "%s" % self.code

    def __repr__(self):
        return self.__str__()

    @property
    def assets(self):
        if not self._assets:
            # Not cached yet - get them
            self._assets = self.snapshot.assets(show=self.code)
            return self._assets
        return self._assets

    @assets.setter
    def assets(self, value):
        # TODO: setter needed?  This does nothing right now.
        self._assets = value
        return locals()

    def assets_filter(self, type_primary=None, type_secondary=None):
        return self.snapshot.assets(show=self, type_primary=type_primary, type_secondary=type_secondary)


