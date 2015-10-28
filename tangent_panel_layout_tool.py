bl_info = {
    "name": "Tangent: Naming Tools for Layout",
    "author": "Jordan Goddard",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Tools > Tangent",
    "description": "Naming Tools for Layout",
    "warning": "",
    "wiki_url": "",
    "category": "Tangent"}

import bpy

class RepairNameToolGUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tangent'
    bl_label = "Name Repair"
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        row.operator("object.rename_tool", text = "Run Name Repair", icon = 'POSE_DATA')
        row.scale_y = 1

class RepairNameTool(bpy.types.Operator):
    bl_idname = "object.rename_tool"
    bl_label = "Rename Tool"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        print("\n\n\n\n\n\nRunning Camera Name Fix Tool\n\n\n\n\n\n")
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
        print("\n\n\n\n\n\nProgram Complete!\n\n\n\n\n\n")
        return {"FINISHED"}

class PlayblastToolGUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tangent'
    bl_label = "Layout"
    bl_idname = "object.playblast_tool"
    bl_label = "Playblast Settings"
    def draw(self, context):
        camera_here = False
        item_prefix_cam = ["cam", "Cam", "CAM"]
        for obj in bpy.data.scenes[bpy.context.scene.name].objects:
            if obj.name.startswith(tuple(item_prefix_cam)):
                camera_here = True
        layout = self.layout
        render = bpy.context.scene.render
        cam = context.scene.camera
        camdata = cam.data
        dof = camdata.gpu_dof
        if camera_here:
            row = layout.row()
            row.operator(operator = "render.test_playblast", text=" Test PB Settings [ON][OFF]", icon='SCRIPT')
            row = layout.row()
            row.operator(operator = "render.dof_playblast", text=" Dof PB Setting [ON][OFF]", icon='SCRIPT')
            row = layout.row()
            row.operator(operator = "object.set_up_render", text = "Set Render Settings", icon = "SCRIPT")
            row = layout.row()
            row.label(text = "Render Output Path")
            layout.prop(render, "filepath", text="")
            row = layout.row()
        else:
            row.label(text = "You must have a Camera for this tool")

class RenderSettingsTool(bpy.types.Operator):
    bl_idname = "object.set_up_render"
    bl_label = "Set_Render_Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        print('Set_Render_Settings Working')
        render = bpy.context.scene.render
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
        render.use_stamp_sequencer_strip = False
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'QUICKTIME'
        render.ffmpeg.codec = 'MPEG4'
        render.ffmpeg.audio_codec = 'PCM'
        return{'FINISHED'}

class PlayblastTestTool(bpy.types.Operator):
    bl_idname = "render.test_playblast"
    bl_label = "test_playblast"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        print('Playblast_Test Working ')
        data = context.space_data
        if data.show_only_render == False:
            data.show_only_render = True
        else:
            data.show_only_render = False
        return{'FINISHED'}

class PlayblastDofTool(bpy.types.Operator):
    bl_idname = "render.dof_playblast"
    bl_label = "dof_playblast"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        print('Playblast_Dof Working ')
        data = context.space_data
        cam = context.scene.camera
        camdata = cam.data
        if data.show_only_render == False:
            data.show_only_render = True
        else:
            data.show_only_render = False
        return{'FINISHED'}

class CameraSettingsToolGUI(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tangent'
    bl_label = "Layout"
    bl_idname = "object.scene_setup"
    bl_label = "Camera Settings"

    def draw(self, context):
        layout = self.layout
        render = context.scene.render
        row = layout.row()
        row.label(text = "Make Camera")
        row = layout.row()
        row.operator(operator = "object.create_cam_fcs", text = "[cam][fcs]", icon = "PLUS")
        row = layout.row()
        row.operator(operator = "object.create_cam_fcs_lkt", text = "[cam][fcs][lkt]", icon = "PLUS")
        row = layout.row()

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
    bpy.utils.register_class(RepairNameToolGUI)
    bpy.utils.register_class(RepairNameTool)
    bpy.utils.register_class(PlayblastToolGUI)
    bpy.utils.register_class(PlayblastTestTool)
    bpy.utils.register_class(PlayblastDofTool)
    bpy.utils.register_class(CreateCamFcs)
    bpy.utils.register_class(CreateCamFcsLkt)
    bpy.utils.register_class(CameraSettingsToolGUI)
    bpy.utils.register_class(RenderSettingsTool)

def unregister():
    bpy.utils.register_class(RepairNameToolGUI)
    bpy.utils.register_class(RepairNameTool)
    bpy.utils.register_class(PlayblastToolGUI)
    bpy.utils.register_class(PlayblastTestTool)
    bpy.utils.register_class(PlayblastDofTool)
    bpy.utils.register_class(CreateCamFcs)
    bpy.utils.register_class(CreateCamFcsLkt)
    bpy.utils.register_class(CameraSettingsToolGUI)
    bpy.utils.register_class(RenderSettingsTool)
    
    
if __name__ == "__main__":
    register()            
                
        
   