bl_info = {
    "name": "Swap Animation Tool",
    "author": "Jordan Goddard",
    "version": (1, 0, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Panel > Tangent",
    "description": "Moves animation from one object bone to another",
    "warning": "This is a custom blender addon. USE AT OWN RISK!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Home.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import bpy
from bpy.types import Panel, Operator


class OBJECT_PT_mainGUI(bpy.types.Panel):                                                                                                                                                       # Main GUI of Animation Mover Tool
    '''
    Main GUI of Animation Mover Tool
    '''
    bl_label = "Swap Animation Tool"                                                                                                                                                            # bl_label
    bl_idname = "OBJECT_swap_animation"                                                                                                                                                         # bl_idname
    bl_space_type = 'VIEW_3D'                                                                                                                                                                   # bl_space_type
    bl_region_type = 'TOOLS'                                                                                                                                                                    # bl_region_type
    bl_category = "Tangent"                                                                                                                                                                     # bp_category

    def draw(self, context):                                                                                                                                                                    # Draw functionality, where the graphics are created and displayed to the user
        '''
        Draw functionality, where the graphics are created and displayed to the user
        '''
        layout = self.layout                                                                                                                                                                    # Create General UI Layout
        row1 = layout.row()                                                                                                                                                                     # Create General UI Layout
        col1 = row1.column()                                                                                                                                                                    # Create General UI Layout
        col2 = row1.column()                                                                                                                                                                    # Create General UI Layout
        row3 = layout.row()                                                                                                                                                                     # Create General UI Layout
        scene = context.scene                                                                                                                                                                   # Set current scene based on context
        col1.prop_search(scene, "PusherObject", scene, "objects")                                                                                                                               # List of objects to pull animation from
        col2.prop_search(scene, "PullerObject", scene, "objects")                                                                                                                               # List of objects to push animation to
        if "proxy" in bpy.context.scene.PusherObject:                                                                                                                                           # Only allow bone selection if object is a proxy object with bones
            col1.prop_search(scene, "PusherBone", bpy.data.scenes[scene.name].objects[bpy.context.scene.PusherObject].pose, "bones")                                                            # List of all bones for selected object to pull animation from
        if "proxy" in bpy.context.scene.PullerObject:                                                                                                                                           # Only allow bone selection if object is a proxy object with bones
            col2.prop_search(scene, "PullerBone", bpy.data.scenes[scene.name].objects[bpy.context.scene.PullerObject].pose, "bones")                                                            # List of all bones for selected object to push animation to
        try:
            push_bone = bpy.data.scenes[scene.name].objects[bpy.context.scene.PusherObject].pose.bones[bpy.context.scene.PusherBone]                                                            # Check if the selected pulling bone is actually in the pulling object
            pull_bone = bpy.data.scenes[scene.name].objects[bpy.context.scene.PullerObject].pose.bones[bpy.context.scene.PullerBone]                                                            # Check if the selected pushing bone is actually in the pushing object
        except:
            if "proxy" in bpy.context.scene.PusherObject:                                                                                                                                       # Only allow bone selection if object is a proxy object with bones
                if "proxy" in bpy.context.scene.PullerObject:                                                                                                                                   # Only allow bone selection if object is a proxy object with bones
                    row3.operator("object.do_not_run_animation_swap", text = "Select Appropriate Bones", icon = 'CONSTRAINT')                                                                   # Show button that shows that the selected bones are not in their given objects
        else:
            if "proxy" in bpy.context.scene.PusherObject:                                                                                                                                       # Only allow bone selection if object is a proxy object with bones
                if "proxy" in bpy.context.scene.PullerObject:                                                                                                                                   # Only allow bone selection if object is a proxy object with bones
                    row3.operator("object.run_animation_swap", text = "Swap Animation", icon = 'CONSTRAINT')                                                                                    # Button to move animation from the pulling bone to the pushing bone


class main(object):
    '''
    Main Functionality of tool
    '''
    bl_label = "main"
    bl_idname = "object.main_function"
    bl_description = "run main functionality of button"
    bl_options = {'UNDO'}

    def activate(outobj,inobj,outbone,inbone):
        print("Transfering data from %s:%s to %s:%s"%(outobj,inobj,outbone,inbone))
        sen_obj = outobj
        rec_obj = inobj
        sen_bon = outbone
        rec_bon = inbone
        if sen_obj:
            if rec_obj:
                if sen_bon:
                    if rec_bon:
                        scene = bpy.context.scene
                        obj_list = []
                        old_obj = None
                        new_obj = None
                        print("\n\n")
                        for o in bpy.data.scenes[scene.name].objects:
                            if sen_obj in o.name:
                                old_obj = o
                            if rec_obj in o.name:
                                new_obj = o
                        try:
                            anim = old_obj.animation_data.action.copy()                    # get action
                        except:
                            print("There are no actions on this bone to push to the new character")
                        else:
                            if anim:
                                new_obj.animation_data.action = anim                    # set action
                                print(anim.name)
                                try:
                                    fc = new_obj.animation_data.action.fcurves
                                except:
                                    print("The action on this bone has no animation data")
                                else:
                                    print("Moving animation")
                                    fc[0].lock = False
                                    fc[0].data_path = 'pose.bones["%s"].location'%rec_bon
                                    fc[0].array_index = 0
                                    fc[0].lock = True
                                    fc[1].lock = False
                                    fc[1].data_path = 'pose.bones["%s"].location'%rec_bon
                                    fc[1].array_index = 1
                                    fc[1].lock = True
                                    fc[2].lock = False
                                    fc[2].data_path = 'pose.bones["%s"].location'%rec_bon
                                    fc[2].array_index = 2
                                    fc[2].lock = True
                            else:
                                print("There are no actions on this bone to push to the new character")
        else:
            print("There is no appropriate bone data")
        return {'FINISHED'}


class SwapAnimation(Operator):                                                                                                                                                                  # Functionallity for button if the user has selected appropriate bones
    '''
    Functionallity for button if the user has selected appropriate bones
    '''
    bl_label = "Run Animation Swap"                                                                                                                                                             # bl_label
    bl_idname = "object.run_animation_swap"                                                                                                                                                     # bl_idname
    bl_description = "Swap animation for one bone to another"                                                                                                                                   # bl_description
    bl_options = {'UNDO'}                                                                                                                                                                       # bl_options

    def execute(self, context):                                                                                                                                                                 # Main fuction if user has chosen appropriate bones
        '''
        Main fuction if user has chosen appropriate bones
        '''
        main.activate(bpy.context.scene.PusherObject,bpy.context.scene.PullerObject,bpy.context.scene.PusherBone,bpy.context.scene.PullerBone)
        return {'FINISHED'}

    def invoke(self, context, event):
        '''
        Run main functionality
        '''
        return self.execute(context)


class DontSwapAnimation(Operator):
    '''
    Functionallity for if you try to run the tool without bones that are appropriate.
    '''
    bl_label = "Run Animation Swap"
    bl_idname = "object.do_not_run_animation_swap"
    bl_description = "Swap animation for one bone to another"
    bl_options = {'UNDO'}

    def execute(self, context):
        '''
        Main functionallity if the user trys to run the tool with incorect bone selection, or objects with no animation
        '''
        print("Transfer is not possible!\nPlease select different objects or bones for the transfer.")                                                                                          # Inform the user that what they are atempting is not possible with this tool
        return {'FINISHED'}

    def invoke(self, context, event):
        '''
        Run main functionality
        '''
        return self.execute(context)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.PusherObject = bpy.props.StringProperty()
    bpy.types.Scene.PullerObject = bpy.props.StringProperty()
    bpy.types.Scene.PusherBone = bpy.props.StringProperty()
    bpy.types.Scene.PullerBone = bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.Scene.PusherObject = bpy.props.StringProperty()
    bpy.types.Scene.PullerObject = bpy.props.StringProperty()
    bpy.types.Scene.PusherBone = bpy.props.StringProperty()
    bpy.types.Scene.PullerBone = bpy.props.StringProperty()

if __name__ == "__main__":
    if bpy.app.background:
        register()
    else:
        register()