from .. import connections

class Movie(object):
    def __init__(
            self,
            url,
            pk,
            name,
            filepath,
            created,
            modified,
            asset,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.filepath = filepath
        self.created = created
        self.modified = modified

        #Foreign Key related data - cache this using properties setters/getters 
        self._asset = None 
        self._asset_urls = None 
        self.asset = asset

        self.snapshot = connections.Connector()

    @property
    def asset(self):
        if self._asset_urls and not self._asset:
            self._asset = self.snapshot.assets(assets_url = self._asset_urls)
        return self._asset

    @asset.setter
    def asset(self, value):
        self._asset_urls = value
        self._asset = None

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
        data['filepath'] = self.filepath
        data['created'] = self.created
        data['modified'] = self.modified
        data['asset'] = None
        if self.asset: data['asset'] = self.asset.url
        return data

    def _update(self, data):
        for key, value in data.__dict__.items():
            setattr(self, key, value)

    def save(self):
        if self.pk:
            response = self.snapshot.session.put(self.url, self.encode())
        else:
            response = self.snapshot.session.post(self.url, self.encode())
        if response.status_code in [200, 201]:
            from ..deserializers import decode_movies
            import json
            self._update(json.loads(response.text, object_hook=decode_movies))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

