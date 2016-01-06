bl_info = {
    "name": "Snapping Tool",
    "author": "Wayne Wu",
    "version": (1, 1, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Snapping Tool (Read Wiki for more info)",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url" : "https://tangentanimation.sharepoint.com/wiki/Pages/Snapping%20Tool.aspx",
    "category": "Tangent"}


import bpy 
from bpy.types import Scene, Panel, PropertyGroup, Operator
from bpy.props import FloatVectorProperty, PointerProperty, StringProperty

class TransformationData(PropertyGroup):
    
    def get_location(self):
        if bpy.context.active_object:
            if bpy.context.active_object.mode == 'POSE':
                item = bpy.context.active_pose_bone
            else: 
                item = bpy.context.active_object            
            vector = item.matrix_world.to_translation()
            return vector
        return ((0,0,0))
    
    def get_scale(self):
        if bpy.context.active_object:
            if bpy.context.active_object.mode == 'POSE':
                item = bpy.context.active_pose_bone
            else: 
                item = bpy.context.active_object
            vector = item.matrix_world.to_scale()
            return vector
        return ((1,1,1))
    
    def get_rotation(self):
        if bpy.context.active_object:
            if bpy.context.active_object.mode == 'POSE':
                item = bpy.context.active_pose_bone
            else: 
                item = bpy.context.active_object
            euler = item.matrix_world.to_euler()
            return euler
        return ((0.0,0.0,0.0))
    
    #Absolute Transformation (Read-Only)
    abs_location = FloatVectorProperty(get = get_location, precision=9)
    abs_scale = FloatVectorProperty(get = get_scale, precision = 9)
    abs_rotation = FloatVectorProperty(get = get_rotation, precision = 9, subtype = 'EULER')
    
    #Stored Transformation
    stored_location = FloatVectorProperty(name = "Stored Location", precision=9)
    stored_scale = FloatVectorProperty(name = "Stored Scale", precision = 9)
    stored_rotation = FloatVectorProperty(name = "Stored Rotation", precision = 9, subtype = 'EULER')
    
    #Other useful detail that may be needed
    stored_context_mode = StringProperty(name = "Stored Context Mode")
    stored_context_object = StringProperty(name = "Stored Object Name")
    

class SnappingToolProperties(PropertyGroup):

    
    def get_matrix(self):
        """
        Retrieve the absolute location of the bone
        """
        list = []
        matrix_world = self.id_data.matrix_world*self.matrix
        for col in matrix_world.col:
            for num in col: 
                list.append(num)
        return tuple(list)
    
    
    def set_matrix(self, value):
        """
        When setting the matrix, it will set the relative matrix instead
        """
        from mathutils import Matrix
        col1 = (value[0], value[4], value[8], value[12])
        col2 = (value[1], value[5], value[9], value[13])
        col3 = (value[2], value[6], value[10], value[14])
        col4 = (value[3], value[7], value[11], value[15])
        global_matrix = Matrix((col1, col2, col3, col4))
        
        #Matrix Inverse
        inverse_matrix = self.id_data.matrix_world.inverted()
        relative_matrix = inverse_matrix*global_matrix
        self.matrix = relative_matrix
        

    bpy.types.PoseBone.matrix_world = FloatVectorProperty(name = "Stored Matrix", subtype = 'MATRIX', size = 16, get = get_matrix, set = set_matrix)
    
    try: 
        bpy.utils.register_class(TransformationData)
    except: pass
    bpy.types.Scene.transformation_data = PointerProperty(type = TransformationData, name = "Transformation Data")
    
      
class SnappingToolGUI(Panel):
    bl_label = "Snapping Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Animation'
    
    
    @classmethod
    def poll(cls, context):
        return context.object
      
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col1 = row.column(align = True)
        col1.label("Active")
        box = col1.box()
        col = box.column()
        col.column().prop(context.scene.transformation_data, "abs_location", text = "Location")
        col.column().prop(context.scene.transformation_data, "abs_rotation", text = "Rotation")
        col.column().prop(context.scene.transformation_data, "abs_scale", text = "Scale")
        col2 = row.column(align = True)
        col2.label("Stored")
        box = col2.box()
        col = box.column()
        col.column().prop(context.scene.transformation_data, "stored_location", text = "Location")
        col.column().prop(context.scene.transformation_data, "stored_rotation", text = "Rotation")
        col.column().prop(context.scene.transformation_data, "stored_scale", text = "Scale")
        
        row = layout.row()
        row.operator("pose.store_transformation", text = "Store Transformation", icon = 'FORWARD')
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator_menu_enum("pose.apply_matrix", "attribute", text = "Apply", icon = 'SNAP_ON')
        row.operator("anim.keyframe_insert", text = "", icon = 'KEY_HLT').type = 'LocRotScale'

        
class StoreTransformation(Operator):
    bl_label = "Store Transformation"
    bl_idname = "pose.store_transformation"
    bl_description = "Store Transformation Data"
    bl_options = {'UNDO'}  
          
    def execute(self, context):
        scene = bpy.context.scene.transformation_data
        scene.stored_location = scene.abs_location 
        scene.stored_rotation = scene.abs_rotation
        scene.stored_scale = scene.abs_scale
        scene.stored_context_mode = bpy.context.mode
        scene.stored_context_object = bpy.context.active_object.name
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

        
class ApplyMatrix(Operator):
    bl_label = "Apply matrix transformation"
    bl_idname = "pose.apply_matrix"
    bl_description = "Apply Transformation (Matrix)"
    bl_options = {'UNDO'}    
    
    
    #Specific transformation attribute to apply
    attribute = bpy.props.EnumProperty(
        items = [
            ('ALL', 'ALL', "all"),
            ('LOC', 'LOCATION', "location"),
            ('ROT', 'ROTATION', "rotation"),
            ('SCALE', 'SCALE', "scale"),
        ],
        name = "attribute"
    )

    
    def execute(self, context):
        
        data = bpy.context.scene.transformation_data
        
        if self.attribute == 'ALL': 
            self.apply(data.stored_location, data.stored_rotation, data.stored_scale)
            
        elif self.attribute == 'LOC': 
            self.apply(data.stored_location, data.abs_rotation, data.abs_scale)
            
        elif self.attribute == 'ROT':
            self.apply(data.abs_location, data.stored_rotation, data.abs_scale)
            
        elif self.attribute == 'SCALE': 
            self.apply(data.abs_location, data.abs_rotation, data.stored_scale)
        
        bpy.context.scene.update()
        
        return {'FINISHED'}
        
     
    def invoke(self, context, event):
        return self.execute(context)
      
      
    def apply(self, location, rotation, scale):
        """
        Given location, rotation, and scale, apply new transformation
        """
        import mathutils
        stored_loc_matrix = mathutils.Matrix.Translation(location)
        stored_rot_matrix = rotation_matrix(rotation)
        stored_scale_matrix = scale_matrix(scale)
        combined_matrix = stored_loc_matrix*stored_rot_matrix*stored_scale_matrix
        
        if bpy.context.active_object.mode == 'POSE': 
            item = bpy.context.active_pose_bone 
            item.matrix_world = matrix_to_list(combined_matrix) 
            #*Why does blender not let you directly assign matrix if it's self defined?
            
        else: 
            item = bpy.context.active_object 
            item.matrix_world = combined_matrix            
  

#Math Utils Functions: *TODO: Separate these into different class, and combine any previously written math functions
def matrix_to_list(matrix):
    """
    Convert matrix to a tupple
    """
    list = []
    for col in matrix.col:
        for num in col: 
            list.append(num)
    return tuple(list)
                   
def rotation_matrix(rotation):
    """
    Convert rotation to a 4x4 matrix
    """ 
    import mathutils
    m1 = rotation.to_matrix()
    m1 = m1.to_4x4()
    return m1
        
def scale_matrix(scale):
    """
    Convert scale to a 4x4 matrix
    """
    from mathutils import Matrix
    m1 = Matrix.Scale(scale[0], 4, (1.0, 0.0, 0.0)) #X
    m2 = Matrix.Scale(scale[1], 4, (0.0, 1.0, 0.0)) #Y
    m3 = Matrix.Scale(scale[2], 4, (0.0, 0.0, 1.0)) #z
    m = m1*m2*m3
    return m
    
        
def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    register()  
    