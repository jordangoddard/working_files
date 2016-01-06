bl_info = {
    "name": "Tangent: Integrity Checker Addon",
    "author": "Jordan Goddard",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Tools > Tangent",
    "description": "Checks integrity of a given belnd file or shot",
    "warning": "This is property of Tangent Animation. Any harm caused by this application is the responsibility of the user",
    "wiki_url": "",
    "category": "Tangent"}

import bpy
import struct
import logging 
import re
import time

class integrity_checker_gui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tangent'
    bl_label = "Integrity Checker"
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text = "Check Integrity")
        row = layout.row()
        row.operator("object.check_current_shots", text = "Check Current Shot", icon = 'RADIO')
        row = layout.row()
        row.operator("object.check_all_shot", text = "Check All Shot", icon = 'RADIO')
        row = layout.row()

class check_current_shot(bpy.types.Operator):
    bl_idname = "object.check_current_shots"
    bl_label = "Check Current Shot"
    bl_options = {'UNDO'}
    def invoke(self, context, event):
        print("\n\n\n\n\n\nCHECKING CURRENT SHOT\n\n\n\n\n\n")
        selected_shot = True
        ic_current = check_file_integrity(selected_shot)
        ic_current.check_all()
        return {'FINISHED'}

class check_all_shots(bpy.types.Operator):
    bl_idname = "object.check_all_shot"
    bl_label = "Check All Shots"
    bl_options = {'UNDO'}
    def invoke(self, context, event):
        print("\n\n\n\n\n\nCHECKING ALL SHOTS\n\n\n\n\n\n")
        selected_shot = False
        ic_current = check_file_integrity(selected_shot)
        ic_current.check_all()
        return {'FINISHED'}

