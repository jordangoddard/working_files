import bpy
selBone = bpy.context.selected_pose_bones
for item in selBone:
    item.rotation_mode = 'XZY'