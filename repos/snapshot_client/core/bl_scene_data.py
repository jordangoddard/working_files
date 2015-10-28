# Blender data to store

import bpy

class BlenderData(object):
    def __init__(self):
        self.data = [
        'actions', 'armatures', 'brushes', 
        'cameras', 'curves', 'filepath', 'fonts', 
        'grease_pencil', 'groups', 'images',  
        'lamps', 'lattices', 'libraries', 
        'linestyles', 'masks', 'materials', 'meshes', 
        'metaballs', 'movieclips', 'node_groups', 
        'objects', 'particles', 'scenes', 
        'scripts', 'shape_keys', 'sounds', 
        'speakers', 'texts', 'textures', 'worlds']

        """
        Encode the following in the DB

        actions
        cameras
        groups
        images
        node_groups
        particles
        scenes
        worlds
        """

    @property
    def actions(self):
        # Return a list of the local actions in the scene
        actions = bpy.data.actions
        local_actions = []
        for action in actions:
            if not action.is_library_indirect:
                local_actions.append(BlenderAction(action))
        return local_actions

    '''
    @actions.setter
    def actions(self, value):
        self.actions = value
        return locals()
    '''

    @property
    def groups(self):
        # Return a list of the local groups in the scene
        groups = bpy.data.groups
        local_groups = []
        for group in groups:
            if not group.is_library_indirect:
                local_groups.append(BlenderGroup(group))
        return local_groups

    @property
    def images(self):
        # Return a list of the local images in the scene
        images = bpy.data.images
        local_images = []
        for image in images:
            if not image.is_library_indirect:
                local_images.append(BlenderImage(image))
        return local_images


class BlenderAction(object):
    def __init__(self, action):
        self.name = action.name
        self.start_frame = action.frame_range[0]
        self.end_frame = action.frame_range[1]

        # TODO: take care of other values, such as groups, fcurves, pose_markers, etc

class BlenderGroup(object):
    def __init__(self, group):
        self.name = group.name

        # TODO: there are a few other attributes that may be of interest, including
        # group.objects, group.layers, etc.


class BlenderImage(object):
    def __init__(self, image):
        self.name = image.name
        self.depth = image.depth
        self.display_aspect = image.display_aspect
        self.filepath = image.filepath
        self.filepath_from_user = image.filepath_from_user
        self.size_x = image.size[0]
        self.size_y = image.size[1]
        self.file_format = image.file_format

        # Note:  images are unique to their filepaths on disk - look for a way
        # to use the filepath as an index for the images, and do not allow
        # duplicates in the database.  If a duplicate is found, create a link
        # to the asset that's using the image, so there's a singular reference
        # to it across all assets that use it.  

