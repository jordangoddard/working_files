from .. import connections

class Layer(object):
    def __init__(
            self,
            url,
            pk,
            name,
            layer_type,
            start,
            end,
            created,
            modified,
            deadline,
            duration,
            render_path_linux,
            path,
            render_path_windows,
            layer_file,
            jobs,
            asset,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.layer_type = layer_type
        self.start = start
        self.end = end
        self.created = created
        self.modified = modified
        self.deadline = deadline
        self.duration = duration
        self.render_path_linux = render_path_linux
        self.path = path
        self.render_path_windows = render_path_windows
        self.layer_file = layer_file

        #Foreign Key related data - cache this using properties setters/getters 
        self._jobs = [] 
        self._jobs_urls = None 
        self.jobs = jobs

        self._asset = None 
        self._asset_urls = None 
        self.asset = asset

        self.snapshot = connections.Connector()

    @property
    def jobs(self):
        if self._jobs_urls and not self._jobs:
            for jobs_url in self._jobs_urls:
                self._jobs.append(self.snapshot.renderfarm(renderfarm_url = jobs_url))
        return self._jobs

    @jobs.setter
    def jobs(self, value):
        self._jobs_urls = value
        self._jobs = []

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
        data['layer_type'] = self.layer_type
        data['start'] = self.start
        data['end'] = self.end
        data['created'] = self.created
        data['modified'] = self.modified
        data['deadline'] = self.deadline
        data['duration'] = self.duration
        data['render_path_linux'] = self.render_path_linux
        data['path'] = self.path
        data['render_path_windows'] = self.render_path_windows
        data['layer_file'] = self.layer_file
        data['jobs'] = None
        if self.jobs: data['jobs'] = [item.url for item in self.jobs]
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
            from ..deserializers import decode_layer
            import json
            self._update(json.loads(response.text, object_hook=decode_layer))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class Render(object):
    def __init__(
            self,
            url,
            pk,
            start,
            end,
            created,
            modified,
            comp_file,
            department,
            quicktime_render_movie_windows,
            quicktime_render_movie_linux,
            deadline,
            duration,
            render_path_linux,
            quicktime_render_path_windows,
            path,
            render_path_windows,
            quicktime_render_path_linux,
            jobs,
            asset,
        ):
        self.url = url
        self.pk = pk
        self.start = start
        self.end = end
        self.created = created
        self.modified = modified
        self.comp_file = comp_file
        self.department = department
        self.quicktime_render_movie_windows = quicktime_render_movie_windows
        self.quicktime_render_movie_linux = quicktime_render_movie_linux
        self.deadline = deadline
        self.duration = duration
        self.render_path_linux = render_path_linux
        self.quicktime_render_path_windows = quicktime_render_path_windows
        self.path = path
        self.render_path_windows = render_path_windows
        self.quicktime_render_path_linux = quicktime_render_path_linux

        #Foreign Key related data - cache this using properties setters/getters 
        self._jobs = [] 
        self._jobs_urls = None 
        self.jobs = jobs

        self._asset = None 
        self._asset_urls = None 
        self.asset = asset

        self.snapshot = connections.Connector()

    @property
    def jobs(self):
        if self._jobs_urls and not self._jobs:
            for jobs_url in self._jobs_urls:
                self._jobs.append(self.snapshot.renderfarm(renderfarm_url = jobs_url))
        return self._jobs

    @jobs.setter
    def jobs(self, value):
        self._jobs_urls = value
        self._jobs = []

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
        data['start'] = self.start
        data['end'] = self.end
        data['created'] = self.created
        data['modified'] = self.modified
        data['comp_file'] = self.comp_file
        data['department'] = self.department
        data['quicktime_render_movie_windows'] = self.quicktime_render_movie_windows
        data['quicktime_render_movie_linux'] = self.quicktime_render_movie_linux
        data['deadline'] = self.deadline
        data['duration'] = self.duration
        data['render_path_linux'] = self.render_path_linux
        data['quicktime_render_path_windows'] = self.quicktime_render_path_windows
        data['path'] = self.path
        data['render_path_windows'] = self.render_path_windows
        data['quicktime_render_path_linux'] = self.quicktime_render_path_linux
        data['jobs'] = None
        if self.jobs: data['jobs'] = [item.url for item in self.jobs]
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
            from ..deserializers import decode_render
            import json
            self._update(json.loads(response.text, object_hook=decode_render))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

