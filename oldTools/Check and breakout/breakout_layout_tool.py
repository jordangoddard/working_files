####################################################
# Tangent Animation                                #
#                                                  #
# Author: Jordan Goddard, Wayne Wu, hgagne         #
#                                                  #
# 01/10/2015                                       #
#                                                  #
# PEPSG: https://www.python.org/dev/peps/pep-0008/ #
#                                                  #
####################################################


"""
Import the necesary libraries for the application to call
"""
import bpy
import struct
import logging 
import re
import time

####################################################
# CLASS: CheckLayout                               #
####################################################
    
class CheckLayout(object):
    import bpy
    import struct
    import logging 
    import re
    import time
    """
    Check if the master file is ready for breakout
    """
    def __init__(self, fix=False):
        """
        Instantiate definition
        """
        self.scene_name = None
        self.file = None
        self.scene = None
        self.filepath = self.file
        self.error_log = []
        self.fix = fix
        self.run_it()
        
    def run_it(self):
        """
        Retrieve 'filepath' and 'scene' name from external file
        """
        try:
            file_read = open('C:\\Temp\\check_data.txt','r').readlines()
        except:
            print("\n\nFailure\n\n")
        else:
            line_one = file_read[0]
            match = re.match("(\S+)", line_one)
            self.file = match.group(0)
        
    def check_all(self):
        """
        Call all of the definitions in order that they need to run
        """
        bpy.ops.wm.open_mainfile(filepath=self.file)
        for scene in bpy.data.scenes:
            self.scene_name = scene.name
            self.scene = bpy.data.scenes[self.scene_name]
            self.camera_check()
            self.focus_check()
            self.look_at_check()
            self.indirect_assets_check()
            self.extra_asset_check()
            self.grp_transform_check()
            self.write_temporary_check_layout_error_log()
            
    def camera_check(self): #jordan
        """
        Check if there is a camera in the scene that is named cam.***.****(cam.{sequence}.{shot})
        """
        camera_type = None
        camera = None
        problem_one = False
        problem_two = False
        problem_three = False
        problem_name = None
        try:
            camera = self.scene.objects["cam.%s" % self.scene.name]
        except:
            for obj in bpy.data.scenes[self.scene_name].objects:
                if obj.name.startswith('cam'):
                    problem_one = True
                    problem_name = obj.name
            if problem_one == False:
                problem_two = True
        if camera:
            if bpy.data.scenes[self.scene.name].objects["cam.%s" % self.scene.name].type == ('CAMERA'):
                camera_type = 'The camera is of type "CAMERA"'
            else:
                problem_three = True
        if problem_one:
            self.error_log.append('The camera called "%s" is named wrong. The camera name should be "cam.%s"'%(problem_name, self.scene_name))
        if problem_two:
            self.error_log.append('There is no camera in this shot! Please add a camera named "cam.%s"'%self.scene_name)
        if problem_three:
            self.error_log.append("The camera in the scene is not of type CAMERA!")
        

    def focus_check(self): #jordan
        """
        Check if there is a focus point in the scene that is named fcs.***.****(fcs.{sequence}.{shot})
        """
        problem_one = False
        problem_two = False
        problem_one_name = None
        focus = None
        try:
            focus = self.scene.objects["fcs.%s" % self.scene.name]
        except:
            for obj in bpy.data.scenes[self.scene_name].objects:
                if obj.name.startswith("fcs"):
                    problem_one = True
                    problem_one_name = obj.name
            if problem_one == False:
                problem_two = True
        if problem_one:
            self.error_log.append('The focus point called "%s" is named wrong. The focus point should be called "fcs.%s"'%(problem_one_name, self.scene_name))
        if problem_two:
            self.error_log.append('There is no focus point in this shot! Please add a focus point named "fcs.%s"'%self.scene_name)

    def look_at_check(self): #wayne
        """
        Check if there is a look at/aim in the scene that is named lkt.***.****(lkt.{sequence}.{shot})
        """
        problem = False
        problem_name = None
        for obj in bpy.data.scenes[self.scene_name].objects:
            if obj.name.startswith('lkt'):
                try:
                    look_at = self.scene.objects['lkt.%s' % self.scene.name]
                except:
                    problem = True
                    problem_name = obj.name
        if problem:
            self.error_log.append('The look at point called "%s" is named wrong. The look at point should be called "lkt.%s"'%(problem_name, self.scene_name))

    def indirect_assets_check(self): #wayne
        """
        Look for non-linked assets
        """
        import re
        item_prefix = ["cam", "fcs", "lkt", "grp.stuff"]
        for obj in self.scene.objects:
            if obj.name.startswith("grp.stuff"):                                            # skip objects under 'grp.stuff'
                pass
            elif obj.name.startswith('grp'):
                proxy = re.search("proxy", obj.name)
                if not proxy:
                    try:
                        group_name = obj.dupli_group.name
                        group = bpy.data.groups[group_name]
                        if group.library:
                            pass                                                   # print(group.library.filepath)
                        else:
                            print("not linked")
                            if obj.name.startswith(tuple(item_prefix)):
                                pass
                            else:
                                #newcheck
                                match_response = False
                                check_grp = False
                                for grp in bpy.data.groups:
                                    if grp.name == "grp.stuff":
                                        check_grp = True
                                if check_grp:
                                    for match in bpy.data.groups["grp.stuff"].objects:
                                        if match.name == obj.name:
                                            match_response = True
                                if match_response:
                                    pass
                                else:
                                    self.error_log.append("%s is not linked" %(obj.name))
                    except:
                        pass                                                       # print('NO DUPLI GROUP')
            else: 
                if obj.library:
                    pass                                                           # print(obj.library.filepath), print("%s is linked" %obj.name)
                else: 
                    if obj.name.startswith(tuple(item_prefix)):
                        pass
                    else:
                        match_response = False
                        check_grp = False
                        for grp in bpy.data.groups:
                            if grp.name == "grp.stuff":
                                check_grp = True
                        if check_grp:
                            for match in bpy.data.groups["grp.stuff"].objects:
                                if match.name == obj.name:
                                    match_response = True
                        if match_response:
                            pass
                        else:
                            self.error_log.append("%s is not linked" %(obj.name))

    def search_thru_library(self, obj_name): #wayne
        """
        Search through the library files to see if objects are linked
        """
        count = 0
        dosearch = True
        linked = False

        while(dosearch and not linked):
            try: 
                bpy.data.libraries[count]
            except: 
                self.error_log.append("Library out of range")
                print("out of range")
                dosearch = False
                pass
            if dosearch:
                for file in bpy.data.libraries[count].users_id:
                    if obj_name == file.name:
                        linked = True                                              # print('%s is linked' % ob_name)
                        break
            count = count + 1
        return linked
        
    def extra_asset_check(self): #hgagne
        """
        Retrieve list of items in shot
        """
        for obj in self.scene.objects:
            item_prefix = ["cam", "fcs", "grp", "lkt", "nul", "render", "world"]
            if obj.name.startswith(tuple(item_prefix)):
                pass                                                                # good, check next scene item (asset) including 'grp.stuff'
            else:
                match_response = False
                check_grp = False
                for grp in bpy.data.groups:
                    if grp.name == "grp.stuff":
                        check_grp = True
                if check_grp:
                    for match in bpy.data.groups["grp.stuff"].objects:
                        if match.name == obj.name:
                            match_response = True
                if match_response:
                    pass
                else:
                    self.error_log.append("%s is an invalid asset"%(obj.name))
                

    def grp_transform_check(self): #wayne
        """
        Anything with the tag grp should have a transformation on nul in object mode
        """
        for obj in self.scene.objects:
            object_name = obj.name
            import re
            grp = re.match('grp\.\S+', object_name)
            if grp:
                grp = grp.group(0)
                (location_x, location_y, location_z) = bpy.data.objects[grp].location
                (rotation_x, rotation_y, rotation_z) = bpy.data.objects[grp].rotation_euler
                (scale_x, scale_y, scale_z) = bpy.data.objects[grp].scale
                if location_x != 0 or location_y != 0 or location_z != 0:
                    self.error_log.append("%s location is not at (0,0,0)"%(obj.name))   # This will log the data to a file
                if rotation_x != 0 or rotation_y != 0 or rotation_z != 0:
                    self.error_log.append("%s rotation is not at (0,0,0)"%(obj.name))   # This will log the data to a file
                if scale_x != 1 or scale_y != 1 or scale_z != 1:
                    self.error_log.append("%s scale is not at (0,0,0)"%(obj.name))      # This will log the data to a file
                    
    def check_audio(self):                                                              # all scenes need an audio track
        """
        Look for presence of 'sequence_editor'; if missing, no audio 
        tracks exist in current scene
        """
        try:
            audio = self.scene.sequence_editor.sequences_all
        except:
            print("ERROR: No Audio")                                                    # not suppose to happen
    def error_log_to_csv(self, message): #jordan
        """
        Write errors to CSV log
        """
        pass                                                                            # log the data, skipped for now

    def write_temporary_check_layout_error_log(self): #jordan                                           # This will log the data to a file
        """
        Write temporary 'check layout' log file
        """
        date_var = time.strftime("%Y%m%d_%H")                 #what if this takes more than one minute to run?
        selection_name = self.scene_name
        try:
            fileread = open("C:\\Temp\\breakout_tool_data\\error_logs\\%s_log_%s00.log"%(self.scene_name[:3], date_var), "r")
            fileread.close()
        except:
            file = open("C:\\Temp\\breakout_tool_data\\error_logs\\%s_log_%s00.log"%(self.scene_name[:3], date_var), "w")
            file.write("------------------%s------------------\n\n\n"%self.scene_name)
            for error in self.error_log:
                file.write("%s: %s\n" %(self.scene_name, error))
            file.close()
        else:
            file = open("C:\\Temp\\breakout_tool_data\\error_logs\\%s_log_%s00.log"%(self.scene_name[:3], date_var), "a")
            file.write("\n\n\n------------------%s------------------\n\n\n"%self.scene_name)
            for error in self.error_log:
                file.write("%s: %s\n" %(self.scene_name, error))
            file.close()
            

