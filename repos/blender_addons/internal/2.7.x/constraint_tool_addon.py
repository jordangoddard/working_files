bl_info = {
    "name": "Constraint Tool",
    "author": "Wayne Wu",
    "version": (2, 3, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Constraint Tool for Layout and Animation",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Constraint%20Tool.aspx",
    "category": "Tangent"}

import bpy
from bpy.types import Panel, Operator, PropertyGroup, UIList
import re


class TargetProperties(PropertyGroup):
    #Properties within the target list
    #name = bpy.props.StringProperty(name = "Name of the item")
    type = bpy.props.StringProperty(name = "Type of the item")
    rna_type = bpy.props.StringProperty(name = "Rna Type")
    proxy = bpy.props.StringProperty(name = "Proxy if available")
    subtarget = bpy.props.StringProperty(name = "subtarget")

    
class ConstraintToolProperties(PropertyGroup):

    try:
        bpy.utils.register_class(TargetProperties)
    except: pass    
    constraint_slave_list = bpy.props.CollectionProperty(type = TargetProperties)
    constraint_master_list = bpy.props.CollectionProperty(type = TargetProperties)
    constraint_slave_index = bpy.props.IntProperty() #---------------Active Constraint Target List (For removing)
    constraint_master_index = bpy.props.IntProperty() 
    constraint_tool_master_node = bpy.props.BoolProperty(
        name = "Create Toplevel Structure", 
        description = "Create intermediate master nodes (master null and master locator)", 
        default = False)
    constraint_tool_offset_num = bpy.props.IntProperty(name = "Offest Num", default = 1, min = 1, max = 10)

    
class CST_ObjectList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):       
        if item.rna_type == 'Object': 
            layout.prop(item, "name", text="", emboss=False, icon = 'MESH_CUBE')
        elif item.rna_type == 'Pose Bone':  
            row = layout.row(align = True)
            row.alignment = 'EXPAND'
            row.label(text= "%s" %item.name, icon = 'ARMATURE_DATA')
            row.prop(item, "subtarget", text="", emboss=False, icon = 'BONE_DATA') 

            
class CST_ConstraintToolGUI(Panel):
    bl_label = "Constraint Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Animation'
     
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        row = col.row()
        row.label("Child List")
        row.label("Target List")
        
        row = layout.row()
        row.template_list(
            "CST_ObjectList", "",
            context.scene.constraint_tool, "constraint_slave_list", 
            context.scene.constraint_tool, "constraint_slave_index")    
        col2 = row.column()
        rowsub = col2.row()
        colsub = rowsub.column(align=True)
        colsub.operator("scene.constraint_target_add", icon='ZOOMIN', text="").mode = 'SLAVES'
        colsub.operator("scene.constraint_target_remove", icon='ZOOMOUT', text="").mode = 'SLAVES'
        rowsub = col2.row()
        rowsub.separator()
        rowsub = col2.row()
        colsub = rowsub.column(align=True)
        colsub.operator("scene.constraint_target_clear", icon='X', text = "").mode = 'SLAVES'
        
        row.template_list(
            "CST_ObjectList", "",
            context.scene.constraint_tool, "constraint_master_list", 
            context.scene.constraint_tool, "constraint_master_index") 
        col2 = row.column()
        rowsub = col2.row()
        colsub = rowsub.column(align=True)
        colsub.operator("scene.constraint_target_add", icon='ZOOMIN', text="").mode = 'MASTERS'
        colsub.operator("scene.constraint_target_remove", icon='ZOOMOUT', text="").mode = 'MASTERS'
        rowsub = col2.row()
        rowsub.separator()
        rowsub = col2.row()
        colsub = rowsub.column(align=True)
        colsub.operator("scene.constraint_target_clear", icon='X', text = "").mode = 'MASTERS'
        
        row = layout.row(align = True)
        col1 = row.column(align = True)
        row = col1.row(align = True)
        row.label("Options:")
        row = col1.row(align = True)
        row.prop(context.scene.constraint_tool, "constraint_tool_master_node", text = "Create Toplevel Structure")
        row = col1.row(align = True)
        row.prop(context.scene.constraint_tool, "constraint_tool_offset_num", text = "Number of offsets")
        
        row = layout.row(align = True)
        row.operator("object.constraint_tool_run", text = "Constrain", icon = 'CONSTRAINT')
        row.scale_y = 1.2

        
