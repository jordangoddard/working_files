import bpy
  # Get a list of bone modifiers

selected = bpy.context.selected_pose_bones


def stretchVolume(input): 
    for bone in selected:    
         for constraint in bone.constraints:
              bone.constraints["Stretch To"].volume = input
     
#make the selected volume choice: "VOLUME_XZX", "VOLUME_X", "VOLUME_Z", "NO_VOLUME"     
stretchVolume("NO_VOLUME")