####################################################
# CLASS: BreakOut                                  #
####################################################


class BreakOut(object):
    import bpy
    import struct
    import logging 
    import re
    import time
    def __init__(self):
        """
        This will run when this class is called and will carry any passed objects
        """
        import bpy
        self.scene_name = None
        self.seqshot = None
        self.filepath = None
        self.context = bpy.context
        self.data = bpy.data
        self.ops = bpy.ops
        self.random_suffix = "2Chia19_"                                # this can be any random 8 charector string you want. (it is just to prevent layout from having a file name the same)
        self.scene = bpy.data.scenes
        self.path = bpy.path
        self.old_start_frame = None
        self.old_end_frame = None
        self.file_name = None
        self.new_scene = None
        self.old_filepath = []
        
        #self.prepare_shot_file()
        self.run_it()
        #self.open_checking_file()
        #self.execute()
        self.offset = None

    def run_it(self):
        """
        Retrieve 'filepath' and 'scene' name from external file
        """
        try:
            file_read = open('C:\\Temp\\pass_temp.txt','r').readlines()
        except:
            print("\n\nFailure\n\n")
        else:
            #print(file_read)
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
    
    def execute(self): #jordan
        """
        This will execute the deffinitions in this class
        """
        self.clean_scene()   
        #                   self.create_self.new_scene()                # Not required for now
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
        #                   self._set_display_options()                 # Not required for now
        #                   self._set_output_options()                  # Not required for now
        #                   self._playblast()                           # Not required for now
        self.delete_original_scene()
        print("DELETE DONE")
        self.remove_new_asset_suffix()
        self.link_LOW()
        self.playblast_manager()
        print("RENAME DONE")
        #                   self._save()a
        #                   self.append_what_we_did_to_some_csv_file_or_something()

    def test_run(self):
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
        
        return {'FINISHED'}
        
    def get_offset(self):
        self.offset = (self.scene[0].frame_start - 1)
    
    def clean_scene(self): #jordan
        """
        This will empty the current scene of all its assets
        """
        selection_pattern = bpy.ops.object.select_pattern
        for obj in self.scene[0].objects:
            selection_pattern(pattern=obj.name)
            bpy.ops.object.delete()
        self.center_cursor()   
    
    def append_original_shot_file(self, filepath, seq_shot): #wayne
        """
        Append the shot at Scene.random_suffix, then use this to gather information on the
        """ 
        import time
        self.filepath = self.file
        print(self.filepath)
        try:
            with bpy.data.libraries.load(self.filepath) as (data_from, data_to):     # append scene here 
                 data_to.scenes = [seq_shot]                                         # Limit this to the scene we're working on (ex. 010.0010)
        except: 
            time.sleep(10)
            quit("Cannot open file")
            
        bpy.context.screen.scene = self.scene[0]                                     # remove original scene (some scene) to make it the current scene
        self.scene[1].name = self.new_name(self.scene[0].name)
        self.new_scene = self.scene[1]
        bpy.ops.file.make_paths_absolute()
        return {'FINISHED'}

    def transfer_asset_data(self, scene_from, scene_to): #Wayne 
        """
        Transfer asset data to new scene
        """
        import re

        self.new_scene = scene_to
        scene = scene_from                                                           # retrieve data from the scene file
        
        self.new_scene.frame_start = scene.frame_start
        self.new_scene.frame_end = scene.frame_end
        self.new_scene.sequence_editor_create()
        try:
            for audio in scene.sequence_editor.sequences_all:
                self.new_scene.sequence_editor.sequences.new_sound(audio.name, audio.filepath, audio.channel, audio.frame_start)
        except:
            print("ERROR: No Audio")                                                 # not a valid scenario
        
        object_list = []
        all_relationship = []
        new_object_list = []                                                         # name only

        for obj in scene.objects:
            if self.useful_check(obj):
                obj.name = obj.name + "X" # -> This it to make sure that the constraints will get copied over (extreme cases)
                object_list.append(obj) 
        #print (object_list)

        for obj in object_list: 
            object_relationship = self.check_relationship(obj.name, object_list)     # returns list
            all_relationship.append(object_relationship)                             # append list

        object_num = 0
        for obj in object_list:
            new_object_list.append(None)
            object_num = 1 + object_num
        #print(object_num)   
        
        for obj in object_list:
            if obj.name.startswith('grp'):
                search_proxy = re.search("proxy", obj.name)
                if not search_proxy:                                                 # it's not a proxy 
                    object_index = object_list.index(obj) 
                    proxy_index = None
                    try:
                        obj.dupli_group.name
                    except: 
                        print("error in group")
                    else:
                        group_name = obj.dupli_group.name
                        group = bpy.data.groups[group_name]
                        publish_link = self._publish_path(group.library.filepath)
                        proxy_name = "%s_proxy" %group_name
                        proxy_name2 = "%s_proxy" %obj.name
                        proxy = False
                        for obj in object_list:                                      # search for proxies here
                            search = re.search(proxy_name, obj.name)
                            search2 = re.search(proxy_name2, obj.name)
                            if search or search2: 
                                print("%s has proxy" %group_name)
                                proxy_index = object_list.index(obj)
                                proxy = True
                                proxy_name = obj.name
                                break
                        new_group_name = self.link_in_groups(publish_link, obj.name)           # link in groups from publish file, return the name of the group; print(new_group_name)
                        new_group_name = self.create_empty(new_group_name, publish_link, self.new_scene.name) # link in HI RES
                        new_object_list[object_index] = new_group_name
                        if proxy: 
                            print("Create Proxy")
                            print(new_group_name)
                            #self.scene[1].objects.link(self.scene[0].objects[proxy_name])
                            new_proxy_name = self.create_armature_proxies(new_group_name) 
                            #new_scene_proxy = self.scene[1].objects[proxy_name]
                            #if new_scene_proxy.name.endswith('X'):
                                #new_scene_proxy.name = new_scene_proxy.name[:-1]
                            #new_proxy_name = new_scene_proxy.name
                            new_object_list[proxy_index] = new_proxy_name
                            self.copy_animation_data(proxy_name, new_proxy_name)
            else:
                object_index = object_list.index(obj)
                new_object_list[object_index] = self.new_name(obj.name)          # note this
                self.copy_item(obj.name)
                self.copy_animation_data(obj.name)    

        self.transfer_constraints(object_list, new_object_list, all_relationship, object_num)
        self.relink_dof()
        
        return {'FINISHED'}
    
    def relink_dof(self):
        
        focus = None
        for obj in self.new_scene.objects: 
            if obj.name.startswith('fcs'):
                focus = obj
                
        for camera in bpy.data.cameras:
            camera.dof_object = focus
        
    def useful_check(self, obj): #wayne
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
    
    def check_relationship(self, obj_name, obj_list): #wayne
        """
        Generate a list of all relationships that existed in the scene
        """
        parent_data=[None, None]                                                 # parent's name, parent's type   
        constraint_data=[None, None, None]                                       # constraint's type, constraint's target, constraint's sub_target
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
                            constraint_data[1] = obj_list.index(obj)    #Interger           
                            constraint_data[2] = constraint.subtarget #String type
                    else:
                        constraint_data[1] = obj_list.index(obj)      #Interger                        
                        constraint_data[2] = constraint.subtarget   #String type 
                all_constraints.append(constraint_data)    
        except AttributeError: 
            print("no constraint")

        if not all_constraints:
            all_constraints.append(None)
        all_relationship = parent_data + all_constraints
        print(all_relationship)
        return all_relationship

    def transfer_constraints(self, object_list, new_object_list, all_relationship, index): #wayne
        """
        Transfer constraints (and parenting) from old scenes to new scenes (Relies heavily on an address/index based procedural code)
        """

        print(new_object_list)
        i = 0
        while (i < index):
            if new_object_list[i]:
                obj = self.new_scene.objects[new_object_list[i]]                     # set parenting
                if all_relationship[i][0]:
                    new_index = all_relationship[i][0]
                    obj.parent = self.new_scene.objects[new_object_list[new_index]]
                    obj.parent_type = all_relationship[i][1]
                constraint_num = 2                                                   # set constraints    
                for copy_from_constraint in object_list[i].constraints:
                    constraint_type = copy_from_constraint.type
                    properties = [prop.identifier for prop in copy_from_constraint.bl_rna.properties if not prop.is_readonly]
                    new_object = self.new_scene.objects[new_object_list[i]]
                    copy_to_constraints = new_object.constraints.new(constraint_type)
                    for prop in properties: 
                        print(prop)
                        setattr(copy_to_constraints, prop, getattr(copy_from_constraint, prop))    
                    #relink constraint to the new one
                    if all_relationship[i][constraint_num]: #has constraint
                        copy_to_constraints.type = all_relationship[i][constraint_num][0]
                        new_index = all_relationship[i][constraint_num][1]
                        import re
                        new_object_name = new_object_list[new_index]
                        search = re.search('proxy', new_object_name)
                        if search:                                                   # it's a proxy
                            copy_to_constraints.target = self.new_scene.objects[new_object_name].proxy
                            copy_to_constraints.subtarget = all_relationship[i][constraint_num][2]
                        else:                                                        # not a proxy
                            copy_to_constraints.target = self.new_scene.objects[new_object_name]
                            try:
                                copy_to_constraints.subtarget = all_relationship[i][constraint_num][2]       
                            except:
                                print("No subtarget")
                    constraint_num = constraint_num + 1   
            i = i + 1

    def create_armature_proxies(self, new_group_name): #jordan/wayne
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
            bpy.ops.object.proxy_make(object = rig_name) #The proper rig 
        except:
            bpy.ops.object.proxy_make()
            print("%s's proxy might be incorrect", obj.name)
        proxy_name = "%s_proxy" %obj.name
        return proxy_name

    def copy_item(self, object_name, copy_to_name = None): #wayne
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

    def copy_animation_data(self, object_name, copy_to_name = None): #wayne
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

    def _publish_path(self, path): #wayne
        """"
        Correct the path of the blender file link so that it points to the publish version 
        """
        import re
        import os                                                                    #for file searching
        import fnmatch

        m = re.match(r'(T:\\Projects\\0043_Ozzy\\Assets\\\w+\\\w+\\publish\\)versions\\\S+', path)
        if m: 
            self.old_filepath.append(path)
            publish_dir = m.group(1)                                                 # print(publish_dir)
            for item in os.listdir(publish_dir):                                     # search through the directory
                if fnmatch.fnmatch(item, '*.blend'):                                 # print(item)
                    path = publish_dir + item                                        # print(path), published blend filepath
                    break                                                            # right now it's assuming that the first file you see is the good version (in most case should be true)
        return path                                                                  # return the corrected path

    def link_in_groups(self, path, obj_name): #wayne
        """"
        Given the link  of the blender file, link in the group in the blender file and select LOW res version if available
        """
        self.center_cursor()                                                         # Link in groups, LOW if possible
        group_name = None

        with bpy.data.libraries.load(path, link = True) as (data_from, data_to):
            for group in data_from.groups:
                #similarity = self.compare_string(obj_name, group)
                #group name has to start with grp
                if group.startswith('grp.') and not group.endswith('LOW') and not group.endswith('MID'): #and similarity > 0.7:
                    group_name = group
                    #if LOW, pick LOW
                    #if group.endswith('LOW'): ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                        #group_name = group
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
        
    def create_empty(self, group_name, path, scene_name = None): #wayne
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

    def set_new_scene_start_end(self): #jordan/hilaire
        """
        Reset newly created scene 'start(1)'/'end' frames relative to original scene 'start'/'end' frames
        """
        shot_original_frame_start = self.scene[0].frame_start                                 # need original scene info, should likely be a global
        shot_original_frame_end = self.scene[0].frame_end                                     # need original scene info, should likely be a global
        self.scene[1].frame_start = shot_original_frame_start - self.offset # sets 'start' at Frame 1
        self.scene[1].frame_end = shot_original_frame_end - self.offset

    def reset_audio_offsets(self): #hilaire
        """
        Moves audio tracks back relative to their original positions
        'Name' has to be changed last since that effectively renames the object
        """
        self.shot_original_scene = self.scene[0]                                              # need original scene info, should likely be a global
        self.shot_new_scene = self.scene[1]                                                   # need target scene info, should likely be a global
        shot_original_frame_start=self.shot_original_scene.frame_start

        for obj in self.new_scene.sequence_editor.sequences_all:                              # iterate through each audio track
            shot_audio_file_path=obj.filepath
            shot_audio_file_name=self.path.basename(shot_audio_file_path)                     # the filename will be the 'friendly' name
            shot_audio_file_current_start_frame=obj.frame_start
            shot_audio_file_new_start_frame = shot_audio_file_current_start_frame - self.offset   # sets 'start' at Frame 1
            obj.frame_start = shot_audio_file_new_start_frame
            obj.name = shot_audio_file_name

    def reset_animation_offsets(self): #hilaire
        """
        Move keyframes and handles back relative to their original positions
        'Left Handle' should be moved last
        """
        self.shot_original_scene = self.scene[0]                                              # need original scene info, should likely be a global
        self.shot_new_scene = self.scene[1]                                                   # need target scene info, should likely be a global

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

    def _set_output_options(self): #jordan
        """
        Set the output settings for the playblast
        """
        scene = bpy.data.scenes
        #render_path = None
        for current_scene in bpy.data.scenes:
            #current_scene.render.filepath("C:\\Temp")
            #render_path = self.output_render_path 
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
            #scene[current_scene.name].render.filepath = render_path

    def playblast_manager(self):
        pass
        """
        This manages the playblast process
        """
        """
        self._set_display_options()
        self._set_output_options()
        self._playblast()

        """
            
    def _playblast(self): 
        """
        Playblast
        """
        bpy.ops.render.opengl(animation=True)

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
        pass

    def remove_new_asset_suffix(self): #jordan
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
                """
                Add a null object to duplicate the group (link the group back in the scene) *from BreakOut Tool
                """
                if found:
                    bpy.context.scene.objects.unlink(obj)
                    scene = bpy.context.scene
                    null = bpy.data.objects.new(group_name, None)
                    null.location = (0,0,0)
                    null.empty_draw_type = 'PLAIN_AXES'
                    null.dupli_type = 'GROUP'
                    null.dupli_group = bpy.data.groups[group_name]
                    group_name = null.name        
                    scene.objects.link(null)

    def remove_old_filepath(self): #Wayne
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
            

    def new_name(self, obj_name): #wayne
        """"
        Generate a random suffix to the object
        """
        obj_name = "%s.%s" % (obj_name, self.random_suffix)

        return obj_name

    def center_cursor(self): #jordan
        """
        This will ensure that the cursor's translation is set to (0, 0, 0)
        """
        self.context.scene.cursor_location.xyz = (0,0,0)
        
    def create_new_scene(self): #jordan
        """ 
        this will create a new scene
        """
        self.ops.scene.new(type="NEW")
        
    def purge_orphan(self): #jordan
        """
        Purge orphan data from scene
        Might need to use the 'old' method: https://github.com/meta-androcto/blenderpython/blob/master/scripts/addons_extern/orphan_cleanup.py
        This is new for blender 2.7 (https://developer.blender.org/rB263518e)
        """
        # bpy.ops.outliner.orphans_purge                              
        pass

    def append_what_we_did_to_some_csv_file_or_something(self): 
        """
        Append activities to CSV file
        May already exist in a separate class
        """
        pass

    def lock_items(self): #jordan
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
