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
    "name": "Create New Resolution Scene",
    "author": "Tangent Animation",
    "version": (1, 2, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tools",
    "description": "Creates a lightweight scene from selected objects",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Create%20New%20Resolution%20Scene.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import datetime
import math
import mathutils
import re
import os
import bpy

# class CreateAnimationScenePanel(bpy.types.Panel):
#     """ Create master panel"""
#     bl_label= "Animation"
#     bl_idname = "object.tempanimscenepanel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "TOOLS"
#     bl_category = "TA - Animation"
#
#     def draw(self, context):
#         layout = self.layout
#
#         row = layout.row()
#         row.label(text = "Create Temporary Animation Scene")
#         row = layout.row()
#         row.label(text = "1. Select objects to add in new scene.")
#         row = layout.row()
#         row.label(text = "2. Click the desired resolution of the asset.")
#         row = layout.row()
#         row.label(text = "")
#
#         row = layout.row()
#         row.operator(operator = "animation.create_low_resolution", text = "Low", icon = "RENDER_ANIMATION")
#
#         row = layout.row()
#         row.operator(operator = "animation.create_mid_resolution", text = "Medium", icon = "RENDER_ANIMATION")
#
#         row = layout.row()
#         row.operator(operator = "animation.create_high_resolution", text = "High", icon = "RENDER_ANIMATION")


class CreateLowResolution(bpy.types.Operator):
    bl_idname = "animation.create_low_resolution"
    bl_label = "Create Temporary Animation Scene (Low)"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """
        Sets asset resolution mode to: LOW
        """
        cas = create_anim_scene("LOW")
        cas.execute()
        
        return {"FINISHED"}


class CreateMidResolution(bpy.types.Operator):
    bl_idname = "animation.create_mid_resolution"
    bl_label = "Create Temporary Animation Scene (Mid)"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """
        Sets asset resolution mode to: MID
        """
        cas = create_anim_scene("MID")
        cas.execute()

        return {"FINISHED"}

class CreateHiResResolution(bpy.types.Operator):
    bl_idname = "animation.create_high_resolution"
    bl_label = "Create Temporary Animation Scene (Current/High)"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """
        Sets asset resolution mode to use current asset resolution
        """
        cas = create_anim_scene("HIGH")
        cas.execute()

        return {"FINISHED"}

class create_anim_scene(object):

    def __init__(self, asset_resolution):
        """
        Modules in use
        """
        # self.app_groups = bpy.data.groups
        # self.app_libraries = bpy.data.libraries
        # self.app_object = bpy.ops.object
        # self.app_objects = bpy.data.objects
        # self.app_screen = bpy.context.screen
        # self.app_scene = bpy.context.scene
        # self.app_scenes = bpy.data.scenes

        """
        Initialize variables
        """
        self.source_scene = bpy.context.scene                                                                   # store current scene
        self.source_scene_name = bpy.context.scene.name                                                         # store current scene name
        self.target_scene_name = None                                                                           # target scene name
        self.asset_resolution = asset_resolution                                                                # resolution of object (HIGH, LOW, MID)
        self.object_list = []                                                                                   # items to process
        self.old_filepath = []                                                                                  # source object filepath

        self.conout = False
        self.conoutmessage = None
        self.displaylog = False
        self.error = []
        self.log = []
        self.check = []
        self.success = []
        self.fail = []

        self.conoutmessage = ("---------- %s ----------\n" %datetime.datetime.now())
        if self.conout:
            print("\n\n%s" %self.conoutmessage)                                                                 # start of execution header
        self.log.append(self.conoutmessage)

    def execute(self):
        """
        Call functions here; abort if no selected objects
        """
        self.store_selected_scene_objects()                                                                     # store selected objects

        if len(self.object_list) > 0:                                                                           # something to do
            self.create_new_empty_scene()
            self.center_3d_cursor()
            self.link_asset()
            self.link_audiostrips()
            self.playback_settings()
            self.framerange_values()
            self.keyingset_selection()
            self.select_source_scene()
        else:
            self.conoutmessage = "No objects selected"
            self.fail.append(self.conoutmessage)
            if self.conout:
                print(self.conoutmessage)

        self.conoutmessage = "\n\n---------- Return: FINISHED ----------"
        if self.conout:
            print("%s\n" %self.conoutmessage)                                                                   # System console logging
        self.log.append(self.conoutmessage)

        if self.displaylog:
            logging = ProcessLogging(self.check, self.error, self.fail, self.log, self.success, self.source_scene_name)
            logging.execute()                                                                                       # Write results to log file

        return {'FINISHED'}

    def store_selected_scene_objects(self):
        """
        Copy selected object list to an array as 'bpy.ops.object.make_links_scene' is global
        """
        for obj in bpy.context.scene.objects:
            if bpy.context.scene.objects[obj.name].select:                                                      # have to check actual 'selected' state
                self.object_list.append(obj)
                self.conoutmessage = ("Adding selected object: %s" %obj.name)
                if self.conout:
                    print(self.conoutmessage)                                                                   # System console logging
                self.log.append(self.conoutmessage)

        self.conoutmessage = ("Number of objects selected: %s" %str(len(self.object_list)))
        if self.conout:
            print(self.conoutmessage)                                                                           # System console logging
        self.log.append(self.conoutmessage)

    def create_new_empty_scene(self):
        """
        Create new empty scene, derive new scene name from selections (60 character max)
        If scene name already exists, blender adds '.###'
        """
        self.target_scene_name = ("%s_%s" % (str(self.source_scene_name[:50]), self.asset_resolution)).lower()

        bpy.context.screen.scene = bpy.data.scenes.new(self.target_scene_name)                                  # create new scene and make it active
        self.target_scene_name = bpy.context.screen.scene.name                                                  # get the current scene name cause it might have existed and been auto-incremented
        
        selection_pattern = bpy.ops.object.select_pattern                                                       # ensure new scene is empty
        for obj in bpy.data.scenes[self.target_scene_name].objects:
            selection_pattern(pattern=obj.name)
            bpy.ops.object.delete()

        self.conoutmessage = ("Creating scene '%s'" %self.target_scene_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

#    def create_new_empty_scene(self):
#        """
#        Create new empty scene, derive new scene name from selections (60 character max)
#        If scene name already exists, blender adds '.###'
#        """
#        valid_letters = None
#        first_split = None
#        second_split = None
#        self.target_scene_name = self.source_scene_name.lower()                                                 # begin with source scene name (ex: ###.####)
#
#        self.log.append("Source scene name is '%s'" %self.source_scene_name)
#        for obj in self.object_list:
#            if obj.name.startswith('grp.'):                                                                     # filter to 'grp.' based names
#                first_split = obj.name.split('.')                                                               # split at instances of '.'
#                second_split = first_split[1].split('_')                                                        # split at instances of '_'
#                if len(second_split) > 1:                                                                       # only 1 index
#                    if not "proxy" in second_split:                                                             # skip if 2nd index contains 'proxy'
#                        valid_letters = "abcdefghijklmnopqrstuvwxyz"
#                        second_split[1] = ''.join([char for char in second_split[1] if char.lower() in valid_letters])
#                        if len(second_split[1]) > 0:                                                            # 2nd index empty after stripping out non-alphnumeric
#                            self.target_scene_name = ("%s_%s" % (self.target_scene_name, second_split[0]))      # name was probably non-descriptive (ex: chr###),
#                            self.target_scene_name = ("%s_%s" % (self.target_scene_name, second_split[1]))      # so we add in 2nd half hoping it is (ex: moe)
#                        else:
#                            self.target_scene_name = ("%s_%s" % (self.target_scene_name, second_split[0]))      # here's to hoping the 1st half is descriptive cause we don't have a 2nd half
#                else:
#                    self.target_scene_name = ("%s_%s" % (self.target_scene_name, second_split[0]))              # here's to hoping the 1st half is descriptive cause we don't have a 2nd half
#        self.target_scene_name = self.target_scene_name[:60].lower()                                            # scene box supports 64 chars but we need to reserve last 4 for '.###'
#        bpy.context.screen.scene = bpy.data.scenes.new(self.target_scene_name)                                  # create new scene and make it active
#        self.target_scene_name = bpy.context.screen.scene.name                                                  # get the current scene name cause it might have existed and been auto-incremented
#
#        selection_pattern = bpy.ops.object.select_pattern                                                       # ensure new scene is empty
#        for obj in bpy.data.scenes[self.target_scene_name].objects:
#            selection_pattern(pattern=obj.name)
#            bpy.ops.object.delete()
#
#        self.conoutmessage = ("Creating scene '%s'" %self.target_scene_name)
#        if self.conout:
#            print(self.conoutmessage)
#        self.log.append(self.conoutmessage)

    def center_3d_cursor(self):
        """
        Set 3D cursor (0, 0, 0), this revealed to be unnecessary during testing
        but adding it in to deal with unanticipated scenarios
        """
        bpy.context.scene.cursor_location.xyz = (0,0,0)

        self.conoutmessage = ("Moving 3D Cursor to origin")
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def link_asset(self):
        """ Link selected asset to new scene, use desired resolution for externally linked assets """
        for obj in self.object_list:
            try:
                obj.dupli_group.name                                                                            # check if externally linked object
            except:                                                                                             # make the non-externally linked object active so that it can be linked to new scene
                bpy.data.scenes[self.target_scene_name].objects.link(bpy.data.scenes[self.source_scene_name].objects[obj.name])
                self.conoutmessage = ("Linked '%s' to '%s'" % (obj.name, self.target_scene_name))
            else:                                                                                               # link in groups from publish file, return the name of the group
                object_name = obj.name
                group_name = obj.dupli_group.name                                                               # get the 'dupli_group.name'
                group = bpy.data.groups[group_name]                                                             # get the '.name' too
                try:
                    publish_link = group.library.filepath                                                       # get '.library.filepath'
                except:
                    self.conoutmessage = ("Asset '%s' has a 'dupli_group' but not externally linked" %obj.name)
                else:
                    target_group_name = self.link_in_groups(publish_link, object_name, group_name)              # has a 'dupli_group' and is externally linked
                    self.conoutmessage = ("Asset '%s' has a 'dupli_group' and externally linked" %obj.name)

            if self.conout:
                print(self.conoutmessage)
            self.log.append(self.conoutmessage)

    def link_in_groups(self, path, object_name, group_name): 
        """"
        Given the link of the blender file, link in the asset in the blender file; possible
        resolutions are: 'LOW', 'MID', and a fake conditional 'HIGH' to use existing scene
        asset at existing resolution
        """
        groupname = None
        found = False
        asset_resolution_filter = ("_%s." %self.asset_resolution)                                               # relax resolution filter 
        self.conoutmessage = ("Look for desired asset resolution: '%s'" %asset_resolution_filter)               # this should contain 'LOW', 'MID', or dummy 'HIGH'
        self.log.append(self.conoutmessage)

        try:
            test_blend = bpy.data.libraries.load(path, link = True)
        except:
            bpy.data.scenes[self.target_scene_name].objects.link(bpy.data.scenes[self.source_scene_name].objects[object_name])
            self.conoutmessage = ("    Linking existing version of '%s'" %object_name)
            if self.conout:
                print(self.conoutmessage)
            self.log.append(self.conoutmessage)
        else:
            with bpy.data.libraries.load(path, link = True) as (data_from, data_to):
                for group in data_from.groups:                                                                  # search through .BLEND for 'GROUP' Data Select Object
                    self.conoutmessage = ("    Found: '%s' \n       in: '%s'" % (group, path))
                    self.log.append(self.conoutmessage)
                    groupname = None                                                                            # clear last value
                    testgroup = None                                                                            # clear last evaluator
                    if group.endswith(asset_resolution_filter[0:-1]) or (asset_resolution_filter in group):     # looking for '_xxx' or '_xxx.'
                        testgroup = group.rsplit(asset_resolution_filter[0:-1])                                 # more than one '_xxx' in group
                        if testgroup[0] == group_name:
                            groupname = group
                            found = True
                            data_to.groups = [groupname]
                            break
                    elif asset_resolution_filter[0:-1] == "_MID":                                               # check for '_LOW' version since no '_MID' exists
                        lowres_check = "_LOW."                                                                  # relax resolution filter 
                        if group.endswith(lowres_check[0:-1]) or (lowres_check in group):                       # looking for '_xxx' or '_xxx.'
                            testgroup = group.rsplit(lowres_check[0:-1])                                        # more than one '_xxx' in group
                            if testgroup[0] == group_name:
                                groupname = group
                                found = True
                                data_to.groups = [groupname]
                                break

                if found:
                    self.conoutmessage = ("    Setting link to '%s'" %groupname)
                    if self.conout:
                        print(self.conoutmessage)
                    self.log.append(self.conoutmessage)
                else:
                    bpy.data.scenes[self.target_scene_name].objects.link(bpy.data.scenes[self.source_scene_name].objects[object_name])
                    self.conoutmessage = ("    Linking existing version of '%s'" %object_name)
                    if self.conout:
                        print(self.conoutmessage)
                    self.log.append(self.conoutmessage)
                    return group_name

            """
            Add a null object to duplicate the group (link the group back in the scene)
            """
            null = bpy.data.objects.new(groupname, None)
            null.location = (0,0,0)
            null.empty_draw_type = 'PLAIN_AXES'
            null.dupli_type = 'GROUP'

            null.dupli_group = bpy.data.groups[groupname]

            group_name = null.name 
            bpy.context.scene.objects.link(null)
            bpy.context.scene.update()

            self.conoutmessage = ("    Adding '%s' to '%s' " % (groupname, self.target_scene_name))
            if self.conout:
                print(self.conoutmessage)
            self.log.append(self.conoutmessage)

        return group_name  

    def link_audiostrips(self):
        """
        Create audio sequence if necessary, link audio strips from source to target
        """
        if str(bpy.data.scenes[self.target_scene_name].sequence_editor) == "None":
            bpy.data.scenes[self.target_scene_name].sequence_editor_create()
            self.log.append("Create audio sequence")
        else:
            self.conoutmessage = ("Couldn't create empty audio sequence")

        try:
            for audio in bpy.data.scenes[self.source_scene_name].sequence_editor.sequences_all:
                self.log.append("Linking '%s' audio strip" %audio)
                bpy.data.scenes[self.target_scene_name].sequence_editor.sequences.new_sound(audio.name, audio.filepath, audio.channel, audio.frame_start)
            self.conoutmessage = ("Linked audio strip(s)")
        except:
            self.conoutmessage = ("No audio strips found")

        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def playback_settings(self):
        """
        Set Playback 'AV-Sync' and 'Audio Scrubbing' to match source scene settings
        """
        bpy.data.scenes[self.target_scene_name].sync_mode = bpy.data.scenes[self.source_scene_name].sync_mode
        bpy.data.scenes[self.target_scene_name].use_audio_scrub = bpy.data.scenes[self.source_scene_name].use_audio_scrub

        self.conoutmessage = ("Changed AV-Sync and Audio Scrubbing to match '%s'" %self.source_scene_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def framerange_values(self):
        """
        Set frame range to match source scene settings
        """
        bpy.data.scenes[self.target_scene_name].frame_end = bpy.data.scenes[self.source_scene_name].frame_end
        bpy.data.scenes[self.target_scene_name].frame_start = bpy.data.scenes[self.source_scene_name].frame_start
        bpy.data.scenes[self.target_scene_name].frame_current = bpy.data.scenes[self.source_scene_name].frame_current

        self.conoutmessage = ("Changed start, end, and current frame values to match '%s'" %self.source_scene_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def keyingset_selection(self):
        """
        Set frame range to match source scene settings
        """
        source_scene_keyset = None

        try:
            source_scene_keyset = bpy.data.scenes[self.source_scene_name].keying_sets_all.active.bl_label
        except:
            self.conoutmessage = ("No active keying set")
        else:
            self.conoutmessage = ("Changed active keying set to match '%s'" %self.source_scene_name)
            bpy.data.scenes[self.target_scene_name].keying_sets_all.active_index = bpy.data.scenes[self.source_scene_name].keying_sets_all.active_index

        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

    def select_source_scene(self):
        """
        Done processing requests, reset scene to source scene
        """
        bpy.context.screen.scene = bpy.data.scenes[self.source_scene_name]

        self.conoutmessage = ("Setting viewport scene back to '%s'" %self.source_scene_name)
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)


class ProcessLogging(object):
    """
    Write script activity to log
    """
    def __init__(self, check = None, error = None, fail = None, log = None, success = None, source_scene_name = None):
        """ Initialize logging variables """
        self.source_scene_name = source_scene_name
        self.conout = False
        self.conoutmessage = None
        self.check = check                                                                                     # Warning
        self.error = error                                                                                     # Unhandled exception
        self.fail = fail                                                                                       # Didn't complete as expected
        self.log = log                                                                                         # General processing comments
        self.success = success                                                                                 # Completed as expected

    def execute(self):
        """ Write process log file """
        # import datetime
        # import re
        # import os
        # filepath = bpy.data.filepath                                                                         # .BLEND file path
        filepath = "c:\\temp\\"                                                                                # Local drive
        directory = os.path.dirname(filepath)
        if not os.path.exists("%s\\log" %directory):
            os.mkdir("%s\\log" %directory)
        date_var = datetime.datetime.now().strftime("%Y%m%d_%H%M")
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

        # self.warning_box(log_file)                                                                             # Display log in Blender 'TEXT_EDITOR'

    def warning_box(self, logfile):
        """ Output to text editor window """
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.text.open(filepath = logfile)

def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    register()