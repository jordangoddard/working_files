bl_info = {
    "name": "Tangent Rig UI",
    "author": "David Hearn/Wayne Wu",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Tools > Character(Rig) GUI",
    "description": "Cutsom rig UI layers",
    "warning": "Report if anything is broken",
    "category": "Tangent"}

import bpy
import re
from bpy.types import (PropertyGroup, Panel, Operator)
    
class BodyControlProperty(PropertyGroup):

    body_armL = bpy.props.BoolProperty(name = "Right Arm Control", default = False)
    body_armR = bpy.props.BoolProperty(name = "Left Arm Control", default = False)
    body_legL = bpy.props.BoolProperty(name = "Right Leg Control", default = False)
    body_legR = bpy.props.BoolProperty(name = "Left Leg Control", default = False)
    front_pawL = bpy.props.BoolProperty(name = "Front Paw Control", default = False)
    front_pawR = bpy.props.BoolProperty(name = "Front Paw Control", default = False)
    back_pawL = bpy.props.BoolProperty(name = "Back Paw Control", default = False)
    back_pawR = bpy.props.BoolProperty(name = "Back Paw Control", default = False)
    hand_pivL = bpy.props.BoolProperty(name = "Hand Pivot Control L", default = False)    
    hand_pivR = bpy.props.BoolProperty(name = "Hand Pivot Control R", default = False)
    foot_pivL = bpy.props.BoolProperty(name = "Foot Pivot Control L", default = False)
    foot_pivR = bpy.props.BoolProperty(name = "Foot Pivot Control R", default = False)

class DisplayOptionProperty(PropertyGroup):
    general_control = bpy.props.BoolProperty(name = "General Controls", default = True)
    body_control = bpy.props.BoolProperty(name = "Body Controls", default = True)
    paw_control = bpy.props.BoolProperty(name = "Paw Controls", default = True)
    pivot_control = bpy.props.BoolProperty(name = "Pivot Controls", default = True)
   
class SpecialCustomProp(PropertyGroup):
    bone_name = bpy.props.StringProperty(name = "Bone Name")

class CharacterGUIProperty(PropertyGroup):
    """
    Property Used for the whole GUI in general
    """
    
    try:
        bpy.utils.register_class(BodyControlProperty)
        bpy.utils.register_class(DisplayOptionProperty)
        bpy.utils.register_class(SpecialCustomProp)
    except:
        pass
    
    bpy.types.Scene.asset_resolution = bpy.props.EnumProperty(
        items = [('HIGH', 'HIGH', "High res",'SOLID', 0),
            ('MID', 'MID', "Mid res", 'ANTIALIASED', 1),
            ('LOW', 'LOW', "Low res", 'ALIASED', 2)],
        )
    bpy.types.Scene.face_controllers = bpy.props.EnumProperty(
        items = [('MOUTH', 'MOUTH', "Mouth controls"),
            ('EYE', 'EYE', "Eye controls"),
            ('FOLLOW', 'FOLLOW', "Follow controls"),
            ('GOD', 'GOD', "God controls"),
            ('SPECIAL', 'SPECIAL', "Special controls"),
            ('NONE', 'NONE', "Collapse")
            ],
        name = "different face controls" )       
    bpy.types.Object.selection_set_name = bpy.props.StringProperty(name = "name of selection set", default = "Custom Set")
    bpy.types.Object.special_custom_prop = bpy.props.CollectionProperty(type = SpecialCustomProp)
    bpy.types.Scene.custom_prop_display = bpy.props.PointerProperty(type = DisplayOptionProperty)
    bpy.types.Scene.body_controllers = bpy.props.PointerProperty(type=BodyControlProperty, name = "Body Controllers")

class RigTag(object):
    """
    Rig Properties to be used within this addon 
    """
    rig_id = None #Classify between HUMAN or DOG
    current_rig = None  #Store the current active rig
    different_rig = False
    
def classify_rig():
    """
    Classify rig for human or dog
    """
    for bone in bpy.context.object.data.bones: 
        if bone.name.startswith("ctl.tail"):
            RigTag.rig_id = 'DOG'
            break
        if bone.name.startswith("ctl.breast"):
            RigTag.rig_id = 'HUMAN'
            break
            
def sort_controllers(layer_index):
    """
    Determine the controllers within given layer
    """
    bone_list = []
    for bone in bpy.context.object.data.bones:
        if bone.layers[layer_index]:
            bone_list.append(bone.name)
    return bone_list

