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
#  Parent: "Breakout Batch Code"
#  Name: "Save Script",
#  Author: "Jordan Goddard",
#  Company: "Tangent Animation"
#  Blender: (2, 74, 0),
#  Description: "Saves the broken out file a second time to remove any unused data and clear the cache"
#  <pep8 compliant>
# ##### END SCRIPT COMMENTS #####

"""
Import the necesary libraries for the application to call
"""
import bpy
import re



try:
        file_read = open('C:\\Temp\\pass_temp.txt','r').readlines()
except:
    print("\n\n\n\n\n\n\n\nFailure in save_script\n\n\n\n\n\n\n\n")
else:
    line_one = file_read[0]
    match = re.match(r'(\S+\.\S+)', line_one)
    scene_name = match.group(1)
    line_two =  file_read[1]
    match_again = re.match("(\S+)", line_two)
    file_path = match_again.group(1)
if scene_name == None:
    print("\n\n\n\n\n\n\n\n ERROR_undifined_scene_name_ \n\n\n\n\n\n\n\n")
    scene_name = "ERROR_undifined_scene_name_"
filepath = "C:\\Temp\\breakout_tool_data\\blender_files\\%s_publish.blend" % scene_name
bpy.ops.wm.open_mainfile(filepath=filepath)
bpy.ops.file.make_paths_absolute()
bpy.ops.wm.save_as_mainfile(filepath=filepath)
