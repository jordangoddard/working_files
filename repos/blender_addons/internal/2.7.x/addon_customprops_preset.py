# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Custom Properties Preset",
    "author": "Tangent Animation",
    "version": (1, 0, 7),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Save/restore custom asset properties",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Custom%20Properties%20Preset.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import datetime
import re
import os
import json

import bpy
from bpy.types import Object, Scene, Panel, Operator, PropertyGroup, UIList


class CTLGODCCustomProperties(PropertyGroup):
    """
    Sub Collection: Custom Properties for each in item in the target list
    """  
    #name = bpy.props.StringProperty(name = "name", description = "")                              # Property name
    value = bpy.props.StringProperty(name = "value", description = "")                             # Property value
    preset = bpy.props.BoolProperty(name = "save", description = "", default=False)                # Preset selection


class TargetProperties(PropertyGroup):
    """
    Main Collection: Properties within the target list
    """
    try:
        bpy.utils.register_class(CTLGODCCustomProperties)
    except: 
        pass 

    #name = bpy.props.StringProperty(name = "Name of the item")
    type = bpy.props.StringProperty(name = "Type of the item")                                     # Object type, ex: 'ARMATURE'
    rnatype = bpy.props.StringProperty(name = "Rna Type")                                          # RNA Type, ex: 'Object'
    proxy = bpy.props.StringProperty(name = "Proxy if available")                                  # Proxy name (unused)
    dataname = bpy.props.StringProperty(name = "Data name if available")                           # Data name
    assetpath = bpy.props.StringProperty(name = "assetpath")                                       # Original asset path
    customproperties = bpy.props.CollectionProperty(type = CTLGODCCustomProperties)                # Array of Custom Properties on 'ctl_node_name' node    


class MasterProperties(PropertyGroup):
    """
    Property Used for the whole GUI in general
    """
    try:                                                                                           # Workaround to unexpected deregistration
        bpy.utils.register_class(TargetProperties)
    except: 
        pass 

    Scene.target_asset_list = bpy.props.CollectionProperty(type = TargetProperties)
    Scene.target_asset_index = bpy.props.IntProperty()

    Scene.presetbutton = bpy.props.StringProperty(name = "presetbutton",                           # Track preset button state
                                                  description = "", 
                                                  default = "APPLY")

    def update_presetmode(self, context):
        """ Set Blender UI selection, clear existing list if preset mode was changed"""
        button_state = context.scene.presetmode
        current_state = context.scene.presetbutton
        if button_state != current_state:                                                          # Switched mode, clear all items
            context.scene.target_asset_list.clear()
            context.scene.presetbutton = button_state

    Scene.presetmode = bpy.props.EnumProperty(name = "readwritepresetstates", 
                                              items = (('CREATE', "Save", "Save an object preset file"),('APPLY', "Apply", "Apply preset file contents to object(s)")), 
                                              default = 'APPLY',
                                              update = update_presetmode)

    bpy.types.Scene.displaylog = bpy.props.BoolProperty(name = "Display processing log", default = False)


class OBJECT_UL_asset_list(UIList):
    """
    Populate selection box
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):       
        layout.prop(item, "name", text="", emboss=False, icon = 'ARMATURE_DATA')


class AddTargetList(Operator):
    """
    Add selected (and valid) scene object to list
    """
    bl_label = "add_target_list"
    bl_idname = "scene.addtargetlist"
    bl_description = "Add selected objects to the list"
    bl_options = {'UNDO'}    

    @classmethod
    def poll(cls, context):
        """ Handle selection cases """
        poll_state = False
        if len(bpy.context.selected_objects) == 1:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    if context.scene.presetmode == 'CREATE' and obj.proxy is None:                 # PRESET MODE = Create preset file, local asset only
                        poll_state = True
                    elif context.scene.presetmode == 'APPLY' and obj.proxy is not None:            # PRESET MODE = Apply preset file, linked assets only
                        poll_state = True
                    else:
                        pass                                                                       # Unhandled preset mode: False
        elif len(bpy.context.selected_objects) > 0 and len(bpy.context.selected_objects) != 1:
                poll_state = True
        return (poll_state)

    mode = bpy.props.StringProperty(name = "add")

    def execute(self, context):
        """ Add all selected ARMATURES with 'ctl_node_name' """
        scene_objects = bpy.context.selected_objects
        jsonip = JSONImportPresets(scene_objects)
        jsonip.execute()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Invoke """
        return self.execute(context)


