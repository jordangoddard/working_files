bl_info = {
    "name": "Character Animation Cleanup",
    "author": "Jordan Goddard",
    "version": (1, 0, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tools",
    "description": "description",
    "warning": "This is a custom blender addon. USE AT OWN RISK!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Home.aspx",
    "category": "Tangent"}

import bpy
from bpy.types import Panel, Operator


class OBJECT_PT_mainGUI(bpy.types.Panel):  # Main GUI of Animation Mover Tool
    '''
    Main GUI of Animation Mover Tool
    '''
    bl_label = "Character Animation Cleanup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "TA - Animation"

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

        row1.label("Select a Character Proxy")
        row2.enabled = True
        row2.prop_search(scene, "MainObject", scene, "objects")  # List of objects to pull animation from
        row3.enabled = False
        if "proxy" in bpy.context.scene.MainObject:
            row3.enabled = True
            row3.operator("object.repair_character_animation", text = "Clean Character Animation", icon = 'CONSTRAINT')
        else:
            row3.enabled = False
            row3.operator("object.repair_character_animation", text = "Clean Character Animation", icon = 'CONSTRAINT')

        row4.label("Clean All Animations")
        row5.enabled = True
        row5.operator("object.repair_all_animation", text = "Clean All Animation", icon = 'CONSTRAINT')


class RepairCharacterAnimation(Operator):
    '''
    Functionallity for button if the user has selected appropriate bones
    '''
    bl_label = "Run Character Animation Swap"
    bl_idname = "object.repair_character_animation"
    bl_description = "..."
    bl_options = {'UNDO'}

    def execute(self, context):                                                                                                                                                                 # Main fuction if user has chosen appropriate bones
        '''
        Main fuction
        '''
        scene = bpy.data.scenes[bpy.context.scene.name]
        obj = scene.objects[bpy.context.scene.MainObject]
        try:
            act = obj.animation_data.action
        except:
            print("There is no action")
        else:
            try: 
                for fc in act.fcurves:
                    if "ctl" in fc.data_path:
                        pass
                    else:
                        act.fcurves.remove(fc)
            except: 
                print("There is no fcurves")
        return {'FINISHED'}

    def invoke(self, context, event):
        '''
        Run main functionality
        '''
        return self.execute(context)


class RepairAllAnimation(Operator):
    '''
    Functionallity for if you try to run the tool without bones that are appropriate.
    '''
    bl_label = "Run Animation Swap"
    bl_idname = "object.repair_all_animation"
    bl_description = "..."
    bl_options = {'UNDO'}

    def execute(self, context):
        '''
        Main function
        '''
        for scene in bpy.data.scenes:
            for obj in scene.objects:
                if "prox" in obj.name:
                    try:
                        act = obj.animation_data.action
                    except:
                        print("There is no action")
                    else:
                        try: 
                            for fc in act.fcurves:
                                if "ctl" in fc.data_path:
                                    pass
                                else:
                                    act.fcurves.remove(fc)
                        except: 
                            print("There is no fcurves")

        return {'FINISHED'}

    def invoke(self, context, event):
        '''
        Run main functionality
        '''
        return self.execute(context)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.MainObject = bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.Scene.MainObject = bpy.props.StringProperty()

if __name__ == "__main__":
    if bpy.app.background:
        register()
    else:
        register()