bl_info = {
    "name": "Repair God",
    "author": "Jordan Goddard",
    "version": (1, 0, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Panel > Tangent",
    "description": "Moves animation from one object bone to another",
    "warning": "This is a custom blender addon. USE AT OWN RISK!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Home.aspx",
    "tracker_url": "",
    "category": "Tangent"}
import datetime
import math
import mathutils
import re
from bpy.types import Panel, Operator, PropertyGroup, UIList
import bpy

#master_data = ("This is a chunck of global data")
bpy.types.Scene.stored_data1 = bpy.props.StringProperty(name= "stored data 1")
bpy.types.Scene.stored_data2 = bpy.props.StringProperty(name= "stored data 2")
bpy.types.Scene.stored_data3 = bpy.props.StringProperty(name= "stored data 3")
bpy.types.Scene.stored_data4 = bpy.props.StringProperty(name= "stored data 4")

class sendingListObject(bpy.types.Operator):
    bl_label = "Sending List Object"
    bl_idname = "object.sending_list_object"
    bl_description = "Sending Lists"
    bl_options = {'UNDO'}

    def __init__(self):
        pass

    def proxy_list(self, context):
        dropdown_items = []
        dropdown_items.clear()
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            name = obj.name
            dropdown_items.append((name,name,name))
        return dropdown_items

    scene_proxy_list = bpy.props.EnumProperty(items=proxy_list)

    def execute(self, context):
        selected_object = self.scene_proxy_list
        bpy.context.scene.stored_data1 = selected_object
        temp_items = []
        temp_items.clear()
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            temp_items.append("%s"%obj.name)
        self.scene_proxy_list
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class recievingListObject(bpy.types.Operator):
    bl_label = "Recieving List Object"
    bl_idname = "object.recieving_list_object"
    bl_description = "Recieving Lists"
    bl_options = {'UNDO'}

    def __init__(self):
        pass

    def proxy_list(self, context):
        dropdown_items = []
        dropdown_items.clear()
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            name = obj.name
            dropdown_items.append((name,name,name))
        return dropdown_items

    scene_proxy_list = bpy.props.EnumProperty(items=proxy_list) 

    def execute(self, context):
        selected_object = self.scene_proxy_list
        bpy.context.scene.stored_data2 = selected_object
        temp_items = []
        temp_items.clear()
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            temp_items.append("%s"%obj.name)
        self.scene_proxy_list
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class sendingListBone(bpy.types.Operator):
    bl_label = "Sending List Bone"
    bl_idname = "object.sending_list_bone"
    bl_description = "Sending Bone"
    bl_options = {'UNDO'}

    def __init__(self):
        pass

    def proxy_list(self, context):
        dropdown_items = []
        dropdown_items.clear()
        for bone in bpy.data.scenes[bpy.context.scene.name].objects[bpy.context.scene.stored_data1].pose.bones:
            name = bone.name
            dropdown_items.append((name,name,name))
        return dropdown_items

    scene_proxy_list = bpy.props.EnumProperty(items=proxy_list) 

    def execute(self, context):
        selected_object = self.scene_proxy_list
        bpy.context.scene.stored_data3 = selected_object
        temp_items = []
        temp_items.clear()
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            temp_items.append("%s"%obj.name)
        self.scene_proxy_list
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class recievingListBone(bpy.types.Operator):
    bl_label = "Recieving List Bone"
    bl_idname = "object.recieving_list_bone"
    bl_description = "Recieving Bone"
    bl_options = {'UNDO'}

    def __init__(self):
        pass

    def proxy_list(self, context):
        dropdown_items = []
        dropdown_items.clear()
        for bone in bpy.data.scenes[bpy.context.scene.name].objects[bpy.context.scene.stored_data2].pose.bones:
            name = bone.name
            dropdown_items.append((name,name,name))
        return dropdown_items

    scene_proxy_list = bpy.props.EnumProperty(items=proxy_list) 

    def execute(self, context):
        selected_object = self.scene_proxy_list
        bpy.context.scene.stored_data4 = selected_object
        temp_items = []
        temp_items.clear()
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            temp_items.append("%s"%obj.name)
        self.scene_proxy_list
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class SwapAnimation(Operator):
    bl_label = "Run Animation Swap"
    bl_idname = "object.run_animation_swap"
    bl_description = "Swap animation for one bone to another"
    bl_options = {'UNDO'}

    def execute(self, context):
        sen_obj = bpy.context.scene.stored_data1
        rec_obj = bpy.context.scene.stored_data2
        sen_bon = bpy.context.scene.stored_data3
        rec_bon = bpy.context.scene.stored_data4
        #print("%s"%master_data)
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

    def invoke(self, context, event):
        return self.execute(context)


class AnimationMoverGUI(bpy.types.Panel):                                                                       # GUI
    bl_label= "God Animation Repair"
    bl_idname = "object.mainGUI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tangent"
    #bpy.types.Scene.stored_data1 = bpy.props.StringProperty(name= "stored data 1")
    #bpy.types.Scene.stored_data2 = bpy.props.StringProperty(name= "stored data 2")
    #bpy.types.Scene.stored_data4 = bpy.props.StringProperty(name= "stored data 3")
    #bpy.types.Scene.stored_data6 = bpy.props.StringProperty(name= "stored data 4")

    def check_validity(self, obj, bone):
        check = False
        for b in bpy.data.scenes[bpy.context.scene.name].objects[obj].pose.bones:
            if b.name == bone:
                check = True
        return check

    def execute(self, context):
        data_object = self.d_list
        bpy.context.scene.stored_data1 = data_object

    def draw(self, context):                                                                                           # GUI
        layout = self.layout
        row1 = layout.row()
        row1col1 = row1.column()
        row1col2 = row1.column()
        row1col1.label(text="From Object")
        row1col2.label(text="To Object")
        row2 = layout.row()
        valid_object = False
        try:
            if bpy.context.scene.stored_data1 == "":
                row1col1.operator_menu_enum("object.sending_list_object", "scene_proxy_list", text = "Select Controller", icon = 'OBJECT_DATA')
            else:
                row1col1.operator_menu_enum("object.sending_list_object", "scene_proxy_list", text = bpy.context.scene.stored_data1, icon = 'OBJECT_DATA')
        except:
            row1col1.operator_menu_enum("object.sending_list_object", "scene_proxy_list", text = "Select Controller", icon = 'OBJECT_DATA')
        else:
            try:
                valid_object = self.check_validity(bpy.context.scene.stored_data1, bpy.context.scene.stored_data3)
            except:
                row1col1.label(text="From Bone")
                row1col1.operator_menu_enum("object.sending_list_bone", "scene_proxy_list", text = "No Bones", icon = 'BONE_DATA')
            else:
                if valid_object == True:
                    if "proxy" in bpy.context.scene.stored_data1:
                        row1col1.label(text="From Bone")
                        row1col1.operator_menu_enum("object.sending_list_bone", "scene_proxy_list", text = bpy.context.scene.stored_data3, icon = 'BONE_DATA')
                elif valid_object == False:
                    row1col1.label(text="From Bone")
                    row1col1.operator_menu_enum("object.sending_list_bone", "scene_proxy_list", text = "Select Bone", icon = 'BONE_DATA')
        try:
            if bpy.context.scene.stored_data2 == "":
                row1col2.operator_menu_enum("object.recieving_list_object", "scene_proxy_list", text = "Select Controller", icon = 'OBJECT_DATA')
            else:
                row1col2.operator_menu_enum("object.recieving_list_object", "scene_proxy_list", text = bpy.context.scene.stored_data2, icon = 'OBJECT_DATA')
        except:
            row1col2.operator_menu_enum("object.recieving_list_object", "scene_proxy_list", text = "Select Controller", icon = 'OBJECT_DATA')
        else:
            try:
                valid_object = self.check_validity(bpy.context.scene.stored_data2, bpy.context.scene.stored_data4)
            except:
                row1col2.label(text="From Bone")
                row1col2.operator_menu_enum("object.recieving_list_bone", "scene_proxy_list", text = "No Bones", icon = 'BONE_DATA')
            else:
                if valid_object == True:
                    if "proxy" in bpy.context.scene.stored_data1:
                        row1col2.label(text="From Bone")
                        row1col2.operator_menu_enum("object.recieving_list_bone", "scene_proxy_list", text = bpy.context.scene.stored_data4, icon = 'BONE_DATA')
                elif valid_object == False:
                    row1col2.label(text="From Bone")
                    row1col2.operator_menu_enum("object.recieving_list_bone", "scene_proxy_list", text = "Select Bone", icon = 'BONE_DATA')
        row2.operator("object.run_animation_swap", text = "Swap Animation", icon = 'CONSTRAINT')


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    if bpy.app.background:
        register()
    else:
        register()


