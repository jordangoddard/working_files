bl_info = {
    "name": "Scene Outliner / Resolution Manager",
    "author": "Wayne Wu",
    "version": (1, 1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Scene Outliner / Resolution Manager",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Scene%20Outliner.aspx",
    "category": "Tangent"}

import datetime
import addon_utils                                                                                 # Built-in script for handling add-on registration
import bpy 
from bpy.types import Panel, UIList, PropertyGroup, Operator


class TA_LocalObject(PropertyGroup):
    """
    xxxx
    """
    def get_local_item(self):
        return bpy.context.scene.objects[self.name].select 
        
    def set_select_local(self, value):
        bpy.context.scene.objects[self.name].select = value  
     
    type = bpy.props.StringProperty(name = "Type tag")
    select_item = bpy.props.BoolProperty(name = "Select the item", get = get_local_item, set = set_select_local)
    

class TA_Object(PropertyGroup):

    def get_proxy_name(self):
        try:
            for obj in bpy.context.scene.objects: 
                if obj.proxy_group == bpy.context.scene.objects[self.name]:
                    return obj.name
                    
            #Asset resolution has been changed, find in a different way        
            obj = bpy.context.scene.objects[self.name]
            filepath = obj.dupli_group.library.filepath
            for object in bpy.context.scene.objects: 
                if object.proxy and object.proxy.library.filepath == filepath:
                    return object.name
            return ""
        except KeyError: 
            return ""
            
    def get_group_select(self):
        return bpy.context.scene.objects[self.name].select 
        
    def set_group_select(self, value):
        bpy.context.scene.objects[self.name].select = value
    
    def get_rig_select(self):
        if self.proxy:
            return bpy.context.scene.objects[self.proxy].select
        else: 
            return False
            
    def set_rig_select(self, value):
        if self.proxy:
            bpy.context.scene.objects[self.proxy].select = value
    
    def get_both_select(self):
        if self.select_group and self.select_rig:
            return True
        else:
            return False
    
    def set_both_select(self, value):
        self.select_group = value
        self.select_rig = value
     
    type = bpy.props.StringProperty(name = "Type tag")
    proxy = bpy.props.StringProperty(name = "Proxy", get = get_proxy_name)
    both = bpy.props.BoolProperty(name = "Select Both", get = get_both_select, set = set_both_select)
    select_group = bpy.props.BoolProperty(name = "Select the group", get = get_group_select, set = set_group_select)
    select_rig = bpy.props.BoolProperty(name = "Select the proxy", get = get_rig_select, set = set_rig_select)

    
class TA_Scene(PropertyGroup):
    
    try: 
        bpy.utils.register_class(TA_Object)
        bpy.utils.register_class(TA_LocalObject)
    except:
        pass
    
    def make_active(self, context):
        scene = bpy.data.scenes[self.name]
        if self.active_type == 'PROXY':
            scene.objects.active = bpy.context.scene.objects[self.objects[self.active].proxy] 
        elif self.active_type == 'GROUP': 
            scene.objects.active = bpy.context.scene.objects[self.objects[self.active].name] 
          
    def get_active_object(self):
        active_object = bpy.context.active_object
        if active_object:
            if not active_object.proxy: 
                i = 0
                for obj in self.objects: 
                    if obj.name == active_object.name:
                        break
                    i += 1
            else: 
                i = 0
                for obj in self.objects: 
                    if obj.proxy == active_object.name: 
                        break 
                    i += 1
            return i
        else: 
            return len(self.objects)
                    
    def set_active_object(self, value):
        scene = bpy.data.scenes[self.name]
        if self.active_type == 'PROXY' and self.objects[value].proxy:
            scene.objects.active = bpy.context.scene.objects[self.objects[value].proxy]
            self.objects[value].select_rig = True
            for i, item in enumerate(self.objects):
                if i != value: 
                    item.select_rig = False
                item.select_group = False
        else: 
            scene.objects.active = bpy.context.scene.objects[self.objects[value].name] 
            self.objects[value].select_group = True
            for i, item in enumerate(self.objects):
                if i != value: 
                    item.select_group = False
                item.select_rig = False

                
    def get_active_local(self):
        active_object = bpy.context.active_object
        if active_object:
            for i, obj in enumerate(self.local_objects):
                if obj.name == active_object.name:
                    return i
        return len(self.local_objects)
            
    def set_active_local(self, value):
        scene = bpy.data.scenes[self.name]
        scene.objects.active = bpy.context.scene.objects[self.local_objects[value].name]
        self.local_objects[value].select_item = True
        for i, item in enumerate(self.local_objects):
            if i != value: 
                item.select_item = False
    
    
    def update_list(self, context):
        bpy.ops.scene.outliner_update_objects(active_scene = bpy.context.screen.tangent_outliner.active_scene)
        
    
    local_objects = bpy.props.CollectionProperty(type = TA_LocalObject)
    active_local_objects = bpy.props.IntProperty(name = "Active local", get = get_active_local, set = set_active_local)
    objects = bpy.props.CollectionProperty(type = TA_Object)
    active = bpy.props.IntProperty(name = "Active Object", get = get_active_object, set = set_active_object)  
    active_type = bpy.props.EnumProperty(
        items = [
            ('GROUP', 'GROUP', "Make group active when selected", 'OUTLINER_OB_EMPTY', 0),
            ('PROXY', 'PROXY', "Make proxy active when selected", 'OUTLINER_OB_ARMATURE', 1)
            ],
        name = "Active type",
        default = 'PROXY',
        update = make_active)
    list_mode = bpy.props.EnumProperty(
        items = [
            ('ASSETS', 'Linked Assets', "linked assets"),
            ('LOCAL', 'Local Assets', "local assets"),
            ],
        name = "objects list",
        default = 'ASSETS',
        update = update_list,
        )
 
 
class TA_Outliner(PropertyGroup):
    try: 
        bpy.utils.register_class(TA_Scene)
        bpy.utils.register_class(TA_Object)
    except: pass
    
    scenes = bpy.props.CollectionProperty(type = TA_Scene)
    
    def get_current_scene(self):
        i = 0
        for scene in self.scenes: 
            if scene.name == bpy.context.scene.name:
                break
            i = i + 1
        return i
    
    def select_scene(self, value):
        scene_name = self.scenes[value].name
        scene = bpy.data.scenes[scene_name]
        bpy.context.screen.scene = scene
        # self.conoutmessage = ("Updating: {} {}".format(value, scene_name))
        # if self.conout:
            # print(self.conoutmessage)
        # self.log.append(self.conoutmessage)
        bpy.ops.scene.outliner_update_objects(active_scene = value)

    
    active_scene = bpy.props.IntProperty(name = "Active scene index", get = get_current_scene, set = select_scene) 
    
    
class TA_Scene_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):       
        layout.prop(item, "name", text="", emboss=False, icon = 'SCENE_DATA')
 
 
