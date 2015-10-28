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
    "name": "Create Close-Up Camera",
    "author": "Tangent Animation",
    "version": (1, 0, 1),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Panel",
    "description": "Creates and attaches a camera to the selected bone.",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Home.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import datetime
import math
import mathutils
import re
import bpy

class CreateCloseUpCameraPanel(bpy.types.Panel):
    """ Create master panel"""
    bl_label= "Close-Up Camera"
    bl_idname = "object.closeupcamerapanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tangent"
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text = "Create Close-Up Camera")
        row = layout.row()
        row.label(text = "1. Select bone (rig) control object.")
        row = layout.row()
        row.label(text = "2. Click the Assign Close-Up Camera button.")
        row = layout.row()
        row.label(text = "")

        row = layout.row()
        row.operator(operator = "animation.create_closeup_camera", text = "Assign Close-Up Camera", icon = "CAMERA_DATA")


class CreateCloseUpCamera(bpy.types.Operator):
    bl_idname = "animation.create_closeup_camera"
    bl_label = "Assign Close-Up Camera"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """
        Execute close-up camera
        """
        ccc = create_closeup_camera()
        ccc.execute()
        
        return {"FINISHED"}

class create_closeup_camera(object):

    def __init__(self):
        """
        Modules in use
        """
        # self.app_groups = bpy.data.groups
        # self.app_objects = bpy.data.objects
        # self.app_scene = bpy.context.scene

        """
        Initialize general variables
        """
        self.source_scene = bpy.context.scene                                                           # store current scene
        self.source_scene_name = bpy.context.scene.name                                                 # store current scene name
        self.cam_data_name = None
        self.cam_object_name = "cam.closeup"
        self.final_object_name = None                                                                   # name to use during creation
        self.nul_object_name = "nul.closeup"
        self.object_list = None                                                                         # selected object(s)
        self.outliner_groupname = "grp.closeup.cams"                                                    # master group name for outliner
        self.posebone_list = None                                                                       # selected pose bone(s)
        self.selection_count = None

        """
        Initialize logging variables
        """
        self.conout = True
        self.conoutmessage = None
        self.check = []
        self.error = []
        self.fail = []
        self.log = []
        self.success = []

        self.conoutmessage = ("\n\n---------- %s ----------\n\n" %datetime.datetime.now())
        if self.conout:
            print(self.conoutmessage)                                                                   # start of execution header
        self.log.append(self.conoutmessage)

    def execute(self):
        """
        Call functions here; abort if selected bones is not equal to single
        """
        self.store_selected_bone_object()                                                             # store selected objects

        if self.selection_count == 1:                                                              # something to do
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
            print(self.conoutmessage)                                                                   # end of execution header
        self.log.append(self.conoutmessage)

