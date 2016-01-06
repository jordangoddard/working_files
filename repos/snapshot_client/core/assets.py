from .base.assets import Asset as Asset_base
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



class Asset(Asset_base):

    #PUT YOUR CODE HERE 
    
    def __str__(self):
        return "%s" % self.code

    def __repr__(self):
        return self.__str__()

    pass


    def set_frame_range(self):
        bpy.context.scene.frame_start = self.start_frame  # TODO: refactor to match blender variable name
        bpy.context.scene.frame_end = self.end_frame  # TODO: refactor to match blender variable name

    @property
    def playblast(self):
        return Playblast(self)

    # Stats
    @property
    def stats_version(self):
        return bpy.context.scene.statistics().replace(" ","").split("|")[0]

    @property
    def stats_verts(self):
        int(bpy.context.scene.statistics().replace(" ","").split("|")[1].split(":")[1].replace(",",""))

    @property
    def stats_faces(self):
        int(bpy.context.scene.statistics().replace(" ","").split("|")[2].split(":")[1].replace(",",""))

    @property
    def stats_tris(self):
        int(bpy.context.scene.statistics().replace(" ","").split("|")[3].split(":")[1].replace(",",""))

    @property
    def stats_objects(self):
        int(bpy.context.scene.statistics().replace(" ","").split("|")[4].split(":")[1].split("/")[1].replace(",",""))

    @property
    def stats_lamps(self):
        int(bpy.context.scene.statistics().replace(" ","").split("|")[5].split(":")[1].split("/")[1].replace(",",""))

    @property
    def stats_memory(self):
        float(bpy.context.scene.statistics().replace(" ","").split("|")[6].split(":")[1].replace("M",""))
        
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