class AddAllTargetList(Operator):
    """
    Add selected valid scene objects to list
    """
    bl_label = "addall_target_list"
    bl_idname = "scene.addalltargetlist"
    bl_description = "Adds all valid objects from the scene"
    bl_options = {'UNDO'}    

    @classmethod
    def poll(cls, context):
        """ Handle selection cases """
        poll_state = len(bpy.context.scene.objects) > 0                                            # Items in list
        return (poll_state)

    mode = bpy.props.StringProperty(name = "addall")

    def execute(self, context):
        """ Add all scene ARMATURES with 'ctl_node_name' nodes """
        scene_objects = bpy.context.scene.objects
        jsonip = JSONImportPresets(scene_objects)
        jsonip.execute()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Invoke """
        return self.execute(context)


class RemoveTargetList(Operator):
    """
    Remove selected (and valid) scene object to list
    """
    bl_label = "remove_target_list"
    bl_idname = "scene.removetargetlist"
    bl_description = "Remove selected objects from the list"
    bl_options = {'UNDO'}    

    @classmethod
    def poll(cls, context):
        """ Handle selection cases """
        poll_state = len(context.scene.target_asset_list) > 0                                      # Items in list
        return (poll_state)

    mode = bpy.props.StringProperty(name = "remove")

    def execute(self, context):
        """ Remove selection """
        context.scene.target_asset_list.remove(context.scene.target_asset_index)                   # Remove selected item
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Invoke """
        return self.execute(context)


class ClearTargetList(Operator):
    """
    Remove all objects from list
    """
    bl_label = "clear_target_list"
    bl_idname = "scene.cleartargetlist"
    bl_description = "Removes all objects from the list"
    bl_options = {'UNDO'}    

    @classmethod
    def poll(cls, context):
        """ Handle selection cases """
        poll_state = len(context.scene.target_asset_list) > 0                                      # Items in list
        return (poll_state)

    mode = bpy.props.StringProperty(name = "clear")
    
    def execute(self, context):
        """ Clear all items """
        context.scene.target_asset_list.clear()                                                    # Clear all items in list
        return {'FINISHED'}

    def invoke(self, context, event):
        """ Invoke """
        return self.execute(context)


class SetFocusToNode(Operator):
    """
    Remove all objects from list
    """
    bl_label = "set_focus_to_node"
    bl_idname = "scene.setfocustonode"
    bl_description = "Select item control node"
    bl_options = {'UNDO'}    

    @classmethod
    def poll(cls, context):
        """ Handle selection cases """
        poll_state = len(context.scene.target_asset_list) > 0                                      # Items in list
        return (poll_state)

    mode = bpy.props.StringProperty(name = "focus")
    
    def execute(self, context):
        """ Set focus to the selected item 'ctl_node_name' node """
        target_item = context.scene.target_asset_list[context.scene.target_asset_index].name
        target_rig = context.scene.target_asset_list[context.scene.target_asset_index].dataname
        active_object = bpy.context.scene.objects.active.name

        bpy.context.scene.objects[active_object].select = False
        bpy.context.scene.objects.active=bpy.context.scene.objects[target_item]
        bpy.context.scene.objects[target_item].select = True

        ctl_node_name = "ctl.god.C"
        obj = bpy.context.object                                                                   # Item from target list
        bone = obj.data.bones[ctl_node_name]                                                       # Control for item from target list
        bone.select = True
        obj.data.bones.active = bone

        bpy.ops.object.mode_set(mode='POSE')                                                       # Expose custom properties 

        for window in bpy.context.window_manager.windows:                                          # Get session spaces
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':                                                         # Found SpaceView3D viewport
                    for region in area.regions:
                        if region.type == 'UI' and region.width <= 1:                              # Found Properties UI, check if hidden
                            override = {'window': window, 
                                        'region' : region, 
                                        'screen': screen, 
                                        'area': area}
                            bpy.ops.view3d.properties(override)                                    # Display SpaceView3D Properties

        return {'FINISHED'}

    def invoke(self, context, event):
        """ Invoke """
        return self.execute(context)