class TA_Object_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align = True)
        row1 = row.row(align = True)
        row1.prop(item, "both", text = "")
        row1.prop(item, "name", text="", emboss=False, icon = 'OBJECT_DATA')
        row1.prop(item, "select_group", text="")
        row1.scale_y = 1
        row2 = row.row(align = True)
        if not item.proxy:
            row2.enabled = False
        row2.prop(item, "select_rig", text="")
        row2.scale_y = 1
        row.scale_y = 1       


class TA_Local_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align = True)
        row1 = row.row(align = True)
        row1.prop(item, "select_item", text = "")
        row1.prop(item, "name", text="", emboss=False, icon = 'OUTLINER_OB_%s' %item.type)     

        
class TA_Update_Objects(Operator):
    bl_label = "Update Objects"
    bl_idname = "scene.outliner_update_objects"
    bl_description = "Update the object collections within the scene (for tangent outliner)"
    bl_options = {'UNDO'} 

    active_scene = bpy.props.IntProperty(name = "SceneName")
    
    def execute(self, context):
        bpy.context.scene.update()
        list_mode = bpy.context.screen.tangent_outliner.scenes[self.active_scene].list_mode
        scene = context.screen.tangent_outliner.scenes[self.active_scene]
        
        #Update linked assets
        if list_mode == 'ASSETS':
            scene_name = scene.name     
            i = 0
            for item in scene.objects: 
                try: 
                    bpy.data.scenes[scene_name].objects[item.name]
                except:
                    scene.objects.remove(i)
                    #Do not increment the index by one if object is removed since every object's index is now -1
                else:
                    #if the object exists (try succeeded), increment the index by one
                    i = i + 1
                      
            for obj in bpy.data.scenes[scene_name].objects:
                if obj.dupli_group and obj.name not in [item.name for item in scene.objects]:
                    new_object = scene.objects.add()
                    new_object.name = obj.name
        
        #Update local assets
        elif list_mode == 'LOCAL':
            scene_name = scene.name
            i = 0
            for item in scene.local_objects:
                try:
                    bpy.data.scenes[scene_name].objects[item.name]
                except: 
                    scene.local_objects.remove(i)
                else: 
                    i = i + 1
                    
            for obj in bpy.data.scenes[scene_name].objects:
                if not obj.dupli_group and not obj.proxy and obj.name not in [item.name for item in scene.local_objects]:
                    new_object = scene.local_objects.add()
                    new_object.name = obj.name
                    new_object.type = obj.type
                        
        return {'FINISHED'}
         
    def invoke(self, context, event):
        return self.execute(context)
           

