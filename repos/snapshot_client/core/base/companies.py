from .. import connections

class Company(object):
    def __init__(
            self,
            url,
            pk,
            name,
            project_root,
            source_root,
            render_root,
            created,
            modified,
            shows,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.project_root = project_root
        self.source_root = source_root
        self.render_root = render_root
        self.created = created
        self.modified = modified

        #Foreign Key related data - cache this using properties setters/getters 
        self._shows = [] 
        self._shows_urls = None 
        self.shows = shows

        self.snapshot = connections.Connector()

    @property
    def shows(self):
        if self._shows_urls and not self._shows:
            for shows_url in self._shows_urls:
                self._shows.append(self.snapshot.show(show_url = shows_url))
        return self._shows

    @shows.setter
    def shows(self, value):
        self._shows_urls = value
        self._shows = []

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
        data['project_root'] = self.project_root
        data['source_root'] = self.source_root
        data['render_root'] = self.render_root
        data['created'] = self.created
        data['modified'] = self.modified
        data['shows'] = None
        if self.shows: data['shows'] = [item.url for item in self.shows]
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
            from ..deserializers import decode_companies
            import json
            self._update(json.loads(response.text, object_hook=decode_companies))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