class ExportSelectionPresets(Operator):
    """
    Perform user request actions
    """
    bl_idname = "preset.export_selection_preset"
    bl_label = "Store Selection Presets"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """ Invoke export presets for each items in selection list """
        jsonep = JSONExportPresets(context.scene.target_asset_list)
        jsonep.execute()

        self.report({'INFO'}, "Saved preset files for all items in selection list.")               # Send output to Blender Info header

        return {"FINISHED"}


class ApplySelectionPresets(Operator):
    """
    Perform user request actions
    """
    bl_idname = "preset.import_selection_preset"
    bl_label = "Apply Selection Presets"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """ Invoke import presets for each items in selection list """
        jsonep = ApplyImportedPresets(context.scene.target_asset_list)
        jsonep.execute()

        self.report({'INFO'}, "Applied presets for all specified items in selection list.")        # Send output to Blender Info header

        return {"FINISHED"}


class JSONImportPresets(object):
    """
    Add 'target_asset_list' entries based on the panel mode: CREATE/APPLY
    """
    def __init__(self, scene_objects):
        """ Initialize general variables """
        self.source_scene_name = bpy.context.scene.name                                            # Store current scene name
        self.ctl_node_name = "ctl.god.C"                                                           # Object control node
        self.scene_objects = scene_objects                                                         # Objects to process

        """ Initialize logging variables """
        self.conout = False
        self.conoutmessage = None
        self.check = []
        self.error = []
        self.fail = []
        self.log = []
        self.success = []

        self.conoutmessage = ("---------- %s ----------\n" %datetime.datetime.now())
        if self.conout:
            print("\n%s\n" %self.conoutmessage)                                                    # System console message
        self.log.append(self.conoutmessage)

    def execute(self):
        """ Add ARMATURES based on mode: local or preset file """
        for obj in self.scene_objects:
            if obj.type == 'ARMATURE':
                if obj.name in [item.name for item in bpy.context.scene.target_asset_list]:
                    pass                                                                           # Already in list

                elif self.ctl_node_name in [pb.name for pb in obj.pose.bones]:
                    if bpy.context.scene.presetmode == 'CREATE' and obj.proxy is None:             # PRESET MODE = Create preset file, local asset only
                        asset_info = bpy.context.scene.target_asset_list.add()
                        asset_info.name = obj.name
                        asset_info.type = obj.type                                                 # Object type: ARMATURE
                        asset_info.dataname = obj.data.name                                        # Rig name
                        asset_info.rnatype = obj.rna_type.name                                     # RNA type: 'Object'

                        asset_filepath = bpy.path.abspath('//')                                    # Path to current .BLEND file
                        asset_filename = bpy.path.display_name_from_filepath(bpy.data.filepath)
                        asset_info.assetpath = ("%sdata\\%s.preset" %(asset_filepath, asset_filename))

                        nodectlprops = obj.pose.bones[self.ctl_node_name]
                        for cp in nodectlprops.items():
                            if cp[0] not in ('rigify_parameters', '_RNA_UI'):                      # Skip non-applicable names (type: str)
                                asset_props = asset_info.customproperties.add()
                                asset_props.name = cp[0]                                           # Custom Property name
                                asset_props.value = str(cp[1])                                     # Custom Property value
                                asset_props.preset = False                                         # Custom Property preset

                    elif bpy.context.scene.presetmode == 'APPLY' and obj.proxy is not None:        # PRESET MODE = Apply preset file, linked assets only
                        asset_info = bpy.context.scene.target_asset_list.add()
                        asset_info.name = obj.name
                        asset_info.type = obj.type                                                 # Object type: ARMATURE
                        asset_info.dataname = obj.data.name                                        # Rig name
                        asset_info.rnatype = obj.rna_type.name                                     # RNA type: 'Object'

                        asset_filepath = bpy.path.abspath('//', library=obj.data.library)          # Library path of linked asset
                        asset_filename = bpy.path.display_name_from_filepath(obj.data.library.filepath)
                        asset_info.assetpath = ("%sdata\\%s.preset" %(asset_filepath, asset_filename))

                        nodectlprops = obj.pose.bones[self.ctl_node_name]                          # Custom Properties location

                        json_file = asset_info.assetpath                                           # Read preset file, imported as a dictionary
                        try:
                            with open(json_file, 'r') as infile:
                                json_data = json.load(infile)
                        except:
                            self.conoutmessage = ("No preset file found in '%s'" %json_file)       # Preset file missing/problem
                            if self.conout:
                                print(self.conoutmessage)                                          # System console message
                            self.log.append(self.conoutmessage)
                        else:
                            for key in json_data.keys():
                                if asset_info.dataname == key:                                     # Key matches rig name
                                    for value in json_data[key]["customproperties"]:               # Ensure preset exists in scene object
                                        if value["property"] in [cp[0] for cp in nodectlprops.items()]:
                                            asset_props = asset_info.customproperties.add()
                                            asset_props.name = value["property"]                   # Custom Property name
                                            asset_props.value = str(value["value"])                # Custom Property value
                                            asset_props.preset = value["restore"]                  # Custom Property preset
                                        else:
                                            self.conoutmessage = ("Property '%s' skipped, not found on '%s'" %(value["property"], asset_info.dataname))
                                            if self.conout:
                                                print(self.conoutmessage)                          # System console message
                                            self.fail.append(self.conoutmessage)
                                else:
                                    self.conoutmessage = ("Preset file is looking for '%s' but scene object was '%s', skipped." %(asset_info.dataname, key))
                                    if self.conout:
                                        print(self.conoutmessage)                                  # System console message
                                    self.error.append(self.conoutmessage)

                    else:
                        pass                                                                       # Unhandled preset mode

        if bpy.context.scene.displaylog:
            logging = ProcessLogging(self.check, self.error, self.fail, self.log, self.success, self.source_scene_name)
            logging.execute()                                                                      # Write results to log file