class AppendSelectionSet(Operator):
    bl_label = "Append Selection Set"
    bl_idname = "object.append_selection_set"
    bl_description = "Append predefined selection Set"
    bl_options = {'UNDO'}    
    
    def invoke(self, context, event):
        #Add Predefined Selection Set Here
        pass
        return {'FINISHED'}
    
class AddSelectionSet(Operator):
    bl_label = "Remove Selection Set"
    bl_idname = "object.add_selection_set"
    bl_description = "Add Selection Set"
    bl_options = {'UNDO'}    
    
    def invoke(self, context, event):
        selection_set  = bpy.context.object.selection_sets.add()
        selection_set.name = bpy.context.object.selection_set_name
        for bone in bpy.context.selected_pose_bones: 
            bone_id = selection_set.bone_ids.add()
            bone_id.name = bone.name
        return {'FINISHED'}
    
class RemoveSelectionSet(Operator):  
    bl_label = "Remove Selection Set"
    bl_idname = "object.remove_selection_set"
    bl_description = "Remove Selection Set"
    bl_options = {'UNDO'}
    
    set_index = bpy.props.IntProperty(name = "selection set index")
    
    def invoke(self, context, evnet):
        bpy.context.object.active_selection_set = self.set_index
        bpy.ops.pose.selection_set_remove()
        return {'FINISHED'}
    
class ToggleSelectionSet(Operator):
    bl_label = "Toggle Selection Set"
    bl_idname = "object.toggle_selection_set"
    bl_description = "Toggle the selection set"
    bl_options = {'UNDO'}   
    
    set_index = bpy.props.IntProperty(name = "selection set index")
    
    def execute(self, context):
        bpy.context.object.active_selection_set = self.set_index
        bpy.ops.pose.selection_set_toggle()
        for bone_id in bpy.context.object.selection_sets[self.set_index].bone_ids:
            i = 0
            for layer in bpy.context.object.data.bones[bone_id.name].layers:
                if layer: 
                    bpy.context.object.data.layers[i] = True
                    break
                i = i + 1
        return {'FINISHED'}
    
    def invoke(self, context, event):      
        return self.execute(context)

class AddSetKeyTransformation(Operator):
    """
    Add keyframes to transformations
    """
    bl_label = "Add Set Key Transfromation"
    bl_idname = "anim.set_key_transformation"
    bl_description = "Add Keyframes to all transformations in bones within the selection set"
    bl_options = {'UNDO'}   
    
    set_index = bpy.props.IntProperty(name = "Index")
    
    def invoke(self, context, event):
        for bone_id in bpy.context.object.selection_sets[self.set_index].bone_ids:
            bpy.context.object.keyframe_insert("pose.bones[\"%s\"].location" %bone_id.name)
            bpy.context.object.keyframe_insert("pose.bones[\"%s\"].rotation_euler" %bone_id.name)
            bpy.context.object.keyframe_insert("pose.bones[\"%s\"].scale" %bone_id.name)
        return {'FINISHED'}
              
class AddLayerKeyTransformation(Operator):
    """
    Add keyframes to transformations
    """
    bl_label = "Add Layer Key Transfromation"
    bl_idname = "anim.layer_key_transformation"
    bl_description = "Add keyframes to all transformations in bones within the layer"
    bl_options = {'UNDO'}   
    
    layer_index = bpy.props.IntProperty(name = "Index")
    
    def invoke(self, context, event):
        bone_list = sort_controllers(self.layer_index)
        for bone_name in bone_list:
            bpy.context.object.keyframe_insert("pose.bones[\"%s\"].location" %bone_name)
            bpy.context.object.keyframe_insert("pose.bones[\"%s\"].rotation_euler" %bone_name)
            bpy.context.object.keyframe_insert("pose.bones[\"%s\"].scale" %bone_name)
        return {'FINISHED'}
        
class SelectControllers(Operator):
    """
    Select controller in laye 
    """
    bl_label = "select_controllers "
    bl_idname = "scene.select_controllers"
    bl_description = "Add Key Transformation"
    bl_options = {'UNDO'}   
    
    layer = bpy.props.IntProperty(name = "Index")
    
    def invoke(self, context, event):
        bone_list = sort_controllers(self.layer)
        for bone_name in bone_list:
            bpy.context.object.data.bones[bone_name].select = True
        return {'FINISHED'}

