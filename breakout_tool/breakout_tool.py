# ##### BEGIN GPL LICENSE BLOCK #####
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
# ##### END GPL LICENSE BLOCK #####

# ##### BEGIN SCRIPT COMMENTS #####
#  Main Tool: "Breakout Tool"
#  Parent: ""
#  Name: "Breakout Tool",
#  Author: "Jordan Goddard",
#  Company: "Tangent Animation"
#  Blender: (2, 74, 0),
#  Description: "Creates new blend files with published links to assets and prepares shots for animation"
#  <pep8 compliant>
# ##### END SCRIPT COMMENTS #####

"""
Import the necesary libraries for the application to call
"""
import bpy
import struct
import logging 
import re
import time

class BreakOut(object):
    """
    Main breakout class, handling the breakout process
    """
    def __init__(self):
        """
        This will run when this class is called and will carry any passed objects
        """
        self.scene_name = None
        self.seqshot = None
        self.filepath = None
        self.context = bpy.context
        self.data = bpy.data
        self.ops = bpy.ops
        self.random_suffix = "2Chia19_"
        self.scene = bpy.data.scenes
        self.path = bpy.path
        self.old_start_frame = None
        self.old_end_frame = None
        self.file_name = None
        self.new_scene = None
        self.old_filepath = []
        self.run_it()
        self.offset = None

    def run_it(self):
        """
        Retrieve 'filepath' and 'scene' name from external temp file
        """
        try:
            file_read = open('C:\\Temp\\pass_temp.txt','r').readlines()
        except:
            print("\n\nFailure\n\n")
        else:
            line_one = file_read[0]
            match = re.match(r'(\S+\.\S+)', line_one)
            self.scene_name = match.group(1)
            line_two =  file_read[1]
            match_again = re.match("(\S+)", line_two)
            self.file = match_again.group(1)
            self.seqshot = self.scene_name

    def open_checking_file(self):
        """
        Open the '.BLEND' file for processing and temporarily removes non-essential scenes
        """
        current_file_path = self.file
        selection_name = self.scene_name
        bpy.ops.wm.open_mainfile(filepath=current_file_path)
        self.seqshot = self.scene_name
        for scene in bpy.data.scenes:
            if scene.name != selection_name:
                bpy.data.screens['Default'].scene = bpy.data.scenes[scene.name]
                bpy.ops.scene.delete()
            elif scene.name == selection_name:
                pass
            else:
                print("Something went wrong!")

    def execute(self):
        """
        This will execute the deffinitions in this class
        """
        self.clean_scene()
        self.append_original_shot_file(self.filepath, self.seqshot)
        print("APPEND DONE")
        self.get_offset()
        self.transfer_asset_data(self.scene[0], self.scene[1])
        print("TRANSFER DONE")
        self.set_new_scene_start_end()
        print("SET NEW SCENE DONE")
        self.reset_audio_offsets()
        print("SET AUDIO DONE")
        self.reset_animation_offsets()
        print("SET KEYFRAMES DONE")
        self.delete_original_scene()
        print("DELETE DONE")
        self.remove_new_asset_suffix()
        self.link_LOW()
        self.playblast_manager()
        print("RENAME DONE")

    def get_offset(self):
        """
        Gather current offset data from master file
        """
        self.offset = (self.scene[0].frame_start - 1)

    def clean_scene(self):
        """
        Empty the current scene of all its assets
        """
        selection_pattern = bpy.ops.object.select_pattern
        for obj in self.scene[0].objects:
            selection_pattern(pattern=obj.name)
            bpy.ops.object.delete()
        self.center_cursor()

    def append_original_shot_file(self, filepath, seq_shot):
        """
        Append the shot at Scene.random_suffix, then use this to gather information on the
        """
        import time
        self.filepath = self.file
        print(self.filepath)
        try:
            with bpy.data.libraries.load(self.filepath) as (data_from, data_to):
                 data_to.scenes = [seq_shot]
        except: 
            time.sleep(10)
            quit("Cannot open file")
        bpy.context.screen.scene = self.scene[0]
        self.scene[1].name = self.new_name(self.scene[0].name)
        self.new_scene = self.scene[1]
        bpy.ops.file.make_paths_absolute()
        return {'FINISHED'}

    def transfer_asset_data(self, scene_from, scene_to):
        """
        Transfer asset data to new scene
        """
        self.new_scene = scene_to
        scene = scene_from
        self.new_scene.frame_start = scene.frame_start
        self.new_scene.frame_end = scene.frame_end
        self.new_scene.sequence_editor_create()
        try:
            for audio in scene.sequence_editor.sequences_all:
                self.new_scene.sequence_editor.sequences.new_sound(audio.name, audio.filepath, audio.channel, audio.frame_start)
        except:
            print("ERROR: No Audio")
        object_list = []
        all_relationship = []
        new_object_list = []
        for obj in scene.objects:
            if self.useful_check(obj):
                obj.name = obj.name + "X"
                object_list.append(obj)
        for obj in object_list: 
            object_relationship = self.check_relationship(obj.name, object_list)
            all_relationship.append(object_relationship)
        object_num = 0
        for obj in object_list:
            new_object_list.append(None)
            object_num = 1 + object_num
        for obj in object_list:
            if obj.name.startswith('grp'):
                search_proxy = re.search("proxy", obj.name)
                if not search_proxy:
                    object_index = object_list.index(obj) 
                    proxy_index = None
                    try:
                        obj.dupli_group.name
                    except: 
                        print("Error in group")
                    else:
                        group_name = obj.dupli_group.name
                        group = bpy.data.groups[group_name]
                        publish_link = self._publish_path(group.library.filepath)
                        proxy_name = "%s_proxy" %group_name
                        proxy_name2 = "%s_proxy" %obj.name
                        proxy = False
                        for obj in object_list:
                            search = re.search(proxy_name, obj.name)
                            search2 = re.search(proxy_name2, obj.name)
                            if search or search2: 
                                print("%s has proxy" %group_name)
                                proxy_index = object_list.index(obj)
                                proxy = True
                                proxy_name = obj.name
                                break
                        new_group_name = self.link_in_groups(publish_link, obj.name)
                        new_group_name = self.create_empty(new_group_name, publish_link, self.new_scene.name)
                        new_object_list[object_index] = new_group_name
                        if proxy: 
                            print("Create Proxy")
                            print(new_group_name)
                            new_proxy_name = self.create_armature_proxies(new_group_name)
                            new_object_list[proxy_index] = new_proxy_name
                            self.copy_animation_data(proxy_name, new_proxy_name)
            else:
                object_index = object_list.index(obj)
                new_object_list[object_index] = self.new_name(obj.name)
                self.copy_item(obj.name)
                self.copy_animation_data(obj.name)
        self.transfer_constraints(object_list, new_object_list, all_relationship, object_num)
        self.relink_dof()
        return {'FINISHED'}

    def relink_dof(self):
        """
        Resets camera focus constraints
        """
        focus = None
        for obj in self.new_scene.objects: 
            if obj.name.startswith('fcs'):
                focus = obj
        for camera in bpy.data.cameras:
            camera.dof_object = focus

    def useful_check(self, obj):
        """
        Check if item needs to be passed to the new scene
        """
        try:
            if obj.users_group.name.startswith("grp.stuff"):
                return True
        except: 
            print("no users group")
        if obj.name.startswith('lkt') or obj.name.startswith('cam') or obj.name.startswith('fcs'):
            return True
        elif obj.name.startswith('grp'):
            return True
        else:
            return False

    def check_relationship(self, obj_name, obj_list):
        """
        Generate a list of all relationships that existed in the scene
        """
        parent_data=[None, None]
        constraint_data=[None, None, None]
        all_constraints = []
        child = self.scene[0].objects[obj_name]
        try:
            for obj in obj_list: 
                if child.parent.name == obj.name:
                    parent[0] = obj_list.index(obj)
                    parent[1] = (obj.parent_type)
        except AttributeError:
            print("no parent")
        try:
            for constraint in obj.constraints:
                constraint_data[0] = constraint.type
                for obj in obj_list:
                    if constraint.target.name.startswith('rig'):
                        import re 
                        match = re.match(r'rig\.(\w+)', constraint.target.name)
                        search = re.search(match.group(1), obj.name)
                        if search:
                            constraint_data[1] = obj_list.index(obj)
                            constraint_data[2] = constraint.subtarget
                    else:
                        constraint_data[1] = obj_list.index(obj)
                        constraint_data[2] = constraint.subtarget
                all_constraints.append(constraint_data)
        except AttributeError: 
            print("no constraint")
        if not all_constraints:
            all_constraints.append(None)
        all_relationship = parent_data + all_constraints
        print(all_relationship)
        return all_relationship

    def transfer_constraints(self, object_list, new_object_list, all_relationship, index):
        """
        Transfer constraints (and parenting) from old scenes to new scenes (Relies heavily on an address/index based procedural code)
        """
        print(new_object_list)
        i = 0
        while (i < index):
            if new_object_list[i]:
                obj = self.new_scene.objects[new_object_list[i]]
                if all_relationship[i][0]:
                    new_index = all_relationship[i][0]
                    obj.parent = self.new_scene.objects[new_object_list[new_index]]
                    obj.parent_type = all_relationship[i][1]
                constraint_num = 2
                for copy_from_constraint in object_list[i].constraints:
                    constraint_type = copy_from_constraint.type
                    properties = [prop.identifier for prop in copy_from_constraint.bl_rna.properties if not prop.is_readonly]
                    new_object = self.new_scene.objects[new_object_list[i]]
                    copy_to_constraints = new_object.constraints.new(constraint_type)
                    for prop in properties: 
                        print(prop)
                        setattr(copy_to_constraints, prop, getattr(copy_from_constraint, prop))
                    if all_relationship[i][constraint_num]:
                        copy_to_constraints.type = all_relationship[i][constraint_num][0]
                        new_index = all_relationship[i][constraint_num][1]
                        import re
                        new_object_name = new_object_list[new_index]
                        search = re.search('proxy', new_object_name)
                        if search:
                            copy_to_constraints.target = self.new_scene.objects[new_object_name].proxy
                            copy_to_constraints.subtarget = all_relationship[i][constraint_num][2]
                        else:
                            copy_to_constraints.target = self.new_scene.objects[new_object_name]
                            try:
                                copy_to_constraints.subtarget = all_relationship[i][constraint_num][2]
                            except:
                                print("No subtarget")
                    constraint_num = constraint_num + 1
            i = i + 1

    def create_armature_proxies(self, new_group_name):
        """
        This will take the file path for the proxies, that was gathered from the original appended file, and create a new proxy on each object
        """
        import re
        selection_pattern = bpy.ops.object.select_pattern
        scene = self.new_scene
        proxy_name = None
        rig_name = None
        obj = scene.objects[new_group_name]
        self.new_scene.objects.active = self.new_scene.objects[new_group_name]
        match = re.match(r'grp\.(\S+)', new_group_name)
        if match: 
            rig_name = "rig.%s" %match.group(1)
        try:
            bpy.ops.object.proxy_make(object = rig_name)
        except:
            bpy.ops.object.proxy_make()
            print("%s's proxy might be incorrect", obj.name)
        proxy_name = "%s_proxy" %obj.name
        return proxy_name

    def copy_item(self, object_name, copy_to_name = None):
        """
        Copy object data to new version of object in new scene
        """
        if copy_to_name is None:
            copy_to_name = self.new_name(object_name)
        copy = self.scene[0].objects[object_name].copy()
        obj = bpy.data.objects.new(self.new_name(object_name), copy.data)
        bpy.context.screen.scene = self.new_scene 
        scene = bpy.context.scene
        scene.objects.link(obj) 

    def copy_animation_data(self, object_name, copy_to_name = None):
        """"
        Copy animation_data of the selected objects
        """
        if copy_to_name is None:
            copy_to_name = self.new_name(object_name)
        try:
            copy_from_animation = self.scene[0].objects[object_name].animation_data
            properties = [prop.identifier for prop in copy_from_animation.bl_rna.properties if not prop.is_readonly]
            new_object = self.new_scene.objects[copy_to_name]
            new_object.animation_data_create()
            copy_to_animation = new_object.animation_data
            for prop in properties: 
                print(prop)
                setattr(copy_to_animation, prop, getattr(copy_from_animation, prop))
        except:
            print("No animation data")

    def _publish_path(self, path):
        """"
        Correct the path of the blender file link so that it points to the publish version 
        """
        import re
        import os
        import fnmatch
        m = re.match(r'(T:\\Projects\\0043_Ozzy\\Assets\\\w+\\\w+\\publish\\)versions\\\S+', path)
        if m: 
            self.old_filepath.append(path)
            publish_dir = m.group(1)
            for item in os.listdir(publish_dir):
                if fnmatch.fnmatch(item, '*.blend'):
                    path = publish_dir + item
                    break # right now it's assuming that the first file you see is the good version (in most case should be true)
        return path

    def link_in_groups(self, path, obj_name):
        """"
        Given the link  of the blender file, link in the group in the blender file and select LOW res version if available
        """
        self.center_cursor()
        group_name = None
        with bpy.data.libraries.load(path, link = True) as (data_from, data_to):
            for group in data_from.groups:
                if group.startswith('grp.') and not group.endswith('LOW') and not group.endswith('MID'): #and similarity > 0.7:
                    group_name = group
                    break
            data_to.groups = [group_name]
        if not group_name:
            print("ERROR: %s in the published version is too different from the current version" %obj_name)
        return group_name

    def compare_string(self, item1, item2):
        """
        Compare two strings and output similarities
        """
        from difflib import SequenceMatcher
        return SequenceMatcher(None, item1, item2).ratio()

    def create_empty(self, group_name, path, scene_name = None):
        """
        Add a null object to duplicate the group
        """
        if scene_name:
             bpy.context.screen.scene = self.scene[scene_name]
        scene = bpy.context.scene
        null = bpy.data.objects.new(group_name, None)
        null.location = (0,0,0)
        null.empty_draw_type = 'PLAIN_AXES'
        null.dupli_type = 'GROUP'
        for group in bpy.data.groups:
            if group_name == group.name and group.library.filepath == path: 
                null.dupli_group = group
                break
        group_name = null.name
        scene.objects.link(null)
        scene.update()
        return group_name

    def set_new_scene_start_end(self):
        """
        Reset newly created scene 'start(1)'/'end' frames relative to original scene 'start'/'end' frames
        """
        shot_original_frame_start = self.scene[0].frame_start
        shot_original_frame_end = self.scene[0].frame_end
        self.scene[1].frame_start = shot_original_frame_start - self.offset
        self.scene[1].frame_end = shot_original_frame_end - self.offset

    def reset_audio_offsets(self):
        """
        Moves audio tracks back relative to their original positions
        'Name' has to be changed last since that effectively renames the object
        """
        self.shot_original_scene = self.scene[0]
        self.shot_new_scene = self.scene[1]
        shot_original_frame_start=self.shot_original_scene.frame_start
        for obj in self.new_scene.sequence_editor.sequences_all:
            shot_audio_file_path=obj.filepath
            shot_audio_file_name=self.path.basename(shot_audio_file_path)
            shot_audio_file_current_start_frame=obj.frame_start
            shot_audio_file_new_start_frame = shot_audio_file_current_start_frame - self.offset
            obj.frame_start = shot_audio_file_new_start_frame
            obj.name = shot_audio_file_name

    def reset_animation_offsets(self):
        """
        Move keyframes and handles back relative to their original positions
        'Left Handle' should be moved last
        """
        self.shot_original_scene = self.scene[0]
        self.shot_new_scene = self.scene[1]
        for obj in self.new_scene.objects:
            try:
                action = obj.animation_data.action                                            # Object contains animation data?
                for fcurve in action.fcurves:                                                 # Keyed actions
                    fcurve_data = fcurve.data_path                                            # RNA Path to property affected by F-Curve
                    fcurve_index = fcurve.array_index                                         # Index to the specific property affected by F-Curve if applicable
                    fcurve_var = None
                    for keyframe_position in fcurve.keyframe_points:
                        keyframe_position.co.x = keyframe_position.co.x - self.offset
                        keyframe_position.handle_right.x = keyframe_position.handle_right.x - self.offset
                        keyframe_position.handle_left.x = keyframe_position.handle_left.x - self.offset
            except: 
                print("Object: %s has no Action" %(obj.name))                                 # No animation data

    def _set_display_options(self): 
        """
        Set the camera settings to Render only, AO, and DOF.
        This is based on the current pannel that is open and should be taken care of by the asset manager
        """
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                area.spaces[0].show_only_render = True
                area.spaces[0].fx_settings.use_dof = True
                area.spaces[0].fx_settings.use_ssao = True

    def _set_output_options(self):
        """
        Set the output settings for the playblast
        """
        scene = bpy.data.scenes
        for current_scene in bpy.data.scenes:
            scene[current_scene.name].render.use_stamp = True
            scene[current_scene.name].render.stamp_font_size = 17
            scene[current_scene.name].render.use_stamp_time = False
            scene[current_scene.name].render.use_stamp_date = False
            scene[current_scene.name].render.use_stamp_render_time = False
            scene[current_scene.name].render.use_stamp_frame = True
            scene[current_scene.name].render.use_stamp_scene = True
            scene[current_scene.name].render.use_stamp_note = False
            scene[current_scene.name].render.use_stamp_camera = False
            scene[current_scene.name].render.use_stamp_lens = False
            scene[current_scene.name].render.use_stamp_filename = False
            scene[current_scene.name].render.use_stamp_marker = False
            scene[current_scene.name].render.use_stamp_sequencer_strip = False

    def delete_original_scene(self):
        """
        Delete original scene leaving the new scene alone
        Delete library path (may be in separate function)
        """
        scene_name = bpy.data.scenes[0].name
        self.purge_orphan()
        bpy.context.window.screen.scene = bpy.data.scenes[0]
        bpy.ops.scene.delete()
        bpy.data.scenes[0].name = scene_name
        self.remove_old_filepath()
        self.purge_orphan()

    def remove_new_asset_suffix(self):
        """
        This will remove the suffix '.new' on any objects in the scene that end with it. (some may not end with it....!)
        """
        temp_asset_name = None
        for obj in bpy.data.scenes[0].objects:
            temp_asset_name = obj.name
            if obj.name.endswith("X.%s" %self.random_suffix):
                obj.name = temp_asset_name[:-10]

    def link_LOW(self):
        """
        Link LOW if available 
        """
        for obj in bpy.context.scene.objects:
            try:
                obj.dupli_group.name
            except: 
                pass
            else:
                group_name = obj.dupli_group.name
                group = obj.dupli_group    
                path = group.library.filepath
                low_name = obj.name + "_LOW"
                with bpy.data.libraries.load(path, link = True) as (data_from, data_to):
                    for group in data_from.groups:
                        if group == low_name:
                            group_name = group
                            found = True
                            data_to.groups = [group_name]
                            break
                if found:   # Add a null object to duplicate the group (link the group back in the scene) *from BreakOut Tool
                    bpy.context.scene.objects.unlink(obj)
                    scene = bpy.context.scene
                    null = bpy.data.objects.new(group_name, None)
                    null.location = (0,0,0)
                    null.empty_draw_type = 'PLAIN_AXES'
                    null.dupli_type = 'GROUP'
                    null.dupli_group = bpy.data.groups[group_name]
                    group_name = null.name        
                    scene.objects.link(null)

    def remove_old_filepath(self):
        """
        Remove old filepath that's not point to publish
        """
        import re
        for library in bpy.data.libraries:
            if library.filepath in self.old_filepath:
                library.filepath = "//..\\"
            search = re.search("versions", library.filepath)
            if search: 
                library.filepath = "//..\\"

    def new_name(self, obj_name):
        """"
        Generate a random suffix to the object
        """
        obj_name = "%s.%s" % (obj_name, self.random_suffix)
        return obj_name

    def center_cursor(self):
        """
        This will ensure that the cursor's translation is set to (0, 0, 0)
        """
        self.context.scene.cursor_location.xyz = (0,0,0)

    def create_new_scene(self):
        """ 
        this will create a new scene
        """
        self.ops.scene.new(type="NEW")

    def lock_items(self):
        """
        Lock object location, rotation, scale
        Objects: cam, fcs, lkt, nul, light
        """
        objects = bpy.data.objects
        for current_object in objects:
            item_prefix = ["cam", "fcs", "grp", "lkt", "nul", "render", "world"]
            if current_object.name.startswith(tuple(item_prefix)):
                    print("%s has been locked" % current_object.name)
                    objects[current_object.name].lock_location = [True, True, True]
                    objects[current_object.name].lock_rotation = [True, True, True]
                    objects[current_object.name].lock_scale = [True, True, True]    
            else:
                print("%s is an object that will not be locked" % current_object.name)
            if current_object.name.startswith("cam") or current_object.name.startswith("fcs") or current_object.name.startswith("lkt"):
                current_object.hide = True
                current_object.hide_select = True