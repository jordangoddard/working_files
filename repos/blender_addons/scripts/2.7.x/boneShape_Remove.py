import bpy

selected = bpy.context.selected_pose_bones


def boneShape(mode):
    for item in selected: 
        item.custom_shape = None
   
   
boneShape(0)
 
 
 
 