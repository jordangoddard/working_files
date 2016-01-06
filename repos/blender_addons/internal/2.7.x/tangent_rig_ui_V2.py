bl_info = {
    "name": "Animation CharacterGUI",
    "author": "Wayne Wu, David Hearn",
    "version": (1, 3, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Character GUI for animation",
    "wiki_url" : "https://tangentanimation.sharepoint.com/wiki/Pages/Character%20GUI.aspx",
    "warning": "The addon still in progress! Make a backup!",
    "category": "Tangent"}

import addon_utils
import bpy
import re
from bpy.types import PropertyGroup, Panel, Operator
    
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
    """
    Display Options for the controllers. Can only be accessed through code as of now
    """
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
    except: pass
    bpy.types.Scene.face_controllers = bpy.props.EnumProperty(
        items = [('MOUTH', 'MOUTH', "Mouth controls"),
            ('EYE', 'EYE', "Eye controls"),
            ('FOLLOW', 'FOLLOW', "Follow controls"),
            ('GOD', 'GOD', "God controls"),
            ('SPECIAL', 'SPECIAL', "Special controls"),
            ('NONE', 'NONE', "Collapse")
            ],
        name = "different face controls" )       
    bpy.types.Object.selection_set_name = bpy.props.StringProperty(name = "name of selection set", default = "Selection Set")
    bpy.types.Object.special_custom_prop = bpy.props.CollectionProperty(type = SpecialCustomProp)
    bpy.types.Scene.custom_prop_display = bpy.props.PointerProperty(type = DisplayOptionProperty)
    bpy.types.Scene.body_controllers = bpy.props.PointerProperty(type=BodyControlProperty, name = "Body Controllers")
    
    def available_groups(self, context):
        items = []
        try:
            filepath = context.object.dupli_group.library.filepath
        except:
            pass
        else:
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                for group in data_from.groups:
                    items.append((group, group, group))
        return items          

class RigTag(object):
    """
    Rig Properties to be used within this addon 
    """
    rig_id = None #Classify between HUMAN or DOG
    current_rig = None  #Store the current active rig
    different_rig = False
                
class ANIM_LY_RigLayersGUI(Panel):
    """Creates a custom Rig UI layers panel"""
    bl_label = "Control Layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Character'

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
   
    def draw_layer(self, layout, layer_name, layer_index):
        layout.prop(bpy.context.active_object.data, 'layers', index = layer_index, toggle = True, text=layer_name)
        layout.operator("scene.select_controllers", icon = 'HAND', text = "").layer = layer_index
        layout.operator("anim.layer_key_transformation", icon = 'KEY_HLT', text = "").layer_index = layer_index
    
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
            self.draw_layer(row, "Body", 0)
            
            col.separator()
            row = col.row(align = True)
            self.draw_layer(row, "Torso", 1)
            row = col.row(align = True)
            self.draw_layer(row, "Head Neck", 2)
            
            col.separator()
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Front Left Leg", 3)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Front Right Leg", 4)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Back Left Leg", 5)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Back Right Leg", 6)
            
            col.separator()
            row = col.row(align = True)
            self.draw_layer(row, "Tail", 7)
            row = col.row(align = True)
            self.draw_layer(row, "Face", 16)
            
            col.separator()
            row = col.row(align = True)
            self.draw_layer(row, "Upper Face Primary", 17)
            row = col.row(align = True)
            self.draw_layer(row, "Upper Face Secondary", 18)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Ear", 22)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Ear", 23)
            row = col.row(align = True)
            self.draw_layer(row, "Lower Face Primary", 19)
            row = col.row(align = True)
            self.draw_layer(row, "Lower Face Secondary", 20)
            row = col.row(align = True)
            self.draw_layer(row, "Tongue and Teeth", 21)
               
        elif RigTag.rig_id == 'HUMAN': 
            row = col.row(align = True)
            self.draw_layer(row, "Body", 28)
            
            col.separator()
            row = col.row(align = True)
            self.draw_layer(row, "Torso", 3)
            row = col.row(align = True)
            self.draw_layer(row, "Torso Tweakers", 4)
            
            col.separator()
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Arm IK", 7)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Arm IK", 10)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Arm FK", 8)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Arm FK", 11)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Arm Tweakers", 9)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Arm Tweakers", 12)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Hand", 6)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Hand", 5)
            
            col.separator()
            
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Leg IK", 13)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Leg IK", 16)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Leg FK", 14)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Leg FK", 17)
            row = col.row()
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Left Leg Tweakers", 15)
            col2 = row.column()
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Right Leg Tweakers", 18)
            
            col.separator()
            
            row = col.row(align = True)
            self.draw_layer(row, "Eyes", 0)
            row = col.row(align = True)
            self.draw_layer(row, "Main Face", 1)
            row = col.row(align = True)
            self.draw_layer(row, "Secondary Face", 2)                 
            
            col.separator()
            row = col.row(align = False)
            col2 = row.column (align = True)
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Extra", 19)
            col2 = row.column (align = True)
            row2 = col2.row(align = True)
            self.draw_layer(row2, "Extra", 20)  
            row = col.row(align = True)
            self.draw_layer(row, "Extra", 21)      
            self.draw_layer(row, "Extra", 22)    
            self.draw_layer(row, "Extra", 23)  
            
        #Selection Set Tools
        col.separator()    
        row = col.row()
        col2 = row.column(align = True)
        row = col2.row(align = True)
        row.prop(context.object, "selection_set_name", icon ='SORTALPHA', text = "Selection Set")
        row.operator("object.add_selection_set", icon = "ZOOMIN", text = "")
        row.operator("object.append_selection_set", icon = 'APPEND_BLEND', text = "")
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

