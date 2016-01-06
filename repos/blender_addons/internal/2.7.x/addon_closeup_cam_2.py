# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Close-Up Camera",
    "author": "Tangent Animation",
    "version": (2, 0, 1),
    "blender": (2, 74, 0),
    "location": "View3D > Tools",
    "description": "Creates and attaches a camera to the selected bone.",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Close-Up%20Camera.aspx",
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


class CreateCloseUpCameraPanel(bpy.types.Panel):
    """ 
    Create user UI panel
    """
    bl_label= "Close-Up Camera"
    bl_idname = "object.closeupcamerapanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "TA - Animation"
    
    def draw(self, context):
        """ Build UI panel elements """
        proxy_in_list = False
        bone_in_list = False

        outliner_object = bpy.context.active_object
        valid_objects = MasterProperties.proxy_objects(self, context)
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

        layout = self.layout
        col = layout.column()
        row = layout.row()

        col.label(text = "Adds a close-up camera")
        col.label(text = "to a control node of a")
        col.label(text = "proxy object.")

        col.label()
        col.label(text="Proxy Object")

        if proxy_in_list:
            col.operator_menu_enum("object.displaylistofproxies",
                                   "scene_proxy_list",
                                   text = outliner_object.name,
                                   icon = 'OBJECT_DATA')

            col.label(text="Controller")

            if bone_in_list:                                                                                           # Valid bone type chosen in Outliner/Viewport
                if outliner_object.mode == 'POSE':                                                                     # POSE mode is enabled
                    try:                                                                                               # Ensure that an actual bone is selected
                        col.operator_menu_enum("object.displaylistofbones",
                                               "object_bone_list",
                                               text = outliner_bone.name,
                                               icon = 'BONE_DATA')
                        col.label()
                        col.operator(operator = "animation.create_closeup_camera",
                                     text = "Assign Close-Up Camera",
                                     icon = "CAMERA_DATA")
                    except:                                                                                            # Unrecognized bone selected
                        col.operator_menu_enum("object.displaylistofbones",
                                               "object_bone_list",
                                               text = "Select Controller",
                                               icon = 'BONE_DATA')
                else:                                                                                                  # OBJECT mode is enabled
                    col.operator_menu_enum("object.displaylistofbones",
                                           "object_bone_list",
                                           text = "Select Controller",
                                           icon = 'BONE_DATA')
            else:                                                                                                      # Unrecognized bone selected
                col.operator_menu_enum("object.displaylistofbones",
                                       "object_bone_list",
                                       text = "Select Controller",
                                       icon = 'BONE_DATA')
        else:                                                                                                          # Not a valid proxy object
            col.operator_menu_enum("object.displaylistofproxies",
                                   "scene_proxy_list",
                                   text = "Select Proxy Object",
                                   icon = 'OBJECT_DATA')


class CreateCloseUpCamera(bpy.types.Operator):
    """
    Perform user request actions
    """
    bl_idname = "animation.create_closeup_camera"
    bl_label = "Assign Close-Up Camera"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """ Execute close-up camera """
        ccc = create_closeup_camera()
        ccc.execute()

        reportrig = bpy.context.object.data.name
        reportctl = bpy.context.object.data.bones.active.name
        self.report({'INFO'}, "Close-Up camera connected to '%s' on '%s'" % (reportctl, reportrig))                    # Send output to Blender Info header

        return {"FINISHED"}

