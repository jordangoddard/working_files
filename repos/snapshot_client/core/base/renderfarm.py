from .. import connections

class DeadlineJob(object):
    def __init__(
            self,
            url,
            pk,
            job,
            duration,
            jobtask_total_time,
            jobtask_average_time,
            jobtask_total_time_norm,
            jobtask_average_time_norm,
            created,
            modified,
            render,
            layer,
        ):
        self.url = url
        self.pk = pk
        self.job = job
        self.duration = duration
        self.jobtask_total_time = jobtask_total_time
        self.jobtask_average_time = jobtask_average_time
        self.jobtask_total_time_norm = jobtask_total_time_norm
        self.jobtask_average_time_norm = jobtask_average_time_norm
        self.created = created
        self.modified = modified

        #Foreign Key related data - cache this using properties setters/getters 
        self._render = None 
        self._render_urls = None 
        self.render = render

        self._layer = None 
        self._layer_urls = None 
        self.layer = layer

        self.snapshot = connections.Connector()

    @property
    def render(self):
        if self._render_urls and not self._render:
            self._render = self.snapshot.render(render_url = self._render_urls)
        return self._render

    @render.setter
    def render(self, value):
        self._render_urls = value
        self._render = None

    @property
    def layer(self):
        if self._layer_urls and not self._layer:
            self._layer = self.snapshot.layer(layer_url = self._layer_urls)
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer_urls = value
        self._layer = None

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['job'] = self.job
        data['duration'] = self.duration
        data['jobtask_total_time'] = self.jobtask_total_time
        data['jobtask_average_time'] = self.jobtask_average_time
        data['jobtask_total_time_norm'] = self.jobtask_total_time_norm
        data['jobtask_average_time_norm'] = self.jobtask_average_time_norm
        data['created'] = self.created
        data['modified'] = self.modified
        data['render'] = None
        if self.render: data['render'] = self.render.url
        data['layer'] = None
        if self.layer: data['layer'] = self.layer.url
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
            from ..deserializers import decode_renderfarm
            import json
            self._update(json.loads(response.text, object_hook=decode_renderfarm))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

