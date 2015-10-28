import bpy 

a = bpy.context.selected_editable_bones 


for bone in a:
    print(bone.name)
    a = bone.tail.xyz
    b = bone.head.xyz 
    bone.tail.xyz = b
    bone.head.xyz = a
    
    