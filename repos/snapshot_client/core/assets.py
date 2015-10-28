# Asset class for Blender - this includes modeling assets, shots, etc.  Snapshot "tags"
# assets to describe what they are, via the type_* tags.
import bpy
from core.playblast import Playblast

class AssetInfoProperties(bpy.types.PropertyGroup):
    """ Defines properties for a Snapshot asset - enables
    tools to determine what file is currently open.  TODO:
    we may only need the URL for this - the rest can be
    pulled via the asset class, given the URL
    """
    url = bpy.props.StringProperty()
    pk = bpy.props.IntProperty()
    code = bpy.props.StringProperty()
    version = bpy.props.IntProperty()
    show_url = bpy.props.StringProperty()


class Asset(object):
    # TODO: many of the attributes are optional - make them so
    def __init__(
            self,
            pk,
            url,
            type_primary,
            type_secondary,
            type_tertiary,
            code,
            created,
            modified,
            show,
            parents,
            children,
            images,
            groups,
            data,
            start_frame = 1,
            end_frame = 24,
            comment = "<No Comment>",
            versions = [],
            path = None,
            file = None,
            filename = None,
        ):

        self.pk = pk
        self.url = url # TODO: If url is not supplied, supply the default url for an asset to create one
        if not self.url:
            self.url = "http://10.1.1.50:8000/api/assets/"
        self.type_primary = type_primary
        self.type_secondary = type_secondary
        self.type_tertiary = type_tertiary
        self.code = code
        self.created = created
        self.modified = modified
        self.show = show
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.data = data  # This is pickled data - probably need the unpickler for this
        self.path = path
        self.file = file
        self.filename = filename
        self.versions = versions
        self.comment = comment

        # Foreign Key related data - cache this using properties setters/getters
        self._show = None
        self._show_url = None
        self.show = show

        self._children = []
        self._children_urls = None
        self.children = children

        self._parents = []
        self._parents_urls = None
        self.parents = parents

        self._images = []
        self._images_urls = None
        self.images = images

        self._groups = []
        self._groups_urls = None
        self.groups = groups

        from core.connections import Connector
        self.snapshot = Connector()

    def __str__(self):
        return "%s" % self.code

    def __repr__(self):
        return self.__str__()

    # Encode for saving

    def encode(self):
        data = {}
        data['pk'] = self.pk
        data['url'] = self.url
        data['type_primary'] = self.type_primary
        data['type_secondary'] = self.type_secondary
        data['type_tertiary'] = self.type_tertiary
        data['code'] = self.code
        data['created'] = self.created
        data['modified'] = self.modified
        data['show'] = self.show.url
        data['data'] = self.data
        data['children'] = None
        data['parents'] = None
        data['images'] = None
        data['groups'] = None
        data['start_frame'] = self.start_frame
        data['end_frame'] = self.end_frame
        data['comment'] = self.comment
        if self.versions: data['versions'] =  [version for version in self.versions]  #self.wersions
        # TODO: versions should return versions objects
        #if self.versions: data['versions'] =  [version.url for version in self.versions]  #self.wersions
        if self.children: data['children'] =  [child.url for child in self.children]  #self.children
        if self.parents: data['parents'] = [parent.url for parent in self.parents]  #self.parents
        if self.images: data['images'] = [image.url for image in self.images]  #self.images
        if self.groups: data['groups'] = [group.url for group in self.groups]
        return data

    def _update(self, data):
        """
        Update the current class instance with the new data
        :param data:
        :return:
        """
        for key, value in data.__dict__.items():
            setattr(self, key, value)

    def set_frame_range(self):
        bpy.context.scene.frame_start = self.start_frame  # TODO: refactor to match blender variable name
        bpy.context.scene.frame_end = self.end_frame  # TODO: refactor to match blender variable name

    @property
    def playblast(self):
        return Playblast(self)

    @property
    def show(self):
        if not self._show:
            self._show = self.snapshot.show(self._show_url)
        return self._show

    @show.setter
    def show(self, value):
        from core.shows import Show
        if value.__class__ == Show:
            self._show_url = value.url
            self._show = value
        else:
            self._show_url = value
            self._show = None # Reset this, since the value for the show_url has changed

    @property
    def children(self):
        if self._children_urls and not self._children:
            # TODO: add filter to the REST API to get a list of children assets for a particular asset - faster
            for child_url in self._children_urls:
                self._children.append(self.snapshot.asset(asset_url=child_url))
        return self._children

    @children.setter
    def children(self, value):
        self._children_urls = value
        self._children = [] # Reset this, since the value for the show_url has changed

    @property
    def parents(self):
        if self._parents_urls and not self._parents:
            # TODO: add filter to the REST API to get a list of parents assets for a particular asset - faster
            for parent_url in self._parents_urls:
                self._parents.append(self.snapshot.asset(asset_url=parent_url))
        return self._parents

    @parents.setter
    def parents(self, value):
        self._parents_urls = value
        self._parents = [] # Reset this, since the value for the show_url has changed

    @property
    def images(self):
        if self._images_urls and not self._images:
            # TODO: add filter to the REST API to get a list of images assets for a particular asset - faster
            for image_url in self._images_urls:
                self._images.append(self.snapshot.image(image_url))
        return self._images

    @images.setter
    def images(self, value):
        self._images_urls = value
        self._images = [] # Reset this, since the value for the show_url has changed

    @property
    def groups(self):
        if self._groups_urls and not self._groups:
            # TODO: add filter to the REST API to get a list of groups assets for a particular asset - faster
            for group_url in self._groups_urls:
                self._groups.append(self.snapshot.group(group_url))
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups_urls = value
        self._groups = [] # Reset this, since the value for the show_url has changed

    """
    @property
    def blend(self):
        return "%s/%s.blend" % self.code

    @property
    def path(self):
        return "%s/%s/%s" % (self.show.path_drive, self.type_primary, self.type_secondary)
    """

    def load(self):
        from core.helpers import load_blender_file
        result = load_blender_file(self)
        self.post_load()
        return result

    def save(self):
        """
        Perform all pre and post save operations, and save information about
        the asset to the Snapshot database
        :return:
        """

        if self.pk:
            # Pre-existing object - put to update the db entry
            response = self.snapshot.session.put(self.url, self.encode())
        else:
            # New object - post instead of put
            response = self.snapshot.session.post(self.url, self.encode())

        if response.status_code == 200 or response.status_code == 201:
            # File saved correctly - update the class instance with the saved data
            from core.deserializers import decode_asset
            import json
            self._update(json.loads(response.text, object_hook = decode_asset))
        if response.status_code == 200:
            print("Updated: %s" % self.code )
        elif response.status_code == 201:
            print("Created: %s" % self.code)
        else:
            print("Error while trying to save file to the database: %s (%s)" % (self.code, response.text))

        # Save the blender file with a version
        from core.helpers import save_blender_file
        save_blender_file(self)

    def append(self):
        from core.helpers import append_blender_file
        return append_blender_file(self)

    def link(self):
        from core.helpers import link_blender_file
        return link_blender_file(self)

    def update_properties(self):
        """
        Make sure that we have a PropertyCollection that describes the
        snapshot database information for this asset
        :return:
        """
        scene = bpy.context.scene
        try:
            print("Updating Asset Properties for %s" % scene.snapshot.code)
        except:
            # Properties for this asset don't exist yet - create them
            print("Creating Asset Properties for %s" % self.code)
            bpy.utils.register_class(AssetInfoSettings)
            bpy.types.Scene.snapshot = bpy.props.PointerProperty(type=AssetInfoSettings)

        # Now, update the properties
        scene.snapshot.url = self.url
        scene.snapshot.pk = self.pk
        scene.snapshot.code = self.code
        # scene.snapshot.version = self.version
        scene.snapshot.show_url = self.show.url
        print("Asset properties for %s updated" % scene.snapshot.code)

    def post_load(self):
        """
        Run scene setup stuff after loading the file
        :return:
        """
        self.set_frame_range()
        self.update_properties()

