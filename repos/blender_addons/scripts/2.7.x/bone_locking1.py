import bpy 



Selbone = bpy.context.selected_pose_bones 


print("bone") 


for bone in Selbone:
    if "ctl." not in bone.name[0:4]:
        print(bone)
        print(bone.name)
        
        #Lock the location 
        bone.lock_location[0] = True
        bone.lock_location[1] = True
        bone.lock_location[2] = True
        
        #Lock the scale
        bone.lock_scale[0] = True
        bone.lock_scale[1] = True
        bone.lock_scale[2] = True
        
        #Lock the Rotation main
        bone.lock_rotation[0] = True
        bone.lock_rotation[1] = True
        bone.lock_rotation[2] = True
        
        #Lock the Rotation if other two types
        bone.lock_rotation_w = True
        bone.lock_rotations_4d = True
 
    else: 
        print("%s is a control bone" % bone)
    
    