class ANIM_LY_AppendSelectionSet(Operator):
    bl_label = "Append Selection Set"
    bl_idname = "object.append_selection_set"
    bl_description = "Append predefined selection Set"
    bl_options = {'UNDO'}    
    
    def invoke(self, context, event):
        #Add Predefined Selection Set Here
        pass
        return {'FINISHED'}
    
class ANIM_LY_AddSelectionSet(Operator):
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
    
class ANIM_LY_RemoveSelectionSet(Operator):  
    bl_label = "Remove Selection Set"
    bl_idname = "object.remove_selection_set"
    bl_description = "Remove Selection Set"
    bl_options = {'UNDO'}
    
    set_index = bpy.props.IntProperty(name = "selection set index")
    
    def invoke(self, context, evnet):
        bpy.context.object.active_selection_set = self.set_index
        bpy.ops.pose.selection_set_remove()
        return {'FINISHED'}
    
class ANIM_LY_ToggleSelectionSet(Operator):
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

class ANIM_LY_AddSetKeyTransformation(Operator):
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
              
class ANIM_LY_AddLayerKeyTransformation(Operator):
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
        
class ANIM_LY_SelectControllers(Operator):
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
    
class ANIM_CTL_CustomControlsGUI(Panel):
    bl_label = "Animation Controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Character'            

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
                    search = re.search('iris', custom_prop)
                    exceptions = ['rigifty_parameters', '_RNA_UI', 'Highlite_intensity', 'Highlite_Size', 'Eye_highlite_world_lock', 'highlite_intensity', 'highlite_size', 'lock_eye_highlite_world']
                    if (custom_prop not in exceptions) and not search:
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
            
        row = col.row()
        if bpy.context.scene.custom_prop_display.body_control: #Body Control ON
            #Display Toggles for body controllers
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
                                #Allow human to continue to the loop, but not dog
                                break
                ##################### LEG.L Controls ##############                
                if context.scene.body_controllers.body_legL:
                    for bone in context.object.pose.bones: 
                        possible_list = PossibleList.body_legL
                        if (self._draw2(bone, col1, RigTag.rig_id, possible_list, 'TRIA_DOWN_BAR')):
                            list.append(bone.name)
                            if RigTag.rig_id == 'DOG':
                                #Allow human to continue to the loop, but not dog
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
            
        #TODO* Potentailly combine everything to ARM and LEGS    
        if RigTag.rig_id == 'DOG': 
            self.draw_dog(context, col)
                 
    def draw_dog(self, context, col):
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
                            #string formating
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
             
class ANIM_CTL_AddSpecial(Operator):
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
        
class ANIM_CTL_RemoveSpecial(Operator):
    bl_label = "Remove_special_custom_prop"
    bl_idname = "scene.special_custom_prop_remove"
    bl_description = "Remove special custom properties"
    bl_options = {'UNDO'}
    
    index = bpy.props.IntProperty(name = "index")
    
    def invoke(self, context, event):
        bpy.context.object.special_custom_prop.remove(self.index)
        return {'FINISHED'}
        
class ANIM_CTL_KeyProperties(Operator):
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

class ANIM_CTL_KeyMultipleProperties(Operator):
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
 
            
class ANIM_OBJ_AssetResolutionGUI(Panel):
    """
    Controllers for Animation
    """
    bl_label = "Object Resolution Swap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Character'                             
       
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        row = col.row(align = True)
        split = row.split(percentage = 0.3, align = True)
        if context.scene.asset_resolution == 'HIGH':
            split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution, icon = 'SOLID')
        elif context.scene.asset_resolution == 'MID':
            split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution, icon = 'ANTIALIASED')
        elif context.scene.asset_resolution == 'LOW':
            split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution, icon = 'ALIASED')
        split = row.split(percentage = 1, align = True)
        split.operator("object.change_asset_resolution", text = "Change Resolution (takes a few second)", icon = 'FILE_REFRESH')
        row = col.row()
        row.label(text = "Resolution Swap will NOT work if the linked groups have orphan data", icon = 'ERROR')
             