class JSONExportPresets(object):
    """
    Write presets selections for each item in corresponding asset folder
    """
    def __init__(self, target_asset_list):
        """ Initialize general variables """
        self.source_scene_name = bpy.context.scene.name                                            # Store current scene name
        self.target_asset_list = target_asset_list                                                 # Data to export
        self.jsonoutput = None

        """ Initialize logging variables """
        self.conout = False
        self.conoutmessage = None
        self.check = []
        self.error = []
        self.fail = []
        self.log = []
        self.success = []

        self.conoutmessage = ("---------- %s ----------\n" %datetime.datetime.now())
        if self.conout:
            print("\n%s\n" %self.conoutmessage)                                                    # System console message
        self.log.append(self.conoutmessage)

    def execute(self):
        """ Process actions """
        self.json_encoder()                                                                        # Write items to separate JSON files

        if bpy.context.scene.displaylog:
            logging = ProcessLogging(self.check, self.error, self.fail, self.log, self.success, self.source_scene_name)
            logging.execute()                                                                      # Write results to log file

    def json_encoder(self):
        """ Create JSON output from collection/sub-collection """
        ctl_node_name = "ctl.god.C"
        customproperties_subcollection = []

        for tal in self.target_asset_list:
            custom_prop_value = bpy.data.objects[tal.name].pose.bones[ctl_node_name]
            for tal_cp in tal.customproperties:
                talcp_name = ("property", tal_cp.name)                                             # List of property names
                talcp_value = ("value", custom_prop_value[tal_cp.name])                            # List of property values
                talcp_preset = ("restore", tal_cp.preset)                                          # List of checkbox states
                
                talcp_combine = (talcp_name, talcp_value, talcp_preset)                            # Combine lists
                customproperties_subcollection.append(dict(talcp_combine))                         # Convert to dictionary

            self.jsonoutput = {tal.name: {'type': tal.type, 
                                          'rna_type' : tal.rnatype, 
                                          'data_name' : tal.dataname, 
                                          'assetpath' : tal.assetpath, 
                                          'customproperties' : customproperties_subcollection}}

            self.conoutmessage = ("Preset file contents will be:\n%s\n" %self.jsonoutput)
            if self.conout:
                print(self.conoutmessage)                                                          # System console message
            self.success.append(self.conoutmessage)

            tal_assetpath = tal.assetpath
            self.filesys_operations(tal_assetpath)                                                 # Pre-write file operations

            tal_assetpath = tal.assetpath
            json_output = self.jsonoutput
            self.json_writefile(tal_assetpath, json_output)                                        # Write dictionary (preset) file

            self.conoutmessage = ("Write preset file in '%s'" %tal_assetpath)
            if self.conout:
                print(self.conoutmessage)                                                          # System console message
            self.log.append(self.conoutmessage)

    def filesys_operations(self, os_assetpath):
        """ Create folder if not present """
        os_filepath = os_assetpath
        os_directory = os.path.dirname(os_filepath)

        if not os.path.exists(os_directory):
            os.mkdir(os_directory)

    def json_writefile(self, tal_assetpath, json_output):
        """ Write dictionary to preset file """
        json_file = tal_assetpath
        json_data = json_output

        with open(json_file, 'w') as outfile:
            json.dump(json_data, outfile)


