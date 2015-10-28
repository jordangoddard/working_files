__author__ = 'Jeff.Bell'

def default_settings(**kwargs):
    import bpy
    from bpy import context
    userprefs = context.user_preferences
    system = userprefs.system

    # Turn on script execution
    system.use_scripts_auto_execute = True

    # Turn on VBO's
    system.use_vertex_buffer_objects = True

    # Load addons that we use - add to this as we go
    addons_to_load = [
        "ui_layer_manager",
    ]

    for addon in addons_to_load:
        result = bpy.ops.wm.addon_enable(module=addon)
        if result != {'FINISHED'}:
            print("%s did not load correctly - contact support@tangent-animation.com" % addon)


