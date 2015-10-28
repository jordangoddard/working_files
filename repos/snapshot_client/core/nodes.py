# Generic nodes - split this up if it become too unwieldy at some point

class Group(object):
    def __init__(self, pk, url, name, asset):
        self.pk = pk
        self.url = url
        self.name = name
        self.asset = asset

        self._asset = None
        self._asset_urls = None
        self.asset = asset

        from core.connections import Connector
        self.snapshot = Connector()

    def __str__(self):
        return "%s" % self.name

    @property
    def asset(self):
        if not self._asset:
            self._asset = self.snapshot.asset(asset_url=self._asset_url)
        return self._asset

    @asset.setter
    def asset(self, value):
        from core.assets import Asset
        if value.__class__ == Asset:
            self._asset_url = value.url
            self._asset = value
        else:
            self._asset_url = value
            self._asset = None # Reset this, since the value for the asset_url has changed


class Material(object):
    def __init__(self, pk, url, name):
        self.pk = pk
        self.url = url
        self.name = name

    def __str__(self):
        return "%s" % self.name


class Action(object):
    def __init__(self, pk, url, name):
        self.pk = pk
        self.url = url
        self.name = name

    def __str__(self):
        return "%s" % self.name


class Camera(object):
    def __init__(
            self,
            pk,
            url,
            name,
            clip_start,
            clip_end,
            camera_type,
            focal_length,
            sensor_width,
    ):
        self.pk = pk
        self.url = url
        self.name = name
        self.clip_start = clip_start
        self.clip_end = clip_end
        self.camera_type = camera_type
        self.focal_length = focal_length
        self.sensor_width = sensor_width

    def __str__(self):
        return "%s > %smm" % (self.name, self.focal_length)


class World(object):
    def __init__(self, pk, url, name):
        self.pk = pk
        self.url = url
        self.name = name

    def __str__(self):
        return "%s" % self.name


class Scene(object):
    def __init__(self, pk, url, name, camera, world, frame_start, frame_end, frame_current):
        self.pk = pk
        self.url = url
        self.name = name
        self.camera = camera
        self.world = world
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.frame_current = frame_current

    def __str__(self):
        return "%s" % self.name