class ApplyImportedPresets(object):
    """
    Write presets selections for each item in corresponding asset folder
    """
    def __init__(self, target_asset_list):
        """ Initialize general variables """
        self.source_scene_name = bpy.context.scene.name                                            # Store current scene name
        self.target_asset_list = target_asset_list                                                 # Values to apply

        """ Initialize logging variables """
        self.conout = False
        self.conoutmessage = None
        self.check = []
        self.error = []
        self.fail = []
        self.log = []
        self.success = []

        self.conoutmessage = ("---------- %s ----------\n" %datetime.datetime.now())
        if self.conout:
            print("\n%s\n" %self.conoutmessage)                                                    # System console message
        self.log.append(self.conoutmessage)

    def execute(self):
        """ Remove keyframes, drivers, and assign property value for items in list """
        ctl_node_name = "ctl.god.C"
        for tal in self.target_asset_list:                                                         # Process items in list
            custom_prop_object = bpy.data.objects[tal.name]
            custom_prop_value = custom_prop_object.pose.bones[ctl_node_name]
            for tal_cp in tal.customproperties:                                                    # Get custom properties for current item
                if tal_cp.preset:                                                                  # Restore selected properties

                    try:
                        custom_prop_object.animation_data.action.fcurves
                    except AttributeError:                                                         # Handle 'AttributeError' only, fail on other exceptions
                        self.conoutmessage = ("%s: No keyframes found on custom properties of '%s'" %(tal.name, ctl_node_name))
                        if self.conout:
                            print("%s" %self.conoutmessage)                                        # System console message
                        self.log.append(self.conoutmessage)
                    else:
                        for fcurve in custom_prop_object.animation_data.action.fcurves:            # No easy way to check current property 'data_path', have to loop them all
                            if tal_cp.name in fcurve.data_path:                                    # Found the current item 'data_path' index
                                if not fcurve.is_valid:                                            # Keyframe datapath is invalid
                                    self.conoutmessage = ("%s: Keyframe data path '%s' is invalid" %(tal.name, tal_cp.name))
                                    if self.conout:
                                        print("%s" %self.conoutmessage)                            # System console message
                                    self.error.append(self.conoutmessage)
                                else:                                                              # Clear the keyframes
                                    custom_prop_object.animation_data.action.fcurves.remove(fcurve)
                                    self.conoutmessage = ("%s: Removed all keyframes found on '%s'" % (tal.name, tal_cp.name))
                                    if self.conout:
                                        print("%s" %self.conoutmessage)                            # System console message
                                    self.check.append(self.conoutmessage)
                                    break                                                          # No need to loop through the r of the indexes

                    try:
                        custom_prop_object.animation_data.drivers
                    except AttributeError:                                                         # Handle 'AttributeError' only, fail on other exceptions
                        self.conoutmessage = ("%s: No driver found on custom properties of '%s'" %(tal.name, ctl_node_name))
                        if self.conout:
                            print("%s" %self.conoutmessage)                                        # System console message
                        self.log.append(self.conoutmessage)
                    else:
                        for driver in custom_prop_object.animation_data.drivers:                   # No easy way to check current property 'data_path', have to loop them all
                            if tal_cp.name in driver.data_path:                                    # Found the current item 'data_path' index
                                if not driver.is_valid:                                            # Driver datapath is invalid
                                    self.conoutmessage = ("%s: Driver data path '%s' is invalid" %(tal.name, tal_cp.name))
                                else:
                                    custom_prop_object.driver_remove(driver.data_path)
                                    self.conoutmessage = ("%s: Removed driver found on '%s'" % (tal.name, tal_cp.name))
                                    if self.conout:
                                        print("%s" %self.conoutmessage)                            # System console message
                                    self.check.append(self.conoutmessage)
                                    break                                                          # No need to loop through the r of the indexes

                    try:
                        value_eval = eval(tal_cp.value)
                    except:
                        value_eval = tal_cp.value
                    self.conoutmessage = ("%s: Changing '%s' value from '%s' to '%s'" % (tal.name, tal_cp.name, custom_prop_value[tal_cp.name], value_eval))
                    if self.conout:
                        print("%s" %self.conoutmessage)                                            # System console message
                    self.check.append(self.conoutmessage)
                    custom_prop_value[tal_cp.name] = value_eval                                    # Set new custom property value

                    custom_prop_object.keyframe_insert('pose.bones["%s"]["%s"]' % (ctl_node_name, tal_cp.name), frame=0)
                    self.conoutmessage = ("%s: Setting a key at Frame '0' on '%s'" % (tal.name, tal_cp.name))
                    if self.conout:
                        print("%s" %self.conoutmessage)                                            # System console message
                    self.check.append(self.conoutmessage)

                else:                                                                              # Skip preset, restore set to 'False'
                    self.conoutmessage = ("%s: Restore '%s' property set to '%s'" % (tal.name, tal_cp.name, tal_cp.preset))
                    if self.conout:
                        print("%s" %self.conoutmessage)                                            # System console message
                    self.log.append(self.conoutmessage)

        if bpy.context.scene.displaylog:
            logging = ProcessLogging(self.check, self.error, self.fail, self.log, self.success, self.source_scene_name)
            logging.execute()                                                                      # Write results to log file


