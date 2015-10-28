#Shot Finaling Module
#Author: Wayne Wu

class CheckShot(object):
    
    def __init__(self, clean_up = False, save = False):
        #global variables
        self.character_list = []
        self.set_list = []
        self.fix = clean_up
        self.save = save
        self.scene = bpy.data.scenes[0]
          
        self.error = []
        self.log = []
        self.check = []
        self.success = []
        self.fail = []
        
    def check_all(self):
        #self.append_shot()
        self.update_objects(self.scene)
        
        for character in self.character_list:
            self.check_character(character)   
        
        for set in self.set_list: 
            self.check_set(set)
            
        self.check_visibility()    
        self.set_camera_clipping()
        self.check_unused_data()
        self.check_scene(self.scene)
   
        self.save_file()
        self.error_logging()
        
        #import time
        #time.sleep(10)
        #quit("next one...")
        return {'FINISHED'}
          
    def append_shot(self):    
        """
        Append the appropriate scene *code from BreakOut Tool 
        """
        #search for filepath from animation\sandbox
        filepath = 'C:\\Temp\\pass_temp.txt'
        
        try:
            file_read = open(filepath,'r').readlines()
        except:
            print("\n\nFailure\n\n")
        else:
            #print(file_read)
            line_one = file_read[0]
            match = re.match(r'(\d+\.\d+)', line_one)
            self.scene_name = match.group(1)
            line_two =  file_read[1]
            match_again = re.match("(\S+)", line_two)
            self.file = match_again.group(1)
            self.seqshot = self.scene_name
        
        #append shot
        try:
            with bpy.data.libraries.load(self.filepath) as (data_from, data_to):     # append scene here 
                 data_to.scenes = [seq_shot]                                         # Limit this to the scene we're working on (ex. 010.0010)
        except: 
            time.sleep(10)
            quit("Cannot open file")
            
        bpy.context.screen.scene = self.scene[0]
        
    def update_objects(self, scene):
        """
        Update all objects to make sure all are pointing to the latest publish directory and the highest resolution possible
        """
        bpy.ops.file.make_paths_absolute()
        self.scene = scene
        import re  
        for obj in self.scene.objects: 
            if obj.name.startswith('grp'):
                try:
                    group_name = obj.dupli_group.name
                except: 
                    self.log.append("%s has no dupli_group, object is not indirect" %obj.name)
                else: 
                    group = bpy.data.groups[group_name]
                    filepath = group.library.filepath
                    is_character = re.search("chr\d+", filepath)
                    if is_character: 
                        self.character_list.append(obj)    
                    is_set = re.search("set\d+", filepath)
                    if is_set:
                        self.set_list.append(obj)
                    if obj.name.startswith('cam') or obj.name.startswith('fcs') or obj.name.startswith('lkt'):
                        #Make sure these are visible and selectable
                        obj.hide = False 
                        obj.hide_select = False
                    if not self._check_filepath(filepath):
                        self.error.append("%s is not pointing the the published version" %obj.name)
                        if self.fix: 
                            pass
                    is_low_res = re.search('LOW', obj.name)
                    if is_low_res:
                        self.error.append("%s is in LOW resolution" %obj.name)
                        if self.fix: 
                            name = obj.name
                            self.scene.objects.unlink(obj)
                            self.link_in_groups(filepath, name)
    
    def _check_filepath(self, filepath):
        """
        Check if the filepath is correct
        """
        import re 
        is_incorrect = re.search('version', filepath)
        if is_incorrect: 
            return False
        else: 
            return True
        
    def character_list(self):
        """
        Cycle through the objects within the scene, and generate a list of characters used in the scene
        """
        import re
        character_list = []   
        for obj in self.scene.objects: 
            if obj.name.startswith('grp'):
                try:
                    group_name = obj.dupli_group.name #the group name 
                except: 
                    self.log.append("%s has no dupli_group" %obj.name)
                else: 
                    group = bpy.data.groups[group_name]
                    file = group.library.filepath
                    is_character = re.search("chr\d+", file)
                    if is_character: 
                        character_list.append(obj)
        self.log.append("Character List: %s", character_list)
        return character_list
     
    def set_list(self):
        """
        Cycle throught the objects within the scene, and generate a list of sets used in the scene
        """        
        import re
        set_list = []   
        for obj in self.scene.objects: 
            if obj.name.startswith('grp'):
                try:
                    group_name = obj.dupli_group.name #the group name 
                except: 
                    self.log.append("%s has no dupli_group" %obj.name)
                else: 
                    group = bpy.data.groups[group_name]
                    file = group.library.filepath
                    is_character = re.search("set\d+", file)
                    if is_character: 
                        set_list.append(obj)     
        self.log.append("Set List: %s", set_list)
        return set_list
    
    def check_set(self, set):
        """
        For each set, check the visibilities of the geo parts
        """
        import re
        group_name = set.name
        similarity = 1.0
        match = re.match("(grp.\w+)", group_name)
        search_str = match.group(1)
        proxy_name = "%s_proxy" %group_name
        for obj in self.scene.objects:         
            is_similar = re.search(search_str, obj.name)# search for proxies here
            has_proxy = re.search('proxy', obj.name)
            if is_similar and has_proxy: 
                #Search for ctl.viz_control.000.C in proxy which has all the controls
                viz_controller = None
                for bone in obj.pose.bones:
                    is_controller = re.search("viz_control", bone.name)
                    if is_controller: 
                        viz_controller = bone
                        break                    
                if viz_controller:
                    items = viz_controller.items()
                    if items:
                        for custom_property in items: 
                            match = re.match(r"\'(\w+)\'", custom_property[0])
                            if match: 
                                custom_prop_name = match.group(1)
                                if custom_prop_name.startswith('Lpoly'):
                                    if god_node[custom_prop_name] > 0:
                                        self.error.append("%s: %s is turned on" %(obj.name, custom_prop_name))
                                    if self.fix: 
                                        god_node[custom_prop_name] = 0
                                        self.success.append("%s: %s is set to 0" %(obj.name, custom_prop_name))
                                elif custom_prop_name != "_RNA_UI":
                                    if god_node[custom_prop_name] > 0:
                                        self.check.append("%s: %s is turned off" %(obj.name, custom_prop_name))
                                    if self.fix: 
                                        god_node[custom_prop_name] = 1
                                        self.success.append("%s: %s is set to 1" %(obj.name, custom_prop_name))
                    else:
                        self.log.append("%s: %s has no custom properties" %(obj.name, viz_controller))
                else: 
                    self.log.append("%s has no viz_control bone" %obj.name)

    def check_character(self, character):
        """
        For each character within the character_list, check the properties
        """
        import re
        group_name = character.name
        match = re.match("(grp.\w+)", group_name)
        search_str = match.group(1)
        proxy_name = "%s_proxy" %group_name
        for obj in self.scene.objects:         
            is_similar = re.search(search_str, obj.name)# search for proxies here
            has_proxy = re.search('proxy', obj.name)
            if is_similar and has_proxy: 
                try:
                    god_node = obj.pose.bones["ctl.god.C"]
                except:
                    self.check.append("%s has no god node" %obj.name)
                else:
                    items = god_node.items()
                    if items: #has custom properties 
                        #print("has custom properties")
                        #print(items)
                        for custom_property in items:
                            custom_prop_name = custom_property[0]
                            if custom_prop_name != "_RNA_UI" and custom_prop_name != "Eye_world_lock":
                                if self.check_animation_data(obj, "pose.bones[\"ctl.god.C\"][\"%s\"]" %custom_prop_name):
                                    self.error.append("%s: Clear keyframes for %s" %(obj.name, custom_prop_name))
                                if self.fix: 
                                    self.remove_animation_data(obj, "pose.bones[\"ctl.god.C\"][\"%s\"]" %custom_prop_name)                                   
                                if custom_prop_name == "Smoothing":
                                    if god_node[custom_prop_name] is 0: 
                                        self.error.append("%s: Smoothing is off" %obj.name)
                                    if self.fix:
                                        god_node[custom_prop_name] = 1
                                        self.success.append("%s: Smoothing is on" %obj.name)
                                elif custom_prop_name == "Proxy_pupil_viz":
                                    if god_node[custom_prop_name] is 1: 
                                        self.error.append("%s:  Proxy_pupil_viz is on" %obj.name)
                                    if self.fix:
                                        god_node[custom_prop_name] = 0 
                                        self.success.append("%s:  Proxy_pupil_viz is off" %obj.name)
                                elif custom_prop_name == "Eye_Smoothing":
                                    if self.fix:
                                        god_node[custom_prop_name] = 1
                                        self.success.append("%s: Eye_Smoothing is on" %obj.name)
                                elif custom_prop_name == "Eye_Smoothing_Level":
                                     if self.fix:
                                        god_node[custom_prop_name] = 2
                                        self.success.append("%s: Eye_Smoothing level is set to 2" %obj.name)
                    else:
                        self.log.append("%s has no custom properties" %god_node)                   
                break
      
    def check_visibility(self):
        for obj in self.scene.objects:
            if obj.name.startswith('lkt') or obj.name.startswith('cam') or obj.name.startswith('fcs'):
                if obj.hide: 
                    self.error.append("%s is not visible" %obj.name)
                    if self.fix: 
                        obj.hide = False
                        self.success.append("%s is visible" %obj.name)
                if obj.hide_select: 
                    self.error.append("%s is not selectable" %obj.name)
                    if self.fix: 
                        obj.hide_select = False
                        self.success.append("%s is selectable" %obj.name)
      
    def check_animation_data(self, obj, datapath):
        try: 
            for fcurve in obj.animation_data.action.fcurves: 
                if fcurve.data_path == datapath: 
                    return True 
                else: 
                    return False
        except AttributeError:
            self.log.append("%s has no animation data" %datapath)
            
    def remove_animation_data(self, obj, datapath):
        try:
            for fcurve in obj.animation_data.action.fcurves: 
                if fcurve.data_path == datapath: 
                    obj.animation_data.action.fcurves.remove(fcurve)
                    self.success.append("%s: %s's keyframe is removed" %(obj, datapath))
                    break
                    
        except AttributeError: 
            self.log.append("%s has no animation data" %datapath)
        
    def set_camera_clipping(self):
        import mathutils
        
        cam_obj = self.scene.camera
        for cam in bpy.data.cameras:
            
            #Remove animation data for end clipping
            clip_end = cam.clip_end
            min = clip_end
            if self.check_animation_data(cam, "clip_end"):
                self.error.append("%s Clear keyframes for clip_end" %cam.name)
                if self.fix: 
                    self.remove_animation_data(cam, "clip_end")
            
            #for obj in self.scene.objects:
            for group in bpy.data.groups: 
                for obj in group.objects: 
                    for box in obj.bound_box:
                        corner_location = mathutils.Vector((box[0], box[1], box[2]))
                        vector = corner_location - cam_obj.location
                        distance = vector.magnitude
                        #OBJ LOCATION IS AT THE CENTER OF THE OBJECT
                        if (distance > min):
                            #print(corner_location)
                            self.log.append("Distance from camera to %s is %f" %(obj.name, distance))
                            min = distance
           
            if min > clip_end:
                self.check.append("End clipping of the camera may not be far enough")
                if self.fix:
                    #clip_end = min
                    #self.success.append("End clipping is set to %f" %clip_end)
                    pass 
                
    def link_in_groups(self, path, obj_name): 
        """"
        Given the link  of the blender file, link in the group in the blender file and select LOW res version if available
        """
        #self.center_cursor()
        # Link in groups, LOW if possible
        import re
        print(path)
        group_name = None
        name = None
        match = re.match(r'(\S+)_LOW', obj_name)#take out "_LOW"
        if match:
            name = match.group(1)
        found = False
        with bpy.data.libraries.load(path, link = True) as (data_from, data_to):
            for group in data_from.groups:
                if group == name:
                    group_name = group
                    found = True
                    data_to.groups = [group_name]
                    break
        if found: 
            self.success.append("%s is relinked" %group_name)  
        if not found:
            self.fail.append("Could not relink %s" %obj_name)
            group_name = obj_name #link back the previous version
             
        """
        Add a null object to duplicate the group (link the group back in the scene) *from BreakOut Tool
        """
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
    
    def compare_string(self, item1, item2):
        """
        Compare two strings and output similarities
        """
        from difflib import SequenceMatcher
        return SequenceMatcher(None, item1, item2).ratio()
    
    def check_unused_data(self):
        for obj in self.scene.objects: 
            
            if not obj.name.startswith('lkt') and not obj.name.startswith('cam') and not obj.name.startswith('fcs') and not obj.name.startswith('grp'):
                try:   
                    obj.users_group.name
                except: 
                    self.check.append("%s might be an unneeded object" %obj.name)
                else:
                    if not obj.users_group.name.startswith("grp.stuff"):
                        self.check.append("%s might be an unneeded object")
                        if self.fix:
                            #self.scene.objects.unlink(obj)
                            pass                
    
    def check_scene(self, scene):

        total_frame = (self.scene.frame_end - self.scene.frame_start) + 1
        self.check.append("Current frame number is %f " %total_frame)
        #Open up connection with shotgun
            #retrieve frame data
            #if different: 
                #FLAG

        if self.fix:
            #Fix procedure
            pass
            
    def save_file(self):
        """
        Save the file if the user selected the save option
        """
        if self.save:
        
            filepath = bpy.data.filepath
            sandbox_dir = None
            import re
            import os

            filename = bpy.path.basename(filepath)
            new_filename = self._filenum_increment(filename)
            sandbox_dir = os.path.dirname(filepath)
            match = re.match(r"(\S+\\)sandbox\\\S+", filepath)
            if match:
                pass
                #publish_dir = "%spublish\\" %match.group(1)
                #publish_path = publish_dir + new_filename
                #bpy.ops.wm.save_as_mainfile(filepath = publish_path, relative_remap = False)
                #self.success.append("File is saved as %s" %publish_path)
            else: 
                self.check.append("File is saved in curruent directory only")
            sandbox_path = "%s\\%s" %(sandbox_dir, new_filename)
            print(sandbox_path)
            bpy.ops.wm.save_as_mainfile(filepath = sandbox_path, relative_remap = False)
            self.success.append("File is saved as %s" %sandbox_path)

    def _filenum_increment(self, filename):
        
        import re
        match = re.match(r'(\d+\.\d+\.v)(\d+)(\.blend)', filename)
        
        if match: 
            digits = len(match.group(2))
            num = int(match.group(2))
            num = num + 1
            num = str(num).zfill(digits)
            
            new_filename = match.group(1) + num + match.group(3)
            return new_filename
        else: 
            self.log.append("Could not increment the file number")
            return filename
      
    def error_logging(self):                               
        """
        Write temporary 'check layout' log file
        """
        import time
        import re      
        import os
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        if not os.path.exists("%s\\log" %directory):
            os.mkdir("%s\\log" %directory)
        date_var = time.strftime("%Y%m%d_%H%M") 
        log_file = "%s\\log\\%s_log_%s.log" %(directory, self.scene.name, date_var)
        try:
            file = open(log_file, "r")
            file.close()
        except:
            file = open(log_file, "w")
            file.close()
        file = open(log_file, "a")
        file.write("\n\n\n------------------%s------------------\n\n\n"%self.scene.name)
        for i in self.log: 
            file.write("-%s- LOG: %s\n" %(self.scene.name, i))
        file.write("\n")
        for i in self.error:
            file.write("-%s- FIX: %s\n" %(self.scene.name, i))
        file.write("\n")
        for i in self.check: 
            file.write("-%s- CHECK: %s\n" %(self.scene.name, i))
        file.write("\n")    
        for i in self.success: 
            file.write("-%s- SUCCESS: %s\n" %(self.scene.name, i))
        file.write("\n")  
        for i in self.fail: 
            file.write("-%s- FAIL: %s\n" %(self.scene.name, i))
        file.close()
          
        self.warning_box(log_file)
         
    def warning_box(self, logfile):
    
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.text.open(filepath = logfile)
   