class PossibleList(object):
    """
    Bunch of possible list for edge cases
    """     
    mouth = ['ctl.mouth_blendshape.C', 'ctl.mouth_blendshapes.C', 'ctl.mouth.blendshape']
    follow = ['ctl.neck.C', 'ctl.head.C']
    body_armL = ['ctl.arm_config.L', 'ctl.arm.config.L', 'ctl.hand.config.L', 'ctl.armpit.blends.L']
    body_armR = ['ctl.arm_config.R', 'ctl.arm.config.R', 'ctl.hand.config.R', 'ctl.armpit.blends.R']
    body_legL = ['ctl.leg_config.L', 'ctl.leg.config.L', 'ctl.ik_heel.L']
    body_legR = ['ctl.leg_config.R', 'ctl.leg.config.R', 'ctl.ik_heel.R']
    front_pawL = ['ctl.paw.front.L', 'ctl.paw_front.L']
    front_pawR = ['ctl.paw.front.R', 'ctl.paw_front.R']
    back_pawL = ['ctl.paw.back.L', 'ctl.paw_back.L']
    back_pawR = ['ctl.paw.back.R', 'ctl.paw_back.R']
    hand_pivL = ['ctl.hand_pivot.L', 'ctl.hand.pivot.L']  
    hand_pivR = ['ctl.hand_pivot.R', 'ctl.hand.pivot.R']
    foot_pivL = ['ctl.foot_pivot.L', 'ctl.foot.pivot.L']
    foot_pivR = ['ctl.foot_pivot.R', 'ctl.foot.pivot.R']
    
    _body_list = body_armL + body_armR + body_legL + body_legR
    _paw_list = front_pawL + front_pawR + back_pawL + back_pawR
    _pivot_list = hand_pivL + hand_pivR + foot_pivL + foot_pivR
             
class AddSpecialCustomProp(Operator):
    bl_label = "Add_special_custom_prop"
    bl_idname = "scene.special_custom_prop_add"
    bl_description = "Add special custom properties to dispay"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        special = bpy.context.object.special_custom_prop.add()
        try:
            special.bone_name = bpy.context.active_pose_bone.name
        except: 
            self.report({'ERROR'}, "No bone selected")
        return {'FINISHED'}
        
class RemoveSpecialCustomProp(Operator):
    bl_label = "Remove_special_custom_prop"
    bl_idname = "scene.special_custom_prop_remove"
    bl_description = "Remove special custom properties"
    bl_options = {'UNDO'}
    
    index = bpy.props.IntProperty(name = "index")
    
    def invoke(self, context, event):
        bpy.context.object.special_custom_prop.remove(self.index)
        return {'FINISHED'}
        
class KeyAllProperties(Operator):
    """
    Add keyframe to all custom properties of the bone
    """
    bl_label = "Add_key_properties"
    bl_idname = "anim.keyframe_add_properties"
    bl_description = "Add Key Custom Properties"
    bl_options = {'UNDO'}
    
    bone_name = bpy.props.StringProperty(name = "Bone's Name")
    
    def execute(self, context):
        bone = bpy.context.object.pose.bones[self.bone_name]
        for custom_prop in bone.keys():
            if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI' and type(bone[custom_prop]).__name__ != 'str':
                bpy.context.object.keyframe_insert("pose.bones[\"%s\"][\"%s\"]" %(self.bone_name, custom_prop))
        return {'FINISHED'}             
    
    def invoke(self, context, event):
        return self.execute(context)                                     

class KeyMultipleProperties(Operator):
    bl_label = "Add_key_properties_multiple"
    bl_idname = "anim.keyframe_add_properties_multiple"
    bl_description = "Add Key to all custom properties within this section"
    bl_options = {'UNDO'}
     
    custom_prop_group = bpy.props.StringProperty(name = "Group Name")
    
    def invoke(self, context, event):
        if self.custom_prop_group == 'BODY': 
            for name in PossibleList._body_list:
                try:
                    bpy.ops.anim.keyframe_add_properties(bone_name = name)
                except: 
                    pass
        elif self.custom_prop_group == 'PAW': 
            for name in PossibleList._paw_list:
                try:
                    bpy.ops.anim.keyframe_add_properties(bone_name = name)
                except:
                    pass
        elif self.custom_prop_group == 'PIVOT': 
            for name in PossibleList._pivot_list:
                try:
                    bpy.ops.anim.keyframe_add_properties(bone_name = name)
                except:
                    pass
        return {'FINISHED'}
                                         
