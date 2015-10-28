import bpy
 # Get a list of bone modifiers

selected = bpy.context.selected_pose_bones

for bone in selected: 
    print("yes")
    
    for constraint in bone.constraints:
        print("yes")
        if constraint.type == "STRETCH_TO":
            print("is type")
            bone.constraints["Stretch To"].rest_length = 0
        else:
            print("no")
