import bpy
import breakout_tool
import re

def open_checking_file():
    """
    Open the '.BLEND' file for processing and temporarily removes non-essential scenes
    """
    try:
        file_read = open('C:\\Temp\\pass_temp.txt','r').readlines()
    except:
        print("\n\n\n\n\n\n\n\nFailure in breakout_run_script\n\n\n\n\n\n\n\n")
    else:
        line_one = file_read[0]
        match = re.match(r'(\S+\.\S+)', line_one)
        scene_name = match.group(1)
        line_two =  file_read[1]
        match_again = re.match("(\S+)", line_two)
        file_path = match_again.group(1)
        bpy.ops.wm.open_mainfile(filepath=file_path)
        for scene in bpy.data.scenes:
            if scene.name != scene_name:
                bpy.data.screens['Default'].scene = bpy.data.scenes[scene.name]
                bpy.ops.scene.delete()
            elif scene.name == scene_name:
                pass
            else:
                print("Something went wrong!")
        file_write = open('C:\\Temp\\group_data_transfer.txt','w')
        for obj in bpy.data.scenes[scene_name].objects:
            for group_obj in bpy.data.groups["grp.stuff"].objects:
                if group_obj.name == obj.name:
                    file_write.write("%s\n"%obj.name)
        file_write.close()

open_checking_file()