class SwapAssetResolution(Operator):
    """
    Swap asset resolution
    """
    bl_label = "Key_all_properties"
    bl_idname = "object.change_asset_resolution"
    bl_description = "Change Asset Resolution to the selected object"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        if bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')  
        
        bpy.context.scene.cursor_location.xyz = (0,0,0)
        for obj in bpy.context.selected_objects:
            try:
                group = obj.dupli_group
            except:
                self.report({'ERROR'}, "Object might not be linked")
            else:
                group_name = None
                new_group_name = None
                if group.name.endswith('LOW') or group.name.endswith('MID'):
                    group_name = group.name[:-4]
                else: 
                    group_name = group.name
                print(group_name)
                bpy.context.scene.objects.unlink(obj)
                resolution = bpy.context.scene.asset_resolution 
                if resolution == 'HIGH': 
                    new_group_name = group_name
                elif resolution == 'MID':
                    new_group_name = group_name + '_MID'
                elif resolution == 'LOW': 
                    new_group_name = group_name + '_LOW'
                dir = group.library.filepath + '\\Group\\'
                    #error = self.link_in_groups(group.library.filepath, bpy.context.scene.asset_resolution, group_name)
                try: 
                    bpy.ops.wm.link(filename= new_group_name, directory = dir)
                except: 
                    self.report({'ERROR'}, "Could not link in different resolution")
                    bpy.context.scene.link(obj) #link back the object
                else:
                    bpy.data.groups.remove(group) #remove current one
                    bpy.data.objects.remove(obj) #remove object completely    
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)

class RigLayerGUI(Panel):
    """Creates a custom Rig UI layers panel"""
    bl_label = "Control Layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'CharacterGUI'

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
   
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        if bpy.context.object.data.name != RigTag.current_rig:
            #If rig name is not the same as the previous one, reclassify the rig
            classify_rig()
            RigTag.current_rig = bpy.context.object.data.name
            RigTag.different_rig = True 
            
        if RigTag.rig_id == 'DOG':
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Body')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 0
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 0
            col.separator()
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Torso')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 1
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 1
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Head Neck')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 2
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 2
            col.separator()
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=3, toggle=True, text='Front Left Leg')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 3
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 3
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Front Right Leg')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 4
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 4
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=5, toggle=True, text='Back Left Leg')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 5
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 5
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=6, toggle=True, text='Back Right Leg')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 6
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 6
            col.separator()
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Face')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 16
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 16 
            col.separator()
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Upper Face Primary')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 17
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 17
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=18, toggle=True, text='Upper Face Secondary')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 18
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 18
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Left Ear')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 22
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 22
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Right Ear')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 23
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 23
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=19, toggle=True, text='Lower Face Primary')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 19
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 19
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=20, toggle=True, text='Lower Face Secondary')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 20
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 20
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=21, toggle=True, text='Toungue and Teeth')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 21
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 21
               
        elif RigTag.rig_id == 'HUMAN': 
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=28, toggle=True, text='Body')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 28
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 28
            
            col.separator()
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=3, toggle=True, text='Torso')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 3
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 3
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Torso Tweakers')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 4
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 4
            
            col.separator()
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=7, toggle=True, text='Left Arm IK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 7
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 7
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=10, toggle=True, text='Right Arm IK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 10
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 10
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=8, toggle=True, text='Left Arm FK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 8
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 8
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=11, toggle=True, text='Right Arm FK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 11
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 11
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=9, toggle=True, text='Left Arm Tweakers')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 9
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 9
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=12, toggle=True, text='Right Arm Tweakers')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 12
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 12
            
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='Hands')  
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 5
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 5
            
            col.separator()
            
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=13, toggle=True, text='Left Leg IK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 13
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 13
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Right Leg IK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 16
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 16
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=14, toggle=True, text='Left Leg FK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 14
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 14
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Right Leg FK')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 17
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 17
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=15, toggle=True, text='Left Leg Tweakers')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 15
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 15
            col2 = row.column()
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=18, toggle=True, text='Right Leg Tweakers')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 18
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 18
            
            col.separator()
            
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Eyes')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 0
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 0
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Main Face')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 1
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 1
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Secondary Face')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 2
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 2                    
            
            col.separator()
            row = col.row(align = False)
            col2 = row.column (align = True)
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=19, toggle=True, text='Extra')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 19
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 19   
            col2 = row.column (align = True)
            row2 = col2.row(align = True)
            row2.prop(context.active_object.data, 'layers', index=20, toggle=True, text='Extra')
            row2.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 20
            row2.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 20   
            row = col.row(align = True)
            row.prop(context.active_object.data, 'layers', index=21, toggle=True, text='Extra')
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 21
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 21        
            row.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Extra')  
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 22
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 22        
            row.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Extra')  
            row.operator("scene.select_controllers", icon= 'HAND', text = "").layer = 23
            row.operator("anim.layer_key_transformation", icon= 'KEY_HLT', text = "").layer_index = 23        
            
        #Selection Set Tools
        col.separator()    
        row = col.row()
        col2 = row.column(align = True)
        row = col2.row(align = False)
        split = row.split(percentage = 1)
        split.operator("object.append_selection_set", icon = 'APPEND_BLEND', text = "Append Predefied Sets")
        split = row.split(percentage = 0.6, align = True)
        split.prop(context.object, "selection_set_name", icon ='SORTALPHA', text = "")
        split.operator("object.add_selection_set", icon = "ZOOMIN", text = "Add")
        i = 0
        for selection_set in bpy.context.object.selection_sets:
            if i % 2 == 0:
                row = col2.row(align = True)
            sub_col = row.column(align = False)
            row = sub_col.row(align = True)
            row.operator("object.remove_selection_set", text = "", icon = 'X').set_index = i
            row.operator("object.toggle_selection_set", text = selection_set.name).set_index = i
            row.operator("anim.set_key_transformation", text = "", icon = 'KEY_HLT').set_index = i
            i = i + 1 
                   