class LIGHT_LightingControlsGUI(Panel):
    """
    Controllers for Lighting
    """
    bl_label = "Lighting Controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Character'
    
    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
            
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        row = col.row()
        row.alignment = 'RIGHT'
        row.operator("scene.render_mode_reset", text = "Reset to Default", icon = 'FILE_REFRESH')
        god_node = context.object.pose.bones["ctl.god.C"]
        for custom_prop in sorted(god_node.keys()): 
            if custom_prop != 'rigify_parameters' and custom_prop != '_RNA_UI':
                row = col.row(align = True)
                row.prop(god_node, '["{}"]'.format(custom_prop), slider = True)
                row.scale_y= 1.0
        
class LIGHT_ResetGod(Operator):
    """
    Reset god node's custom properties to default
    """
    bl_label = "reset_render_mode"
    bl_idname = "scene.render_mode_reset"
    bl_description = "Switch Render Mode"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        import addon_utils
        try:
            addon_utils.enable("_wm_properties_new", default_set = True)
        except:
            self.report({'ERROR'}, "Could not enable module: WM_OT_Properties")
        else: 
            god_node = context.object.pose.bones["ctl.god.C"]
            props = bpy.context.object.pose.bones["ctl.god.C"].keys()
            print(props)
            for item in props: 
                if item == "Collar_viz":
                    god_node[item] = 1
                if item in ["Cornea_viz", "viewport_viz_cornea"]:
                    god_node[item] = 1
                if item in ["Eye_highlite_world_lock", "lock_eye_highlite_world"]:
                    god_node[item] = 0.0
                if item in ["Eye_world_lock", "lock_eye_world"]:
                    god_node[item] = 0.0
                if item in ["Hair", "viewport_viz_hair"]:
                    god_node[item] = 0
                if item in ["Highlite_Size", "highlite_size"]:
                    god_node[item] = 1.0
                if item in ["Highlite_intensity", "highlite_intensity"]:
                    god_node[item] = 8.0
                if item in ["viewport_viz_highlite_proxy"]:
                    god_node[item] = 0
                if item in ["Proxy_pupil_viz", "viewport_viz_pupil_proxy"]:
                    god_node[item] = 1
                if item in ["Smoothing", "viewport_viz_smoothing"]:
                    god_node[item] = 0
                if item == "highlite_iris_intensity":
                    god_node[item] = 3.0              
                if item == "highlite_iris_manual":
                    god_node[item] = 0.2  
                if item == "highlite_iris_offset":
                    god_node[item] = 0.4  
                if item == "highlite_iris_size":
                    god_node[item] = 1.0              
            bpy.context.scene.update()
        return {'FINISHED'}
         
    def invoke(self, context, event):
        return self.execute(context)
                  
                  
def register():
    bpy.utils.register_module(__name__)

    addon_name = "proxy_refresh"
    addon_state = addon_utils.check(addon_name)                                                # Returns: loaded_default, loaded_state
    addon_state_pr = addon_state[1]
    if not addon_state_pr:
        default_set=True                                                                       # From addon_utils function
        persistent=True                                                                        # From addon_utils function
        result = addon_utils.enable(addon_name, default_set, persistent)
        if result is None:                                                                     # Add-on not found
            addon_state_pr = False

    addon_name = "addon_create_animation_scene"
    addon_state = addon_utils.check(addon_name)                                                # loaded_default, loaded_state
    addon_state_acas = addon_state[1]
    if not addon_state_acas:
        default_set=True                                                                       # From addon_utils function
        persistent=True                                                                        # From addon_utils function
        result = addon_utils.enable(addon_name, default_set, persistent)
        if result is None:                                                                     # Add-on not found
            addon_state_acas = False

    addon_name = "tangent_animation_outliner"
    addon_state = addon_utils.check(addon_name)                                                # loaded_default, loaded_state
    addon_state_acas = addon_state[1]
    if not addon_state_acas:
        default_set=True                                                                       # From addon_utils function
        persistent=True                                                                        # From addon_utils function
        result = addon_utils.enable(addon_name, default_set, persistent)
        if result is None:                                                                     # Add-on not found
            addon_state_acas = False

def unregister():
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    register()
                    