class CST_ClearList(Operator):
    bl_label = "clear_target_list"
    bl_idname = "scene.constraint_target_clear"
    bl_description = "Clear List"
    bl_options = {'UNDO'}    
    
    mode = bpy.props.StringProperty(name = "list")
    
    def execute(self, context):
        if self.mode == 'SLAVES':
            bpy.context.scene.constraint_tool.constraint_slave_list.clear()
        elif self.mode == 'MASTERS':
            bpy.context.scene.constraint_tool.constraint_master_list.clear()
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)

        
class CST_AddTarget(Operator):
    bl_label = "add_target_list"
    bl_idname = "scene.constraint_target_add"
    bl_description = "Add selected item to target (slave or master) list. Multiselect is only available within the same context (eg. bones within same rig)"
    bl_options = {'UNDO'}    
    
    mode = bpy.props.StringProperty(name = "mode")
    
    def execute(self, context):
        if self.mode == 'SLAVES':
            if bpy.context.active_object.mode == 'POSE':     
                for bone in bpy.context.selected_pose_bones: 
                    list = bpy.context.scene.constraint_tool.constraint_slave_list.add()
                    list.name = bpy.context.object.name #---------------- Selected Obect's name
                    list.subtarget = bone.name #------------------------- Subtarget Name eg. Bone
                    list.type = bpy.context.object.type #---------------- Object type eg. Armature
                    list.rna_type = bone.rna_type.name #----------------- Rna_type eg. Pose Bone
                    if bpy.context.object.proxy: 
                        list.proxy = bpy.context.object.proxy.name #----- If object is a proxy, proxy name is the Rig Name
                    else: 
                        list.proxy = bpy.context.object.name #Rig name
            elif bpy.context.active_object.mode == 'OBJECT':
                for obj in bpy.context.selected_objects: 
                    list = bpy.context.scene.constraint_tool.constraint_slave_list.add()
                    list.name = obj.name
                    list.type = obj.type
                    list.rna_type = obj.rna_type.name
        elif self.mode == 'MASTERS':
            if bpy.context.active_object.mode == 'POSE':     
                for bone in bpy.context.selected_pose_bones: 
                    list = bpy.context.scene.constraint_tool.constraint_master_list.add()
                    list.name = bpy.context.object.name #---------------- Selected Obect's name
                    list.subtarget = bone.name #------------------------- Subtarget Name eg. Bone
                    list.type = bpy.context.object.type #---------------- Object type eg. Armature
                    list.rna_type = bone.rna_type.name #----------------- Rna_type eg. Pose Bone
                    if bpy.context.object.proxy: 
                        list.proxy = bpy.context.object.proxy.name #----- If object is a proxy, proxy name is the Rig Name
                    else: 
                        list.proxy = bpy.context.object.name #Rig name
            elif bpy.context.active_object.mode == 'OBJECT':
                for obj in bpy.context.selected_objects: 
                    list = bpy.context.scene.constraint_tool.constraint_master_list.add()
                    list.name = obj.name
                    list.type = obj.type
                    list.rna_type = obj.rna_type.name
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)

        
class CST_RemoveTarget(Operator):
    bl_label = "constraints_target_remove"
    bl_idname = "scene.constraint_target_remove"
    bl_description = "Remove highlited item from the list"
    bl_options = {'UNDO'}  
    
    mode = bpy.props.StringProperty(name = "mode")
    
    def execute(self, context):
        constraint_tool = bpy.context.scene.constraint_tool
        if self.mode == 'SLAVES':
            constraint_tool.constraint_slave_list.remove(constraint_tool.constraint_slave_index)
        elif self.mode == 'MASTERS':
            constraint_tool.constraint_master_list.remove(constraint_tool.constraint_master_index)  
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)

        
class CST_RunConstraintTool(Operator):
    bl_label = "Run_constraint_tool"
    bl_idname = "object.constraint_tool_run"
    bl_description = "Run Constraint Tool"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        scene = bpy.context.scene
        ct = ConstraintTool(
            scene.constraint_tool.constraint_tool_master_node, 
            scene.constraint_tool.constraint_master_list,
            scene.constraint_tool.constraint_slave_list,
            scene.constraint_tool.constraint_tool_offset_num)
        ct.execute()
        scene.constraint_tool.constraint_master_list.clear()
        scene.constraint_tool.constraint_slave_list.clear()
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)

        
class ConstraintTool(object):
    
    def __init__(self, master_node = False, master_list = [], slave_list = [], offset_num = 1):
    
        self.scene_name = bpy.context.scene.name
        self.master_node = master_node
        self.master_list = master_list
        self.slave_list = slave_list
        self.offset_num = offset_num
        try:
            self.group = bpy.data.groups["grp.stuff"]
        except: 
            self.group = bpy.data.groups.new("grp.stuff")
              
        import addon_utils
        try:
            addon_utils.enable("_wm_properties_new", default_set = True)
        except:
            self.report({'ERROR'}, "Could not enable module: WM_OT_Properties")      
           
    def execute(self):
        for master_obj in self.master_list: 
            master = bpy.context.scene.objects[master_obj.name]
            self.master_location = master.location #-------------------------------------------------location of master
            self.master_short_name = self.simplify_name(master_obj.name)
            if self.master_node: 
                if master_obj.rna_type == 'Pose Bone':
                    #self.master_short_name = "%s/%s" %(self.simplify_name(master_obj.name))
                    if master.proxy: 
                        master = master.proxy #-----------------------------------------------------------if it is a proxy, then master becomes the proxy
                    master_location = bpy.context.active_pose_bone.head
                master_null = self.create_master_null(master, master_obj, self.master_short_name)
                master_empty = self.create_master_offset(master_obj, master_null, self.master_short_name)
            
            for target in self.slave_list: 
                self.slave_short_name = self.simplify_name(target.name)
                if self.master_node:
                    slave_null = self.create_slave_null(target, master, master_obj, self.slave_short_name, master_empty)
                else: 
                    slave_null = self.create_slave_null(target, master, master_obj, self.slave_short_name)
                
                i = 0
                slave_offset = slave_null
                while(i < self.offset_num):
                    slave_empty = self.create_slave_offset(target, slave_offset, master, master_obj, self.slave_short_name)
                    slave_offset = slave_empty
                    
                    i = i + 1
                
                self.make_active(bpy.data.objects[target.name])
                if target.rna_type == 'Pose Bone':
                    bpy.context.object.data.bones.active = bpy.context.object.data.bones[target.subtarget] #------------Set active bones to current one
                    if bpy.context.active_object.mode != 'POSE':
                        bpy.ops.object.mode_set(mode='POSE')
                    bone = bpy.context.object.pose.bones[target.subtarget]
                    bpy.ops.pose.constraint_add(type = 'COPY_LOCATION')
                    constraint = bone.constraints[len(bone.constraints)-1]
                    constraint.target = slave_empty
                    copy_loc_name = constraint.name
                    bpy.ops.pose.constraint_add(type = 'COPY_ROTATION')
                    constraint = bone.constraints[len(bone.constraints)-1]
                    constraint.target = slave_empty
                    copy_rot_name = constraint.name
                    self.make_active(slave_null)
                    custom_prop_name = "%s/%s" %(target.name, target.subtarget)
                    if len(custom_prop_name) > 63:
                        subtract = len(custom_prop_name)-63
                        custom_prop_name = custom_prop_name[:-subtract]
                    bpy.ops.wm.properties_new_add(data_path = "object", prop_name = custom_prop_name, default_value = "1.0", default_max = 1.0, default_min = 0.0)
                    self.make_active(bpy.data.objects[target.name])
                    self.create_driver("pose.bones[\"%s\"].constraints[\"%s\"].influence" %(target.subtarget, copy_loc_name), slave_null, custom_prop_name)
                    self.create_driver("pose.bones[\"%s\"].constraints[\"%s\"].influence" %(target.subtarget, copy_rot_name), slave_null, custom_prop_name)
                    
                else: 
                    if bpy.context.active_object.mode != 'OBJECT':
                        bpy.ops.object.mode_set(mode='OBJECT')
                    obj = bpy.data.objects[target.name]
                    new_constraint = obj.constraints.new(type = 'COPY_LOCATION')
                    new_constraint.target = slave_empty   
                    copy_loc_name = new_constraint.name
                    new_constraint = obj.constraints.new(type = 'COPY_ROTATION')
                    new_constraint.target = slave_empty
                    copy_rot_name = new_constraint.name
                    self.make_active(slave_null)
                    custom_prop_name = "%s" %(target.name)
                    if len(custom_prop_name) > 63:
                        subtract = len(custom_prop_name)-63
                        custom_prop_name = custom_prop_name[:-subtract]
                    bpy.ops.wm.properties_new_add(data_path = "object", prop_name = custom_prop_name, default_value = "1.0", default_max = 1.0, default_min = 0.0)
                    self.make_active(bpy.data.objects[target.name])
                    self.create_driver("constraints[\"%s\"].influence" %(copy_loc_name), slave_null, custom_prop_name)
                    self.create_driver("constraints[\"%s\"].influence" %(copy_rot_name), slave_null, custom_prop_name)                                          
                                                
                bpy.context.scene.update()
    
    def create_driver(self, data_path, slave_offset, custom_prop_name):
        new_driver = bpy.context.object.driver_add(data_path)
        new_driver.driver.expression = "var"
        try: 
            var = new_driver.driver.variables[0]
        except: 
            var = new_driver.driver.variables.new()     
        var.name = "var"
        target = var.targets[0]
        target.id = slave_offset
        target.data_path = "[\"%s\"]" %custom_prop_name

    def create_master_null(self, master, master_obj, name):
       
        master_null_name = "cst.%s.masternull" %name 
        master_null = bpy.data.objects.new(master_null_name, None)
        master_null.empty_draw_type = 'PLAIN_AXES'
        master_null.location = (0,0,0) #---------------------------------------------------Location does not matter since it's copying transformation
        new_constraint = master_null.constraints.new(type = 'COPY_LOCATION')
        new_constraint.target = master
        if master_obj.rna_type == 'Pose Bone':
            new_constraint.subtarget = master_obj.subtarget
        new_constraint = master_null.constraints.new(type = 'COPY_ROTATION')
        new_constraint.target = master
        if master_obj.rna_type == 'Pose Bone':
            new_constraint.subtarget = master_obj.subtarget
        self.group.objects.link(master_null)
        bpy.context.scene.objects.link(master_null) 
        return master_null
     
    def create_master_offset(self, master_obj, master_null, name):
        master_empty_name = "cst.%s.masteroffset" %name
        master_empty = bpy.data.objects.new(master_empty_name, None)
        master_empty.empty_draw_type = 'PLAIN_AXES'
        master_empty.location = self.master_location #-----------------------------------------Create the master_empty at the master's location
        self.group.objects.link(master_empty)
        bpy.context.scene.objects.link(master_empty)
        self.make_active(master_null)
        master_empty.select = True #------------------------------------------------------Select the master_empty
        bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True) #---------------Parent the nulls but keep transformation      
        return master_empty
        
    def create_slave_null(self, target, master, master_obj, name, master_empty = None):
    
        short_name = self.simplify_name(name)
        slave_null_name = "cst.%s/%s.null" %(self.master_short_name, short_name) 
        slave_null_exist = False           
        slave_null = bpy.data.objects.new(slave_null_name, None)
        slave_null.empty_draw_type = 'PLAIN_AXES'
        self.group.objects.link(slave_null)
        bpy.context.scene.objects.link(slave_null)        
        constraint_num = len(slave_null.constraints)
        new_constraint = slave_null.constraints.new(type = 'COPY_LOCATION')
        if self.master_node: #------------------------------------------------------Master Node is enabled
            new_constraint.target = master_empty #----------------------------------Target is the master empty
        else:
            new_constraint.target = master
            try:
                new_constraint.subtarget = master_obj.subtarget
            except:
                pass
        new_constraint = slave_null.constraints.new(type = 'COPY_ROTATION')
        if self.master_node:
            new_constraint.target = master_empty
        else:
            new_constraint.target = master
            try:
                new_constraint.subtarget = master_obj.subtarget
            except: 
                pass  
        return slave_null
             
    def create_slave_offset(self, target, slave_null, master, master_obj, name): 
        
        slave_empty_name = "cst.%s.offset" %(name) 
        slave_empty = bpy.data.objects.new(slave_empty_name, None)
        slave_empty.empty_draw_type = 'PLAIN_AXES'    
        
        if target.rna_type == 'Pose Bone': 
            bone = bpy.data.objects[target.name].pose.bones[target.subtarget]
            bone_matrix = bone.matrix.copy()
            slave_empty.matrix_world = bpy.data.objects[target.name].matrix_world*bone_matrix
            # slave_empty.location = bone.matrix.to_translation()
            # slave_empty.rotation_euler = bone.matrix.to_euler()
            # slave_empty.scale = bone.matrix.to_scale()
        else: 
            slave_empty.location = bpy.data.objects[target.name].matrix_world.to_translation()
            slave_empty.rotation_euler = bpy.data.objects[target.name].matrix_world.to_euler()
        
        self.group.objects.link(slave_empty)
        bpy.context.scene.objects.link(slave_empty)
        self.make_active(slave_empty)
        
        #Create the custom properties
        bpy.ops.wm.properties_tag_add(data_path = "object", prop_name = "master_name", default_value = master_obj.name)
        if master_obj.rna_type == 'Pose Bone': 
            bpy.ops.wm.properties_tag_add(data_path = "object", prop_name = "master_subtarget", default_value = master_obj.subtarget)
        else:
            bpy.ops.wm.properties_tag_add(data_path = "object", prop_name = "master_subtarget", default_value = "")
        
        bpy.ops.wm.properties_tag_add(data_path = "object", prop_name = "object_name", default_value = target.name)
        if target.rna_type == 'Pose Bone':
            bpy.ops.wm.properties_tag_add(data_path = "object", prop_name = "bone_name", default_value = target.subtarget)
        else: 
            bpy.ops.wm.properties_tag_add(data_path = "object", prop_name = "bone_name", default_value = "")
        
        self.make_active(slave_null)
        slave_empty.select = True 
        bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True) #--------------------------------Parent the nulls but keep transformation      
        bpy.context.scene.update()
          
        return slave_empty  
     
    def simplify_name(self, name):
        """
        Simplify name by getting rid of the prefix
        """
        match = re.match(r'\w+\.(\S+)', name)
        if match: 
            short_name = match.group(1)
            return short_name
        else: 
            return name
    
    def make_active(self, object):
        """
        Make object active
        """
        for obj in bpy.context.scene.objects: #----------------------------------------------------------------Deselect all objects
            obj.select = False
        object.select = True
        bpy.context.scene.objects.active = object #--------------------------------------Select the rig object  
        
         

