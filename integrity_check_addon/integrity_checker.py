####################################################
# Tangent Animation                                #
#                                                  #
# Author: Jordan Goddard, Wayne Wu, hgagne         #
#                                                  #
# 01/10/2015                                       #
#                                                  #
# PEPSG: https://www.python.org/dev/peps/pep-0008/ #
#                                                  #
# Integrity checker tool                           #
####################################################

import bpy
import struct
import logging 
import re
import time


class check_file_integrity(object):
    import bpy
    import struct
    import logging 
    import re
    import time

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
        self.pull_file_data()
        
    def pull_file_data(self):
        """
        Retrieve 'filepath' name from external file
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
            self.write_asset_log()
            self.write_error_log()

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

    def check_audio(self): #jordan
        """
        Look for presence of 'sequence_editor'; if missing, no audio 
        tracks exist in current scene
        """
        try:
            audio = self.scene.sequence_editor.sequences_all
        except:
            print("ERROR: No Audio")                                                    # not suppose to happen

    def write_error_log(self): #jordan
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

    def write_asset_log(self): #jordan
        """
        Create a log file that lists all the assets in each shot.
        """
        date_var = time.strftime("%Y%m%d_%H")                 #what if this takes more than one minute to run?
        selection_name = self.scene_name
        
        try:
            fileread = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(new_file_name), "r")
            fileread.close()
        except:
            file = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name[:3]), "w")
            file.write("------------------Asset List for: %s------------------\n\n\n"%self.scene_name)
            for obj in bpy.data.scenes[self.scene_name].objects:
                file.write("%s: %s\n" %(self.scene_name, obj.name))
            file.close()
        else:
            file = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name[:3]), "a")
            file.write("\n\n\n------------------Asset List for: %s------------------\n\n\n"%self.scene_name)
            for obj in bpy.data.scenes[self.scene_name].objects:
                file.write("%s: %s\n" %(self.scene_name, obj.name))
            file.close()