class AnimationControlGUI(Panel):
    bl_label = "Animation Controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'CharacterGUI'            

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
    
    def draw(self, context):
               
        layout = self.layout
        col = layout.column()
        
        if bpy.context.object.data.name != RigTag.current_rig:
            #If rig name is not the same as the previous one, reclassify the rig
            classify_rig()
            RigTag.current_rig = bpy.context.object.data.name
            RigTag.different_rig = True
        
        if bpy.context.scene.custom_prop_display.general_control: #General Control ON
            row = col.row(align = True)
            row.prop(context.scene, "face_controllers", expand = True)
            controller = context.scene.face_controllers
            ##################### MOUTH Controls ###########
            if controller == 'MOUTH':
                for bone in context.object.pose.bones:
                    search1 = re.search('blendshape', bone.name)
                    possible_list = PossibleList.mouth
                    if self._draw2(bone, col, RigTag.rig_id, possible_list):
                        break                       
            ##################### EYE Controls ###########
            if controller == 'EYE':
                for bone in context.object.pose.bones:
                    search1 = re.search("head_blink", bone.name)
                    search2 = re.search("eye", bone.name)
                    search3 = re.search("blendshape", bone.name)
                    possible_list = ['ctl.mouth.blendshape.001']
                    if bone.name.startswith('ctl.') and (search1 or (search2 and search3)) or bone.name in possible_list: 
                        row = col.row()
                        box = row.box()
                        col2 = box.column(align = True)
                        sub_col = None
                        key = False
                        for custom_prop in sorted(bone.keys()):
                            if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI':
                                if type(bone[custom_prop]).__name__ == 'str':
                                    row = col2.row(align = False)
                                    prop_name = custom_prop
                                    custom_prop = custom_prop.replace('_', ' ')
                                    custom_prop = custom_prop.title()
                                    row.label(custom_prop)
                                    row.label(bone[prop_name])
                                    if not key: 
                                        row.operator("anim.keyframe_add_properties", text = "", icon = 'KEY_HLT').bone_name = bone.name
                                        key = True
                                    row = col2.row(align = True)
                                    sub_col = row.column(align = True)
                                else:
                                    row = sub_col.row(align = True)
                                    row.prop(bone,'["{}"]'.format(custom_prop), slider = True)
                        break
            ##################### GOD Controls #############
            if controller == 'GOD':     
                god_node = context.object.pose.bones["ctl.god.C"]
                row = col.row()
                box = row.box()
                col2 = box.column(align = True)
                for custom_prop in sorted(god_node.keys()): 
                    exceptions = ['rigifty_parameters', '_RNA_UI', 'highlite_intensity', 'highlite_size', 'lock_eye_highlite_world']
                    if custom_prop not in exceptions:
                        row = col2.row(align = True)
                        row.prop(god_node, '["{}"]'.format(custom_prop), slider = True)             
            #################### FOLLOW Controls ############
            if controller == 'FOLLOW': 
                possible_list = PossibleList.follow
                key = False
                row = col.row()
                box = row.box()
                col2 = box.column(align = True)
                for bone_name in possible_list: 
                    bone = bpy.context.object.pose.bones[bone_name] 
                    sub_col = None
                    for custom_prop in sorted(bone.keys()):
                        if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI':
                            if type(bone[custom_prop]).__name__ == 'str':
                                row = col2.row(align = False)
                                prop_name = custom_prop
                                custom_prop = custom_prop.replace('_', ' ')
                                custom_prop = custom_prop.title()
                                row.label(custom_prop)
                                row.label(bone[prop_name])
                                # if not key: 
                                    # row.operator("anim.keyframe_add_properties", text = "", icon = 'KEY_HLT').bone_name = bone.name
                                    # key = True
                                row = col2.row(align = True)
                                sub_col = row.column(align = True)
                            else:
                                if not sub_col: 
                                    # if not key: 
                                        # row = col2.row(align = False)
                                        # row.alignment = 'RIGHT'
                                        # row.operator("anim.keyframe_add_properties", text = "", icon = 'KEY_HLT').bone_name = bone.name
                                        # key = True
                                    row = col2.row(align = True)
                                    sub_col = row.column(align = True)
                                row = sub_col.row(align = True)
                            row.prop(bone,'["{}"]'.format(custom_prop), slider = True)
            #################### SPECIAL Controls #########
            if controller == 'SPECIAL': 
                row = col.row()
                row.operator("scene.special_custom_prop_add", text = "Add Special Custom Properties", icon = 'ZOOMIN')
                i = 0
                while i < len(bpy.context.object.special_custom_prop):
                    row = col.row(align = True)
                    box = row.box()
                    col2 = box.column(align = True)
                    bone = bpy.context.object.pose.bones[bpy.context.object.special_custom_prop[i].bone_name]
                    row = col2.row(align = False)
                    row.label(bone.name)
                    row.operator("scene.special_custom_prop_remove", text = "", icon = 'X').index = i
                    row = col2.row(align = True)
                    sub_col = row.column(align = True)
                    for custom_prop in sorted(bone.keys()):
                        if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI':
                            if type(bone[custom_prop]).__name__ == 'str':
                                row = sub_col.row(align = False)
                                prop_name = custom_prop
                                custom_prop = custom_prop.replace('_', ' ')
                                custom_prop = custom_prop.title()
                                row.label(custom_prop)
                                if bone[prop_name]:
                                    row.label(bone[prop_name])
                            row = sub_col.row(align = True)
                            row.prop(bone,'["{}"]'.format(custom_prop), slider = True)
                    i = i + 1 #First Exception
               
        # if RigTag.different_rig: 
            # """
            # Turn Everythin On
            # """
            # b = bpy.context.scene.body_controllers
            # b.body_armL = True 
            # b.body_armR = True
            # b.body_legL = True
            # b.body_legR = True
            # b.front_pawL = True
            # b.front_pawR = True
            # b.back_pawL = True
            # b.back_pawR = True
            # b.hand_pivL = True
            # b.hand_pivR = True
            # b.foot_pivL = True
            # b.foot_pivR = True
            
        row = col.row()
        if bpy.context.scene.custom_prop_display.body_control: #Body Control ON
            row = col.row(align = True)
            row.prop(context.scene.body_controllers, "body_armL", toggle=True, text='ARM.L', icon = 'TRIA_LEFT')
            row.prop(context.scene.body_controllers, "body_legL", toggle=True, text='LEG.L', icon = 'TRIA_LEFT')
            row.operator("anim.keyframe_add_properties_multiple", text = "", icon = 'KEY_HLT').custom_prop_group = "BODY"
            row.prop(context.scene.body_controllers, "body_armR", toggle=True, text='ARM.R', icon = 'TRIA_RIGHT')
            row.prop(context.scene.body_controllers, "body_legR", toggle=True, text='LEG.R', icon = 'TRIA_RIGHT')
            
            row1 = col.row(align = True)
            list = []
            if context.scene.body_controllers.body_armL or context.scene.body_controllers.body_legL:
                col1 = row1.column(align = True)     
                ##################### ARM.L Controls ##############                
                if context.scene.body_controllers.body_armL:
                    for bone in context.object.pose.bones: 
                        possible_list = PossibleList.body_armL
                        if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_UP_BAR')):
                            list.append(bone.name)
                            if RigTag.rig_id == 'DOG': 
                                break
                 ##################### LEG.L Controls ##############                
                if context.scene.body_controllers.body_legL:
                    for bone in context.object.pose.bones: 
                        possible_list = PossibleList.body_legL
                        if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                            list.append(bone.name)
                            if RigTag.rig_id == 'DOG':
                                break
                        
            if context.scene.body_controllers.body_armR or context.scene.body_controllers.body_legR:
                col1 = row1.column(align = True)
                
                ##################### ARM.R Controls ##############                
                if context.scene.body_controllers.body_armR:
                    for bone in context.object.pose.bones: 
                        possible_list = PossibleList.body_armR
                        if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_UP_BAR')):
                            list.append(bone.name)
                            if RigTag.rig_id == 'DOG':
                                break              
                ##################### LEG.R Controls ##############                
                if context.scene.body_controllers.body_legR:
                    for bone in context.object.pose.bones: 
                        possible_list = PossibleList.body_legR
                        if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                            list.append(bone.name)
                            if RigTag.rig_id == 'DOG': 
                                break
            #if RigTag.different_rig:
            #PossibleList._body_list = list
                
        if RigTag.rig_id == 'DOG': 
            if bpy.context.scene.custom_prop_display.paw_control: #Paw Control ON
                row = col.row(align = True)
                row = col.row(align = True)
                row.prop(context.scene.body_controllers, "front_pawL", toggle=True, text='Front PAW', icon = 'TRIA_LEFT')
                row.prop(context.scene.body_controllers, "back_pawL", toggle=True, text='Back PAW', icon = 'TRIA_LEFT')
                row.operator("anim.keyframe_add_properties_multiple", text = "", icon = 'KEY_HLT').custom_prop_group = 'PAW'
                row.prop(context.scene.body_controllers, "front_pawR", toggle=True, text='Front PAW', icon = 'TRIA_RIGHT')
                row.prop(context.scene.body_controllers, "back_pawR", toggle=True, text='Back PAW', icon = 'TRIA_RIGHT')
                    
                list = []
                row1 = col.row(align = True)
                if context.scene.body_controllers.front_pawL or context.scene.body_controllers.back_pawL:
                    col1 = row1.column(align = True)     
                    ##################### Front PAW.L Controls ##############                
                    if context.scene.body_controllers.front_pawL:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.front_pawL
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_UP_BAR')):
                                list.append(bone.name)
                                break
                     ##################### Back PAW L Controls ##############                
                    if context.scene.body_controllers.back_pawL:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.back_pawL
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                                list.append(bone.name)
                                break
                            
                if context.scene.body_controllers.front_pawR or context.scene.body_controllers.back_pawR:
                    col1 = row1.column(align = True)
                    
                    ##################### FRONT PAW R Controls ##############                
                    if context.scene.body_controllers.front_pawR:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.front_pawR
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_UP_BAR')):
                                list.append(bone.name)
                                break
                   
                    ##################### Back PAW R Controls ##############                
                    if context.scene.body_controllers.back_pawR:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.back_pawR
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                                list.append(bone.name)
                                break
                #if RigTag.different_rig:
                #PossibleList._paw_list = list
                
            if bpy.context.scene.custom_prop_display.pivot_control: #Pivot Control ON
                row = col.row(align = True)
                row.prop(context.scene.body_controllers, "hand_pivL", toggle=True, text='Hand Piv', icon = 'TRIA_LEFT')
                row.prop(context.scene.body_controllers, "foot_pivL", toggle=True, text='Foot Piv', icon = 'TRIA_LEFT')
                row.operator("anim.keyframe_add_properties_multiple", text = "", icon = 'KEY_HLT').custom_prop_group = 'PIVOT'
                row.prop(context.scene.body_controllers, "hand_pivR", toggle=True, text='Hand Piv', icon = 'TRIA_RIGHT')
                row.prop(context.scene.body_controllers, "foot_pivR", toggle=True, text='Foot Piv', icon = 'TRIA_RIGHT')
                
                row1 = col.row(align = True)
                list = []
                if context.scene.body_controllers.hand_pivL or context.scene.body_controllers.foot_pivL:
                    col1 = row1.column(align = True)     
                    ##################### Hand Pivot L Controls ##############                
                    if context.scene.body_controllers.hand_pivL:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.hand_pivL
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_UP_BAR')):
                                list.append(bone.name)
                                break
                     ##################### Foot Pivot L Controls ##############                
                    if context.scene.body_controllers.foot_pivL:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.foot_pivL
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                                list.append(bone.name)
                                break
                                    
                if context.scene.body_controllers.hand_pivR or context.scene.body_controllers.foot_pivR:
                    col1 = row1.column(align = True)     
                    ##################### Hand Pivot R Controls ##############                
                    if context.scene.body_controllers.hand_pivR:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.hand_pivR
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_UP_BAR')):
                                list.append(bone.name)
                                break
                     ##################### Foot Pivot R Controls ##############                
                    if context.scene.body_controllers.foot_pivR:
                        for bone in context.object.pose.bones: 
                            possible_list = PossibleList.foot_pivR
                            if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                                list.append(bone.name)
                                break
                #if RigTag.different_rig:
                #PossibleList._pivot_list = list
                 
        # if RigTag.different_rig: 
            # b = bpy.context.scene.body_controllers
            # b.body_armL = False
            # b.body_armR = False
            # b.body_legL = False
            # b.body_legR = False
            # b.front_pawL = False
            # b.front_pawR = False
            # b.back_pawL = False
            # b.back_pawR = False
            # b.hand_pivL = False
            # b.hand_pivR = False
            # b.foot_pivL = False
            # b.foot_pivR = False 
            # RigTag.different_rig = False
        
    def _draw2(self, bone, col1, rig_id, possible_list = [], icon_name = 'NONE'):

        if bone.name in possible_list:
            run = False
            if rig_id == 'DOG':
                i = 0
                for layer in bpy.context.object.data.bones[bone.name].layers:
                    if layer and (i < 8 or 15 < i < 24):  
                        run = True
                    else: 
                        i = i + 1
            else:
                run = True
            if run:
                row = col1.row()
                box = row.box()
                col2 = box.column(align = True)
                sub_col = None
                key = False
                for custom_prop in sorted(bone.keys()):
                    if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI':
                        if type(bone[custom_prop]).__name__ == 'str':
                            row = col2.row(align = False)
                            prop_name = custom_prop
                            custom_prop = custom_prop.replace('_', ' ')
                            custom_prop = custom_prop.title()
                            row.label(custom_prop)
                            if bone[prop_name]:
                                row.label(bone[prop_name])
                            if not key: 
                                row.label(icon = icon_name)
                                row.operator("anim.keyframe_add_properties", text = "", icon = 'KEY_HLT').bone_name = bone.name
                                key = True
                            row = col2.row(align = True)
                            sub_col = row.column(align = True)
                        else:
                            if not sub_col: 
                                if not key: 
                                    row = col2.row(align = False)
                                    row.alignment = 'RIGHT'
                                    row.label(icon = icon_name)
                                    row.operator("anim.keyframe_add_properties", text = "", icon = 'KEY_HLT').bone_name = bone.name
                                    key = True
                                row = col2.row(align = True)
                                sub_col = row.column(align = True)
                            row = sub_col.row(align = True)
                            row.prop(bone,'["{}"]'.format(custom_prop), slider = True)
                return True
            else: 
                return False
        else:
            return False
          
