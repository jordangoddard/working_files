import bpy
import re

try:
        file_read = open('C:\\Temp\\pass_temp.txt','r').readlines()
except:
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFailure\n\n")
else:
    line_one = file_read[0]
    match = re.match(r'(\d+\.\d+)', line_one)
    scene_name = match.group(1)
    line_two =  file_read[1]
    match_again = re.match("(\S+)", line_two)
    file_path = match_again.group(1)
if scene_name == None:
    scene_name = "ERROR_undifined_scene_name_"
filepath = "C:\\Temp\\breakout_tool_data\\blender_files\\%s_publish.blend" % scene_name
bpy.ops.wm.open_mainfile(filepath=filepath)
bpy.ops.file.make_paths_absolute()
bpy.ops.wm.save_as_mainfile(filepath=filepath)
print("I'm done.\nI hope all is good now! :)")