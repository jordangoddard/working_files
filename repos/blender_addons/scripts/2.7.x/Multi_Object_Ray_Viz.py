import bpy

a = bpy.context.selected_objects
state = False
    
for object in a: 
    object.cycles_visibility.camera = state
    object.cycles_visibility.diffuse = state
    object.cycles_visibility.glossy = state
    object.cycles_visibility.transmission = state
    object.cycles_visibility.scatter = state
    object.cycles_visibility.shadow = state