class TA_SelectLocalLinked(Operator):
    bl_label = "SelectAll"
    bl_idname = "scene.outliner_select_localinked"
    bl_description = "Select/Deselect all objects within the same asset type"
    bl_options = {'UNDO'} 

    select = bpy.props.BoolProperty(name = "Select", default = True)

    def invoke(self, context, event):
        scene = context.screen.tangent_outliner.scenes[bpy.context.screen.tangent_outliner.active_scene]
        list_mode = scene.list_mode
        if list_mode == 'ASSETS':
            for obj in scene.objects: 
                obj.both = self.select
        if list_mode == 'LOCAL': 
            for obj in scene.local_objects:
                obj.select_item = self.select
        return {'FINISHED'}


class TA_SelectAll(Operator):
    bl_label = "SelectLocalLinked"
    bl_idname = "scene.outliner_select_all"
    bl_description = "Select/Deselect all Local and Linked assets"
    bl_options = {'UNDO'} 
    
    select = bpy.props.BoolProperty(name = "Select", default = True)
    
    def invoke(self, context, event):
        scene = context.screen.tangent_outliner.scenes[bpy.context.screen.tangent_outliner.active_scene]
        for obj in scene.objects: 
            obj.both = self.select
        for obj in scene.local_objects:
            obj.select_item = self.select
        return {'FINISHED'}

    