class INF_InfluenceConstrolsGUI(Panel):
    bl_label = "Influence Controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Animation'
    
    bpy.types.Scene.influence_controls_mode = bpy.props.EnumProperty(
        items = [('DEFAULT', 'All', 'Default'), ('SELECTION', 'Selection', 'Selection')],
        name = "Display Mode"
        )
    
    def draw(self, context):
        layout = self.layout      
        
        layout.prop(context.scene, "influence_controls_mode", expand = True)
        
        col = layout.column(align = False)      
        i = 0
        
        object_list = []
        
        if bpy.context.scene.influence_controls_mode == 'DEFAULT':
            object_list = self.find_all_drivers()
            
        elif bpy.context.scene.influence_controls_mode == 'SELECTION':
            object_list = self.find_selected_drivers()
            
        for item in object_list:   
            box = col.box()
            subcol = box.column(align = False)
            is_named = False
            for obj in bpy.context.scene.objects: 
                if obj.name.startswith('cst') and (".offset" in obj.name):
                    try: 
                        obj.parent[item]
                    except:
                        pass
                    else:
                        if not is_named:
                            subrow = subcol.row(align = False)
                            subrow.label(obj['object_name'])
                            subrow.label(obj['bone_name'])
                            #subrow.operator("anim.keyframe_influences_add", text ="", icon = 'KEY_HLT').index
                            is_named = True
                        row = subcol.row()
                        row.label(icon = 'CONSTRAINT')
                        row.prop(obj.parent, '["{}"]'.format(item), slider = True, text = "%s/%s" %(obj['master_name'], obj['master_subtarget']))
                        row.scale_y = 1
        
        # #for item in GlobalVar.data_list: 
                # box = col.box()
                # subcol = box.column(align = True)
                # subrow = subcol.row(align = False)
                # if item.rna_type.name == 'Pose Bone':
                    # subrow.label(item.id_data.name)
                # subrow.label(item.name)
                # #subrow.operator("anim.constraint_switch_master", text = "", icon = 'ROTACTIVE').index = i
                # subrow.operator("anim.keyframe_influences_add", text ="", icon = 'KEY_HLT').index = i
                # prev_master = None
                
                # for constraint in item.constraints: 
                    # if constraint.type == 'COPY_LOCATION' or constraint.type == 'COPY_ROTATION':
                        # if constraint.target:
                            # master_text = "%s/%s" %(constraint.target['master_name'], constraint.target['master_subtarget'])
                            # if master_text != prev_master:
                                # subrow = box.row(align = True)
                                # subrow.label(text = master_text, icon = 'CONSTRAINT')
                                # prev_master = master_text
                            # subrow = box.row(align = True)
                            # subrow.prop(constraint, "influence", text = constraint.type)
                # i = i + 1
    
    def find_all_drivers(self):
    
        object_list = []
        for obj in bpy.context.scene.objects: 
            if obj.name.startswith('cst') and obj.name.endswith('.null'):
                for prop in obj.keys():
                    if prop not in object_list and prop != '_RNA_UI': 
                        object_list.append(prop)
        return object_list                
    
    
    def find_selected_drivers(self):
    
        object_list = []
        for obj in bpy.context.selected_objects: 
            if obj.name.startswith('cst') and obj.name.endswith('.null'):
                for prop in obj.keys():
                    if prop not in object_list and prop != '_RNA_UI': 
                        object_list.append(prop)
        return object_list    
        
        
    def find_locators(self):
        list = []
        scene_name = bpy.context.scene.name
        for obj in bpy.context.scene.objects: 
            if obj.name.startswith('cst') and obj.name.endswith('.offset'):
                obj_name = obj['object_name']
                if obj['bone_name']:
                    bone_name = obj['bone_name']
                    bone = bpy.data.objects[obj_name].pose.bones[bone_name]
                    if bone not in list:
                        list.append(bpy.data.objects[obj_name].pose.bones[bone_name])
                else:
                    object = bpy.data.objects[obj_name]
                    if object not in list:
                        list.append(object)                 
        return list 
 
 