class DisplayOptionsGUI(Panel):
    bl_label = "Display Options (Controls)"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'CharacterGUI'  
    
    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
    
    def draw(self, context):
        layout = self.layout 
        col = layout.column()
        row = col.row(align = True)
        row.alignment = 'LEFT'
        row.prop(context.scene.custom_prop_display, "general_control", text = "General")
        row.prop(context.scene.custom_prop_display, "body_control", text = "Body")
        row.prop(context.scene.custom_prop_display, "paw_control", text = "Paw")
        row.prop(context.scene.custom_prop_display, "pivot_control", text = "Pivot")
        
class AssetResolutionGUI(Panel):
    """
    Controllers for Animation
    """
    bl_label = "Object Resolution Swap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'CharacterGUI'                             
    
    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'OBJECT' 
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(align = True)
        split = row.split(percentage = 0.3, align = True)
        split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution)
        split = row.split(percentage = 1, align = True)
        split.operator("object.change_asset_resolution", text = "Change Resolution (takes a few seconds)", icon = 'FILE_REFRESH')
        row = col.row(align = True)
        row.label(text = "Resolution Swap will NOT work if the linked groups have orphan data", icon = 'ERROR')
  
class LightingControl(Panel):
    """
    Controllers for Lighting
    """
    bl_label = "Lighting Controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'CharacterGUI'
    
    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
            
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        god_node = context.object.pose.bones["ctl.god.C"]
        for custom_prop in sorted(god_node.keys()): 
            if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI':
                row = col.row(align = True)
                row.prop(god_node, '["{}"]'.format(custom_prop), slider = True)
                row.scale_y= 1.1
      
def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    register()
                    