class OutlinerGUI(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "TA - Animation"
    bl_label = "Scene Outliner"  

    def draw(self, context):
        self.add_scene()
        layout = self.layout
        col = layout.column(align = False)
        row = col.row()
        row.template_list(
            "TA_Scene_list", "",
            context.screen.tangent_outliner, "scenes", context.screen.tangent_outliner, "active_scene", rows = 3, maxrows = 3)    
        row = col.row(align = False)
        row.alignment = 'EXPAND'
        row.operator("scene.outliner_update_objects", text = "Update", icon = 'FILE_REFRESH').active_scene = context.screen.tangent_outliner.active_scene
        scene = context.screen.tangent_outliner.scenes[context.screen.tangent_outliner.active_scene]
        row.prop(scene, "list_mode", text = "")
        row.prop(scene, "active_type", expand = True, icon_only = True)
        row = col.row()
        if scene.list_mode == 'ASSETS':
            row.template_list(
                "TA_Object_list", "",
                scene, "objects", scene, "active", rows = 7, maxrows = 5)
            row = col.row(align = True)
            row.operator("scene.outliner_select_localinked", text = "Select All Linked").select = True
            row.operator("scene.outliner_select_localinked", text = "Deselect All Linked").select = False
        elif scene.list_mode == 'LOCAL':
            row.template_list(
                "TA_Local_list", "", 
                scene, "local_objects", scene, "active_local_objects", rows = 7, maxrows = 5)
            row = col.row(align = True)
            row.operator("scene.outliner_select_localinked", text = "Select All Local").select = True
            row.operator("scene.outliner_select_localinked", text = "Deselect All Local").select = False

        row = col.row(align = True)
        row.operator("scene.outliner_select_all", text = "Select Scene").select = True
        row.operator("scene.outliner_select_all", text = "Deselect Scene").select = False

        
    def add_scene(self):
        for scene in bpy.data.scenes: 
            if scene.name not in [item.name for item in bpy.context.screen.tangent_outliner.scenes]:
                new_scene = bpy.context.screen.tangent_outliner.scenes.add()
                new_scene.name = scene.name
        i = 0
        for item in bpy.context.screen.tangent_outliner.scenes: 
            if item.name not in [scene.name for scene in bpy.data.scenes]:
                bpy.context.screen.tangent_outliner.scenes.remove(i)
            i += 1


class ANIM_OBJ_AssetResolution(PropertyGroup):

    def get_resolution(self):
        group = None
        if self.dupli_group and self.dupli_group.library.filepath:
            group = self.dupli_group
        
        if self.proxy:
            if self.proxy_group:
                try: 
                    bpy.context.scene.objects[self.proxy_group.name]
                    group = self.proxy_group.dupli_group
                except: 
                    for obj in bpy.context.scene.objects: 
                        if obj.dupli_group and obj.dupli_group.library.filepath: 
                            if obj.dupli_group.library.filepath == self.proxy.library.filepath: 
                                group = obj.dupli_group  
            else: 
                for obj in bpy.context.scene.objects: 
                    if obj.dupli_group and obj.dupli_group.library.filepath: 
                        if obj.dupli_group.library.filepath == self.proxy.library.filepath: 
                            group = obj.dupli_group
                            
        if group: 
            if group.name.endswith('MID'):
                return 1
            elif group.name.endswith('LOW'):
                return 2
            else: 
                return 0    
        else: 
            return 3
    
    bpy.types.Scene.asset_resolution = bpy.props.EnumProperty(
        items=[('HIGH', 'HIGH', "High res", 'SOLID', 0), 
            ('MID', 'MID', "Mid res", 'ANTIALIASED', 1), 
            ('LOW', 'LOW', "Low res", 'ALIASED', 2)])

    bpy.types.Scene.scene_resolution = bpy.props.EnumProperty(
        items=[('HIGH', 'HIGH', "High res", 'SOLID', 0), 
            ('MID', 'MID', "Mid res", 'ANTIALIASED', 1), 
            ('LOW', 'LOW', "Low res", 'ALIASED', 2)])

    bpy.types.Object.asset_resolution = bpy.props.EnumProperty(
        items=[('HIGH', 'HIGH', "High res", 'SOLID', 0), 
            ('MID', 'MID', "Mid res", 'ANTIALIASED', 1), 
            ('LOW', 'LOW', "Low res", 'ALIASED', 2),
            ('NONE', 'NONE', "Not available", '', 3)],
        name= "Asset_resolution",
        get = get_resolution)
        
            
class ANIM_OBJ_AssetToolsGUI(Panel):
    """
    Controllers for Animation
    """
    bl_label = "Resolution Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'TA - Animation'                             
       
    def draw(self, context):
        addon_state_pr = addon_utils.check("proxy_refresh")                                      # Panel requires 'proxy_refresh' add-on
        addon_state_acas = addon_utils.check("addon_create_animation_scene")                     # Panel requires 'addon_create_animation_scene' add-on

        layout = self.layout
        col = layout.column(align = False)
        col.label("Local Scene")
        box = col.box()
        row = box.row(align = True)

        if addon_state_pr:
            row.label(icon = 'OUTLINER_OB_ARMATURE')
            row.operator("object.proxy_refresh", text = "Refresh Proxy", icon = 'FILE_REFRESH')
        else:
            row.label(text = "Add-on Failed to Load", icon = 'CANCEL')
            row = box.row(align = True)
            row.label(text = "     [Tangent: Proxy Refresh Tool]")

        row = box.row(align = True)
        row = box.row(align = True)
        subcol = row.column(align = True)
        subrow = subcol.row(align = True)
        split = subrow.split(percentage = 0.3, align = True)
        if context.scene.asset_resolution == 'HIGH':
            split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution, icon = 'SOLID')
        elif context.scene.asset_resolution == 'MID':
            split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution, icon = 'ANTIALIASED')
        elif context.scene.asset_resolution == 'LOW':
            split.prop_menu_enum(context.scene, "asset_resolution", text = context.scene.asset_resolution, icon = 'ALIASED')
        split = subrow.split(percentage = 1, align = True)
        split.operator("object.change_asset_resolution", text = "Change Resolution", icon = 'FILE_REFRESH')
        subrow = subcol.row(align = True)
        subrow.label(text = "Resolution Swap will NOT work if", icon = 'ERROR')
        subrow = subcol.row(align = True)
        subrow.label(text = "      the linked groups have orphan data")

        col.separator()
        col.separator()
        row = col.row()
        row.label(text = "New Scene", icon = 'SCENE_DATA')
        box = col.box()
        row = box.row(align = True)

        if addon_state_acas:
            subrow = box.row(align = True)
            subcol = row.column(align = True)
            subrow = subcol.row(align = True)
            split = subrow.split(percentage = 0.3, align = True)
            if context.scene.scene_resolution == 'HIGH':
                split.prop_menu_enum(context.scene, "scene_resolution", text = context.scene.scene_resolution, icon = 'SOLID')
            elif context.scene.scene_resolution == 'MID':
                split.prop_menu_enum(context.scene, "scene_resolution", text = context.scene.scene_resolution, icon = 'ANTIALIASED')
            elif context.scene.scene_resolution == 'LOW':
                split.prop_menu_enum(context.scene, "scene_resolution", text = context.scene.scene_resolution, icon = 'ALIASED')
            split = subrow.split(percentage = 1, align = True)
            split.operator("object.create_scene_resolution", text = "Create Scene", icon = 'FILE_REFRESH')
            subrow = subcol.row(align = True)
            subrow.label(text = "Objects with missing resolution are", icon = 'INFO')
            subrow = subcol.row(align = True)
            subrow.label(text = "      linked at their current resolution")
        else:
            row.label(text = "Add-on Failed to Load", icon = 'CANCEL')
            row = box.row(align = True)
            row.label(text = "     [Tangent: Create Temporary Animation Scene]")