class create_closeup_camera(object):

    def __init__(self):
        """ Modules in use """
        # self.app_groups = bpy.data.groups
        # self.app_objects = bpy.data.objects
        # self.app_scene = bpy.context.scene

        """ Initialize general variables """
        self.source_scene = bpy.context.scene                                                                          # store current scene
        self.source_scene_name = bpy.context.scene.name                                                                # store current scene name
        self.cam_data_name = None
        self.cam_object_name = "cam.closeup"
        self.final_object_name = None                                                                                  # name to use during creation
        self.nul_object_name = "nul.closeup"
        self.object_list = None                                                                                        # selected object(s)
        self.outliner_groupname = "grp.closeup.cams"                                                                   # master group name for outliner
        self.posebone_list = None                                                                                      # selected pose bone(s)
        self.selection_count = None

        """ Initialize logging variables """
        self.conout = False
        self.conoutmessage = None
        self.check = []
        self.error = []
        self.fail = []
        self.log = []
        self.success = []

        self.conoutmessage = ("\n\n---------- %s ----------\n\n" %datetime.datetime.now())
        if self.conout:
            print(self.conoutmessage)                                                                                  # start of execution header
        self.log.append(self.conoutmessage)

    def execute(self):
        """ Call functions here; abort if selected bones is not equal to single """
        self.store_selected_bone_object()                                                                              # store selected objects

        if self.selection_count == 1:                                                                                  # something to do
            self.generate_object_name()
            self.create_null_object()
            self.create_camera_object()
            self.create_group_object()
            self.move_null_object_vec_location()
            self.parent_null_object()
            self.constrain_object_to_selection()
            self.apply_settings_objects()
            self.refresh_source_scene()
        else:
            self.conoutmessage = "Invalid number of objects selected"
            if self.conout:
                print(self.conoutmessage)
            self.log.append(self.conoutmessage)

        self.conoutmessage = "\n\n---------- Return: FINISHED ----------\n\n"
        if self.conout:
            print(self.conoutmessage)                                                                                  # end of execution header
        self.log.append(self.conoutmessage)
