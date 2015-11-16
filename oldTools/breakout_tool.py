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
        self.log = []
        self.group_objects = []
        self.gather_group_data()
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
            self.log.append("run_it function has failed")
            print("\n\nFailureRunIt\n\n")
        else:
            line_one = file_read[0]
            match = re.match(r'(\S+\.\S+)', line_one)
            self.scene_name = match.group(1)
            line_two =  file_read[1]
            match_again = re.match("(\S+)", line_two)
            self.file = match_again.group(1)
            self.seqshot = self.scene_name

    def gather_group_data(self):
        try:
            file_read = open('C:\\Temp\\group_data_transfer.txt','r')
        except:
            self.log.append("Failure in gathering grp.stuff data from pass file")
        else:
            for line in file_read:
                self.group_objects.append(line[:-1])
        finally:
            file_read.close()

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

        for obj in bpy.data.scenes[self.scene_name].objects:
            for group in obj.users_groups:
                if group.name == "grp.stuff":
                    self.stuff_grp.append(obj.name)

    def execute(self):
        """
        This will execute the deffinitions in this class
        """
        self.clean_scene()
        self.append_original_shot_file(self.filepath, self.seqshot)
        #print("APPEND DONE")
        self.get_offset()
        self.transfer_asset_data(self.scene[0], self.scene[1])
        #print("TRANSFER DONE")
        self.set_new_scene_start_end()
        #print("SET NEW SCENE DONE")
        self.reset_audio_offsets()
        #print("SET AUDIO DONE")
        self.reset_animation_offsets()
        #print("SET KEYFRAMES DONE")
        self.delete_original_scene()
        #print("DELETE DONE")
        self.remove_new_asset_suffix()
        #self.link_LOW()
        self.playblast_manager()
        # self.relink_grp_stuff()
        #print("RENAME DONE")
        self._log_()

    def playblast_manager(self):
        pass

    def get_offset(self):
        """
        Gather current offset data from master file
        """
        self.offset = (bpy.data.scenes[self.scene_name].frame_start - 1)

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
        Append the shot at Scene.random_suffix, then use this to gather information
        """
        scene_obj = []
        import time
        self.filepath = self.file
        print(self.filepath)
        try:
            with bpy.data.libraries.load(self.filepath) as (data_from, data_to):
                 data_to.scenes = [seq_shot]
        except: 
            time.sleep(10)
            self.log.append("Cannot append original file")
            quit("Cannot open file")
        bpy.context.screen.scene = self.scene[0]
        self.scene[1].name = self.new_name(self.scene[0].name)
        self.new_scene = self.scene[1]
        bpy.ops.file.make_paths_absolute()
        
        bpy.ops.group.create(name="grp.stuff")                              # Create grp.stuff Group
        
        current_appended_scene_name = self.scene[0].name                    # Set scene name
        for obj in bpy.data.scenes[current_appended_scene_name].objects:    # Compair objects to group from master
            if obj.name in self.group_objects:
                bpy.context.scene.objects[bpy.context.scene.objects.active.name].select=False
                #bpy.context.scene.objects.active = obj
                #if obj not in bpy.data.groups["grp.stuff"].objects:
                #    print("Adding it")
                try:
                    bpy.data.groups["grp.stuff"].objects.link(obj)
                except:
                    self.log.append("Cannot add %s to grp.stuff, because it is already in grp.stuff."%obj.name)
                    print("OOPS")
                '''
                for grgobj in bpy.data.groups["grp.stuff"].objects:
                    print("%s:%s"%(grgobj.name, obj.name))
                    if obj.name == grgobj.name:
                        print("pass: %s"%obj.name)
                    else:
                        print("copy: %s"%obj.name)
                        bpy.data.groups["grp.stuff"].objects.link(obj)
                '''
                #bpy.ops.object.group_link(group="grp.stuff")
            else:
                print("\n%s is not a match"%obj.name)
       
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
        object_list = [] #-------------------------------------------------------------------Stores ObjectData
        all_relationship = [] 
        new_object_list = [] #---------------------------------------------------------------Stores ObjectName only 
        for obj in scene.objects:
            if self.useful_check(obj):
                obj.name = obj.name + "X" #--------------------------------------------------This is to make sure that all the constraints will be transfered correctly
                object_list.append(obj)
        for obj in object_list: 
            object_relationship = self.check_relationship(obj.name, object_list)
            all_relationship.append(object_relationship)
        print(self.parent_offset)
        object_num = 0
        for obj in object_list:
            new_object_list.append(None)
            object_num = 1 + object_num
        for obj in object_list:
            if obj.name.startswith('grp'):
                is_proxy = re.search("proxy", obj.name)
                if not is_proxy:  
                    object_index = object_list.index(obj) 
                    proxy_index = None
                    try:
                        obj.dupli_group.name
                    except: 
                        pass #----------------------------------------------------------------No dupli group
                        #print("Error in group")
                    else:
                        group_name = obj.dupli_group.name
                        group = bpy.data.groups[group_name]
                        publish_link = self._publish_path(group.library.filepath)
                        shorten_name = re.match(r'grp.(\w+)', group_name)
                        proxy_name = "%s_proxy" %group_name #grp.ozzy_proxy
                        #proxy_name2 = "%s_proxy" %obj.name  #grp.ozzy.001_proxy
                        proxy = False
                        for obj in object_list:
                            search = re.search(shorten_name.group(1), obj.name) #-------------it has the name in it
                            search2 = re.search("proxy", obj.name) #--------------------------it has the word proxy in it 
                            if search and search2: 
                                print("LOG: %s has proxy" %group_name)
                                proxy_index = object_list.index(obj)
                                proxy = True
                                proxy_name = obj.name
                                break
                        new_group_name = self.link_in_groups(publish_link, group_name)
                        print("LOG: %s %s" %(group_name, publish_link))
                        new_group_name = self.create_empty(new_group_name, publish_link, self.new_scene.name)
                        new_object_list[object_index] = new_group_name
                        if proxy: 
                            print("LOG: Create Proxy for %s" %new_group_name)
                            new_proxy_name = self.create_armature_proxies(new_group_name)
                            new_object_list[proxy_index] = new_proxy_name
                            self.copy_animation_data(proxy_name, copy_to_name = new_proxy_name)
            else:
                object_index = object_list.index(obj)
                new_object_list[object_index] = self.new_name(obj.name)
                if all_relationship[object_index][0]:
                    self.copy_item(obj.name, True)
                else:
                    self.copy_item(obj.name)
        self.transfer_constraints(object_list, new_object_list, all_relationship, len(object_list))
        self.relink_dof(object_list, new_object_list)
        self.attach_bone_constraints(object_list, new_object_list)
        return {'FINISHED'}

    def relink_dof(self, object_list, new_object_list):
        """
        Resets camera focus constraints
        """
        for obj in self.scene[0].objects: 
            if obj.name.startswith('cam'):
                focus = obj.data.dof_object
                new_cam = self.scene[1].objects[new_object_list[object_list.index(obj)]]
                new_cam.data.dof_object = focus

    def useful_check(self, obj):
        """
        Check if item needs to be passed to the new scene
        """
        try:
            for group in obj.users_group:
                if group.name.startswith("grp.stuff"):
                    return True
        except: 
            pass #-----------------------------------------------------------------------------------No users group
            #print("no users group")
        if obj.name.startswith('lkt') or obj.name.startswith('cam') or obj.name.startswith('fcs'):
            return True
        elif obj.name.startswith('grp'):
            return True
        else:
            print("LOG: %s is not useful", obj.name)
            return False

    def check_relationship(self, obj_name, obj_list):
        """
        Generate a list of all relationships that existed in the scene
        """
        parent_data=[None, None]
        all_constraints = []
        child = self.scene[0].objects[obj_name]
        try:
            child.parent.name
        except AttributeError:
            pass #--------------------------------------------------------------------------------No Parent
        else:
            for obj in obj_list: 
                if child.parent.name == obj.name:
                    list = []
                    parent_data[0] = obj_list.index(obj) #-----------------------------------------Append Index of the parent object 
                    parent_data[1] = obj.parent_type#----------------------------------------------Parent Type
                    
                    #Create a null object to track the global location of the child
                    break
        try:
            child.constraints[0]
        except IndexError:
            pass #--------------------------------------------------------------------------------No Constraint
            #print("no constraint")
        else:
            for constraint in child.constraints:
                constraint_data = [None, None]
                try:
                    constraint.target.name
                except AttributeError:
                    constraint_data[0] = None
                    constraint_data[1] = None
                else:
                    if constraint.target.name.startswith('rig'): 
                        for obj in obj_list:
                            import re 
                            match = re.match(r'rig\.(\w+)', constraint.target.name)
                            search = re.search(match.group(1), obj.name)
                            search2 = re.search('proxy', obj.name)
                            if search and search2:
                                constraint_data[0] = obj_list.index(obj)
                                constraint_data[1] = constraint.subtarget
                    else:
                        try:
                            constraint_data[0] = obj_list.index(constraint.target)
                        except: 
                            print("CHECK: Target object: %s is not in grp.stuff. Constraint will not be copied" %constraint.target)
                            constraint_data[0] = None
                        else:
                            try:
                                constraint_data[1] = constraint.subtarget
                            except: 
                                pass #-------------------------------------------------------------No SubTarget
                                #print("no subtarget")
                all_constraints.append(constraint_data)
        if not all_constraints:
            all_constraints.append(None)
        all_relationship = parent_data + all_constraints #[parent type, parent object, constraints]
        print(all_relationship)
        return all_relationship

    def transfer_constraints(self, object_list, new_object_list, all_relationship, index):
        """
        Transfer constraints (and parenting) from old scenes to new scenes (Relies heavily on an address/index based procedural code)
        """
        #print(new_object_list)
        i = 0
        #print(index)
        while (i < index):
            if new_object_list[i]:
                obj = self.new_scene.objects[new_object_list[i]]
                print(obj.name)
                if all_relationship[i][0]:
                    new_index = all_relationship[i][0]
                    for ob in self.new_scene.objects: 
                        ob.select = False
                    obj.select = True
                    bpy.context.screen.scene = self.new_scene
                    self.new_scene.objects.active = self.new_scene.objects[new_object_list[new_index]]
                    bpy.ops.object.parent_set(type = all_relationship[i][1], keep_transform = True) #--------------Set Parent, Keep Transformation
                    #obj.parent = self.new_scene.objects[new_object_list[new_index]]
                    #obj.parent_type = all_relationship[i][1]
                constraint_num = 2
                for copy_from_constraint in object_list[i].constraints:
                    constraint_type = copy_from_constraint.type
                    properties = [prop.identifier for prop in copy_from_constraint.bl_rna.properties if not prop.is_readonly]
                    new_object = self.new_scene.objects[new_object_list[i]]
                    copy_to_constraints = new_object.constraints.new(constraint_type)
                    for prop in properties: 
                        #print(prop)
                        setattr(copy_to_constraints, prop, getattr(copy_from_constraint, prop))
                    print(constraint_num)
                    if all_relationship[i][constraint_num]:
                        #copy_to_constraints.type = all_relationship[i][constraint_num][0] #String
                        new_index = all_relationship[i][constraint_num][0] #Int
                        if new_index is None: 
                            copy_to_constraints.target = None
                        else:
                            import re
                            new_object_name = new_object_list[new_index] #Corresponding New Object
                            search = re.search('proxy', new_object_name)
                            if search:
                                copy_to_constraints.target = self.new_scene.objects[new_object_name] #---------Connect to the proxy
                                try:
                                    copy_to_constraints.subtarget = all_relationship[i][constraint_num][1] #---------Add bone subtarget
                                except: 
                                    print("ERROR: no bone as subtarget")
                            else:
                                copy_to_constraints.target = self.new_scene.objects[new_object_name] #---------------Connect to the object
                                try:
                                    copy_to_constraints.subtarget = all_relationship[i][constraint_num][1] #---------If subtarget exist, copy subtarget
                                except:
                                    pass #---------------------------------------------------------------------------No subtarget
                                    print("LOG: %s has no subtarget" %new_object_name)
                    constraint_num = constraint_num + 1
            i = i + 1

    def attach_bone_constraints(self, obj_list, new_object_list):
        """
        Reattach all the bone constriants in the new scene
        """
        for obj in self.scene[0].objects: 
            import re
            is_proxy = re.search('proxy', obj.name)
            if is_proxy and obj.type != 'EMPTY':
                for bone in obj.pose.bones: 
                    if bone.name.startswith('ctl.') and bone.constraints: #----------------------------------------------------------------------------------------Bone has constraint
                        for con in bone.constraints:
                            new_proxy = self.scene[1].objects[new_object_list[obj_list.index(obj)]]
                            try:
                                con.target
                            except: 
                                try:
                                    other_bone = new_proxy.pose.bones[bone.name]
                                except: 
                                    print("ERROR: OBJ: %s Bone: %s has different name in the new object" %(obj.name, bone.name))
                                else:
                                    properties = [prop.identifier for prop in con.bl_rna.properties if not prop.is_readonly]
                                    new_constraint = other_bone.constraints.new(type = con.type)
                                    for prop in properties: 
                                        setattr(new_constraint, prop, getattr(con, prop))
                                    try:
                                        if con.target:
                                            new_constraint.target = self.scene[1].objects[new_object_list[obj_list.index(con.target)]]
                                    except:
                                        print("LOG: OBJ: %s Bone: %s Constraint: %s has no target" %(obj.name, bone.name, con.name))
                            else:
                                if con.target != obj and con.target in obj_list:
                                    try:
                                        other_bone = new_proxy.pose.bones[bone.name]
                                    except: 
                                        print("ERROR: OBJ: %s Bone: %s has different name in the new object" %(obj.name, bone.name))
                                    else:
                                        properties = [prop.identifier for prop in con.bl_rna.properties if not prop.is_readonly]
                                        new_constraint = other_bone.constraints.new(type = con.type)
                                        for prop in properties: 
                                            setattr(new_constraint, prop, getattr(con, prop))
                                        try:
                                            if con.target:
                                                new_constraint.target = self.scene[1].objects[new_object_list[obj_list.index(con.target)]]
                                        except:
                                            print("LOG: OBJ: %s Bone: %s Constraint: %s has no target" %(obj.name, bone.name, con.name))
                                                                                                
    def create_armature_proxies(self, new_group_name):
        """
        This will take the file path for the proxies, that was gathered from the original appended file, and create a new proxy on each object
        """
        import re
        proxy_name = None #-----------------------------------------------------------------name of the proxy
        rig_name = None #-------------------------------------------------------------------name of the rig
        dupli_name = None #-----------------------------------------------------------------name of the actual group
        obj = self.new_scene.objects[new_group_name]
        self.new_scene.objects.active = obj
        try:
            dupli_name = obj.dupli_group.name
        except: 
            pass
        match = re.match(r'grp\.(\S+)', dupli_name)
        if match: 
            rig_name = "rig.%s" %match.group(1)
        try:
            bpy.ops.object.proxy_make(object = rig_name)
        except:
            bpy.ops.object.proxy_make()
            print("CHECK: %s's proxy might be incorrect", obj.name)
        proxy_name = "%s_proxy" %obj.name
        return proxy_name

    def copy_item(self, object_name, offset = False, copy_to_name = None):
        """
        Copy object data to new version of object in new scene
        """
        if copy_to_name is None:
            copy_to_name = self.new_name(object_name)
        copy = self.scene[0].objects[object_name].copy()
        #copy.name = self.new_name(object_name)
        obj = bpy.data.objects.new(self.new_name(object_name), copy.data)
        
        obj.location = copy.location
        obj.rotation_euler = copy.rotation_euler
        obj.scale = copy.scale
        
        offset_location = ((0,0,0))
        offset_rotation = ((0,0,0))
        offset_scale = ((0,0,0))
        
        if offset:
            child = self.scene[0].objects[object_name]
            slave_temp = bpy.data.objects.new("slave_temp", None) 
            slave_temp.empty_draw_type = 'PLAIN_AXES'
            slave_temp.location = (0,0,0)
            slave_temp.parent = child.parent
            new_constraint = slave_temp.constraints.new(type ='COPY_LOCATION')
            new_constraint.target = child
            new_constraint = slave_temp.constraints.new(type ='COPY_ROTATION')
            new_constraint.target = child
            new_constraint = slave_temp.constraints.new(type ='COPY_SCALE')
            new_constraint.target = child
            self.scene[0].objects.link(slave_temp)
            self.scene[0].update         
            bpy.context.screen.scene = self.scene[0]
            for ob in self.scene[0].objects: 
                ob.select = False
            slave_temp.select = True
            self.scene[0].objects.active = slave_temp
            bpy.ops.object.parent_clear(type = 'CLEAR_KEEP_TRANSFORM')
            obj.location = slave_temp.location
            obj.rotation_euler = slave_temp.rotation_euler  
            obj.scale = slave_temp.scale
            offset_location = slave_temp.location - copy.location
            offset_rotation = ((slave_temp.rotation_euler[0]-copy.rotation_euler[0]),(slave_temp.rotation_euler[1]-copy.rotation_euler[1]),(slave_temp.rotation_euler[2]-copy.rotation_euler[2]))
            offset_scale = slave_temp.scale - copy.scale
            # print(offset_location)
            # print(offset_rotation)        
            self.scene[0].objects.unlink(slave_temp)
            bpy.data.objects.remove(slave_temp)
            
        # print(obj.name)
        # print(obj.location)
        # print(obj.rotation_euler)
        self.new_scene.objects.link(obj)    
        if self.copy_animation_data(object_name, self.copy_action_data(object_name)): #-------------------------------------------Object has animation data
            self.offset_animation(obj, offset_location, offset_rotation, offset_scale)
           
    def offset_animation(self, obj, offset_location, offset_rotation, offset_scale):
        for fcurve in obj.animation_data.action.fcurves:
            i = 0 
            while(i < 3):
                if fcurve.data_path == 'location' and fcurve.array_index == i:
                    for key in fcurve.keyframe_points: 
                        key.co[1] = key.co[1] + offset_location[i]
                        key.handle_left[1] =  key.handle_left[1] + offset_location[i]
                        key.handle_right[1] =  key.handle_right[1] + offset_location[i]
                i = i + 1
            i = 0 
            while(i < 3):
                if fcurve.data_path == 'rotation_euler' and fcurve.array_index == i:
                    for key in fcurve.keyframe_points: 
                        key.co[1] = key.co[1] + offset_rotation[i]
                        key.handle_left[1] =  key.handle_left[1] + offset_rotation[i]
                        key.handle_right[1] =  key.handle_right[1] + offset_rotation[i]
                i = i + 1
            i = 0 
            while(i < 3):
                if fcurve.data_path == 'scale' and fcurve.array_index == i:
                    for key in fcurve.keyframe_points: 
                        key.co[1] = key.co[1] + offset_scale[i]
                        key.handle_left[1] =  key.handle_left[1] + offset_scale[i]
                        key.handle_right[1] =  key.handle_right[1] + offset_scale[i]
                i = i + 1
    
    def copy_action_data(self, object_name, copy_to_name = None):
        if copy_to_name is None:
            copy_to_name = self.new_name(object_name)
        try:
            copy_from_action = self.scene[0].objects[object_name].animation_data.action
        except AttributeError: 
            print("LOG: %s has no action" %object_name)
            return None
        else:
            copy_to_action = copy_from_action.copy()
            copy_to_action.name = copy_to_name
            return copy_to_action 
            
    def copy_animation_data(self, object_name, new_action = None, copy_to_name = None):
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
                setattr(copy_to_animation, prop, getattr(copy_from_animation, prop))
            if new_action:
                copy_to_animation.action = new_action
            return True
        except AttributeError:
            print("LOG: %s no animation data" %object_name)
            return False

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
        found = False 
        most_similar = None
        min = 0.3
        
        with bpy.data.libraries.load(path, link = True) as (data_from, data_to):
            for group in data_from.groups:
                if group.startswith('grp.') and not group.endswith('LOW') and not group.endswith('MID'): #and similarity > 0.7:
                    print(group)
                    if group == obj_name:
                        group_name = group
                        found = True
                        break
                    else:
                        ratio = self.compare_string(group, obj_name)
                        if ratio >= min:
                            min = ratio
                            most_similar = group
            if found: 
                data_to.groups = [group_name]
            else: 
                print("Could be potentially wrong")
                print(obj_name)
                data_to.groups = [most_similar]
                group_name = most_similar
     
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
        #self.purge_orphan()
        bpy.context.window.screen.scene = bpy.data.scenes[0]
        bpy.ops.scene.delete()
        bpy.data.scenes[0].name = scene_name
        self.remove_old_filepath()
        #self.purge_orphan()

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
                found = False
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
    
    def relink_grp_stuff(self):
        bpy.ops.group.create(name="grp.stuff")                              # Create grp.stuff Group
        current_appended_scene_name = self.scene_name                       # Set scene name
        for obj in bpy.data.scenes[current_appended_scene_name].objects:    # Compair objects to group from master
            if obj.name == (tuple(self.group_objects)):
                bpy.context.scene.objects[bpy.context.scene.objects.active.name].select=False
                bpy.context.scene.objects.active = bpy.data.scenes[current_appended_scene_name].objects[obj.name]
                bpy.ops.object.group_link(group="grp.stuff")

    def _log_(self): #jordan
        """
        Write temporary log file
        """
        import time
        from datetime import datetime
        date_stamp = time.strftime("%Y-%m-%d")
        try:
            fileread = open("C:\\Temp\\main.log", "r")
            fileread.close()
        except:
            file = open("C:\\Temp\\main.log", "w")
            file.write("%s------------------%s------------------\n\n\n"%(date_stamp, self.scene_name))
            for log in self.log:
                file.write("%s --> %s: %s\n" %(datetime.now(), self.scene_name, log))
            file.close()
        else:
            file = open("C:\\Temp\\main.log", "a")
            file.write("\n\n\n%s------------------%s------------------\n\n\n"%(date_stamp, self.scene_name))
            for log in self.log:
                file.write("%s --> %s: %s\n" %(datetime.now(), self.scene_name, log))
            file.close()
                
                