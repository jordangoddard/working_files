bl_info = {
    "name": "Layout Preparation",
    "author": "Jordan Goddard",
    "version": (1, 1, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Prepare Scene for Layout",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Naming%20Tools%20for%20Layout.aspx",
    "category": "Tangent"}

import bpy

class LayoutPreparationPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Layout'
    bl_label = "Layout Preparation"

    def draw(self, context):
        render = context.scene.render

        layout = self.layout
        col = layout.column(align = False)

        row = col.row(align = True)
        row.operator("object.rename_tool", text = "Name Cleanup", icon = 'SCENE_DATA')
        row.scale_y = 1

        col.separator()                                                                                 # Add spacer
        col.separator()                                                                                 # Add spacer
        row = col.row()
        row.label(text = "Add Camera", icon = 'CAMERA_DATA')

        box = col.box()
        row = box.row(align = True)                                                                     # UI text
        row.operator(operator = "object.create_cam_fcs", text = "[cam][fcs]", icon = "OUTLINER_OB_CAMERA")
        row = box.row(align = True)   
        row.operator(operator = "object.create_cam_fcs_lkt", text = "[cam][fcs][lkt]", icon = "OUTLINER_OB_EMPTY")


class RepairNameTool(bpy.types.Operator):
    bl_idname = "object.rename_tool"
    bl_label = "Rename Tool"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        print("\n\nCleaning up camera names\n\n")
        item_prefix_cam = ["cam", "Cam", "CAM"]
        item_prefix_lkt = ["lkt", "Lkt", "LKT", "LOO", "loo"]
        item_prefix_fcs = ["fcs", "Fcs", "FCS", "FOC", "foc"]
        for scene in bpy.data.scenes:
            for obj in bpy.data.scenes[scene.name].objects:
                if obj.name.startswith(tuple(item_prefix_cam)):
                    obj.name = "cam.%s"%scene.name
                if obj.name.startswith(tuple(item_prefix_lkt)):
                    obj.name = "lkt.%s"%scene.name
                if obj.name.startswith(tuple(item_prefix_fcs)):
                    obj.name = "fcs.%s"%scene.name
            print("Naming change complete for %s"%scene.name)
        print("\n\nProgram Complete!\n\n")
        return {"FINISHED"}


class RenderSettingsTool(bpy.types.Operator):
    bl_idname = "object.set_up_render"
    bl_label = "Set_Render_Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        print('Set_Render_Settings Working')
        scene = bpy.context.scene
        render = bpy.data.scenes[scene.name].render
        render.stamp_font_size = 17
        render.stamp_background = (0,0,0,1)
        render.use_stamp = True
        render.use_stamp_time = False
        render.use_stamp_date = False
        render.use_stamp_render_time = False
        render.use_stamp_frame = True
        render.use_stamp_scene = True
        render.use_stamp_camera = False
        render.use_stamp_lens = True
        render.use_stamp_filename = False
        render.use_stamp_marker = False
        render.resolution_x = 1920
        render.resolution_y = 1080
        render.resolution_percentage = 50
        render.use_stamp_sequencer_strip = False
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'QUICKTIME'
        render.ffmpeg.codec = 'MPEG4'
        render.ffmpeg.audio_codec = 'PCM'
        return{'FINISHED'}


class CreateCamFcsLkt(bpy.types.Operator):
    bl_idname = "object.create_cam_fcs_lkt"
    bl_label = "Create [Cam][Fcs][Lkt]"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        print('Create_Cam_Fcs_Lkt Working')
        scene = bpy.context.scene
        object = bpy.data.objects
        cam_data = bpy.data.cameras.new(name = "cam." + scene.name)
        cam_obj = object.new(name = "cam." + scene.name, object_data = cam_data)
        scene.objects.link(cam_obj)
        bpy.ops.object.add(type='EMPTY')
        bpy.context.active_object.name = "fcs." + scene.name
        bpy.ops.object.add(type='EMPTY')
        bpy.context.active_object.name = "lkt." + scene.name
        cam_obj.data.dof_object = bpy.data.objects["fcs." + scene.name]
        scene.camera = object["cam." + scene.name]
        bpy.context.scene.objects.active = bpy.data.objects["cam." + scene.name]
        bpy.ops.object.constraint_add(type='TRACK_TO')
        context.object.constraints["Track To"].target = bpy.data.objects["lkt." + scene.name]
        context.object.constraints["Track To"].up_axis = 'UP_Y'
        context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        return{'FINISHED'}


class CreateCamFcs(bpy.types.Operator):
    bl_idname = "object.create_cam_fcs"
    bl_label = "Create [Cam][Fcs]"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        print('Create_Cam_Fcs Working')
        scene = bpy.context.scene
        object = bpy.data.objects
        cam_data = bpy.data.cameras.new(name = "cam." + scene.name)
        cam_obj = object.new(name = "cam." + scene.name, object_data = cam_data)
        scene.objects.link(cam_obj)
        bpy.ops.object.add(type='EMPTY')
        bpy.context.active_object.name = "fcs." + scene.name
        cam_obj.data.dof_object = bpy.data.objects["fcs." + scene.name]
        scene.camera = object["cam." + scene.name]
        return{'FINISHED'}

def register():
    """ Register classes """
    bpy.utils.register_module(__name__)
    
def unregister():
    """ Unregister classes """
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()