class ProcessLogging(object):
    """
    Write script activity to log
    """
    def __init__(self, check = None, error = None, fail = None, log = None, success = None, source_scene_name = None):
        """ Initialize logging variables """
        self.source_scene_name = source_scene_name
        self.conout = False
        self.conoutmessage = None
        self.check = check                                                                         # Warning
        self.error = error                                                                         # Unhandled exception
        self.fail = fail                                                                           # Didn't complete as expected
        self.log = log                                                                             # General processing comments
        self.success = success                                                                     # Completed as expected

    def execute(self):
        """ Write process log file """
        # import datetime
        # import re
        # import os
        # filepath = bpy.data.filepath                                                             # .BLEND file path
        filepath = "c:\\temp\\"                                                                    # Local drive
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

        self.warning_box(log_file)                                                             # Display log in Blender 'TEXT_EDITOR'

    def warning_box(self, logfile):
        """ Output to text editor window """
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.text.open(filepath = logfile)


class SaveIncrementalFile(object):
    """
    Save incremental version of file
    """

    def __init__(self):
        """
        Initialize
        """
        self.filepath = bpy.path.abspath('//')
        self.current_filename = bpy.path.display_name_from_filepath(bpy.data.filepath)
        self.current_filename = current_filename.rsplit('.', 1)

        self.does_file_exist = None
        self.file_exists = True
        self.next_numeric = 0
        self.new_filename = ""
        self.new_suffix = ""
        self.non_numerics = ""
        self.numerics = ""

    def execute(self):
        """
        Execute
        """
        # Check if current filename is versioned (ex: .0000).  If not, use Blender
        # numbering convention
        if len(self.current_filename) < 2:
            self.current_filename.append('0000')

        # Filter the version information for non-numerics.  
        chars = set('0123456789')
        for strval in self.current_filename[1]:
            if strval in chars:
                self.numerics += strval
            else:
                self.non_numerics += strval

        # If non-numerics value is greater than one (ex: .v0000), give up and create 
        # the Blender numbering convention
        if len(self.non_numerics) > 1:
            self.current_filename[0] = ("%s.%s" % (self.current_filename[0], self.current_filename[1]))
            self.current_filename[1] = '0000'
            self.numerics = self.current_filename[1]
            self.non_numerics = ""

        # Set the version number starting value equal to the current file version (ex: 0050)
        # and increment to the next potential version number.  Assemble the file path and 
        # check to see if a file with the incremented version exists.  If a file with the
        # new name already exists, rinse-and-repeat.
        self.next_numeric = int(self.numerics)
        while (self.file_exists == True):
            self.next_numeric += 1
            self.new_suffix = str(self.next_numeric).zfill(len(self.numerics))
            self.new_filename = ("%s%s.%s%s.blend" % (self.filepath, self.current_filename[0], self.non_numerics, self.new_suffix))
            try:
                self.does_file_exist = open(self.new_filename,'r')
            except:
                bpy.ops.wm.save_as_mainfile(filepath=self.new_filename)
                self.file_exists = False


