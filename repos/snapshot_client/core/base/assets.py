from .. import connections

class Asset(object):
    def __init__(
            self,
            url,
            pk,
            type_primary,
            type_secondary,
            type_tertiary,
            code,
            description,
            comment,
            start_frame,
            end_frame,
            data,
            stats_version,
            stats_verts,
            stats_faces,
            stats_tris,
            stats_objects,
            stats_lamps,
            stats_memory,
            created,
            modified,
            current_version,
            file,
            filename,
            path,
            images,
            parents,
            layers,
            children,
            movies,
            renders,
            show,
            versions,
            groups,
        ):
        self.url = url
        self.pk = pk
        self.type_primary = type_primary
        self.type_secondary = type_secondary
        self.type_tertiary = type_tertiary
        self.code = code
        self.description = description
        self.comment = comment
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.data = data
        self.stats_version = stats_version
        self.stats_verts = stats_verts
        self.stats_faces = stats_faces
        self.stats_tris = stats_tris
        self.stats_objects = stats_objects
        self.stats_lamps = stats_lamps
        self.stats_memory = stats_memory
        self.created = created
        self.modified = modified
        self.current_version = current_version
        self.file = file
        self.filename = filename
        self.path = path

        #Foreign Key related data - cache this using properties setters/getters 
        self._images = [] 
        self._images_urls = None 
        self.images = images

        self._parents = [] 
        self._parents_urls = None 
        self.parents = parents

        self._layers = [] 
        self._layers_urls = None 
        self.layers = layers

        self._children = [] 
        self._children_urls = None 
        self.children = children

        self._movies = [] 
        self._movies_urls = None 
        self.movies = movies

        self._renders = None 
        self._renders_urls = None 
        self.renders = renders

        self._show = None 
        self._show_urls = None 
        self.show = show

        self._versions = [] 
        self._versions_urls = None 
        self.versions = versions

        self._groups = [] 
        self._groups_urls = None 
        self.groups = groups

        self.snapshot = connections.Connector()

    @property
    def images(self):
        if self._images_urls and not self._images:
            for images_url in self._images_urls:
                self._images.append(self.snapshot.images(images_url = images_url))
        return self._images

    @images.setter
    def images(self, value):
        self._images_urls = value
        self._images = []

    @property
    def parents(self):
        if self._parents_urls and not self._parents:
            for parents_url in self._parents_urls:
                self._parents.append(self.snapshot.assets(assets_url = parents_url))
        return self._parents

    @parents.setter
    def parents(self, value):
        self._parents_urls = value
        self._parents = []

    @property
    def layers(self):
        if self._layers_urls and not self._layers:
            for layers_url in self._layers_urls:
                self._layers.append(self.snapshot.layer(layer_url = layers_url))
        return self._layers

    @layers.setter
    def layers(self, value):
        self._layers_urls = value
        self._layers = []

    @property
    def children(self):
        if self._children_urls and not self._children:
            for children_url in self._children_urls:
                self._children.append(self.snapshot.assets(assets_url = children_url))
        return self._children

    @children.setter
    def children(self, value):
        self._children_urls = value
        self._children = []

    @property
    def movies(self):
        if self._movies_urls and not self._movies:
            for movies_url in self._movies_urls:
                self._movies.append(self.snapshot.movies(movies_url = movies_url))
        return self._movies

    @movies.setter
    def movies(self, value):
        self._movies_urls = value
        self._movies = []

    @property
    def renders(self):
        if self._renders_urls and not self._renders:
            self._renders = self.snapshot.render(render_url = self._renders_urls)
        return self._renders

    @renders.setter
    def renders(self, value):
        self._renders_urls = value
        self._renders = None

    @property
    def show(self):
        if self._show_urls and not self._show:
            self._show = self.snapshot.show(show_url = self._show_urls)
        return self._show

    @show.setter
    def show(self, value):
        self._show_urls = value
        self._show = None

    @property
    def versions(self):
        if self._versions_urls and not self._versions:
            for versions_url in self._versions_urls:
                self._versions.append(self.snapshot.versions(versions_url = versions_url))
        return self._versions

    @versions.setter
    def versions(self, value):
        self._versions_urls = value
        self._versions = []

    @property
    def groups(self):
        if self._groups_urls and not self._groups:
            for groups_url in self._groups_urls:
                self._groups.append(self.snapshot.group(group_url = groups_url))
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups_urls = value
        self._groups = []

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['type_primary'] = self.type_primary
        data['type_secondary'] = self.type_secondary
        data['type_tertiary'] = self.type_tertiary
        data['code'] = self.code
        data['description'] = self.description
        data['comment'] = self.comment
        data['start_frame'] = self.start_frame
        data['end_frame'] = self.end_frame
        data['data'] = self.data
        data['stats_version'] = self.stats_version
        data['stats_verts'] = self.stats_verts
        data['stats_faces'] = self.stats_faces
        data['stats_tris'] = self.stats_tris
        data['stats_objects'] = self.stats_objects
        data['stats_lamps'] = self.stats_lamps
        data['stats_memory'] = self.stats_memory
        data['created'] = self.created
        data['modified'] = self.modified
        data['current_version'] = self.current_version
        data['file'] = self.file
        data['filename'] = self.filename
        data['path'] = self.path
        data['images'] = None
        if self.images: data['images'] = [item.url for item in self.images]
        data['parents'] = None
        if self.parents: data['parents'] = [item.url for item in self.parents]
        data['layers'] = None
        if self.layers: data['layers'] = [item.url for item in self.layers]
        data['children'] = None
        if self.children: data['children'] = [item.url for item in self.children]
        data['movies'] = None
        if self.movies: data['movies'] = [item.url for item in self.movies]
        data['renders'] = None
        if self.renders: data['renders'] = self.renders.url
        data['show'] = None
        if self.show: data['show'] = self.show.url
        data['versions'] = None
        if self.versions: data['versions'] = [item.url for item in self.versions]
        data['groups'] = None
        if self.groups: data['groups'] = [item.url for item in self.groups]
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
            from ..deserializers import decode_assets
            import json
            self._update(json.loads(response.text, object_hook=decode_assets))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