class INF_SwitchMaster(Operator):
    bl_label = "switch_master"
    bl_idname = "anim.constraint_switch_master"
    bl_description = "Switch the master by changing the influence"
    bl_options = {'UNDO'}   
    
    index = bpy.props.IntProperty(name = "index")
    
    """
    NO LONGER USED
    """  
    
    def execute(self, context):
        item = GlobalVar.data_list[self.index]
        #Sort out master_list
        master_list = []
        for constraint in item.constraints: 
            if constraint.type == 'COPY_LOCATION' or constraint.type == 'COPY_ROTATION':
                if constraint.target and constraint.target not in master_list:
                    master_list.append(constraint.target)
        
        #find current index 
        # current_index = 0 
        # for constraint in item.constraints: 
            # if constraint.type == 'COPY_LOCATION' or constraint.type == 'COPY_ROTATION':
                # if constraint.target in master_list and constraint.influence == 1:
                    # break
                # else: 
                    # current_index = current_index + 1
        #The Current Index will record which one it's currently on
        i = GlobalVar.current_index + 1
        if i >= len(master_list):
            i = 0
        for constraint in item.constraints:
            if constraint.type == 'COPY_LOCATION' or constraint.type == 'COPY_ROTATION':
                if constraint.target == master_list[i]:
                    constraint.influence = 1
                else: 
                    constraint.influence = 0
        GlobalVar.current_index = i
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)

        
class INF_KeyInfluence(Operator):
    bl_label = "key_influence"
    bl_idname = "anim.keyframe_influences_add"
    bl_description = "Add Keyframe for the influence for Copy Rotation and Copy Location"
    bl_options = {'UNDO'}  
    
    index = bpy.props.IntProperty(name = "index")
    
    """
    NO LONGER USED
    """  
    
    def execute(self, context):
        item = GlobalVar.data_list[self.index]
        for constraint in item.constraints: 
            if constraint.type == 'COPY_LOCATION' or constraint.type == 'COPY_ROTATION':
                if item.rna_type.name == 'Pose Bone':
                    object = item.id_data
                    object.keyframe_insert("pose.bones[\"%s\"].constraints[\"%s\"].influence" %(item.name, constraint.name))
                else: 
                    item.keyframe_insert("constraints[\"%s\"].influence" %constraint.name)
        bpy.context.scene.update()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)

     
def menu_draw(self, context):
    """
    Menu ShortCut for using the constraint tool (Not activated)
    """
    layout = self.layout
    layout.operator("scene.constraint_target_clear", text = "CONSTRAINT TOOL: Clear Target List", icon = 'X')
    layout.operator("scene.constraint_target_add", text = "CONSTRAINT TOOL: Add as Target", icon = 'ZOOMIN')
    layout.operator("object.constraint_tool_run", text = "CONSTRAINT TOOL: Run Constraint Tool",  icon = 'PLAY').mode = bpy.context.scene.constraint_tool_mode
   
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.constraint_tool = bpy.props.PointerProperty(type = ConstraintToolProperties)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.constraint_tool
     
if __name__ == "__main__":
    register()    
     