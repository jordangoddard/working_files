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


class OBJECT_PT_mainGUI(bpy.types.Panel):  # Main GUI of Animation Mover Tool
    '''
    Main GUI of Animation Mover Tool
    '''
    bl_label = "Swap Animation Tool"
    bl_idname = "OBJECT_swap_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tangent"

    def draw(self, context):  # Draw functionality, where the graphics are created and displayed to the user
        '''
        Draw functionality, where the graphics are created and displayed to the user
        '''
        layout = self.layout
        row1 = layout.row()
        row2 = layout.row()
        row3 = layout.row()
        row4 = layout.row()
        row5 = layout.row()
        scene = context.scene
        row1.enabled = True
        row1.prop_search(scene, "SourceObject", scene, "objects")  # List of objects to pull animation from
        row2.enabled = False
        if "proxy" in bpy.context.scene.SourceObject:
            row2.enabled = True
            row2.prop_search(scene, "SourceBone", bpy.data.scenes[scene.name].objects[bpy.context.scene.SourceObject].pose, "bones")  # List of all bones for selected object to pull animation from
        else:
            row2.enabled = False
            row2.prop_search(scene, "SourceBone", scene, "objects")
        row3.enabled = True
        row3.prop_search(scene, "TargetObject", scene, "objects")  # List of objects to push animation to
        row4.enabled = False
        if "proxy" in bpy.context.scene.TargetObject:
            row4.enabled = True
            row4.prop_search(scene, "TargetBone", bpy.data.scenes[scene.name].objects[bpy.context.scene.TargetObject].pose, "bones")  # List of all bones for selected object to push animation to
        else:
            row4.enabled = False
            row4.prop_search(scene, "TargetBone", scene, "objects")
        try:
            push_bone = bpy.data.scenes[scene.name].objects[bpy.context.scene.SourceObject].pose.bones[bpy.context.scene.SourceBone]  # Check if the selected pulling bone is actually in the pulling object
            pull_bone = bpy.data.scenes[scene.name].objects[bpy.context.scene.TargetObject].pose.bones[bpy.context.scene.TargetBone]  # Check if the selected pushing bone is actually in the pushing object
        except:
            row5.enabled = False
            row5.operator("object.do_not_run_animation_swap", text = "Can't Swap Animation", icon = 'CONSTRAINT')  # Show button that shows that the selected bones are not in their given objects
        else:
            row5.enabled = False
            if "proxy" in bpy.context.scene.SourceObject:
                if "proxy" in bpy.context.scene.TargetObject:
                    row5.enabled = True
                else:
                    row5.enabled = False
            else:
                row5.enabled = False
            row5.operator("object.run_animation_swap", text = "Swap Animation", icon = 'CONSTRAINT')  # Button to move animation from the pulling bone to the pushing bone


class main(object):  # Functionality for moving animation from selected bone to selected bone, and create a custom datablock for the new action
    '''
    Functionality for moving animation from selected bone to selected bone, and create a custom datablock for the new action
    '''
    bl_label = "main"
    bl_idname = "object.main_function"
    bl_description = "run main functionality of button"
    bl_options = {'UNDO'}

    def activate(source_object,target_object,source_bone,target_bone):
        print("Transfering data from %s:%s to %s:%s"%(source_object,target_object,source_bone,target_bone))
        run_variable = False
        if source_object and target_object and source_bone and target_bone:
            run_variable = True
        if run_variable:
                        scene = bpy.context.scene
                        obj_list = []
                        source_obj = None
                        target_obj = None
                        print("\n\n")
                        for obj in bpy.data.scenes[scene.name].objects:
                            if source_object in obj.name:
                                source_obj = obj
                            if target_object in obj.name:
                                target_obj = obj
                        try:
                            anim = source_obj.animation_data.action.copy()                    # get action
                        except:
                            print("There are no actions on this bone to push to the new character")
                        else:
                            if anim:
                                target_obj.animation_data.action = anim                    # set action
                                print(anim.name)
                                try:
                                    fc = target_obj.animation_data.action.fcurves
                                except:
                                    print("The action on this bone has no animation data")
                                else:
                                    print("Moving animation")
                                    fc[0].lock = False
                                    fc[0].data_path = 'pose.bones["%s"].location'%target_bone
                                    fc[0].array_index = 0
                                    fc[0].lock = True
                                    fc[1].lock = False
                                    fc[1].data_path = 'pose.bones["%s"].location'%target_bone
                                    fc[1].array_index = 1
                                    fc[1].lock = True
                                    fc[2].lock = False
                                    fc[2].data_path = 'pose.bones["%s"].location'%target_bone
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
        main.activate(bpy.context.scene.SourceObject,bpy.context.scene.TargetObject,bpy.context.scene.SourceBone,bpy.context.scene.TargetBone)
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
    bpy.types.Scene.SourceObject = bpy.props.StringProperty()
    bpy.types.Scene.TargetObject = bpy.props.StringProperty()
    bpy.types.Scene.SourceBone = bpy.props.StringProperty()
    bpy.types.Scene.TargetBone = bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.Scene.SourceObject = bpy.props.StringProperty()
    bpy.types.Scene.TargetObject = bpy.props.StringProperty()
    bpy.types.Scene.SourceBone = bpy.props.StringProperty()
    bpy.types.Scene.TargetBone = bpy.props.StringProperty()

if __name__ == "__main__":
    if bpy.app.background:
        register()
    else:
        register()