class ANIM_OBJ_CreateSceneResolution(Operator):
    """
    Create scene resolution
    """
    bl_label = "swap_scene_resolution"
    bl_idname = "object.create_scene_resolution"
    bl_description = "Create scene with selected object at chosen resolution"
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.scene.scene_resolution == "LOW":
            bpy.ops.animation.create_low_resolution('INVOKE_DEFAULT')
        elif context.scene.scene_resolution == "MID":
            bpy.ops.animation.create_mid_resolution('INVOKE_DEFAULT')
        elif context.scene.scene_resolution == "HIGH":
            bpy.ops.animation.create_high_resolution('INVOKE_DEFAULT')

        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class ANIM_OBJ_SwapAssetResolution(Operator):
    """
    Swap asset resolution
    """
    bl_label = "swap_asset_resolution"
    bl_idname = "object.change_asset_resolution"
    bl_description = "Change Asset Resolution to the selected object"
    bl_options = {'UNDO'}

    def compile_list(self, obj_list):
        list = []
        for obj in obj_list: 
            if obj.proxy: 
                object = self.find_proxy_group(obj);
                if object and object not in list:
                    list.append(object)
            if obj.dupli_group and obj.dupli_group.library.filepath:
                if obj not in list:
                    list.append(obj)
        return list
    
    def find_proxy_group(self, proxy_object):
        """
        Find the corresponding proxy group
        """
        if proxy_object.proxy_group:
            try: 
                bpy.context.scene.objects[proxy_object.proxy_group.name]
                return proxy_object.proxy_group
            except: 
                pass         
        for obj in bpy.context.scene.objects: 
            if obj.dupli_group: 
                if obj.dupli_group.library.filepath == proxy_object.data.library.filepath:
                    return obj

    def dupli_group_swap(self, obj, new_group):
        """
        Swap the dupli group, if the asset is already in the file to avoid going out the file to link in the asset
        """
        obj.dupli_group = new_group 
        obj.name = new_group.name

    def execute(self, context):

        self.source_scene_name = bpy.context.scene.name
        self.conout = False
        self.conoutmessage = None
        self.displaylog = False
        self.error = []
        self.log = []
        self.check = []
        self.success = []
        self.fail = []

        self.conoutmessage = ("---------- %s ----------\n" %datetime.datetime.now())
        if self.conout:
            print("\n\n%s" %self.conoutmessage)                                                                # start of execution header
        self.log.append(self.conoutmessage)

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')    
            self.conoutmessage = ("Selecting '%s' mode" %bpy.context.mode)
            if self.conout:
                print(self.conoutmessage)                                                                      # Console logging
            self.log.append(self.conoutmessage)

        bpy.context.scene.cursor_location.xyz = (0,0,0)  
        self.conoutmessage = ("Moving 3D Cursor to origin")
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

        for obj in self.compile_list(bpy.context.selected_objects):
            group = obj.dupli_group
            self.conoutmessage = ("Asset '%s' has dupli_group: '%s'" %(obj.name, group.name))
            if self.conout:
                print(self.conoutmessage)
            self.log.append(self.conoutmessage)

            if group:
                group_name = None
                new_group_name = None
                if group.name.endswith(('LOW', 'MID')):                                                        # this should always be name_LOW, name_MID
                    group_name = group.name[:-4]                                                               # remove suffix
                    self.conoutmessage = ("Group name will be: %s" %group_name)
                else: 
                    group_name = group.name
                    self.conoutmessage = ("Group name is: %s" %group_name)

                if self.conout:
                    print(self.conoutmessage)
                self.log.append(self.conoutmessage)

                resolution = bpy.context.scene.asset_resolution 
                self.conoutmessage = ("Desired asset resolution: '%s'" %resolution)
                if self.conout:
                    print(self.conoutmessage)
                self.log.append(self.conoutmessage)

                if obj.asset_resolution != resolution and group_name:
                    if resolution == 'HIGH': 
                        new_group_name = group_name
                        self.conoutmessage = ("Group name is: %s" %new_group_name)
                    elif resolution == 'MID':
                        new_group_name = group_name + '_MID'
                        self.conoutmessage = ("Group name will be: %s" %new_group_name)
                    elif resolution == 'LOW': 
                        new_group_name = group_name + '_LOW'
                        self.conoutmessage = ("Group name will be: %s" %new_group_name)

                    if self.conout:
                        print(self.conoutmessage)
                    self.log.append(self.conoutmessage)

                    try: 
                        #See if the group is in the asset folder already
                        new_group = bpy.data.groups[new_group_name]
                    except: 
                        #If not, link it in
                        # print("Unlinking %s" %obj.name)
                        # bpy.context.scene.objects.unlink(obj) #delete object from scene temporarily   
                        dir = group.library.filepath + '\\Group\\'  
                        found = False
                        with bpy.data.libraries.load(group.library.filepath, link = True) as (data_from, data_to):
                                for group in data_from.groups:
                                    self.conoutmessage = ("Found: '%s' \n       in: '%s'" % (group, dir))
                                    if self.conout:
                                        print(self.conoutmessage)
                                    self.log.append(self.conoutmessage)
                                    if group == new_group_name:
                                        found = True
                                        data_to.groups = [group]
                                        break

                        if not found:    
                            self.conoutmessage = ("Can't find '%s' resolution for '%s'" %(resolution, obj.name))
                            if self.conout:
                                print(self.conoutmessage)
                            self.log.append(self.conoutmessage)

                            #self.report({'ERROR'}, "%s in %s resolution does not exist" %(obj.name, resolution))
                            #bpy.context.scene.objects.link(obj) #link back the object 

                        else: 
                            new_group = bpy.data.groups[new_group_name]
                            self.dupli_group_swap(obj, new_group)
                            self.conoutmessage = ("Linking existing '%s' from '%s'" %(new_group_name, dir))
                            if self.conout:
                                print(self.conoutmessage)
                            self.log.append(self.conoutmessage)

                            # print("Linking from filename: %s directory: %s" %(new_group_name, dir))
                            # bpy.ops.wm.link(filename= new_group_name, directory = dir, relative_path = False)
                            # Remove the group if needed
                            # bpy.data.groups.remove(group) #remove previous group completely
                            # bpy.data.objects.remove(obj) #remove old object permanently
                    else: 
                        #Swap the dupli group
                        self.dupli_group_swap(obj, new_group)
                        self.conoutmessage = ("Changing 'dupli_group' to '%s'" %new_group)
                        if self.conout:
                            print(self.conoutmessage)
                        self.log.append(self.conoutmessage)
        
        #Update Outliner
        bpy.ops.scene.outliner_update_objects(active_scene = bpy.context.screen.tangent_outliner.active_scene) 
        self.conoutmessage = ("Refreshing outliner")
        if self.conout:
            print(self.conoutmessage)
        self.log.append(self.conoutmessage)

        if self.displaylog:
            logging = ProcessLogging(self.check, self.error, self.fail, self.log, self.success, self.source_scene_name)
            logging.execute()                                                                                      # Write results to log file

        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)


