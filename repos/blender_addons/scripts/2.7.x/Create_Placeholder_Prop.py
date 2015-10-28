bl_info = {
    "name": "Tangent: Placeholder Prop",
    "author": "Wayne Wu",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Tools > Prop",
    "description": "Add a placeholder prop(box)",
    "warning": "DO NOT create object with the same name more than once",
    "wiki_url": "",
    "category": "Add Prop"}


import bpy
from bpy.props import StringProperty
from math import pi


#UI
class AddTempProp_UI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Props'
    bl_label = "Placeholder Prop (Box)"
    
    bpy.types.Scene.prop_name = StringProperty(name = "Name", default = "prpXXX_name")
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        row.prop(context.scene, "prop_name" )
        
        row2 = col.row()
        row2.operator("object.temp_prop", text = "Add", icon = 'MESH_CUBE')
        row2.scale_y = 2
        

#Add Operator
class AddTempProp_button(bpy.types.Operator):
    bl_idname = "object.temp_prop"
    bl_label = "ADD"
    bl_options = {"UNDO"}
    
    def invoke(self, context, event):
        AddTempProp()
        return {"FINISHED"}
 

#Add Temporary Prop with proper name
def AddTempProp():  

    name = bpy.context.scene.prop_name
    
    #names
    armature_name = "rig." + name
    bone_name = "ctl.god.C"
    geo_name = "geo." + name
    msh_name = "msh." + name
    god = "god_shape"
    geo_name_god = geo_name + "_" + god
    msh_name_god = msh_name + "_" + god
    group_name = "group." + name


    #delete all objects in scene 
    def DeleteAllObjects():
        override = {'selected_bases': list(bpy.context.scene.object_bases)}
        bpy.ops.object.delete(override)



    #CREATE ARMATURE (Data method) 
    def CreateArmature():
        
        amt = bpy.data.armatures.new(armature_name)
        rig = bpy.data.objects.new(armature_name, amt)
        rig.location = (0,0,0)
        rig.show_x_ray = False
        #rig.layers = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
        amt.show_names = False

        # Link object to scene
        scn = bpy.context.scene
        scn.objects.link(rig)
        scn.objects.active = rig
        scn.update()
        
        bpy.ops.object.editmode_toggle()

        bone = amt.edit_bones.new(bone_name)
        bone.head = (0,0,0)
        bone.tail = (0,1,0)
        
        #Disable Deform
        bone.use_deform = False
        bone.show_wire = True

        
        #Bone relative
        bone.use_relative_parent = True
        
        amt.layers_protected[0] = True
        
        return rig
        

    #CREATE MESH (Primitive method)
    def CreateMesh():
        
        bpy.ops.mesh.primitive_cube_add(location = (0,0,1))
        ob = bpy.context.object
        ob.name = geo_name
        ob.show_name = False
        me = ob.data
        me.name = msh_name
        
        #Parenting
        ob.parent = bpy.data.objects[armature_name]
        ob.parent_type = "BONE"
        ob.parent_bone = bone_name
        
        
        #Add Material
        mat = bpy.data.materials.new('Red')
        mat.diffuse_color = (1,0,0,)
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 0.8 
        mat.specular_color = (1,1,1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.5
        mat.alpha = 1
        mat.ambient = 1
        
        me.materials.append(mat)
       
        ob.hide_select = True
        
        return ob

    #Create Controller Shape
    def CreateShape():
        
        bpy.ops.mesh.primitive_circle_add(vertices=4, radius=2, location=(0,0,0), rotation=(0,0,pi/4))
        ob = bpy.context.object
        ob.name = geo_name_god
        me = ob.data
        me.name = msh_name_god
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        #ob.hide = True
        #ob.hide_select = True
        ob.hide_render = True
        
        return ob


    def LinkShape():
         
        amt = bpy.data.objects[armature_name]
        pose_bone = amt.pose.bones[bone_name]
        pose_bone.custom_shape = bpy.data.objects[geo_name_god]
        
        #Quaterion -> Euler
        pose_bone.rotation_mode = 'XYZ'
        
        #Show Wireframe
        bone = bpy.data.armatures[armature_name].bones[bone_name]
        bone.show_wire = True
        #Disable Deform
        #bone.use_deform = False
        
        scn = bpy.context.scene
        scn.update()
       
        return amt


    def MoveLayer():
        ob = bpy.data.objects[geo_name_god]
        ob.select = True 
        bpy.ops.object.move_to_layer(layers = (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
        ob.hide = True 
        ob.hide_select = True
        #ob.hide_render = True

    def CreateGroup():
        bpy.context.scene.layers[0] = True
        bpy.ops.object.select_by_layer()
        bpy.ops.group.create()
        bpy.data.groups["Group"].name = group_name
               
           
    #RUN 
    
    delete = DeleteAllObjects()
     
    rig = CreateArmature()
    box = CreateMesh()
    controller = CreateShape()
    link = LinkShape()
    
    move = MoveLayer()
    group = CreateGroup()
    

            
def register():
    bpy.utils.register_class(AddTempProp_UI)
    bpy.utils.register_class(AddTempProp_button)


def unregister():
    bpy.utils.unregister_class(AddTempProp_UI)
    bpy.utils.unregister_class(AddTempProp_button)


if __name__ == "__main__":
    register()
