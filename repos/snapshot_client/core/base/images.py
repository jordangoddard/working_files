from .. import connections

class Image(object):
    def __init__(
            self,
            url,
            pk,
            name,
            filepath,
            created,
            modified,
            assets,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.filepath = filepath
        self.created = created
        self.modified = modified

        #Foreign Key related data - cache this using properties setters/getters 
        self._assets = [] 
        self._assets_urls = None 
        self.assets = assets

        self.snapshot = connections.Connector()

    @property
    def assets(self):
        if self._assets_urls and not self._assets:
            for assets_url in self._assets_urls:
                self._assets.append(self.snapshot.assets(assets_url = assets_url))
        return self._assets

    @assets.setter
    def assets(self, value):
        self._assets_urls = value
        self._assets = []

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
        data['filepath'] = self.filepath
        data['created'] = self.created
        data['modified'] = self.modified
        data['assets'] = None
        if self.assets: data['assets'] = [item.url for item in self.assets]
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
            from ..deserializers import decode_images
            import json
            self._update(json.loads(response.text, object_hook=decode_images))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

