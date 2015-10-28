""" Various methods for use by classes, or directly """
__author__ = 'Jeff.Bell'

import bpy
from bpy.app.handlers import persistent

@persistent
def load_handler(dummy):
    print("Load Handler:", bpy.data.filepath)

bpy.app.handlers.load_post.append(load_handler)

def load_blender_file(self):
    """ Blender file load method
    """
    print("Loading %s" % self.file)
    return bpy.ops.wm.open_mainfile(filepath=self.file)

def save_blender_file(self, relative_remap=False, copy=False, compress=False):
    """ Blender file save method
    :return:
    """
    return bpy.ops.wm.save_as_mainfile(
        filepath=self.file,
        check_existing=False,
        relative_remap = relative_remap,
        copy = copy,
        compress = compress,
    )

def append_blender_file(self):
    """ Blender file load method
    """
    print("Appending %s" % self.file)

def link_blender_file(self):
    """ Blender file load method
    """
    print("Linking %s" % self.file)

"""
Blender File loading, appending, and linking examples

# Link stuff from a blend file
import bpy
scn = bpy.context.scene
filepath = "D:\\File.blend"

# append object from .blend file
with bpy.data.libraries.load(filepath) as (data_from, data_to):
    data_to.objects = data_from.objects

# link object to current scene
for obj in data_to.objects:
    if obj is not None:
        scn.objects.link(obj)

# append objects to the current scene


# Load the main file - this blows away the current context
bpy.ops.wm.open_mainfile(filepath=path)

# Save the main file
bpy.ops.wm.save_as_mainfile(filepath=path_to_export, check_existing=False )

# Persistent handlers

import bpy
from bpy.app.handlers import persistent

@persistent
def load_handler(dummy):
    print("Load Handler:", bpy.data.filepath)

bpy.app.handlers.load_post.append(load_handler)

"""
