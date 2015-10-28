bl_info = {
    "name": "Tangent: Shot Finaling",
    "author": "Wayne Wu",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tools > Tangent",
    "description": "Check the shot before passing to lightings",
    "warning": "",
    "wiki_url": "",
    "category": "Shot Finaling"}
        
import bpy
from bpy.props import BoolProperty
 
class ShotFinalingGUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tangent'
    bl_label = "Shot Finaling"
    
    bpy.types.Scene.shot_final_fix = BoolProperty(name = "Fix", default = False)
    bpy.types.Scene.shot_final_save = BoolProperty(name = "Save to Sandbox", default = False)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        row.operator("scene.shot_finalize", text = "RUN", icon = 'FILE_TICK')
        row.scale_y = 2  
        row2 = col.row()
        row2.label("Options")
        row3 = col.row(align = True)
        row3.prop(context.scene, "shot_final_fix" ) 
        row4 = col.row(align = True)
        row4.prop(context.scene, "shot_final_save")      
        
class ShotFinalingButton(bpy.types.Operator):
    bl_idname = "scene.shot_finalize"
    bl_label = "ADD"
    bl_options = {"UNDO"}
    
    def invoke(self, context, event):
        import shot_finaling
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