#        self.process_logging()                                                                                        # logging feature
        return {'FINISHED'}

    def store_selected_bone_object(self):
        """ Copy selected to bone and owner object and check if none/multiple selected """
        self.object_list = bpy.context.selected_objects                                                                # selected object(s)
        self.posebone_list = bpy.context.selected_pose_bones                                                           # selected pose bone(s)

        if not self.posebone_list:
            self.selection_count = "0"
        else:
            self.selection_count = len(self.posebone_list)

        self.conoutmessage = ("Number of pose bones selected: %s" %self.selection_count)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def generate_object_name(self):
        """ Create new empty scene, derive new scene name from selections (60 character max) """
        """ If scene name already exists, blender adds '.###' """
        first_split = None
        second_split = None
        valid_letters = None

        object_name = self.object_list[0].name                                                                         # since it's only one selected
        bone_name = self.posebone_list[0].name                                                                         # since it's only one selected

        self.conoutmessage = ("Selected object is '%s'\nSelected bone is '%s'" % (object_name, bone_name))
        self.log.append(self.conoutmessage)

        first_split = object_name.split('.')                                                                           # split at instances of '.'
        second_split = first_split[1].split('_')                                                                       # split at instances of '_'
        if len(second_split) > 1:                                                                                      # only 1 index
            valid_letters = "abcdefghijklmnopqrstuvwxyz"
            second_split[1] = ''.join([char for char in second_split[1] if char.lower() in valid_letters])
            if len(second_split[1]) > 0:                                                                               # 2nd index empty after stripping out non-alphnumeric
                self.final_object_name = second_split[0]                                                               # name was probably non-descriptive (ex: chr###),
                self.final_object_name = ("%s_%s" % (self.final_object_name, second_split[1]))                         # so we add in 2nd half hoping it is (ex: moe)
            else:
                self.final_object_name = second_split[0]                                                               # here's to hoping the 1st half is descriptive cause we don't have a 2nd half
        else:
            self.final_object_name = second_split[0]                                                                   # here's to hoping the 1st half is descriptive cause we don't have a 2nd half

        self.final_object_name = ("%s_%s" % (self.final_object_name, bone_name))
        self.conoutmessage = ("Final object is '%s'" %self.final_object_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def create_null_object(self):
        """ Create null object ('EMPTY'), used a camera parent and selection constraint """
        nul_object_name = ("%s_%s" % (self.nul_object_name, self.final_object_name))

        nullobj = bpy.data.objects.new(nul_object_name, None)

        nullobj.location = (0,0,0)
        nullobj.empty_draw_type = 'PLAIN_AXES'
        nullobj.empty_draw_size = 0.1
        nullobj.dupli_type = 'GROUP'

        bpy.context.scene.objects.link(nullobj)

        self.nul_object_name = nullobj.name                                                                            # duplicate could have existed, so set this as new name

        self.conoutmessage = ("Created '%s'" %self.nul_object_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def create_camera_object(self):
        """ Create camera object ('CAMERAS'), this is the close-up cam """
        cam_object_name = ("%s_%s" % (self.cam_object_name, self.final_object_name))
        cam_data_name = ("%s_sub" % cam_object_name)

        cameradata = bpy.data.cameras.new(cam_data_name)
        cameraobj = bpy.data.objects.new(cam_object_name, cameradata)

        cameraobj.location = (0,0,0)
        cameraobj.rotation_euler = (0, 0, 0)                                                                           # 90 Degrees (1.5708, 0, 0)

        bpy.context.scene.objects.link(cameraobj)

        self.cam_object_name = cameraobj.name                                                                          # duplicate could have existed, so set this as new name
        self.cam_data_name = cameradata.name                                                                           # duplicate could have existed, so set this as new name

        self.conoutmessage = ("Created '%s'" %self.cam_object_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def create_group_object(self):
        """ Create outliner group if missing, add objects to it """
        if self.outliner_groupname in bpy.data.groups:
            outliner_group = bpy.data.groups[self.outliner_groupname]
            self.conoutmessage = ("Found '%s' group" %self.outliner_groupname)
            self.log.append(self.conoutmessage)
        else:
            outliner_group = bpy.data.groups.new(self.outliner_groupname)
            self.conoutmessage = ("Created '%s' group" %self.outliner_groupname)
            self.log.append(self.conoutmessage)

        try:
            outliner_group.objects.link(bpy.context.scene.objects[self.cam_object_name])                               # add camera to group
        except:
            outliner_group.objects.link(bpy.context.scene.objects[self.cam_object_name])
            self.conoutmessage = ("    Added '%s' to group '%s'" % (self.cam_object_name, self.outliner_groupname))
            self.log.append(self.conoutmessage)
        else:
            self.conoutmessage = ("    Object '%s' already in group '%s'" % (self.cam_object_name, self.outliner_groupname))
            self.log.append(self.conoutmessage)

        try:
            outliner_group.objects.link(bpy.context.scene.objects[self.nul_object_name])                               # add empty (null) to group
        except:
            outliner_group.objects.link(bpy.context.scene.objects[self.nul_object_name])
            self.conoutmessage = ("    Added '%s' to group '%s'" % (self.nul_object_name, self.outliner_groupname))
            self.log.append(self.conoutmessage)
        else:
            self.conoutmessage = ("    Object '%s' already in group '%s'" % (self.cam_object_name, self.outliner_groupname))
            self.log.append(self.conoutmessage)

        self.conoutmessage = ("Added objects to group '%s'" %self.outliner_groupname)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def move_null_object_vec_location(self):
        """ Move null (empty) object to bone head position, step camera back for ease of selection """
        vec_location = self.posebone_list[0].head                                                                     # head of the selected control

        bpy.data.objects[self.nul_object_name].location = vec_location

        self.conoutmessage = ("Moved '%s' to '%s'" % (self.nul_object_name, vec_location))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def parent_null_object(self):
        """ Parent camera object to null (empty) object """
        parent = self.nul_object_name
        child = self.cam_object_name
        bpy.context.scene.objects[child].parent = bpy.context.scene.objects[parent]

        self.conoutmessage = ("Parented '%s' to '%s'" % (self.cam_object_name, self.nul_object_name))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def constrain_object_to_selection(self):
        """ Constrain 'COPY_LOCATION' constraint to selected bone """
        objconstraint = bpy.data.objects[self.nul_object_name]                                                         # null object
        target = self.object_list[0]                                                                                   # name of selected object
        subtarget = self.posebone_list[0].name                                                                         # name of selected bone in object

        self.conoutmessage = ("Selected object is '%s'\nSelected target is '%s'\nSelected subtarget is '%s'" % (objconstraint.name, target.name, subtarget))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

        constraintype = objconstraint.constraints.new(type='COPY_LOCATION')
        constraintype.name = ("cl_%s" %self.nul_object_name)
        constraintype.target = target
        constraintype.subtarget = subtarget

        self.conoutmessage = ("Constrained location of '%s' to '%s'" % (self.nul_object_name, subtarget))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

        constraintype = objconstraint.constraints.new(type='COPY_ROTATION')                                            # Constrain 'COPY_ROTATION' constraint to selected bone
        constraintype.name = ("cr_%s" %self.nul_object_name)
        constraintype.target = target
        constraintype.subtarget = subtarget

        self.conoutmessage = ("Constrained rotation of '%s' to '%s'" % (self.nul_object_name, subtarget))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def apply_settings_objects(self):
        """ Set parameters on null (empty), camera and move to layer for cleanliness """
        """ https://tangentanimation.sharepoint.com/wiki/Pages/Layer%20Conventions.aspx """
        display_layer = 9

        bpy.data.objects[self.nul_object_name].hide = True
        bpy.data.objects[self.nul_object_name].hide_select = True

        bpy.data.cameras[self.cam_data_name].show_name = True
        bpy.context.scene.objects[self.cam_object_name].location = (0, 0, 1.5)

        # bpy.data.objects[self.cam_object_name].layers[0] = False
        # bpy.data.objects[self.cam_object_name].layers[display_layer] = True
        # bpy.data.objects[self.nul_object_name].layers[0] = False
        # bpy.data.objects[self.nul_object_name].layers[display_layer] = True

        # bpy.context.scene.layers[0]=True
        # bpy.context.scene.layers[display_layer]=True

        self.conoutmessage = ("Applying final settings")
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def refresh_source_scene(self):
        """ Done processing requests, apply scene update """
        bpy.context.scene.update()

        self.conoutmessage = ("Refreshing viewport for '%s'" %self.source_scene_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def process_logging(self):
        """ Write process log file """
        import time
        import re
        import os
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        if not os.path.exists("%s\\log" %directory):
            os.mkdir("%s\\log" %directory)
        date_var = time.strftime("%Y%m%d_%H%M") 
        log_file = "%s\\log\\%s_log_%s.log" %(directory, self.source_scene_name, date_var)
        try:
            file = open(log_file, "r")
            file.close()
        except:
            file = open(log_file, "w")
            file.close()
        file = open(log_file, "a")
        for i in self.log: 
            file.write("-%s- LOG: %s\n" %(self.source_scene_name, i))
        file.write("\n")
        for i in self.error:
            file.write("-%s- FIX: %s\n" %(self.source_scene_name, i))
        file.write("\n")
        for i in self.check: 
            file.write("-%s- CHECK: %s\n" %(self.source_scene_name, i))
        file.write("\n")    
        for i in self.success: 
            file.write("-%s- SUCCESS: %s\n" %(self.source_scene_name, i))
        file.write("\n")  
        for i in self.fail: 
            file.write("-%s- FAIL: %s\n" %(self.source_scene_name, i))
        file.close()
          
        self.warning_box(log_file)

    def warning_box(self, logfile):
        """ Output to text editor window """
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.text.open(filepath = logfile)

def register():
    """ Register classes """
    bpy.utils.register_module(__name__)
    
def unregister():
    """ Unregister classes """
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    """ Code testing, background mode """ 
    """ https://www.blender.org/api/blender_python_api_2_75a_release/bpy.app.html) """
    if bpy.app.background:
        # http://blender.stackexchange.com/questions/39641/how-to-enable-an-addon-on-startup-via-script
        # 
        # Blender launched in background mode; run relevant functions
        # UI panel classes/functions might have to be skipped or coded to accept passed parameters from here
        # Logic to iterate through all scenes in .blend file and/or file save required

        print("Blender running in background mode: %s" %(bpy.app.background))
        register()
    else:
        # Blender launched in foreground mode; wait for user interaction
        register()