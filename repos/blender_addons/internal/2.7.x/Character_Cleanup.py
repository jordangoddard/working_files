bl_info = {
    "name": "Tangent: Character Cleanup",
    "author": "Wayne Wu",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Tools > Character Tools",
    "description": "Character Cleanup",
    "warning": "",
    "wiki_url": "",
    "category": "Character Tools"}


import bpy

class CharacterCleanUpGUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Character Tools'
    bl_label = "Character Clean Up"
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        row.operator("object.character_add_dummy", text = "Add Dummy Modifier", icon = 'POSE_DATA')
        row.scale_y = 1
        row2 = col.row(align = True)
        row2.operator("object.character_remove_dependencies", text = "Clear Dependencies", icon = 'X')
        row2.scale_y = 1
        
class AddDummy(bpy.types.Operator):
    bl_idname = "object.character_add_dummy"
    bl_label = "Character_Add_Dummy"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        put_dummy()
            
        return {"FINISHED"}
        
class RemoveDependency(bpy.types.Operator):
    bl_idname = "object.character_remove_dependencies"
    bl_label = "Character_Remove_Dependencies"
    bl_options = {"UNDO"}
    
    def invoke(self, context, event):
        
        error_list = remove_dependencies()
        if error_list:
            for error in error_list: 
                self.report({'ERROR'}, error)
        return {"FINISHED"}

def put_dummy():
    """
    Add a dummy simpledeform modifier at the end of every mesh 
    """
    mesh_list = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers: 
                if modifier.type == 'SUBSURF' or modifier.type == 'MULTIRES':
                    mesh_list.append(obj)
                    break
     
    for obj in mesh_list: 
        index = len(obj.modifiers) - 1
        if not obj.modifiers[index].type == 'SIMPLE_DEFORM': 
            simple_deform = obj.modifiers.new("SimpleDeform_Dummy", 'SIMPLE_DEFORM')
            simple_deform.limits[0] = 0
            simple_deform.limits[1] = 0
            simple_deform.angle = 0
            
def remove_dependencies():

    """
    Remove all dependencies at the armature level
    """
    error =[]
    for armature in bpy.data.armatures: 
        if armature.name.startswith('rig'):
            try: 
                armature.animation_data
            except: 
                print("ERROR: no animation data(driver)")
            else:
                try:
                    for d in armature.animation_data.drivers:
                        if d.data_path.endswith('.hide') or d.data_path.endswith('.bbone_in') or d.data_path.endswith('.bbone_out'):
                            try:
                                armature.driver_remove(d.data_path)
                                #print("%s removed" %d.data_path)
                            except TypeError: #driver path is broken
                                for var in d.driver.variables:
                                    d.driver.variables.remove(var)
                                d.data_path = 'bones[\"ctl.god.C\"].hide'      #change data_path target to ctl.god.C so that it's deletable                
                                armature.driver_remove(d.data_path)              
                        else:
                            error.append("Driver(Armature %s) pointed to %s will not be removed" %(armature.name, d.data_path)) 
                except AttributeError: 
                    print("No driver")
                for layer in armature.layers: 
                   layer = True
                try: 
                    for b in bpy.data.objects[armature.name].pose.bones:
                        b.bone.hide = False
                except KeyError:
                    pass                
                i = 0
                while (i < 32):
                    if 7 < i < 16 or i > 23:
                        armature.layers[i] = False
                    i = i + 1  
    for obj in bpy.data.objects: 
        if obj.name.startswith('rig'):
            try:
                for d in obj.animation_data.drivers:
                    if not d.is_valid:
                        error.append("Driver(Object %s) Datapath %s is broken" %(obj.name, d.data_path))      
            except AttributeError: 
                pass
    return error
                    
def register():
    bpy.utils.register_class(CharacterCleanUpGUI)
    bpy.utils.register_class(AddDummy)
    bpy.utils.register_class(RemoveDependency)

def unregister():
    bpy.utils.unregister_class(CharacterCleanUpGUI)
    bpy.utils.unregister_class(AddDummy)
    bpy.utils.unregister_class(RemoveDependency)
    
if __name__ == "__main__":
    register()            