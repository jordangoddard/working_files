bl_info = {
    "name": "Shot Finaler",
    "author": "Wayne Wu",
    "version": (1, 2, 3),
    "blender": (2, 74, 0),
    "location": "View3D > Tools",
    "description": "Check the shot before passing to lightings",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Shot%20Finaler.aspx",
    "category": "Tangent"}
        
import bpy
from bpy.props import BoolProperty
 
class ShotFinalingGUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Shot Finaler"
    bl_category = "TA - Finaling"


    bpy.types.Scene.shot_final_fix = BoolProperty(name = "Auto-correct issues", default = False)
    bpy.types.Scene.shot_final_save = BoolProperty(name = "Auto-save file to Sandbox", default = False)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text = "Verifies the integrity of")
        col.label(text = "the scene and optionally")
        col.label(text = "corrects issues.")

        row = col.row()
        row.label("")

        row = col.row(align = True)
        row.prop(context.scene, "shot_final_fix" ) 
 
        """ 
        REQ hgagne: David Russel, Mon 2015-11-30 12:38 PM
        It would be great if you could remove the save tick. We will never use it, and I dont want people helping to use it.
        """

        # row = col.row()
        # row.label("")
        # 
        # row = col.row(align = True)
        # row.prop(context.scene, "shot_final_save")   

        row = col.row()
        row.label("")

        row = col.row(align = True)
        row.operator("scene.shot_finalize", text = "RUN", icon = 'FILE_TICK')
        row.scale_y = 1


class ShotFinalingButton(bpy.types.Operator):
    bl_idname = "scene.shot_finalize"
    bl_label = "ADD"
    bl_options = {"UNDO"}
    
    def invoke(self, context, event):
        from imp import reload
        import shot_finaling
        reload(shot_finaling)
        cs = shot_finaling.CheckShot(bpy.context.scene.shot_final_fix, bpy.context.scene.shot_final_save)
        cs.check_all()
            
        return {"FINISHED"}

def register():
    bpy.utils.register_class(ShotFinalingGUI)
    bpy.utils.register_class(ShotFinalingButton)

def unregister():
    bpy.utils.unregister_class(ShotFinalingGUI)
    bpy.utils.unregister_class(ShotFinalingButton)
    
if __name__ == "__main__":
    register()