class check_file_integrity(object):
    import bpy
    import struct
    import logging 
    import re
    import time

    def __init__(self, selected_shot):
        """
        Instantiate definition
        """
        self.selected_shot = selected_shot
        self.scene_name = None
        self.file = None
        self.scene = None
        self.filepath = self.file
        self.error_log = []
        
    def check_all(self):
        """
        Call all of the definitions in order that they need to run
        """
        print(self.selected_shot)
        if self.selected_shot:
            print("\nOnly one shot\n")
            self.scene_name = bpy.context.scene.name
            self.scene = bpy.data.scenes[self.scene_name]
            self.camera_check()
            self.focus_check()
            self.look_at_check()
            self.indirect_assets_check()
            self.check_special_characters()
            self.extra_asset_check()
            self.grp_transform_check()
            self.write_asset_log()
            self.write_error_log()
        else:
            print("\nAll the shots\n")
            for scene in bpy.data.scenes:
                self.scene_name = scene.name
                self.scene = bpy.data.scenes[self.scene_name]
                self.camera_check()
                self.focus_check()
                self.look_at_check()
                self.indirect_assets_check()
                self.check_special_characters()
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

    def check_special_characters(self):
        for group in bpy.data.groups:
            path_name = "%s"%group.library.filepath
            if "ozzy" in path_name:
                if "ozzy_a" not in path_name:
                    self.error_log.append("%s has ozzy, but should have ozzy_a"%scene.name)
            if "chester" in path_name:
                if "chester_a" not in path_name:
                    self.error_log.append("%s has chester, but should have chester_a"%scene.name)
            if "grunt" in path_name:
                if "grunt_a" in path_name:
                    self.error_log.append("%s has grunt_a, but should have grunt_b"%scene.name)
                elif "grunt_b" not in path_name:
                    self.error_log.append("%s has grunt, but should have grunt_b"%scene.name)

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
                                    try:
                                        par = "grp%s_proxy"%obj.parent.name[3:]
                                    except:
                                        pass
                                    else:
                                        self.error_log.append("%s is a broken part of the rig for %s"%(obj.name, par))
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
        if self.selected_shot:
            save_file = ("C:\\Temp\\breakout_tool_data\\error_logs\\%s_log_%s00.log"%(self.scene_name, date_var))
            try:
                fileread = open(save_file, "r")
                fileread.close()
            except:
                file = open(save_file, "w")
                file.write("------------------%s------------------\n\n\n"%self.scene_name)
                for error in self.error_log:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"),self.scene_name, error))
                file.close()
            else:
                file = open(save_file, "a")
                file.write("\n\n\n------------------%s------------------\n\n\n"%self.scene_name)
                for error in self.error_log:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"),self.scene_name, error))
                file.close()
            finally:
                bpy.context.area.type = 'TEXT_EDITOR'
                bpy.ops.text.open(filepath = save_file)
        elif not self.selected_shot:
            save_file = ("C:\\Temp\\breakout_tool_data\\error_logs\\%s_log_%s00.log"%(self.scene_name[:3], date_var))
            try:
                fileread = open(save_file, "r")
                fileread.close()
            except:
                file = open(save_file, "w")
                file.write("------------------%s------------------\n\n\n"%self.scene_name)
                for error in self.error_log:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"),self.scene_name, error))
                file.close()
            else:
                file = open(save_file, "a")
                file.write("\n\n\n------------------%s------------------\n\n\n"%self.scene_name)
                for error in self.error_log:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"),self.scene_name, error))
                file.close()
            finally:
                bpy.context.area.type = 'TEXT_EDITOR'
                bpy.ops.text.open(filepath = save_file)

    def write_asset_log(self): #jordan
        """
        Create a log file that lists all the assets in each shot.
        """
        date_var = time.strftime("%Y%m%d_%H")                 #what if this takes more than one minute to run?
        selection_name = self.scene_name
        if self.selected_shot:
            try:
                fileread = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name), "r")
                fileread.close()
            except:
                file = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name), "w")
                file.write("------------------Asset List for: %s------------------\n\n\n"%self.scene_name)
                for lib in bpy.data.libraries:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"), self.scene_name, lib.filepath))
                file.close()
            else:
                file = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name), "a")
                file.write("\n\n\n------------------Asset List for: %s------------------\n\n\n"%self.scene_name)
                for lib in bpy.data.libraries:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"), self.scene_name, lib.filepath))
                file.close()
        elif not self.selected_shot:
            try:
                fileread = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name[:3]), "r")
                fileread.close()
            except:
                file = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name[:3]), "w")
                file.write("------------------Asset List for: %s------------------\n\n\n"%self.scene_name)
                for lib in bpy.data.libraries:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"), self.scene_name, lib.filepath))
                file.close()
            else:
                file = open("C:\\Temp\\breakout_tool_data\\asset_logs\\%s_AssetList.log"%(self.scene_name[:3]), "a")
                file.write("\n\n\n------------------Asset List for: %s------------------\n\n\n"%self.scene_name)
                for lib in bpy.data.libraries:
                    file.write("%s:%s: %s\n" %(time.strftime("%Y%m%d_%H%M%S"), self.scene_name, lib.filepath))
                file.close()

def register():
    bpy.utils.register_class(integrity_checker_gui)
    bpy.utils.register_class(check_current_shot)
    bpy.utils.register_class(check_all_shots)
    #bpy.utils.register_class(check_file_integrity)

def unregister():
    bpy.utils.register_class(integrity_checker_gui)
    bpy.utils.register_class(check_current_shot)
    bpy.utils.register_class(check_all_shots)
    #bpy.utils.register_class(check_file_integrity)

def directory_creation():
    import os
    new_path = ["C:\\Temp\\breakout_tool_data", "C:\\Temp\\breakout_tool_data\\error_logs"]
    if not os.path.exists(new_path[0]):
        os.makedirs(new_path[0])
    if not os.path.exists(new_path[1]):
        os.makedirs(new_path[1])

if __name__ == "__main__":
    register()
    directory_creation()
elif __name__ == "__main__":
    unregister()
