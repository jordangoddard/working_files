from .. import connections

class Action(object):
    def __init__(
            self,
            url,
            pk,
            name,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.snapshot = connections.Connector()

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
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
            from ..deserializers import decode_action
            import json
            self._update(json.loads(response.text, object_hook=decode_action))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class Camera(object):
    def __init__(
            self,
            url,
            pk,
            name,
            clip_start,
            clip_end,
            camera_type,
            focal_length,
            sensor_width,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.clip_start = clip_start
        self.clip_end = clip_end
        self.camera_type = camera_type
        self.focal_length = focal_length
        self.sensor_width = sensor_width
        self.snapshot = connections.Connector()

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
        data['clip_start'] = self.clip_start
        data['clip_end'] = self.clip_end
        data['camera_type'] = self.camera_type
        data['focal_length'] = self.focal_length
        data['sensor_width'] = self.sensor_width
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
            from ..deserializers import decode_camera
            import json
            self._update(json.loads(response.text, object_hook=decode_camera))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class Group(object):
    def __init__(
            self,
            url,
            pk,
            name,
            asset,
        ):
        self.url = url
        self.pk = pk
        self.name = name

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
            from ..deserializers import decode_group
            import json
            self._update(json.loads(response.text, object_hook=decode_group))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class Material(object):
    def __init__(
            self,
            url,
            pk,
            name,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.snapshot = connections.Connector()

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
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
            from ..deserializers import decode_material
            import json
            self._update(json.loads(response.text, object_hook=decode_material))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class Scene(object):
    def __init__(
            self,
            url,
            pk,
            name,
            camera,
            world,
            frame_start,
            frame_end,
            frame_current,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.camera = camera
        self.world = world
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.frame_current = frame_current
        self.snapshot = connections.Connector()

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
        data['camera'] = self.camera
        data['world'] = self.world
        data['frame_start'] = self.frame_start
        data['frame_end'] = self.frame_end
        data['frame_current'] = self.frame_current
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
            from ..deserializers import decode_scene
            import json
            self._update(json.loads(response.text, object_hook=decode_scene))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class World(object):
    def __init__(
            self,
            url,
            pk,
            name,
        ):
        self.url = url
        self.pk = pk
        self.name = name
        self.snapshot = connections.Connector()

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['name'] = self.name
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
            from ..deserializers import decode_world
            import json
            self._update(json.loads(response.text, object_hook=decode_world))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

