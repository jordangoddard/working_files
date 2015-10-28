import bpy
import breakout_layout_tool
import re


br = breakout_layout_tool.BreakOut()

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

def _save(scene_name): #hilaire
    temp_scene_name = scene_name
    filepath = "C:\\Temp\\breakout_tool_data\\blender_files\\%s_publish.blend" % temp_scene_name
    bpy.ops.wm.save_as_mainfile(filepath=filepath) #Save file here

if __name__ == "__main__":
    br.execute()
    if scene_name == None:
        scene_name = "_error_finding_name"
    _save(scene_name)