class CustomPropsPresetPanel(Panel):
    """
    Display Panel/UI
    """
    bl_label = "Custom Properties Presets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_idname = "object.custompropspresetpanel"
    bl_category = "TA - Finaling"

    def draw(self, context):
        """ Build UI Panel """
        layout = self.layout
        col = layout.column()  

        """ UI: Object/item list """

        row = col.row(align = True)                                                                # New row with two elements
        row.prop(context.scene, "presetmode", text = context.scene.presetmode, expand = True)

        row = col.row()
        row.label("")

        row = col.row()
        row.label("Selected Items")

        row = layout.row()
        row.template_list("OBJECT_UL_asset_list", "", context.scene, "target_asset_list", context.scene, "target_asset_index")

        col = row.column()
        rowsub = col.row()
        colsub = rowsub.column(align=True)

        colsub.operator("scene.addtargetlist", icon='TRIA_LEFT', text="").mode = 'ADD'
        colsub.operator("scene.removetargetlist", icon='TRIA_RIGHT', text="").mode = 'REMOVE'

        colsub.separator()
        colsub.separator()

        colsub.operator("scene.addalltargetlist", icon='COLLAPSEMENU', text = "").mode = 'ADDALL'
        colsub.operator("scene.cleartargetlist", icon='MESH_PLANE', text = "").mode = 'CLEARALL'

        """ UI: Custom Properties, no Custom Properties returns box with message """

        ctl_node_name = "ctl.god.C"
        ta_length = len(context.scene.target_asset_list)
        ta_index = context.scene.target_asset_index

        if ta_length > 0 and ta_index <= (ta_length - 1):

            colsub.separator()
            colsub.separator()

            colsub.operator("scene.setfocustonode", icon='BONE_DATA', text = "").mode = 'BONEDATA'

            ta_name = context.scene.target_asset_list[ta_index].name
            ta_bone = bpy.data.objects[ta_name].pose.bones[ctl_node_name]

            col = layout.column() 
            row = col.row()
            row.separator()

            row = col.row()
            row.label("Select properties")

            box = layout.box()
            flow = box.column_flow(columns=1, align=True)

            if len(context.scene.target_asset_list[ta_index].customproperties) > 0:
                for custom_props in context.scene.target_asset_list[ta_index].customproperties:
                    row = flow.row(align=True)
                    split = row.split(percentage = 0.7)
                    if context.scene.presetmode == 'CREATE':
                        split.prop(custom_props, "preset", text = custom_props.name)
                        split.prop(ta_bone, '["{}"]'.format(custom_props.name), text = "", slider = False, expand=True)
                    elif context.scene.presetmode == 'APPLY':
                        split.prop(custom_props, "preset", text = custom_props.name)
                        split.label("[%s]" %custom_props.value)
                    else:
                        pass                                                                       # Unhandled preset mode
            else:
                row = flow.row(align=True)
                split = row.split(percentage = 1)
                if context.scene.presetmode == 'CREATE':
                    split.label("No presets", icon = 'ERROR')
                elif context.scene.presetmode == 'APPLY':
                    split.label("No preset file or compatible presets", icon = 'ERROR')
                else:
                    pass                                                                           # Unhandled preset mode

            """ UI: Button Mode, 'CREATE' requires at least one Custom Property """

            col = layout.column() 
            if context.scene.presetmode == 'CREATE' and len(context.scene.target_asset_list[ta_index].customproperties) > 0:
                row = col.row()
                row.separator()
                row = col.row()
                row.label("Export properties for each item in list")
                col.operator(operator = "preset.export_selection_preset", text = "Export Presets", icon = "EXPORT")
            elif context.scene.presetmode == 'APPLY':
                row = col.row()
                row.separator()
                row = col.row()
                row.label("Apply selected properties for each item in list")
                col.operator(operator = "preset.import_selection_preset", text = "Apply Presets", icon = "IMPORT")
            else:
                pass                                                                               # Unhandled preset mode

            row = col.row()

            row = col.row(align = True)
            row.prop(context.scene, "displaylog" ) 


