bl_info = {
    "name": "Fix Hiden Bone Tool",
    "author": "Jordan Goddard",
    "version": (1, 0, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Panel > Tangent",
    "description": "Removes animation on bones that should not have keys",
    "warning": "This is a custom blender addon. USE AT OWN RISK!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Home.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import bpy
from bpy.types import Panel, Operator


class OBJECT_PT_mainGUI(bpy.types.Panel):
    '''
    Creates a panel in the 3D view tools menu under the tangent tab
    '''
    bl_label = "Remove Hiden Animation"
    bl_idname = "OBJECT_PT_mainGUI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tangent"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        row.operator("object.move_to_first_frame", text = "Reset Start Frame", icon = 'CONSTRAINT')
        row.operator("object.fix_hidden_animation", text = "Fix Broken Bones", icon = 'CONSTRAINT')


class fix_hidden_animation(Operator):
    bl_label = "Fix hiden bones"
    bl_idname = "object.fix_hidden_animation"
    bl_description = ""
    bl_options = {'UNDO'}

    def execute(self, context):
        self.gather_objects()
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

    def gather_objects(self):
        scene = bpy.data.scenes[bpy.context.scene.name]
        main_obj = None
        dest_bone = "mch.eyebrow.002.R"
        get_bone = None
        for obj in scene.objects:
            if "ozzy" in obj.name:
                if "proxy" in obj.name:
                    for bone in obj.pose.bones:
                        if "ctl" in bone.name:
                            pass
                        else:
                            action = obj.animation_data.action
                            if action != None:
                                name = bone.name
                                correct_curve = False
                                rot_typ = False
                                for fc in obj.animation_data.action.fcurves:
                                    if name in fc.data_path:
                                        if "rotation_quat" in fc.data_path:
                                            rot_typ = True
                                        correct_curve = True
                                if correct_curve == True:
                                    start_frame = scene.frame_start
                                    end_frame = scene.frame_end
                                    clearBoneAnimation(bone, "location", start_frame, end_frame)
                                    clearBoneAnimation(bone, "scale", start_frame, end_frame)
                                    if rot_typ == True:
                                        clearBoneAnimation(bone, "rotation_quaternion", start_frame, end_frame)
                                    else:
                                        clearBoneAnimation(bone, "rotation_euler", start_frame, end_frame)

    def clearBoneAnimation(bone, typ, from_frame, to_frame):
        obj = bone.id_data
        action = obj.animation_data.action
        if action is None:
            return
        name = bone.name
        fcurves = [fc for fc in action.fcurves if fc.data_path.startswith('pose.bones["%s"].%s' % (name, typ))]
        for fc in fcurves:
            frames = [kfp.co[0] for kfp in fc.keyframe_points if kfp.co[0] > from_frame and kfp.co[0] < to_frame]
            for f in frames:
                success = bone.keyframe_delete(typ, frame=f)
                print("delete %s %s %3.1f" % (name, typ, f), success)


class MoveToFrameOne(Operator):
    bl_label = "Reset Frame"
    bl_idname = "object.move_to_first_frame"
    bl_description = ""
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.data.scenes[bpy.context.scene.name].frame_current = 1
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