class ProcessLogging(object):
    """
    Write script activity to log
    """
    def __init__(self, check = None, error = None, fail = None, log = None, success = None, source_scene_name = None):
        """ Initialize logging variables """
        self.source_scene_name = source_scene_name
        self.conout = False
        self.conoutmessage = None
        self.check = check                                                                                     # Warning
        self.error = error                                                                                     # Unhandled exception
        self.fail = fail                                                                                       # Didn't complete as expected
        self.log = log                                                                                         # General processing comments
        self.success = success                                                                                 # Completed as expected

    def execute(self):
        """ Write process log file """
        # import datetime
        # import re
        # import os
        # filepath = bpy.data.filepath                                                                         # .BLEND file path
        filepath = "c:\\temp\\"                                                                                # Local drive
        directory = os.path.dirname(filepath)
        if not os.path.exists("%s\\log" %directory):
            os.mkdir("%s\\log" %directory)
        date_var = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        log_file = "%s\\log\\%s_log_%s.log" %(directory, self.source_scene_name, date_var)
        try:
            file = open(log_file, "r")
            file.close()
        except:
            file = open(log_file, "w")
            file.close()
        file = open(log_file, "a")
        for i in self.log: 
            file.write("-%s- LOG: %s\n" %(self.source_scene_name, i))
        file.write("\n")
        for i in self.error:
            file.write("-%s- FIX: %s\n" %(self.source_scene_name, i))
        file.write("\n")
        for i in self.check: 
            file.write("-%s- CHECK: %s\n" %(self.source_scene_name, i))
        file.write("\n")    
        for i in self.success: 
            file.write("-%s- SUCCESS: %s\n" %(self.source_scene_name, i))
        file.write("\n")  
        for i in self.fail: 
            file.write("-%s- FAIL: %s\n" %(self.source_scene_name, i))
        file.close()

        # self.warning_box(log_file)                                                                             # Display log in Blender 'TEXT_EDITOR'

    def warning_box(self, logfile):
        """ Output to text editor window """
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.text.open(filepath = logfile)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Screen.tangent_outliner = bpy.props.PointerProperty(type = TA_Outliner)

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

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Screen.tangent_outliner

    
if __name__ == "__main__":
    register()       