def collection_viewer(self):
    """ Stored here as a function: Standalone code to view collection/sub-collection contents
    JSON Online Validator: http://jsonlint.com/
    """
    import bpy

    print("\n\n\n\n")


    for ob in bpy.context.scene.target_asset_list:
        print("-----------------------------------------------")
        print("COLLECTION: bpy.context.scene.target_asset_list")
        print("-----------------------------------------------")
        print("Name      : %s" %ob.name)
        print("Type      : %s" %ob.type)
        print("RNA Type  : %s" %ob.rnatype)
        # print("Proxy     : %s" %ob.proxy)
        print("Data Name : %s" %ob.dataname)
        print("Asset Path: %s" %ob.assetpath)

        print("\n\t-------------------------------------------------------------------")
        print("\tSUB-COLLECTION: bpy.context.scene.target_asset_list.customproperties")
        print("\t--------------------------------------------------------------------")
        
        for cp in ob.customproperties:
            print("\tProperty: %s Value: %s Restore: %s" %(cp.name.ljust(28), cp.value.ljust(8), cp.preset))
        
        print("\n\n")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    """
    https://www.blender.org/api/blender_python_api_2_75a_release/bpy.app.html
    """

    if bpy.app.background:
        # http://blender.stackexchange.com/questions/39641/how-to-enable-an-addon-on-startup-via-script
        # 
        # Blender launched in background mode; run relevant functions
        # UI panel classes/functions might have to be skipped or coded to accept passed parameters from here
        # Logic to iterate through all scenes in .blend file may be required

        print("Blender running in background mode: %s" %(bpy.app.background))
        register()

        # sif = SaveIncrementalFile()
        # sif.execute()

    else:
        # Blender launched in foreground mode; wait for user interaction
        register()
