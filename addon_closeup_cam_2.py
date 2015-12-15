bl_info = {
    "name": "Move Animation Tool",
    "author": "Tangent Animation",
    "version": (0, 0, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Panel > Tangent",
    "description": "Moves animation from one object bone to another",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Home.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import datetime
import math
import mathutils
import re
import bpy


class MasterProperties(bpy.types.PropertyGroup):
    """
    Property Used for the whole GUI in general
    """

    # Get proxy objects in the scene
    def proxy_objects(self, context):
        """ Obtains a list of proxy objects from the active scene, handles reference bug in Blender 2.6x + """
        get_proxy_objects = []                                                                                         # Define list (of lists)
        get_proxy_objects.clear()                                                                                      # Format/clear list
        for pxyobj in bpy.data.scenes[bpy.context.scene.name].objects:
            if pxyobj.type == 'ARMATURE':                                                                              # Only want armatures
                name = pxyobj.name[:]                                                                                  # Passing result to a temporary variable to deal with blender bug
                get_proxy_objects.append((name, name, name))                                                           # Build the EnumProperty minimum requirements
        get_proxy_objects.sort()
        return get_proxy_objects
    scene_proxy_objects = []                                                                                           # Define list (of lists)
    scene_proxy_objects.clear()                                                                                        # Format/clear list
    scene_proxy_objects = proxy_objects                                                                                # Populate list
    bpy.types.Scene.valid_proxy_objects = bpy.props.EnumProperty(items = lambda self, context: scene_proxy_objects)    # Custom GUI variable

    # Get 'ctl' bones from selected object
    def bone_objects(self, context):
        """ Obtains a list of 'proxy' objects from the active scene, handles reference bug in Blender 2.6x + """
        get_object_bones = []                                                                                          # Define list (of lists)
        get_object_bones.clear()                                                                                       # Format/clear list
        for bnsobj in bpy.context.object.data.bones:
            if bnsobj.name.startswith("ctl."):
                name = bnsobj.name[:]                                                                                  # Passing result to a temporary variable to deal with blender bug
                get_object_bones.append((name, name, name))
        get_object_bones.sort()
        return get_object_bones
    proxy_object_bones = []                                                                                            # Define list (of lists)
    proxy_object_bones.clear()                                                                                         # Format/clear list
    proxy_object_bones = bone_objects                                                                                  # Populate list
    bpy.types.Scene.valid_object_bones = bpy.props.EnumProperty(items = lambda self, context: proxy_object_bones)      # Custom GUI variable

    # Get proxy objects in the scene
    def newproxy_objects(self, context):
        """ Obtains a list of proxy objects from the active scene, handles reference bug in Blender 2.6x + """
        newget_proxy_objects = []                                                                                         # Define list (of lists)
        newget_proxy_objects.clear()                                                                                      # Format/clear list
        for newpxyobj in bpy.data.scenes[bpy.context.scene.name].objects:
            if newpxyobj.type == 'ARMATURE':                                                                              # Only want armatures
                newname = newpxyobj.name[:]                                                                                  # Passing result to a temporary variable to deal with blender bug
                newget_proxy_objects.append((newname, newname, newname))                                                           # Build the EnumProperty minimum requirements
        newget_proxy_objects.sort()
        return newget_proxy_objects
    newscene_proxy_objects = []                                                                                           # Define list (of lists)
    newscene_proxy_objects.clear()                                                                                        # Format/clear list
    newscene_proxy_objects = newproxy_objects                                                                                # Populate list
    bpy.types.Scene.newvalid_proxy_objects = bpy.props.EnumProperty(items = lambda self, context: newscene_proxy_objects)    # Custom GUI variable

    # Get 'ctl' bones from selected object
    def newbone_objects(self, context):
        """ Obtains a list of 'proxy' objects from the active scene, handles reference bug in Blender 2.6x + """
        newget_object_bones = []                                                                                          # Define list (of lists)
        newget_object_bones.clear()                                                                                       # Format/clear list
        for newbnsobj in bpy.context.object.data.bones:
            if newbnsobj.name.startswith("ctl."):
                newname = newbnsobj.name[:]                                                                                  # Passing result to a temporary variable to deal with blender bug
                get_object_bones.append((newname, newname, newname))
        newget_object_bones.sort()
        return newget_object_bones
    newproxy_object_bones = []                                                                                            # Define list (of lists)
    newproxy_object_bones.clear()                                                                                         # Format/clear list
    newproxy_object_bones = newbone_objects                                                                                  # Populate list
    bpy.types.Scene.newvalid_object_bones = bpy.props.EnumProperty(items = lambda self, context: newproxy_object_bones)      # Custom GUI variable


class NewDisplayListOfProxies(bpy.types.Operator):
    """
    Obtain a list of proxies (armatures) from the current scene
    """
    bl_label = "New Display List Of Proxy Objects"
    bl_idname = "object.newdisplaylistofproxies"
    bl_description = "Testing New Proxy List"
    bl_options = {'UNDO'}

    def __init__(self):
        """ Initialize """
        pass

    def newproxy_list(self, context):
        """ Get list """
        newdropdown_items = []                                                                                            # Define list (of lists)
        newdropdown_items.clear()                                                                                         # Format/clear list
        newdropdown_items = MasterProperties.newproxy_objects(self, context)                                                 # Populate list
        return newdropdown_items
    newproxies_in_scene = []                                                                                              # Define list (of lists)
    newproxies_in_scene.clear()                                                                                           # Format/clear list
    newproxies_in_scene = newproxy_list                                                                                      # Populate list
    newscene_proxy_list = bpy.props.EnumProperty(items=newproxies_in_scene) 

    def execute(self, context):
        """ Allows for dynamic population of dropdown list Panel/Outliner/Viewport """
        newselected_object = self.newscene_proxy_list                                                                        # Current active object
        newvalid_objects = MasterProperties.newproxy_objects(self, context)
        for newsublist in newvalid_objects:
            if newselected_object == newsublist[1]:                                                                          # Update Outliner/Viewport with selection
                try:
                    self.newactive_object = bpy.context.scene.objects.active.name                                         # Current active object
                    bpy.context.scene.objects[self.newactive_object].select = False
                except:
                    pass
                bpy.context.scene.objects.active=bpy.context.scene.objects[newselected_object]
                bpy.context.scene.objects[newselected_object].select = True
                break
            else:
                pass
        self.newscene_proxy_list                                                                                          # Refresh list of scene proxy objects
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Call execution """
        return self.execute(context)


class NewDisplayListOfBones(bpy.types.Operator):
    """
    Obtain a list of control (ctl) bones (armatures) from the active proxy (armature)
    """
    bl_label = "New Display List Of Proxy Object Bones"
    bl_idname = "object.newdisplaylistofbones"
    bl_description = "Testing New Bones List"
    bl_options = {'UNDO'}

    def __init__(self):
        """ Initialize """
        pass

    def newbone_list(self, context):
        """ Get list """
        newdropdown_items = []                                                                                            # Define list (of lists)
        newdropdown_items.clear()                                                                                         # Format/clear list
        newdropdown_items = MasterProperties.newbone_objects(self, context)                                                  # Populate list
        return newdropdown_items
    newbones_in_object = []                                                                                               # Define list (of lists)
    newbones_in_object.clear()                                                                                            # Format/clear list
    newbones_in_object = newbone_list                                                                                        # Populate list
    newobject_bone_list = bpy.props.EnumProperty(items=newbones_in_object) 

    def execute(self, context):
        """ Allows for dynamic population of dropdown list Panel/Outliner/Viewport """
        self.newactive_object = bpy.context.scene.objects.active.name                                                     # Current active object
        newactive_rig = bpy.context.scene.objects.active.data                                                             # Current active object rig
        newactive_bone = bpy.context.object.data.bones.active.name                                                        # Current active bone
        newselected_bone = self.newobject_bone_list                                                                          # Current active object
        newvalid_bones = MasterProperties.newbone_objects(self, context)
        for newsublist in newvalid_bones:
            if newselected_bone == newsublist[1]:                                                                            # Update Outliner/Viewport with selection, activate layers
                bpy.context.object.data.bones[newactive_bone].select = False
                bpy.context.object.data.bones.active=bpy.context.object.data.bones[newselected_bone]
                bpy.context.object.data.bones[newselected_bone].select = True
                for i in range(0, 8):     # Layer range 00 - 07
                    bpy.data.armatures[newactive_rig.name].layers[i] = active_rig.bones[newselected_bone].layers[i]
                for i in range(16, 24):   # Layer range 16 - 23
                    bpy.data.armatures[newactive_rig.name].layers[i] = active_rig.bones[newselected_bone].layers[i]
                break
            else:
                pass
        if bpy.context.newactive_object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        self.newobject_bone_list                                                                                          # Refresh list of object bones
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Call execution """
        return self.execute(context)


class DisplayListOfProxies(bpy.types.Operator):
    """
    Obtain a list of proxies (armatures) from the current scene
    """
    bl_label = "Display List Of Proxy Objects"
    bl_idname = "object.displaylistofproxies"
    bl_description = "Testing Proxy List"
    bl_options = {'UNDO'}

    def __init__(self):
        """ Initialize """
        pass

    def proxy_list(self, context):
        """ Get list """
        dropdown_items = []                                                                                            # Define list (of lists)
        dropdown_items.clear()                                                                                         # Format/clear list
        dropdown_items = MasterProperties.proxy_objects(self, context)                                                 # Populate list
        return dropdown_items
    proxies_in_scene = []                                                                                              # Define list (of lists)
    proxies_in_scene.clear()                                                                                           # Format/clear list
    proxies_in_scene = proxy_list                                                                                      # Populate list
    scene_proxy_list = bpy.props.EnumProperty(items=proxies_in_scene) 

    def execute(self, context):
        """ Allows for dynamic population of dropdown list Panel/Outliner/Viewport """
        selected_object = self.scene_proxy_list                                                                        # Current active object
        valid_objects = MasterProperties.proxy_objects(self, context)
        for sublist in valid_objects:
            if selected_object == sublist[1]:                                                                          # Update Outliner/Viewport with selection
                try:
                    self.active_object = bpy.context.scene.objects.active.name                                         # Current active object
                    bpy.context.scene.objects[self.active_object].select = False
                except:
                    pass
                bpy.context.scene.objects.active=bpy.context.scene.objects[selected_object]
                bpy.context.scene.objects[selected_object].select = True
                break
            else:
                pass
        self.scene_proxy_list                                                                                          # Refresh list of scene proxy objects
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Call execution """
        return self.execute(context)


class DisplayListOfBones(bpy.types.Operator):
    """
    Obtain a list of control (ctl) bones (armatures) from the active proxy (armature)
    """
    bl_label = "Display List Of Proxy Object Bones"
    bl_idname = "object.displaylistofbones"
    bl_description = "Testing Bones List"
    bl_options = {'UNDO'}

    def __init__(self):
        """ Initialize """
        pass

    def bone_list(self, context):
        """ Get list """
        dropdown_items = []                                                                                            # Define list (of lists)
        dropdown_items.clear()                                                                                         # Format/clear list
        dropdown_items = MasterProperties.bone_objects(self, context)                                                  # Populate list
        return dropdown_items
    bones_in_object = []                                                                                               # Define list (of lists)
    bones_in_object.clear()                                                                                            # Format/clear list
    bones_in_object = bone_list                                                                                        # Populate list
    object_bone_list = bpy.props.EnumProperty(items=bones_in_object) 

    def execute(self, context):
        """ Allows for dynamic population of dropdown list Panel/Outliner/Viewport """
        self.active_object = bpy.context.scene.objects.active.name                                                     # Current active object
        active_rig = bpy.context.scene.objects.active.data                                                             # Current active object rig
        active_bone = bpy.context.object.data.bones.active.name                                                        # Current active bone
        selected_bone = self.object_bone_list                                                                          # Current active object
        valid_bones = MasterProperties.bone_objects(self, context)
        for sublist in valid_bones:
            if selected_bone == sublist[1]:                                                                            # Update Outliner/Viewport with selection, activate layers
                bpy.context.object.data.bones[active_bone].select = False
                bpy.context.object.data.bones.active=bpy.context.object.data.bones[selected_bone]
                bpy.context.object.data.bones[selected_bone].select = True
                for i in range(0, 8):     # Layer range 00 - 07
                    bpy.data.armatures[active_rig.name].layers[i] = active_rig.bones[selected_bone].layers[i]
                for i in range(16, 24):   # Layer range 16 - 23
                    bpy.data.armatures[active_rig.name].layers[i] = active_rig.bones[selected_bone].layers[i]
                break
            else:
                pass
        if bpy.context.active_object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        self.object_bone_list                                                                                          # Refresh list of object bones
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Call execution """
        return self.execute(context)


class CreateCloseUpCameraPanel(bpy.types.Panel):                                                                       # GUI
    """ 
    Create user UI panel
    """
    bl_label= "Close-Up Camera"
    bl_idname = "object.closeupcamerapanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tangent"

    def draw(self, context):                                                                                           # GUI
        proxy_in_list = True
        bone_in_list = True
        outliner_object = bpy.context.active_object
        valid_objects = MasterProperties.proxy_objects(self, context)
        '''
        if len(bpy.context.selected_objects) == 1:
            for objlist in valid_objects:
                if outliner_object.name == objlist[1]:
                    proxy_in_list = True
                    break
                    
        if proxy_in_list == True:
            bone_in_list = False
            outliner_bone = bpy.context.object.data.bones.active
            valid_bones = MasterProperties.bone_objects(self, context)
            if bpy.context.object.mode == 'POSE' and len(bpy.context.selected_pose_bones) == 1:
                for bonlist in valid_bones:
                    if outliner_bone.name == bonlist[1]:
                        bone_in_list = True
                        break
                        '''
        layout = self.layout
        col = layout.column()
        row = layout.row()
        col.label(text="Proxy Objects")
        if proxy_in_list:
            col.operator_menu_enum("object.displaylistofproxies", "scene_proxy_list", text = outliner_object.name, icon = 'OBJECT_DATA')
            col.label(text="Bones")
            if bone_in_list:                                                                                           # Valid bone type chosen in Outliner/Viewport
                if outliner_object.mode == 'POSE':                                                                     # POSE mode is enabled
                    try:                                                                                               # Ensure that an actual bone is selected
                        col.operator_menu_enum("object.displaylistofbones", "object_bone_list", text = outliner_bone.name, icon = 'BONE_DATA')
                    except:                                                                                            # Unrecognized bone selected
                        col.operator_menu_enum("object.displaylistofbones", "object_bone_list", text = "Select Controller", icon = 'BONE_DATA')
                else:                                                                                                  # OBJECT mode is enabled
                    col.operator_menu_enum("object.displaylistofbones", "object_bone_list", text = "Select Controller", icon = 'BONE_DATA')
            else:                                                                                                      # Unrecognized bone selected
                col.operator_menu_enum("object.displaylistofbones", "object_bone_list", text = "Select Controller", icon = 'BONE_DATA')
        else:                                                                                                          # Not a valid proxy object
            col.operator_menu_enum("object.displaylistofproxies", "scene_proxy_list", text = "Select Proxy Object", icon = 'OBJECT_DATA')
        
        
        
        


def register():
    """ Register classes """
    bpy.utils.register_module(__name__)


def unregister():
    """ Unregister classes """
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    if bpy.app.background:
        register()
    else:
        register()




