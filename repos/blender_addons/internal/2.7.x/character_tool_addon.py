bl_info = {
    "name": "Rigging Tools",
    "author": "Wayne Wu",
    "version": (2, 3, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Rigging Tools",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Rigging%20Tool.aspx",
    "category": "Tangent"}

import bpy
from bpy.types import Panel, Operator, PropertyGroup
import bone_tools
import mesh_tools
     
class ArmatureLayerGUI(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Rigging'
    bl_label = "Armature Layers"
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE'
    
    def draw(self, context):
        layout = self.layout

        arm = context.active_object.data
        layout.prop(arm, "pose_position", expand=True)
        
        col = layout.column()
        col.label(text="Layers:")
        col.prop(arm, "layers", text="")
        col.label(text="Protected Layers:")
        col.prop(arm, "layers_protected", text="")    

        
class ExceptionsProperty(PropertyGroup):
    """
    A property class for exception 
    """
    exception = bpy.props.StringProperty(name="Exception", default = "")
    index = bpy.props.IntProperty(name="Index")
    
class BONE_ToolProperty(PropertyGroup):
    bpy.types.Object.bone_change_prefix = bpy.props.BoolProperty(name = "Change Prefix", description= "Check this to allow changing the prefix of the bones", default = False)
    bpy.types.Object.bone_old_prefix = bpy.props.StringProperty(name = "Old Prefix", default = "ctl.")
    bpy.types.Object.bone_new_prefix = bpy.props.StringProperty(name = "New Prefix", default = "acc.")
    bpy.types.Object.bone_new_scale = bpy.props.FloatProperty(name = "Scale", default = 1.5)
    bpy.types.Object.boneshape_apply = bpy.props.BoolProperty(name = "Assign", description ="Assign bone shape if selected, otherwise will remove bone shape for the selected bones", default = False)
    bpy.types.Object.bone_show_wireframe = bpy.props.BoolProperty(name = "Wireframe", description = "Bone is drawn as wireframe", default = True)
    bpy.types.Object.boneshape_shape_name = bpy.props.StringProperty(name = "Shape name")
    try:
        bpy.utils.register_class(ExceptionsProperty) #Need to find a way around this
    except:
        pass
    bpy.types.Object.bone_exceptions = bpy.props.CollectionProperty(type = ExceptionsProperty)
    bpy.types.Object.bone_deform_enable = bpy.props.BoolProperty(name = "Enable", description = "Will enable deform for selected bones if checked, otherwise will remove", default = False)
    bpy.types.Object.bone_source = bpy.props.StringProperty(name = "Source Bone")
    bpy.types.Object.bone_stretch_volume = bpy.props.EnumProperty(
        items = [('VOLUME_XZX', 'XZX', "volume_xzx"), ('VOLUME_X', "X", "volume_x"),('VOLUME_Z','Z', "volume_z"), ('NO_VOLUME','NO VOLUME', "no_volume")], 
        name = "Stretch To Volume" 
        )
               
class BONE_ToolsGUI(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Rigging'
    bl_label = "Bone Tools"
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()

        ################################BOX1#########################
        row = col.row(align = True)
        box = row.box()
        row = box.row(align = True)
        col2 = row.column(align = True)
        row = col2.row(align = True)
        row.label("Bone Attributes (Based on Selection)")
        row = col2.row(align = True)
        row.operator("object.bone_lock", text = "Lock", icon = 'LOCKED')
        row.operator("object.bone_unlock", text = "Unlock", icon = 'UNLOCKED')
        row = col2.row(align = True)
        row.operator("object.bone_flip", text = "Flip", icon = 'FULLSCREEN_ENTER' )
        row.operator("object.bone_set_xzy", text = "Set XZY", icon = 'NDOF_TURN')
        
        row = box.row(align = True)
        row.alignment = 'LEFT'
        row.prop(context.object, "bone_deform_enable")
        if bpy.context.object.bone_deform_enable:
            row.operator("object.bone_deform", text = "Enable Deform", icon = 'ZOOMIN')
        else:
            row.operator("object.bone_deform", text = "Remove Deform", icon = 'X')
        row = box.row(align = True)
        col2 = row.column(align = False)
        i = 0
        while i < len(bpy.context.object.bone_exceptions):
            col2.prop(context.object.bone_exceptions[i], "exception", icon = 'GROUP_BONE')
            i = i + 1 #First Exception
        row = col2.row(align = True)
        row.operator("object.add_bone_exception", text="Add Exception")
        row.operator("object.remove_bone_exception", text = "", icon = "X")
                    
        ###################################BOX2##########################
        row = col.row(align = True)
        box = row.box()
        col2 = box.column()
        row = col2.row()
        row.label("Bone Parenting (Based on Selection)")
        row = col2.row(align = True)
        row.prop(context.object, "bone_change_prefix")
        if bpy.context.object.bone_change_prefix:
            row = col2.row(align = True)
            row.prop(context.object, "bone_old_prefix" ) 
            row = col2.row(align = True)
            row.prop(context.object, "bone_new_prefix")   
        row = col2.row(align = True)
        row.prop(context.object, "bone_new_scale")   
        row = col2.row(align = True)
        row.operator("object.parent_bones", text = "Create Parent Bones", icon = 'CONSTRAINT_BONE')
        row = col2.row()
        row.separator()
        #Section 3
        row = col2.row()
        row.label("Bone Shape (Based on Selection)")
        row = col2.row(align = True)
        row.prop(context.object, "boneshape_apply")
        if bpy.context.object.boneshape_apply: 
            row.prop(context.object, "bone_show_wireframe")
            row = col2.row(align = True)
            row.prop_search(context.object, "boneshape_shape_name", bpy.context.scene, 'objects', text = "Shape", icon = 'OBJECT_DATA')
        row = col2.row(align = True)
        if bpy.context.object.boneshape_apply:
            row.operator("object.bone_shape", text = "Assign Bone Shape", icon = 'ZOOMIN' )
        else:   
            row.operator("object.bone_shape", text = "Remove Bone Shape", icon = 'X')
        
        #####################################BOX3###############################
        row = col.row()
        box = row.box()
        col2 = box.column(align = True)
        col2.label("Bone Constraints (Based on Selection)")
        row = col2.row(align = True)
        row.alignment = 'EXPAND'
        row.label(icon = 'CONSTRAINT_BONE')
        row.operator("object.mute_bone_constraints", text = "Mute", icon = "RESTRICT_VIEW_ON")
        row.operator("object.unmute_bone_constraints", text = "Unmute", icon = "RESTRICT_VIEW_OFF")
        col2 = box.column()
        col2.label(text="Stretch To")
        row = col2.row(align = True)
        row.label(text ="RESET")
        row.operator("object.reset_stretch_all", text = "All")
        row.operator("object.reset_stretch_selected", text = "Selected")
        row = col2.row(align = True)
        row.alignment = 'EXPAND'
        row.prop_menu_enum(context.object, "bone_stretch_volume", text = bpy.context.object.bone_stretch_volume)
        #row.prop(context.object, "bone_stretch_volume")
        row.operator("object.stretch_volume_change_all", text = "All")
        row.operator("object.stretch_volume_change_selected", text = "Selected")
        row = col.row()
        
        ########################################BOX4#############################
        if bpy.context.selected_pose_bones:
            row = col.row(align = False)
            box = row.box()
            box.prop_search(context.object, "bone_source", bpy.context.object.pose, 'bones', text="Source", icon = 'BONE_DATA')
            box.operator("object.copy_driver", text = "Copy Constraint Drivers", icon = "GHOST")            

class BONE_AddException(Operator):
    bl_idname = "object.add_bone_exception"
    bl_description = "Add exception"
    bl_label = "Add_Exception"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        new_exception = bpy.context.object.bone_exceptions.add()
        i = len(bpy.context.object.bone_exceptions) - 1
        new_exception.index = i
        return{'FINISHED'}
        
class BONE_RemoveException(Operator):
    bl_idname = "object.remove_bone_exception"
    bl_description = "Remove the last exception"
    bl_label = "Remove Exception"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        index = len(bpy.context.object.bone_exceptions) - 1
        bpy.context.object.bone_exceptions.remove(index)
        return{'FINISHED'}
            
class BONE_Flip(Operator):
    bl_idname = "object.bone_flip"
    bl_label = "Flip Bones"
    bl_description = "Flip the selected bones head to tail, tail to head"
    bl_option = {'UNDO'}
    def invoke (self, context, event):  
        bone_tools.bone_flip(compile_bone_exceptions())
        return {'FINISHED'}   

class BONE_Deform(Operator):
    bl_idname = "object.bone_deform"
    bl_label = "Enable Deform Bone to selected"
    bl_description = "Enable/Disable Bone Deform for the selected bones"
    bl_option = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.selected_pose_bones
    
    def invoke (self, context, event):
        if bpy.context.active_object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
            
        for item in bpy.context.selected_pose_bones: 
            if not item.name.startswith(compile_bone_exceptions()):
                if bpy.context.object.bone_deform_enable:
                    item.bone.use_deform = True
                else: 
                    item.bone.use_deform = False   
                    
        return {'FINISHED'}  
        
class BONE_Lock(Operator):
    bl_idname = "object.bone_lock"
    bl_label = "Lock Bone Transformations"
    bl_description = "Lock the transformations of the selected bones"
    bl_option = {'UNDO'}
    
    def invoke (self, context, event):
        bone_tools.bone_lock(compile_bone_exceptions(), True)
        return {'FINISHED'}
        
class BONE_Unlock(Operator):
    bl_idname = "object.bone_unlock"
    bl_label = "Unlock Bone Transformations"
    bl_description = "Unlock the transformations of the selected bones"
    bl_option = {'UNDO'}
    
    def invoke (self, context, event):
        bone_tools.bone_lock(compile_bone_exceptions(), False)
        return {'FINISHED'}
                
class BONE_Parenting(Operator):
    bl_idname = "object.parent_bones"
    bl_label = "Parent_Bone"
    bl_description = "Create a parented bones at the same spot with given scale"
    bl_option = {'UNDO'}
    
    def invoke (self, context, event):
        obj = bpy.context.object
        bone_tools.bone_parenting(obj.bone_change_prefix, obj.bone_new_prefix, obj.bone_old_prefix, obj.bone_new_scale)
        return {'FINISHED'}

class BONE_Shape(Operator):
    bl_idname = "object.bone_shape"
    bl_label = "Remove_Assign_BoneShape"
    bl_description = "Assign/Remove Custom Bone Shape to selected bones"
    bl_option = {'UNDO'}
     
    def invoke (self, context, event):
        shape_name = bpy.context.object.boneshape_shape_name
        if bpy.context.object.boneshape_apply:
            if not shape_name:
                self.report({'ERROR'}, "No Shape Name Entered")
            else: 
                bone_tools.bone_shape(shape_name, bpy.context.object.bone_show_wireframe)
        else: 
            bone_tools.bone_shape()
        return {'FINISHED'}

class BONE_SetXZY(Operator):
    bl_idname = "object.bone_set_xzy"
    bl_label = "Set_XZY"
    bl_description = "Set rotation mode to XZY for all bones in the selected objects"
    bl_option = {'UNDO'}
    
    def invoke (self, context, event):
        
        for item in bpy.context.object.pose.bones:
            if not item.name.startswith(compile_bone_exceptions()):
                item.rotation_mode = 'XZY'          
        return {'FINISHED'}    
        
class BONE_MuteConstraints(Operator):

    bl_idname = "object.mute_bone_constraints"
    bl_label = "Mute_Bone_Constraints"
    bl_description = "Mute constraints on the selected bone"
    bl_option = {'UNDO'}
    
    def invoke (self, context, event):
        bone_tools.mute_bone_constraint(True)
        return {'FINISHED'}    
   
class BONE_UnmuteConstraints(Operator):

    bl_idname = "object.unmute_bone_constraints"
    bl_label = "Unmute_Bone_Constraints"
    bl_description = "Unmute constraints on the selected bone"
    bl_option = {'UNDO'}
    
    def invoke (self, context, event):
        bone_tools.mute_bone_constraint(False)
        return {'FINISHED'}      
        
class BONE_CopyConstraintDriver(Operator):
    bl_idname = "object.copy_driver"
    bl_label = "Copy Drivers after copying constraints"
    bl_description = "Copy source bone's constraint drivers to selected bones"
    bl_option = {'UNDO'}    
    
    @classmethod
    def poll(cls, context):
        return bpy.context.object.bone_source
    
    def invoke (self, context, event):  
        bone_tools.copy_driver(bpy.context.object.bone_source)         
        return {'FINISHED'}

class BONE_ResetStretchAll(Operator):
    bl_idname = "object.reset_stretch_all"
    bl_label = "Reset_Stretch_All"
    bl_description = "Reset stretch to constraint to all pose bones"
    bl_option = {'UNDO'}    
    
    def invoke (self, context, event):
        bone_tools.reset_stretch_constraint('ALL')
        return {'FINISHED'}
        
class BONE_ResetStretchSelected(Operator):
    bl_idname = "object.reset_stretch_selected"
    bl_label = "Reset Stretch Selected"
    bl_description = "Reset stretch to constraint to selected pose bones"
    bl_option = {'UNDO'}    
    
    @classmethod
    def poll(cls, context):
        return context.selected_pose_bones
        
    def invoke (self, context, event):
        bone_tools.reset_stretch_constraint()
        return {'FINISHED'}

class BONE_StretchVolumeChangeAll(Operator):
    bl_idname = "object.stretch_volume_change_all"
    bl_label = "Stretch_Volume_Change_All"
    bl_description = "Change Stretch To Constriant's Volume to all bones"
    bl_option = {'UNDO'}    
    
    def invoke (self, context, event):
        bone_tools.change_stretch_volume(bpy.context.object.bone_stretch_volume,'ALL')
        return {'FINISHED'}
        
class BONE_StretchVolumeChangeSelected(Operator):
    bl_idname = "object.stretch_volume_change_selected"
    bl_label = "Stretch_Volume_Change_Selected"
    bl_description = "Change Stretch To Constriant's Volume to selected bones"
    bl_option = {'UNDO'}    
    
    @classmethod
    def poll(cls, context):
        return context.selected_pose_bones
        
    def invoke (self, context, event):
        bone_tools.change_stretch_volume(bpy.context.object.bone_stretch_volume)
        return {'FINISHED'} 
  

class Mesh_ToolsProperties(PropertyGroup):
    class DriverSettings(PropertyGroup):
        driver_target = bpy.props.StringProperty(name = "Driver Target")
        driver_target_datapath = bpy.props.StringProperty(name = "Driver Target Datapath")
        driver_subtarget = bpy.props.StringProperty(name = "Driver Target Subtarget")
        driver_datapath = bpy.props.StringProperty(name = "Datapath")
        driver_expression = bpy.props.StringProperty(name = "Expression", default = "-var+1")

    try: 
        bpy.utils.register_class(DriverSettings)
    except: pass
    
    bpy.types.Scene.driver_settings = bpy.props.PointerProperty(type = DriverSettings)
    
class MESH_ToolsGUI(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Rigging'
    bl_label = "Mesh Tools"
    
    #*TODO Create a pointer property to point to these
    bpy.types.Object.weight_mirror_side = bpy.props.EnumProperty(
        items = [('LEFT', 'L', "left"), ('RIGHT', 'R', "right")],
        name = "Source Side"
        )
        
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        row.label(text="Modifiers")
        
        row = col.row(align = True)
        row.operator("object.mesh_remove_modifiers", text = "Remove Modifiers", icon = "X")
        
        row = col.row(align = True)
        row.operator("object.mesh_add_dummy", text = "Add Dummy Modifier", icon = "POSE_DATA")
        row = col.row(align = True)
        row.operator("object.lock_transformations", text = "Transformation", icon = 'LOCKED').lock = True
        row.operator("object.lock_transformations", text = "Transformation", icon = 'UNLOCKED').lock = False
        row = col.row(align = True)
        row.label(text="Vertex Groups")
        row = col.row()
        row.label("Source Side:")
        row.prop(context.object, "weight_mirror_side", text = "Source Side", expand = True)
        row = col.row()
        row.operator("object.weight_mirror", text = "Weight Mirror", icon = 'WPAINT_HLT')
        row = col.row() #Small Gap
        
        box = col.box()
        col2 = box.column(align = True)
        col2.label(text="Cycles Render")
        row = col2.row(align = True)
        row.alignment = 'LEFT'
        row.label(text="Ray Visibility", icon = "SEQ_CHROMA_SCOPE")
        row.operator("object.ray_viz_on", text = "ON")
        row.operator("object.ray_viz_off", text = "OFF")
        
        row = col.row()
        box = row.box()
        row = box.row()
        col2 = row.column(align = True)
        col2.label("Create Driver: Target")
        col2.prop_search(context.scene.driver_settings, "driver_target", context.scene, "objects", text = "Object", icon = 'OBJECT_DATA')
        if context.scene.driver_settings.driver_target:
            obj = context.scene.objects[context.scene.driver_settings.driver_target]
            if obj.type == 'ARMATURE':
                col2.prop_search(context.scene.driver_settings, "driver_subtarget", obj.pose, "bones", text = "Bone", icon = 'BONE_DATA')
            col2.prop(context.scene.driver_settings, "driver_target_datapath", text = "Datapath", icon = 'RNA')
            col2.prop(context.scene.driver_settings, "driver_expression", text = "Expression")
        row = box.row(align = True)
        row.prop(context.scene.driver_settings, "driver_datapath", text = "Datapath", icon = 'RNA')
        row.operator("object.create_driver", text = "Create Driver", icon = 'ZOOMIN')    
      
class MESH_RemoveModifiers(Operator):
    bl_idname = "object.mesh_remove_modifiers"
    bl_label = "Remove the modifiers and particle systems"
    bl_description = "Remove all modifiers and all particle systems"
    bl_option = {'UNDO'}    
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'
    
    def invoke (self, context, event):
        mesh_tools.remove_modifiers()
        return {'FINISHED'}

class MESH_LockTransformation(Operator):
    bl_idname = "object.lock_transformations"
    bl_label = "lock_transformations_selected_mesh"
    bl_description = "Lock Transformations for selected objects"
    bl_option = {'UNDO'} 
    
    lock = bpy.props.BoolProperty(name = "state")
    def invoke (self, context, event):
        mesh_tools.lock_objects(self.lock)
        return {'FINISHED'}
               
class MESH_AddDummy(Operator):
    bl_idname = "object.mesh_add_dummy"
    bl_description = "Add Simple Deform Modifier to the end of the selected object's modifier stack"
    bl_label = "Character_Add_Dummy"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        mesh_tools.put_dummy()
            
        return {"FINISHED"}

class MESH_ObjectRayVizOff(Operator):
    bl_idname = "object.ray_viz_off"
    bl_label = "Object_Ray_Viz_off"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'
    
    def invoke(self, context, event):
        mesh_tools.object_ray_viz(False)
            
        return {"FINISHED"}    
        
class MESH_ObjectRayVizOn(Operator):
    bl_idname = "object.ray_viz_on"
    bl_label = "Object_Ray_Viz_on"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'
    
    def invoke(self, context, event):
        mesh_tools.object_ray_viz(True)
            
        return {"FINISHED"}  
        
class MESH_WeightMirroring(Operator):
    bl_idname = "object.weight_mirror"
    bl_label = "Mirror Weight across the X Axis"
    bl_options = {'UNDO'}
    
    @classmethod 
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'
        
    def invoke(self, context, event):
        weight = mesh_tools.WeightMirroring(bpy.context.object.weight_mirror_side)
        weight.execute()
        return {"FINISHED"}  
 
class OBJ_CreateDriver(Operator):
    bl_idname = "object.create_driver"
    bl_label = "Create Drivers"
    bl_description = "Create the same driver on the selected meshes"
    bl_options = {'UNDO'}
    
    
    @classmethod
    def poll(cls, context):
        settings = context.scene.driver_settings
        return (
            context.object 
            and context.object.mode == 'OBJECT' 
            and settings.driver_target_datapath 
            and settings.driver_datapath)
    
    def execute(self, context):
        settings = context.scene.driver_settings
        for obj in bpy.context.selected_objects:
            self.create_driver(
                obj, 
                settings.driver_datapath, 
                settings.driver_expression,
                settings.driver_target_datapath, 
                settings.driver_target, 
                settings.driver_subtarget)
                
        return {'FINISHED'}   
    
    def invoke(self, context, event):
        return self.execute(context)
       
    def create_driver(self, obj, data_path, expression, custom_prop_name, target_id, subtarget = None):
        new_driver = obj.driver_add(data_path)
        new_driver.driver.expression = expression
        try: 
            var = new_driver.driver.variables[0]
        except: 
            var = new_driver.driver.variables.new()     
        var.name = "var"
        target = var.targets[0]
        target.id = bpy.context.scene.objects[target_id]
        if subtarget: 
            target.bone_target = subtarget
        target.data_path = custom_prop_name    

    
class CLEAN_ToolsGUI(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Rigging'
    bl_label = "Clean Up Tools"
    
    bpy.types.Scene.clear_action_name = bpy.props.StringProperty(name = "Clear Action Name")  
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        row.label(icon = 'LINKED')
        row.operator("object.character_remove_dependencies", text = "Clear Dependencies", icon = 'X')
        row = col.row(align = True)
        row.label(icon= 'SPLITSCREEN')
        row.operator("screen.delete_none_default", text = "Delete Screens", icon = 'X')
        row = col.row(align = True)
        row.prop_search(context.scene, "clear_action_name", bpy.data, "actions", text = "Action")
        row.operator("action.clear_action", text = "Remove", icon = "X")
        
class CLEAN_RemoveDependency(Operator):
    bl_idname = "object.character_remove_dependencies"
    bl_label = "Character_Remove_Dependencies"
    bl_description = "Remove all dependencies at the rig level" 
    bl_options = {"UNDO"}
    
    def invoke(self, context, event):     
        error_list = self.remove_dependencies()
        if error_list:
            for error in error_list: 
                self.report({'ERROR'}, error)
        return {"FINISHED"}
        
    def remove_dependencies(self):
        """
        Remove all dependencies at the armature level
        """
        error=[]
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
                                    try:
                                        d.data_path = 'bones[\"ctl.god.C\"].hide'      #change data_path target to ctl.god.C so that it's deletable    
                                    except: 
                                        print("No such datapath")
                                        break
                                    else:
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
             
class CLEAN_ClearAction(Operator):
    bl_idname = "action.clear_action"
    bl_label = "Clear_action"
    bl_description = "Clear all users in an action and remove it"
    bl_options = {'UNDO'}
    
    
    def execute(self, context):
    
        action = bpy.data.actions[bpy.context.scene.clear_action_name]
        action.user_clear() 
        bpy.data.actions.remove(action)
   
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)
        
class CLEAN_DeleteScreens(Operator):
    bl_idname = "screen.delete_none_default"
    bl_label = "Delete_None_Default"
    bl_description = "Delete None Default screens"
    bl_options = {'UNDO'}
      
    def execute(self, context):
        
        default_screens = [
            "3D View Full",
            "Animation",
            "Composition",
            "Default",
            "Game Logic",
            "Motion Tracking",
            "Scripting",
            "UV Editing",
            "Video Editing",
            ]
        
        i = 0
        while(i<len(bpy.data.screens)):
            bpy.ops.screen.screen_set(delta = 1)
            if bpy.context.screen.name not in default_screens:
                bpy.ops.screen.delete()
            i = i + 1
        bpy.context.window.screen = bpy.data.screens["Default"]
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)
               
def compile_bone_exceptions():
    
    strings = []
    try: 
        bpy.context.object.bone_exceptions
    except: 
        pass
    else: 
        for b in bpy.context.object.bone_exceptions: 
            strings.append(b.exception)
    if not strings:
        #string is empty
        strings.append("\t\t\t") 
    str = tuple(strings)
    return str
        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()            
                
        
   