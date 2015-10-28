import bpy

selected = bpy.context.selected_pose_bones


def boneDeform(mode):
    print("New test")
    for item in selected: 
        if item.bone.use_deform == mode: 
            print(item.bone.name)
            print(item.bone.use_deform)
   
   
#change your input True to check is on, False to check if off 
boneDeform(True)
 
 
 
 