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


class OBJECT_PT_mainGUI(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Swap Animation Tool"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tangent"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row1 = layout.row()
        row2 = layout.row()
        col1 = row1.column()
        col2 = row1.column()
        row3 = layout.row()
        scene = context.scene
        col1.prop_search(scene, "PusherObject", scene, "objects")
        col2.prop_search(scene, "PullerObject", scene, "objects")
        if "proxy" in bpy.context.scene.PusherObject:
            col1.prop_search(scene, "PusherBone", bpy.data.scenes[scene.name].objects[bpy.context.scene.PusherObject].pose, "bones")
        if "proxy" in bpy.context.scene.PullerObject:
            col2.prop_search(scene, "PullerBone", bpy.data.scenes[scene.name].objects[bpy.context.scene.PullerObject].pose, "bones")
        try:
            push_bone = bpy.data.scenes[scene.name].objects[bpy.context.scene.PusherObject].pose.bones[bpy.context.scene.PusherBone]
            pull_bone = bpy.data.scenes[scene.name].objects[bpy.context.scene.PullerObject].pose.bones[bpy.context.scene.PullerBone]
        except:
            row3.operator("object.do_not_run_animation_swap", text = "Select Appropriate Bones", icon = 'CONSTRAINT')
        else:
            row3.operator("object.run_animation_swap", text = "Swap Animation", icon = 'CONSTRAINT')


class main(object):
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


class SwapAnimation(Operator):
    bl_label = "Run Animation Swap"
    bl_idname = "object.run_animation_swap"
    bl_description = "Swap animation for one bone to another"
    bl_options = {'UNDO'}

    def execute(self, context):
        main.activate(bpy.context.scene.PusherObject,bpy.context.scene.PullerObject,bpy.context.scene.PusherBone,bpy.context.scene.PullerBone)
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class DontSwapAnimation(Operator):
    bl_label = "Run Animation Swap"
    bl_idname = "object.do_not_run_animation_swap"
    bl_description = "Swap animation for one bone to another"
    bl_options = {'UNDO'}

    def execute(self, context):
        print("Transfer is not possible!\nPlease select different objects or bones for the transfer.")
        return {'FINISHED'}

    def invoke(self, context, event):
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