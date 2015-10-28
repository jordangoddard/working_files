import bpy

selected = bpy.context.selected_pose_bones


def boneDeform(mode):
    for item in selected: 
        item.bone.use_deform = mode
   
   
#change your input 1 is on 0 is off    
boneDeform(0)
 
 
 
 
 