#        self.process_logging()                                                                         # logging feature
        return {'FINISHED'}

    def store_selected_bone_object(self):
        """
        Copy selected to bone and owner object and check if none/multiple selected
        """
        self.object_list = bpy.context.selected_objects                                                 # selected object(s)
        self.posebone_list = bpy.context.selected_pose_bones                                            # selected pose bone(s)

        if not self.posebone_list:
            self.selection_count = "0"
        else:
            self.selection_count = len(self.posebone_list)

        self.conoutmessage = ("Number of pose bones selected: %s" %self.selection_count)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def generate_object_name(self):
        """
        Create new empty scene, derive new scene name from selections (60 character max)
        If scene name already exists, blender adds '.###'
        """
        first_split = None
        second_split = None
        valid_letters = None

        object_name = self.object_list[0].name                                                          # since it's only one selected
        bone_name = self.posebone_list[0].name                                                          # since it's only one selected

        self.conoutmessage = ("Selected object is '%s'\nSelected bone is '%s'" % (object_name, bone_name))
        self.log.append(self.conoutmessage)

        first_split = object_name.split('.')                                                            # split at instances of '.'
        second_split = first_split[1].split('_')                                                        # split at instances of '_'
        if len(second_split) > 1:                                                                       # only 1 index
            valid_letters = "abcdefghijklmnopqrstuvwxyz"
            second_split[1] = ''.join([char for char in second_split[1] if char.lower() in valid_letters])
            if len(second_split[1]) > 0:                                                                # 2nd index empty after stripping out non-alphnumeric
                self.final_object_name = second_split[0]                                                # name was probably non-descriptive (ex: chr###),
                self.final_object_name = ("%s_%s" % (self.final_object_name, second_split[1]))          # so we add in 2nd half hoping it is (ex: moe)
            else:
                self.final_object_name = second_split[0]                                                # here's to hoping the 1st half is descriptive cause we don't have a 2nd half
        else:
            self.final_object_name = second_split[0]                                                    # here's to hoping the 1st half is descriptive cause we don't have a 2nd half

        self.final_object_name = ("%s_%s" % (self.final_object_name, bone_name))
        self.conoutmessage = ("Final object is '%s'" %self.final_object_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def create_null_object(self):
        """
        Create null object ('EMPTY'), used a camera parent and selection constraint
        """
        nul_object_name = ("%s_%s" % (self.nul_object_name, self.final_object_name))

        nullobj = bpy.data.objects.new(nul_object_name, None)

        nullobj.location = (0,0,0)
        nullobj.empty_draw_type = 'PLAIN_AXES'
        nullobj.empty_draw_size = 0.1
        nullobj.dupli_type = 'GROUP'

        bpy.context.scene.objects.link(nullobj)

        self.nul_object_name = nullobj.name                                                             # duplicate could have existed, so set this as new name

        self.conoutmessage = ("Created '%s'" %self.nul_object_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def create_camera_object(self):
        """
        Create camera object ('CAMERAS'), this is the close-up cam
        """
        cam_object_name = ("%s_%s" % (self.cam_object_name, self.final_object_name))
        cam_data_name = ("%s_sub" % cam_object_name)

        cameradata = bpy.data.cameras.new(cam_data_name)
        cameraobj = bpy.data.objects.new(cam_object_name, cameradata)

        cameraobj.location = (0,0,0)
        cameraobj.rotation_euler = (0, 0, 0)                                                            # 90 Degrees (1.5708, 0, 0)

        bpy.context.scene.objects.link(cameraobj)

        self.cam_object_name = cameraobj.name                                                           # duplicate could have existed, so set this as new name
        self.cam_data_name = cameradata.name                                                            # duplicate could have existed, so set this as new name

        self.conoutmessage = ("Created '%s'" %self.cam_object_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def create_group_object(self):
        """
        Create outliner group if missing, add objects to it
        """
        if self.outliner_groupname in bpy.data.groups:
            outliner_group = bpy.data.groups[self.outliner_groupname]
            self.conoutmessage = ("Found '%s' group" %self.outliner_groupname)
            self.log.append(self.conoutmessage)
        else:
            outliner_group = bpy.data.groups.new(self.outliner_groupname)
            self.conoutmessage = ("Created '%s' group" %self.outliner_groupname)
            self.log.append(self.conoutmessage)

        try:
            outliner_group.objects.link(bpy.context.scene.objects[self.cam_object_name])                # add camera to group
        except:
            outliner_group.objects.link(bpy.context.scene.objects[self.cam_object_name])
            self.conoutmessage = ("    Added '%s' to group '%s'" % (self.cam_object_name, self.outliner_groupname))
            self.log.append(self.conoutmessage)
        else:
            self.conoutmessage = ("    Object '%s' already in group '%s'" % (self.cam_object_name, self.outliner_groupname))
            self.log.append(self.conoutmessage)

        try:
            outliner_group.objects.link(bpy.context.scene.objects[self.nul_object_name])                # add empty (null) to group
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
        """
        Move null (empty) object to head position of selected bone
        and step camera back for ease of user selection
        """
        vec_location = self.posebone_list[0].head                                                      # head of the selected control

        bpy.data.objects[self.nul_object_name].location = vec_location

        self.conoutmessage = ("Moved '%s' to '%s'" % (self.nul_object_name, vec_location))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def parent_null_object(self):
        """
        Parent camera object to null (empty) object
        """
        parent = self.nul_object_name
        child = self.cam_object_name
        bpy.context.scene.objects[child].parent = bpy.context.scene.objects[parent]

        self.conoutmessage = ("Parented '%s' to '%s'" % (self.cam_object_name, self.nul_object_name))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def constrain_object_to_selection(self):
        """
        Constrain 'COPY_LOCATION' constraint to selected bone
        """
        objconstraint = bpy.data.objects[self.nul_object_name]                                          # null object
        target = self.object_list[0]                                                                    # name of selected object
        subtarget = self.posebone_list[0].name                                                          # name of selected bone in object

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

        """
        Constrain 'COPY_ROTATION' constraint to selected bone
        """
        constraintype = objconstraint.constraints.new(type='COPY_ROTATION')
        constraintype.name = ("cr_%s" %self.nul_object_name)
        constraintype.target = target
        constraintype.subtarget = subtarget

        self.conoutmessage = ("Constrained rotation of '%s' to '%s'" % (self.nul_object_name, subtarget))
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def apply_settings_objects(self):
        """
        Set parameters on null (empty), camera and move to layer for cleanliness
        
        https://tangentanimation.sharepoint.com/wiki/Pages/Layer%20Conventions.aspx
        """
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
        """
        Done processing requests, apply scene update
        """
        bpy.context.scene.update()

        self.conoutmessage = ("Refreshing viewport for '%s'" %self.source_scene_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def process_logging(self):                               
        """
        Write process log file
        """
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

        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.text.open(filepath = logfile)

def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    register()