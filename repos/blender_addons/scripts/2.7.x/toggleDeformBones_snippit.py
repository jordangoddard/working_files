import bpy

# Rename default pitchipoy controls to tangent animation control nameing convension

bonelist=bpy.data.armatures['rig'].bones

for item in bonelist:
    item.use_deform= (0)
