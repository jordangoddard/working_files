#Bone Parenting Script 

import bpy

armature_name = "Armature.001"
bone_prefix = "ctl."
size_scale = 1.5

#Check if in edit mode
if bpy.context.active_object.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')


#Copy bone parenting
for bone in bpy.context.selected_bones: 
    
    parent_bone = bone.parent
    tail_location = bone.tail
    
    amt = bpy.data.armatures[armature_name]
    
    new_bone = amt.edit_bones.new(bone_prefix + bone.name)
    print(bone.head)
    new_bone.head = bone.head
    print(bone.tail)
    new_bone.tail = bone.tail
    new_bone.tail.z = size_scale*bone.tail.z
    new_bone.parent = bone.parent
    new_bone.parent.use_connect = False
    new_bone.use_inherit_rotation = True
    new_bone.use_inherit_scale = True
    new_bone.use_local_location = True
    
    bone.parent = new_bone
  
    