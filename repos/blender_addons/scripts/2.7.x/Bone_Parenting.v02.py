#Bone Parenting Script 
#Author: Wayne Wu

import bpy
import re

#User Input
mew_bone_prefix = "acc."
old_bone_prefix = "ctl."
size_scale = 1.5


#None User input var 
armature_name = None
new_bone_name = None


#Check if in edit mode
if bpy.context.active_object.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')

#Retrieve armature name
for obj in bpy.context.selected_objects: 
    if obj.type == 'ARMATURE':
        armature_name = obj.name


#Copy bone parenting
for bone in bpy.context.selected_bones: 
    
    parent_bone = bone.parent
    tail_location = bone.tail
    
    amt = bpy.data.armatures[armature_name]
    
    match = re.match("%s(\S+)" %old_bone_prefix, bone.name)
    if match:
        new_bone_name = match.group(1)
        
    new_bone = amt.edit_bones.new(new_bone_name)
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
    new_bone.use_deform = False
    
    bone.parent = new_bone