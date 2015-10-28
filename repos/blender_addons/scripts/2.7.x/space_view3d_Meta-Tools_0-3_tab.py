# 
#### ALL included Scripts ###########################################################################################################
#### ALL included Scripts ###########################################################################################################
#
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
#
#
#### ALL included Scripts ###########################################################################################################
#### ALL included Scripts ###########################################################################################################


bl_info = {
    "name": "META-TOOLS",
    "author": "MKB",
    "version": (0, 2),
    "blender": (2, 7, 0),
    "location": "View3D > Properties Tool Shelf > META TOOLS",
    "description": "Collection of different Blender Addons",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}






####################################################################################################################################
####################################################################################################################################

import bpy, re, math, sys, os, stat, bmesh, time, random, mathutils, itertools

from bpy.props import *
from mathutils import *
from mathutils.geometry import *
from bgl import *
from bpy.props import *
from bpy_extras import *
from pdb import set_trace

from re import search
from time import time
from random import gauss
from sys import exc_info
from functools import reduce

from itertools import islice
from collections import defaultdict
from platform import system as currentOS

from bmesh.types import BMVert, BMEdge, BMFace, BMLoop

from math import radians, tan, cos, degrees, sin, pi, pow

from mathutils import Matrix, Euler, Vector, Quaternion
from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_line_plane, intersect_line_line
from mathutils.geometry import intersect_ray_tri

from bpy.types import Operator, Panel, PropertyGroup

from bpy_extras.io_utils import ExportHelper
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy_extras.view3d_utils import location_3d_to_region_2d as loc3d2d

from bpy.props import IntProperty, BoolProperty, FloatProperty, FloatVectorProperty, EnumProperty, StringProperty
from bpy.props import CollectionProperty, BoolVectorProperty

from bpy.app.translations import contexts as i18n_contexts
from bpy.app.handlers import persistent




mesh = 0
curve =0
lamp =0
bone = 0
camera =0
particles = 0
pfopath=""
opps=0
opps1=0	




## CREA PANELES EN TOOLS
bpy.types.Scene.osc_object_array = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_manage = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_cad = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_modi = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_visual = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_fly = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_xtras = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_arewo = bpy.props.BoolProperty(default=False)
bpy.types.Scene.osc_object_material = bpy.props.BoolProperty(default=False)




###################################################-------------------------------------------------------
###################################################-------------------------------------------------------
########  Help Text  ##############################-------------------------------------------------------
########  Help Text  ##############################-------------------------------------------------------

#Button:
#row.operator("help.operator3", text="", icon = "INFO")


class help1_text(bpy.types.Operator):
    """how to"""
    bl_idname = 'help.operator1'
    bl_label = ''
    
    def draw(self, context):
        layout = self.layout
        layout.label('a. > set pivot')
        layout.label('b. > mirror editable local')
        layout.label('c. > flatten vertices like scale+(xyz)+0+enter')

    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width = 250)



class help2_text(bpy.types.Operator):
    """how to"""
    bl_idname = 'help.operator2'
    bl_label = ''
    
    def draw(self, context):
        layout = self.layout
        layout.label('a. > as middle point for mirror')
        layout.label('b. > to align location to other objects')
        layout.label('c. > for local rotation on large objects')

    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width = 200)


class help3_text(bpy.types.Operator):
	bl_idname = 'help.operator3'
	bl_label = ''

	def draw(self, context):
		layout = self.layout
		layout.label('Line 1. > Set Pivot...')
		layout.label('Line 2. > Mirror Global...')
		layout.label('Line 3. > Apply Scale & Rotation...')
        
	
	def execute(self, context):
		return {'FINISHED'}

	def invoke(self, context, event):
		return context.window_manager.invoke_popup(self, width = 200)


class help4_text(bpy.types.Operator):
	bl_idname = "help.operator4"
	bl_label = ''

	def draw(self, context):
		layout = self.layout
		layout.label('> Make single from duplication (object property) <')
		layout.label('1. parent selected to activ / 2. apply Make Duplicates Real')
		layout.label('3. clear Parent / 4. to Join > selected Linked Object Data')

	
	def execute(self, context):
		return {'FINISHED'}

	def invoke(self, context, event):
		return context.window_manager.invoke_popup(self, width = 300)



#####################################################-------------------------------------------------------
#####################################################-------------------------------------------------------
######  Repeat Menu  ################################-------------------------------------------------------
######  Repeat Menu  ################################-------------------------------------------------------



######  Keyframing  ##################-------------------------------------------------------  

def draw_keyframing_tools(context, layout):
    if context.mode=="OBJECT" or context.mode=="POSE":
            
            
       if context.active_object and context.active_object.type in {'MESH', 'CURVE', 'SURFACE', 'ARMATURE'}:

          col = layout.column(align=True)
          row = col.row(align=True)
          row.operator("anim.keyframe_insert_menu", icon='ZOOMIN', text="")
          row.operator("anim.keyframe_delete_v3d", icon='ZOOMOUT', text="")
          row.prop_search(context.scene.keying_sets_all, "active", context.scene, "keying_sets_all", text="")
          row.operator("anim.keyframe_insert", text="", icon='KEY_HLT')
          row.operator("anim.keyframe_delete", text="", icon='KEY_DEHLT')
        



######  Full History  ##################-------------------------------------------------------                         
        
def draw_history_tools(context, layout):

     col = layout.column(align=True)
     col = layout.column(align=True)
     
     row = col.row(align=True)
     sub = row.row()
     sub.scale_x = 2.0
     sub.operator("screen.repeat_last_new", text="", icon="RECOVER_LAST")	 

     sub.operator("view3d.ruler", text="R", icon="NOCURVE")
     sub.menu("VIEW3D_MT_view_cameraview", text="", icon="CAMERA_DATA")
     sub.menu("VIEW3D_MT_view_datablock", text="", icon="SETTINGS")

     #col = layout.column(align=True)
     draw_keyframing_tools(context, layout)        

     col = layout.column(align=True)
     split = layout.split()

     row = col.row(align=True)
     row.operator("ed.undo", text="", icon="LOOP_BACK")
     row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

     sub = row.row()
     sub.scale_x = 2.0 
     sub.operator("ed.undo_history", text="History")
     sub.operator("screen.redo_last", text="", icon="LOAD_FACTORY")
        

######  Half History  ##################-------------------------------------------------------                         
        
def draw_halfhistory_tools(context, layout):

     col = layout.column(align=True)
     col = layout.column(align=True)
     
     col = layout.column(align=True)
     split = layout.split()

     row = col.row(align=True)
     row.operator("ed.undo", text="", icon="LOOP_BACK")
     row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

     sub = row.row()
     sub.scale_x = 2.0 
     sub.operator("ed.undo_history", text="History")
     sub.operator("screen.redo_last", text="", icon="LOAD_FACTORY")         



######--------------####################################################################################################
######--------------####################################################################################################
######  Objectmode  ####################################################################################################
######  Objectmode  ####################################################################################################
######--------------####################################################################################################
######--------------####################################################################################################



class AlignUi(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_label = "META TOOLS"
    bl_context = "objectmode"
    bl_idname = "AlignUi"
    #bl_options = {'DEFAULT_CLOSED'}
    

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'OBJECT'))
        



    def draw(self, context):

        layout = self.layout
        obj = context.object
        scene = context.scene
        
        col = layout.column()
        row = col.row(align=True) 
        row.prop(bpy.context.object, "name")
        row.operator("wm.save_mainfile",text="",icon="FILE_TICK")
        row.operator("wm.save_as_mainfile",text="",icon="SAVE_AS") 


        if obj != None:
            row = layout.row()
            row.label(text="Active-->>>>>>: ", icon='OBJECT_DATA')
            row.label(obj.name, icon='EDITMODE_HLT')
            #row.operator("help.operator3", text="", icon = "INFO")
            
            
                
#############--------------------------------------      
   


        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")
        
        
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")


        col = layout.column(align=True)
        row = col.row(align=True)        
        row.label(text="", icon='MOD_MIRROR')

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.loops1",text="m-X")
        sub.operator("object.loops2",text="m-Y")
        sub.operator("object.loops3",text="m-Z")
        sub.operator("object.distribute_osc", text="", icon="ALIGN")
        #sub.operator("object.loops8","", icon="FILE_TICK")
        



##### Align Location ######------------------------------------------------------------
##### Align Location ######------------------------------------------------------------



        lt = bpy.context.window_manager.paul_manager
        layout = self.layout
            
       
        col = layout.column(align=True)
        split = col.split(percentage=0.15)
        
        
        if lt.display_location:
            
            split.prop(lt, "display_location", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_location", text="", icon='RIGHTARROW')
            
        spread_op = split.operator("object.align_location_all",text="Align Location", icon='MAN_TRANS') 
            
        
        if lt.display_location:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            

            #row.label(text="Align Location Axis:")
            row = col_top.row(align=True) 
            row.operator("object.align_location_x",text="X")
            row.operator("object.align_location_y",text="Y")
            row.operator("object.align_location_z",text="Z")
        
            sub = row.row()
            sub.scale_x = 2.0    
            sub.operator("object.location_clear", text="", icon="X")
          
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= True
            props.rotation= False
            props.scale= False
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("object.align_by_faces", text="Face 2 Face")
            row.operator("object.drop_on_active", text="Drop 2 Active")

       


##### Align Rotation ######------------------------------------------------------------
##### Align Rotation ######------------------------------------------------------------        



        #col = layout.column(align=True)
        split = col.split(percentage=0.15)
        
        
        if lt.display_rotation:
            
            split.prop(lt, "display_rotation", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_rotation", text="", icon='RIGHTARROW')
            
        spread_op = split.operator("object.align_rotation_all",text=" Align Rotation", icon='MAN_ROT')


        if lt.display_rotation:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)        
        

            #row.label(text="Align Rotation Axis:")
            row = col_top.row(align=True) 
            row.operator("object.align_rotation_x",text="X")
            row.operator("object.align_rotation_y",text="Y")
            row.operator("object.align_rotation_z",text="Z")
            
            sub = row.row()
            sub.scale_x = 2.0           
            sub.operator("object.rotation_clear", text="", icon="X")
            row. operator("object.loops8","", icon="FILE_TICK")
           
            col_top = box.column(align=True)
            row = col_top.row(align=True)        
            row.operator("lookat.it", text="Look @ Obj")
            row.operator("lookat.cursor", text="Look @ Cursor")               
            
            


##### Align Scale ######------------------------------------------------------------
##### Align Scale ######------------------------------------------------------------

            

        #col = layout.column(align=True)
        split = col.split(percentage=0.15)
        
        
        if lt.display_scale:
            
            split.prop(lt, "display_scale", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_scale", text="", icon='RIGHTARROW')
            
        spread_op = split.operator("object.align_objects_scale_all",text=" Align Scale", icon='MAN_SCALE')    


        if lt.display_scale:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)              
                   
            #row.label(text="Align Scale Axis:")
            row = col_top.row(align=True) 
            row.operator("object.align_objects_scale_x",text="X")
            row.operator("object.align_objects_scale_y",text="Y")
            row.operator("object.align_objects_scale_z",text="Z")
            
            sub = row.row()
            sub.scale_x = 2.0           
            sub.operator("object.scale_clear", text="", icon="X")
            
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= False
            props.rotation= False
            props.scale= True        
        


#######  Freeze  #######-------------------------------------------------------  
#######  Freeze  #######-------------------------------------------------------


        split = col.split(percentage=0.15)
        
        
        if lt.display_freeze:
            
            split.prop(lt, "display_freeze", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_freeze", text="", icon='RIGHTARROW')
            
        spread_op = split.operator("view3d.freeze_selected", text="Freeze", icon="FREEZE")

        if lt.display_freeze:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("freeze_transform.selected", text="Zero Transform Position", icon="MANIPUL")

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("object.mesh_all", text="Mesh", icon="OBJECT_DATAMODE")
            row.operator("object.lamp_all",text="Lampe", icon="LAMP")
        
            row = col_top.row(align=True)
            row.operator("object.curve_all",text="Curve", icon="OUTLINER_OB_CURVE")
            row.operator("object.bone_all",text="Bone", icon="BONE_DATA")
        
            row = col_top.row(align=True)
            row.operator("object.particles_all", text="Particle", icon="MOD_PARTICLES")
            row.operator("object.camera_all", text="Camera", icon="OUTLINER_DATA_CAMERA")

            
##### Align Rotation ######------------------------------------------------------------
##### Align Rotation ######------------------------------------------------------------
        


        #col = layout.column(align=True)
        split = col.split(percentage=0.15)
        
        
        if lt.display_selection:
            
            split.prop(lt, "display_selection", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_selection", text="", icon='RIGHTARROW')
            
        spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")

        if lt.display_selection:
            
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)        
        

            row.operator("object.hide_view_set", text="Hide").unselected=False
            row.operator("object.hide_view_set", text="Unhide").unselected=True
            row.operator("object.hide_view_clear", text="Show All") 
      
            row = col_top.row(align=True)
            row.label(text="------------------------------------------------------------------------------------------------------------")

            row = col_top.row(align=True) 
            row.operator("object.select_linked", text="Linked", icon="EXPORT") 
            row.operator("object.select_grouped", text="Group", icon="EXPORT")        
        
            row = col_top.row(align=True) 
            row.operator("object.select_by_type", text="Type", icon="EXPORT")        
            row.operator("object.select_pattern", text="Name", icon="EXPORT")
            
            row = col_top.row(align=True)
            row.label(text="------------------------------------------------------------------------------------------------------------")
            
            row = col_top.row(align=True)
            row.operator("object.select_pattern", text="Pattern")


            row = col_top.row(align=True) 
            row.operator("object.select_random", text="Random")            
            row.operator("object.select_all", text="Inverse").action = 'INVERT'

            
            row = col_top.row(align=True)
            row.operator("object.select_mirror", text="Mirror")
            row.operator("object.select_by_layer", text="Layer")

            
            row = col_top.row(align=True)
            row.operator("object.select_camera", text="Camera")        

        col.label(text="----------------------------------------------------------------------------------------------------------------")                

        ###----------------------------

        #col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("view3d.origin_3dcursor", text="", icon="CURSOR")
        row.operator("object.origin_set", text="", icon="OBJECT_DATAMODE").type='ORIGIN_GEOMETRY'
        row.operator("object.origin_set", text="", icon="FORCE_FORCE").type='ORIGIN_CURSOR'
        
        row.operator("object.origin_set", text="Origin")
        row.operator("help.operator2", text="", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("object.join",text=">>>  Join Objects  <<<")
        

      


            
        col.label(text="----------------------------------------------------------------------------------------------------------------")                

        
###########################-------------------------------------------------------
#######  Im-Export  #######-------------------------------------------------------  
#######  Im-Export  #######-------------------------------------------------------
###########################-------------------------------------------------------

    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_inexport:
            split.prop(lt, "display_inexport", text="...Im-Export...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_inexport", text="...Im-Export...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_inexport:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.menu("INFO_MT_file_import", icon='IMPORT')
            #row = col_top.row(align=True)
            row.menu("INFO_MT_file_export", icon='EXPORT')
            row = col_top.row(align=True)
            row.menu("OBJECT_MT_selected_export", text="Export Selected",icon='EXPORT')

            row = col_top.row(align=True)
            row.label(text="------------------------------------------------------------------------------------------------------------")
             

            row = col_top.row(align=True)
           
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)            
            row.operator_context = 'INVOKE_AREA'
            row.operator("wm.link_append", text="Link", icon='LINK_BLEND')
            props = row.operator("wm.link_append", text="Append", icon='APPEND_BLEND')
            props.link = False
            props.instance_groups = False
            
            
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("object.make_local")
            row.operator("object.proxy_make")



            col_top = box.column(align=True)           	
            row = col_top.row(align=True)
            row.label(text="------------------------------------------------------------------------------------------------------------")
            
           
            row = col_top.row(align=True)
            row.operator("productionfolder_scene.selected",text="Production Folder",icon="FILE_FOLDER")
            row = col_top.row(align=True)
            row.operator("production_scene.selected",text="Save into Folder",icon="NEWFOLDER")
            #if vismaya_tools.pfopath != "":
               #row.operator("file.production_folder", text="Show Production",icon="SHOW_PRODUCTION")
        

###############################------------------------------------------------------- 
#######  Modifier  ############-------------------------------------------------------     
#######  Modifier  ############-------------------------------------------------------   
###############################------------------------------------------------------- 

        split = col.split()#percentage=0.15)
        
        
        if lt.display_placer:
            
            split.prop(lt, "display_placer", text="...ModTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_placer", text="...ModTools...", icon='RIGHTARROW')
            
        #spread_op = split.operator("view3d.select_border", text="Placer", icon="SNAP_SURFACE")

        if lt.display_placer:
            
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)                    
            row.operator_menu_enum("object.modifier_add", "type", text="--- Add Modifier ---", icon="MODIFIER")

            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("view3d.fullmirror",icon='MOD_MIRROR',text="Mir-X")
            row.operator("view3d.fullmirrory",icon='MOD_MIRROR',text="Mir-Y")
            row.operator("view3d.fullmirrorz",icon='MOD_MIRROR',text="Mir-Z")
            row = col_top.row(align=True)
            row.operator("view3d.halfshrink",icon='MOD_SHRINKWRAP',text="Shrinkwrap")
         
            
            row = col_top.row(align=True)            
            row.operator("mesh.primitive_symmetrical_empty_add",text="Symmetrical Empty",icon="OUTLINER_OB_EMPTY") 


         


#######  Subdivision Level  #######------------------------------------------------------- 
#######  Subdivision Level  #######-------------------------------------------------------         

                 

        #col = layout.column(align=True)   
            split = col.split()#percentage=0.15)
        
            if lt.display_modi:
                split.prop(lt, "display_modi", text="-- Subdivision Level --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_modi", text="-- Subdivision Level --", icon='RIGHTARROW')

            #spread_op = split.operator("object.modifier_add", text="Subdivision Level", icon = 'MOD_SUBSURF').type="SUBSURF"

            
            if lt.display_modi:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)


                #row.label("Levels")
        
                row = col_top.row(align=True)
                row.operator("view3d.modifiers_subsurf_level_0")
                row.operator("view3d.modifiers_subsurf_level_1")
                row.operator("view3d.modifiers_subsurf_level_2")
                row.operator("view3d.modifiers_subsurf_level_3")
                row.operator("view3d.modifiers_subsurf_level_4")
                row.operator("view3d.modifiers_subsurf_level_5")
                row.operator("view3d.modifiers_subsurf_level_6")
            


 
#######  Visual  #######-------------------------------------------------------  
#######  Visual  #######-------------------------------------------------------  



        #col = layout.column(align=True)
            split = col.split()#percentage=0.15)
        
        
            if lt.display_shade:
                split.prop(lt, "display_shade", text="-- Visual --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_shade", text="-- Visual --", icon='RIGHTARROW')
            
            #spread_op = split.operator("object.shade_smooth", text="Visual", icon="MESH_CUBE")
            
        
            if lt.display_shade:
                box = col.column(align=True).box().column()
			
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                
                col.alignment = 'EXPAND'

                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_viewport_on",icon = 'RESTRICT_VIEW_OFF')
                row.operator("view3d.display_modifiers_edit_on", icon = 'EDITMODE_HLT')
                row.operator("view3d.display_modifiers_cage_on",icon = 'OUTLINER_OB_MESH')
                row.operator("view3d.display_wire_on", "On", icon = 'WIRE')

           
                col.alignment = 'EXPAND'


                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_viewport_off",icon = 'VISIBLE_IPO_OFF')         
                row.operator("view3d.display_modifiers_edit_off",icon = 'SNAP_VERTEX')  
                row.operator("view3d.display_modifiers_cage_off",icon = 'OUTLINER_DATA_MESH')
                row.operator("view3d.display_wire_off", "Off", icon = 'SOLID')

        
                col_top = box.column(align=True)
      
                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_apply", icon = 'FILE_TICK')
                row.operator("view3d.display_modifiers_delete", icon = 'X')

                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_expand", icon = 'TRIA_DOWN')
                row.operator("view3d.display_modifiers_collapse", icon = 'TRIA_RIGHT') 
                

                         
            



#######  Mirror #######-------------------------------------------------------  
#######  Mirror #######-------------------------------------------------------   

            

            
        #col = layout.column(align=True)
            split = col.split()#percentage=0.15)
        
        
            if lt.display_mirrorcut:
                split.prop(lt, "display_mirrorcut", text="-- Custom --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_mirrorcut", text="-- Custom -- ", icon='RIGHTARROW')
            
            #spread_op = split.operator("object.modifier_add", text="Mirrorcut", icon="MOD_MIRROR").type="MIRROR"
            
        
            if lt.display_mirrorcut:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)  
                row.operator("object.add_fracture_cell_objects", text="Cell Fracture") 
    
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.label(text="half cut geometry",icon="MOD_MIRROR")       
            
            
                row = col_top.row(align=True)
                row.operator("add.mmx", text="X")
                row.operator("add.mmy", text="Y")    
                row.operator("add.mmz", text="Z")

                col = layout.column(align=True)             
        
                row = col_top.row(align=True)
                row.operator("add.mmmx", text="-X")
                row.operator("add.mmmy", text="-Y")     
                row.operator("add.mmmz", text="-Z")


##########################-------------------------------------------------------  
#######  CadTools  #######-------------------------------------------------------  
#######  CadTools  #######-------------------------------------------------------  
##########################------------------------------------------------------- 



        #col = layout.column(align=True)

        split = col.split()#percentage=0.15)
        
        if lt.display_cadtools:
            split.prop(lt, "display_cadtools", text="...CadTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_cadtools", text="...CadTools...", icon='RIGHTARROW')

        #split.operator("mesh.intersect_meshes",text="Intersection Line")        

               
        if lt.display_cadtools:
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)      
            row.operator("object.bounding_boxers",text="Box", icon="OBJECT_DATA")
            row.operator("view3d.fullcurve", "Curve", icon="OUTLINER_OB_CURVE")
            row = col_top.row(align=True)          
            row.operator("mesh.intersect_meshes",text="Object Intersection Line", icon="GROUP")

     


######  AlignEdges  ######-----------------------------------------
######  AlignEdges  ######-----------------------------------------              

            
        
            split = col.split()
            if lt.display_align:
                split.prop(lt, "display_align", text="-- Align Edges --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_align", text="-- Align Edges --", icon='RIGHTARROW')
            
        
            if lt.display_align and context.mode == 'EDIT_MESH':
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
                row = col_top.row(align=True)
                align_op = row.operator("mesh.align_operator", text = 'Align').type_op = 0
                row = col_top.row(align=True)
                row.prop(lt, 'align_dist_z', text = 'Superpose')
                row = col_top.row(align=True)
                row.prop(lt, 'align_lock_z', text = 'lock Z')
            
            if lt.display_align and context.mode == 'OBJECT':
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
                row = col_top.row(align=True)
                align_op = row.operator("mesh.align_operator", text = 'Align').type_op = 2
                row = col_top.row(align=True)
                row.prop(context.scene,'AxesProperty', text = 'Axis')
                row = col_top.row(align=True)
                row.prop(context.scene,'ProjectsProperty', text = 'Projection')

            
      
######  SideShift  ######-----------------------------------------
######  SideShift  ######-----------------------------------------    


            
        
            split = col.split()
            if lt.display_offset:
                split.prop(lt, "display_offset", text="-- SideShift --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_offset", text="-- SideShift --", icon='RIGHTARROW')
        
            if lt.display_offset:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)
            
                row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
                row = col_top.row(align=True)
                row.operator("mesh.offset_operator", text = 'Active » Cursor').type_op = 3
            
                row = col_top.row(align=True)
                lockX_op = row.prop(lt,"shift_lockX", text="X", icon='FREEZE')
                lockY_op = row.prop(lt,"shift_lockY", text="Y", icon='FREEZE')
                lockZ_op = row.prop(lt,"shift_lockZ", text="Z", icon='FREEZE')
                row = col_top.row(align=True)
                row.prop(lt,"shift_local", text="Local")
            
                row = col_top.row(align=True)
                split = col_top.split(percentage=0.76)
                split.prop(lt,'step_len', text = 'dist')
                getlenght_op = split.operator("mesh.offset_operator", text="Get dist").type_op = 1
                row = col_top.row(align=True)
                split = col_top.split(percentage=0.5)
                left_op = split.operator("mesh.offset_operator", text="", icon='TRIA_LEFT')
                left_op.type_op = 0
                left_op.sign_op = -1
                right_op = split.operator("mesh.offset_operator", text="", icon='TRIA_RIGHT')
                right_op.type_op = 0
                right_op.sign_op = 1
                row = col_top.row(align=True)
            
                if context.mode == 'EDIT_MESH':
                    row.prop(lt,"shift_copy", text="Copy")
                else:
                    row.prop(lt, "instance", text='Instance')
                    row = col_top.row(align=True)
                    row.prop(lt,"shift_copy", text="Copy")
                    


#############################-------------------------------------------------------
#######  Array Tools  #######-------------------------------------------------------                  
#######  Array Tools  #######-------------------------------------------------------        
#############################-------------------------------------------------------


        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_obarray:
            split.prop(lt, "display_obarray", text="...ArrayTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_obarray", text="...ArrayTools...", icon='RIGHTARROW')
            
         #spread_op = split.operator("object.shade_smooth", text="Visual", icon="MESH_CUBE")
            
        
        if lt.display_obarray:
            box = col.column(align=True).box().column()
			
            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.prop(bpy.context.scene, "osc_object_arewo", text="Arewo", icon="MOD_ARRAY")

            row = col_top.row(align=True)
            row.operator("object.arewo",text="Replicator")
            row.operator("object.cursor_array", text="2 Cursor")     
            

            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.operator("object.add_2array", text="2d Grid")
            row.operator("object.add_3array", text="3d Grid")

  

              
      
        
                             

######  Curve  ######--------------------------------------
######  Curve  ######--------------------------------------


            #col_top = box.column(align=True)
            split = col.split()#percentage=0.15)
        
        
            if lt.display_bezcurve:
                split.prop(lt, "display_bezcurve", text="-- Curve --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_bezcurve", text="-- Curve --", icon='RIGHTARROW')
            
           
        
            if lt.display_bezcurve:
                box = col.column(align=True).box().column()
            
                col_top = box.column(align=True)
                row = col_top.row(align=True)  
                row.operator("object.loops12", text="", icon="CURVE_BEZCURVE")
                row.operator("object.loops13", text="Beziér Curve",)
            
                col_top = box.column(align=True)
                row = col_top.row(align=True)              
                row.operator("object.loops10", text="", icon="CURVE_BEZCIRCLE")
                row.operator("object.loops11", text="Beziér Circle",)                  

                col_top = box.column(align=True)
                row = col_top.row(align=True)  
                row.operator("object.loops14", text="", icon="CURVE_BEZCIRCLE")
                row.operator("object.loops15", text="", icon="CONSTRAINT_DATA")          
                row.operator("object.fpath_array",text="Follow Path")
                row.operator("constraint.followpath_path_animate", text="", icon='ANIM_DATA')

       
                col_top = box.column(align=True)
                row = col_top.row(align=True)  
                row.operator("object.loops16",text="linked Obj")                  
                row.operator("object.loops17",text="single Obj")  
            


######  Empty  ######--------------------------------------
######  Empty  ######-------------------------------------


            #col_top = box.column(align=True)
            split = col.split()#percentage=0.15)
        
        
            if lt.display_circle:
                split.prop(lt, "display_circle", text="-- Empty --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_circle", text="-- Empty --", icon='RIGHTARROW')
            
                #spread_op = split.operator("objects.circle_array_operator1", text="Empty Array", icon="OUTLINER_OB_EMPTY")
            
        
            if lt.display_circle:
                box = col.column(align=True).box().column()
            
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("objects.circle_array_operator1", text="Cursor", icon="FORCE_FORCE")

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("objects.circle_array_operator1", text="1/4-90°", icon="MOD_ARRAY")
                row.operator("objects.circle_array_operator2", text="1/6-60°", icon="MOD_ARRAY")
            
                row = col_top.row(align=True)
                row.operator("objects.circle_array_operator3", text="1/8-45°", icon="MOD_ARRAY")
                row.operator("objects.circle_array_operator4", text="1/12-30°", icon="MOD_ARRAY")




###########################-------------------------------------------------------
#######  Relations  #######-------------------------------------------------------                  
#######  Relations  #######-------------------------------------------------------        
###########################-------------------------------------------------------


    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_relationsOB:
            split.prop(lt, "display_relationsOB", text="...Relations...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_relationsOB", text="...Relations...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_relationsOB:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_make_links", text="M.Links", icon="LINKED")
            row.menu("VIEW3D_MT_make_single_user", text="Single User")

            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("object.visual_transform_apply", icon="NDOF_DOM")
            
            row = col_top.row(align=True)
            row.operator("object.duplicates_make_real", icon="MOD_PARTICLES")
            row.operator("help.operator4",text="", icon="INFO")
            
            
            row = col_top.row(align=True)
            row.operator("object.set_instance",text="Set as Instance", icon="LINK_AREA")


######  Group  ######-------------------------------------             
######  Group  ######-------------------------------------


            split = col.split(percentage=0.15)

        
            if lt.display_group:
                split.prop(lt, "display_group", text="", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_group", text="", icon='RIGHTARROW')
            
            spread_op = split.operator("group.create", text="Group", icon="STICKY_UVS_LOC") 
            
        
            if lt.display_group:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)
    
                row = col_top.row(align=True)
                row.operator("group.create", text="Group")
                row.operator("group.objects_add_active", text="-> to Active")
            
                row = col_top.row(align=True)
                row.operator("group.objects_remove", text="Remove")
                row.operator("group.objects_remove_active", text="-> from Active")
                

######  Parent  ######-------------------------------------
######  Parent  ######-------------------------------------


            
            split = col.split(percentage=0.15)

        
            if lt.display_parent:
                split.prop(lt, "display_parent", text="", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_parent", text="", icon='RIGHTARROW')
            
            spread_op = split.operator("object.parent_set", text="Parent", icon="CONSTRAINT")

        
            if lt.display_parent:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("object.parent_clear").type="CLEAR"
                row.operator("object.parent_clear", text="Clear Inverse").type="CLEAR_INVERSE" 
                row = col_top.row(align=True)                
                row.operator("object.parent_clear", text="Clear Keep Transform").type="CLEAR_KEEP_TRANSFORM"
       

            
######  Constraint  ######-------------------------------------
######  Constraint  ######-------------------------------------


            
            split = col.split(percentage=0.15)

        
            if lt.display_constraint:
                split.prop(lt, "display_constraint", text="", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_constraint", text="", icon='RIGHTARROW')
            
            spread_op = split.operator_menu_enum("object.constraint_add", "type", text="  Constraint", icon="CONSTRAINT_DATA") 
            
        
            if lt.display_constraint:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("lookat.it", text="Look @ Obj")
                row.operator("lookat.cursor", text="Look @ Cursor")     
            
                col_top = box.column(align=True)
                row = col_top.row(align=True)           
                row.label(text="to Selected:",icon="LAYER_ACTIVE")
            
                row = col_top.row(align=True)
                row.operator("track.to", text="Track To")
                row.operator("damped.track", text="Damped Track")
                row.operator("lock.track", text="Lock Track")

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.label(text="to CursorPos+Empty:",icon="LAYER_ACTIVE")

                row = col_top.row(align=True)
                row.operator("track.toempty", text="Track To")
                row.operator("damped.trackempty", text="Damped Track")
                row.operator("lock.trackempty", text="Lock Track")
            
                #col_top = box.column(align=True)
                #row = col_top.row(align=True)
                #row.operator("object.track_set",text=">>>  Track  <<<")
                
                
                
############################-------------------------------------------------------
#######  UV Mapping  #######-------------------------------------------------------  
#######  UV Mapping  #######------------------------------------------------------- 
############################-------------------------------------------------------


        split = col.split()#percentage=0.15)
        
        if lt.display_unwrap:
            split.prop(lt, "display_unwrap", text="...UvTools ...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_unwrap", text="...UvTools....", icon='RIGHTARROW')

       #spread_op = split.operator("object.modifier_add", text="Subdivision Level", icon = 'MOD_SUBSURF').type="SUBSURF"

            
        if lt.display_unwrap:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)          

            row = col_top.row(align=True)
            row.operator("transform.translate", text ="Move Texture Space").texture_space = True



######  UV Utility  ######-------------------------------------------------
######  UV Utility  ######-------------------------------------------------
           
            
            
            split = col.split()#percentage=0.15)
       
            if lt.display_uvut:
                split.prop(lt, "display_uvut", text="-- UV Utility --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_uvut", text="-- UV Utility --", icon='RIGHTARROW')
          
        
            #split.operator("uv.reset",text="Reset")
   
            if lt.display_uvut:
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("uvutil.change_index", text="Drop Active UV Back")

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.prop(scene, "UVTexRenderActive")

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("uvutil.select_index", text="Select UVTexCoord")
                row = col_top.row(align=True)                
                row.prop(scene, "UVTexIndex", text="UVTexCoord")
                
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("uvutil.select_name", text="Select UV Name")
                row = col_top.row(align=True)                
                row.prop(scene, "UVTexGetName", text="")
                
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("uvutil.remove_active", text="Remove Active UV")     
            


######  SureUVW  ######-------------------------------------------------
######  SureUVW  ######-------------------------------------------------


            split = col.split()#percentage=0.15)
       
            if lt.display_uvsure:
                split.prop(lt, "display_uvsure", text="-- SureUVW --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_uvsure", text="-- SureUVW --", icon='RIGHTARROW')
          
        
            #split.operator("uv.reset",text="Reset")
   
            if lt.display_uvsure:
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
                row = col_top.row(align=True)

                row.label("Press this button first:")
                row = col_top.row(align=True)                
                row.operator("object.sureuvw_operator",text="Show active texture on object").action='showtex'
                row = col_top.row(align=True)
                row.label("UVW Mapping:")
                row = col_top.row(align=True)                
                row.operator("object.sureuvw_operator",text="UVW Box Map").action='box'
                row = col_top.row(align=True)
                row.operator("object.sureuvw_operator",text="Best Planar Map").action='bestplanar'
                row = col_top.row(align=True)
                row.label("1. Make Material With Raster Texture!")
                row = col_top.row(align=True)
                row.label("2. Set Texture Mapping Coords: UV!")
                row = col_top.row(align=True)
                row.label("3. Use Addon buttons")
		


################################-------------------------------------------------------                            
#######  Material Tools  #######-------------------------------------------------------  
#######  Material Tools  #######-------------------------------------------------------
################################-------------------------------------------------------

    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_material:
            split.prop(lt, "display_material", text="...MatTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_material", text="...MatTools...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_material:
            
            wm = bpy.context.window_manager
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            layout.operator_context = 'INVOKE_REGION_WIN'
            
            row = col_top.row(align=True)
            row.operator("view3d.assign_material", text="New", icon='ZOOMIN')
            row.operator("object.material_slot_remove", text="Delete", icon="ZOOMOUT")


            row = col_top.row(align=True)  
            row.menu("VIEW3D_MT_assign_material", text="Assign Material", icon='ZOOMIN')
            row = col_top.row(align=True) 
            row.menu("VIEW3D_MT_select_material", text="Select by Material",icon='HAND')
            

            row = col_top.row(align=True)
            row.operator("materials.rgbcmyw", text="RGB / CMYK", icon='ZOOMIN')    
            
            row = col_top.row(align=True)
            row.operator("node.idgenerator", text="Add ID Color Node", icon='ZOOMIN')
  


               



######  Random Face Materials  ######-------------------------------------------------
######  Random Face Materials  ######-------------------------------------------------


            split = col.split()#percentage=0.15)
       
            if lt.display_matrandom:
                split.prop(lt, "display_matrandom", text="-- Random Face --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_matrandom", text="-- Random Face --", icon='RIGHTARROW')
          
        
            #spread_op = split.operator("assign_method", text="")
            
   
            if lt.display_matrandom:
                wm = bpy.context.window_manager
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
            
                row = col_top.row(align=True)  
   
                props = context.scene.face_assigner # Create reference material assigner property group

                row = col_top.row(align=True)
                row.label(text="skip to apply")
        
                row = col_top.row(align=True)
                row.prop( props, "rand_seed" ) # Create randomization seed property on column
            
                row = col_top.row(align=True)            
                row.label(text="material prefix:")
            
                row = col_top.row(align=True)            
                row.prop( props, "mat_prefix", text="") # Material prefix property too
            
                row = col_top.row(align=True)            
                row.label(text="assignment method:")
            
                row = col_top.row(align=True)            
                row.prop( props, "assign_method", text="") # Material assignment method prop
         




######  Material Option  ######-------------------------------------------------
######  Material Option  ######-------------------------------------------------


            split = col.split()#percentage=0.15)
       
            if lt.display_matoption:
                split.prop(lt, "display_matoption", text="-- Mat Options --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_matoption", text="-- Mat Options --", icon='RIGHTARROW')
          
        
            #split.operator("view3d.replace_material", text='Replace Material', icon='ARROW_LEFTRIGHT') 
   
            if lt.display_matoption:
                wm = bpy.context.window_manager
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
            
                row = col_top.row(align=True)              
                row.operator("view3d.material_to_texface", text="Material to Texface", icon='MATERIAL_DATA')
            
                row = col_top.row(align=True)              
                row.operator("view3d.texface_to_material", text="Texface to Material", icon='MATERIAL_DATA')

                row = col_top.row(align=True)              
                row.operator("view3d.fake_user_set", text='Set Fake User', icon='UNPINNED')
            
                row = col_top.row(align=True) 
                row.operator("object.materials_to_data",text="Data",icon="MATERIAL_DATA")                   
                row.operator("object.materials_to_object",text="Object",icon="MATERIAL_DATA")            
                
                
 

######  Clean Material  ######-------------------------------------------------
######  Clean Material  ######-------------------------------------------------


            split = col.split()#percentage=0.15)
       
            if lt.display_cleanmat:
                split.prop(lt, "display_cleanmat", text="-- Mat Clean up --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_cleanmat", text="-- Mat Clean up --", icon='RIGHTARROW')
          

            #split.operator("view3d.replace_material", text='Replace Material', icon='ARROW_LEFTRIGHT')        
            
   
            if lt.display_cleanmat:

                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
                

           
                
                row = col_top.row(align=True)
                row.operator("object.clean_images")
            
                row = col_top.row(align=True)
                row.operator("object.clean_materials")

                #row = col_top.row(align=True)              
                #row.operator("view3d.clean_material_slots", text="Clean Material Slots", icon='CANCEL')
                
                row = col_top.row(align=True)              
                row.operator("view3d.material_remove", text="Remove until 1 Slots", icon='CANCEL')                
                
                row = col_top.row(align=True)
                row.operator("material.remove", text="Remove all Slot Mat", icon='CANCEL')   
                
######  Setup Wire Render  ######-------------------------------------------------
######  Setup Wire Render  ######-------------------------------------------------


            split = col.split()#percentage=0.15)
       
            if lt.display_wireset:
                split.prop(lt, "display_wireset", text="-- Mat Wire Render --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_wireset", text="-- Mat Wire Render --", icon='RIGHTARROW')
          
        
            #split.operator("scene.wire_render", text="Setup Wire Render")
   
            if lt.display_wireset:
                wm = bpy.context.window_manager
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
                
                row = col_top.row(align=True)
                row.operator("scene.wire_render", text="Apply Setup")
                
                row = col_top.row(align=True)
                row.prop(wm, 'col_clay')
                row.prop(wm, 'col_wire')
                
                col_top = box.column(align=True)
                
                row = col_top.row(align=True)
                row.prop(wm, 'selected_meshes')

                row = col_top.row(align=True)
                row.prop(wm, 'shadeless_mat')
                
                row = col_top.row(align=True)
                row.prop(wm, 'wire_view')
                
                row = col_top.row(align=True)
                row.prop(wm, 'wire_object')
                

###########################-------------------------------------------------------
#######  Extension  #######-------------------------------------------------------                  
#######  Extension  #######-------------------------------------------------------        
###########################-------------------------------------------------------


    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")


        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
      



######--------------####################################################################################################
######--------------####################################################################################################
######  Sculptmode  ####################################################################################################
######  Sculptmode  ####################################################################################################
######--------------####################################################################################################
######--------------####################################################################################################



class mask(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'    
    bl_label = "META SCULPT-MASK"
    #bl_context = "texturepaint"
    
    @classmethod
    def poll(cls, context):
        return (context.sculpt_object)
    

    
    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        
        props = row.operator("paint.hide_show", text="Box Hide")
        props.action = 'HIDE'
        props.area = 'INSIDE'

        
        props = row.operator("paint.hide_show", text="Box Show")
        props.action = 'SHOW'
        props.area = 'INSIDE' 

        
        col = layout.column(align=True)
        row = col.row(align=True)
        
        props = row.operator("paint.mask_flood_fill", text="Fill")
        props.mode = 'VALUE'
        props.value = 1
        
        
        props = row.operator("paint.mask_flood_fill", text="Clear")
        props.mode = 'VALUE'
        props.value = 0
        
        row.operator("paint.mask_flood_fill", text="Invert").mode='INVERT' 
        
        
        col = layout.column(align=True)
        row = col.row(align=True)
       
        props = row.operator("paint.hide_show", text="Show All")
        props.action = 'SHOW'
        props.area = 'ALL'
        
        props = row.operator("paint.hide_show", text="Hide Masked")
        props.area = 'MASKED'
        props.action = 'HIDE'
        

        
        #col = layout.column(align=True)
        #col.label(text="Box Masking:")
        #col.label(text="1. Fill > Box Hide")
        #col.label(text="2. Invert > Show All")
        
        ######  History  ##################-------------------------------------------------------                         
        
        draw_halfhistory_tools(context, layout)    
        


######----------------####################################################################################################        
######----------------####################################################################################################
######  Vertex Paint  ####################################################################################################
######  Vertex Paint  ####################################################################################################
######----------------####################################################################################################
######----------------####################################################################################################




class vertexpaint(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'    
    bl_label = "META V PAINT"

    
    @classmethod
    def poll(cls, context):
        return (context.vertex_paint_object)


    def draw(self, context):
        layout = self.layout
     

        col = layout.column(align=True)
      
        row = col.row(align=True)
        
        row.operator("paint.vertex_color_set", text="Set Color ")
        row.operator("paint.vertex_color_smooth", text="Smooth Color ")
        
        row = col.row(align=True)
        
        row.operator("paint.vertex_color_dirt", text="Dirt Color ")
        row = col.row(align=True)
        row.operator("paint.worn_edges", text="Worn Edges")

        ######  History  ##################-------------------------------------------------------                         
        
        draw_halfhistory_tools(context, layout)    


        
######----------------####################################################################################################
######----------------####################################################################################################
######  Weight Paint  ####################################################################################################
######  Weight Paint  ####################################################################################################
######----------------####################################################################################################
######----------------####################################################################################################


class weightpaint(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'    
    bl_context = "weightpaint"
    bl_label = "META WEIGHT"
    
    @classmethod
    def poll(cls, context):
        return (context.weight_paint_object)

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)

        row = col.row(align=True)
        row.operator("mesh.slope2vgroup", text="Slope 2 VertGroup", icon='PLUGIN')
        row = col.row(align=True)
        row.operator("mesh.height2vgroup", text="Height 2 VertGroup", icon='PLUGIN')        
        row = col.row(align=True)
        row = col.row(align=True)
        row.operator("mesh.visiblevertices", text="Visible Vertices in Cam View", icon='PLUGIN')

        ######  History  ##################-------------------------------------------------------                         
        
        draw_halfhistory_tools(context, layout)       
                                


######------------#######################################################################################################        
######------------#######################################################################################################        
######  Posemode  #######################################################################################################
######  Posemode  #######################################################################################################
######------------#######################################################################################################
######------------#######################################################################################################



class AlignUi7(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_label = "META POSE"
    bl_context = "posemode"
    #bl_options = {'DEFAULT_CLOSED'}
    

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'POSE'))


    def draw(self, context):
        layout = self.layout
      
        ob = context.active_object
        row = layout.row()
        row.label(text="", icon='OBJECT_DATA')
        row.prop(ob, "name", text="")

        if ob.type == 'ARMATURE' and ob.mode in {'EDIT', 'POSE'}:
            bone = context.active_bone
            if bone:
                row = layout.row()
                row.label(text="", icon='BONE_DATA')
                row.prop(bone, "name", text="")

        row.operator("wm.save_mainfile",text="",icon="FILE_TICK")
        row.operator("wm.save_as_mainfile",text="",icon="SAVE_AS") 

   

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager

        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")




        col.label(text="----------------------------------------------------------------------------------------------------------------")                

#########---------------------        
        

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True
        

        col.label(text="----------------------------------------------------------------------------------------------------------------")
        split = col.split()
        


################################-------------------------------------------------------             
#######  Selection Pose  #######-------------------------------------------------------  
#######  Selection Pose  #######------------------------------------------------------- 
################################------------------------------------------------------- 



        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
       
        if lt.display_editselect:
            split.prop(lt, "display_editselect", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_editselect", text="...Selection...", icon='RIGHTARROW')
            
        #spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")                    
 

        if lt.display_editselect:
            box = col.column(align=True).box().column()
			
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator_menu_enum("pose.select_grouped", "type", text="Grouped...")
            row.operator("object.select_pattern", text="Pattern...")
        
            
            row = col_top.row(align=True)
            row.label("---------------------------------------------------------------------------------------------------------------")


            col_top = box.column(align=True)   
            row = col_top.row(align=True)      
            row.operator("pose.select_mirror", text="Flip Active")
            row.operator("pose.select_all", text="Inverse").action = 'INVERT'


            col_top = box.column(align=True)
            row = col_top.row(align=True)            

            row.operator("pose.select_constraint_target", text="Constraint Target")
            row.operator("pose.select_linked", text="Linked")
        
            row = col_top.row(align=True)
            row.label("---------------------------------------------------------------------------------------------------------------")


            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("pose.select_hierarchy", text="Parent").direction = 'PARENT'
            row.operator("pose.select_hierarchy", text="Child").direction = 'CHILD'


            row = col_top.row(align=True)
            props = row.operator("pose.select_hierarchy", text="Extend Parent")
            props.extend = True
            props.direction = 'PARENT'
            
            props = row.operator("pose.select_hierarchy", text="Extend Child")
            props.extend = True
            props.direction = 'CHILD'




        

#######  PoseTools  #######-------------------------------------------------------                  
#######  PoseTools  #######-------------------------------------------------------        



    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_bonetool:
            split.prop(lt, "display_bonetool", text="...PoseTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_bonetool", text="...PoseTools...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_bonetool:
            box = col.column(align=True).box().column()


            
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("pose.push")
            row.operator("pose.relax")
            
            row = col_top.row(align=True)
            row.operator("pose.breakdown")
            

            col_top = box.column(align=True)            
            row = col_top.row(align=True)
            row.operator("pose.paste", text="Paste X-Flipped Pose").flipped = True


#######  Clear Pose  #######------------------------------------------------------- 
#######  Clear Pose  #######-------------------------------------------------------         

                 

 
        split = col.split()#percentage=0.15)
        
        if lt.display_modi:
           split.prop(lt, "display_modi", text="...Clear Pose...", icon='DOWNARROW_HLT')
        else:
           split.prop(lt, "display_modi", text="...Clear Pose...", icon='RIGHTARROW')

       #spread_op = split.operator("object.modifier_add", text="Subdivision Level", icon = 'MOD_SUBSURF').type="SUBSURF"

            
        if lt.display_modi:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("pose.transforms_clear", text="Clear All")
            row.operator("pose.user_transforms_clear", text="Reset unkeyed")
            row = col_top.row(align=True)
            row.operator("pose.loc_clear", text="Location")
            row.operator("pose.rot_clear", text="Rotation")
            row.operator("pose.scale_clear", text="Scale")                     


######  Pose Library  ######----------------------------------------- 
######  Pose Library  ######----------------------------------------- 
      

        split = col.split()#percentage=0.15)
        
        if lt.display_poselib:
            split.prop(lt, "display_poselib", text="...Pose Library...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_poselib", text="...Pose Library...", icon='RIGHTARROW')

       #split.operator("bpt.boolean_2d_union", text= "Union 2d Face")

            
        if lt.display_poselib:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True) 
            row = col_top.row(align=True)           
            row.operator("poselib.pose_add", text="Add Pose...")
            row.operator("poselib.pose_rename", text="Rename Pose...")
            
            row = col_top.row(align=True)
            row.operator("poselib.browse_interactive", text="Browse Poses...")
            
            row.operator("poselib.pose_remove", text="Remove Pose...")
            
            
            


#######  Relations Pose  #######-------------------------------------------------------                  
#######  Relations Pose  #######-------------------------------------------------------        



    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_relationsPose:
            split.prop(lt, "display_relationsPose", text="...Relations...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_relationsPose", text="...Relations...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_relationsPose:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)            
            row = col_top.row(align=True)
            
            
            row.menu("VIEW3D_MT_object_parent")
            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_pose_ik")
            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_pose_constraints")


######  Parent  ######-------------------------------------
######  Parent  ######-------------------------------------


            
        split = col.split()#percentage=0.15)

        
        if lt.display_poseparent:
            split.prop(lt, "display_poseparent", text="...Bone Groups...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_poseparent", text="...Bone Groups...", icon='RIGHTARROW')
            
        #spread_op = split.operator("armature.parent_set", text="Parent", icon="CONSTRAINT_BONE")

        
        if lt.display_poseparent:
            pose = context.active_object.pose
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)
            row = col_top.row(align=True)

            row.operator_context = 'EXEC_AREA'
            row.operator("pose.group_assign", text="Assign to New Group").type = 0
            row = col_top.row(align=True)
            if pose.bone_groups:
                active_group = pose.bone_groups.active_index + 1
                row.operator("pose.group_assign", text="Assign to Group").type = active_group
                
                row = col_top.row(align=True)
                #layout.operator_context = 'INVOKE_AREA'
                row.operator("pose.group_unassign")
                row = col_top.row(align=True)
                row.operator("pose.group_remove")
            
######  Auotname  ######----------------------------------------- 
######  Autoname  ######----------------------------------------- 
      


            col_top = box.column(align=True)
            split = col.split()#percentage=0.15)
        
            if lt.display_merge:
                split.prop(lt, "display_merge", text="-- AutoName --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_merge", text="-- AutoName --", icon='RIGHTARROW')

            #split.operator("bpt.boolean_2d_union", text= "Union 2d Face")

            
            if lt.display_merge:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)          
                row = col_top.row(align=True)
                row.operator_context = 'EXEC_AREA'
                row.operator("pose.autoside_names", text="Left/Right").axis = 'XAXIS'
                row.operator("pose.autoside_names", text="Front/Back").axis = 'YAXIS'
                row = col_top.row(align=True)
                row.operator("pose.autoside_names", text="Top/Bottom").axis = 'ZAXIS'
                row.operator("pose.flip_names", text="Flip Name")





 
################################-------------------------------------------------------
#######  Extension Pose  #######-------------------------------------------------------                  
#######  Extension Pose  #######-------------------------------------------------------        
################################-------------------------------------------------------


    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")

                        



        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
        
        
        
        

#####-----------------#######################################################################################################        
#####-----------------#######################################################################################################        
#####  Editmode Mesh  #######################################################################################################
#####  Editmode Mesh  #######################################################################################################
#####-----------------#######################################################################################################
#####-----------------#######################################################################################################



class AlignUi3(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'    
    bl_label = "META EDIT"
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH')) 

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj != None:
            row = layout.row()
            row.label(text="Active object is: ", icon='OBJECT_DATA')
            row.label(obj.name, icon='EDITMODE_HLT')
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager

        layout = self.layout
        obj = context.object
        mesh = context.active_object.data

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")


        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="EDIT")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.vertex_align",text="A", icon="ALIGN")
        sub.operator("mesh.vertex_distribute",text="D", icon="PARTICLE_POINT")          
        sub.operator("bpt.smart_vtx",text="XVT")
        sub.operator("mesh.vertices_smooth", text="S", icon ="SPHERECURVE")
          



        col.label(text="----------------------------------------------------------------------------------------------------------------")                

#########---------------------        
        
        
        #col = layout.column(align=True)
        
        row = col.row(align=True)
        row.label(text="", icon="SPACE2")

        
        row.operator("object.loops7", "Ob-Mode")
        row.operator("object.loops9", "Ed-Mode")
        row.operator("help.operator2", text="", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True
        

        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator_menu_enum("mesh.separate", "type",text=">>>  Separate Objects  <<<")
        row = col.row(align=True)
        row.operator("mesh.subdivide",text="1").number_cuts=1
        row.operator("mesh.subdivide",text="2").number_cuts=2
        row.operator("mesh.subdivide",text="3").number_cuts=3
        row.operator("mesh.subdivide",text="4").number_cuts=4
        row.operator("mesh.subdivide",text="5").number_cuts=5
        row.operator("mesh.subdivide",text="6").number_cuts=6
        row = col.row(align=True)
        row.operator("mesh.tris_convert_to_quads",text="", icon="OUTLINER_OB_LATTICE") 
        row.operator("mesh.unsubdivide", text="Un-Subdivide")
        row.operator("screen.redo_last", text="", icon="LAYER_USED")
           
        row.operator("mesh.quads_convert_to_tris",text="", icon="OUTLINER_OB_MESH")
        

        

        col.label(text="----------------------------------------------------------------------------------------------------------------")
        split = col.split()
        


###########################-------------------------------------------------------             
#######  Selection  #######-------------------------------------------------------  
#######  Selection  #######------------------------------------------------------- 
###########################------------------------------------------------------- 



        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
       
        if lt.display_editselect:
            split.prop(lt, "display_editselect", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_editselect", text="...Selection...", icon='RIGHTARROW')
            
        #spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")                    
 

        if lt.display_editselect:
            box = col.column(align=True).box().column()
			
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("object.hide_view_set", text="Hide ").unselected = False
            row.operator("object.hide_view_set", text="UnHide").unselected = True            
            row.operator("object.hide_view_clear", text="ShowAll")
            
            row = col_top.row(align=True)
            row.label("---------------------------------------------------------------------------------------------------------------")


            col_top = box.column(align=True)   
            row = col_top.row(align=True)      
            row.operator("mesh.faces_select_linked_flat", text="Linked Flat Faces", icon="FACESEL")
            row = col_top.row(align=True)
            row.operator("mesh.select_face_by_sides",text="by Side" ,icon="EDITMODE_HLT")
            row.operator("mesh.select_side_osc", text="by Vertices", icon="VERTEXSEL")


            row = col_top.row(align=True)
            sub = row.row()
            sub.scale_x = 0.3
            sub.operator("mesh.select_more",text="+")
            sub.operator("mesh.edges_select_sharp", text="Sharp")
            sub.operator("mesh.select_less",text="-")

            col_top = box.column(align=True)
            row = col_top.row(align=True)            

            row.operator("mesh.loop_multi_select",text="Ring").ring=True
            row.operator("mesh.loop_multi_select",text="Loop").ring=False
            row.operator("mesh.select_all",text="All")
        
            row = col_top.row(align=True)
            row.operator("mesh.e2e_efnve", text="Ring+")
            row.operator("mesh.e2e_evnfe", text="Loop+")
            row.operator("mesh.select_loose",text="Loose")
        
            row = col_top.row(align=True)
            row.operator("mesh.select_similar",text="Similar")
            row.operator("mesh.select_all", text="Inverse").action = 'INVERT'
            row.operator("mesh.select_linked",text="Linked")
 


##########################-------------------------------------------------------  
#######  CadTools  #######-------------------------------------------------------  
#######  CadTools  #######-------------------------------------------------------  
##########################------------------------------------------------------- 



        #col = layout.column(align=True)

        split = col.split()#percentage=0.15)
        
        if lt.display_cadtools:
            split.prop(lt, "display_cadtools", text="...CadTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_cadtools", text="...CadTools...", icon='RIGHTARROW')

        #split.operator("mesh.intersect_meshes",text="Intersection Line")        

               
        if lt.display_cadtools:
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)      
            row.operator("object.bounding_boxers",text="Box", icon="OBJECT_DATA")
            row.operator("view3d.fullcurve", "Curve", icon="OUTLINER_OB_CURVE")
            
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("bpt.boolean_2d_union", text= "Union 2d Faces")          
            row.operator("mesh.singlevertex",text="Vertex", icon="LAYER_ACTIVE")

           


######  Intersection  ######-----------------------------------------        
######  Intersection  ######-----------------------------------------        
        


            col_top = box.column(align=True)
            split = col.split(percentage=0.15)
        
            if lt.display_cad:
                split.prop(lt, "display_cad", text="", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_cad", text="", icon='RIGHTARROW')

            split.operator("bpt.smart_vtx",text="XVT Edges")       

               
            if lt.display_cad:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
            
                row = col_top.row(align=True)
                row.operator("mesh.intersectall", text="Bevel X ")
                row.operator("mesh.vertdelete", text="X Delete")              
            
            
                col_top = box.column(align=True)
            

                row = col_top.row(align=True)
                row.operator(LengthChange.bl_idname, "Edge Length")

              
                row = col_top.row(align=True)          
                row.operator("mesh.offset_edges",text="Offset Edges") 


                row = col_top.row(align=True)          
                row.operator("mesh.intersect_meshes",text="Mesh Intersection")                




######  Rotate Face  ######-----------------------------------------        
######  Rotate Face  ######-----------------------------------------        

        
            col_top = box.column(align=True)
            col_top = box.column(align=True)
        
            split = col.split(percentage=0.15)
        
            if lt.display_rotface:
                split.prop(lt, "display_rotface", text="", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_rotface", text="", icon='RIGHTARROW')
            
            split.operator("mesh.rot_con", "Rotate Face") 
        
        
            if lt.display_rotface:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
            
                row = col_top.row(align=True)
                row.operator("mesh.face_rotate_xz45", "Xz 45°")
                row.operator("mesh.face_rotate_yz45", "Yz 45°")
                row.operator("mesh.face_rotate_zx45", "Zx 45°")
            

                row = col_top.row(align=True)
                row.operator("mesh.face_rotate_xy45", "Xy 45°")
                row.operator("mesh.face_rotate_yx45", "Yx 45°")            
                row.operator("mesh.face_rotate_zy45", "Zy 45°")

            
           
                 



             
        

######  Merge Vertices  ######----------------------------------------- 
######  Merge Vertices  ######----------------------------------------- 
      


#            col_top = box.column(align=True)
#            split = col.split(percentage=0.15)
        
#            if lt.display_merge:
#                split.prop(lt, "display_merge", text="", icon='DOWNARROW_HLT')
#            else:
#                split.prop(lt, "display_merge", text="", icon='RIGHTARROW')

#            split.operator("bpt.boolean_2d_union", text= "Union 2d Face")

            
#            if lt.display_merge:
#                box = col.column(align=True).box().column()
#                col_top = box.column(align=True)
            
#               row = col_top.row(align=True)
#                row.operator("mesh.simple_scale_operator", text='XYcollapse')
#                row = col_top.row(align=True)
#                row.operator("mesh.merge", text= "Merge Vertices")
  

######  Spread Loops  ######-----------------------------------------          
######  Spread Loops  ######----------------------------------------- 

      

#            col_top = box.column(align=True)
#            split = col.split(percentage=0.15)
       
#            if lt.display:
#                split.prop(lt, "display", text="", icon='DOWNARROW_HLT')
#            else:
#                split.prop(lt, "display", text="", icon='RIGHTARROW')

#            spread_op = split.operator("mesh.spread_operator", text = 'Spread Loop')
#            spread_op.spread_x = lt.spread_x
#            spread_op.spread_y = lt.spread_y
#            spread_op.spread_z = lt.spread_z
#            spread_op.relation = lt.relation
            
#            if lt.display:
#                box = col.column(align=True).box().column()
#                col_top = box.column(align=True)
#                row = col_top.row(align=True)
#                row.prop(lt, 'spread_x', text = 'Spread X')
#                row = col_top.row(align=True)
#                row.prop(lt, 'spread_y', text = 'Spread Y')
#                row = col_top.row(align=True)
#                row.prop(lt, 'spread_z', text = 'Spread Z')
#                row = col_top.row(align=True)
#                row = col_top.row(align=True)
#                row.prop(lt, 'relation', text = 'Relation')
           


                

######  ExtrudeSpecial  ######-----------------------------------------         
######  ExtrudeSpecial  ######-----------------------------------------         



            split = col.split()#percentage=0.15)
        
            if lt.display_extrude:
                split.prop(lt, "display_extrude", text="-- Extrude --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_extrude", text="-- Extrude --", icon='RIGHTARROW')

            #split.operator("mesh.intersect_meshes",text="Intersection Line")        

               
            if lt.display_extrude:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
            
                row = col_top.row(align=True)
                row.operator('object.mextrude', text="Multi Extrude")
            
                row = col_top.row(align=True) 
                row.operator("faceinfillet.op0_id",  text="Face Inset Fillet")
            
                row = col_top.row(align=True) 
                row.operator("f.op0_id",  text="Edge Fillet")
         
                row = col_top.row(align=True) 
                row.operator("mesh.extrude_along_curve", text="Extrude Along Curve")
            
                
                row = col_top.row(align=True)
                row.operator("mechappo.select", text="Mechappo_Random Select")
                row = col_top.row(align=True)
                row.operator("mechappo.create", text="Mechappo_Extrude")   



######  AlignEdges  ######-----------------------------------------
######  AlignEdges  ######-----------------------------------------              

            
        
            split = col.split()
            if lt.display_align:
                split.prop(lt, "display_align", text="-- Align Edges --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_align", text="-- Align Edges --", icon='RIGHTARROW')
            
        
            if lt.display_align and context.mode == 'EDIT_MESH':
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
                row = col_top.row(align=True)
                align_op = row.operator("mesh.align_operator", text = 'Align').type_op = 0
                row = col_top.row(align=True)
                row.prop(lt, 'align_dist_z', text = 'Superpose')
                row = col_top.row(align=True)
                row.prop(lt, 'align_lock_z', text = 'lock Z')
            
            if lt.display_align and context.mode == 'OBJECT':
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
                row = col_top.row(align=True)
                align_op = row.operator("mesh.align_operator", text = 'Align').type_op = 2
                row = col_top.row(align=True)
                row.prop(context.scene,'AxesProperty', text = 'Axis')
                row = col_top.row(align=True)
                row.prop(context.scene,'ProjectsProperty', text = 'Projection')

            
      
######  SideShift  ######-----------------------------------------
######  SideShift  ######-----------------------------------------    


            
        
            split = col.split()
            if lt.display_offset:
                split.prop(lt, "display_offset", text="-- SideShift --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_offset", text="-- SideShift --", icon='RIGHTARROW')
        
            if lt.display_offset:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)
            
                row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
                row = col_top.row(align=True)
                row.operator("mesh.offset_operator", text = 'Active » Cursor').type_op = 3
            
                row = col_top.row(align=True)
                lockX_op = row.prop(lt,"shift_lockX", text="X", icon='FREEZE')
                lockY_op = row.prop(lt,"shift_lockY", text="Y", icon='FREEZE')
                lockZ_op = row.prop(lt,"shift_lockZ", text="Z", icon='FREEZE')
                row = col_top.row(align=True)
                row.prop(lt,"shift_local", text="Local")
            
                row = col_top.row(align=True)
                split = col_top.split(percentage=0.76)
                split.prop(lt,'step_len', text = 'dist')
                getlenght_op = split.operator("mesh.offset_operator", text="Get dist").type_op = 1
                row = col_top.row(align=True)
                split = col_top.split(percentage=0.5)
                left_op = split.operator("mesh.offset_operator", text="", icon='TRIA_LEFT')
                left_op.type_op = 0
                left_op.sign_op = -1
                right_op = split.operator("mesh.offset_operator", text="", icon='TRIA_RIGHT')
                right_op.type_op = 0
                right_op.sign_op = 1
                row = col_top.row(align=True)
            
                if context.mode == 'EDIT_MESH':
                    row.prop(lt,"shift_copy", text="Copy")
                else:
                    row.prop(lt, "instance", text='Instance')
                    row = col_top.row(align=True)
                    row.prop(lt,"shift_copy", text="Copy")
                    
                    
                    
##########################------------------------------------------------------- 
#######  Modifier  #######-------------------------------------------------------     
#######  Modifier  #######-------------------------------------------------------   
##########################------------------------------------------------------- 
 

        split = col.split()#percentage=0.15)
        
        
        if lt.display_placer:
            
            split.prop(lt, "display_placer", text="...ModTools...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_placer", text="...ModTools...", icon='RIGHTARROW')
            
        #spread_op = split.operator("view3d.select_border", text="Placer", icon="SNAP_SURFACE")

        if lt.display_placer:
            
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)                    
            row.operator_menu_enum("object.modifier_add", "type", text="--- Add Modifier ---", icon="MODIFIER")


            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("view3d.fullmirror",icon='MOD_MIRROR',text="Mir-X")
            row.operator("view3d.fullmirrory",icon='MOD_MIRROR',text="Mir-Y")
            row.operator("view3d.fullmirrorz",icon='MOD_MIRROR',text="Mir-Z")
            row = col_top.row(align=True)
            row.operator("object.vertex_group_assign", text="", icon="ZOOMIN")
            row.operator("object.vertex_group_remove_from", text="", icon="ZOOMOUT")
            row.operator("view3d.fullshrink",icon='MOD_SHRINKWRAP',text="Shrinkwrap")
            row.operator("object.vertex_group_select", text="", icon="RESTRICT_SELECT_OFF")
            row.operator("object.vertex_group_deselect", text="", icon="RESTRICT_SELECT_ON")            

            
            row = col_top.row(align=True)            
            row.operator("mesh.primitive_symmetrical_empty_add",text="Symmetrical Empty",icon="OUTLINER_OB_EMPTY")
            row.operator("mesh.singlevertex",text="",icon="LAYER_ACTIVE")  
      


#######  Subdivision Level  #######------------------------------------------------------- 
#######  Subdivision Level  #######-------------------------------------------------------         

                 

        #col = layout.column(align=True)   
            split = col.split()#percentage=0.15)
        
            if lt.display_modi:
                split.prop(lt, "display_modi", text="-- Subdivision Level --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_modi", text="-- Subdivision Level --", icon='RIGHTARROW')

            #spread_op = split.operator("object.modifier_add", text="Subdivision Level", icon = 'MOD_SUBSURF').type="SUBSURF"

            
            if lt.display_modi:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)


                #row.label("Levels")
        
                row = col_top.row(align=True)
                row.operator("view3d.modifiers_subsurf_level_0")
                row.operator("view3d.modifiers_subsurf_level_1")
                row.operator("view3d.modifiers_subsurf_level_2")
                row.operator("view3d.modifiers_subsurf_level_3")
                row.operator("view3d.modifiers_subsurf_level_4")
                row.operator("view3d.modifiers_subsurf_level_5")
                row.operator("view3d.modifiers_subsurf_level_6")
            


 
#######  Visual  #######-------------------------------------------------------  
#######  Visual  #######-------------------------------------------------------  



        #col = layout.column(align=True)
            split = col.split()#percentage=0.15)
        
        
            if lt.display_shade:
                split.prop(lt, "display_shade", text="-- Visual --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_shade", text="-- Visual --", icon='RIGHTARROW')
            
            #spread_op = split.operator("object.shade_smooth", text="Visual", icon="MESH_CUBE")
            
        
            if lt.display_shade:
                box = col.column(align=True).box().column()
			
                col_top = box.column(align=True)
                row = col_top.row(align=True)

                col.alignment = 'EXPAND'

                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_viewport_on",icon = 'RESTRICT_VIEW_OFF')
                row.operator("view3d.display_modifiers_edit_on", icon = 'EDITMODE_HLT')
                row.operator("view3d.display_modifiers_cage_on",icon = 'OUTLINER_OB_MESH')
                row.operator("view3d.display_wire_on", "On", icon = 'WIRE')

           
                col.alignment = 'EXPAND'


                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_viewport_off",icon = 'VISIBLE_IPO_OFF')         
                row.operator("view3d.display_modifiers_edit_off",icon = 'SNAP_VERTEX')  
                row.operator("view3d.display_modifiers_cage_off",icon = 'OUTLINER_DATA_MESH')
                row.operator("view3d.display_wire_off", "Off", icon = 'SOLID')

        
                col_top = box.column(align=True)
      
                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_apply", icon = 'FILE_TICK')
                row.operator("view3d.display_modifiers_delete", icon = 'X')

                row = col_top.row(align=True)
                row.operator("view3d.display_modifiers_expand", icon = 'TRIA_DOWN')
                row.operator("view3d.display_modifiers_collapse", icon = 'TRIA_RIGHT') 
                



#######  Mirror #######-------------------------------------------------------  
#######  Mirror #######-------------------------------------------------------   

            

            
        #col = layout.column(align=True)
            split = col.split()#percentage=0.15)
        
        
            if lt.display_mirrorcut:
                split.prop(lt, "display_mirrorcut", text="-- Custom --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_mirrorcut", text="-- Custom --", icon='RIGHTARROW')
            
            #spread_op = split.operator("object.modifier_add", text="Mirrorcut", icon="MOD_MIRROR").type="MIRROR"
            
        
            if lt.display_mirrorcut:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)
                row = col_top.row(align=True)


                row.label(text="half cut geometry",icon="MOD_MIRROR")       
            
            
                row = col_top.row(align=True)
                row.operator("add.mmx", text="X")
                row.operator("add.mmy", text="Y")    
                row.operator("add.mmz", text="Z")

                col = layout.column(align=True)             
        
                row = col_top.row(align=True)
                row.operator("add.mmmx", text="-X")
                row.operator("add.mmmy", text="-Y")     
                row.operator("add.mmmz", text="-Z")


######  Hook  ######-------------------------------------
######  Hook  ######-------------------------------------



            split = col.split()#percentage=0.15)

        
            if lt.display_hook:
                split.prop(lt, "display_hook", text="-- Hook --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_hook", text="-- Hook --", icon='RIGHTARROW')
            
            #spread_op = split.operator_menu_enum("object.constraint_add", "type", text="Constraint", icon="CONSTRAINT_DATA") 
            
        
            if lt.display_hook:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)
                row = col_top.row(align=True)

                row.operator_context = 'EXEC_AREA'
                row.operator("object.hook_add_newob", text="to New")
                row.operator("object.hook_add_selob", text="to Selected").use_bone = False
                
                row = col_top.row(align=True)
                row.operator("object.hook_add_selob", text="to Selected Object Bone").use_bone = True

                if [mod.type == 'HOOK' for mod in context.active_object.modifiers]:
                    
                    row = col_top.row(align=True)
                    row.operator_menu_enum("object.hook_assign", "modifier")
                    row = col_top.row(align=True)
                    row.operator_menu_enum("object.hook_remove", "modifier")
                    
                    row = col_top.row(align=True)
                    row.operator_menu_enum("object.hook_select", "modifier")
                    row = col_top.row(align=True)
                    row.operator_menu_enum("object.hook_reset", "modifier")
                    row = col_top.row(align=True)
                    row.operator_menu_enum("object.hook_recenter", "modifier")      




#########################-------------------------------------------------------
#######  Normals  #######-------------------------------------------------------                  
#######  Normals  #######-------------------------------------------------------        
#########################-------------------------------------------------------


       
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        if lt.display_normals:
            split.prop(lt, "display_normals", text="...Normals...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_normals", text="...Normals...", icon='RIGHTARROW')

        #split.operator("mesh.intersect_meshes",text="Intersection Line")        

               
        if lt.display_normals:
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("mesh.faces_shade_smooth", text="Smooth")
            row.operator("mesh.faces_shade_flat", text="Flat")          

            row = col_top.row(align=True)
            row.operator("mesh.normals_make_consistent",text="Recalculate")
            row.operator("mesh.flip_normals", text="Flip")            
            
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.prop(mesh, "show_normal_vertex", text="", icon='VERTEXSEL')
            row.prop(mesh, "show_normal_face", text="", icon='FACESEL')

            row.active = mesh.show_normal_vertex or mesh.show_normal_face
            row.prop(context.scene.tool_settings, "normal_size", text="Size")

            row = col_top.row(align=True)
            row.label("--------------------------------------------------------------------------------------------------------")
            
            row = col_top.row(align=True) 
            row.prop(mesh, "show_double_sided") 
            row = col_top.row(align=True)      
            row.prop(mesh, "use_auto_smooth")
        
            row = col_top.row(align=True)
            row.active = mesh.use_auto_smooth
            row.prop(mesh, "auto_smooth_angle", text="Angle")



#########################-------------------------------------------------------
#######  CleanUp  #######-------------------------------------------------------  
#######  CleanUp  #######------------------------------------------------------- 
#########################-------------------------------------------------------

        
        #col = layout.column(align=True)
        split = col.split()
       
        if lt.display_cleanup:
            split.prop(lt, "display_cleanup", text="...Clean Up...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_cleanup", text="...Clean Up...", icon='RIGHTARROW')
          

        if lt.display_cleanup:
            box = col.column(align=True).box().column()
			
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("mesh.remove_doubles", "X-Doubles")
            row.menu("VIEW3D_MT_object_showhide",text="Show/Hide")

            row = col_top.row(align=True)
            row.operator("mesh.delete_loose", text="X-Loose")
            row.operator("mesh.fill_holes")
            
            row = col_top.row(align=True)
            row.operator("mesh.vert_connect_nonplanar")

            row = col_top.row(align=True)           
            row.operator("mesh.dissolve_degenerate")
            row = col_top.row(align=True)
            row.operator("mesh.dissolve_limited")            



#################################-------------------------------------------------------
#######  UV Mapping Edit  #######-------------------------------------------------------  
#######  UV Mapping Edit  #######------------------------------------------------------- 
#################################-------------------------------------------------------


        split = col.split()#percentage=0.15)
        
        if lt.display_unwrap:
            split.prop(lt, "display_unwrap", text="...UvTools ...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_unwrap", text="...UvTools....", icon='RIGHTARROW')

       #spread_op = split.operator("object.modifier_add", text="Subdivision Level", icon = 'MOD_SUBSURF').type="SUBSURF"

            
        if lt.display_unwrap:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)          
            row = col_top.row(align=True)
            
            row.operator("mesh.mark_seam").clear = False
            row.operator("mesh.mark_seam", text="Clear Seam").clear = True
        

######  Uv Move  ######-------------------------------------------------------  
######  Uv Move  ######-------------------------------------------------------
        
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("view3d.move_uv", text ="Move UV [ALT+G]")
        
     

            split = col.split()#percentage=0.15)
       
            if lt.display_modi:
                split.prop(lt, "display_modi", text="-- Unwrap --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_modi", text="-- Unwrap --", icon='RIGHTARROW')
          
        
            #split.operator("uv.reset",text="Reset")
   
            if lt.display_modi:
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
            
                row = col_top.row(align=True)
                row.operator("uv.unwrap", text="Unwrap")
                row.operator("uv.reset",text="Reset")
                                
                row = col_top.row(align=True)
                row.operator("uv.smart_project", text="Smart UV Project")
                                
                row = col_top.row(align=True)
                row.operator("uv.lightmap_pack", text="Lightmap Pack")
                                
                row = col_top.row(align=True)
                row.operator("uv.follow_active_quads", text="Follow Active Quads")
                
                col_top = box.column(align=True)                                
                
                row = col_top.row(align=True)
                row.operator("uv.cube_project", text="Cube Project")
                
                row = col_top.row(align=True)
                row.operator("uv.cylinder_project", text="Cylinder Project")

                row = col_top.row(align=True)
                row.operator("uv.sphere_project", text="Sphere Project")

                row = col_top.row(align=True)
                row.operator("uv.tube_uv_unwrap", text="Tube Project")                

                col_top = box.column(align=True)                                
                
                row = col_top.row(align=True)
                row.operator("uv.project_from_view", text="Project from View").scale_to_bounds = False

                row = col_top.row(align=True)
                row.operator("uv.project_from_view", text="Project from View > Bounds").scale_to_bounds = True                                                                      



######  SureUVW  ######-------------------------------------------------
######  SureUVW  ######-------------------------------------------------


            split = col.split()#percentage=0.15)
       
            if lt.display_uvsure:
                split.prop(lt, "display_uvsure", text="-- SureUVW --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_uvsure", text="-- SureUVW --", icon='RIGHTARROW')
          
        
            #split.operator("uv.reset",text="Reset")
   
            if lt.display_uvsure:
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
                row = col_top.row(align=True)

                row.label("Press this button first:")
                row = col_top.row(align=True)                
                row.operator("object.sureuvw_operator",text="Show active texture on editor").action='showtex'
                row = col_top.row(align=True)
                row.label("UVW Mapping:")
                row = col_top.row(align=True)                
                row.operator("object.sureuvw_operator",text="UVW Box Map").action='box'
                row = col_top.row(align=True)
                row.operator("object.sureuvw_operator",text="Best Planar Map").action='bestplanar'
                row = col_top.row(align=True)
                row.label("1. Make Material With Raster Texture!")
                row = col_top.row(align=True)
                row.label("2. Set Texture Mapping Coords: UV!")
                row = col_top.row(align=True)
                row.label("3. Use Addon buttons")
		




######  TexSpace / Freestyle  ######-------------------------------------------------
######  TexSpace / Freestyle  ######-------------------------------------------------
            
            
            split = col.split()#percentage=0.15)
       
            if lt.display_uvnext:
                split.prop(lt, "display_uvnext", text="-- TexSpace / Freestyle --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_uvnext", text="-- TexSpace / Freestyle --", icon='RIGHTARROW')
          
        
            #split.operator("uv.reset",text="Reset")
   
            if lt.display_uvnext:
                box = col.column(align=True).box().column()
        
                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.label(text="Texture Space:")
                
                row = col_top.row(align=True)
                row.operator("transform.translate", text ="Move").texture_space = True
                row.operator("mesh.mark_seam", text="Scale").clear = True

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.label(text="Freestyle:")
             
                row = col_top.row(align=True)
                row.operator("mesh.mark_freestyle_face", text="Mark Face").clear=False
                row.operator("mesh.mark_freestyle_face", text="Clear Face").clear=True             
            



            

###########################-------------------------------------------------------                            
#######  Extension  #######-------------------------------------------------------  
#######  Extension  #######-------------------------------------------------------
###########################-------------------------------------------------------

    
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
 
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Add", icon="RETOPO")

            #row = col_top.row(align=True)            
            #row.prop(bpy.context.scene, "osc_object_setup", text="Setup", icon="WORLD")            	         
            #row.prop(bpy.context.scene, "osc_object_custom", text="Custom", icon="FILE_BACKUP")
            

        
        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
        
        

               
#####------------------#######################################################################################################
#####------------------#######################################################################################################
#####  Editmode Curve  #######################################################################################################
#####  Editmode Curve  #######################################################################################################
#####------------------#######################################################################################################
#####------------------#######################################################################################################



class AlignUi2(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_context = "curve_edit"
    bl_label = "META CURVE"
    #bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_CURVE'))
    
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager        
        layout = self.layout
        obj = context.object



        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")  



        col.label(text="----------------------------------------------------------------------------------------------------------------")                

#########---------------------        
        
        
        #col = layout.column(align=True)
        
        row = col.row(align=True)
        row.label(text="", icon="SPACE2")

        
        row.operator("object.loops7", "Ob-Mode")
        row.operator("object.loops9", "Ed-Mode")
        row.operator("help.operator2", text="", icon = "INFO")        

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("curve.subdivide", text="1").number_cuts=1        
        row.operator("curve.subdivide", text="2").number_cuts=2
        row.operator("curve.subdivide", text="3").number_cuts=3
        row.operator("curve.subdivide", text="4").number_cuts=4
        row.operator("curve.subdivide", text="5").number_cuts=5        
        row.operator("curve.subdivide", text="6").number_cuts=6  

        ###---------------------    		

        row = col.row(align=True) 
        row.operator("object._curve_outline",  text="Outline")
        row.operator("bpt.bezier_curve_split",  text="Split")
        row.operator("curve.make_segment",  text="Segment")
                
        


######  Selection Curve  ######-------------------------------------------------
######  selection Curve  ######-------------------------------------------------



        col.label(text="----------------------------------------------------------------------------------------------------------------")                

		

        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_selection:
            
            split.prop(lt, "display_selection", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_selection", text="...Selection...", icon='RIGHTARROW')

        #spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")

        if lt.display_selection:

            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True) 

            row.operator("curve.select_all", text="Inverse").action = 'INVERT'
            row.operator("curve.select_random", text="Random") 

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("curve.select_linked", text="Linked")             
            row.operator("curve.select_nth", text="Checker")
            

            col_top = box.column(align=True)
            row = col_top.row(align=True) 
            row.operator("curve.de_select_first", text="First")
            row.operator("curve.de_select_last", text="Last")
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)             
            row.operator("curve.select_next", text="Next")
            row.operator("curve.select_previous", text="Previous")
                   



######  Extension Curve  ######-------------------------------------------------
######  Extension Curve  ######-------------------------------------------------


    
        
        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
 
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")
            
                  

        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
 


#####--------------------#######################################################################################################
#####--------------------#######################################################################################################
#####  Editmode Lattice  #######################################################################################################
#####  Editmode Lattice  #######################################################################################################
#####--------------------#######################################################################################################
#####--------------------#######################################################################################################




class AlignUi1(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_context = "lattice_edit"
    bl_label = "META LATTICE"
    #bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_LATTICE'))
    
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager        
        layout = self.layout
        obj = context.object

        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="ARROW_LEFTRIGHT")
        sub = row.row()
        sub.scale_x = 0.2          
        sub.operator("lattice.flip", text="FlX").axis = "U"
        sub.operator("lattice.flip", text="FlY").axis = "V"
        sub.operator("lattice.flip", text="FlZ").axis = "W"
        sub.operator("lattice.make_regular", text="MReg")   



        col.label(text="----------------------------------------------------------------------------------------------------------------")                

        
        row = col.row(align=True)
        row.label(text="", icon="SPACE2")

        
        row.operator("object.loops7", "Ob-Mode")
        row.operator("object.loops9", "Ed-Mode")
        row.operator("help.operator2", text="", icon = "INFO")        

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True


      
        



######  Selection Lattice  ######-----------------------------------------------
######  Selection Lattice  ######-----------------------------------------------



        col.label(text="----------------------------------------------------------------------------------------------------------------")                
        
  	

        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_selection:
            
            split.prop(lt, "display_selection", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_selection", text="...Selection...", icon='RIGHTARROW')

        #spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")

        if lt.display_selection:

            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)

            row.operator("lattice.select_mirror", text="Mirror")
            row.operator("lattice.select_random", text="Random")

            col_top = box.column(align=True)
            row = col_top.row(align=True)            
            row.operator("lattice.select_all").action = 'TOGGLE'
            row.operator("lattice.select_all", text="Inverse").action = 'INVERT'

            col_top = box.column(align=True)
            row = col_top.row(align=True)

            row.operator("lattice.select_ungrouped", text="Ungrouped Verts")                

        


######  Extension Lattice  ######-----------------------------------------------
######  Extension Lattice  ######-----------------------------------------------


    
        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
 
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")
                      

        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
         



#####---------------------#######################################################################################################              
#####---------------------#######################################################################################################
#####  Editmode Armature  #######################################################################################################                 
#####  Editmode Armature  #######################################################################################################
#####---------------------#######################################################################################################
#####---------------------#######################################################################################################




class AlignUi4(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_context = "armature_edit"
    bl_label = "META ARMATURE"
    #bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_ARMATURE'))
    
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager        
        layout = self.layout
        obj = context.object


        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")  

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")  



        col.label(text="----------------------------------------------------------------------------------------------------------------")                


        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True
        

        col = layout.column(align=True)
        row = col.row(align=True)       
        row.operator("armature.subdivide",text="1").number_cuts=1
        row.operator("armature.subdivide",text="2").number_cuts=2
        row.operator("armature.subdivide",text="3").number_cuts=3
        row.operator("armature.subdivide",text="4").number_cuts=4
        row.operator("armature.subdivide",text="5").number_cuts=5
        row.operator("armature.subdivide",text="6").number_cuts=6                
        


######  Selection  Armature  ######------------------------------------------
######  Selection  Armature  ######------------------------------------------
        
        
        col.label(text="----------------------------------------------------------------------------------------------------------------")                



        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_selection:
            
            split.prop(lt, "display_selection", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_selection", text="...Selection...", icon='RIGHTARROW') 

            #spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")

        if lt.display_selection:

            box = col.column(align=True).box().column()

                               
            col_top = box.column(align=True)
            row = col_top.row(align=True) 
            row.operator("armature.select_mirror", text="Mirror").extend = False
            row.operator("armature.select_all", text="Inverse").action = 'INVERT'            
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)   
            row.operator("armature.select_hierarchy", text="Parent").direction = 'PARENT'
            row.operator("armature.select_hierarchy", text="Child").direction = 'CHILD'


            col_top = box.column(align=True)
            row = col_top.row(align=True) 
    
            props = row.operator("armature.select_hierarchy", text="Extend Parent")
            props.extend = True
            props.direction = 'PARENT'

            props = row.operator("armature.select_hierarchy", text="Extend Child")
            props.extend = True
            props.direction = 'CHILD'

            col_top = box.column(align=True)
            row = col_top.row(align=True)               
            
            row.operator_menu_enum("armature.select_similar", "type", text="Similar")
            row.operator("object.select_pattern", text="Pattern...")
                   

#######  BoneTools  #######-------------------------------------------------------                  
#######  BoneTools  #######-------------------------------------------------------        


    
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_bonetool:
            split.prop(lt, "display_bonetool", text="...BoneTool...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_bonetool", text="...BoneTool...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_bonetool:
            box = col.column(align=True).box().column()
            

            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("armature.merge", text="Merge", icon="AUTOMERGE_ON")
            row.operator("armature.split", text="Split")
            row = col_top.row(align=True)
            row.operator("armature.fill",text="Filler", icon="GROUP_BONE")
            row.operator("armature.separate", text="Separate")

            row = col_top.row(align=True)
            row.operator("transform.transform", text="Set Roll", icon="MAN_ROT").mode="BONE_ROLL"
            row = col_top.row(align=True)
            row.operator("armature.calculate_roll", text="Recalculate Roll", icon="FRAME_PREV")
            row = col_top.row(align=True)
            row.operator("armature.switch_direction", icon="ARROW_LEFTRIGHT")             
                    
             


#######  Relations  #######-------------------------------------------------------                  
#######  Relations  #######-------------------------------------------------------        
   
        
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_relationsARMA:
            split.prop(lt, "display_relationsARMA", text="...Relations...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_relationsARMA", text="...Relations...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_relationsARMA:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_bone_options_toggle", text="Bone Settings", icon="LONGDISPLAY")




######  Parent  ######-------------------------------------
######  Parent  ######-------------------------------------

            
            split = col.split(percentage=0.15)

        
            if lt.display_parent:
                split.prop(lt, "display_parent", text="", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_parent", text="", icon='RIGHTARROW')
            
            spread_op = split.operator("armature.parent_set", text="Parent", icon="CONSTRAINT_BONE")

        
            if lt.display_parent:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)
                row = col_top.row(align=True)

                row.operator("armature.parent_clear").type="CLEAR"
                row = col_top.row(align=True)
                row.operator("armature.parent_clear",text="Disconnect Bone").type="DISCONNECT"
        
######  Auotname  ######----------------------------------------- 
######  Autoname  ######----------------------------------------- 
      


            col_top = box.column(align=True)
            split = col.split()#percentage=0.15)
        
            if lt.display_merge:
                split.prop(lt, "display_merge", text="-- AutoName --", icon='DOWNARROW_HLT')
            else:
                split.prop(lt, "display_merge", text="-- AutoName --", icon='RIGHTARROW')

            #split.operator("bpt.boolean_2d_union", text= "Union 2d Face")

            
            if lt.display_merge:
                box = col.column(align=True).box().column()

                col_top = box.column(align=True)          
                row = col_top.row(align=True)
                row.operator_context = 'EXEC_AREA'
                row.operator("armature.autoside_names", text="AutoName Left/Right").type = 'XAXIS'
                row = col_top.row(align=True)
                row.operator("armature.autoside_names", text="AutoName Front/Back").type = 'YAXIS'
                row = col_top.row(align=True)
                row.operator("armature.autoside_names", text="AutoName Top/Bottom").type = 'ZAXIS'
                col_top = box.column(align=True)            
                row = col_top.row(align=True)
                row.operator("armature.flip_names", text="Flip Name")

    

######  Extension  Armature  ######--------------------- 
######  Extension  Armature  ######---------------------


       
        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
 
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")

        
        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
 


        
#####----------------------#######################################################################################################
#####----------------------#######################################################################################################
#####  Editmode Meta Tools #######################################################################################################
#####  Editmode Meta Tools #######################################################################################################
#####----------------------#######################################################################################################
#####----------------------#######################################################################################################




class AlignUi5(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_context = "mball_edit"
    bl_label = "META MBALL"
    #bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_METABALL'))
    
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager
        layout = self.layout
        obj = context.object


        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")  


        col.label(text="----------------------------------------------------------------------------------------------------------------")                


        row = col.row(align=True)
        row.label(text="", icon="SPACE2")

        
        row.operator("object.loops7", "Ob-Mode")
        row.operator("object.loops9", "Ed-Mode")
        row.operator("help.operator2", text="", icon = "INFO")        

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True 




######  Selection Mball  ######-------------------------------------------------
######  Selection Mball  ######-------------------------------------------------



        col.label(text="----------------------------------------------------------------------------------------------------------------")                



        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_selection:
            
            split.prop(lt, "display_selection", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_selection", text="...Selection...", icon='RIGHTARROW')

        #spread_op = split.operator("view3d.select_border", text="Selection", icon="HAND")

        if lt.display_selection:
            
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator_menu_enum("mball.select_similar", "type", text="Similar")              
            row.operator("mball.select_all").action = 'TOGGLE'
            

            col_top = box.column(align=True)
            row = col_top.row(align=True) 
            row.operator("mball.select_random_metaelems", text="Random")
            row.operator("mball.select_all", text="Inverse").action = 'INVERT'          
            
      
        
        
######  Extension Mball  ######--------------------------------------------------
######  Extension Mball  ######-------------------------------------------------



        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
 
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")
            
            

        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     

        
          
#####-------------------#######################################################################################################        
#####-------------------#######################################################################################################
#####  Editmode Surface #######################################################################################################
#####  Editmode Surface #######################################################################################################
#####-------------------#######################################################################################################
#####-------------------#######################################################################################################




class AlignUi6(bpy.types.Panel):
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_context = "surface_edit"
    bl_label = "META SURFACE"
    #bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_SURFACE'))
    
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager        
        layout = self.layout
        obj = context.object

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="",icon="MANIPUL")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
        sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
        sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")        
 
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_MIRROR")
        sub = row.row()
        sub.scale_x = 0.2	
        sub.operator("object.loops4",text="m-X")
        sub.operator("object.loops5",text="m-Y")
        sub.operator("object.loops6",text="m-Z")
        sub.operator("help.operator1", text="..", icon = "INFO")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="MOD_DISPLACE")

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.face_align_x", "f-X")
        sub.operator("mesh.face_align_y", "f-Y")           
        sub.operator("mesh.face_align_z", "f-Z")
        sub.operator("view3d.ruler", text="R", icon="NOCURVE")  


        col.label(text="----------------------------------------------------------------------------------------------------------------")                

        
        row = col.row(align=True)
        row.label(text="", icon="SPACE2")

        
        row.operator("object.loops7", "Ob-Mode")
        row.operator("object.loops9", "Ed-Mode")
        row.operator("help.operator2", text="", icon = "INFO")        

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="", icon="FORCE_FORCE")        
        
        row.operator("view3d.snap_cursor_to_center", "Center")
        row.operator("view3d.snap_cursor_to_selected", "Selected")                   
        row.operator("view3d.snap_cursor_to_active", "Active")

        row = col.row(align=True) 
        row.label(text="", icon="RESTRICT_SELECT_OFF")
                       
        row.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        row.operator("view3d.snap_selected_to_grid", text="Grid")
        row.operator("view3d.snap_selected_to_cursor", text="Offset").use_offset = True 
       
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("curve.subdivide", text="1").number_cuts=1        
        row.operator("curve.subdivide", text="2").number_cuts=2
        row.operator("curve.subdivide", text="3").number_cuts=3
        row.operator("curve.subdivide", text="4").number_cuts=4
        row.operator("curve.subdivide", text="5").number_cuts=5        
        row.operator("curve.subdivide", text="6").number_cuts=6        





######  Selection Surface  ######-----------------------------------------------
######  Selection Surface  ######-----------------------------------------------



        col.label(text="----------------------------------------------------------------------------------------------------------------")                


        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_selection:
            
            split.prop(lt, "display_selection", text="...Selection...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_selection", text="...Selection...", icon='RIGHTARROW')

        #spread_op = split.operator("view3d.select_border", text="...Selection...", icon="HAND")

        if lt.display_selection:

            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True) 

            col_top = box.column(align=True)
            row = col_top.row(align=True)             
            row.operator("curve.select_row", text="Control Point")
            row.operator("curve.select_all").action = 'TOGGLE'


            col_top = box.column(align=True)
            row = col_top.row(align=True)             
            row.operator("curve.select_random", text="Random")
            row.operator("curve.select_nth", text="Checker")

            col_top = box.column(align=True)
            row = col_top.row(align=True)             
            row.operator("curve.select_linked", text="Linked")
            row.operator("curve.select_all", text="Inverse").action = 'INVERT'            
            
            

        

######  Extension Surface  ######-----------------------------------------------
######  Extension Surface  ######-----------------------------------------------



        split = col.split()#percentage=0.15)
        
        
        if lt.display_extension:
            split.prop(lt, "display_extension", text="...Extension...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extension", text="...Extension...", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.origin_set", text="Extension", icon="UNPINNED")
            
        
        if lt.display_extension:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
 
            row.prop(bpy.context.scene, "osc_object_manage", text="Manage", icon="SEQ_SEQUENCER")
            row.prop(bpy.context.scene, "osc_object_array", text="Arrays", icon="MOD_ARRAY")


            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_visual", text="Visual", icon="VISIBLE_IPO_ON")
            row.prop(bpy.context.scene, "osc_object_cad", text="CAD", icon="GRID")
            
            
            row = col_top.row(align=True)
            
            row.prop(bpy.context.scene, "osc_object_fly", text="Flymode", icon="MOD_SOFT")
            row.prop(bpy.context.scene, "osc_object_modi", text="Modifier", icon="MODIFIER")             
            
            
            row = col_top.row(align=True)            
            
            row.prop(bpy.context.scene, "osc_object_material", text="Material", icon="MATERIAL")	         
            row.prop(bpy.context.scene, "osc_object_xtras", text="Xtras", icon="RETOPO")
                        

        ######  History  ##################-------------------------------------------------------                         
        
        draw_history_tools(context, layout)     
 



######------------##########################################################################################################
######------------##########################################################################################################
######  MenuMenu  ##########################################################################################################
######  MenuMenu  ##########################################################################################################
######------------##########################################################################################################
######------------##########################################################################################################




class VIEW3D_MT_view_cameraview(bpy.types.Menu):
    """Align Camera & View"""    
    bl_label = "Align Camera & View"

    def draw(self, context):
        layout = self.layout
        
        
        layout.operator("object.camera_add")
        
        
        layout.operator("lookat.it", text="Look @ Obj")
        layout.operator("lookat.cursor", text="Look @ Cursor") 
        
        layout.separator()  
                
        layout.operator("object.build_dolly_rig")
        layout.operator("object.build_crane_rig")

        layout.separator()
        
        layout.operator("view3d.viewnumpad", text="Active Camera").type = 'CAMERA'
        layout.operator("view3d.object_as_camera")
        
        layout.operator("view3d.camera_to_view", text="Align Active Camera to View")
        layout.operator("view3d.camera_to_view_selected", text="Align Active Camera to Selected")		

        layout.separator()

        layout.operator("view3d.view_selected")
        layout.operator("view3d.view_center_cursor")
        layout.operator("view3d.view_all", text="Center Cursor and View All").center = True   

        layout.separator()         
        layout.operator("view3d.view_lock_to_active")
        layout.operator("view3d.view_lock_clear")      

        layout.separator()        
        layout.menu("VIEW3D_MT_view_align_selected")




class VIEW3D_MT_view_datablock(bpy.types.Menu):
    """Copy & Clear Data"""  
    bl_label = "Datablock"

    def draw(self, context):
        layout = self.layout

        layout.menu("VIEW_MT_datablock_tools", text="Datablock Tools")
        layout.menu("VIEW3D_MT_copypopup", text="Copy Object Data")
        layout.menu("VIEW3D_MT_posecopypopup", text="Copy Pose Data")
        layout.menu("MESH_MT_CopyFaceSettings", text="Copy Face Settings")
        
        


class normals(bpy.types.Menu):
    bl_label = "---Normals & Shading:---"
    bl_idname = "VIEW3D_MT_normal_shading"


    def draw(self, context):
        layout = self.layout



        col = layout.column(align=True)
        #col.label(text="-----Normals & Shading:-----")
    

        row = col.row(align=True)
        row.operator("mesh.faces_shade_smooth", text="Smooth")
        
        row = col.row(align=True)
        row.operator("mesh.faces_shade_flat", text="Flat")          

 
        row = col.row(align=True)
        row.operator("mesh.normals_make_consistent",text="Recalculate")

        row = col.row(align=True)
        row.operator("mesh.flip_normals", text="Flip")
        




######-------------------##########################################################################################################
######-------------------##########################################################################################################
######  Small Functions  ##########################################################################################################
######  Small Functions  ##########################################################################################################
######-------------------##########################################################################################################
######-------------------##########################################################################################################




#####  Rotate  #####################################################################################################   
#####  Rotate  #####################################################################################################   


#----X Axis----



class rotateXz(bpy.types.Operator):
    """rotate selected face > Xz 45° """
    bl_label = "Xz 45°"
    bl_idname = "mesh.face_rotate_xz45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.mesh.rot_con(axis='0', caxis='2', rdeg=45)

        return {"FINISHED"}
    

class rotateXy(bpy.types.Operator):
    """rotate selected face > Xy 45° """
    bl_label = "Xy 45°"
    bl_idname = "mesh.face_rotate_xy45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.mesh.rot_con(axis='0', caxis='1', rdeg=45)

        return {"FINISHED"}



#----Y Axis----


class rotateYz(bpy.types.Operator):
    """rotate selected face > Yz 45° """
    bl_label = "Yz 45°"
    bl_idname = "mesh.face_rotate_yz45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.mesh.rot_con(axis='1', caxis='2', rdeg=45)

        return {"FINISHED"}  



class rotateYx(bpy.types.Operator):
    """rotate selected face > Yx 45° """
    bl_label = "Yx 45°"
    bl_idname = "mesh.face_rotate_yx45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.mesh.rot_con(axis='1', caxis='0', rdeg=45)

        return {"FINISHED"}   


#----Z Axis----

class rotateZy(bpy.types.Operator):
    """rotate selected face > Zy 45° """
    bl_label = "Zy 45°"
    bl_idname = "mesh.face_rotate_zy45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.mesh.rot_con(axis='2', caxis='1', rdeg=45)

        return {"FINISHED"}


class rotateZx(bpy.types.Operator):
    """rotate selected face > Zx 45° """
    bl_label = "Zx 45°"
    bl_idname = "mesh.face_rotate_zx45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.mesh.rot_con(axis='2', caxis='0', rdeg=45)

        return {"FINISHED"}        




#####  Flat Align XYZ  ###############################################################################################
#####  Flat Align XYZ  ###############################################################################################




class alignx(bpy.types.Operator):
    """align selected face > x"""
    bl_label = "align selected face to X axis"
    bl_idname = "mesh.face_align_x"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"} 



class aligny(bpy.types.Operator):
    """align selected face to Y axis"""
    bl_label = "align y"
    bl_idname = "mesh.face_align_y"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}



class alignz(bpy.types.Operator):
    """align selected face to Z axis"""
    bl_label = "align z"
    bl_idname = "mesh.face_align_z"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}                   



#####  Grid Array  #############################################################################################
#####  Grid Array  #############################################################################################


#bl_info = {  
 #    "name": "Grid Array",  
  #   "author": "MKB",  
   #  "version": (1, 0),  
    # "blender": (2, 6, 9),  
     #"location": "",  
     #"description": "add Array Modifiers ",  
     #"warning": "please select mesh objects",  
     #"wiki_url": "",  
     #"tracker_url": "",  
     #"category": ""}  


class addArray2(bpy.types.Operator):
    """add 2 array modifier"""
    bl_label = "2 Array Modifier"
    bl_idname = "object.add_2array"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0
    
       
    def execute(self, context):
        
       
        for obj in bpy.context.selected_objects:
	        
            bpy.context.scene.objects.active = obj
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].count = 3
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1.5
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array.001"].count = 3
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1.5
        
        return {"FINISHED"}



class addArray3(bpy.types.Operator):
    """add 3 array modifier"""
    bl_label = "3 Array Modifier"
    bl_idname = "object.add_3array"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0
    
    def execute(self, context):
        
       
        for obj in bpy.context.selected_objects:
	        
            bpy.context.scene.objects.active = obj
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].count = 3
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1.5
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array.001"].count = 3
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1.5
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array.002"].count = 3
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[2] = 1.5            

                
        return {"FINISHED"}




#####  Circle_Array  #############################################################################################
#####  Circle_Array  #############################################################################################





class Circle_ArrayB(bpy.types.Operator):
    """add an empty with array modifier to cursor / Z axis"""
    bl_label = "1/6 Circle Array"
    bl_idname = "objects.circle_array_operator2"   
    

    
    def execute(self, context):
        
       
        for obj in bpy.context.selected_objects:
	        
            bpy.context.scene.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].count = 6
            
           
        if len(bpy.context.selected_objects) == 2:
            list = bpy.context.selected_objects
            active = list[0]
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            active.select = False
            bpy.context.scene.objects.active = list[0]
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object                
            bpy.context.scene.objects.active = active            
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            return {'FINISHED'}     
        
        
        else:
            active = context.active_object
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object
            bpy.context.scene.objects.active = active
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            return {'FINISHED'} 


####----


class Circle_ArrayC(bpy.types.Operator):
    """add an empty with array modifier to cursor / Z axis"""
    bl_label = "1/8 Circle Array"
    bl_idname = "objects.circle_array_operator3"   
    

    
    def execute(self, context):
        
       
        for obj in bpy.context.selected_objects:
	        
            bpy.context.scene.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].count = 8
            
           
        if len(bpy.context.selected_objects) == 2:
            list = bpy.context.selected_objects
            active = list[0]
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            active.select = False
            bpy.context.scene.objects.active = list[0]
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object                
            bpy.context.scene.objects.active = active            
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            return {'FINISHED'}     
        
        
        else:
            active = context.active_object
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object
            bpy.context.scene.objects.active = active
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            return {'FINISHED'} 
    
        
####----


class Circle_ArrayD(bpy.types.Operator):
    """add an empty with array modifier to cursor / Z axis"""
    bl_label = "1/12 Circle Array"
    bl_idname = "objects.circle_array_operator4"   
    

    
    def execute(self, context):
        
       
        for obj in bpy.context.selected_objects:
	        
            bpy.context.scene.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].count = 12
            
           
        if len(bpy.context.selected_objects) == 2:
            list = bpy.context.selected_objects
            active = list[0]
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            active.select = False
            bpy.context.scene.objects.active = list[0]
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object                
            bpy.context.scene.objects.active = active            
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            return {'FINISHED'}     
        
        
        else:
            active = context.active_object
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object
            bpy.context.scene.objects.active = active
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            return {'FINISHED'}         
                


                         
#####  Mirror XYZ Global  ############################################################################################
#####  Mirror XYZ Global  ############################################################################################



class loop1(bpy.types.Operator):
    """Mirror over X axis / global"""                 
    bl_idname = "object.loops1"          
    bl_label = "mirror selected on X axis"                  
    bl_options = {'REGISTER', 'UNDO'}   

        
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))
       
        return {'FINISHED'}
        


class loop2(bpy.types.Operator):
    """Mirror over Y axis / global"""                
    bl_idname = "object.loops2"         
    bl_label = "mirror selected on Y axis"                 
    bl_options = {'REGISTER', 'UNDO'}   

        
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))
        
        return {'FINISHED'}
        


class loop3(bpy.types.Operator):
    """Mirror over Z axis / global"""                 
    bl_idname = "object.loops3"        
    bl_label = "mirror selected on Z axis"                  
    bl_options = {'REGISTER', 'UNDO'}   


        
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.transform.mirror(constraint_axis=(False, False, True))
        
        return {'FINISHED'}

        

#####  Mirror XYZ Local  #########################################################################################        
#####  Mirror XYZ Local  #########################################################################################



class loop4(bpy.types.Operator):
    """Mirror over X axis / local"""                 
    bl_idname = "object.loops4"          
    bl_label = "mirror selected on X axis > local"                  
    bl_options = {'REGISTER', 'UNDO'}   

        
    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='LOCAL')
       
        return {'FINISHED'}
        


class loop5(bpy.types.Operator):
    """Mirror over Y axis / local"""                
    bl_idname = "object.loops5"         
    bl_label = "mirror selected on Y axis > local"                 
    bl_options = {'REGISTER', 'UNDO'}   

        
    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(False, True, False), constraint_orientation='LOCAL')
        
        return {'FINISHED'}
        


class loop6(bpy.types.Operator):
    """Mirror over Z axis / local"""                 
    bl_idname = "object.loops6"        
    bl_label = "mirror selected on Z axis > local"                  
    bl_options = {'REGISTER', 'UNDO'}   
        
    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(False, False, True), constraint_orientation='LOCAL')
        
        return {'FINISHED'}
    
    

        
#########------------------------------------ 



class loop7(bpy.types.Operator):
    """set origin to selected / objectmode"""                 
    bl_idname = "object.loops7"          
    bl_label = "origin to selected / in objectmode"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()


        return {'FINISHED'}
    

class loop8(bpy.types.Operator):
    """apply rotation & scale to use Mirror & Face to Face correctly"""                 
    bl_idname = "object.loops8"          
    bl_label = "apply rotation & scale"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        return {'FINISHED'}    


class loop9(bpy.types.Operator):
    """set origin to selected / editmode / tip: change for local rotation"""                 
    bl_idname = "object.loops9"          
    bl_label = "origin to selected in editmode"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):


        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class loop10(bpy.types.Operator):
    """place a circle curve"""                 
    bl_idname = "object.loops10"          
    bl_label = "Circle Curve"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):
        #bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.curve.primitive_bezier_circle_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.context.object.name = "Circle Curve Array"

        return {'FINISHED'}  
    

class loop11(bpy.types.Operator):
    """place a Array & Curve modifier to selected object"""                 
    bl_idname = "object.loops11"          
    bl_label = "Circle Curve & Array"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects["Circle Curve Array"]
     
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 5 
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["Circle Curve Array"]        

        return {'FINISHED'}   
       

class loop12(bpy.types.Operator):
    """place a path curve"""                 
    bl_idname = "object.loops12"          
    bl_label = "Path Curve & Array"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):

        #bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.curve.primitive_bezier_curve_add(radius=10)
        bpy.context.object.name = "Path Curve Array"        
        return {'FINISHED'}
    

class loop13(bpy.types.Operator):
    """place a Array & Curve modifier to selected object"""                 
    bl_idname = "object.loops13"          
    bl_label = "Path Curve Array"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects["Path Curve Array"]
     
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["Path Curve Array"]  

        return {'FINISHED'}         
        


###############-------------------------------------------


 
class pivotCursor(bpy.types.Operator):
   """Set pivot point to 3D Cursor"""
   bl_label = "Set pivot point to 3D Cursor"
   bl_idname = "view3d.pivot_3d_cursor"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'CURSOR'
       return {"FINISHED"} 



class pivotMedian(bpy.types.Operator):
    """Set pivot point to Median Point"""
    bl_label = "Set pivot point to Median Point"
    bl_idname = "view3d.pivot_median"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        return {"FINISHED"}


class pivotActive(bpy.types.Operator):
   """Set pivot point to Active"""
   bl_label = "Set pivot point to Active"
   bl_idname = "view3d.pivot_active"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
       return {"FINISHED"} 



class pivotIndividual(bpy.types.Operator):
    """Set pivot point to Individual"""
    bl_label = "Set pivot point to Individual Point"
    bl_idname = "view3d.pivot_individual"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        return {"FINISHED"}    



############-----------------------------------------------------



class pivotCursor3d(bpy.types.Operator):
    """place the origin between all selected with 3d cursor"""
    bl_label = "Set origin between selected with 3d cursor"
    bl_idname = "view3d.origin_3dcursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.space_data.pivot_point = 'CURSOR'
  
        return {"FINISHED"}
    

class pivotCursor3d2(bpy.types.Operator):
    """place the origin of the active to cursor with 3d cursor"""
    bl_label = "place the origin to cursor with 3d cursor"
    bl_idname = "view3d.origin_3dcursor2"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.space_data.pivot_point = 'CURSOR'

  
        return {"FINISHED"}


class pivotCursor3d3(bpy.types.Operator):
    """origin to geometry with median pivot"""
    bl_label = "origin to geometry"
    bl_idname = "view3d.origin_3dcursor3"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'

  
        return {"FINISHED"}




############-----------------------------------------------------



class FullCurve(bpy.types.Operator):
    """Add A full Bevel Curve"""
    bl_idname = "view3d.fullcurve"
    bl_label = "A full Bevel Curve"

    def execute(self, context):
    
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_resolution = 8
        bpy.context.object.data.resolution_u = 10
        bpy.context.object.data.bevel_depth = 0.2
        return {'FINISHED'}    




class Freeze_Selected(bpy.types.Operator):
    """freeze selection / unfreeze by type - doupleclick"""
    bl_idname = "view3d.freeze_selected"
    bl_label = "Freeze Selected"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        
        for obj in bpy.context.selected_objects:
    
            bpy.context.scene.objects.active = obj
    
            bpy.context.object.hide_select = True        
        

        return{'FINISHED'}



class UnFreeze_Selected(bpy.types.Operator):
    bl_idname = "view3d.unfreeze_selected"
    bl_label = "UnFreeze Selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        for obj in bpy.context.selected_objects:
    
             bpy.context.object.hide_select = False
             bpy.context.scene.objects.active = obj        

        return{'FINISHED'}  


class FullMIRROR(bpy.types.Operator):
    """Add a x mirror modifier"""
    bl_idname = "view3d.fullmirror"
    bl_label = "Mirror X"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}


class FullMIRRORY(bpy.types.Operator):
    """Add a y mirror modifier"""
    bl_idname = "view3d.fullmirrory"
    bl_label = "Mirror Y"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_x = False
        bpy.context.object.modifiers["Mirror"].use_y = True
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}


class FullMIRRORZ(bpy.types.Operator):
    """Add a z mirror modifier"""
    bl_idname = "view3d.fullmirrorz"
    bl_label = "Mirror Z"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_x = False
        bpy.context.object.modifiers["Mirror"].use_z = True        
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}    




class FullShrink(bpy.types.Operator):
    """Add a shrink modifier with first assigned vertex group"""
    bl_idname = "view3d.fullshrink"
    bl_label = "Shrinkwrap"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.ops.object.vertex_group_add()
        bpy.ops.object.vertex_group_assign()
        bpy.context.object.modifiers["Shrinkwrap"].vertex_group = "Group"
        bpy.ops.view3d.display_modifiers_cage_on()


        return {'FINISHED'}  

class HalfShrink(bpy.types.Operator):
    """Add a shrink modifier with cage on"""
    bl_idname = "view3d.halfshrink"
    bl_label = "Shrinkwrap"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.ops.view3d.display_modifiers_cage_on()


        return {'FINISHED'}  


    

class SINGLEVERTEX(bpy.types.Operator):
    """Add a single Vertex in Editmode"""
    bl_idname = "mesh.singlevertex"
    bl_label = "Single Vertex"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')    

    def execute(self, context):

        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')


        return {'FINISHED'} 


class deleteMat(bpy.types.Operator):
    """repeat last with value slider"""
    bl_idname = "material.remove"
    bl_label = "Delete all Material"
    bl_options = {'REGISTER', 'UNDO'}


    deleteMat = bpy.props.IntProperty(name="Delete all Material", description="How many times?", default=100, min=1, soft_max=1000, step=1)
    
    def execute(self, context):
        
        for i in range(self.deleteMat):
          
            bpy.ops.object.material_slot_remove()


        return {'FINISHED'}



class repeatlast(bpy.types.Operator):
    """repeat last with value slider"""
    bl_idname = "screen.repeat_last_new"
    bl_label = "Delete all Material"
    #bl_options = {'REGISTER', 'UNDO'}


    repeat = bpy.props.IntProperty(name="Repeat last step", description="How many times?", default=2, min=1, soft_max=1000, step=1)
    
    def execute(self, context):
        
        for i in range(self.repeat):
          
            bpy.ops.screen.repeat_last()


        return {'FINISHED'}  




class VertDelete(bpy.types.Operator):
 
    bl_idname = 'mesh.vertdelete'
    bl_label = bl_info['name']
    bl_options = {'REGISTER', 'UNDO'}
 
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj != None and obj.type == 'MESH' and obj.mode == 'EDIT'
 
    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (True, False,False)
        bpy.ops.view3d.snap_cursor_to_active()
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.context.space_data.transform_orientation = 'GLOBAL'

        bpy.ops.mesh.select_linked(limit=False)
        bpy.ops.mesh.delete(type='VERT')

        return {'FINISHED'}




class BevelX(bpy.types.Operator):

    bl_idname = 'mesh.intersectall'
    bl_label = "Bevel X"
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj != None and obj.type == 'MESH' and obj.mode == 'EDIT'

    def execute(self, context):
        # must force edge selection mode here
        
        
        bpy.context.scene.tool_settings.use_mesh_automerge = False
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1})
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        bpy.ops.transform.resize(value=(50, 50, 50), constraint_axis=(False, False, False), constraint_orientation='NORMAL')        
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
          
        return {'FINISHED'}


########################
######  oscurart  ######
######  oscurart  ######
########################
###http://oscurart.blogspot.com.ar/2013/12/blender-script-generador-id-color-mask.html###

class idgenerator(bpy.types.Operator):
    """add a id colorramp node to node editor"""
    bl_idname = "node.idgenerator"
    bl_label = "ID Color Node Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.view3d.assign_material()
        bpy.context.object.active_material.use_nodes = True

        ACTOBJ=bpy.context.active_object
        ACTMAT=ACTOBJ.material_slots[bpy.context.object.active_material_index].material
        NODE=ACTMAT.node_tree.nodes.new(type='ShaderNodeValToRGB')
    
        COLORS=30
        CHUNK=1/COLORS
        I=0
    

        for ELEMENT in range(COLORS):
            NODE.color_ramp.interpolation="CONSTANT"
            ELEMENTO=NODE.color_ramp.elements.new(I)    
            ELEMENTO.color=(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),1)
            I+=CHUNK        


        return {'FINISHED'}
    
#def register():
#    bpy.utils.register_class(idgenerator)


#def unregister():
#    bpy.utils.unregister_class(idgenerator)
    
        
#######---------------------##################################################################################################################
#######---------------------##################################################################################################################    
#######  Extension Buttons  ##################################################################################################################
#######  Extension Buttons  ##################################################################################################################
#######---------------------##################################################################################################################
#######---------------------##################################################################################################################  



#######################################################
###-----------------  ADD  -------------------------###
###-----------------  ADD  -------------------------###
#######################################################


### POLLS 

class OscPollXTRAS():
    """xtras tools"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_xtras


class OscPanelXTRAS(OscPollXTRAS, bpy.types.Panel):
    """xtras tools"""
    bl_idname = """xtras_tools"""
    bl_label = """XtraTools"""


    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager
        active_obj = context.active_object
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="add to scene")
        
        
        row = col.row(align=True)
        row.operator("object.trilighting", text="Add Tri-Lighting", icon ="LAMP_DATA")    
        row = col.row(align=True)
        row.operator("set.tmpcamera", text="Box+Camera", icon="FACESEL_HLT")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("object.bounding_boxers",text="Boundingbox", icon="OBJECT_DATA")         
        
        row = col.row(align=True)
        row.operator("view3d.fullcurve", "Full Bevel Curve", icon="OUTLINER_OB_CURVE")
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("object.name_objects",icon="OUTLINER_OB_FONT")

        row = col.row(align=True)
        row.operator("object.vertices_numbers3d",icon="SPACE2")        

        
        col = layout.column(align=True)
        col = layout.column(align=True)
        row = col.row(align=True)

        if context.selected_objects:
            if context.selected_objects[0].type == 'CURVE':
                row = layout.row()
                row.operator("object.curv_to_3d",text="Curve 3d", icon="CURVE_DATA")
                row.operator("object.curv_to_2d",text="Curve 2d",icon="CURVE_DATA")


        
        if context.selected_objects:
            if context.selected_objects[0].type == 'MESH':
                row = layout.row()
                row.operator("object.connect2objects",text ="connect 2 Obj with lines",icon="MESH_DATA")
                row = layout.row()
                row.prop(bpy.context.scene, "shift_verts", text="shift")
                #row.label(text="max " + str(maxim))
                row = layout.row()
                row.prop(bpy.context.scene, "hook_or_not", text="hook new vertices?")

              


        
###--------------------------------------------------------------------
        
        
        col = layout.column(align=True)
        col = layout.column(align=True)
        split = layout.split()

        row = col.row(align=True)
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

        sub = row.row()
        sub.scale_x = 2.0 
        sub.operator("ed.undo_history", text="History")

        
        return {'FINISHED'}        
        



############################################################
###--------------  CAD TOOLS  ---------------------------###       
###--------------  CAD TOOLS  ---------------------------###  
############################################################

### POLLS 

class OscPollCAD():
    """CAD Tools for Edit Mode"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_cad




class LayoutSSPanel(OscPollCAD, bpy.types.Panel):
    def axe_select(self, context):
        axes = ['X','Y','Z']
        return [tuple(3 * [axe]) for axe in axes]
    
    def project_select(self, context):
        projects = ['XY','XZ','YZ','XYZ']
        return [tuple(3 * [proj]) for proj in projects]
    
    bl_label = "CAD Tools"
    bl_idname = "Paul_Operator"
    
    bpy.types.Scene.AxesProperty = bpy.props.EnumProperty(items=axe_select)
    bpy.types.Scene.ProjectsProperty = bpy.props.EnumProperty(items=project_select)
    


    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager
        
        layout = self.layout
   
        col = layout.column(align=True)
        row = col.row(align=True)
        
        row.operator("object.bounding_boxers",text="Box", icon="OBJECT_DATA")
        row.operator("view3d.fullcurve", "Curve", icon="OUTLINER_OB_CURVE")

        col = layout.column(align=True)
        row = col.row(align=True)

        sub = row.row()
        sub.scale_x = 0.2
        sub.operator("mesh.vertex_align",text="A", icon="ALIGN")
        sub.operator("mesh.vertex_distribute",text="D", icon="PARTICLE_POINT")
        sub.operator("mesh.vertices_smooth", text="S", icon ="SPHERECURVE")                         
        sub.operator("mesh.singlevertex",text="V", icon="LAYER_ACTIVE")
          
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("bpt.boolean_2d_union", text= "Union 2d Faces", icon="LOCKVIEW_ON")
        row = col.row(align=True)
        row.operator("mesh.intersect_meshes",text="Object Intersection Line", icon="GROUP")  
                    
        
        col = layout.column(align=True)

#        split = col.split(percentage=0.15)
        
#        if lt.display_alignvert:
#            split.prop(lt, "display_alignvert", text="...CadTools...", icon='DOWNARROW_HLT')
#        else:
#            split.prop(lt, "display_alignvert", text="...CadTools...", icon='RIGHTARROW')

#        split.operator("mesh.intersect_meshes",text="Intersection Line")        

               
#        if lt.display_alignvert:
#            box = col.column(align=True).box().column()
#            col_top = box.column(align=True)
#            row = col_top.row(align=True)                

            

###--------------------------------------------------------------------
        

        split = col.split(percentage=0.15)
        
        if lt.display_cad:
            split.prop(lt, "display_cad", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_cad", text="", icon='RIGHTARROW')

        split.operator("bpt.smart_vtx",text="XVT Edges")       

               
        if lt.display_cad:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("mesh.intersectall", text="Bevel X ")
            row.operator("mesh.vertdelete", text="X Delete")              
            
            
            col_top = box.column(align=True)
            

            row = col_top.row(align=True)
            row.operator(LengthChange.bl_idname, "Edge Length")

              
            row = col_top.row(align=True)          
            row.operator("mesh.offset_edges",text="Offset Edges") 


            row = col_top.row(align=True)          
            row.operator("mesh.intersect_meshes",text="Mesh Intersection")                




###--------------------------------------------------------------------
       

        split = col.split(percentage=0.15)
        
        if lt.display_rotface:
            split.prop(lt, "display_rotface", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_rotface", text="", icon='RIGHTARROW')
            
        split.operator("mesh.rot_con", "Rotate Face") 
        
        
        if lt.display_rotface:
           box = col.column(align=True).box().column()
           col_top = box.column(align=True)
            
           row = col_top.row(align=True)
           row.operator("mesh.face_rotate_xz45", "Xz 45°")
           row.operator("mesh.face_rotate_yz45", "Yz 45°")
           row.operator("mesh.face_rotate_zx45", "Zx 45°")
            
           row = col_top.row(align=True)
           row.operator("mesh.face_rotate_xy45", "Xy 45°")
           row.operator("mesh.face_rotate_yx45", "Yx 45°")            
           row.operator("mesh.face_rotate_zy45", "Zy 45°")



###--------------------------------------------------------------------
      


#            col_top = box.column(align=True)
#            split = col.split(percentage=0.15)
        
#            if lt.display_merge:
#                split.prop(lt, "display_merge", text="", icon='DOWNARROW_HLT')
#            else:
#                split.prop(lt, "display_merge", text="", icon='RIGHTARROW')

#            split.operator("bpt.boolean_2d_union", text= "Union 2d Face")

            
#            if lt.display_merge:
#                box = col.column(align=True).box().column()
#                col_top = box.column(align=True)
            


###--------------------------------------------------------------------

      

#            col_top = box.column(align=True)
#            split = col.split(percentage=0.15)
       
#            if lt.display:
#                split.prop(lt, "display", text="", icon='DOWNARROW_HLT')
#            else:
#                split.prop(lt, "display", text="", icon='RIGHTARROW')

#            spread_op = split.operator("mesh.spread_operator", text = 'Spread Loop')

#            if lt.display:
#                box = col.column(align=True).box().column()
#                col_top = box.column(align=True)
#                row = col_top.row(align=True)



###--------------------------------------------------------------------
       

        split = col.split()#percentage=0.15)
        
        if lt.display_extrude:
            split.prop(lt, "display_extrude", text="-- Extrude --", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_extrude", text="-- Extrude --", icon='RIGHTARROW')

       #split.operator("mesh.intersect_meshes",text="Intersection Line")        

               
        if lt.display_extrude:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator('object.mextrude', text="Multi Extrude")
            
            row = col_top.row(align=True) 
            row.operator("faceinfillet.op0_id",  text="Face Inset Fillet")
            
            row = col_top.row(align=True) 
            row.operator("f.op0_id",  text="Edge Fillet")
         
            row = col_top.row(align=True) 
            row.operator("mesh.extrude_along_curve", text="Extrude Along Curve")
            
                
            row = col_top.row(align=True)
            row.operator("mechappo.select", text="Mechappo_Random Select")
            row = col_top.row(align=True)
            row.operator("mechappo.create", text="Mechappo_Extrude")   



###--------------------------------------------------------------------              

            
        
        split = col.split()
        if lt.display_align:
            split.prop(lt, "display_align", text="-- Align Edges --", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_align", text="-- Align Edges --", icon='RIGHTARROW')
            
        
        if lt.display_align and context.mode == 'EDIT_MESH':
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
            row = col_top.row(align=True)
            align_op = row.operator("mesh.align_operator", text = 'Align').type_op = 0
            row = col_top.row(align=True)
            row.prop(lt, 'align_dist_z', text = 'Superpose')
            row = col_top.row(align=True)
            row.prop(lt, 'align_lock_z', text = 'lock Z')
            
        if lt.display_align and context.mode == 'OBJECT':
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
            row = col_top.row(align=True)
            align_op = row.operator("mesh.align_operator", text = 'Align').type_op = 2
            row = col_top.row(align=True)
            row.prop(context.scene,'AxesProperty', text = 'Axis')
            row = col_top.row(align=True)
            row.prop(context.scene,'ProjectsProperty', text = 'Projection')

            
      
###-------------------------------------------------------------------- 


            
        
        split = col.split()
        if lt.display_offset:
            split.prop(lt, "display_offset", text="-- SideShift --", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_offset", text="-- SideShift --", icon='RIGHTARROW')
        
        if lt.display_offset:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            
            row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
            row = col_top.row(align=True)
            row.operator("mesh.offset_operator", text = 'Active » Cursor').type_op = 3
            
            row = col_top.row(align=True)
            lockX_op = row.prop(lt,"shift_lockX", text="X", icon='FREEZE')
            lockY_op = row.prop(lt,"shift_lockY", text="Y", icon='FREEZE')
            lockZ_op = row.prop(lt,"shift_lockZ", text="Z", icon='FREEZE')
            row = col_top.row(align=True)
            row.prop(lt,"shift_local", text="Local")
            
            row = col_top.row(align=True)
            split = col_top.split(percentage=0.76)
            split.prop(lt,'step_len', text = 'dist')
            getlenght_op = split.operator("mesh.offset_operator", text="Get dist").type_op = 1
            row = col_top.row(align=True)
            split = col_top.split(percentage=0.5)
            left_op = split.operator("mesh.offset_operator", text="", icon='TRIA_LEFT')
            left_op.type_op = 0
            left_op.sign_op = -1
            right_op = split.operator("mesh.offset_operator", text="", icon='TRIA_RIGHT')
            right_op.type_op = 0
            right_op.sign_op = 1
            row = col_top.row(align=True)
            
            if context.mode == 'EDIT_MESH':
                row.prop(lt,"shift_copy", text="Copy")
            else:
                row.prop(lt, "instance", text='Instance')
                row = col_top.row(align=True)
                row.prop(lt,"shift_copy", text="Copy")
                    
                    

###--------------------------------------------------------------------
    
        
        col = layout.column(align=True)        
        col = layout.column(align=True)
        split = layout.split()

        row = col.row(align=True)
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

        sub = row.row()
        sub.scale_x = 2.0 
        sub.operator("ed.undo_history", text="History")
        sub.operator("screen.repeat_last", text="Repeat")
                   
        


############################################################################
###------------------  Modifier  ----------------------------------------###
###------------------  Modifier  ----------------------------------------###
############################################################################



### POLLS 

class OscPollMOD():
    """MODIFIER TOOLS"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_modi


class OscPanelMOD(OscPollMOD, bpy.types.Panel):
    def axe_select(self, context):
        axes = ['X','Y','Z']
        return [tuple(3 * [axe]) for axe in axes]
    
    def project_select(self, context):
        projects = ['XY','XZ','YZ','XYZ']
        return [tuple(3 * [proj]) for proj in projects]
    

    
    bl_label = "Modifier Tools"
    bl_idname = "Modi_Operator"

    
    bpy.types.Scene.AxesProperty = bpy.props.EnumProperty(items=axe_select)
    bpy.types.Scene.ProjectsProperty = bpy.props.EnumProperty(items=project_select)
    

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager
        
        layout = self.layout

        col = layout.column(align=True)

        row = col.row(align=True)
        row.operator_menu_enum("object.modifier_add", "type", text="--- Modifier to Object ---", icon="MODIFIER")        



###--------------------------------------------------------


        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_tempmodi:
            split.prop(lt, "display_tempmodi", text="Modi Custom", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_tempmodi", text="Modi Custom", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.shade_smooth", text="Visual", icon="MESH_CUBE")
            
        
        if lt.display_tempmodi:
            box = col.column(align=True).box().column()
			
            col_top = box.column(align=True)
            row = col_top.row(align=True)
           
            row = col_top.row(align=True)
            row.operator("object.modifier_add",icon='MOD_ARRAY',text=" Array").type="ARRAY"
            row.operator("object.modifier_add",icon='MOD_SIMPLEDEFORM',text=" Deform").type="SIMPLE_DEFORM"
        
            row = col_top.row(align=True)
            row.operator("object.modifier_add",icon='MOD_BUILD',text=" Build").type="BUILD"
            row.operator("object.modifier_add",icon='MOD_ARMATURE',text=" Armature").type="ARMATURE"
        
            row = col_top.row(align=True)
            row.operator("view3d.fullmirror",icon='MOD_MIRROR',text="Mirror")
            row.operator("object.modifier_add",icon='MOD_SHRINKWRAP',text="Shrinkwrap").type="SHRINKWRAP"
            
            row = col_top.row(align=True)            
            row.operator("mesh.primitive_symmetrical_empty_add",text="Symmetrical Empty",icon="OUTLINER_OB_EMPTY") 



###--------------------------------------------------------
        
                 

        #col = layout.column(align=True)   
        split = col.split()#percentage=0.15)
        
        if lt.display_modi:
            split.prop(lt, "display_modi", text="Subdivision Level", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_modi", text="Subdivision Level", icon='RIGHTARROW')

        #spread_op = split.operator("object.modifier_add", text="Subdivision Level", icon = 'MOD_SUBSURF').type="SUBSURF"

            
        if lt.display_modi:
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)


            #row.label("Levels")
        
            row = col_top.row(align=True)
            row.operator("view3d.modifiers_subsurf_level_0")
            row.operator("view3d.modifiers_subsurf_level_1")
            row.operator("view3d.modifiers_subsurf_level_2")
            row.operator("view3d.modifiers_subsurf_level_3")
            row.operator("view3d.modifiers_subsurf_level_4")
            row.operator("view3d.modifiers_subsurf_level_5")
            row.operator("view3d.modifiers_subsurf_level_6")
            




###--------------------------------------------------------



        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_shade:
            split.prop(lt, "display_shade", text="Visual", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_shade", text="Visual", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.shade_smooth", text="Visual", icon="MESH_CUBE")
            
        
        if lt.display_shade:
            box = col.column(align=True).box().column()
			
            col_top = box.column(align=True)
            row = col_top.row(align=True)

            col_top = box.column(align=True)
            
            col.alignment = 'EXPAND'

            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_viewport_on",icon = 'RESTRICT_VIEW_OFF')
            row.operator("view3d.display_modifiers_edit_on", icon = 'EDITMODE_HLT')
            row.operator("view3d.display_modifiers_cage_on",icon = 'OUTLINER_OB_MESH')
            row.operator("view3d.display_wire_on", "On", icon = 'WIRE')

           
            col.alignment = 'EXPAND'


            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_viewport_off",icon = 'VISIBLE_IPO_OFF')         
            row.operator("view3d.display_modifiers_edit_off",icon = 'SNAP_VERTEX')  
            row.operator("view3d.display_modifiers_cage_off",icon = 'OUTLINER_DATA_MESH')
            row.operator("view3d.display_wire_off", "Off", icon = 'SOLID')

        
            col_top = box.column(align=True)
      
            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_apply", icon = 'FILE_TICK')
            row.operator("view3d.display_modifiers_delete", icon = 'X')

            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_expand", icon = 'TRIA_DOWN')
            row.operator("view3d.display_modifiers_collapse", icon = 'TRIA_RIGHT')             
            


###--------------------------------------------------------
            

            
        #col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_mirrorcut:
            split.prop(lt, "display_mirrorcut", text="Mirror", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_mirrorcut", text="Mirror", icon='RIGHTARROW')
            
        #spread_op = split.operator("object.modifier_add", text="Mirrorcut", icon="MOD_MIRROR").type="MIRROR"
            
        
        if lt.display_mirrorcut:
            box = col.column(align=True).box().column()
			


            col_top = box.column(align=True)
            row = col_top.row(align=True)            
            row.operator("mesh.primitive_symmetrical_empty_add",text="Symmetrical Empty",icon="OUTLINER_OB_EMPTY") 


            col_top = box.column(align=True)
            row = col_top.row(align=True)


            row.label(text="half cut geometry",icon="MOD_MIRROR")       
            
            
            row = col_top.row(align=True)
            row.operator("add.mmx", text="X")
            row.operator("add.mmy", text="Y")    
            row.operator("add.mmz", text="Z")

            col = layout.column(align=True)             
        
            row = col_top.row(align=True)
            row.operator("add.mmmx", text="-X")
            row.operator("add.mmmy", text="-Y")     
            row.operator("add.mmmz", text="-Z")
            
            
                    
        ###----------------------------
        
        col = layout.column(align=True)        
        
        col = layout.column(align=True)
        split = layout.split()

        row = col.row(align=True)
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

        sub = row.row()
        sub.scale_x = 2.0 
        sub.operator("ed.undo_history", text="History")
        sub.operator("screen.repeat_last", text="Repeat") 
        
        
        
################################################################
###-------------------  FLY  --------------------------------###
###-------------------  FLY  --------------------------------###
################################################################



### POLLS 

class OscPollFLY():
    """open Array Tools for Object Mode"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_fly




### PANELES

class OscPanelFLY(OscPollFLY, bpy.types.Panel):
    """Fly Mode Tools"""
    bl_idname = "Fly Mode Tools"
    bl_label = "Fly Mode Tools"

    def draw(self, context):
        active_obj = context.active_object
        layout = self.layout
        
        col = layout.column(align=True)
        
        scene = context.scene
        row = layout.row(align=True)
        
        row.alignment = 'LEFT'
        row.operator("view3d.fast_navigate_operator")
        row.operator("view3d.fast_navigate_stop")
        layout.label("Settings :")
        
        row = layout.row()
        box = row.box()
        box.prop(scene,"OriginalMode")
        box.prop(scene,"FastMode")
        box.prop(scene, "EditActive", "Edit mode")
        box.prop(scene, "Delay")
        box.prop(scene, "DelayTimeGlobal", "Delay time")
        box.alignment = 'LEFT'
        box.prop(scene,"ShowParticles")
        box.prop(scene,"ParticlesPercentageDisplay")
        



#########################################################
###----------------  VISUAL  -------------------------###
###----------------  VISUAL  -------------------------###
#########################################################




### POLLS 

class OscPollVISUAL():
    """open Array Tools for Object Mode"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_visual




### PANELES

class OscPanelVISUAL(OscPollVISUAL, bpy.types.Panel):
    """Visual Tools"""
    bl_idname = "Visual Tools"
    bl_label = "Visual Tools"

    def draw(self, context):
        active_obj = context.active_object
        layout = self.layout
        
        col = layout.column(align=True)
        
        row = col.row(align=True)  
        row.operator("view3d.display_wire_on", "Wire On", icon = 'WIRE')
        row.operator("view3d.display_wire_off", "Wire Off", icon = 'SOLID')          
                        
        row = col.row(align=True)      
        row.operator("view3d.display_shadeless_on", "Shadeless On", icon = 'SMOOTH')
        row.operator("view3d.display_shadeless_off", "Shadeless Off", icon = 'SOLID')
        
            
        row = col.row(align=True)       
        row.operator("view3d.display_bounds_on", "Bounds On", icon = 'ROTATE')
        row.operator("view3d.display_bounds_off", "Bounds Off", icon = 'BBOX')
            
        
        row = col.row(align=True)  
        row.operator("view3d.display_double_sided_on","DSided On", icon = 'OUTLINER_OB_MESH')
        row.operator("view3d.display_double_sided_off","DSided Off", icon = 'MESH_DATA')
        
        row = col.row(align=True)     
        row.operator("view3d.display_x_ray_on","XRay On", icon = 'GHOST_ENABLED')
        row.operator("view3d.display_x_ray_off", "XRay Off", icon = 'GHOST_DISABLED')
            
        row = col.row(align=True)  
        row.separator()
            
        row = col.row(align=True)  
        scene = context.scene
        row.prop(scene, "BoundingMode") 
        
   



#########################################################        	
###-----------------  ARRAYS  ------------------------###
###-----------------  ARRAYS  ------------------------###
#########################################################


### POLLS 

class OscPollArray():
    """open ArrayTools for Object Mode"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_array




### PANELES

class OscPanelArray(OscPollArray, bpy.types.Panel):
    """Array Tools for Object Mode"""
    bl_idname = "arraytools"
    bl_label = "ArrayTools"

    def draw(self, context):
        lt = bpy.context.window_manager.paul_manager
        active_obj = context.active_object
        layout = self.layout
        


        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_grid:
            split.prop(lt, "display_grid", text="...AREWO...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_grid", text="...ARRAY...", icon='RIGHTARROW')
            
        #spread_op = split.prop(bpy.context.scene, "osc_object_arewo", text="Arewo", icon="MOD_ARRAY")
            
        
        if lt.display_grid:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.prop(bpy.context.scene, "osc_object_arewo", text="Arewo", icon="MOD_ARRAY")

            row = col_top.row(align=True)    
            row.operator("object.arewo",text="Replicator")
            row.operator("object.cursor_array", text="2 Cursor")   

            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.operator("object.add_2array", text="2d Grid")
            row.operator("object.add_3array", text="3d Grid") 
  
         
                             

####--------------------------------------


        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_bezcurve:
            split.prop(lt, "display_bezcurve", text="...Curve...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_bezcurve", text="...Curve...", icon='RIGHTARROW')
            
        #spread_op = split.prop(bpy.context.scene, "osc_object_arewo", text="Arewo", icon="LAYER_ACTIVE")
            
        
        if lt.display_bezcurve:
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.operator("object.loops12", text="", icon="CURVE_BEZCURVE")
            row.operator("object.loops13", text="Beziér Curve",)
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)              
            row.operator("object.loops10", text="", icon="CURVE_BEZCIRCLE")
            row.operator("object.loops11", text="Beziér Circle",)                  

            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.operator("object.loops14", text="", icon="CURVE_BEZCIRCLE")
            row.operator("object.loops15", text="", icon="CONSTRAINT_DATA")          
            row.operator("object.fpath_array",text="Follow Path")
            row.operator("constraint.followpath_path_animate", text="", icon='ANIM_DATA')

       
            col_top = box.column(align=True)
            row = col_top.row(align=True)  
            row.operator("object.loops16",text="linked Obj")                  
            row.operator("object.loops17",text="single Obj")  
            


####--------------------------------------



        col = layout.column(align=True)
        split = col.split()#percentage=0.15)
        
        
        if lt.display_circle:
            split.prop(lt, "display_circle", text="...Empty Array...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_circle", text="...Empty...", icon='RIGHTARROW')
            
            #spread_op = split.operator("objects.circle_array_operator1", text="Empty Array", icon="OUTLINER_OB_EMPTY")
            
        
        if lt.display_circle:
            box = col.column(align=True).box().column()
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("objects.circle_array_operator1", text="1/4-90°", icon="MOD_ARRAY")
            row.operator("objects.circle_array_operator2", text="1/6-60°", icon="MOD_ARRAY")
            
            row = col_top.row(align=True)
            row.operator("objects.circle_array_operator3", text="1/8-45°", icon="MOD_ARRAY")
            row.operator("objects.circle_array_operator4", text="1/12-30°", icon="MOD_ARRAY")

####--------------------------------------


        col = layout.column(align=True)
        split = col.split()#percentage=0.15)

        
        if lt.display_constraint:
            split.prop(lt, "display_constraint", text="...Constraint...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_constraint", text="...Constraint...", icon='RIGHTARROW')
            
        #spread_op = split.operator_menu_enum("object.constraint_add", "type", text="Constraint", icon="CONSTRAINT_DATA") 
            
        
        if lt.display_constraint:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator_menu_enum("object.constraint_add", "type", text=" > add Constraint", icon="CONSTRAINT_DATA") 
            
            col_top = box.column(align=True)
            row = col_top.row(align=True)           
            row.label(text="to Selected:",icon="LAYER_ACTIVE")
            
            row = col_top.row(align=True)
            row.operator("track.to", text="Track To")
            row.operator("damped.track", text="Damped Track")
            row.operator("lock.track", text="Lock Track")

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.label(text="to CursorPos+Empty:",icon="LAYER_ACTIVE")

            row = col_top.row(align=True)
            row.operator("track.toempty", text="Track To")
            row.operator("damped.trackempty", text="Damped Track")
            row.operator("lock.trackempty", text="Lock Track")
            
            #col_top = box.column(align=True)
            #row = col_top.row(align=True)
            #row.operator("object.track_set",text=">>>  Track  <<<")



####--------------------------------------


        col = layout.column(align=True)
        split = col.split()#percentage=0.15)

        
        if lt.display_group:
            split.prop(lt, "display_group", text="...Group...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_group", text="...Group...", icon='RIGHTARROW')
            
        #spread_op = split.operator_menu_enum("object.constraint_add", "type", text="Constraint", icon="CONSTRAINT_DATA") 
            
        
        if lt.display_group:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("group.create", text="Group")
            row.operator("group.objects_add_active", text="-> to Active")
            
            row = col_top.row(align=True)
            row.operator("group.objects_remove", text="Remove")
            row.operator("group.objects_remove_active", text="-> from Active")             



###-----------------------------------------------------------------------------


        col = layout.column(align=True)
        split = col.split()#percentage=0.15)

        
        if lt.display_relations:
            split.prop(lt, "display_relations", text="...Relations...", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_relations", text="...Relations...", icon='RIGHTARROW')
            
        #spread_op = split.operator_menu_enum("object.constraint_add", "type", text="Constraint", icon="CONSTRAINT_DATA") 
            
        
        if lt.display_relations:
            box = col.column(align=True).box().column()

            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.set_instance",text=">>>  Set as Instance  <<<")	            

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("object.parent_set", text="Set Parent")
            row.operator("object.parent_clear", text="Clear Parent")
        
            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_make_links", text="Links")
            row.menu("VIEW3D_MT_make_single_user", text="Single User")

            col_top = box.column(align=True)
            
            row = col_top.row(align=True)
            row.operator("object.visual_transform_apply")
            row = col_top.row(align=True)
            row.operator("object.duplicates_make_real", icon="MOD_PARTICLES")
      
        
        
        
        ###---------


        col = layout.column(align=True)
        col = layout.column(align=True)
        split = layout.split()

        row = col.row(align=True)
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

        sub = row.row()
        sub.scale_x = 2.0 
        sub.operator("ed.undo_history", text="History")
        sub.operator("screen.repeat_last", text="Repeat")                     




###########################################################
###----------------  MATERIAL  -------------------------###        
###----------------  MATERIAL  -------------------------###
###########################################################
  
  

### POLLS

class OscPollMATERIAL():
    """Material Tools"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_material
        


### PANELES

class OscPanelMATERIAL(OscPollMATERIAL, bpy.types.Panel):
    """Material Tools"""
    bl_idname = "materialtools"
    bl_label = "MaterialTools"
    bl_context = "mesh_edit"

    def draw(self, context):
        wm = context.window_manager
        scn = context.scene
        layout = self.layout

        

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("material.remove", text="Remove all Materials", icon="LOOP_BACK")        

        col = layout.column(align=True)
        row = layout.row()
        row.operator("object.materials_to_object",icon="MATERIAL_DATA")
        
        row = layout.row()
        row.operator("object.materials_to_data",icon="MATERIAL_DATA") 

        row = layout.row()
        row.operator("object.clean_images")
        row = layout.row()
        row.operator("object.clean_materials")
       
          



        ##------
       
        col = layout.column(align=True)
        col = layout.column(align=True)
        split = layout.split()

        row = col.row(align=True)
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 

        sub = row.row()
        sub.scale_x = 2.0 
        sub.operator("ed.undo_history", text="History")
        sub.operator("screen.repeat_last", text="Repeat")
        
        



#############################################################
###---------------  MANAGEMENT  --------------------------###
###---------------  MANAGEMENT  --------------------------###
#############################################################



### POLLS

class OscPollMANAGE():
    """Management Tools"""
    bl_category="META"
    #bl_region_type = 'UI'
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_manage
        


### PANELES

class OscPanelMANAGE(OscPollMANAGE, bpy.types.Panel):
    """Management"""
    bl_label = "Management"
    bl_idname = "_PT_rig_layers"


    def draw(self, context):
        layout = self.layout


        col = layout.column(align=True)

        pack_all = layout.row()
        pack_all.operator("file.pack_all")
        pack_all.active = not bpy.data.use_autopack

        unpack_all = layout.row()
        unpack_all.operator("file.unpack_all")
        unpack_all.active = not bpy.data.use_autopack
        
        icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
        layout.operator("file.autopack_toggle", text="autom. Pack into .blend",icon=icon)        

        col = layout.column(align=True)

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("file.make_paths_relative")
        row = col.row(align=True)
        row.operator("file.make_paths_absolute")

        col = layout.column(align=True)

        col = layout.column(align=True)
        row = col.row(align=True)        
        row.operator("file.report_missing_files")
        row = col.row(align=True)
        row.operator("file.find_missing_files")
        
        
        
        
       
########################################################        
###---------------  AREWO  --------------------------###        
###---------------  AREWO  --------------------------###  
########################################################
        
   

### POLLS

class OscPollarewo():
    """open Arewo Tools"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_arewo




### PANELES

class OscPanelArewo(OscPollarewo, bpy.types.Panel):
	"""Animation Offset""" 
	bl_idname = "arewo.replicate" # unique identifier for buttons and menu items to reference.
	bl_label = "Arewo" # display name in the interface.
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_context = "objectmode"

	bpy.types.Scene.placer_object = StringProperty(name="Placer Object")

	def draw(self, context):
		layout = self.layout
		split = layout.split()
		row = layout.row()
		col = split.column(align = True)
		col.operator("anim.arewo_simple", icon = "MOD_ARRAY")
		if len(bpy.context.selected_objects) > 0 and bpy.context.active_object != None:
			col.enabled = True
		else:
			col.enabled = False
		split = row.split()
		
		col = split.column(align = True)
		col.operator("anim.arewo_object_offset", icon = "PARTICLE_POINT")
		if (bpy.context.active_object == None or len(bpy.context.selected_objects) == 0 or bpy.context.scene.placer_object == ""):
			col.active = False
		else:
			col.active = True
		
		row2 = layout.row()
		split = row2.split()		
		col = split.column(align = True)
		col.operator("anim.arewo_armature_offset", icon = "ARMATURE_DATA")
		if (bpy.context.active_object == None or len(bpy.context.selected_objects) < 2 or bpy.context.scene.placer_object == "" or not 'ARMATURE' in (ob.type for ob in bpy.context.selected_objects)):
			col.active = False
		else:
			col.active = True
		# Helper tools
		layout.prop_search(
			context.scene,  # not sure
			"placer_object",	# Scene property
			bpy.context.scene, # where to search
			"objects",	  # category to search in
			"Placer:"		 # lable name
			)

		layout.label("Speed Up Tools")
		row = layout.row()
		split = row.split()
		col = split.column(align = True)
		col.operator("object.mute_modifiers", icon = 'VISIBLE_IPO_OFF')
		col.operator("object.enable_modifiers", icon = 'VISIBLE_IPO_ON')
		col.operator("object.apply_modifier_for_multi", icon = 'MOD_REMESH')




    
        
###----------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx----------###
###----------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx----------###
###----------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx----------###
###----------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx--------------------xxxxxxxxxxxxxxx----------###





####################################################################################################################################
####################################################################################################################################
#########  Simple Align  ###########################################################################################################
#########  Simple Align  ###########################################################################################################

# AlingTools.py (c) 2009, 2010 Gabriel Beaudin (gabhead)

#bl_info = {
 #   "name": "Simple Align",
  #  "author": "Gabriel Beaudin (gabhead)",
   # "version": (0,1),
    #"blender": (2, 61, 0),
    #"location": "View3D > Tool Shelf > Simple Align Panel",
    #"description": "Align Selected Objects to Active Object",
    #"warning": "",
    #"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"\
    #    "Scripts/3D interaction/Align_Tools",
    #"tracker_url": "https://projects.blender.org/tracker/index.php?"\
    #    "func=detail&aid=22389",
    #"category": "3D View"}

###############################################################################


"""Align Selected Objects"""
##Align all
def main(context):
    for i in bpy.context.selected_objects:
        i.location = bpy.context.active_object.location
        i.rotation_euler = bpy.context.active_object.rotation_euler

## Align Location

def LocAll(context):
    for i in bpy.context.selected_objects:
        i.location = bpy.context.active_object.location

def LocX(context):
    for i in bpy.context.selected_objects:
        i.location.x = bpy.context.active_object.location.x

def LocY(context):
    for i in bpy.context.selected_objects:
        i.location.y = bpy.context.active_object.location.y

def LocZ(context):
    for i in bpy.context.selected_objects:
        i.location.z = bpy.context.active_object.location.z

## Aling Rotation
def RotAll(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler = bpy.context.active_object.rotation_euler

def RotX(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler.x = bpy.context.active_object.rotation_euler.x

def RotY(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler.y = bpy.context.active_object.rotation_euler.y

def RotZ(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler.z = bpy.context.active_object.rotation_euler.z
## Aling Scale
def ScaleAll(context):
    for i in bpy.context.selected_objects:
        i.scale = bpy.context.active_object.scale

def ScaleX(context):
    for i in bpy.context.selected_objects:
        i.scale.x = bpy.context.active_object.scale.x

def ScaleY(context):
    for i in bpy.context.selected_objects:
        i.scale.y = bpy.context.active_object.scale.y

def ScaleZ(context):
    for i in bpy.context.selected_objects:
        i.scale.z = bpy.context.active_object.scale.z

## Classes

## Align All Rotation And Location
class AlignOperator(bpy.types.Operator):
    """Align All Rotation and Location from Selected to Active"""
    bl_idname = "object.align"
    bl_label = "Align Selected To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

#######################Align Location########################
## Align LocationAll
class AlignLocationOperator(bpy.types.Operator):
    """Align Selected Location To Active"""
    bl_idname = "object.align_location_all"
    bl_label = "Align Selected Location To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocAll(context)
        return {'FINISHED'}
    
## Align LocationX
class AlignLocationXOperator(bpy.types.Operator):
    """Align Selected Location X To Active"""
    bl_idname = "object.align_location_x"
    bl_label = "Align Selected Location X To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocX(context)
        return {'FINISHED'}
    
## Align LocationY
class AlignLocationYOperator(bpy.types.Operator):
    """Align Selected Location Y To Active"""
    bl_idname = "object.align_location_y"
    bl_label = "Align Selected Location Y To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocY(context)
        return {'FINISHED'}
    
## Align LocationZ
class AlignLocationZOperator(bpy.types.Operator):
    """Align Selected Location Z To Active"""
    bl_idname = "object.align_location_z"
    bl_label = "Align Selected Location Z To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocZ(context)
        return {'FINISHED'}

#######################Align Rotation########################
## Align RotationAll
class AlignRotationOperator(bpy.types.Operator):
    """Align Selected Rotation To Active"""
    bl_idname = "object.align_rotation_all"
    bl_label = "Align Selected Rotation To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotAll(context)
        return {'FINISHED'}
    
## Align RotationX
class AlignRotationXOperator(bpy.types.Operator):
    """Align Selected Rotation X To Active"""
    bl_idname = "object.align_rotation_x"
    bl_label = "Align Selected Rotation X To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotX(context)
        return {'FINISHED'}
    
## Align RotationY
class AlignRotationYOperator(bpy.types.Operator):
    """Align Selected Rotation Y To Active"""
    bl_idname = "object.align_rotation_y"
    bl_label = "Align Selected Rotation Y To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotY(context)
        return {'FINISHED'}
    
## Align RotationZ
class AlignRotationZOperator(bpy.types.Operator):
    """Align Selected Rotation Z To Active"""
    bl_idname = "object.align_rotation_z"
    bl_label = "Align Selected Rotation Z To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotZ(context)
        return {'FINISHED'}
   
#######################Align Scale########################

## Scale All
class AlignScaleOperator(bpy.types.Operator):
    """Align Selected Scale To Active"""
    bl_idname = "object.align_objects_scale_all"
    bl_label = "Align Selected Scale To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleAll(context)
        return {'FINISHED'}
    
## Align ScaleX
class AlignScaleXOperator(bpy.types.Operator):
    """Align Selected Scale X To Active"""
    bl_idname = "object.align_objects_scale_x"
    bl_label = "Align Selected Scale X To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleX(context)
        return {'FINISHED'}
    
## Align ScaleY
class AlignScaleYOperator(bpy.types.Operator):
    """Align Selected Scale Y To Active"""
    bl_idname = "object.align_objects_scale_y"
    bl_label = "Align Selected Scale Y To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleY(context)
        return {'FINISHED'}
    
## Align ScaleZ
class AlignScaleZOperator(bpy.types.Operator):
    """Align Selected Scale Z To Active"""
    bl_idname = "object.align_objects_scale_z"
    bl_label = "Align Selected Scale Z To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleZ(context)
        return {'FINISHED'}


   
################################################################################################################


def register():
    bpy.utils.register_class(addArray2)
    bpy.utils.register_class(addArray3)
    bpy.utils.register_class(Circle_ArrayA)
    bpy.utils.register_class(Circle_ArrayB)
    bpy.utils.register_class(Circle_ArrayC)
    bpy.utils.register_class(Circle_ArrayD)            
    
    
    bpy.utils.register_class(loop1)
    bpy.utils.register_class(loop2)
    bpy.utils.register_class(loop3)
    bpy.utils.register_class(loop4)
    bpy.utils.register_class(loop5)
    bpy.utils.register_class(loop6)
    bpy.utils.register_class(loop7)
    bpy.utils.register_class(loop8)
    
    bpy.utils.register_class(pivotCursor)
    bpy.utils.register_class(pivotMedian)
    bpy.utils.register_class(pivotCursor3d)
    bpy.utils.register_class(pivotCursor3d2)
    bpy.utils.register_class(pivotCursor3d3)
    
    
    bpy.utils.register_class(ARewO)
    bpy.utils.register_class(RotateConstrained)

    bpy.utils.register_module(__name__)
    pass

    
def unregister():
    bpy.utils.unregister_class(Circle_ArrayA)
    bpy.utils.unregister_class(Circle_ArrayB)
    bpy.utils.unregister_class(Circle_ArrayC)
    bpy.utils.unregister_class(Circle_ArrayD)       
    
    bpy.utils.unregister_class(loop1)
    bpy.utils.unregister_class(loop2)
    bpy.utils.unregister_class(loop3)
    bpy.utils.unregister_class(loop4)
    bpy.utils.unregister_class(loop5)
    bpy.utils.unregister_class(loop6)
    bpy.utils.unregister_class(loop7)
    bpy.utils.unregister_class(loop8)


    bpy.utils.unregister_class(addArray2)
    bpy.utils.unregister_class(addArray3)
    
    bpy.utils.unregister_class(pivotCursor)
    bpy.utils.unregister_class(pivotMedian)
    bpy.utils.unregister_class(pivotCursor3d)
    bpy.utils.unregister_class(pivotCursor3d2)
    bpy.utils.unregister_class(pivotCursor3d3)       
    
    bpy.utils.unregister_class(ARewO)
    bpy.utils.unregister_class(RotateConstrained)

    bpy.utils.unregister_module(__name__)
    pass        



#########################################################################################################################
#########################################################################################################################
#########  Worn Edges  ##################################################################################################
#########  Worn Edges  ##################################################################################################


#bl_info = {
#    "name": "Worn Edges",
#    "author": "Oscurart",
#    "version": (1, 2),
#    "blender": (2, 6, 8),
#    "location": "Vertex Paint > Paint > Worn Edges",
#    "description": "Create a Vertex Color map with Worn Edges",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Paint"}




def CreateWornEdges(context, factor):
    actobj = bpy.context.object

    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(actobj.data)

    sf = [(vert.calc_shell_factor() - 1.0) * factor for vert in bm.verts[:]]

    bpy.ops.object.mode_set(mode="VERTEX_PAINT")
    purge = {}

    for ind, loop in enumerate(bpy.context.object.data.loops[:]):
        if loop.vertex_index not in purge:
            purge[loop.vertex_index] = [ind]
        else:
            purge[loop.vertex_index].append(ind)

    for vert in actobj.data.vertices[:]:
        if vert.select:
            ran = (sf[vert.index], sf[vert.index], sf[vert.index])
            for i in purge[vert.index]:
                actobj.data.vertex_colors.active.data[i].color = ran
    actobj.data.update()


class OscurartWorn(bpy.types.Operator):
    """create a vertex color map with worn edges"""
    bl_idname = "paint.worn_edges"
    bl_label = "Worn Edges Map"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    factor = bpy.props.FloatProperty(name="Factor", min=.001, default=1)

    def execute(self, context):
        CreateWornEdges(context, self.factor)
        return {'FINISHED'}


def add_osc_futurism_button(self, context):
    self.layout.operator(
        OscurartWorn.bl_idname,
        text="Worn Edges",
        icon="PLUGIN")


#--Registry-----------------------------------------------------------------------------


def register():
    bpy.utils.register_class(vertexpaint)
    bpy.utils.register_class(OscurartWorn)
    bpy.types.VIEW3D_MT_paint_vertex.append(add_osc_futurism_button)


def unregister():
    bpy.utils.unregister_class(vertexpaint)
    bpy.utils.unregister_class(OscurartWorn)
    bpy.types.VIEW3D_MT_paint_vertex.remove(add_osc_futurism_button)
    
    


###############################################################################################################################
###############################################################################################################################
##########  Vismaya  ##########################################################################################################
##########  Vismaya  ##########################################################################################################


#bl_info = {
#    'name' : 'Vismaya Tools-v1.1',
#    'author' : 'Project Vismaya',
#    'version' : (0, 1),
#    'blender' : (2, 56, 2),
#    'location' : 'View3D > Toolbar',
#    'description' : 'Vismaya Tools v1.1',
#    'category' : '3D View'}

################ Production Folder #################
class Set_Production_Folder(bpy.types.Operator, ExportHelper):
    '''Save selected objects to a chosen format'''
    bl_idname = "production_scene.selected"
    bl_label = "Set Production"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = bpy.props.StringProperty(
        default="",
        options={'HIDDEN'},
        )

    def invoke(self, context, event):
        self.filename_ext = ".blend" 
        self.filepath = pfopath + "/prod/scenes/untitled"
        return ExportHelper.invoke(self, context, event)
    
    def execute(self, context):        
        bpy.ops.wm.save_mainfile(
            filepath=self.filepath,
        )
        return {'FINISHED'}

class Production_Folder(bpy.types.Operator, ExportHelper):
    """Open the Production Folder in a file Browser"""
    bl_idname = "productionfolder_scene.selected"
    bl_label = "Create Production"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = bpy.props.StringProperty(  #--- If we hides this, both 2menu works but 2nd shows only run time error after creating folder.
        default="",
        options={'HIDDEN'},
        )
    
    filter_glob = bpy.props.StringProperty(
        default="",
        options={'HIDDEN'},
        )

    def invoke(self, context, event):
        self.filepath = "Production Folder"
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        try : 
            global pfopath
            pfopath = self.filepath
            folder_path = self.filepath
            path = folder_path + '/preprod'
            if not os.path.exists(path): os.makedirs(path)
            path = folder_path + '/prod'
            if not os.path.exists(path): os.makedirs(path)
            path = folder_path + '/ref'
            if not os.path.exists(path): os.makedirs(path)
            path = folder_path + '/resources'
            if not os.path.exists(path): os.makedirs(path)
            path = folder_path + '/wip'
            if not os.path.exists(path): os.makedirs(path)
            path1 = folder_path + '/prod/scenes'
            if not os.path.exists(path1): os.makedirs(path1)
            path1 = folder_path + '/prod/sets'
            if not os.path.exists(path1): os.makedirs(path1)
            path1 = folder_path + '/prod/props/textures'
            if not os.path.exists(path1): os.makedirs(path1)
            path1 = folder_path + '/prod/chars/textures'
            if not os.path.exists(path1): os.makedirs(path1)
            path1 = folder_path + '/prod/envs/textures'
            if not os.path.exists(path1): os.makedirs(path1)
            path1 = folder_path + '/prod/mattes/textures'
            if not os.path.exists(path1): os.makedirs(path1)
            self.report({'INFO'}, "Production folder created.")
        except ValueError:
            self.report({'INFO'}, "No Production folder created yet")
            return {'FINISHED'}
        return {'FINISHED'}

class Show_Production_Folder(bpy.types.Operator):
    bl_idname = "file.production_folder"
    bl_label = "Show Project"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try :
            bpy.ops.wm.path_open(filepath=pfopath) 
        except ValueError:
            self.report({'INFO'}, "No project folder yet")
            return {'FINISHED'}       
        return {'FINISHED'}





########### Freeze Transformation ###########
class Set_Freezetransform(bpy.types.Operator):
    """set transform values to zero"""
    bl_idname = "freeze_transform.selected"
    bl_label = "Freeze Transform"	
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):       
   
        str = context.active_object.type       
        if str.startswith('EMPTY') or str.startswith('SPEAKER') or str.startswith('CAMERA')or str.startswith('LAMP')or str.startswith('FONT'):                 
            #Location
            context.active_object.delta_location+=context.active_object.location
            context.active_object.location=[0,0,0]       
            
            #Rotation
            
            rotX=bpy.context.active_object.rotation_euler.x
            rotDeltaX=bpy.context.active_object.delta_rotation_euler.x
            bpy.context.active_object.delta_rotation_euler.x=rotX+rotDeltaX    
                
            rotY=bpy.context.active_object.rotation_euler.y
            rotDeltaY=bpy.context.active_object.delta_rotation_euler.y
            bpy.context.active_object.delta_rotation_euler.y=rotDeltaY+rotY           
         
            rotZ= bpy.context.active_object.rotation_euler.z
            rotDeltaZ=bpy.context.active_object.delta_rotation_euler.z
            bpy.context.active_object.delta_rotation_euler.z= rotDeltaZ+rotZ  
                        
            rquatW = context.active_object.rotation_quaternion.w
            rquatX = context.active_object.rotation_quaternion.x
            rquatY = context.active_object.rotation_quaternion.y
            rquatZ = context.active_object.rotation_quaternion.z
            
            drquatW = context.active_object.delta_rotation_quaternion.w
            drquatX = context.active_object.delta_rotation_quaternion.x
            drquatY = context.active_object.delta_rotation_quaternion.y
            drquatZ = context.active_object.delta_rotation_quaternion.z
            
            context.active_object.delta_rotation_quaternion.w = 1.0
            context.active_object.delta_rotation_quaternion.x = rquatX + drquatX
            context.active_object.delta_rotation_quaternion.y = rquatY + drquatY
            context.active_object.delta_rotation_quaternion.z = rquatZ + drquatZ
            
            context.active_object.rotation_quaternion.w = 1.0
            context.active_object.rotation_quaternion.x = 0.0
            context.active_object.rotation_quaternion.y = 0.0
            context.active_object.rotation_quaternion.z = 0.0
            
            bpy.context.active_object.rotation_euler.x = 0        
            bpy.context.active_object.rotation_euler.y = 0
            bpy.context.active_object.rotation_euler.z = 0
                      
            #Scale        
            context.active_object.delta_scale.x += (context.active_object.scale.x-1) * context.active_object.delta_scale.x
            context.active_object.delta_scale.y += (context.active_object.scale.y-1) * context.active_object.delta_scale.y
            context.active_object.delta_scale.z += (context.active_object.scale.z-1) * context.active_object.delta_scale.z
            context.active_object.scale=[1,1,1]   
            
            return {'FINISHED'}  
        else:            
            context.active_object.delta_location+=context.active_object.location
            context.active_object.location=[0,0,0]
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True)                   
        
            return {'FINISHED'}




############### Freeze/ UnFreeze Objects ##############



class OBJECT_OT_mesh_all(bpy.types.Operator):
	"""restrict viewport selection"""
	bl_idname = "object.mesh_all"
	bl_label = "Freez / UnFreez Mesh"

	def execute(self, context):
		objects = []
		eligible_objects = []
		objects = bpy.context.scene.objects
		#objects = scene.objects 
		#Only Specific Types? + Filter layers
		for obj in objects:
			for i in range(0,20):
				if obj.layers[i]:
					if obj.type == 'MESH':
						if obj not in eligible_objects:
							eligible_objects.append(obj)                     
		objcts = eligible_objects
		if mesh == 0:
			global mesh
			mesh = 1
			for obj in objcts: # deselect all objects
				obj.hide_select = True
		else:
			global mesh
			mesh = 0
			for obj in objcts: # deselect all objects
				obj.hide_select = False
		return {'FINISHED'}

class OBJECT_OT_curve_all(bpy.types.Operator):
	"""restrict viewport selection"""
	bl_idname = "object.curve_all"
	bl_label = "Freez / UnFreez Curve"
	def execute(self, context):
		objects = []
		eligible_objects = []
		objects = bpy.context.scene.objects
		for obj in objects:
			for i in range(0,20):
				if obj.layers[i]:
					if obj.type == 'CURVE':
						if obj not in eligible_objects:
							eligible_objects.append(obj)                     
		objcts = eligible_objects
		if curve == 0:
			global curve
			curve = 1
			for obj in objcts: # deselect all objects
				obj.hide_select = True
		else:
			global curve
			curve = 0
			for obj in objcts: # deselect all objects
				obj.hide_select = False
		return {'FINISHED'} 


class OBJECT_OT_lamp_all(bpy.types.Operator):
	"""restrict viewport selection"""
	bl_idname = "object.lamp_all"
	bl_label = "Freez / UnFreez Lamp"
	def execute(self, context):
		objects = []
		eligible_objects = []
		objects = bpy.context.scene.objects
		#objects = scene.objects 
		#Only Specific Types? + Filter layers
		for obj in objects:
			for i in range(0,20):
				if obj.layers[i]:
					if obj.type == 'LAMP':
						if obj not in eligible_objects:
							eligible_objects.append(obj)                     
		objcts = eligible_objects
		if lamp == 0:
			global lamp
			lamp = 1
			for obj in objcts: # deselect all objects
				obj.hide_select = True
		else:
			global curve
			lamp = 0
			for obj in objcts: # deselect all objects
				obj.hide_select = False

		return {'FINISHED'}


class OBJECT_OT_bone_all(bpy.types.Operator):
	"""restrict viewport selection"""
	bl_idname = "object.bone_all"
	bl_label = "Freez / UnFreez Bone"
	def execute(self, context):
		objects = []
		eligible_objects = []
		objects = bpy.context.scene.objects
		for obj in objects:
			for i in range(0,20):
				if obj.layers[i]:
					if obj.type == 'ARMATURE':
						if obj not in eligible_objects:
							eligible_objects.append(obj)                     
		objcts = eligible_objects
		if bone == 0:
			global bone
			bone = 1
			for obj in objcts: # deselect all objects
				obj.hide_select = True
		else:
			global bone
			bone = 0
			for obj in objcts: # deselect all objects
				obj.hide_select = False
		return {'FINISHED'}


class OBJECT_OT_camera_all(bpy.types.Operator):
	"""restrict viewport selection"""
	bl_idname = "object.camera_all"
	bl_label = "Freez / UnFreez Camera"
	def execute(self, context):
		objects = []
		eligible_objects = []
		objects = bpy.context.scene.objects
		for obj in objects:
			for i in range(0,20):
				if obj.layers[i]:
					if obj.type == 'CAMERA':
						if obj not in eligible_objects:
							eligible_objects.append(obj)                     
		objcts = eligible_objects
		if camera == 0:
			global camera
			camera = 1
			for obj in objcts: # deselect all objects
				obj.hide_select = True
		else:
			global camera
			camera = 0
			for obj in objcts: # deselect all objects
				obj.hide_select = False
		return {'FINISHED'}


class OBJECT_OT_particules_all(bpy.types.Operator):
	"""restrict viewport selection"""
	bl_idname = "object.particles_all"
	bl_label = "Freez / UnFreez Praticles"
	def execute(self, context):
		objects = []
		eligible_objects = []
		objects = bpy.context.scene.objects
		for obj in objects:
			for i in range(0,20):
				if obj.layers[i]:
					if obj.type == 'PARTICLES':
						if obj not in eligible_objects:
							eligible_objects.append(obj)                     
		objcts = eligible_objects
		if particles == 0:
			global particles
			particles = 1
			for obj in objcts: # deselect all objects
				obj.hide_select = True
		else:
			global particles
			particles = 0
			for obj in objcts: # deselect all objects
				obj.hide_select = False
		return {'FINISHED'}


	def invoke(self, context, event):
		return {'RUNNING_MODAL'}



########################################################################################################################################
########################################################################################################################################
############  Symmetrical Empty  #######################################################################################################
############  Symmetrical Empty  #######################################################################################################


#bl_info = {
#    "name": "Add Symmetrical Empty",
#    "author": "Pablo Vazquez",			
#    "version": (1,0,2),
#    "blender": (2, 64, 0),
#    "location": "View3D > Add > Mesh > Symmetrical Empty",
#    "description": "Add an empty mesh with a Mirror Modifier for quick symmetrical modeling",
#    "warning": "",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"\
#        "Scripts/Add_Mesh/Add_Symmetrical_Empty",
#    "tracker_url": "",
#    "category": "Add Mesh"}
#'''
#Adds an empty mesh with a mirror modifier.
#'''    


def Add_Symmetrical_Empty():

    bpy.ops.mesh.primitive_plane_add(enter_editmode = True)

    sempty = bpy.context.object
    sempty.name = "SymmEmpty"

    # check if we have a mirror modifier, otherwise add
    if (sempty.modifiers and sempty.modifiers['Mirror']):
        pass
    else:
        bpy.ops.object.modifier_add(type ='MIRROR')

    # Delete all!
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.delete(type ='VERT')


class AddSymmetricalEmpty(bpy.types.Operator):
    
    bl_idname = "mesh.primitive_symmetrical_empty_add"
    bl_label = "Add Symmetrical Empty Mesh"
    bl_description = "Add an empty mesh with a Mirror Modifier for quick symmetrical modeling"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        mirror = bpy.context.object.modifiers['Mirror']

        layout.prop(mirror,'use_clip', text="Use Clipping")

        layout.label("Mirror Axis")
        row = layout.row(align=True)
        row.prop(mirror, "use_x")
        row.prop(mirror, "use_y")
        row.prop(mirror, "use_z")

    def execute(self, context):
        Add_Symmetrical_Empty()
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True
        return {'FINISHED'}

## menu option ##
def menu_item(self, context):
    # only in object mode
    if bpy.context.mode == "OBJECT":
        self.layout.operator("mesh.primitive_symmetrical_empty_add",
            text="Symmetrical Empty", icon="EMPTY_DATA")

## register and add it on top of the list ##
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.prepend(menu_item)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)
    
    
#######################################################################################################################################
#######################################################################################################################################
############  Boolean 2D Union  #######################################################################################################
############  Boolean 2D Union  #######################################################################################################


#bl_info = {
#    'name': "Boolean 2D Union",
#    'author': "luxuy blendercn",
#    'version': (1, 0, 0),
#    'blender': (2, 70, 0),
#    'location': 'View3D > EditMode > (w) Specials', 
#    'warning': "",
#    'category': 'Mesh'}


#================================================================================
class Boolean2DUnion(bpy.types.Operator):
    bl_idname = "bpt.boolean_2d_union"
    bl_label = "Boolean 2D Union"
    bl_options = {'REGISTER', 'UNDO'}
    
    flag=BoolProperty( name="Dissolve edges", default=0)
    
    @classmethod
    def poll(cls, context):
        if context.mode=='EDIT_MESH':
            return True

    def invoke( self, context, event ):
        ob=context.object
        bpy.ops.object.mode_set(mode = 'OBJECT')
        faces=[f for f in ob.data.polygons if f.select]
        print(faces)
        bpy.ops.object.mode_set(mode = 'EDIT')
        if len(faces)>1:
            
            self.execute(context)
        else:
            msg ="Please select at least 2 faces !"
            self.report( {"INFO"}, msg  )
        
        
        
        return {"FINISHED"}
    def execute(self, context):
        ob_old=context.object
        bpy.ops.mesh.separate(type='SELECTED')
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        ob=list(set(context.selected_objects)-set([ob_old]))[0]
        
        old=bpy.data.objects[:]
        bpy.ops.object.select_all(action='DESELECT')
        ob.select=True
        bpy.context.scene.objects.active=ob
        print(ob)
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        new=bpy.data.objects[:]
        new_obs=list(set(new)-set(old))
        new_obs.append(ob)

        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(new_obs)):
            for j in range(len(new_obs)):
                if i!=j:
                    bpy.ops.object.select_all(action='DESELECT')
                    new_obs[j].select=True
                    bpy.context.scene.objects.active=new_obs[i]
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.knife_project(cut_through=True)
                    bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in new_obs:
            obj.select=True
        bpy.context.scene.objects.active=ob
        bpy.ops.object.join()
        
        bm=bmesh.new()
        bm.from_mesh(ob.data)

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0003)
        if self.flag:
            bmesh.ops.dissolve_limit(bm, angle_limit=0.087, use_dissolve_boundaries=0, verts=bm.verts, edges=bm.edges)
        bm.to_mesh(ob.data)
        bm.free()
        bpy.ops.object.select_all(action='DESELECT')
        ob.select=True
        ob_old.select=True
        bpy.context.scene.objects.active=ob_old
        bpy.ops.object.join()
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        return {'FINISHED'}
    
#---------------------------------------------
def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator('bpt.boolean_2d_union')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)



#################################################################################################################################
#################################################################################################################################
############  Mechappo  #########################################################################################################
############  Mechappo  #########################################################################################################

####################################
# Mechappo
#       v.1.0
#  (c)ishidourou 2013
####################################


#bl_info = {
#    "name": "Mechappo",
#    "author": "ishidourou",
#    "version": (1, 0),
#    "blender": (2, 65, 0),
#    "location": "View3D > Toolbar",
#    "description": "Mechappo",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": 'Mesh'}
  

#---- main ------

def subdiv(obj,number,fromall):
    if number == 0:
        return
    mode = bpy.context.mode
    if mode != 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_mode(type='FACE')
    if fromall == True:
        bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=number)
    bpy.ops.mesh.select_mode(type='FACE')
    if mode != 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()

def makemat(obj,matname,ct):
    mat = bpy.data.materials.new(matname)
    obj.data.materials.append(mat)
    #obj.data.materials[0] = mat
    bpy.context.object.active_material_index = ct
    bpy.ops.object.material_slot_assign()
    bpy.context.object.active_material.diffuse_color = (random.random(), random.random(), random.random())

def randselect(obj,ratio,fromall):
    bpy.ops.object.mode_set(mode = 'EDIT')
    if fromall == True:
        bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    ct = 0
    for i in obj.data.polygons:
        randval = random.random()
        if randval > ratio:
             i.select = False
        ct += 1
    bpy.ops.object.mode_set(mode = 'EDIT')
    
def hide():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.hide(unselected=True)


def unhide():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='INVERT')

def extrude(size):
    bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":size, "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})

def selectcheck(obj):
     
    if obj == None:
        print('not selected object')
        return False
    if  obj.type != 'MESH':
        print('not mesh type')
        return False

def get_polygon_number(obj):
    mesh = obj.data
    num = 0
    for face in mesh.polygons:
        num += 1
    return num
    
def valuecheck(obj,cuts,depth,ratio,sidepoly):
    if ratio == 0:
        ratio = 0.001
    polygons = get_polygon_number(obj)
    sidepoly += 1
    cuts += 1
    cuts **= 2
    value = polygons
    for i in range(depth):
        polygons = polygons * cuts
    #polygons *= sidepoly
    if polygons > 300000/ratio:
        print('polygons=',polygons,value,'limit=',300000/ratio)
        return False
    print('OK')
    print('polygons=',polygons,value,300000/ratio)
    return True
    

class ErrorDialog(bpy.types.Operator):
    bl_idname = "error.dialog"
    bl_label = "Warning:"
    bl_options = {'REGISTER'}
        
    my_message = StringProperty(name="message",default='Prease Input Smaller Values to Cuts or Depth.')    

    def execute(self, context):
        message = self.my_message
        print(message)
        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        global wmessage
        self.layout.label(wmessage)
 

cuts = 0
depth = 1
thickness = 0.01
ratio = 0.5
addmat = True
wmessage = 'Dummy'


class MechappoCreate(bpy.types.Operator):

    bl_idname = "mechappo.create"
    bl_label = "Mechappo Create"
    bl_options = {'REGISTER'}

    my_fromall = BoolProperty(name="from Selected All",default=False)
    my_cuts = bpy.props.IntProperty(name="Subdivide:",min=0,max=100,default = cuts)
    my_depth = bpy.props.IntProperty(name="Depth:",min=1,max=10,default = depth)
    my_thickness = bpy.props.FloatProperty(name="Thickness:",default = thickness)
    my_ratio = bpy.props.FloatProperty(name="Selected ratio:",min=0,max=1,default = ratio)
    my_addmat = BoolProperty(name="Add Material",default = addmat)


    def execute(self, context):
        
        fromall = self.my_fromall
        cuts = self.my_cuts
        depth = self.my_depth
        thickness = self.my_thickness
        ratio = self.my_ratio
        addmat = self.my_addmat
        global wmessage
        
        obj = bpy.context.active_object
        if selectcheck(obj) == False:
            wmessage = "Prease Select Mesh Object."
            bpy.ops.error.dialog('INVOKE_DEFAULT')
            return{'FINISHED'}
        if valuecheck(obj,cuts,depth,ratio,4) == False:
            wmessage = "Prease Input Smaller Values to Cuts or Depth."
            bpy.ops.error.dialog('INVOKE_DEFAULT')
            return{'FINISHED'}
      
        ct = 0
        ii = 0
        for i in obj.data.materials:
            ii += 1
        print(ii)
        hide()
        for i in range(depth):
            subdiv(obj,cuts,fromall)
            randselect(obj,ratio,fromall)
            if ct == 0:
                thickness *= -1
            else:
                if random.random() < 0.5:
                    thickness *= -1
            extrude(thickness)
            if addmat == True:
                makemat(obj,'mat',ct+ii)
            ct += 1
        unhide()
        
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)

        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class MechappoSelect(bpy.types.Operator):

    bl_idname = "mechappo.select"
    bl_label = "Mechappo Select"
    bl_options = {'REGISTER'}

    my_fromall = BoolProperty(name="from Selected All",default=False)
    my_cuts = bpy.props.IntProperty(name="Subdivide:",min=0,max=100,default = cuts)
    my_depth = bpy.props.IntProperty(name="Depth:",min=1,max=10,default = depth)
    my_ratio = bpy.props.FloatProperty(name="Selected ratio:",min=0,max=1,default = ratio)
    my_addmat = BoolProperty(name="Add Material",default = False)


    def execute(self, context):
        
        fromall = self.my_fromall
        cuts = self.my_cuts
        depth = self.my_depth
        ratio = self.my_ratio
        addmat = self.my_addmat
        global wmessage
        
        obj = bpy.context.active_object
        if selectcheck(obj) == False:
            wmessage = "Prease Select Mesh Object."
            bpy.ops.error.dialog('INVOKE_DEFAULT')
            return{'FINISHED'}
        if cuts != 0:
            if valuecheck(obj,cuts,depth,ratio,0) == False:
                wmessage = "Prease Input Smaller Values to Cuts or Depth."
                bpy.ops.error.dialog('INVOKE_DEFAULT')
                return{'FINISHED'}
            
        ct = 0
        ii = 0
        for i in obj.data.materials:
            ii += 1
        for i in range(depth):
            subdiv(obj,cuts,fromall)
            randselect(obj,ratio,fromall)
            if addmat == True:
                makemat(obj,'mat',ct+ii)
            ct += 1
        
        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#	Registration

def register():
    bpy.utils.register_class(MechappoCreate)
    bpy.utils.register_class(MechappoSelect)
    bpy.utils.register_class(ErrorDialog)

def unregister():
    bpy.utils.unregister_class(MechappoCreate)
    bpy.utils.unregister_class(MechappoSelect)
    bpy.utils.unregister_class(ErrorDialog)
    
    
#################################################################################################################################
#################################################################################################################################
############  Look at it  #######################################################################################################
############  Look at it  #######################################################################################################

####################################
# Look at it
#       v.1.0
#  (c)ishidourou 2013
####################################


#bl_info = {
#    "name": "Look at it",
#    "author": "ishidourou",
#    "version": (1, 0),
#    "blender": (2, 65, 0),
#    "location": "View3D > Toolbar",
#    "description": "LookatIt",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": '3D View'}
    

#---- main ------

def objselect(objct,selection):
    if (selection == 'ONLY'):
        bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = objct
    objct.select = True

class LookatIt(bpy.types.Operator):
    """align the Y axis / normal world space"""
    bl_idname = "lookat.it"
    bl_label = "Look at it"
    def execute(self, context):
        cobj = bpy.context.object
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        if cobj == None:
            return{'FINISHED'}
        slist = bpy.context.selected_objects
        ct = 0
        for i in slist:
            ct += 1
        if ct == 1:
            return{'FINISHED'}
        bpy.ops.object.track_set(type='TRACKTO')
        bpy.ops.object.track_clear(type='CLEAR_KEEP_TRANSFORM')
        return{'FINISHED'}


def lookatempty(mode):
    if bpy.context.mode != 'OBJECT':
        return
    cobj = bpy.context.object
    slist = bpy.context.selected_objects
    ct = 0
    for i in slist:
        ct += 1
    if ct == 0:
        return            
    bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False)
    bpy.context.object.empty_draw_size = 3.00
    target = bpy.context.object
    for i in slist:
        i.select = True
    if mode == 'cursor' or 'damptrackempty':
        bpy.ops.object.track_set(type='DAMPTRACK')
    if mode == 'tracktoempty':
        bpy.ops.object.track_set(type='TRACKTO')
    if mode == 'locktrackempty':
        bpy.ops.object.track_set(type='LOCKTRACK')
    if mode == 'cursor':
        bpy.ops.object.track_clear(type='CLEAR_KEEP_TRANSFORM')
        objselect(target,'ONLY')
        bpy.ops.object.delete(use_global=False)
        objselect(cobj,'ADD')
        for i in slist:
            i.select = True

class LookatCursor(bpy.types.Operator):
    """align the Y axis - normal world space - to cusor"""
    bl_idname = "lookat.cursor"
    bl_label = "Look at Cursor"
    def execute(self, context):
        lookatempty('cursor')
        return{'FINISHED'}
    
class TrackTo(bpy.types.Operator):
    bl_idname = "track.to"
    bl_label = "TrackTo"
    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        bpy.ops.object.track_set(type='TRACKTO')
        return{'FINISHED'}

class DampedTrack(bpy.types.Operator):
    bl_idname = "damped.track"
    bl_label = "DampedTrack"
    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        bpy.ops.object.track_set(type='DAMPTRACK')
        return{'FINISHED'}

class LockTrack(bpy.types.Operator):
    bl_idname = "lock.track"
    bl_label = "LockTrack"
    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        bpy.ops.object.track_set(type='LOCKTRACK')
        return{'FINISHED'}

class TrackToEmpty(bpy.types.Operator):
    bl_idname = "track.toempty"
    bl_label = "TrackTo"
    def execute(self, context):
        lookatempty('tracktoempty')
        return{'FINISHED'}

class DampedTrackEmpty(bpy.types.Operator):
    bl_idname = "damped.trackempty"
    bl_label = "DampedTrack"
    def execute(self, context):
        lookatempty('damptrackempty')
        return{'FINISHED'}

class LockTrackEmpty(bpy.types.Operator):
    bl_idname = "lock.trackempty"
    bl_label = "LockTrack"
    def execute(self, context):
        lookatempty('locktrackempty')
        return{'FINISHED'}

#	Registration

def register():
    bpy.utils.register_class(LookatIt)
    bpy.utils.register_class(LookatCursor)
    bpy.utils.register_class(TrackTo)
    bpy.utils.register_class(DampedTrack)
    bpy.utils.register_class(LockTrack)
    bpy.utils.register_class(TrackToEmpty)
    bpy.utils.register_class(DampedTrackEmpty)
    bpy.utils.register_class(LockTrackEmpty)

def unregister():
    bpy.utils.unregister_class(LookatIt)
    bpy.utils.unregister_class(LookatCursor)
    bpy.utils.unregister_class(TrackTo)
    bpy.utils.unregister_class(DampedTrack)
    bpy.utils.unregister_class(LockTrack)
    bpy.utils.unregister_class(TrackToEmpty)
    bpy.utils.unregister_class(DampedTrackEmpty)
    bpy.utils.unregister_class(LockTrackEmpty)




##################################################################################################################################
##################################################################################################################################
############  Distribute  ########################################################################################################
############  Distribute  ########################################################################################################


#bl_info = {
 #   "name": "Distribute",
  #  "author": "Oscurart, CodemanX",
   # "version": (3,1),
    #"location": "View3D > Tools > Oscurart Tools",
    #"description": "Space Objects between there Origins",
    #"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Oscurart_Tools",
    #"category": ""}



# POLLS
class OscPollObject():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(cls, context):
        return context.scene.osc_object_tools
    

## ------------------------------------ SELECTION --------------------------------------
bpy.selection_osc=[]

def select_osc():
    if bpy.context.mode == "OBJECT":
        obj = bpy.context.object
        sel = len(bpy.context.selected_objects)

        if sel == 0:
            bpy.selection_osc=[]
        else:
            if sel == 1:
                bpy.selection_osc=[]
                bpy.selection_osc.append(obj)
            elif sel > len(bpy.selection_osc):
                for sobj in bpy.context.selected_objects:
                    if (sobj in bpy.selection_osc) == False:
                        bpy.selection_osc.append(sobj)

            elif sel < len(bpy.selection_osc):
                for it in bpy.selection_osc:
                    if (it in bpy.context.selected_objects) == False:
                        bpy.selection_osc.remove(it)

class OscSelection(bpy.types.Header):
    
    bl_label = "Selection Osc"
    bl_space_type = "VIEW_3D"

    def __init__(self):
        select_osc()

    def draw(self, context):
        """
        layout = self.layout
        row = layout.row()
        row.label("Sels: "+str(len(bpy.selection_osc)))
        """  

##=============== DISTRIBUTE ======================    


def ObjectDistributeOscurart (self, X, Y, Z):
    if len(bpy.selection_osc[:]) > 1:
        # VARIABLES
        dif = bpy.selection_osc[-1].location-bpy.selection_osc[0].location
        chunkglobal = dif/(len(bpy.selection_osc[:])-1)
        chunkx = 0
        chunky = 0
        chunkz = 0
        deltafst = bpy.selection_osc[0].location
        
        #ORDENA
        for OBJECT in bpy.selection_osc[:]:          
            if X:  OBJECT.location.x=deltafst[0]+chunkx
            if Y:  OBJECT.location[1]=deltafst[1]+chunky
            if Z:  OBJECT.location.z=deltafst[2]+chunkz
            chunkx+=chunkglobal[0]
            chunky+=chunkglobal[1]
            chunkz+=chunkglobal[2]
    else:  
        self.report({'ERROR'}, "Selection is only 1!")      
    
class DialogDistributeOsc(bpy.types.Operator):
    """Space Objects between there Origins"""
    bl_idname = "object.distribute_osc"
    bl_label = "Distribute Objects"       
    Boolx = bpy.props.BoolProperty(name="X")
    Booly = bpy.props.BoolProperty(name="Y")
    Boolz = bpy.props.BoolProperty(name="Z")
    
    def execute(self, context):
        ObjectDistributeOscurart(self, self.Boolx,self.Booly,self.Boolz)
        return {'FINISHED'}
    def invoke(self, context, event):
        self.Boolx = True
        self.Booly = True
        self.Boolz = True        
        return context.window_manager.invoke_props_dialog(self)



#############################################################################################################################
#############################################################################################################################
#############  Drop to Ground  ##############################################################################################
#############  Drop to Ground  ##############################################################################################


#bl_info = {
 #   'name': 'Drop to Ground',
  #  'author': 'Unnikrishnan(kodemax), Florian Meyer(testscreenings)',
   # 'version': (1,2),
    #"blender": (2, 63, 0),
    #'location': '3D View -> Tool Shelf -> Object Tools Panel (at the bottom)',
    #'description': 'Drop selected objects on active object',
    #'warning': '',
    #'wiki_url': 'http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/Drop_to_ground',
    #"tracker_url": "http://projects.blender.org/tracker/?func=detail&atid=25349",
    #'category': ''}


def get_align_matrix(location, normal):
    up = Vector((0,0,1))                      
    angle = normal.angle(up)
    axis = up.cross(normal)                            
    mat_rot = Matrix.Rotation(angle, 4, axis) 
    mat_loc = Matrix.Translation(location)
    mat_align = mat_rot * mat_loc                      
    return mat_align

def transform_ground_to_world(sc, ground):
    tmpMesh = ground.to_mesh(sc, True, 'PREVIEW')
    tmpMesh.transform(ground.matrix_world)
    tmp_ground = bpy.data.objects.new('tmpGround', tmpMesh)
    sc.objects.link(tmp_ground)
    sc.update()
    return tmp_ground

def get_lowest_world_co_from_mesh(ob, mat_parent=None):
    bme = bmesh.new()
    bme.from_mesh(ob.data)
    mat_to_world = ob.matrix_world.copy()
    if mat_parent:
        mat_to_world = mat_parent * mat_to_world
    lowest=None
    #bme.verts.index_update() #probably not needed
    for v in bme.verts:
        if not lowest:
            lowest = v
        if (mat_to_world * v.co).z < (mat_to_world * lowest.co).z:
            lowest = v
    lowest_co = mat_to_world * lowest.co
    bme.free()
    return lowest_co

def get_lowest_world_co(context, ob, mat_parent=None):
    if ob.type == 'MESH':
        return get_lowest_world_co_from_mesh(ob)
    
    elif ob.type == 'EMPTY' and ob.dupli_type == 'GROUP':
        if not ob.dupli_group:
            return None
        
        else:
            lowest_co = None
            for ob_l in ob.dupli_group.objects:
                if ob_l.type == 'MESH':
                    lowest_ob_l = get_lowest_world_co_from_mesh(ob_l, ob.matrix_world)
                    if not lowest_co:
                        lowest_co = lowest_ob_l
                    if lowest_ob_l.z < lowest_co.z:
                        lowest_co = lowest_ob_l
                        
            return lowest_co

def drop_objects(self, context):
    ground = context.object
    obs = context.selected_objects
    obs.remove(ground)
    tmp_ground = transform_ground_to_world(context.scene, ground)
    down = Vector((0, 0, -10000))
    
    for ob in obs:
        if self.use_origin:
            lowest_world_co = ob.location
        else:
            lowest_world_co = get_lowest_world_co(context, ob)
        if not lowest_world_co:
            print(ob.type, 'is not supported. Failed to drop', ob.name)
            continue
        hit_location, hit_normal, hit_index = tmp_ground.ray_cast(lowest_world_co,
                                                                  lowest_world_co + down)
        if hit_index == -1:
            print(ob.name, 'didn\'t hit the ground')
            continue
        
        # simple drop down
        to_ground_vec =  hit_location - lowest_world_co
        ob.location += to_ground_vec
        
        # drop with align to hit normal
        if self.align:
            to_center_vec = ob.location - hit_location #vec: hit_loc to origin
            # rotate object to align with face normal
            mat_normal = get_align_matrix(hit_location, hit_normal)
            rot_euler = mat_normal.to_euler()
            mat_ob_tmp = ob.matrix_world.copy().to_3x3()
            mat_ob_tmp.rotate(rot_euler)
            mat_ob_tmp = mat_ob_tmp.to_4x4()
            ob.matrix_world = mat_ob_tmp
            # move_object to hit_location
            ob.location = hit_location
            # move object above surface again
            to_center_vec.rotate(rot_euler)
            ob.location += to_center_vec
        

    #cleanup
    bpy.ops.object.select_all(action='DESELECT')
    tmp_ground.select = True
    bpy.ops.object.delete('EXEC_DEFAULT')
    for ob in obs:
        ob.select = True
    ground.select = True
    


class OBJECT_OT_drop_to_ground(Operator):
    """Drop selected objects on active object"""
    bl_idname = "object.drop_on_active"
    bl_label = "Drop to Ground"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Drop selected objects on active object"

    align = BoolProperty(
            name="Align to ground",
            description="Aligns the object to the ground",
            default=True)
    use_origin = BoolProperty(
            name="Use Center",
            description="Drop to objects origins",
            default=False)

    ##### POLL #####
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 2
    
    ##### EXECUTE #####
    def execute(self, context):
        print('\nDropping Objects')
        drop_objects(self, context)
        return {'FINISHED'}




################################################################################################################################
################################################################################################################################
###########  Face Inset Fillet  ################################################################################################
###########  Face Inset Fillet  ################################################################################################


# based completely on addon by zmj100

# ------ ------
def edit_mode_out():
    bpy.ops.object.mode_set(mode = 'OBJECT')

def edit_mode_in():
    bpy.ops.object.mode_set(mode = 'EDIT')

def a_rot(ang, rp, axis, q):
    return (Matrix.Rotation(ang, 3, axis) * (q - rp)) + rp

# ------ ------
def f_(bme, list_0, opp, adj1, n_, out, radius, en0, kp):

    list_del = []
    for fi in list_0:
        f = bme.faces[fi]
        f.select_set(0)
        list_del.append(f)
        f.normal_update()
        list_2 = [v.index for v in f.verts]
        dict_0 = {}
        list_1 = []
        n = len(list_2)
        for i in range(n):
            dict_0[i] = []
            p = (bme.verts[ list_2[i] ].co).copy()
            p1 = (bme.verts[ list_2[(i - 1) % n] ].co).copy()
            p2 = (bme.verts[ list_2[(i + 1) % n] ].co).copy()
            dict_0[i].append(bme.verts[list_2[i]])
            vec1 = p - p1
            vec2 = p - p2
            ang = vec1.angle(vec2)
            adj = opp / tan(ang * 0.5)
            h = (adj ** 2 + opp ** 2) ** 0.5
            if round(degrees(ang)) == 180 or round(degrees(ang)) == 0.0:
                p6 = a_rot(radians(90), p, vec1, p + ((f.normal).normalized() * opp) if out == True else p - ((f.normal).normalized() * opp))
                list_1.append(p6)
            else:
                p6 = a_rot(-radians(90), p, ((p - (vec1.normalized() * adj)) - (p - (vec2.normalized() * adj))), p + ((f.normal).normalized() * h) if out == True else p - ((f.normal).normalized() * h))
                list_1.append(p6)

        list_2 = []
        n1_ = len(list_1)
        for j in range(n1_):
            q = list_1[j]
            q1 = list_1[(j - 1) % n1_]
            q2 = list_1[(j + 1) % n1_]
            vec1_ = q - q1
            vec2_ = q - q2
            ang_ = vec1_.angle(vec2_)
            if round(degrees(ang_)) == 180 or round(degrees(ang_)) == 0.0:
                bme.verts.new(q)
                bme.verts.index_update()
                list_2.append(bme.verts[-1])
                dict_0[j].append(bme.verts[-1])
            else:
                opp_ = adj1
                if radius == False:
                    h_ = adj1 * (1 / cos(ang_ * 0.5))
                    d = adj1
                elif radius == True:
                    h_ = opp_ / sin(ang_ * 0.5)
                    d = opp_ / tan(ang_ * 0.5)

                q3 = q - (vec1_.normalized() * d)
                q4 = q - (vec2_.normalized() * d)
                rp_ = q - ((q - ((q3 + q4) * 0.5)).normalized() * h_)
                axis_ = vec1_.cross(vec2_)
                vec3_ = rp_ - q3
                vec4_ = rp_ - q4
                rot_ang = vec3_.angle(vec4_)
                list_3 = []
                
                for o in range(n_ + 1):
                    q5 = a_rot((rot_ang * o / n_), rp_, axis_, q4)
                    bme.verts.new(q5)
                    bme.verts.index_update()
                    dict_0[j].append(bme.verts[-1])
                    list_3.append(bme.verts[-1])
                list_3.reverse()
                list_2.extend(list_3)

        if out == False:
            bme.faces.new(list_2)
            bme.faces.index_update()
            bme.faces[-1].select_set(1)
        elif out == True and kp == True:
            bme.faces.new(list_2)
            bme.faces.index_update()
            bme.faces[-1].select_set(1)

        n2_ = len(dict_0)
        for o in range(n2_):
            list_a = dict_0[o]
            list_b = dict_0[(o + 1) % n2_]
            bme.faces.new( [ list_a[0], list_b[0], list_b[-1], list_a[1] ] )
            bme.faces.index_update()

        if en0 == 'opt0':
            for k in dict_0:
                if len(dict_0[k]) > 2:
                    bme.faces.new(dict_0[k])
                    bme.faces.index_update()
        if en0 == 'opt1':
            for k_ in dict_0:
                q_ = dict_0[k_][0]
                dict_0[k_].pop(0)
                n3_ = len(dict_0[k_])
                for kk in range(n3_ - 1):
                    bme.faces.new( [ dict_0[k_][kk], dict_0[k_][(kk + 1) % n3_], q_ ] )
                    bme.faces.index_update()


    del_ = [bme.faces.remove(f) for f in list_del]
    del del_

# ------ operator 0 ------
class faceinfillet_op0(bpy.types.Operator):
    bl_idname = 'faceinfillet.op0_id'
    bl_label = 'Face Inset Fillet'
    bl_description = 'inset selected faces'
    bl_options = {'REGISTER', 'UNDO'}

    opp = FloatProperty( name = '', default = 0.04, min = 0, max = 100.0, step = 1, precision = 3 )      # inset amount
    n_ = IntProperty( name = '', default = 4, min = 1, max = 100, step = 1 )      # number of sides
    adj1 = FloatProperty( name = '', default = 0.04, min = 0.00001, max = 100.0, step = 1, precision = 3 )
    out = BoolProperty( name = 'Out', default = False )
    radius = BoolProperty( name = 'Radius', default = False )
    en0 = EnumProperty( items =( ('opt0', 'Type 1', ''), ('opt1', 'Type 2', '') ), name = '', default = 'opt0' )
    kp = BoolProperty( name = 'Keep face', default = False )
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'en0', text = 'Corner type')
        row0 = box.row(align = True)
        row0.prop(self, 'out')
        if self.out == True:
            row0.prop(self, 'kp')
        row = box.split(0.40, align = True)
        row.label('Inset amount:')
        row.prop(self, 'opp')
        row1 = box.split(0.60, align = True)
        row1.label('Number of sides:')
        row1.prop(self, 'n_', slider = True)
        box.prop(self, 'radius')
        row2 = box.split(0.40, align = True)
        if self.radius == True:
            row2.label('Radius:')
        else:
            row2.label('Distance:')
        row2.prop(self, 'adj1')

    def execute(self, context):
        opp = self.opp
        n_ = self.n_
        adj1 = self.adj1
        out = self.out
        radius = self.radius
        en0 = self.en0
        kp = self.kp

        edit_mode_out()
        ob_act = context.active_object
        bme = bmesh.new()
        bme.from_mesh(ob_act.data)
        
        list_0 = [ f.index for f in bme.faces if f.select and f.is_valid ]

        if len(list_0) == 0:
            self.report({'INFO'}, 'No faces selected unable to continue.')
            edit_mode_in()
            return {'CANCELLED'}
        elif len(list_0) != 0:
            f_(bme, list_0, opp, adj1, n_, out, radius, en0, kp)

        bme.to_mesh(ob_act.data)
        edit_mode_in()
        return {'FINISHED'}

class inset_help(bpy.types.Operator):
	bl_idname = 'help.face_inset'
	bl_label = ''

	def draw(self, context):
		layout = self.layout
		layout.label('To use:')
		layout.label('Select a face or faces & inset.')
		layout.label('Inset square, circle or outside.')
		layout.label('To Help:')
		layout.label('Circle: use remove doubles to tidy joins.')
		layout.label('Outset: select & use normals flip before extruding.')
	
	def execute(self, context):
		return {'FINISHED'}

	def invoke(self, context, event):
		return context.window_manager.invoke_popup(self, width = 350)



        
#############################################################################################################################################
#############################################################################################################################################
##########  Curve Outline  ##################################################################################################################
##########  Curve Outline  ##################################################################################################################

#bl_info = {
#    "name": "Curve Outline",
#    "description": "creates an Outline",
#    "category": "Object",
#    "author": "Yann Bertrand (jimflim)",
#    "version": (0, 4),
#    "blender": (2, 69, 0),
#}


def createOutline(curve, outline):

    for spline in curve.data.splines[:]:
        p = spline.bezier_points
        out = []
        
        n = ((p[0].handle_right-p[0].co).normalized()-(p[0].handle_left-p[0].co).normalized()).normalized()
        n = Vector((-n[1], n[0], n[2]))
        o = p[0].co+outline*n
        out.append(o)
        
        for i in range(1,len(p)):
            n = ((p[i].handle_right-p[i].co).normalized()-(p[i].handle_left-p[i].co).normalized()).normalized()
            n = Vector((-n[1], n[0], n[2]))
            o = intersect_line_line(out[-1], (out[-1]+p[i].co-p[i-1].co), p[i].co, p[i].co+n)[0]
            out.append(o)
            
        curve.data.splines.new('BEZIER')
        if spline.use_cyclic_u:
            curve.data.splines[-1].use_cyclic_u = True
        p_out = curve.data.splines[-1].bezier_points
        p_out.add(len(out)-1)
    
        for i in range(len(out)):
            p_out[i].handle_left_type = 'FREE'  
            p_out[i].handle_right_type = 'FREE'
            
            p_out[i].co = out[i]
            
            if i<len(out)-1:
                l = (p[i+1].co-p[i].co).length
                l2 = (out[i]-out[i+1]).length
            
            if i==0:
                p_out[i].handle_left = out[i] + ((p[i].handle_left-p[i].co)*l2/l)
            if i<len(out)-1:
                p_out[i+1].handle_left = out[i+1] + ((p[i+1].handle_left-p[i+1].co)*l2/l)
            p_out[i].handle_right = out[i] + ((p[i].handle_right-p[i].co)*l2/l)
    
        for i in range(len(p)):
            p_out[i].handle_left_type = p[i].handle_left_type
            p_out[i].handle_right_type = p[i].handle_right_type
            
    return


class CurveOutline(bpy.types.Operator):
    """Curve Outliner"""
    bl_idname = "object._curve_outline"
    bl_label = "Create Outline"
    bl_options = {'REGISTER', 'UNDO'}
    outline = bpy.props.FloatProperty(name="Amount", default=0.1, min=-10, max=10)
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'CURVE')

    def execute(self, context):
        createOutline(context.object, self.outline)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)
    
def menu_func(self, context):
    self.layout.operator(CurveOutline.bl_idname)
    
def register():
    bpy.utils.register_class(CurveOutline)

def unregister():
    bpy.utils.unregister_class(CurveOutline)



#############################################################################################################################
#############################################################################################################################
#############  Align by faces  ##############################################################################################
#############  Align by faces  ##############################################################################################


#bl_info = {
 #   "name": "Align by faces",
  #  "author": "Tom Rethaller",
   # "version": (0,2,2),
    #"blender": (2, 65, 0),
    #"description": "Align two objects by their active faces",
    #"category": ""}

def get_ortho(a,b,c):
    if c != 0.0 and -a != b:
        return [-b-c, a,a]
    else:
        return [c,c,-a-b]

def clamp(v,min,max):
    if v < min:
        return min
    if v > max:
        return max
    return v

def align_faces(from_obj, to_obj):
    fpolys = from_obj.data.polygons
    tpolys = to_obj.data.polygons
    fpoly = fpolys[fpolys.active]
    tpoly = tpolys[tpolys.active]
    
    to_obj.rotation_mode = 'QUATERNION'
    tnorm = to_obj.rotation_quaternion * tpoly.normal
    
    fnorm = fpoly.normal
    axis = fnorm.cross(tnorm)
    dot = fnorm.normalized().dot(tnorm.normalized())
    dot = clamp(dot, -1.0, 1.0)
    
    # Parallel faces need a new rotation vactor
    if axis.length < 1.0e-8:
        axis = Vector(get_ortho(fnorm.x, fnorm.y, fnorm.z))
        
    from_obj.rotation_mode = 'AXIS_ANGLE'
    from_obj.rotation_axis_angle = [math.acos(dot) + math.pi, axis[0],axis[1],axis[2]]
    bpy.context.scene.update()  
    
    # Move from_obj so that faces match
    fvertices = [from_obj.data.vertices[i].co for i in fpoly.vertices]
    tvertices = [to_obj.data.vertices[i].co for i in tpoly.vertices]
    
    fbary = from_obj.matrix_world * (reduce(Vector.__add__, fvertices) / len(fvertices))
    tbary = to_obj.matrix_world * (reduce(Vector.__add__, tvertices) / len(tvertices))
    
    from_obj.location = tbary - (fbary - from_obj.location)


class OBJECT_OT_AlignByFaces(bpy.types.Operator):
    """Align two objects by their active faces"""
    bl_label = "Align by faces"
    bl_description= "Align two objects by their active faces"
    bl_idname = "object.align_by_faces"

    @classmethod
    def poll(cls, context):
        if not len(context.selected_objects) is 2:
            return False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                return False
        return True

    def execute(self, context):
        objs_to_move = [o for o in context.selected_objects if o != context.active_object]
        for o in objs_to_move:
        	align_faces(o, context.active_object)
        return {'FINISHED'}



###########################################################################################################################
############################################################################################################################
##########  Circle Array   #################################################################################################
##########  Circle Array   #################################################################################################

# -*- coding: utf-8 -*-

#bl_info = {  
 #    "name": "Circle Array",  
  #   "author": "Antonis Karvelas",  
   #  "version": (1, 0),  
    # "blender": (2, 6, 7),  
     #"location": "View3D > Object > Circle_Array",  
     #"description": "Uses an existing array and creates an empty,rotates it properly and makes a Circle Array ",  
     #"warning": "You must have an object and an array, or two objects, with only the first having an array",  
     #"wiki_url": "",  
     #"tracker_url": "",  
     #"category": ""}  


    
class Circle_ArrayA(bpy.types.Operator):
    """add an empty with array modifier / Z axis"""
    bl_label = "1/4 Circle Array"
    bl_idname = "objects.circle_array_operator1"   
    

    
    def execute(self, context):
        
       
        for obj in bpy.context.selected_objects:
	        
            bpy.context.scene.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].count = 4
            
           
        if len(bpy.context.selected_objects) == 2:
            list = bpy.context.selected_objects
            active = list[0]
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            active.select = False
            bpy.context.scene.objects.active = list[0]
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object                
            bpy.context.scene.objects.active = active            
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            return {'FINISHED'}     
        
        
        else:
            active = context.active_object
            active.modifiers[0].use_object_offset = True 
            active.modifiers[0].use_relative_offset = False
            bpy.ops.view3d.snap_cursor_to_selected()
            if active.modifiers[0].offset_object == None:
                bpy.ops.object.add(type='EMPTY')
                empty_name = bpy.context.active_object
                empty_name.name = "EMPTY"
                active.modifiers[0].offset_object = empty_name
            else:
                empty_name = active.modifiers[0].offset_object
            bpy.context.scene.objects.active = active
            num = active.modifiers["Array"].count
            print(num)
            rotate_num = 360 / num
            print(rotate_num)
            active.select = True
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True) 
            empty_name.rotation_euler = (0, 0, radians(rotate_num))
            empty_name.select = False
            active.select = True
            return {'FINISHED'} 



class ObjectCursorArray(bpy.types.Operator):
    """Array the active object to the cursor location"""
    bl_idname = "object.cursor_array"
    bl_label = "Cursor Array"
    bl_options = {'REGISTER', 'UNDO'}

    total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        for i in range(self.total):
            obj_new = obj.copy()
            scene.objects.link(obj_new)

            factor = i / self.total
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ObjectCursorArray.bl_idname)



##########################################################################################################################################   
##########################################################################################################################################           
###########  Replicator  #################################################################################################################   
###########  Replicator  #################################################################################################################  
#import bpy
#import math

# bl_info is a dictionary containing addon meta-data such as the title, version and author to be displayed in the user preferences addon list.
#bl_info = {
 #   "name": "ARewO",
  #  "author": "Frederik Steinmetz & Gottfried Hofmann",
   # "version": (0, 3),
    #"blender": (2, 66, 0),
    #"location": "SpaceBar Search -> ARewO",
    #"description": "Animation replicator with offset",
    #"category": "",}


# time_start = time.time()
# offset_extra = 0
# replicat = bpy.context.active_object


class ARewO(bpy.types.Operator):
    """replicator with optionsetting"""     
    bl_idname = "object.arewo"        
    bl_label = "ARewO"         
    bl_options = {'REGISTER', 'UNDO'}  
    

    loops = bpy.props.IntProperty(name="Replications", description="How many?", default=1, min=1, soft_max=1000, step=1)
    
    offset = bpy.props.FloatProperty(name="Offset", description="Offset of the animations in frames", default = 10.0, soft_max=1000.0, soft_min=-1000.0, step=1.0)
    
    distance = bpy.props.FloatVectorProperty(name="Distance", description="Distance between the elements in BUs", default = (0.1, 0.0, 0.0))
    
    rotation = bpy.props.FloatVectorProperty(name="Rotation", description="Delta rotation of the elements in radians", default = (0.0, 0.0, 0.0))

    scale = bpy.props.FloatVectorProperty(name="Scale", description="Delta scale of the elements in BUs", default = (0.0, 0.0, 0.0))

    def execute(self, context):
        
        #the actual script
        for i in range(self.loops):
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False})
            obj = bpy.context.active_object
            
            obj.delta_location[0] += self.distance[0]
            obj.delta_location[1] += self.distance[1]
            obj.delta_location[2] += self.distance[2]
            
            obj.delta_rotation_euler.x += self.rotation[0]
            obj.delta_rotation_euler.y += self.rotation[1]
            obj.delta_rotation_euler.z += self.rotation[2]
            
            obj.delta_scale[0] += self.scale[0]
            obj.delta_scale[1] += self.scale[1]
            obj.delta_scale[2] += self.scale[2]
            

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(ARewO.bl_idname)




###################################################################################################################################
###################################################################################################################################
#########  RotateConstrained  #####################################################################################################
#########  RotateConstrained  #####################################################################################################    


#bl_info = {
#    "name": "Rotate Constrained",
#    "author": "Ryan Southall",
#    "version": (0, 0, 1),
#    "blender": (2, 6, 6),
#   "category": ""}




class RotateConstrained(bpy.types.Operator):
    """Rotation with constrained vertices"""
    bl_idname = "mesh.rot_con"
    bl_label = "Rotate Constrained"
    bl_options = {'REGISTER', 'UNDO'}

    axis = bpy.props.EnumProperty(
            items=[("0", "X", "Rotate around X-axis"),
                   ("1", "Y", "Rotate around Y-axis"),
                   ("2", "Z", "Rotate around Z-axis"),
                   ],
            name="Rotation Axis",
            description="Specify the axis of rotation",
            default="1")
    
    caxis = bpy.props.EnumProperty(
            items=[("0", "X", "Constrain to X-axis"),
                   ("1", "Y", "Constrain to Y-axis"),
                   ("2", "Z", "Constrain to Z-axis"),
                   ],
            name="Constraint Axis",
            description="Specify the vertex constraint axis",
            default="2")
    
    rpoint = bpy.props.EnumProperty(
            items=[("0", "Mid", "Rotate the end face around its midpoint"),
                   ("1", "Max", "Rotate the end face around its highpoint"),
                   ("2", "Min", "Rotate the end face around its lowpoint"),
                   ],
            name="Rotation point",
            description="Specify the point on the end face to rotate around",
            default="0")
    
    rdeg = bpy.props.FloatProperty(name="Degrees", default = 0, min = -120, max = 120)
    
    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode = "OBJECT")
        self.fnorm = [face.normal for face in context.active_object.data.polygons if face.select == True][0]
        (self.fnormx, self.fnormy, self.fnormz) = self.fnorm
        bpy.ops.object.mode_set(mode = "EDIT")
        return {'FINISHED'}
        
    def execute(self, context):
        if self.rdeg != 0 and self.caxis != self.axis:
            bpy.ops.object.mode_set(mode = "OBJECT")
            mesh = context.active_object.data
            posaxis = [int(paxis) for paxis in ("0", "1", "2") if paxis not in (self.axis, self.caxis)][0]
            verts = [vert.index for vert in mesh.vertices if vert.select == True]
            vmax = max([v.co[posaxis] for v in bpy.context.active_object.data.vertices if v.index in verts])
            vmin = min([v.co[posaxis] for v in bpy.context.active_object.data.vertices if v.index in verts])
            refpos = ((vmin+vmax)/2, vmax, vmin)[int(self.rpoint)]
            if context.space_data.transform_orientation == 'NORMAL':
                for v in bpy.context.active_object.data.vertices:
                    if v.index in verts:
                        v.co += (v.co[posaxis]-refpos) * mathutils.Vector((self.fnormx, self.fnormy, self.fnormz)) * math.tan(float(self.rdeg)*0.0174533)
            else:
                for v in bpy.context.active_object.data.vertices:
                    if v.index in verts:
                        v.co[int(self.caxis)] += (v.co[posaxis]-refpos) * math.tan(float(self.rdeg)*0.0174533)
            bpy.ops.object.mode_set(mode = "EDIT")
        return {'FINISHED'}



def register():
    bpy.utils.register_class(RotateConstrained)

def unregister():
    bpy.utils.unregister_class(RotateConstrained)




#########################################################################################################################
#########################################################################################################################
#########  AREWO  #######################################################################################################
#########  AREWO  #######################################################################################################


#bl_info = {
	#"name": "arewo",
	#"description": "Replicates Objects with their animation offset in time",
	#"author": "Frederik Steinmetz",
	#"version": (1, 0),
	#"blender": (2, 68, 0),
	#"location": "Toolshelf",
	#"warning": "This is an Alpha version", # used for warning icon and text in addons panel
	#"wiki_url": "",
	#"tracker_url": "http://www.blenderdiplom.com",
	#"category": "Animation"}

# Arewo Simple
def run_linear_offset(loops, offset_frames, random_range, offset_position, offset_rotation, create_parent):
	
	obj = bpy.context.active_object
	if create_parent: # if a parent needs to be created
		if obj.parent == None:
			bpy.ops.object.empty_add(type = "PLAIN_AXES", location = (0, 0, 0), layers = obj.layers)
			par = bpy.context.active_object
			par.name = "Arewo_Parent"
			obj.parent = par
		else:
			print("Your object already has a parent, this may cause problems.")
	# store original object data
	base_mesh = obj.data
	original_location = obj.matrix_world.to_translation()
	original_rotation = obj.rotation_euler
	
	for n in range(3): # Gets the true values for pos and rot in case of delta
		original_rotation[n] += obj.delta_rotation_euler[n]
	
	for i in range(loops): 
		# Creates parameters for the new object
		name = obj.name + str(i)
		new_object = bpy.data.objects.new(name, base_mesh)
		bpy.context.scene.objects.link(new_object) 
		new_object.layers = obj.layers
		# Offset in Time, Space and Scale
		new_object.location = original_location
		new_object.delta_location = new_object.delta_location + Vector(offset_position) * (i + 1) # without for loop
		
		for n in range(3): 
			new_object.delta_rotation_euler[n] = obj.rotation_euler[n] + offset_rotation[n] * (i + 1)
		# creates a random number in +/- half the given range 
		random_offset = int(round((random.random() - 0.5) * random_range))
		if offset_frames == 0:
			offset_time = round(random.random() * random_range)
		else:
			offset_time = offset_frames * (i + 1) + random_offset
		
		# Offset keyframes if Exist 
		if obj.animation_data != None: 
			new_action = obj.animation_data.action.copy()
			fcurves = new_action.fcurves
			print(i, ": random: ", random_offset, ", offset Time: ", offset_time)
			for curve in fcurves: 
				keyframePoints = curve.keyframe_points
				for keyframe in keyframePoints:
					keyframe.co[0] += offset_time 
					keyframe.handle_left[0] += offset_time
					keyframe.handle_right[0] += offset_time

			new_object.animation_data_create() 
			new_object.animation_data.action = new_action
		
		if create_parent: # if a parent object was created, the new object will be a child of it
			new_object.parent = par
	bpy.context.scene.update() # probably unnecessary, just in case though

##################################################################################

# Run Object Offset
def run_object_offset(loops, offset_frames, random_range, starting_frame, spacing, inherit_scale, inherit_rotation, create_parent, hide_render):
	# starting frame of the evaluation of the placer object animation
	bpy.context.scene.frame_set(starting_frame - spacing)
	#Temporarily storing obj as vars
	par = obj = bpy.context.active_object
	
	if obj.parent != None:
		print("Your object has a parenting relation, results could be unexpected")
	if create_parent: # creates a parent object, if needed
		bpy.ops.object.empty_add(type = "PLAIN_AXES", location = (0, 0, 0), layers = obj.layers)
		par = bpy.context.active_object
		par.name = "Arewo_Parent"
	
	placer = bpy.data.objects[bpy.context.scene.placer_object] 
	evaluated_frame = starting_frame
	obj_list = []
	for i in range(loops):
		# defines the parameters for the new object
		name_object = obj.name + "_" + str(i)
		empty_mesh = bpy.data.meshes.new("Empty_Mesh")
		obj_list.append(bpy.data.objects.new(name_object, empty_mesh))
		obj_list[i].layers = obj.layers
		bpy.context.scene.objects.link(obj_list[i])
		# sychnronize the parameters with the placer animation
		obj_list[i].location = placer.matrix_world.to_translation()
		if inherit_scale: 
			obj_list[i].delta_scale = placer.matrix_world.to_scale()
		if inherit_rotation:
			obj_list[i].delta_rotation_euler = placer.matrix_world.to_euler()
		# creates a random number in +/- half the given range 
		
		random_offset = int(round((random.random() - 0.5) * random_range))
		if offset_frames == 0:
			offset_time = round(random.random() * random_range)
		else:
			random_offset = int(round((random.random() - 0.5) * random_range))
			offset_time = offset_frames * i + random_offset	  
		
		if obj.animation_data != None: # Offset keyframes - if Exist
			if obj.animation_data.action != None: # Offset keyframes - if Exist
				new_action = bpy.data.actions.new(obj.animation_data.action.name + str(i))
				# creates a copy of the original action
				new_action = obj.animation_data.action.copy()
				# offsets the keyframes by the calculated value
				fcurves = new_action.fcurves
				for curve in fcurves: 
					keyframePoints = curve.keyframe_points
					for keyframe in keyframePoints:
						keyframe.co[0] += offset_time 
						keyframe.handle_left[0] += offset_time
						keyframe.handle_right[0] += offset_time

				obj_list[i].animation_data_create()
				obj_list[i].animation_data.action = new_action

		if create_parent:
			obj_list[i].parent = par
		# evaluates the next frame of the placer animation
		evaluated_frame += spacing
		bpy.context.scene.frame_set(evaluated_frame)
	for me in obj_list:
		me.data = obj.data
	if hide_render:
		obj.hide_render = True
		obj.parent = None
	bpy.context.scene.update()
##################################################################################
# Arewo Experimental
def run_with_armature(loops, offset_frames, random_range, starting_frame, spacing, inherit_rotation, inherit_scale, mute_mods, hide_render):
	if mute_mods:
		run_mute_modifiers()
	else:
		run_enable_modifiers()

	bpy.context.scene.frame_set(starting_frame - spacing) # moves in time to evaluate placer location
	placer = bpy.data.objects[bpy.context.scene.placer_object]
	par = obj = original_obj = arm = placer # temp storing objects
	kinder = bpy.context.selected_objects # stores selected objects
	offset_time = offset_frames
	temp_location = obj.location # For placing the original at it's original location

	# determines which is the armature 
	armcount = 0
	for ob in kinder:
		ob.hide_render = False # in case they got hidden in the last run
		if ob.type == 'ARMATURE': 
			original_arm = ob 
			temp_location = original_arm.location # not working, gets changed everytime you change a parameter, should not be the case...
			armcount += 1
			if armcount > 1: # checks if there's already an armature in the selected objec
				print("Using multiple armatures can be problematic")
	evaluated_frame = starting_frame
	bpy.context.scene.frame_set(evaluated_frame)
	original_arm.location = placer.matrix_world.to_translation()
	if inherit_rotation:
		original_arm.delta_rotation_euler = placer.matrix_world.to_euler()
	if inherit_scale:
	#   original_arm.delta_scale = placer.matrix_world.to_scale() # give weird results for negative scales
		for n in range(3):
			original_arm.delta_scale[n] = placer.scale[n]

	# For loop starts
	for i in range(loops):
		evaluated_frame += spacing
		bpy.context.scene.frame_set(evaluated_frame) # advances in time to evaluate placer location 
		
		bpy.ops.object.select_all(action = 'DESELECT') # They will only be addressed directly
		for ob in kinder:
			ob.select = True		

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":True})
		for ob in bpy.context.selected_objects: # determine the copy of the armature
			if ob.type == 'ARMATURE':
				arm = ob
		bpy.ops.object.make_single_user( # Makes the animation data a single user
			type = 'SELECTED_OBJECTS', 
			object = False, 
			obdata = False, 
			material = False, 
			texture = False, 
			animation = True
			)
		# Determining how many frammes the animation needs to be offset
		if offset_frames == 0:
			offset_time = round(random.random() * random_range)
		else: # creates a random number in +/- half the given range
			random_offset = int(round((random.random() - 0.5) * random_range))
			offset_time = offset_frames * i + random_offset
	
		original_arm.location = placer.matrix_world.to_translation()
		if inherit_rotation:
			original_arm.delta_rotation_euler = placer.matrix_world.to_euler()
		if inherit_scale:
			for n in range(3):
				original_arm.delta_scale[n] = placer.scale[n]
		# Offset the animation if there is one
		if arm.animation_data != None:
			if arm.animation_data.action != None: # Previously deleted actions still get stored in animation data, so double check
				animData = arm.animation_data
				action = animData.action
				fcurves = action.fcurves
				for curve in fcurves: 
					keyframePoints = curve.keyframe_points
					for keyframe in keyframePoints:
						keyframe.co[0] += offset_time
						keyframe.handle_left[0] += offset_time
						keyframe.handle_right[0] += offset_time
			 
	# END FOR LOOP
	# hides the original objects
	if hide_render:
		for ob in kinder:
			ob.hide_render = True
	bpy.context.scene.update()

# helper function
def layer(n):
	return (n - 1) * [False] + [True] + (20 - n) * [False]

# function to temporarily disable all but the armature modifiers - for performance increas, duh
def run_mute_modifiers():
	objects = bpy.context.selected_objects
	for ob in objects:
		for mod in ob.modifiers:
			if mod.type != 'ARMATURE':
				mod.show_viewport = False

# function to reenable all modifiers
def run_enable_modifiers():
	objects = bpy.context.selected_objects
	for ob in objects:
		for mod in ob.modifiers:
			mod.show_viewport = True
# Able to apply a modifier and transfers the changes to all objects sharing this datablock
def apply_for_multi(remove_existing, remove_same):
	users = []
	success = False
	mod_type = 'ARMATURE' # temp storing modifier name
	original = bpy.context.active_object
	for ob in bpy.data.objects:
		ob.select = False
		if ob.data == original.data:
			users.append(ob)
	
	original.select = True
	bpy.ops.object.make_single_user(object = True, obdata = True)
	try:
		mod_type = original.modifiers[0].type
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier = original.modifiers[0].name)
		success = True
	except: 
		print("No modifiers found on this object, doing nothing")
	if success:
		for obj in users:
			obj.data = original.data
			if remove_existing:
				for mod in obj.modifiers:
					obj.modifiers.remove(mod)
			elif remove_same:
				for mod in obj.modifiers:
					if mod.type == mod_type:
						obj.modifiers.remove(mod)



# ----------------------------- Operators ------------------------------
# Operator Arewo simple
class arewo_simple(bpy.types.Operator):
	bl_idname = "anim.arewo_simple"
	bl_label = "Linear Offset"
	bl_description = "Linear version, only allows for limited options, only one object, no modifiers supported"
	bl_options = {'REGISTER', 'UNDO'}
	# Defining the adjustable parameters
	loops = bpy.props.IntProperty(
			name = "Iterations",
			default = 2,
			min = 1,
			max = 10000,
			description = "Number of copies to be generated."
			)
	offset_frames = bpy.props.IntProperty(
			name = "Offset Frames",
			default = 10,
			min = 0,
			max = 10000,
			description = "Offset for the animation in frames"
			)
	random_offset = bpy.props.IntProperty(
			name = "Random Offset",
			default = 0,
			min = 0,
			max = 10000,
			description = "Random offset for the animation in frames"
			)
	offset_position = bpy.props.FloatVectorProperty(
			name = "Location Offset",
			default = (1, 0, 0),
			subtype = 'TRANSLATION',
			description = "Linear location offset"
			)
	offset_rotation = bpy.props.FloatVectorProperty(
			name = "Rotation Offset",
			default = (0, 0, 0),
			subtype = 'EULER',
			description = "Rotation offset"
			)
	create_parent = bpy.props.BoolProperty(
			name = "Create Parent", 
			default = False,
			description = "Create a parent object for all added objects"
			)
	def execute(self, context): 
		run_linear_offset(
				self.loops, 
				self.offset_frames, 
				self.random_offset, 
				self.offset_position, 
				self.offset_rotation, 
				self.create_parent
				)
		return {'FINISHED'}


##################################################################################


# Operator arewo Offset Object 
class arewo_object_offset(bpy.types.Operator):
	bl_idname = "anim.arewo_object_offset"
	bl_label = "Object Offset"
	bl_description = "Allows great control via a placer object. Only one object, no modifiers supported"
	bl_options = {'REGISTER', 'UNDO'}
	loops = bpy.props.IntProperty(
			name = "Iterations",
			default = 2,
			min = 1,
			max = 10000,
			description = "Number of copies to be generated."
			)
	offset_frames = bpy.props.IntProperty(
			name = "Offset Frames",
			default = 10,
			min = 0,
			max = 10000,
			description = "Offset for the animation in frames"
			)
	random_offset = bpy.props.IntProperty(
			name = "Random Offset",
			default = 0,
			min = 0,
			max = 10000,
			description = "Random offset for the animation in frames"
			)
	starting_frame = bpy.props.IntProperty(
			name = "Start Frame",
			default = 1,
			min = 0,
			max = 10000,
			description = "Starting time of the path / animation for the placer object"
			)
	spacing = bpy.props.IntProperty(
			name = "Spacing",
			default = 1,
			min = 0,
			max = 1000,
			description = "Skipped frames in path / animation for the placer object"
			)
	inherit_scale = bpy.props.BoolProperty(
			name = "Inherit Scale", 
			default = False,
			description = "Also copies the scale of the placer object"
			)
	inherit_rotation = bpy.props.BoolProperty(
			name = "Inherit Rotation", 
			default = False,
			description = "Also copies the rotation of the placer object"
			)
	create_parent = bpy.props.BoolProperty(
			name = "Create Parent", 
			default = False,
			description = "Create a parent object for all added objects"
			)
	hide_render = bpy.props.BoolProperty(
			name = "Hide Render", 
			default = True,
			description = "Keeps the original object from being rendered"
	)
	def execute(self, context): 
		run_object_offset(
			self.loops, 
			self.offset_frames, 
			self.random_offset,
			self.starting_frame, 
			self.spacing,
			self.inherit_scale,
			self.inherit_rotation,
			self.create_parent,
			self.hide_render
			)
		return {'FINISHED'} 




##################################################################################


# Operator Armature Offset


class arewo_advanced(bpy.types.Operator):
	bl_idname = "anim.arewo_armature_offset"
	bl_label = "Armature Offset"
	bl_description = "Allows great control via a placer object. Multiple objects and armature supported"
	bl_options = {'REGISTER', 'UNDO'}
	loops = bpy.props.IntProperty(
			name = "Iterations",
			default = 2,
			min = 1,
			max = 10000,
			description = "Number of copies to be generated."
			)
	offset_frames = bpy.props.IntProperty(
			name = "Offset Frames",
			default = 10,
			min = 0,
			max = 10000,
			description = "Offset for the animation in frames"
			)
	random_offset = bpy.props.IntProperty(
			name = "Random Offset",
			default = 0,
			min = 0,
			max = 1000,
			description = "Random offset for the animation in frames"
			)
	starting_frame = bpy.props.IntProperty(
			name = "Start Frame",
			default = 1,
			min = 0,
			max = 10000,
			description = "Starting time of the path / animation for the placer object"
			)
	spacing = bpy.props.IntProperty(
			name = "Spacing",
			default = 1,
			min = 1,
			max = 10000,
			description = "Offset for the animation in frames"
			)
	inherit_scale = bpy.props.BoolProperty(
			name = "Inherit Scale", 
			default = False,
			description = "Makes the copies the same scale as the placer object at the evaluated frame"
			)
	inherit_rotation = bpy.props.BoolProperty(
			name = "Inherit Rotation", 
			default = False,
			description = "Gives the copies the same rotation as the placer object at the evaluated frame"
			)
	mute_mods = bpy.props.BoolProperty(
			name = "Mute Modifiers",
			default = False,
			description = "Temporarily hide modifiers, you can reenable them by using the Enable Modifiers button from the Speed Up Tools",
			) 
	hide_render = bpy.props.BoolProperty(
			name = "Hide Render", 
			default = True,
			description = "Keeps the original object from being rendered"
	)
	def execute(self, context): 
		run_with_armature(
			self.loops, 
			self.offset_frames, 
			self.random_offset, 
			self.starting_frame, 
			self.spacing,
			self.inherit_rotation, 
			self.inherit_scale,
			self.mute_mods,
			self.hide_render
			)
		return {'FINISHED'} 




################################################################################################################


class mute_modifiers(bpy.types.Operator):
	bl_idname = "object.mute_modifiers"
	bl_label = "Mute Modifiers"
	bl_description = "Shuts off Viewport visibility of every modifier of the selected objects that is not an Armature"
	bl_options = {'REGISTER', 'UNDO'} 
	def execute(self, context):
		run_mute_modifiers()
		return {'FINISHED'} 
 


class enable_modifiers(bpy.types.Operator):
	bl_idname = "object.enable_modifiers"
	bl_label = "Enable Modifiers"
	bl_description = "Enables Viewport visibility of all modifiers of the selected objects"
	bl_options = {'REGISTER', 'UNDO'} 
	def execute(self, context):
		run_enable_modifiers()
		return {'FINISHED'}



class apply_modifier_for_multi(bpy.types.Operator):
	bl_idname = "object.apply_modifier_for_multi"
	bl_label = "Apply Modifier"
	bl_description = "Applies the 1. Modifier of the selected objects and passes the changes to all objects sharing the same datablock"
	bl_options = {'REGISTER', 'UNDO'}
	remove_existing = bpy.props.BoolProperty(
			name = "Remove Existing", 
			default = False,
			description = "Removes all modifiers from objects with the same datablock"
	)   
	remove_same = bpy.props.BoolProperty(
			name = "Remove Same Type", 
			default = True,
			description = "Removes modifiers with the same type as the applied one from objects"
	)   
	def execute(self, context):
		apply_for_multi(
			self.remove_existing, 
			self.remove_same
			)
		return {'FINISHED'} 





###############################################################################################################################
###############################################################################################################################
###### Display Tools ##########################################################################################################
###### Display Tools ##########################################################################################################

#bl_info = {
    #"name": "Display Tools",
    #"author": "Jordi Vall-llovera Medina",
    #"version": (1, 5, 5),
    #"blender": (2, 6, 7),
    #"location": "Toolshelf",
    #"description": "Display tools for fast navigate/interact with the viewport",
    #"warning": "",
    #"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/\
    #3D_interaction/Display_Tools",
    #"tracker_url": "",
    #"category": "3D View"}

"""
#Additional links:
   #Author Site: http://jordiart3d.blogspot.com.es/
"""

import bpy

from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty

# init delay variables
bpy.types.Scene.Delay = bpy.props.BoolProperty(
        default = False,
        description = "Activate delay return to normal viewport mode")

bpy.types.Scene.DelayTime = bpy.props.IntProperty(
        default = 30,
        min = 1,
        max = 500,
        soft_min = 10,
        soft_max = 250,
        description = "Delay time to return to normal viewport\
         mode after move your mouse cursor")

bpy.types.Scene.DelayTimeGlobal = bpy.props.IntProperty(
        default = 30,
        min = 1,
        max = 500,
        soft_min = 10,
        soft_max = 250,
        description = "Delay time to return to normal viewport\
         mode after move your mouse cursor")

#init variable for fast navigate
bpy.types.Scene.EditActive = bpy.props.BoolProperty(
        default = True,
        description = "Activate for fast navigate in edit mode too")

#Fast Navigate toggle function
def trigger_fast_navigate(trigger):
    scene = bpy.context.scene
    scene.FastNavigateStop = False
    
    if trigger == True:
        trigger = False
    else:
        trigger = True

#Control how to display particles during fast navigate
def display_particles(mode):
    scene = bpy.context.scene
    
    if mode == True:
        for particles in bpy.data.particles:
            if particles.type == 'EMITTER':
                particles.draw_method = 'DOT'
                particles.draw_percentage = 100
            else:
                particles.draw_method = 'RENDER'  
                particles.draw_percentage = 100
    else:
        for particles in bpy.data.particles:
            if particles.type == 'EMITTER':
                particles.draw_method = 'DOT'
                particles.draw_percentage = scene.ParticlesPercentageDisplay
            else:
                particles.draw_method = 'RENDER'  
                particles.draw_percentage = scene.ParticlesPercentageDisplay

#Do repetitive fast navigate related stuff         
def fast_navigate_stuff(self, context, event):    
    scene = bpy.context.scene
    view = context.space_data
        
    if bpy.context.area.type != 'VIEW_3D':
        return self.cancel(context)    
                          
    if event.type == 'ESC' or event.type == 'RET' or event.type == 'SPACE':
        return self.cancel(context)
     
    if scene.FastNavigateStop == True:
        return self.cancel(context)    
    
    #fast navigate while orbit/panning
    if event.type == 'MIDDLEMOUSE':
        if scene.Delay == True:
            if scene.DelayTime < scene.DelayTimeGlobal:
                scene.DelayTime += 1
        view.viewport_shade = scene.FastMode
        self.mode = False
        
    #fast navigate while transform operations
    if event.type == 'G' or event.type == 'R' or event.type == 'S': 
        if scene.Delay == True:
            if scene.DelayTime < scene.DelayTimeGlobal:
                scene.DelayTime += 1
        view.viewport_shade = scene.FastMode
        self.mode = False
     
    #fast navigate while menu popups or duplicates  
    if event.type == 'W' or event.type == 'D' or event.type == 'L'\
        or event.type == 'U' or event.type == 'I' or event.type == 'M'\
        or event.type == 'A' or event.type == 'B': 
        if scene.Delay == True:
            if scene.DelayTime < scene.DelayTimeGlobal:
                scene.DelayTime += 1
        view.viewport_shade = scene.FastMode
        self.mode = False
    
    #fast navigate while numpad navigation
    if event.type == 'NUMPAD_PERIOD' or event.type == 'NUMPAD_1'\
        or event.type == 'NUMPAD_2' or event.type == 'NUMPAD_3'\
        or event.type == 'NUMPAD_4' or event.type == 'NUMPAD_5'\
        or event.type == 'NUMPAD_6' or event.type == 'NUMPAD_7'\
        or event.type == 'NUMPAD_8' or event.type == 'NUMPAD_9': 
        if scene.Delay == True:
            if scene.DelayTime < scene.DelayTimeGlobal:
                scene.DelayTime += 1
        view.viewport_shade = scene.FastMode
        self.mode = False
        
    #fast navigate while zooming with mousewheel too
    if event.type == 'WHEELUPMOUSE' or event.type == 'WHEELDOWNMOUSE':
        scene.DelayTime = scene.DelayTimeGlobal
        view.viewport_shade = scene.FastMode
        self.mode = False
        
    if event.type == 'MOUSEMOVE': 
        if scene.Delay == True:
            if scene.DelayTime == 0:
                scene.DelayTime = scene.DelayTimeGlobal
                view.viewport_shade = scene.OriginalMode 
                self.mode = True
        else:
            view.viewport_shade = scene.OriginalMode 
            self.mode = True
    
    if scene.Delay == True:
        scene.DelayTime -= 1   
        if scene.DelayTime == 0:
            scene.DelayTime = scene.DelayTimeGlobal
            view.viewport_shade = scene.OriginalMode 
            self.mode = True
        
    if scene.ShowParticles == False:
        for particles in bpy.data.particles:
            if particles.type == 'EMITTER':
                particles.draw_method = 'NONE'
            else:
                particles.draw_method = 'NONE'    
    else:
        display_particles(self.mode)   
    
#Fast Navigate operator
class FastNavigate(bpy.types.Operator):
    """Operator that runs Fast navigate in modal mode"""
    bl_idname = "view3d.fast_navigate_operator"
    bl_label = "Fast Navigate"
    trigger = BoolProperty(default = False)
    mode = BoolProperty(default = False)

    def modal(self, context, event):     
        scene = bpy.context.scene
        view = context.space_data
        
        if scene.EditActive == True:     
            fast_navigate_stuff(self, context ,event)
            return {'PASS_THROUGH'}       
        else:
            obj = context.active_object
            if obj: 
                if obj.mode != 'EDIT':
                    fast_navigate_stuff(self, context ,event)
                    return {'PASS_THROUGH'}            
                else:
                    return {'PASS_THROUGH'}        
            else:
                fast_navigate_stuff(self, context ,event)
                return {'PASS_THROUGH'}
     
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        trigger_fast_navigate(self.trigger)
        scene = bpy.context.scene
        scene.DelayTime = scene.DelayTimeGlobal
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        scene = context.scene
        for particles in bpy.data.particles:
            particles.draw_percentage = scene.InitialParticles
        return {'CANCELLED'}

#Fast Navigate Stop
def fast_navigate_stop(context):
    scene = bpy.context.scene
    scene.FastNavigateStop = True

#Fast Navigate Stop Operator
class FastNavigateStop(bpy.types.Operator):
    '''Stop Fast Navigate Operator'''
    bl_idname = "view3d.fast_navigate_stop"
    bl_label = "Stop"    
    FastNavigateStop = IntProperty(name = "FastNavigateStop", 
		description = "Stop fast navigate mode",
		default = 0)

    def execute(self,context):
        fast_navigate_stop(context)
        return {'FINISHED'}
    
#Drawtype textured
def draw_textured(context):   
    view = context.space_data
    view.viewport_shade = 'TEXTURED'
    bpy.context.scene.game_settings.material_mode = 'GLSL'
    selection = bpy.context.selected_objects  
    
    if not(selection):
        for obj in bpy.data.objects:
            obj.draw_type = 'TEXTURED'
    else:
        for obj in selection:
            obj.draw_type = 'TEXTURED' 
    
class DisplayTextured(bpy.types.Operator):
    '''Display objects in textured mode'''
    bl_idname = "view3d.display_textured"
    bl_label = "Textured"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        draw_textured(context)
        return {'FINISHED'}
    
#Drawtype solid
def draw_solid(context):
    view = context.space_data
    view.viewport_shade = 'TEXTURED'
    bpy.context.scene.game_settings.material_mode = 'GLSL'
    selection = bpy.context.selected_objects 
    
    if not(selection):
        for obj in bpy.data.objects:
            obj.draw_type = 'SOLID'
    else:
        for obj in selection:
            obj.draw_type = 'SOLID'

class DisplaySolid(bpy.types.Operator):
    '''Display objects in solid mode'''
    bl_idname = "view3d.display_solid"
    bl_label = "Solid"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        draw_solid(context)
        return {'FINISHED'}
    
#Drawtype wire
def draw_wire(context):
    view = context.space_data
    view.viewport_shade = 'TEXTURED'
    bpy.context.scene.game_settings.material_mode = 'GLSL'
    selection = bpy.context.selected_objects 
    
    if not(selection):
        for obj in bpy.data.objects:
            obj.draw_type = 'WIRE'
    else:
        for obj in selection:
            obj.draw_type = 'WIRE'

class DisplayWire(bpy.types.Operator):
    '''Display objects in wireframe mode'''
    bl_idname = "view3d.display_wire"
    bl_label = "Wire"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        draw_wire(context)
        return {'FINISHED'}
    
#Drawtype bounds
def draw_bounds(context):
    view = context.space_data
    view.viewport_shade = 'TEXTURED'
    bpy.context.scene.game_settings.material_mode = 'GLSL'
    selection = bpy.context.selected_objects 
    
    if not(selection):
        for obj in bpy.data.objects:
            obj.draw_type = 'BOUNDS'
    else:
        for obj in selection:
            obj.draw_type = 'BOUNDS'

class DisplayBounds(bpy.types.Operator):
    '''Display objects in bounds mode'''
    bl_idname = "view3d.display_bounds"
    bl_label = "Bounds"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        draw_bounds(context)
        return {'FINISHED'}

#Shade smooth
def shade_smooth(context):
    selection = bpy.context.selected_objects   
    
    if not(selection): 
        for obj in bpy.data.objects:
            bpy.ops.object.select_all(action = 'TOGGLE')
            bpy.ops.object.shade_smooth()
            bpy.ops.object.select_all(action = 'TOGGLE')               
    else:
        obj = context.active_object
        if obj.mode == 'OBJECT':
            for obj in selection:
                bpy.ops.object.shade_smooth()
        else:
            bpy.ops.mesh.faces_shade_smooth()

class DisplayShadeSmooth(bpy.types.Operator):
    '''Display shade smooth meshes'''
    bl_idname = "view3d.display_shade_smooth"
    bl_label = "Smooth"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shade_smooth(context)
        return {'FINISHED'}
    
#Shade flat
def shade_flat(context):
    selection = bpy.context.selected_objects 
      
    if not(selection): 
        for obj in bpy.data.objects:
            bpy.ops.object.select_all(action = 'TOGGLE')
            bpy.ops.object.shade_flat()
            bpy.ops.object.select_all(action = 'TOGGLE')
    else:
        obj = context.active_object
        if obj.mode == 'OBJECT':
            for obj in selection:
                bpy.ops.object.shade_flat()
        else:
            bpy.ops.mesh.faces_shade_flat()    

class DisplayShadeFlat(bpy.types.Operator):
    '''Display shade flat meshes'''
    bl_idname = "view3d.display_shade_flat"
    bl_label = "Flat"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shade_flat(context)
        return {'FINISHED'}
    
#Shadeless on
def shadeless_on(context):
    selection = bpy.context.selected_objects
    
    if not(selection): 
        for obj in bpy.data.materials:
            obj.use_shadeless = True
    else:
        for sel in selection:
            if sel.type == 'MESH':
                materials = sel.data.materials
                for mat in materials:
                    mat.use_shadeless = True  
            
class DisplayShadelessOn(bpy.types.Operator):
    '''Display shadeless material'''
    bl_idname = "view3d.display_shadeless_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shadeless_on(context)
        return {'FINISHED'}
    
#Shadeless off
def shadeless_off(context):
    selection = bpy.context.selected_objects
    
    if not(selection): 
        for obj in bpy.data.materials:
            obj.use_shadeless = False
    else:
        for sel in selection:
            if sel.type == 'MESH':
                materials = sel.data.materials
                for mat in materials:
                    mat.use_shadeless = False   

class DisplayShadelessOff(bpy.types.Operator):
    '''Display shaded material'''
    bl_idname = "view3d.display_shadeless_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shadeless_off(context)
        return {'FINISHED'}

#Wireframe on
def wire_on(context):
    selection = bpy.context.selected_objects  
     
    if not(selection): 
        for obj in bpy.data.objects:
            obj.show_wire = True
            obj.show_all_edges = True
            
    else:
        for obj in selection:
            obj.show_wire = True
            obj.show_all_edges = True 

class DisplayWireframeOn(bpy.types.Operator):
    '''Display wireframe overlay on'''
    bl_idname = "view3d.display_wire_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        wire_on(context)
        return {'FINISHED'}
    
#Wireframe off
def wire_off(context):
    selection = bpy.context.selected_objects  
    
    if not(selection): 
        for obj in bpy.data.objects:
            obj.show_wire = False
            obj.show_all_edges = False
            
    else:
        for obj in selection:
            obj.show_wire = False
            obj.show_all_edges = False   

class DisplayWireframeOff(bpy.types.Operator):
    '''Display wireframe overlay off'''
    bl_idname = "view3d.display_wire_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        wire_off(context)
        return {'FINISHED'}

#Bounds on
def bounds_on(context):
    scene = context.scene
    selection = bpy.context.selected_objects 
      
    if not(selection): 
        for obj in bpy.data.objects:
            obj.show_bounds = True
            obj.draw_bounds_type = scene.BoundingMode 
    else:
        for obj in selection:
            obj.show_bounds = True
            obj.draw_bounds_type = scene.BoundingMode                 

class DisplayBoundsOn(bpy.types.Operator):
    '''Display Bounding box overlay on'''
    bl_idname = "view3d.display_bounds_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bounds_on(context)
        return {'FINISHED'}
    
#Wireframe off
def bounds_off(context):
    scene = context.scene
    selection = bpy.context.selected_objects 
     
    if not(selection): 
        for obj in bpy.data.objects:
            obj.show_bounds = False
    else:
        for obj in selection:
            obj.show_bounds = False    

class DisplayBoundsOff(bpy.types.Operator):
    '''Display Bounding box overlay off'''
    bl_idname = "view3d.display_bounds_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bounds_off(context)
        return {'FINISHED'}
    
#Double Sided on
def double_sided_on(context):
    selection = bpy.context.selected_objects
    
    if not(selection):
        for mesh in bpy.data.meshes:
            mesh.show_double_sided = True
    else:
        for sel in selection:
            if sel.type == 'MESH':
                mesh = sel.data
                mesh.show_double_sided = True        

class DisplayDoubleSidedOn(bpy.types.Operator):
    '''Turn on face double shaded mode'''
    bl_idname = "view3d.display_double_sided_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        double_sided_on(context)
        return {'FINISHED'}
    
#Double Sided off
def double_sided_off(context):
    selection = bpy.context.selected_objects
    
    if not(selection):
        for mesh in bpy.data.meshes:
            mesh.show_double_sided = False
    else:
        for sel in selection:
            if sel.type == 'MESH':
                mesh = sel.data
                mesh.show_double_sided = False 

class DisplayDoubleSidedOff(bpy.types.Operator):
    '''Turn off face double sided shade mode'''
    bl_idname = "view3d.display_double_sided_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        double_sided_off(context)
        return {'FINISHED'}
    
#XRay on
def x_ray_on(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):  
        for obj in bpy.data.objects:
            obj.show_x_ray = True
    else:
        for obj in selection:
            obj.show_x_ray = True        

class DisplayXRayOn(bpy.types.Operator):
    '''X-Ray display on'''
    bl_idname = "view3d.display_x_ray_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        x_ray_on(context)
        return {'FINISHED'}
    
#XRay off
def x_ray_off(context):
    selection = bpy.context.selected_objects  
              
    if not(selection):  
        for obj in bpy.data.objects:
            obj.show_x_ray = False
    else:
        for obj in selection:
            obj.show_x_ray = False  

class DisplayXRayOff(bpy.types.Operator):
    '''X-Ray display off'''
    bl_idname = "view3d.display_x_ray_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        x_ray_off(context)
        return {'FINISHED'}
    
#Init properties for scene
bpy.types.Scene.FastNavigateStop = bpy.props.BoolProperty(
        name = "Fast Navigate Stop", 
        description = "Stop fast navigate mode",
        default = False)

bpy.types.Scene.OriginalMode = bpy.props.EnumProperty(
        items = [('TEXTURED', 'Texture', 'Texture display mode'), 
            ('SOLID', 'Solid', 'Solid display mode')], 
        name = "Normal",
        default = 'SOLID')

bpy.types.Scene.BoundingMode = bpy.props.EnumProperty(
        items = [('BOX', 'Box', 'Box shape'), 
            ('SPHERE', 'Sphere', 'Sphere shape'),
            ('CYLINDER', 'Cylinder', 'Cylinder shape'),
            ('CONE', 'Cone', 'Cone shape')], 
        name = "BB Mode")

bpy.types.Scene.FastMode = bpy.props.EnumProperty(
        items = [('WIREFRAME', 'Wireframe', 'Wireframe display'), 
            ('BOUNDBOX', 'Bounding Box', 'Bounding Box display')], 
        name = "Fast")
        
bpy.types.Scene.ShowParticles = bpy.props.BoolProperty(
        name = "Show Particles", 
        description = "Show or hide particles on fast navigate mode",
		default = True)

bpy.types.Scene.ParticlesPercentageDisplay = bpy.props.IntProperty(
        name = "Display", 
        description = "Display only a percentage of particles",
		default = 25,
        min = 0,
        max = 100,
        soft_min = 0,
        soft_max = 100,
        subtype = 'FACTOR')
    
bpy.types.Scene.InitialParticles = bpy.props.IntProperty(
        name = "Count for initial particle setting before enter fast navigate", 
        description = "Display a percentage value of particles",
		default = 100,
        min = 0,
        max = 100,
        soft_min = 0,
        soft_max = 100)

#Set Render Settings
def set_render_settings(conext):
    scene = bpy.context.scene
    render = bpy.context.scene.render
    view = bpy.context.space_data
    render.simplify_subdivision = 0
    render.simplify_shadow_samples = 0
    render.simplify_child_particles = 0
    render.simplify_ao_sss = 0

class DisplaySimplify(bpy.types.Operator):
    '''Display scene simplified'''
    bl_idname = "view3d.display_simplify"
    bl_label = "Reset"
    
    Mode = EnumProperty(
        items = [('WIREFRAME', 'Wireframe', ''), 
            ('BOUNDBOX', 'Bounding Box', '')], 
        name = "Mode")
        
    ShowParticles = BoolProperty(
        name = "ShowParticles", 
        description = "Show or hide particles on fast navigate mode",
		default = True)
    
    ParticlesPercentageDisplay = IntProperty(
        name = "Display", 
        description = "Display a percentage value of particles",
		default = 25,
        min = 0,
        max = 100,
        soft_min = 0,
        soft_max = 100,
        subtype = 'FACTOR')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        set_render_settings(context)
        return {'FINISHED'}

#Display Modifiers Render on
def modifiers_render_on(context):    
    scene = bpy.context.scene
    bpy.types.Scene.Symplify = IntProperty(
    name = "Integer",description = "Enter an integer")
    scene['Simplify'] = 1    
    selection = bpy.context.selected_objects  
    
    if not(selection):   
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_render = True
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_render = True
            
class DisplayModifiersRenderOn(bpy.types.Operator):
    '''Display modifiers in render'''
    bl_idname = "view3d.display_modifiers_render_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_render_on(context)
        return {'FINISHED'}
    
#Display Modifiers Render off
def modifiers_render_off(context):
    selection = bpy.context.selected_objects  
    
    if not(selection):   
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_render = False
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_render = False

class DisplayModifiersRenderOff(bpy.types.Operator):
    '''Hide modifiers in render'''
    bl_idname = "view3d.display_modifiers_render_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_render_off(context)
        return {'FINISHED'}
    
#Display Modifiers Viewport on
def modifiers_viewport_on(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_viewport = True
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_viewport = True
        
class DisplayModifiersViewportOn(bpy.types.Operator):
    '''Display modifiers in viewport'''
    bl_idname = "view3d.display_modifiers_viewport_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_viewport_on(context)
        return {'FINISHED'}
    
#Display Modifiers Viewport off
def modifiers_viewport_off(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_viewport = False
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_viewport = False

class DisplayModifiersViewportOff(bpy.types.Operator):
    '''Hide modifiers in viewport'''
    bl_idname = "view3d.display_modifiers_viewport_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_viewport_off(context)
        return {'FINISHED'}
    
#Display Modifiers Edit on
def modifiers_edit_on(context):
    selection = bpy.context.selected_objects 
      
    if not(selection):  
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_in_editmode = True
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_in_editmode = True

class DisplayModifiersEditOn(bpy.types.Operator):
    '''Display modifiers during edit mode'''
    bl_idname = "view3d.display_modifiers_edit_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_edit_on(context)
        return {'FINISHED'}
    
#Display Modifiers Edit off
def modifiers_edit_off(context):
    selection = bpy.context.selected_objects  
     
    if not(selection):  
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_in_editmode = False
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_in_editmode = False

class DisplayModifiersEditOff(bpy.types.Operator):
    '''Hide modifiers during edit mode'''
    bl_idname = "view3d.display_modifiers_edit_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_edit_off(context)
        return {'FINISHED'}


#Display Modifiers Clipping On    
class DisplayModifiersclipOn(bpy.types.Operator):
    '''Display modifiers clipping'''
    bl_idname = "view3d.display_modifiers_clip_on"
    bl_label = "On"

    def execute(self, context):
        bpy.context.object.modifiers["Mirror"].use_clip = True
        return {'FINISHED'}
		

#Display Modifiers Clipping Off  
class DisplayModifiersclipOFF(bpy.types.Operator):
    '''Display modifiers clipping'''
    bl_idname = "view3d.display_modifiers_clip_on"
    bl_label = "On"

    def execute(self, context):
        bpy.context.object.modifiers["Mirror"].use_clip = False
        return {'FINISHED'}



#Display Modifiers Cage on
def modifiers_cage_on(context):
    selection = bpy.context.selected_objects  
      
    if not(selection): 
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_on_cage = True
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_on_cage = True

class DisplayModifiersCageOn(bpy.types.Operator):
    '''Display modifiers editing cage during edit mode'''
    bl_idname = "view3d.display_modifiers_cage_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_cage_on(context)
        return {'FINISHED'}
    
#Display Modifiers Cage off
def modifiers_cage_off(context):
    selection = bpy.context.selected_objects 
       
    if not(selection): 
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_on_cage = False
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_on_cage = False

class DisplayModifiersCageOff(bpy.types.Operator):
    '''Hide modifiers editing cage during edit mode'''
    bl_idname = "view3d.display_modifiers_cage_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_cage_off(context)
        return {'FINISHED'}
    
#Display Modifiers Expand
def modifiers_expand(context):
    selection = bpy.context.selected_objects  
      
    if not(selection): 
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_expanded = True
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_expanded = True

class DisplayModifiersExpand(bpy.types.Operator):
    '''Expand all modifiers on modifier stack'''
    bl_idname = "view3d.display_modifiers_expand"
    bl_label = "Expand"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_expand(context)
        return {'FINISHED'}
    
#Display Modifiers Collapse
def modifiers_collapse(context):
    selection = bpy.context.selected_objects  
      
    if not(selection): 
        for obj in bpy.data.objects:        
            for mod in obj.modifiers:
                mod.show_expanded = False
    else:
        for obj in selection:        
            for mod in obj.modifiers:
                mod.show_expanded = False

class DisplayModifiersCollapse(bpy.types.Operator):
    '''Collapse all modifiers on modifier stack'''
    bl_idname = "view3d.display_modifiers_collapse"
    bl_label = "Collapse"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_collapse(context)
        return {'FINISHED'}
    
#Apply modifiers
def modifiers_apply(context):
    selection = bpy.context.selected_objects
    
    if not(selection):  
        bpy.ops.object.select_all(action = 'TOGGLE')
        bpy.ops.object.convert(target = 'MESH', keep_original = False)
        bpy.ops.object.select_all(action = 'TOGGLE')
    else:
        for mesh in selection:
            if mesh.type == "MESH":
                bpy.ops.object.convert(target='MESH', keep_original = False)
                
class DisplayModifiersApply(bpy.types.Operator):
    '''Apply modifiers'''
    bl_idname = "view3d.display_modifiers_apply"
    bl_label = "Apply All"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_apply(context)
        return {'FINISHED'}
    
#Delete modifiers
def modifiers_delete(context):
    selection = bpy.context.selected_objects
    
    if not(selection):  
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                bpy.context.scene.objects.active = obj
                bpy.ops.object.modifier_remove(modifier = mod.name)
    else:
        for obj in selection:
            for mod in obj.modifiers:
                bpy.context.scene.objects.active = obj
                bpy.ops.object.modifier_remove(modifier = mod.name)
                
class DisplayModifiersDelete(bpy.types.Operator):
    '''Delete modifiers'''
    bl_idname = "view3d.display_modifiers_delete"
    bl_label = "Delete All"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_delete(context)
        return {'FINISHED'}
    
#Put dummy modifier for boost subsurf
def modifiers_set_dummy(context):
    selection = bpy.context.selected_objects 
   
    if not(selection):             
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
            value = 0
            for mod in obj.modifiers:
                if mod != 0:
                  if mod.type == 'SIMPLE_DEFORM':
                    value = value +1
                    mod.factor = 0
                  if value > 1:
                      bpy.ops.object.modifier_remove(modifier="SimpleDeform")
    else:
        for obj in selection:
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SIMPLE_DEFORM':
                value = value +1
                mod.factor = 0
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="SimpleDeform")
                  
                  
#Delete dummy modifier 
def modifiers_delete_dummy(context):
    selection = bpy.context.selected_objects 
   
    if not(selection):             
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            for mod in obj.modifiers:
                  if mod.type == 'SIMPLE_DEFORM':
                      bpy.ops.object.modifier_remove(modifier="SimpleDeform")
                      bpy.ops.object.modifier_remove(modifier="SimpleDeform.001")
    else:
        for obj in selection:
            bpy.context.scene.objects.active = obj 
            for mod in obj.modifiers:
                  if mod.type == 'SIMPLE_DEFORM':
                      bpy.ops.object.modifier_remove(modifier="SimpleDeform") 
                      bpy.ops.object.modifier_remove(modifier="SimpleDeform.001")     
                                               
                  
class DisplayAddDummy(bpy.types.Operator):
    '''Add a dummy simple deform modifier to boost\
     subsurf modifier viewport performance'''
    bl_idname = "view3d.display_modifiers_set_dummy"
    bl_label = "Put Dummy"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_set_dummy(context)
        return {'FINISHED'}
    
class DisplayDeleteDummy(bpy.types.Operator):
    '''Delete a dummy simple deform modifier to boost\
    subsurf modifier viewport performance'''
    bl_idname = "view3d.display_modifiers_delete_dummy"
    bl_label = "Delete Dummy"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        modifiers_delete_dummy(context)
        return {'FINISHED'}
      
#Display subsurf level 0
def modifiers_subsurf_level_0(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 0
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
 
                
    else:
        for obj in selection:  
            bpy.ops.object.subdivision_set(level=0, relative=False)  
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                mod.levels = 0
              
                
#Display subsurf level 1
def modifiers_subsurf_level_1(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 1
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:
        for obj in selection:  
            bpy.ops.object.subdivision_set(level=1, relative=False)       
            for mod in obj.modifiers:
                if mod.type == 'SUBSURF':
                  mod.levels = 1
                
#Display subsurf level 2
def modifiers_subsurf_level_2(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 2
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:
        for obj in selection:        
            bpy.ops.object.subdivision_set(level=2, relative=False) 
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                mod.levels = 2
                
#Display subsurf level 3
def modifiers_subsurf_level_3(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):   
        for obj in bpy.data.objects:   
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 3
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:
        for obj in selection:          
            bpy.ops.object.subdivision_set(level=3, relative=False) 
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                mod.levels = 3

#Display subsurf level 4
def modifiers_subsurf_level_4(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 4
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:
        for obj in selection:        
            bpy.ops.object.subdivision_set(level=4, relative=False) 
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                mod.levels = 4
                
#Display subsurf level 5
def modifiers_subsurf_level_5(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):    
        for obj in bpy.data.objects:  
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 5
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:
        for obj in selection:        
            bpy.ops.object.subdivision_set(level=5, relative=False) 
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                mod.levels = 5

#Display subsurf level 6
def modifiers_subsurf_level_6(context):
    selection = bpy.context.selected_objects 
    
    if not(selection):  
        for obj in bpy.data.objects:    
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.modifier_add(type='SUBSURF')
            value = 0
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                value = value +1
                mod.levels = 6
              if value > 1:
                  bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:
        for obj in selection:        
            bpy.ops.object.subdivision_set(level=6, relative=False)    
            for mod in obj.modifiers:
              if mod.type == 'SUBSURF':
                mod.levels = 6

#main class of Display subsurf level 0           
class ModifiersSubsurfLevel_0(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_0"
    bl_label = "0"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_0(context)
        return {'FINISHED'}
      
#main class of Display subsurf level 1        
class ModifiersSubsurfLevel_1(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_1"
    bl_label = "1"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_1(context)
        return {'FINISHED'}
      
#main class of Display subsurf level 2           
class ModifiersSubsurfLevel_2(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_2"
    bl_label = "2"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_2(context)
        return {'FINISHED'}
      
#main class of Display subsurf level 3         
class ModifiersSubsurfLevel_3(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_3"
    bl_label = "3"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_3(context)
        return {'FINISHED'}
      
#main class of Display subsurf level 4          
class ModifiersSubsurfLevel_4(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_4"
    bl_label = "4"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_4(context)
        return {'FINISHED'}
      
#main class of Display subsurf level 5         
class ModifiersSubsurfLevel_5(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_5"
    bl_label = "5"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_5(context)
        return {'FINISHED'}
      
#main class of Display subsurf level 6          
class ModifiersSubsurfLevel_6(bpy.types.Operator):
    '''Change subsurf modifier level'''
    bl_idname = "view3d.modifiers_subsurf_level_6"
    bl_label = "6"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers_subsurf_level_6(context)
        return {'FINISHED'}


             
# register the classes
def register():
    bpy.utils.register_class(FastNavigate)
    bpy.utils.register_class(DisplayTextured)
    bpy.utils.register_class(DisplaySolid)
    bpy.utils.register_class(DisplayWire)
    bpy.utils.register_class(DisplayBounds)
    bpy.utils.register_class(DisplayWireframeOn)
    bpy.utils.register_class(DisplayWireframeOff)
    bpy.utils.register_class(DisplayBoundsOn)
    bpy.utils.register_class(DisplayBoundsOff)
    bpy.utils.register_class(DisplayShadeSmooth)
    bpy.utils.register_class(DisplayShadeFlat)
    bpy.utils.register_class(DisplayShadelessOn)
    bpy.utils.register_class(DisplayShadelessOff)
    bpy.utils.register_class(DisplayDoubleSidedOn)
    bpy.utils.register_class(DisplayDoubleSidedOff)
    bpy.utils.register_class(DisplayXRayOn)
    bpy.utils.register_class(DisplayXRayOff)
    bpy.utils.register_class(DisplayModifiersRenderOn)
    bpy.utils.register_class(DisplayModifiersRenderOff)
    bpy.utils.register_class(DisplayModifiersViewportOn)
    bpy.utils.register_class(DisplayModifiersViewportOff)
    bpy.utils.register_class(DisplayModifiersEditOn)
    bpy.utils.register_class(DisplayModifiersEditOff)
    bpy.utils.register_class(DisplayModifiersCageOn)
    bpy.utils.register_class(DisplayModifiersCageOff)
    bpy.utils.register_class(DisplayModifiersExpand)
    bpy.utils.register_class(DisplayModifiersCollapse)
    bpy.utils.register_class(DisplayModifiersApply)
    bpy.utils.register_class(DisplayModifiersDelete)
    bpy.utils.register_class(DisplayAddDummy)
    bpy.utils.register_class(DisplayDeleteDummy)
    bpy.utils.register_class(DisplaySimplify)
    bpy.utils.register_class(ModifiersSubsurfLevel_0)
    bpy.utils.register_class(ModifiersSubsurfLevel_1)
    bpy.utils.register_class(ModifiersSubsurfLevel_2)
    bpy.utils.register_class(ModifiersSubsurfLevel_3)
    bpy.utils.register_class(ModifiersSubsurfLevel_4)
    bpy.utils.register_class(ModifiersSubsurfLevel_5)
    bpy.utils.register_class(ModifiersSubsurfLevel_6)



def unregister():
    bpy.utils.unregister_class(FastNavigate)
    bpy.utils.unregister_class(DisplayTextured)
    bpy.utils.unregister_class(DisplaySolid)
    bpy.utils.unregister_class(DisplayWire)
    bpy.utils.unregister_class(DisplayBounds)
    bpy.utils.unregister_class(DisplayShadeSmooth)
    bpy.utils.unregister_class(DisplayShadeFlat)
    bpy.utils.unregister_class(DisplayShadelessOn)
    bpy.utils.unregister_class(DisplayShadelessOff)
    bpy.utils.unregister_class(DisplayWireframeOn)
    bpy.utils.unregister_class(DisplayWireframeOff)
    bpy.utils.unregister_class(DisplayBoundsOn)
    bpy.utils.unregister_class(DisplayBoundsOff)
    bpy.utils.unregister_class(DisplayDoubleSidedOn)
    bpy.utils.unregister_class(DisplayDoubleSidedOff)
    bpy.utils.unregister_class(DisplayXRayOn)
    bpy.utils.unregister_class(DisplayXRayOff)
    bpy.utils.unregister_class(DisplayModifiersRenderOn)
    bpy.utils.unregister_class(DisplayModifiersRenderOff)
    bpy.utils.unregister_class(DisplayModifiersViewportOn)
    bpy.utils.unregister_class(DisplayModifiersViewportOff)
    bpy.utils.unregister_class(DisplayModifiersEditOn)
    bpy.utils.unregister_class(DisplayModifiersEditOff)
    bpy.utils.unregister_class(DisplayModifiersCageOn)
    bpy.utils.unregister_class(DisplayModifiersCageOff)
    bpy.utils.unregister_class(DisplayModifiersExpand)
    bpy.utils.unregister_class(DisplayModifiersCollapse)
    bpy.utils.unregister_class(DisplayModifiersApply)
    bpy.utils.unregister_class(DisplayModifiersDelete)
    bpy.utils.unregister_class(DisplayAddDummy)
    bpy.utils.unregister_class(DisplayDeleteDummy)
    bpy.utils.unregister_class(DisplaySimplify)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_0)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_1)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_2)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_3)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_4)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_5)
    bpy.utils.unregister_class(ModifiersSubsurfLevel_6)
    





######################################################################################################################################
######################################################################################################################################
############  EdgeTune  ##############################################################################################################
############  EdgeTune  ##############################################################################################################


#bl_info = {
	#"name": "EdgeTune",
	#"author": "Gert De Roost",
	#"version": (3, 5, 0),
	#"blender": (2, 6, 3),
	#"location": "View3D > Tools",
	#"description": "Tuning edgeloops by redrawing them manually, sliding verts.",
	#"warning": "",
	#"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Mesh/EdgeTune",
	#"tracker_url": "",
	#"category": "Mesh"}


""" ------------------------------------------------ """

class EdgeTune(bpy.types.Operator):
	bl_idname = "mesh.edgetune"
	bl_label = "Tune Edge"
	bl_description = "Tuning edgeloops by redrawing them manually, sliding verts"
	bl_options = {"REGISTER", "UNDO"}
	
	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return (obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH')

	def invoke(self, context, event):
		
		self.scn = context.scene
		self.screen = context.screen
		self.area = context.area
		self.region = context.region  
		self.selobj = context.active_object
		self.init_edgetune()
		
		context.window_manager.modal_handler_add(self)
		self._handle = bpy.types.SpaceView3D.draw_handler_add(self.redraw, (), 'WINDOW', 'POST_PIXEL')
		
		return {'RUNNING_MODAL'}


	def modal(self, context, event):
	
		self.viewchange = False
		if event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				self.mbns = True
			if event.value == 'RELEASE':
				self.mbns = False
				self.contedge = None
				self.movedoff = True
		if event.type == 'RIGHTMOUSE':
			# cancel operation, reset to bmumdo mesh
			bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
			self.bm.free()
			bpy.ops.object.editmode_toggle()
			self.bmundo.to_mesh(self.mesh)
			bpy.ops.object.editmode_toggle()
			return {'CANCELLED'}
		elif event.type == 'MIDDLEMOUSE':
			# recalculate view parameters
			self.viewchange = True
			return {'PASS_THROUGH'}
		elif event.type in {'WHEELDOWNMOUSE', 'WHEELUPMOUSE'}:
			# recalculate view parameters
			self.viewchange = True		
			return {'PASS_THROUGH'}
		elif event.type == 'Z':
			if event.value == 'PRESS':
				if event.ctrl:
					if self.undolist != []:
						# put one vert(last) back to undo coordinate, found in list
						self.undolist.pop(0)
						vert = self.bm.verts[self.undocolist[0][0].index]
						vert.co[0] = self.undocolist[0][1]
						vert.co[1] = self.undocolist[0][2]
						vert.co[2] = self.undocolist[0][3]
						self.undocolist.pop(0)
						self.mesh.update()
			return {'RUNNING_MODAL'}
			
		elif event.type == 'RET':
			# Consolidate changes.
			# Free the bmesh.
			self.bm.free()
			self.bmundo.free()
			bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
			return {'FINISHED'}
			
		elif event.type == 'MOUSEMOVE':
			mxa = event.mouse_x
			mya = event.mouse_y
			self.region = None
			for a in context.screen.areas:
				if not(a.type == 'VIEW_3D'):
					continue
				for r in a.regions:
					if not(r.type == 'WINDOW'):
						continue
					if mxa > r.x and mya > r.y and mxa < r.x + r.width and mya < r.y + r.height:
						self.region = r
						break
					
			if not(self.region):
				return {'RUNNING_MODAL'}
			mx = mxa - self.region.x
			my = mya - self.region.y

			hoveredge = None
	
			# First check mouse is in bounding box edge of which edges.
			testscrl = []
			for edge in self.slideedges[self.region]:
				x1, y1, dummy = self.getscreencoords(edge.verts[0].co, self.region)
				x2, y2, dummy = self.getscreencoords(edge.verts[1].co, self.region)
				if x1 < x2:
					lwpx = x1 - 5
					uppx = x2 + 5
				else:
					lwpx = x2 - 5
					uppx = x1 + 5
				if y1 < y2:
					lwpy = y1 - 5
					uppy = y2 + 5
				else:
					lwpy = y2 - 5
					uppy = y1 + 5		
				if (((x1 < mx < x2) or (x2 < mx < x1)) and (lwpy < my < uppy)) or (((y1 < my < y2) or (y2 < my < y1)) and (lwpx < mx < uppx)):
					testscrl.append(edge)
				if self.contedge != None:
					testscrl.append(self.contedge)
	
			# Then check these edges to see if mouse is on one of them.
			allhoveredges = []
			hovering = False
			zmin = 1e10
			if testscrl != []:
				for edge in testscrl:
					x1, y1, z1 = self.getscreencoords(edge.verts[0].co, self.region)
					x2, y2, z2 = self.getscreencoords(edge.verts[1].co, self.region)
	
					if x1 == x2 and y1 == y2:
						dist = math.sqrt((mx - x1)**2 + (my - y1)**2)
					else:
						dist = ((mx - x1)*(y2 - y1) - (my - y1)*(x2 - x1)) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	
					if -5 < dist < 5:
						if self.movedoff or (not(self.movedoff) and edge == self.contedge):
							allhoveredges.append(edge)
							if hoveredge != None and ((z1 + z2) / 2) > zmin:
								pass
							else:
								hovering = True
								hoveredge = edge
								zmin = (z1 + z2) / 2
								self.mouseover = True
								x1, y1, dummy = self.getscreencoords(hoveredge.verts[0].co, self.region)
								x2, y2, dummy = self.getscreencoords(hoveredge.verts[1].co, self.region)
								for r in self.regions:
									self.bx1[r], self.by1[r], dummy = self.getscreencoords(hoveredge.verts[0].co, r)
									self.bx2[r], self.by2[r], dummy = self.getscreencoords(hoveredge.verts[1].co, r)
								self.region.tag_redraw()
								break
								
			if hovering == False:
				self.movedoff = True
				if self.mouseover == True:
					self.highoff = True
					self.region.tag_redraw()
				self.mouseover = False
				self.bx1[self.region] = -1 
				self.bx2[self.region] = -1
				self.by1[self.region] = -1
				self.by2[self.region] = -1, -1, -1, -1
			
	
	
			if hoveredge != None and self.mbns == True:
				self.contedge = edge
				self.movedoff = False
				# Find projection mouse perpend on edge.
				if x1 == x2:	x1 += 1e-6
				if y1 == y2:	y1 += 1e-6
				a = (x2 - x1) / (y2 - y1)
				x = ((x1 / a) + (mx * a) + my - y1) / ((1 / a) + a)
				y = ((mx - x) * a) + my
				# Calculate relative position on edge and adapt screencoords accoringly.
				div = (x - x1) / (x2 - x1)
				if hoveredge.verts[0] in self.sverts[self.region]:
					vert = hoveredge.verts[0]
					vert2 = hoveredge.verts[1]
				else:
					vert = hoveredge.verts[1]
					vert2 = hoveredge.verts[0]
					
				# Update local undo info.
				if self.undolist == []:
					self.undolist.insert(0, hoveredge)
					self.undocolist.insert(0, [vert, vert.co[0], vert.co[1], vert.co[2]])
				if self.undolist[0] != hoveredge:
					self.undolist.insert(0, hoveredge)
					self.undocolist.insert(0, [vert, vert.co[0], vert.co[1], vert.co[2]])

				hx1, hy1, dummy = self.getscreencoords(hoveredge.verts[0].co, self.region)
				hx2, hy2, dummy = self.getscreencoords(hoveredge.verts[1].co, self.region)
				coords = [((hx2 - hx1) * div ) + hx1, ((hy2 - hy1) * div ) + hy1]
				for verts in self.selverts[self.region]:
					if vert == verts[0]:
						self.selcoords[self.region][self.selverts[self.region].index(verts)][0] = coords
					elif vert == verts[1]:	
						self.selcoords[self.region][self.selverts[self.region].index(verts)][1] = coords
				if vert in self.singles:
					self.boxes[self.region][self.singles.index(vert)] = coords
				# Calculate new vert 3D coordinates.		
				vx1, vy1, vz1 = hoveredge.verts[0].co[:]
				vx2, vy2, vz2 = hoveredge.verts[1].co[:]
				self.vertd[vert] = [((vx2 - vx1) * div ) + vx1, ((vy2 - vy1) * div ) + vy1, ((vz2 - vz1) * div ) + vz1]
				vert = self.bm.verts[vert.index]
				vert.co[0] = ((vx2 - vx1) * div ) + vx1
				vert.co[1] = ((vy2 - vy1) * div ) + vy1
				vert.co[2] = ((vz2 - vz1) * div ) + vz1
				self.mesh.update()
				
		return {'RUNNING_MODAL'}

	
	
	def adapt(self):
		
		self.firstrun = False
			
		self.regions = []
		self.spaces = []
		self.halfheight = {}
		self.halfwidth = {}
		self.perspm = {}
		for a in self.screen.areas:
			if not(a.type == 'VIEW_3D'):
				continue
			for r in a.regions:
				if not(r.type == 'WINDOW'):
					continue
				self.regions.append(r)
				self.halfwidth[r] = r.width / 2
				self.halfheight[r] = r.height / 2
				for sp in a.spaces:
					if sp.type == 'VIEW_3D':
						self.spaces.append(sp)
						self.perspm[r] = sp.region_3d.perspective_matrix
						
		self.selcoords = {}
		self.slidecoords = {}
		self.boxes = {}
		self.sverts = {}
		self.selverts = {}
		self.seledges = {}
		self.slideverts = {}
		self.slideedges = {}
		for r in self.regions:
			self.selcoords[r] = []
			self.slidecoords[r] = []
			self.boxes[r] = []
			self.sverts[r] = []
			self.selverts[r] = []
			self.seledges[r] = []
			self.slideverts[r] = []
			self.slideedges[r] = []
			
		for r in self.regions:

			self.getlayout(r)
			
			# recalculate screencoords in lists
			for posn in range(len(self.selverts[r])):
				self.selcoords[r][posn] = [self.getscreencoords(Vector(self.vertd[self.selverts[r][posn][0]]), r)[:2], self.getscreencoords(Vector(self.vertd[self.selverts[r][posn][1]]), r)[:2]]
			for posn in range(len(self.slideverts[r])):
				self.slidecoords[r][posn] = [self.getscreencoords(self.slideverts[r][posn][0].co, r)[:2],  self.getscreencoords(self.slideverts[r][posn][1].co, r)[:2]]
			for posn in range(len(self.singles)):
				self.boxes[r][posn] = self.getscreencoords(Vector(self.vertd[self.singles[posn]]), r)[:2]
			
	
	
	def findworldco(self, vec):
	
		vec = vec.copy()
		vec.rotate(self.selobj.matrix_world)
		vec.rotate(self.selobj.matrix_world)
		vec = vec * self.selobj.matrix_world + self.selobj.matrix_world.to_translation()
		return vec
	
	def getscreencoords(self, vec, reg):
	
		# calculate screencoords of given Vector
		vec = self.findworldco(vec)
		prj = self.perspm[reg] * vec.to_4d()
		return (self.halfwidth[reg] + self.halfwidth[reg] * (prj.x / prj.w), self.halfheight[reg] + self.halfheight[reg] * (prj.y / prj.w), prj.z)
	
	
	
	
	def init_edgetune(self):
	
		self.mesh = self.selobj.data
		self.bm = bmesh.from_edit_mesh(self.mesh)
		self.bmundo = self.bm.copy()
	
		self.viewwidth = self.area.width
		self.viewheight = self.area.height
		
		#remember initial selection
		self.keepverts = []
		for vert in self.bm.verts:
			if vert.select:
				self.keepverts.append(vert)
		self.keepedges = []
		for edge in self.bm.edges:
			if edge.select:
				self.keepedges.append(edge)
	
		self.firstrun = True
		self.highoff = False
		self.mbns = False
		self.viewchange = False
		self.mouseover = False	
		self.bx1, self.bx2, self.by1, self.by2 = {}, {}, {}, {}
		self.undolist = []
		self.undocolist = []
		self.contedge = None
	
		self.adapt()
		for r in self.regions:
			r.tag_redraw()
	
	
	
	def getlayout(self, reg):
		
		# seledges: selected edges list
		# selverts: selected verts list per edge
		# selcoords: selected verts coordinate list per edge
		self.sverts[reg] = []
		self.seledges[reg] = []
		self.selverts[reg] = []
		self.selcoords[reg] = []
		visible = {}
		if self.spaces[self.regions.index(reg)].use_occlude_geometry:
			rv3d = self.spaces[self.regions.index(reg)].region_3d
			eyevec = Vector(rv3d.view_matrix[2][:3])
			eyevec.length = 100000
			eyeloc = Vector(rv3d.view_matrix.inverted().col[3][:3])
			for vert in self.keepverts:
				vno = vert.normal
				vno.length = 0.0001
				vco = self.findworldco(vert.co + vno)
				if rv3d.is_perspective:
					hit = self.scn.ray_cast(vco, eyeloc)
					if hit[0]:
						vno = -vno
						vco = self.findworldco(vert.co + vno)
						hit = self.scn.ray_cast(vco, eyevec)
				else:
					hit = self.scn.ray_cast(vco, vco + eyevec)
					if hit[0]:
						vno = -vno
						vco = self.findworldco(vert.co + vno)
						hit = self.scn.ray_cast(vco, vco + eyevec)
				if not(hit[0]):
					visible[vert] = True
					self.sverts[reg].append(self.bmundo.verts[vert.index])
				else:
					visible[vert] = False
		else:
			for vert in self.keepverts:
				visible[vert] = True
				self.sverts[reg].append(self.bmundo.verts[vert.index])
				
		for edge in self.keepedges:
			if visible[edge.verts[0]] and visible[edge.verts[1]]:
				edge = self.bmundo.edges[edge.index]
				self.seledges[reg].append(edge)
				self.selverts[reg].append([edge.verts[0], edge.verts[1]])
				x1, y1, dummy = self.getscreencoords(edge.verts[0].co, reg)
				x2, y2, dummy = self.getscreencoords(edge.verts[1].co, reg)
				self.selcoords[reg].append([[x1, y1],[x2, y2]])
	
		# selverts: selected verts list
		# slideedges: slideedges list
		# slideverts: slideverts list per edge
		# slidecoords: slideverts coordinate list per edge
		self.vertd = {}
		self.slideverts[reg] = []
		self.slidecoords[reg] = []
		self.slideedges[reg] = []
		count = 0
		for vert in self.sverts[reg]:
			self.vertd[vert] = vert.co[:]
			for edge in vert.link_edges:
				count += 1
				if not(edge in self.seledges[reg]):
					self.slideedges[reg].append(edge)
					self.slideverts[reg].append([edge.verts[0], edge.verts[1]])
					x1, y1, dummy = self.getscreencoords(edge.verts[0].co, reg)
					x2, y2, dummy = self.getscreencoords(edge.verts[1].co, reg)
					self.slidecoords[reg].append([[x1, y1], [x2, y2]])				
		# Box out single vertices.
		self.singles = []
		self.boxes[reg] = []
		for vert in self.sverts[reg]:
			single = True
			for edge in self.seledges[reg]:
				if vert == edge.verts[0] or vert == edge.verts[1]:
					single = False
					break
			if single:
				self.singles.append(vert)
				self.boxes[reg].append(self.getscreencoords(vert.co, reg)[:2])
	
	
	def redraw(self):
		
		drawregion = bpy.context.region
					
		if self.viewchange:
			self.adapt()
			
		if self.slideverts[drawregion] != []:
			# Draw single verts as boxes.
			glColor3f(1.0,1.0,0)
			for self.vertcoords in self.boxes[drawregion]:
				glBegin(GL_POLYGON)
				x, y = self.vertcoords
				glVertex2f(x-2, y-2)
				glVertex2f(x-2, y+2)
				glVertex2f(x+2, y+2)
				glVertex2f(x+2, y-2)
				glEnd()
		
			# Accentuate selected edges.
			glColor3f(1.0, 1.0, 0)
			for posn in range(len(self.selcoords[drawregion])):
				glBegin(GL_LINES)
				x, y = self.selcoords[drawregion][posn][0]
				glVertex2f(x, y)
				x, y = self.selcoords[drawregion][posn][1]
				glVertex2f(x, y)
				glEnd()
		
			# Draw slide-edges.
			glColor3f(1.0, 0, 0)
			for posn in range(len(self.slidecoords[drawregion])):
				glBegin(GL_LINES)
				x, y = self.slidecoords[drawregion][posn][0]
				glVertex2f(x, y)
				x, y = self.slidecoords[drawregion][posn][1]
				glVertex2f(x, y)
				glEnd()
	
		# Draw mouseover highlighting.
		if self.mouseover:
			glColor3f(0, 0, 1.0)
			glBegin(GL_LINES)
			x,y = self.bx1[drawregion], self.by1[drawregion]
			if not(x == -1):
				glVertex2f(x,y)
			x,y = self.bx2[drawregion], self.by2[drawregion]
			if not(x == -1):
				glVertex2f(x,y)
			glEnd()
		if self.highoff:
			self.highoff = 0
			glColor3f(1.0, 0, 0)
			glBegin(GL_LINES)
			x,y = self.bx1[drawregion], self.by1[drawregion]
			if not(x == -1):
				glVertex2f(x,y)
			x,y = self.bx2[drawregion], self.by2[drawregion]
			if not(x == -1):
				glVertex2f(x,y)
			glEnd()





def panel_func(self, context):
	self.layout.label(text="Deform:")
	self.layout.operator("mesh.edgetune", text="EdgeTune")




###################################################################################################################################
###################################################################################################################################
##################  CAD VTX  ######################################################################################################
##################  CAD VTX  ######################################################################################################

#bl_info = {
#    'name': "Smart two edges intersect tool (cad VTX)",
#    'author': "luxuy blendercn",
#    'version': (1, 0, 0),
#    'blender': (2, 70, 0),
#    'location': 'View3D > EditMode > (w) Specials', 
#    'warning': "",
#    'category': 'Mesh'}
   
    

def pt_in_line(pt,line):
    vec1=pt-line[0]
    vec2=pt-line[1]
    
    k=vec1.cross(vec2)
    print("---------",k.length)
    if k.length<10e-4:
        #共线
        m=vec1.dot(vec2)
        if m==0:
            return 1
            
        if m>0:
            return "out"
        else:
            return "in"
    else:
        return None

    

    

class CurToIntersect(bpy.types.Operator):
    bl_idname = "bpt.smart_vtx"
    bl_label = "Smart 2 edges intersect(auto vtx)"
    
    bl_options = {'REGISTER', 'UNDO'}
    flag=BoolProperty( name="Force to co planar", default=True)

 

    @classmethod
    def poll(cls, context):
        if  bpy.context.mode=='EDIT_MESH':
            return True
        return False
    def invoke( self, context, event ):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        context.tool_settings.mesh_select_mode = (False,True,True)
        
        ob=context.object
        me=ob.data
        
        bm=bmesh.new()
        
        
        bm.from_mesh(ob.data)
        #bmesh.from_edit_mesh(me)
        mw=ob.matrix_world
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        sel_edges=[]
        for e in ob.data.edges:
            if e.select:
                sel_edges.append(e)
        if len(sel_edges)!=2:
            msg ="Must select only 2 edges !"
            self.report( {"INFO"}, msg  )
            bpy.ops.object.mode_set(mode = 'EDIT')
            return {"FINISHED"}
        e1=bm.edges[sel_edges[0].index]
        e2=bm.edges[sel_edges[1].index]
        
        
        
        pts=intersect_line_line(e1.verts[0].co,e1.verts[1].co,e2.verts[0].co,e2.verts[1].co)
        
        if (pts[0]-pts[1]).length>10e-4:
            bpy.ops.object.editmode_toggle()
            
            
            if self.flag:
                msg ="No coplanar, but changed to co-planar now!"
       
                save=context.space_data.transform_orientation,context.space_data.pivot_point
                context.space_data.transform_orientation = 'VIEW' 
                context.space_data.pivot_point = 'ACTIVE_ELEMENT'
                bpy.ops.transform.resize(value=(1,1,0), constraint_axis=(False, False, True), constraint_orientation='VIEW')
                
                context.space_data.transform_orientation,context.space_data.pivot_point=save
                self.execute(context)
            else:
                msg ="No coplanar!"
       
            self.report( {"INFO"}, msg  )
            
        else:
            self.execute(context)
            
        

        return {"FINISHED"}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        ob=context.object
        me=ob.data
        
        bm=bmesh.new()
        
        
        bm.from_mesh(ob.data)
        #bmesh.from_edit_mesh(me)
        mw=ob.matrix_world
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        sel_edges=[]
        for e in ob.data.edges:
            if e.select:
                sel_edges.append(e)
        
        e1=bm.edges[sel_edges[0].index]
        e2=bm.edges[sel_edges[1].index]
        
        
        
        pts=intersect_line_line(e1.verts[0].co,e1.verts[1].co,e2.verts[0].co,e2.verts[1].co)
        
        if (pts[0]-pts[1]).length>10e-4:
            bpy.ops.object.editmode_toggle()
            return {'FINISHED'}
        
        #context.scene.cursor_location=mw*pts[0]
        line1=[v.co for v in e1.verts]
        line2=[v.co for v in e2.verts]
        s1=pt_in_line(pts[0],line1)
        s2=pt_in_line(pts[1],line2)
        print(s1,s2)
        edges=[]
        if s1=='in':
            edges.append(e1)
        if s2=='in':
            edges.append(e2)
        print(edges)
        
       
        bm.verts.index_update()
        bm.edges.index_update()
        bmesh.ops.subdivide_edges(bm, edges=edges,cuts=1)
        
        
        if len(edges)==1:
            bm.verts[-1].co=pts[0]
            if s1=='in':
                print("---")
                
                if (e2.verts[0].co-pts[0]).length>(e2.verts[1].co-pts[0]).length:
                    #v4.co=pts[0]
                    if len(e2.verts[1].link_edges)==1: #自由端
                        print("free")
                        e2.verts[1].co=pts[0]
                        if len(set(e1.link_faces) & set(e2.verts[0].link_faces))>0:
                            print("ok")
                            v=e2.verts[0]
                            bmesh.ops.delete(bm, geom=[e2.verts[1]], context=1)
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],v])
                    else:
                        if len(set(e1.link_faces) & set(e2.verts[1].link_faces))>0:
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],e2.verts[1]])
                        else:
                            bm.edges.new([bm.verts[-1],e2.verts[1]])
                else:
                    if len(e2.verts[0].link_edges)==1: #自由端
                        print("free")
                        e2.verts[0].co=pts[0]
                        if len(set(e1.link_faces) & set(e2.verts[1].link_faces))>0:
                            print("ok")
                            v=e2.verts[1]
                            bmesh.ops.delete(bm, geom=[e2.verts[0]], context=1)
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],v])
                    else:
                        if len(set(e1.link_faces) & set(e2.verts[0].link_faces))>0:
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],e2.verts[0]])
                        else:
                            bm.edges.new([bm.verts[-1],e2.verts[0]])
            else:
                if (e1.verts[0].co-pts[0]).length>(e1.verts[1].co-pts[0]).length:
                    #v4.co=pts[0]
                    if len(e1.verts[1].link_edges)==1: #自由端
                        print("free")
                        e1.verts[1].co=pts[0]
                        if len(set(e2.link_faces) & set(e1.verts[0].link_faces))>0:
                            print("ok")
                            v=e1.verts[0]
                            bmesh.ops.delete(bm, geom=[e1.verts[1]], context=1)
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],v])
                    else:
                        if len(set(e2.link_faces) & set(e1.verts[1].link_faces))>0:
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],e1.verts[1]])
                        else:
                            bm.edges.new([bm.verts[-1],e1.verts[1]])
                else:
                    #v3.co=pts[0]
                    if len(e1.verts[0].link_edges)==1: #自由端
                        print("free")
                        e1.verts[0].co=pts[0]
                        if len(set(e2.link_faces) & set(e1.verts[1].link_faces))>0:
                            print("ok")
                            v=e1.verts[1]
                            bmesh.ops.delete(bm, geom=[e1.verts[0]], context=1)
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],v])
                    else:
                        
                        if len(set(e2.link_faces) & set(e1.verts[0].link_faces))>0:
                        
                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1],e1.verts[0]])
                        else:
                            bm.edges.new([bm.verts[-1],e1.verts[0]])
        
        if len(edges)==2:
            bm.verts[-1].co=pts[0]
            bm.verts[-2].co=pts[0]
        if len(edges)==0:
            print("\n"*10)
            bm.verts.new(pts[0])
            if (e1.verts[0].co-pts[0]).length>(e1.verts[1].co-pts[0]).length:
                #v4.co=pts[0]
                if len(e1.verts[1].link_edges)==1: #自由端
                    
                    e1.verts[1].co=pts[0]
                else:
                    
                    bm.edges.new([bm.verts[-1],e1.verts[1]])
            else:
                if len(e1.verts[0].link_edges)==1: #自由端
                    e1.verts[0].co=pts[0]
                else:
                    bm.edges.new([bm.verts[-1],e1.verts[0]])
                        
            if (e2.verts[0].co-pts[0]).length>(e2.verts[1].co-pts[0]).length:
                    #v4.co=pts[0]
                if len(e2.verts[1].link_edges)==1: #自由端
                    
                    e2.verts[1].co=pts[0]
                else:
                    
                    bm.edges.new([bm.verts[-1],e2.verts[1]])
            else:
                if len(e2.verts[0].link_edges)==1: #自由端
                    e2.verts[0].co=pts[0]
                else:
                    bm.edges.new([bm.verts[-1],e2.verts[0]])
            
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
        bm.to_mesh(ob.data)
        bpy.ops.object.editmode_toggle()
        #bmesh.update_edit_mesh(me, tessface=True, destructive=True)
        bm.free()
        
        
        #bpy.ops.mesh.remove_doubles()
        
        
        return {'FINISHED'}
#---------------------------------------------
def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator('bpt.smart_vtx')


 
def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)
    

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func) 



########################################################################################################################################
########################################################################################################################################
############  Offset Edges  ############################################################################################################
############  Offset Edges  ############################################################################################################

# <pep8 compliant>

bl_info = {
    "name": "Offset Edges",
    "author": "Hidesato Ikeya",
    "version": (0, 1, 15),
    "blender": (2, 70, 0),
    "location": "VIEW3D > Edge menu(CTRL-E) > Offset Edges",
    "description": "Offset Edges",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/offset_edges",
    "tracker_url": "",
    "category": "Mesh"}


#from time import perf_counter

X_UP = Vector((1.0, .0, .0))
Y_UP = Vector((.0, 1.0, .0))
Z_UP = Vector((.0, .0, 1.0))
ZERO_VEC = Vector((.0, .0, .0))
ANGLE_90 = pi / 2
ANGLE_180 = pi
ANGLE_360 = 2 * pi


class OffsetEdges(bpy.types.Operator):
    """Offset Edges."""
    bl_idname = "mesh.offset_edges"
    bl_label = "Offset Edges"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.FloatProperty(
        name="Width", default=.2, precision=3, step=0.05)
    geometry_mode = bpy.props.EnumProperty(
        items=[('offset', "Offset", "Offset edges"),
               ('extrude', "Extrude", "Extrude edges"),
               ('move', "Move", "Move selected edges")],
        name="Geometory mode", default='offset')
    follow_face = bpy.props.BoolProperty(
        name="Follow Face", default=False,
        description="Offset along faces around")
    end_align_edge = bpy.props.BoolProperty(
        name="Align Ends with Edges", default=False,
        description="Align End vertices with edges")
    flip = bpy.props.BoolProperty(
        name="Flip", default=False,
        description="Flip direction")
    mirror_modifier = bpy.props.BoolProperty(
        name="Mirror Modifier", default=False,
        description="Take into account for Mirror modifier")

    threshold = bpy.props.FloatProperty(
        name="Threshold", default=1.0e-4, step=1.0e-5,
        description="Angle threshold which determines folding edges",
        options={'HIDDEN'})
    limit_hole_check = bpy.props.IntProperty(
        name="Limit Hole Check", default=5, min=0,
        description="Limit number of hole check per edge loop",
        options={'HIDDEN'})

    @classmethod
    def poll(self, context):
        return context.mode == 'EDIT_MESH'

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'geometry_mode', text="")

        layout.prop(self, 'width')
        layout.prop(self, 'flip')
        layout.prop(self, 'end_align_edge')
        layout.prop(self, 'follow_face')

        for m in context.edit_object.modifiers:
            if m.type == 'MIRROR':
                layout.prop(self, 'mirror_modifier')
                break

    def create_edgeloops(self, bm, mirror_planes):
        selected_edges = []
        self.mirror_v_p_pairs = mirror_v_p_pairs = dict()
        # key is vert, value is the mirror plane to which the vert belongs.
        for e in bm.edges:
            if e.select:
                co_faces_selected = 0
                for f in e.link_faces:
                    if f.select:
                        co_faces_selected += 1
                else:
                    if co_faces_selected <= 1:
                        selected_edges.append(e)
                        if mirror_planes:
                            v1, v2 = e.verts
                            v1_4d = v1.co.to_4d()
                            v2_4d = v2.co.to_4d()
                            for plane, threshold in mirror_planes:
                                if (abs(v1_4d.dot(plane)) < threshold
                                   and abs(v2_4d.dot(plane)) < threshold):
                                    # This edge is on the mirror plane
                                    selected_edges.pop()
                                    mirror_v_p_pairs[v1] = \
                                        mirror_v_p_pairs[v2] = plane
                                    break

        if not selected_edges:
            self.report({'WARNING'},
                        "No edges selected.")
            return None

        v_es_pairs = dict()
        self.selected_verts = selected_verts= \
            set(v for e in selected_edges for v in e.verts)
        self.end_verts = end_verts= selected_verts.copy()
        for e in selected_edges:
            for v in e.verts:
                edges = v_es_pairs.get(v)
                if edges is None:
                    v_es_pairs[v] = e
                elif isinstance(edges, BMEdge):
                    v_es_pairs[v] = (edges, e)
                    end_verts.remove(v)
                else:
                    self.report({'WARNING'},
                                "Edge polls detected. Select non-branching edge loops")
                    return None

        if self.follow_face:
            self.e_lp_pairs = e_lp_pairs = dict()
            for e in selected_edges:
                loops = []
                for lp in e.link_loops:
                    f = lp.face
                    if not f.hide and f.normal != ZERO_VEC:
                        if f.select:
                            e_lp_pairs[e] = (lp,)
                            break
                        else:
                            loops.append(lp)
                else:
                    e_lp_pairs[e] = loops

        if mirror_planes:
            for v in end_verts:
                if v not in mirror_v_p_pairs:
                    for plane, threshold in mirror_planes:
                        if abs(v.co.to_4d().dot(plane)) < threshold:
                            # This vert is on the mirror plane
                            mirror_v_p_pairs[v] = plane
                            break

        edge_loops = selected_edges

        self.extended_verts = extended_verts = set()
        end_verts = end_verts.copy()
        while end_verts:
            v_start = end_verts.pop()
            e_start = v_es_pairs[v_start]
            edge_chain = [(v_start, e_start)]
            v_current = e_start.other_vert(v_start)
            e_prev = e_start
            while v_current not in end_verts:
                e1, e2 = v_es_pairs[v_current]
                e = e1 if e1 != e_prev else e2
                edge_chain.append((v_current, e))
                v_current = e.other_vert(v_current)
                e_prev = e
            end_verts.remove(v_current)

            geom = bmesh.ops.extrude_vert_indiv(bm, verts=[v_start, v_current])
            ex_verts = geom['verts']
            selected_verts.update(ex_verts)
            extended_verts.update(ex_verts)
            edge_loops += geom['edges']
            for ex_v in ex_verts:
                ex_edge = ex_v.link_edges[0]
                delta = .0
                if ex_edge.other_vert(ex_v) is v_start:
                    v_orig = v_start
                    for v, e in edge_chain:
                        if e.calc_length() != 0.0:
                            delta = v.co - e.other_vert(v).co
                            break
                else:
                    v_orig = v_current
                    for v, e in reversed(edge_chain):
                        if e.calc_length() != 0.0:
                            delta = e.other_vert(v).co - v.co
                            break

                ex_v.co += delta
            edge_loops.append(bm.edges.new(geom['verts']))

        self.edge_loops_set = set(edge_loops)

        return edge_loops

    def create_geometry(self, bm, e_loops):
        geom_extruded = bmesh.ops.extrude_edge_only(bm, edges=e_loops)['geom']

        self.offset_verts = offset_verts = \
            [e for e in geom_extruded if isinstance(e, BMVert)]
        self.offset_edges = offset_edges = \
            [e for e in geom_extruded if isinstance(e, BMEdge)]
        self.side_faces = side_faces = \
            [f for f in geom_extruded if isinstance(f, BMFace)]
        bmesh.ops.recalc_face_normals(bm, faces=side_faces)
        self.side_edges = side_edges = \
            [e.link_loops[0].link_loop_next.edge for e in offset_edges]
        self.side_edges_set = set(side_edges) # Used in get_inner_vec()
                                              # and apply_mirror()

        extended_verts, end_verts = self.extended_verts, self.end_verts
        mirror_v_p_pairs = self.mirror_v_p_pairs
        mirror_v_p_pairs_new = dict()
        self.v_v_pairs = v_v_pairs = dict()  # keys is offset vert,
                                             # values is original vert.
        orig_verts = self.selected_verts
        for e in side_edges:
            v1, v2 = e.verts
            if v1 in orig_verts:
                v_offset, v_orig = v2, v1
            else:
                v_offset, v_orig = v1, v2
            v_v_pairs[v_offset] = v_orig

            if v_orig in extended_verts:
                extended_verts.add(v_offset)
            if v_orig in end_verts:
                end_verts.add(v_offset)
                end_verts.remove(v_orig)
            plane = mirror_v_p_pairs.get(v_orig)
            if plane:
                # Offsetted vert should be on the mirror plane.
                mirror_v_p_pairs_new[v_offset] = plane
        self.mirror_v_p_pairs = mirror_v_p_pairs_new

        self.img_faces = img_faces = bmesh.ops.edgeloop_fill(
            bm, edges=offset_edges, mat_nr=0, use_smooth=False)['faces']

        self.e_e_pairs = e_e_pairs = {
            fl.edge: fl.link_loop_radial_next.link_loop_next.link_loop_next.edge
            for face in img_faces for fl in face.loops}

        if self.follow_face:
            e_lp_pairs = self.e_lp_pairs
            self.e_lp_pairs = {
                e_offset: e_lp_pairs.get(e_orig, tuple())
                for e_offset, e_orig in e_e_pairs.items()}
            # Calculate normals
            self.calc_average_fnorm()
            e_fn_pairs = self.e_fn_pairs
            for face in img_faces:
                for fl in face.loops:
                    fn = e_fn_pairs[fl.edge]
                    if fn:
                        if face.normal.dot(fn) < .0:
                            face.normal_flip()
                        break
        else:
            for face in img_faces:
                if face.normal[2] < .0:
                    face.normal_flip()

        return img_faces

    def calc_average_fnorm(self):
        self.e_fn_pairs = e_fn_pairs = dict()
        # edge:average_face_normal pairs.
        e_lp_pairs = self.e_lp_pairs

        for e in self.offset_edges:
            loops = e_lp_pairs[e]
            if loops:
                normal = Vector()
                for lp in loops:
                    normal += lp.face.normal
                normal.normalize()
                e_fn_pairs[e] = normal
            else:
                e_fn_pairs[e] = None

    def get_inner_vec(self, floop, threshold=1.0e-3):
        """Get inner edge vector connecting to floop.vert"""
        vert = self.v_v_pairs[floop.vert]
        vec_edge = floop.edge.verts[0].co - floop.edge.verts[1].co
        vec_edge.normalize()
        side_edges, edge_loops = self.side_edges_set, self.edge_loops_set
        co = 0
        for e in vert.link_edges:
            if (e in side_edges or e in edge_loops or e.hide
               or e.calc_length() == .0):
                continue
            inner = e
            co += 1
            if e.select:
                break
        else:
            if co != 1:
                return None
        vec_inner = (inner.other_vert(vert).co - vert.co).normalized()
        if abs(vec_inner.dot(vec_edge)) > 1. - threshold:
            return None
        else:
            return vec_inner

    def is_hole(self, floop, tangent):
        edge = self.e_e_pairs[floop.edge]
        adj_loop = self.e_lp_pairs[floop.edge]
        if len(adj_loop) != 1:
            return None
        adj_loop = adj_loop[0]

        vec_edge = edge.verts[0].co - edge.verts[1].co
        vec_adj = adj_loop.calc_tangent()
        vec_adj -= vec_adj.project(vec_edge)
        dot = vec_adj.dot(tangent)
        if dot == .0:
            return None
        elif dot > .0:
            # Hole
            return True
        else:
            return False

    def clean_geometry(self, bm):
        bm.normal_update()

        img_faces = self.img_faces
        offset_verts = self.offset_verts
        offset_edges = self.offset_edges
        side_edges = self.side_edges
        side_faces = self.side_faces
        extended_verts = self.extended_verts
        v_v_pairs = self.v_v_pairs

        for e in self.offset_edges:
            e.select = True

        if self.geometry_mode == 'extrude':
            for face in img_faces:
                flip = True if self.flip else False

                lp = face.loops[0]
                side_lp = lp.link_loop_radial_next
                if lp.vert is not side_lp.vert:
                    # imaginary face normal and side faces normal
                    # should be inconsistent.
                    flip = not flip

                if face in self.should_flip:
                    flip = not flip

                if flip:
                    sides = (
                        lp.link_loop_radial_next.face for lp in face.loops)
                    for sf in sides:
                        sf.normal_flip()

        bmesh.ops.delete(bm, geom=img_faces, context=3)

        if self.geometry_mode != 'extrude':
            if self.geometry_mode == 'offset':
                bmesh.ops.delete(bm, geom=side_edges+side_faces, context=2)
            elif self.geometry_mode == 'move':
                for v_target, v_orig in v_v_pairs.items():
                    v_orig.co = v_target.co
                bmesh.ops.delete(
                    bm, geom=side_edges+side_faces+offset_edges+offset_verts,
                    context=2)
                extended_verts -= set(offset_verts)

        extended = extended_verts.copy()
        for v in extended_verts:
            extended.update(v.link_edges)
            extended.update(v.link_faces)
        bmesh.ops.delete(bm, geom=list(extended), context=2)

    @staticmethod
    def skip_zero_length_edges(floop, normal=None, reverse=False):
        floop_orig = floop
        if normal:
            normal = normal.normalized()
        skip_co = 0
        length = floop.edge.calc_length()
        if length and normal:
            # length which is perpendicular to normal
            edge = floop.vert.co - floop.link_loop_next.vert.co
            edge -= edge.project(normal)
            length = edge.length

        while length == 0:
            floop = (floop.link_loop_next if not reverse
                     else floop.link_loop_prev)
            if floop is floop_orig:
                # length of all edges are zero.
                return None, None
            skip_co += 1
            length = floop.edge.calc_length()
            if length and normal:
                edge = floop.vert.co - floop.link_loop_next.vert.co
                edge -= edge.project(normal)
                length = edge.length

        return floop, skip_co

    @staticmethod
    def get_mirror_planes(edit_object):
        mirror_planes = []
        e_mat_inv = edit_object.matrix_world.inverted()
        for m in edit_object.modifiers:
            if (m.type == 'MIRROR' and m.use_mirror_merge
               and m.show_viewport and m.show_in_editmode):
                mthreshold = m.merge_threshold
                if m.mirror_object:
                    xyz_mat = e_mat_inv * m.mirror_object.matrix_world
                    x, y, z, w = xyz_mat.adjugated()
                    loc = xyz_mat.to_translation()
                    for axis in (x, y, z):
                        axis[0:3] = axis.to_3d().normalized()
                        dist = -axis.to_3d().dot(loc)
                        axis[3] = dist
                else:
                    x, y, z = X_UP.to_4d(), Y_UP.to_4d(), Z_UP.to_4d()
                    x[3] = y[3] = z[3] = .0
                if m.use_x:
                    mirror_planes.append((x, mthreshold))
                if m.use_y:
                    mirror_planes.append((y, mthreshold))
                if m.use_z:
                    mirror_planes.append((z, mthreshold))
        return mirror_planes

    def apply_mirror(self):
        # Crip or extend edges to the mirror planes
        side_edges, extended_verts = self.side_edges_set, self.extended_verts
        for v, plane in self.mirror_v_p_pairs.items():
            for e in v.link_edges:
                if e in side_edges or e.other_vert(v) in extended_verts:
                    continue
                point = v.co.to_4d()
                direction = e.verts[0].co - e.verts[1].co
                direction = direction.to_4d()
                direction[3] = .0
                t = -plane.dot(point) / plane.dot(direction)
                v.co = (point + t * direction)[:3]
                break


    def get_tangent(self, loop_act, loop_prev,
                    f_normal_act=None, f_normal_prev=None,
                    threshold=1.0e-4, end_align=False, end_verts=None):
        def decompose_vector(vec, vec_s, vec_t):
            det_xy = vec_s.x * vec_t.y - vec_s.y * vec_t.x
            if det_xy:
                s = (vec.x * vec_t.y - vec.y * vec_t.x) / det_xy
                t = (-vec.x * vec_s.y + vec.y * vec_s.x) / det_xy
            else:
                det_yz = vec_s.y * vec_t.z - vec_s.z * vec_t.y
                if det_yz:
                    s = (vec.x * vec_t.z - vec.y * vec_t.y) / det_yz
                    t = (-vec.x * vec_s.z + vec.y * vec_s.y) / det_yz
                else:
                    det_zx = vec_s.z * vec_t.x - vec_s.x * vec_t.z
                    s = (vec.x * vec_t.x - vec.y * vec_t.z) / det_zx
                    t = (-vec.x * vec_s.x + vec.y * vec_s.z) / det_zx
            return s, t

        vec_edge_act = loop_act.link_loop_next.vert.co - loop_act.vert.co
        vec_edge_act.normalize()

        vec_edge_prev = loop_prev.vert.co - loop_prev.link_loop_next.vert.co
        vec_edge_prev.normalize()

        if f_normal_act:
            if f_normal_act != ZERO_VEC:
                f_normal_act = f_normal_act.normalized()
            else:
                f_normal_act = None
        if f_normal_prev:
            if f_normal_prev != ZERO_VEC:
                f_normal_prev = f_normal_prev.normalized()
            else:
                f_normal_prev = None

        f_cross = None
        vec_tangent = None
        if f_normal_act and f_normal_prev:
            f_angle = f_normal_act.angle(f_normal_prev)
            if threshold < f_angle < ANGLE_180 - threshold:
                vec_normal = f_normal_act + f_normal_prev
                vec_normal.normalize()
                f_cross = f_normal_act.cross(f_normal_prev)
                f_cross.normalize()
            elif f_angle > ANGLE_90:
                inner = self.get_inner_vec(loop_act)
                if inner:
                    vec_tangent = -inner
                else:
                    vec_tangent = vec_edge_act.cross(f_normal_act)
                    vec_tangent.normalize()
                corner_type = 'FACE_FOLD'
            else:
                vec_normal = f_normal_act
        elif f_normal_act or f_normal_prev:
            vec_normal = f_normal_act or f_normal_prev
        else:
            vec_normal = loop_act.face.normal.copy()
            if vec_normal == ZERO_VEC:
                if threshold < vec_edge_act.angle(Z_UP) < ANGLE_180 - threshold:
                    vec_normal = Z_UP - Z_UP.project(vec_edge_act)
                    vec_normal.normalize()
                else:
                    # vec_edge is parallel to Z_UP
                    vec_normal = Y_UP.copy()

        if vec_tangent is None:
            # 2d edge vectors are perpendicular to vec_normal
            vec_edge_act2d = vec_edge_act - vec_edge_act.project(vec_normal)
            vec_edge_act2d.normalize()

            vec_edge_prev2d = vec_edge_prev - vec_edge_prev.project(vec_normal)
            vec_edge_prev2d.normalize()

            angle2d = vec_edge_act2d.angle(vec_edge_prev2d)
            if angle2d < threshold:
                # folding corner
                corner_type = 'FOLD'
                vec_tangent = vec_edge_act2d
                vec_angle2d = ANGLE_360
            elif angle2d > ANGLE_180 - threshold:
                # straight corner
                corner_type = 'STRAIGHT'
                vec_tangent = vec_edge_act2d.cross(vec_normal)
                vec_angle2d = ANGLE_180
            else:
                direction = vec_edge_act2d.cross(vec_edge_prev2d).dot(vec_normal)
                if direction > .0:
                    # convex corner
                    corner_type = 'CONVEX'
                    vec_tangent = -(vec_edge_act2d + vec_edge_prev2d)
                    vec_angle2d = angle2d
                else:
                    # concave corner
                    corner_type = 'CONCAVE'
                    vec_tangent = vec_edge_act2d + vec_edge_prev2d
                    vec_angle2d = ANGLE_360 - angle2d

            if vec_tangent.dot(vec_normal):
                # Make vec_tangent perpendicular to vec_normal
                vec_tangent -= vec_tangent.project(vec_normal)

            vec_tangent.normalize()

        if f_cross:
            if vec_tangent.dot(f_cross) < .0:
                f_cross *= -1

            if corner_type == 'FOLD' or corner_type == 'STRAIGHT':
                vec_tangent = f_cross
            else:
                f_cross2d = f_cross - f_cross.project(vec_normal)
                s, t = decompose_vector(
                    f_cross2d, vec_edge_act2d, vec_edge_prev2d)
                if s * t < threshold:
                    # For the case in which vec_tangent is not
                    # between vec_edge_act2d and vec_edge_prev2d.
                    # Probably using 3d edge vectors is
                    # more intuitive than 2d edge vectors.
                    if corner_type == 'CONVEX':
                        vec_tangent = -(vec_edge_act + vec_edge_prev)
                    else:
                        # CONCAVE
                        vec_tangent = vec_edge_act + vec_edge_prev
                    vec_tangent.normalize()
                else:
                    vec_tangent = f_cross
        elif end_align and loop_act.vert in end_verts:
            inner = self.get_inner_vec(loop_act)
            if inner:
                vec_tangent = \
                    inner if inner.dot(vec_tangent) > .0 else -inner

        if corner_type == 'FOLD':
            factor_act = factor_prev = 0
        else:
            factor_act = 1. / sin(vec_tangent.angle(vec_edge_act))
            factor_prev = 1. / sin(vec_tangent.angle(vec_edge_prev))

        return vec_tangent, factor_act, factor_prev

    def execute(self, context):
        edit_object = context.edit_object
        me = edit_object.data
        #bm = bmesh.from_edit_mesh(me)  # This method causes blender crash
                                        # if an error occured during script
                                        # execution.
        bpy.ops.object.editmode_toggle()
        bm = bmesh.new()
        bm.from_mesh(me)

        mirror_planes = None
        if self.mirror_modifier:
            mirror_planes = self.get_mirror_planes(edit_object)

        e_loops = self.create_edgeloops(bm, mirror_planes)
        if e_loops is None:
            bm.free()
            bpy.ops.object.editmode_toggle()
            return {'CANCELLED'}

        fs = self.create_geometry(bm, e_loops)
        self.should_flip = should_flip =set()
        # includes faces, side faces around which should flip its normal
        # later in clean_geometry()

        # using self is slow, so take off self
        follow_face = self.follow_face
        if follow_face:
            e_fn_pairs = self.e_fn_pairs
        threshold = self.threshold
        skip_zero_length_edges = self.skip_zero_length_edges
        get_tangent = self.get_tangent
        end_align, end_verts = self.end_align_edge, self.end_verts
        is_hole = self.is_hole

        for f in fs:
            width = self.width if not self.flip else -self.width
            normal = f.normal if not follow_face else None
            move_vectors = []
            co_hole_check = self.limit_hole_check
            loop_act = loop_prev = None
            for floop in f.loops:
                if loop_act:
                    move_vectors.append(move_vectors[-1])
                    if floop is loop_act:
                        loop_prev = loop_act
                        loop_act = None
                    continue

                loop_act, skip_next_co = \
                    skip_zero_length_edges(floop, normal, reverse=False)
                if loop_act is None:
                    # All edges is zero length
                    break

                if loop_prev is None:
                    loop_prev = floop.link_loop_prev
                    loop_prev, skip_prev_co = \
                        skip_zero_length_edges(loop_prev, normal, reverse=True)

                if not follow_face:
                    n1, n2 = None, None
                else:
                    n1 = e_fn_pairs[loop_act.edge]
                    n2 = e_fn_pairs[loop_prev.edge]

                tangent = get_tangent(
                    loop_act, loop_prev, n1, n2, threshold,
                    end_align, end_verts)

                if follow_face and co_hole_check:
                    co_hole_check -= 1
                    hole = is_hole(loop_act, tangent[0])
                    if hole is not None:
                        co_hole_check = 0
                        if hole:
                            width *= -1
                            # side face normals should be flipped
                            should_flip.add(f)

                move_vectors.append(tangent)

                if floop is loop_act:
                    loop_prev = loop_act
                    loop_act = None

            for floop, vecs in zip(f.loops, move_vectors):
                vec_tan, factor_act, factor_prev = vecs
                floop.vert.co += \
                    width * min(factor_act, factor_prev) * vec_tan

        if self.mirror_modifier:
            self.apply_mirror()

        self.clean_geometry(bm)

        #bmesh.update_edit_mesh(me)
        bm.to_mesh(me)
        bm.free()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

    def invoke(self, context, event):
        edit_object = context.edit_object
        me = edit_object.data
        bpy.ops.object.editmode_toggle()
        for p in me.polygons:
            if p.select:
                self.follow_face = True
                break
        bpy.ops.object.editmode_toggle()

        self.mirror_modifier = False
        for m in edit_object.modifiers:
            if (m.type == 'MIRROR' and m.use_mirror_merge
               and m.show_viewport and m.show_in_editmode):
                self.mirror_modifier = True
                break

        return self.execute(context)


def draw_item(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator_menu_enum('mesh.offset_edges', 'geometry_mode')


def register():
    bpy.utils.register_class(OffsetEdges)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(draw_item)
    #bpy.types.VIEW3D_PT_tools_meshedit.append(draw_item)


def unregister():
    bpy.utils.unregister_class(OffsetEdges)
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(draw_item)
    #bpy.types.VIEW3D_PT_tools_meshedit.remove(draw_item)




########################################################################################################################################
########################################################################################################################################
############  Follow Path Operator  ####################################################################################################
############  Follow Path Operator  ####################################################################################################

###Follow Path Operator
#bl_info = {
    #"name": "FollowPathArray",
    #"author": "pink vertex",
    #"version": (1, 0),
    #"blender": (2, 69, 0),
    #"location": "Search Menu > FollowPathArray",
    #"description": "creates duplicates of an object with a follow-path-constraint",
    #"warning": "",
    #"wiki_url": "",
    #"tracker_url": "",
    #"category": "Object"}



def main(context,count,offset,type):
    obj=bpy.context.object
    ctr=get_constraint(obj)
    curve=ctr.target
    curve.data.use_path=True
    
    cyclic=0 if curve.data.splines[0].use_cyclic_u else 1
    
    group=bpy.data.groups.get("fpath.duplicates." + obj.name)
    if(group is None):
        group=bpy.data.groups.new("fpath.duplicates." + obj.name)
    
    for i in range(1,count+cyclic):
        dupli=obj.copy() #also copies constraints!
        group.objects.link(dupli)
        if  (type=="EVENLY_SPACED"):
            if cyclic==1:
                ctr.offset=0.0
            dupli.constraints[ctr.name].offset=-(curve.data.path_duration/count)*i+ctr.offset
        elif(type=="OFFSET"):
            dupli.constraints[ctr.name].offset=-(offset*i)+ctr.offset
        elif(type=="FIXED_POSITION"):
            dupli.constraints[ctr.name].offset_factor=offset*i+ctr.offset_factor
            dupli.constraints[ctr.name].use_fixed_location=True
    
    bpy.ops.object.fpath_link(group_name=group.name)
    
def check(context):
    obj=context.active_object
    if(obj is not None and len(obj.constraints)>=1):
        if(get_constraint(obj) is not None):
            return True;
    return False;

def get_constraint(obj):
    for ctr in obj.constraints:
        if(ctr.type=="FOLLOW_PATH" and ctr.target is not None):
            return ctr
    #nothing found
    return None

from bpy.props import FloatProperty, IntProperty, EnumProperty

class FollowPathArray(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.fpath_array"
    bl_label = "FollowPathArray"
    bl_options = {'REGISTER', 'UNDO'}
    
    type   = EnumProperty(
             name="type",
             items=[
             ("OFFSET"        , "offset",         "", 0),
             ("FIXED_POSITION", "fixed position", "", 1),
             ("EVENLY_SPACED" , "evenly spaced",  "", 2)
             ],
             default="OFFSET"
             )

    offset = FloatProperty(
             name="offset",
             description="offset",
             default=0.0
             )
   
    factor = FloatProperty(
             name="offset factor",
             description="offset factor",
             subtype="FACTOR",
             default=0.0,
             min=0.0,
             max=1.0
             )   
   
    count = IntProperty(
             name="count",
             description="number of duplicates",
             default=0,
             min=0,
             soft_max=100
             )
             
    @classmethod
    def poll(cls, context):
        return check(context)

    def execute(self, context):
        offset=self.offset if self.type=="OFFSET"         else\
               self.factor if self.type=="FIXED_POSITION" else\
               None
        main(context,self.count,offset,self.type)
        return {'FINISHED'}

    def draw(self, context):
        layout=self.layout
        col=layout.column()
        col.prop(self,"type","")
        col.prop(self,"count")
        if   self.type == "OFFSET":
            col.prop(self,"offset")
        elif self.type == "FIXED_POSITION":
            col.prop(self,"factor")        

class LinkToScene(bpy.types.Operator):
    bl_idname="object.fpath_link"
    bl_label="link to scene"
    bl_options={'INTERNAL'}
    
    from bpy.props import StringProperty
    
    group_name=StringProperty()
    
    def execute(self,context):
        group=bpy.data.groups[self.group_name]
        for obj in group.objects:
            if len(obj.users_scene)==0:
                context.scene.objects.link(obj)
        return {'FINISHED'}            
    

class loops14(bpy.types.Operator):
    """place a curve for follow path"""                 
    bl_idname = "object.loops14"          
    bl_label = "Follow Path Curve"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):

        bpy.ops.curve.primitive_bezier_circle_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.context.object.name = "Follow Path Curve"
        return {'FINISHED'}  
         

class loops15(bpy.types.Operator):
    """place a follow path constraint"""                 
    bl_idname = "object.loops15"          
    bl_label = "Follow Path Constraint"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):
     
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects["Follow Path Curve"]
        bpy.context.object.constraints["Follow Path"].use_curve_follow = True
        bpy.context.object.constraints["Follow Path"].forward_axis = 'FORWARD_X'



        return {'FINISHED'}                      
    
class loops16(bpy.types.Operator):
    """linked object from constraint"""                 
    bl_idname = "object.loops16"          
    bl_label = "linked object from constraint"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):
        
        bpy.ops.object.select_linked(type='OBDATA')     
        bpy.ops.object.visual_transform_apply()
        bpy.ops.object.constraints_clear()
        #bpy.ops.object.make_single_user(type='ALL', object=True, obdata=True)


        return {'FINISHED'}  


class loops17(bpy.types.Operator):
    """single objects & data from constraint"""                 
    bl_idname = "object.loops17"          
    bl_label = "single objects & data from constraint"                 
    bl_options = {'REGISTER', 'UNDO'}   


    def execute(self, context):
        
        bpy.ops.object.select_linked(type='OBDATA')     
        bpy.ops.object.visual_transform_apply()
        bpy.ops.object.constraints_clear()
        bpy.ops.object.make_single_user(type='ALL', object=True, obdata=True)


        return {'FINISHED'}  
        

    
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


################################################################################
#    Adaptation for Blender 2.5: Witold Jaworski (2011)
#    The code below is a fragment of original Geom Tools for Blender 2.4x
################################################################################
# ---------------- mesh_geom_tool_math.py (fragments) --------------------------
################################################################################

#CONSTANTS--------------------------------------------------

EPSILON = 0.001
DEBUG = 1 #set it to 0, for the "productive version"
#Functions--------------------------------------------------
def XYZvertexsort(verts):
    """ Sort a list of vertex with the most appropriate coordinate (x, y or z).
        Arguments:
        @verts (list): a list of vertices (MeshVertex instances).
        returns: the sorted list.
        NB: verts is modified.
    """
    ##sort the vertices to get a list of aligned point (normally :)
    verts.sort(key=lambda v: v.co.x)    #X coord sort
    vertstmp = list(verts)
    vertstmp.sort(key=lambda v: v.co.y) #Y coord sort

    #compare the x diff and the y diff
    diff  = abs(verts[0].co.x - verts[-1].co.x)
    diffy = abs(vertstmp[0].co.y - vertstmp[-1].co.y)
    if diff < diffy:
        verts, vertstmp = vertstmp, verts
        diff = diffy

    vertstmp.sort(key=lambda v: v.co.z) #Z coord sort

    #compare the x|y diff and the z diff
    if diff < abs((vertstmp[0].co.z - vertstmp[-1].co.z)):
        verts = vertstmp

    return verts

def project_point_vect(point, o, vect):
    """ Projection of a point on an 'affine vector'.
        Arguments:
        @point(Vector): the projected point
        @o (Vector): start extremity of the vector 
        @vect (Vector): direction vector 
        returns: the projected vector (Vector object)
    """
    t = (point - o)
    return o + t.project(vect)
# Classes -------------------------------------------------
class BezierInterpolator:
    """Interpolate a vertex loop/string with a bezier curve."""
    def __init__(self, vertloop):
        """Constructor.
            Arguments:
            @vertloop (list): the vertex loop a list of vertices (MeshVertex objects).
                              If it's a true loop (and not a simple string), the first and the last
                              vertices are the same vertex.
        """
        nodes = [None, None] #2 first nodes

        it = (v.co for v in vertloop)
        p0 = next(it)
        p1 = next(it)

        for p2 in it:
            vect = p2 - p0
            vect.normalize()

            nodes.append(p1 - (abs(vect.dot(p1-p0)) / 3.0) * vect)
            nodes.append(Vector(p1))
            nodes.append(p1 + (abs(vect.dot(p2-p1)) / 3.0) * vect)

            p0 = p1
            p1 = p2


        if vertloop[0].index == vertloop[-1].index: #it's a true loop
            p0 = vertloop[-2].co
            p1 = vertloop[0].co
            p2 = vertloop[1].co

            vect = p2 - p0
            vect.normalize()

            nodes[1] =   p1 + (abs(vect.dot(p2-p1)) / 3.0) * vect
            nodes.append(p1 - (abs(vect.dot(p1-p0)) / 3.0) * vect)

            tmpvect  = Vector(p0)
            nodes[0] = tmpvect
            nodes.append(tmpvect)

        else: #it's a 'false' loop: a simple edge string
            #1rst intermediate node
            p0  = vertloop[0].co
            p1  = vertloop[1].co
            p01 = nodes[2]

            nodes[0] = Vector(p0)
            nodes[1] = p0 - 2.0*project_point_vect(p01, p1, p0-p1) + p1 + p01

            #last one
            p0  = vertloop[-1].co
            p1  = vertloop[-2].co
            p01 = nodes[-1]

            nodes.append(p0 - 2.0*project_point_vect(p01, p1, p0-p1) + p1 + p01)
            nodes.append(Vector(p0))

        self._nodes = nodes

    def interpolate(self, t, vind):
        """ Interpolates 2 vertices of the original vertex loop.
            Arguments:
            @t (float): parameter for the bezier curve - between 0.0 and 1.0.
            @vind (int): the index of the first vertex, in the original loop
            returns Vector object (interpolation between vertloop[vind] and vertloop[vind+1])
        """
        _1_t  = 1.0 - t
        i     = 3 * vind
        nodes = self._nodes

        return nodes[i]                * (_1_t**3) + \
               nodes[i+1] * 3 *  t     * (_1_t**2) + \
               nodes[i+2] * 3 * (t**2) *  _1_t     + \
               nodes[i+3] *     (t**3)
################################################################################
# ---------------- mesh_geom_tool.py (fragments) -------------------------------
################################################################################

# general code -------------------------------------------------
def get_selected_vertices(mesh):
    """ Returns the list of selected vertices (there is nothing like this in current API)
        Arguments:
        @mesh (Mesh): the edited mesh datablock
    """
    return list(filter(lambda v: v.select, mesh.vertices))

def get_selected_edges(mesh):
    """ Returns the list of selected edges (there is nothing like this in current API)
        Arguments:
        @mesh (Mesh): the edited mesh datablock
    """
    return list(filter(lambda e: e.select, mesh.edges))

# align vertices --------------------------------------

def align_vertices(mesh, distr):
    """Distribute vertices regularly or align them.
        Arguments:
        @mesh (Mesh): the edited mesh datablock
        @distr (Bool): True, when to perform align & distribute
    """
    vsel = get_selected_vertices(mesh)

    if len(vsel) < 3:
        raise Exception("need 3 vertices at least")


    vsel  = XYZvertexsort(vsel)
    point = vsel[0].co
    vect  = (vsel[-1].co - point) * (1.0/(len(vsel)-1))

    if vect.length < EPSILON: return

    if distr == True: #align & distribute
        for mult, vert in enumerate(islice(vsel, 1, len(vsel)-1)):
            v = vert.co
            finalv = (mult+1) * vect + point
            v.x = finalv.x
            v.y = finalv.y
            v.z = finalv.z

    else: #align only
        for vert in islice(vsel, 1, len(vsel)-1):
            v = vert.co
            finalv = project_point_vect(v, point, vect)
            v.x = finalv.x
            v.y = finalv.y
            v.z = finalv.z

    mesh.update()

# distribute vertices ------------------------------------------
class EdgeVert(object):
    """Helper structure: a vertex of an edge."""
    __slots__ = ('edge', 'vind')

    def __init__(self, edge, vind):
        self.edge = edge  #MeshEdge object
        self.vind = vind  #index of vertex for the edge (1 or 2)

def vertex_string(edict, vert):
    """ Builds a list of edge-connected vertex indices.
        Arguments:
        @edict (dict): edge dictionary {vextex_index, [list_of_EdgeVert_linked_to_this_vertex]}
        @vert (int): the index of 1rst vertex of the vertex string.
        returns: the list of vertex indices.
    """
    vlist = [vert]
    vind  = vert

    try:
        while True:
            convert = edict[vind].pop() #connected vertex
            edge    = convert.edge

            if convert.vind == 1: v2add = edge.vertices[1]
            else:                 v2add = edge.vertices[0]

            vind = v2add
            vlist.append(v2add)

            lst = edict[vind]

            for i, elt in enumerate(lst):
                if elt.edge.index == edge.index:
                    del lst[i]
                    break
    except KeyError:   pass #edict[vind] with vind not a valid key
    except IndexError: pass #pop() on an empty list

    return vlist

def get_loop(edges, verts):
    """ Return a 'loop' of vertices edge-connected (loop[N] and loop[N+1] are edge-connected).
        Arguments:
        @edges(list): list of selected edges (MeshEdge objects).
        @verts(list): list of selected vertices (MeshVertex objects).
        returns: a list of MeshVertex objects
        NB: if the loop is a 'true loop' (and not a simple string), the first
        and the last vertex of the list are the same.
    """
    e = edges.pop() #we need an edge to begin
    
    edict = dict((v.index, []) for v in verts)
    for edge in edges:
        edict[edge.vertices[0]].append(EdgeVert(edge, 1))
        edict[edge.vertices[1]].append(EdgeVert(edge, 2))

    looptmp = vertex_string(edict, e.vertices[0])
    loop    = vertex_string(edict, e.vertices[1])

    for val in edict.values():
        if val: raise Exception("need an edge loop")

    loop.reverse()
    loop.extend(looptmp)
    
    vdict = dict((v.index, v) for v in verts) #dictionary of vertices, by their index
    
    return list(vdict[i] for i in loop) #build the list of vertex objects...

def loop_size(loop):
    """ Get the geometric length of a vertex loop.
        Arguments:
        @loop(list): vertices (MeshVertex objects).
        returns: the length (float).
    """
    size = 0.0
    vects = (v.co for v in loop)
    v1    = next(vects)

    for v2 in vects:
        size += (v2-v1).length
        v1 = v2

    return size

def distribute_vertices(mesh):
    """ Distribute vertices regularly on a curve.
        Arguments:
        @mesh (Mesh): the mesh datablock, containing the vertices
    """
    vsel = get_selected_vertices(mesh)

    if len(vsel) < 3:
        raise Exception("need 3 vertices at least")
    
    loop   = get_loop(get_selected_edges(mesh), vsel)
    interp = BezierInterpolator(loop)

    new_coords = []
    average    = loop_size(loop) / (len(loop)-1)

    vects = (v.co for v in loop)
    v1    = next(vects)
    v2    = next(vects)
    index = 0

    size_acc = 0.0             #size accumulator
    vec_len  = (v2-v1).length

    for coeff in (average*i for i in range(1, len(loop)-1)):
        while coeff > (size_acc+vec_len):
            size_acc += vec_len
            v1 = v2
            v2 = next(vects)
            index += 1
            vec_len = (v2-v1).length

        #here we have: size_acc < coeff < (size_acc+vec_len)
        # ~~> coeff 'between' v1 & v2
        new_coords.append(interp.interpolate((coeff-size_acc)/vec_len, index))


    it = iter(loop)
    next(it) #begin with the 2nd vertex
    for coord in new_coords:
        v   = next(it).co
        v.x = coord.x
        v.y = coord.y
        v.z = coord.z

    mesh.update()


    
##############################################################################################################################
##############################################################################################################################
###########  Vertex Tools  ###################################################################################################
###########  Vertex Tools  ###################################################################################################

    
################################################################################
# ---------------- Add-On implementation ---------------------------------------
################################################################################
#bl_info = {
#    "name": "Vertex Tools",
#    "author": "Guillaume Englert, Witold Jaworski",
#    "version": (1, 0, 1),
#    "blender": (2, 5, 7),
#    "api": 36147,
#    "location": "View 3D > Mesh > Vertex >Align & Distribute",
#    "category": "Mesh",
#    "description": "Align or distribute selected vertices (from the old Geom Tool)",
#    "warning": "",
#    "tracker_url": "http://airplanes3d.net/track-254_e.xml",
#    "wiki_url": "http://airplanes3d.net/scripts-254_e.xml"
#    }

#common base for operators:
#just to not implement the same checks twice
class VertexOperator:
    #--- methods to override:
    def action(self,mesh):
        """Override this function in the children classes
            Arguments:
            @mesh (Mesh): the mesh datablock with selected vertices
            NB: this method can throw exceptions!
        """
        pass #default implementation: empty
    
    def show(self, msg): 
        """Override this function to use the Operator.report method
            Arguments:
            @msg (str): the message to be displayed 
        """
        print(msg)
        
    #--- common implementation of the Operator interface: 
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def invoke(self, context, event):
        return self.execute(context)
        
    def execute(self, context):
        mesh = context.object.data
        bpy.ops.object.editmode_toggle()
        result = 'FINISHED'
        try:
            self.action(mesh)
            
        except Exception as e:
            if len(e.args) > 0 :
                msg = e.args[0]
            else:
                msg = "Error: " + exc_info()[1]
                
            self.show(msg)
            
            result = 'CANCELLED'
        bpy.ops.object.editmode_toggle()
        return {result}
    
# operators --------------------------------------------------------------------
class DistributeVertices(bpy.types.Operator, VertexOperator):
    ''' Distribute vertices evenly along interpolated shape of their polyline 
    '''
    bl_idname = "mesh.vertex_distribute"
    bl_label = "Vertex Distribute"
    bl_description = "Distribute selected vertices evenly along their loop"
    
    def show(self, msg):
        self.report('ERROR', message = msg) 
    
    def action(self, mesh):
        distribute_vertices(mesh)

class AlignVertices(bpy.types.Operator, VertexOperator):
    ''' Project vertices onto the line between the first and last selected vertex 
    '''
    bl_idname = "mesh.vertex_align"
    bl_label = "Vertex Align"
    bl_description = "Project vertices onto the line between the first and last selected vertex"
    
    def show(self, msg):
        self.report('ERROR', message = msg) 
    
    def action(self, mesh):
        align_vertices(mesh,False)

class InlineVertices(bpy.types.Operator, VertexOperator):
    ''' Place vertices evenly along straight line 
    '''
    bl_idname = "mesh.vertex_inline"
    bl_label = "Vertex Align & Distribute"
    bl_description = "Distribute vertices evenly along a straight line"
    
    def show(self, msg):
        self.report('ERROR', message = msg) 
    
    def action(self, mesh):
        align_vertices(mesh,True)

def menu_draw(self, context):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.separator()
        self.layout.operator(DistributeVertices.bl_idname, "Distribute")
        self.layout.operator(AlignVertices.bl_idname, "Align")
        self.layout.operator(InlineVertices.bl_idname, "Align & Distribute")

#--- ### Register
def register():
    register_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_draw)
    bpy.types.WindowManager.extend_func = BoolProperty(default=False)
    bpy.types.WindowManager.rotface_func = BoolProperty(default=False)
    bpy.types.WindowManager.cad_func = BoolProperty(default=False)
    bpy.types.WindowManager.align_func = BoolProperty(default=False)    

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_draw)

    unregister_module(__name__)




#####################################################################################################################################
#####################################################################################################################################    
##############  Copy Attributes Menu  ###############################################################################################
##############  Copy Attributes Menu  ###############################################################################################


#bl_info = {
#    "name": "Copy Attributes Menu",
#    "author": "Bassam Kurdali, Fabian Fricke, Adam Wiseman",
#    "version": (0, 4, 7),
#    "blender": (2, 63, 0),
#    "location": "View3D > Ctrl-C",
#    "description": "Copy Attributes Menu from Blender 2.4",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
#                "Scripts/3D_interaction/Copy_Attributes_Menu",
#    "tracker_url": "https://developer.blender.org/T22588",
#    "category": "3D View"}




def build_exec(loopfunc, func):
    """Generator function that returns exec functions for operators """

    def exec_func(self, context):
        loopfunc(self, context, func)
        return {'FINISHED'}
    return exec_func


def build_invoke(loopfunc, func):
    """Generator function that returns invoke functions for operators"""

    def invoke_func(self, context, event):
        loopfunc(self, context, func)
        return {'FINISHED'}
    return invoke_func


def build_op(idname, label, description, fpoll, fexec, finvoke):
    """Generator function that returns the basic operator"""

    class myopic(bpy.types.Operator):
        bl_idname = idname
        bl_label = label
        bl_description = description
        execute = fexec
        poll = fpoll
        invoke = finvoke
    return myopic


def genops(copylist, oplist, prefix, poll_func, loopfunc):
    """Generate ops from the copy list and its associated functions """
    for op in copylist:
        exec_func = build_exec(loopfunc, op[3])
        invoke_func = build_invoke(loopfunc, op[3])
        opclass = build_op(prefix + op[0], "Copy " + op[1], op[2],
           poll_func, exec_func, invoke_func)
        oplist.append(opclass)


def generic_copy(source, target, string=""):
    """ copy attributes from source to target that have string in them """
    for attr in dir(source):
        if attr.find(string) > -1:
            try:
                setattr(target, attr, getattr(source, attr))
            except:
                pass
    return


def getmat(bone, active, context, ignoreparent):
    """Helper function for visual transform copy,
       gets the active transform in bone space
    """
    obj_act = context.active_object
    data_bone = obj_act.data.bones[bone.name]
    #all matrices are in armature space unless commented otherwise
    otherloc = active.matrix  # final 4x4 mat of target, location.
    bonemat_local = data_bone.matrix_local.copy()  # self rest matrix
    if data_bone.parent:
        parentposemat = obj_act.pose.bones[data_bone.parent.name].matrix.copy()
        parentbonemat = data_bone.parent.matrix_local.copy()
    else:
        parentposemat = parentbonemat = Matrix()
    if parentbonemat == parentposemat or ignoreparent:
        newmat = bonemat_local.inverted() * otherloc
    else:
        bonemat = parentbonemat.inverted() * bonemat_local

        newmat = bonemat.inverted() * parentposemat.inverted() * otherloc
    return newmat


def rotcopy(item, mat):
    """copy rotation to item from matrix mat depending on item.rotation_mode"""
    if item.rotation_mode == 'QUATERNION':
        item.rotation_quaternion = mat.to_3x3().to_quaternion()
    elif item.rotation_mode == 'AXIS_ANGLE':
        quat = mat.to_3x3().to_quaternion()
        item.rotation_axis_angle = quat.axis[:] + (quat.angle, )
    else:
        item.rotation_euler = mat.to_3x3().to_euler(item.rotation_mode)


def pLoopExec(self, context, funk):
    """Loop over selected bones and execute funk on them"""
    active = context.active_pose_bone
    selected = context.selected_pose_bones
    selected.remove(active)
    for bone in selected:
        funk(bone, active, context)

#The following functions are used o copy attributes frome active to bone


def pLocLocExec(bone, active, context):
    bone.location = active.location


def pLocRotExec(bone, active, context):
    rotcopy(bone, active.matrix_basis.to_3x3())


def pLocScaExec(bone, active, context):
    bone.scale = active.scale


def pVisLocExec(bone, active, context):
    bone.location = getmat(bone, active, context, False).to_translation()


def pVisRotExec(bone, active, context):
    rotcopy(bone, getmat(bone, active,
      context, not context.active_object.data.bones[bone.name].use_inherit_rotation))


def pVisScaExec(bone, active, context):
    bone.scale = getmat(bone, active, context,
       not context.active_object.data.bones[bone.name].use_inherit_scale)\
          .to_scale()


def pDrwExec(bone, active, context):
    bone.custom_shape = active.custom_shape


def pLokExec(bone, active, context):
    for index, state in enumerate(active.lock_location):
        bone.lock_location[index] = state
    for index, state in enumerate(active.lock_rotation):
        bone.lock_rotation[index] = state
    bone.lock_rotations_4d = active.lock_rotations_4d
    bone.lock_rotation_w = active.lock_rotation_w
    for index, state in enumerate(active.lock_scale):
        bone.lock_scale[index] = state


def pConExec(bone, active, context):
    for old_constraint in  active.constraints.values():
        new_constraint = bone.constraints.new(old_constraint.type)
        generic_copy(old_constraint, new_constraint)


def pIKsExec(bone, active, context):
    generic_copy(active, bone, "ik_")


def pBBonesExec(bone, active, context):
    object = active.id_data
    generic_copy(
        object.data.bones[active.name], 
        object.data.bones[bone.name],
        "bbone_")

pose_copies = (('pose_loc_loc', "Local Location",
                "Copy Location from Active to Selected", pLocLocExec),
                ('pose_loc_rot', "Local Rotation",
                "Copy Rotation from Active to Selected", pLocRotExec),
                ('pose_loc_sca', "Local Scale",
                "Copy Scale from Active to Selected", pLocScaExec),
                ('pose_vis_loc', "Visual Location",
                "Copy Location from Active to Selected", pVisLocExec),
                ('pose_vis_rot', "Visual Rotation",
                "Copy Rotation from Active to Selected", pVisRotExec),
                ('pose_vis_sca', "Visual Scale",
                "Copy Scale from Active to Selected", pVisScaExec),
                ('pose_drw', "Bone Shape",
                "Copy Bone Shape from Active to Selected", pDrwExec),
                ('pose_lok', "Protected Transform",
                "Copy Protected Tranforms from Active to Selected", pLokExec),
                ('pose_con', "Bone Constraints",
                "Copy Object Constraints from Active to Selected", pConExec),
                ('pose_iks', "IK Limits",
                "Copy IK Limits from Active to Selected", pIKsExec),
                ('bbone_settings', "BBone Settings",
                "Copy BBone Settings from Active to Selected", pBBonesExec),)


@classmethod
def pose_poll_func(cls, context):
    return(context.mode == 'POSE')


def pose_invoke_func(self, context, event):
    wm = context.window_manager
    wm.invoke_props_dialog(self)
    return {'RUNNING_MODAL'}


class CopySelectedPoseConstraints(bpy.types.Operator):
    """Copy Chosen constraints from active to selected"""
    bl_idname = "pose.copy_selected_constraints"
    bl_label = "Copy Selected Constraints"
    selection = bpy.props.BoolVectorProperty(size=32)

    poll = pose_poll_func
    invoke = pose_invoke_func

    def draw(self, context):
        layout = self.layout
        for idx, const in enumerate(context.active_pose_bone.constraints):
            layout.prop(self, "selection", index=idx, text=const.name,
               toggle=True)

    def execute(self, context):
        active = context.active_pose_bone
        selected = context.selected_pose_bones[:]
        selected.remove(active)
        for bone in selected:
            for index, flag in enumerate(self.selection):
                if flag:
                    old_constraint = active.constraints[index]
                    new_constraint = bone.constraints.new(\
                       active.constraints[index].type)
                    generic_copy(old_constraint, new_constraint)
        return {'FINISHED'}

pose_ops = []  # list of pose mode copy operators

genops(pose_copies, pose_ops, "pose.copy_", pose_poll_func, pLoopExec)


class VIEW3D_MT_posecopypopup(bpy.types.Menu):
    bl_label = "Copy Attributes"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        for op in pose_copies:
            layout.operator("pose.copy_" + op[0])
        layout.operator("pose.copy_selected_constraints")
        layout.operator("pose.copy", text="copy pose")


def obLoopExec(self, context, funk):
    """Loop over selected objects and execute funk on them"""
    active = context.active_object
    selected = context.selected_objects[:]
    selected.remove(active)
    for obj in selected:
        msg = funk(obj, active, context)
    if msg:
        self.report({msg[0]}, msg[1])


def world_to_basis(active, ob, context):
    """put world coords of active as basis coords of ob"""
    local = ob.parent.matrix_world.inverted() * active.matrix_world
    P = ob.matrix_basis * ob.matrix_local.inverted()
    mat = P * local
    return(mat)

#The following functions are used o copy attributes from
#active to selected object


def obLoc(ob, active, context):
    ob.location = active.location


def obRot(ob, active, context):
    rotcopy(ob, active.matrix_local.to_3x3())


def obSca(ob, active, context):
    ob.scale = active.scale


def obVisLoc(ob, active, context):
    if ob.parent:
        mat = world_to_basis(active, ob, context)
        ob.location = mat.to_translation()
    else:
        ob.location = active.matrix_world.to_translation()


def obVisRot(ob, active, context):
    if ob.parent:
        mat = world_to_basis(active, ob, context)
        rotcopy(ob, mat.to_3x3())
    else:
        rotcopy(ob, active.matrix_world.to_3x3())


def obVisSca(ob, active, context):
    if ob.parent:
        mat = world_to_basis(active, ob, context)
        ob.scale = mat.to_scale()
    else:
        ob.scale = active.matrix_world.to_scale()


def obDrw(ob, active, context):
    ob.draw_type = active.draw_type
    ob.show_axis = active.show_axis
    ob.show_bounds = active.show_bounds
    ob.draw_bounds_type = active.draw_bounds_type
    ob.show_name = active.show_name
    ob.show_texture_space = active.show_texture_space
    ob.show_transparent = active.show_transparent
    ob.show_wire = active.show_wire
    ob.show_x_ray = active.show_x_ray
    ob.empty_draw_type = active.empty_draw_type
    ob.empty_draw_size = active.empty_draw_size


def obOfs(ob, active, context):
    ob.time_offset = active.time_offset
    return('INFO', "time offset copied")


def obDup(ob, active, context):
    generic_copy(active, ob, "dupli")
    return('INFO', "duplication method copied")


def obCol(ob, active, context):
    ob.color = active.color


def obMas(ob, active, context):
    ob.game.mass = active.game.mass
    return('INFO', "mass copied")


def obLok(ob, active, context):
    for index, state in enumerate(active.lock_location):
        ob.lock_location[index] = state
    for index, state in enumerate(active.lock_rotation):
        ob.lock_rotation[index] = state
    ob.lock_rotations_4d = active.lock_rotations_4d
    ob.lock_rotation_w = active.lock_rotation_w
    for index, state in enumerate(active.lock_scale):
        ob.lock_scale[index] = state
    return('INFO', "transform locks copied")


def obCon(ob, active, context):
    #for consistency with 2.49, delete old constraints first
    for removeconst in ob.constraints:
        ob.constraints.remove(removeconst)
    for old_constraint in  active.constraints.values():
        new_constraint = ob.constraints.new(old_constraint.type)
        generic_copy(old_constraint, new_constraint)
    return('INFO', "constraints copied")


def obTex(ob, active, context):
    if 'texspace_location' in dir(ob.data) and 'texspace_location' in dir(
       active.data):
        ob.data.texspace_location[:] = active.data.texspace_location[:]
    if 'texspace_size' in dir(ob.data) and 'texspace_size' in dir(active.data):
        ob.data.texspace_size[:] = active.data.texspace_size[:]
    return('INFO', "texture space copied")


def obIdx(ob, active, context):
    ob.pass_index = active.pass_index
    return('INFO', "pass index copied")


def obMod(ob, active, context):
    for modifier in ob.modifiers:
        #remove existing before adding new:
        ob.modifiers.remove(modifier)
    for old_modifier in active.modifiers.values():
        new_modifier = ob.modifiers.new(name=old_modifier.name,
           type=old_modifier.type)
        generic_copy(old_modifier, new_modifier)
    return('INFO', "modifiers copied")


def obGrp(ob, active, context):
    for grp in bpy.data.groups:
        if active.name in grp.objects and ob.name not in grp.objects:
            grp.objects.link(ob)
    return('INFO', "groups copied")


def obWei(ob, active, context):
    me_source = active.data
    me_target = ob.data
    # sanity check: do source and target have the same amount of verts?
    if len(me_source.vertices) != len(me_target.vertices):
        return('ERROR', "objects have different vertex counts, doing nothing")
    vgroups_IndexName = {}
    for i in range(0, len(active.vertex_groups)):
        groups = active.vertex_groups[i]
        vgroups_IndexName[groups.index] = groups.name
    data = {}  # vert_indices, [(vgroup_index, weights)]
    for v in me_source.vertices:
        vg = v.groups
        vi = v.index
        if len(vg) > 0:
            vgroup_collect = []
            for i in range(0, len(vg)):
                vgroup_collect.append((vg[i].group, vg[i].weight))
            data[vi] = vgroup_collect
    # write data to target
    if ob != active:
        # add missing vertex groups
        for vgroup_name in vgroups_IndexName.values():
            #check if group already exists...
            already_present = 0
            for i in range(0, len(ob.vertex_groups)):
                if ob.vertex_groups[i].name == vgroup_name:
                    already_present = 1
            # ... if not, then add
            if already_present == 0:
                ob.vertex_groups.new(name=vgroup_name)
        # write weights
        for v in me_target.vertices:
            for vi_source, vgroupIndex_weight in data.items():
                if v.index == vi_source:

                    for i in range(0, len(vgroupIndex_weight)):
                        groupName = vgroups_IndexName[vgroupIndex_weight[i][0]]
                        groups = ob.vertex_groups
                        for vgs in range(0, len(groups)):
                            if groups[vgs].name == groupName:
                                groups[vgs].add((v.index,),
                                   vgroupIndex_weight[i][1], "REPLACE")
    return('INFO', "weights copied")

object_copies = (
                #('obj_loc', "Location",
                #"Copy Location from Active to Selected", obLoc),
                #('obj_rot', "Rotation",
                #"Copy Rotation from Active to Selected", obRot),
                #('obj_sca', "Scale",
                #"Copy Scale from Active to Selected", obSca),
                ('obj_vis_loc', "Location",
                "Copy Location from Active to Selected", obVisLoc),
                ('obj_vis_rot', "Rotation",
                "Copy Rotation from Active to Selected", obVisRot),
                ('obj_vis_sca', "Scale",
                "Copy Scale from Active to Selected", obVisSca),
                ('obj_drw', "Draw Options",
                "Copy Draw Options from Active to Selected", obDrw),
                ('obj_ofs', "Time Offset",
                "Copy Time Offset from Active to Selected", obOfs),
                ('obj_dup', "Dupli",
                "Copy Dupli from Active to Selected", obDup),
                ('obj_col', "Object Color",
                "Copy Object Color from Active to Selected", obCol),
                ('obj_mas', "Mass",
                "Copy Mass from Active to Selected", obMas),
                #('obj_dmp', "Damping",
                #"Copy Damping from Active to Selected"),
                #('obj_all', "All Physical Attributes",
                #"Copy Physical Atributes from Active to Selected"),
                #('obj_prp', "Properties",
                #"Copy Properties from Active to Selected"),
                #('obj_log', "Logic Bricks",
                #"Copy Logic Bricks from Active to Selected"),
                ('obj_lok', "Protected Transform",
                "Copy Protected Tranforms from Active to Selected", obLok),
                ('obj_con', "Object Constraints",
                "Copy Object Constraints from Active to Selected", obCon),
                #('obj_nla', "NLA Strips",
                #"Copy NLA Strips from Active to Selected"),
                #('obj_tex', "Texture Space",
                #"Copy Texture Space from Active to Selected", obTex),
                #('obj_sub', "Subsurf Settings",
                #"Copy Subsurf Setings from Active to Selected"),
                #('obj_smo', "AutoSmooth",
                #"Copy AutoSmooth from Active to Selected"),
                ('obj_idx', "Pass Index",
                "Copy Pass Index from Active to Selected", obIdx),
                ('obj_mod', "Modifiers",
                "Copy Modifiers from Active to Selected", obMod),
                ('obj_wei', "Vertex Weights",
                "Copy vertex weights based on indices", obWei),
                ('obj_grp', "Group Links",
                "Copy selected into active object's groups", obGrp))


@classmethod
def object_poll_func(cls, context):
    return(len(context.selected_objects) > 1)


def object_invoke_func(self, context, event):
    wm = context.window_manager
    wm.invoke_props_dialog(self)
    return {'RUNNING_MODAL'}


class CopySelectedObjectConstraints(bpy.types.Operator):
    """Copy Chosen constraints from active to selected"""
    bl_idname = "object.copy_selected_constraints"
    bl_label = "Copy Selected Constraints"
    selection = bpy.props.BoolVectorProperty(size=32)

    poll = object_poll_func

    invoke = object_invoke_func

    def draw(self, context):
        layout = self.layout
        for idx, const in enumerate(context.active_object.constraints):
            layout.prop(self, "selection", index=idx, text=const.name,
               toggle=True)

    def execute(self, context):
        active = context.active_object
        selected = context.selected_objects[:]
        selected.remove(active)
        for obj in selected:
            for index, flag in enumerate(self.selection):
                if flag:
                    old_constraint = active.constraints[index]
                    new_constraint = obj.constraints.new(\
                       active.constraints[index].type)
                    generic_copy(old_constraint, new_constraint)
        return{'FINISHED'}


class CopySelectedObjectModifiers(bpy.types.Operator):
    """Copy Chosen modifiers from active to selected"""
    bl_idname = "object.copy_selected_modifiers"
    bl_label = "Copy Selected Modifiers"
    selection = bpy.props.BoolVectorProperty(size=32)

    poll = object_poll_func

    invoke = object_invoke_func

    def draw(self, context):
        layout = self.layout
        for idx, const in enumerate(context.active_object.modifiers):
            layout.prop(self, 'selection', index=idx, text=const.name,
               toggle=True)

    def execute(self, context):
        active = context.active_object
        selected = context.selected_objects[:]
        selected.remove(active)
        for obj in selected:
            for index, flag in enumerate(self.selection):
                if flag:
                    old_modifier = active.modifiers[index]
                    new_modifier = obj.modifiers.new(\
                       type=active.modifiers[index].type,
                       name=active.modifiers[index].name)
                    generic_copy(old_modifier, new_modifier)
        return{'FINISHED'}

object_ops = []
genops(object_copies, object_ops, "object.copy_", object_poll_func, obLoopExec)


class VIEW3D_MT_copypopup(bpy.types.Menu):
    bl_label = "Copy Attributes"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        for op in object_copies:
            layout.operator("object.copy_" + op[0])
        layout.operator("object.copy_selected_constraints")
        layout.operator("object.copy_selected_modifiers")

#Begin Mesh copy settings:


class MESH_MT_CopyFaceSettings(bpy.types.Menu):
    bl_label = "Copy Face Settings"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def draw(self, context):
        mesh = context.object.data
        uv = len(mesh.uv_textures) > 1
        vc = len(mesh.vertex_colors) > 1
        layout = self.layout

        op = layout.operator(MESH_OT_CopyFaceSettings.bl_idname,
                        text="Copy Material")
        op['layer'] = ''
        op['mode'] = 'MAT'
        if mesh.uv_textures.active:
            op = layout.operator(MESH_OT_CopyFaceSettings.bl_idname,
                            text="Copy Image")
            op['layer'] = ''
            op['mode'] = 'IMAGE'
            op = layout.operator(MESH_OT_CopyFaceSettings.bl_idname,
                            text="Copy UV Coords")
            op['layer'] = ''
            op['mode'] = 'UV'
        if mesh.vertex_colors.active:
            op = layout.operator(MESH_OT_CopyFaceSettings.bl_idname,
                            text="Copy Vertex Colors")
            op['layer'] = ''
            op['mode'] = 'VCOL'
        if uv or vc:
            layout.separator()
            if uv:
                layout.menu("MESH_MT_CopyImagesFromLayer")
                layout.menu("MESH_MT_CopyUVCoordsFromLayer")
            if vc:
                layout.menu("MESH_MT_CopyVertexColorsFromLayer")


def _buildmenu(self, mesh, mode):
    layout = self.layout
    if mode == 'VCOL':
        layers = mesh.vertex_colors
    else:
        layers = mesh.uv_textures
    for layer in layers:
        if not layer.active:
            op = layout.operator(MESH_OT_CopyFaceSettings.bl_idname,
                                 text=layer.name)
            op['layer'] = layer.name
            op['mode'] = mode


@classmethod
def _poll_layer_uvs(cls, context):
    return context.mode == "EDIT_MESH" and len(
       context.object.data.uv_layers) > 1


@classmethod
def _poll_layer_vcols(cls, context):
    return context.mode == "EDIT_MESH" and len(
       context.object.data.vertex_colors) > 1


def _build_draw(mode):
    return (lambda self, context: _buildmenu(self, context.object.data, mode))

_layer_menu_data = (("UV Coords", _build_draw("UV"), _poll_layer_uvs),
                    ("Images", _build_draw("IMAGE"), _poll_layer_uvs),
                    ("Vertex Colors", _build_draw("VCOL"), _poll_layer_vcols))
_layer_menus = []
for name, draw_func, poll_func in _layer_menu_data:
    classname = "MESH_MT_Copy" + "".join(name.split()) + "FromLayer"
    menuclass = type(classname, (bpy.types.Menu,),
                     dict(bl_label="Copy " + name + " from layer",
                          bl_idname=classname,
                          draw=draw_func,
                          poll=poll_func))
    _layer_menus.append(menuclass)


class MESH_OT_CopyFaceSettings(bpy.types.Operator):
    """Copy settings from active face to all selected faces"""
    bl_idname = 'mesh.copy_face_settings'
    bl_label = "Copy Face Settings"
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.StringProperty(name="mode")
    layer = bpy.props.StringProperty(name="layer")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        mode = getattr(self, 'mode', '')
        if not mode in {'MAT', 'VCOL', 'IMAGE', 'UV'}:
            self.report({'ERROR'}, "No mode specified or invalid mode.")
            return self._end(context, {'CANCELLED'})
        layername = getattr(self, 'layer', '')
        mesh = context.object.data

        # Switching out of edit mode updates the selected state of faces and
        # makes the data from the uv texture and vertex color layers available.
        bpy.ops.object.editmode_toggle()

        polys = mesh.polygons
        if mode == 'MAT':
            to_data = from_data = polys
        else:
            if mode == 'VCOL':
                layers = mesh.vertex_colors
                act_layer = mesh.vertex_colors.active
            elif mode == 'IMAGE':
                layers = mesh.uv_textures
                act_layer = mesh.uv_textures.active
            elif mode == 'UV':
                layers = mesh.uv_layers
                act_layer = mesh.uv_layers.active
            if not layers or (layername and not layername in layers):
                self.report({'ERROR'}, "Invalid UV or color layer.")
                return self._end(context, {'CANCELLED'})
            from_data = layers[layername or act_layer.name].data
            to_data = act_layer.data
        from_index = polys.active

        for f in polys:
            if f.select:
                if to_data != from_data:
                    # Copying from another layer.
                    # from_face is to_face's counterpart from other layer.
                    from_index = f.index
                elif f.index == from_index:
                    # Otherwise skip copying a face to itself.
                    continue
                if mode == 'MAT':
                    f.material_index = polys[from_index].material_index
                    continue
                elif mode == 'IMAGE':
                    to_data[f.index].image = from_data[from_index].image
                    continue
                if len(f.loop_indices) != len(polys[from_index].loop_indices):
                    self.report({'WARNING'}, "Different number of vertices.")
                for i in range(len(f.loop_indices)):
                    to_vertex = f.loop_indices[i]
                    from_vertex = polys[from_index].loop_indices[i]
                    if mode == 'VCOL':
                        to_data[to_vertex].color = from_data[from_vertex].color
                    elif mode == 'UV':
                        to_data[to_vertex].uv = from_data[from_vertex].uv

        return self._end(context, {'FINISHED'})

    def _end(self, context, retval):
        if context.mode != 'EDIT_MESH':
            # Clean up by returning to edit mode like it was before.
            bpy.ops.object.editmode_toggle()
        return(retval)



##########################################################################################################
##########################################################################################################
############  Tri-Lighting Creator  ######################################################################
############  Tri-Lighting Creator  ######################################################################


#bl_info = {
#    "name": "Tri-Lighting Creator",
#    "category": "Object",
#    "author": "Daniel Schalla",
#    "version": (1, 0),
#    "blender": (2, 68, 0),
#    "location": "Object Mode > Toolbar > Add Tri-Lighting",
#    "description": "Add 3 Point Lighting to selected Object"
#}


class TriLighting(bpy.types.Operator):
    """TriL ightning"""
    bl_idname = "object.trilighting"        # unique identifier for buttons and menu items to reference.
    bl_label = "Tri-Lighting Creator"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    height = bpy.props.FloatProperty(name="Height", default=5)
    distance = bpy.props.FloatProperty(name="Distance",default=5,min=0.1,subtype="DISTANCE")
    energy = bpy.props.IntProperty(name="Base Energy",default=3,min=1)
    contrast = bpy.props.IntProperty(name="Contrast",default=50,min=-100,max=100,subtype="PERCENTAGE")
    leftangle = bpy.props.IntProperty(name="Left Angle", default=26, min=1, max=90, subtype="ANGLE")
    rightangle = bpy.props.IntProperty(name="Right Angle", default=45, min=1, max=90, subtype="ANGLE")
    backangle = bpy.props.IntProperty(name="Back Angle", default=235, min=90, max=270, subtype="ANGLE")


    Light_Type_List = [('POINT','Point','Point Light'),
                        ('SUN','Sun','Sun Light'),
                        ('SPOT','Spot','Spot Light'),
                        ('HEMI','Hemi','Hemi Light'),
                        ('AREA','Area','Area Light')]
    primarytype = EnumProperty( attr='tl_type',
            name='Key Type',
            description='Choose the type off Key Light you would like',
            items = Light_Type_List, default = 'HEMI')

    secondarytype = EnumProperty( attr='tl_type',
            name='Fill+Back Type',
            description='Choose the type off secondary Light you would like',
            items = Light_Type_List, default = 'POINT')


    def execute(self, context):
        scene = context.scene
        view = context.space_data
        if view.type == 'VIEW_3D' and not view.lock_camera_and_layers:
            camera = view.camera
        else:
            camera = scene.camera

        if (camera is None):

            cam_data= bpy.data.cameras.new(name='Camera')
            cam_obj = bpy.data.objects.new(name='Camera',object_data=cam_data)
            scene.objects.link(cam_obj)
            scene.camera=cam_obj
            bpy.ops.view3d.camera_to_view()
            camera=cam_obj
            bpy.ops.view3d.viewnumpad(type='TOP')

        obj = bpy.context.scene.objects.active

        #####Calculate Energy for each Lamp

        if(self.contrast>0):
            keyEnergy=self.energy
            backEnergy=(self.energy/100)*abs(self.contrast)
            fillEnergy=(self.energy/100)*abs(self.contrast)
        else:
            keyEnergy=(self.energy/100)*abs(self.contrast)
            backEnergy=self.energy
            fillEnergy=self.energy

        print(self.contrast)
        #####Calculate Direction for each Lamp

        #Calculate current Distance and get Delta
        obj_position=obj.location
        cam_position=camera.location

        delta_position=cam_position-obj_position
        vector_length=math.sqrt((pow(delta_position.x,2)+pow(delta_position.y,2)+pow(delta_position.z,2)))
        single_vector=(1/vector_length)*delta_position

        #Calc back position
        singleback_vector=single_vector.copy()
        singleback_vector.x=math.cos(math.radians(self.backangle))*single_vector.x+(-math.sin(math.radians(self.backangle))*single_vector.y)
        singleback_vector.y=math.sin(math.radians(self.backangle))*single_vector.x+(math.cos(math.radians(self.backangle))*single_vector.y)
        backx=obj_position.x+self.distance*singleback_vector.x
        backy=obj_position.y+self.distance*singleback_vector.y

        backData = bpy.data.lamps.new(name="TriLamp-Back", type=self.secondarytype)
        backData.energy=backEnergy

        backLamp = bpy.data.objects.new(name="TriLamp-Back", object_data=backData)
        scene.objects.link(backLamp)
        backLamp.location = (backx, backy, self.height)

        trackToBack=backLamp.constraints.new(type="TRACK_TO")
        trackToBack.target=obj
        trackToBack.track_axis="TRACK_NEGATIVE_Z"
        trackToBack.up_axis="UP_Y"

        #Calc right position
        singleright_vector=single_vector.copy()
        singleright_vector.x=math.cos(math.radians(self.rightangle))*single_vector.x+(-math.sin(math.radians(self.rightangle))*single_vector.y)
        singleright_vector.y=math.sin(math.radians(self.rightangle))*single_vector.x+(math.cos(math.radians(self.rightangle))*single_vector.y)
        rightx=obj_position.x+self.distance*singleright_vector.x
        righty=obj_position.y+self.distance*singleright_vector.y

        rightData = bpy.data.lamps.new(name="TriLamp-Fill", type=self.secondarytype)
        rightData.energy=fillEnergy
        rightLamp = bpy.data.objects.new(name="TriLamp-Fill", object_data=rightData)
        scene.objects.link(rightLamp)
        rightLamp.location = (rightx, righty, self.height)
        trackToRight=rightLamp.constraints.new(type="TRACK_TO")
        trackToRight.target=obj
        trackToRight.track_axis="TRACK_NEGATIVE_Z"
        trackToRight.up_axis="UP_Y"


        #Calc left position
        singleleft_vector=single_vector.copy()
        singleleft_vector.x=math.cos(math.radians(-self.leftangle))*single_vector.x+(-math.sin(math.radians(-self.leftangle))*single_vector.y)
        singleleft_vector.y=math.sin(math.radians(-self.leftangle))*single_vector.x+(math.cos(math.radians(-self.leftangle))*single_vector.y)
        leftx=obj_position.x+self.distance*singleleft_vector.x
        lefty=obj_position.y+self.distance*singleleft_vector.y

        leftData = bpy.data.lamps.new(name="TriLamp-Key", type=self.primarytype)
        leftData.energy=keyEnergy

        leftLamp = bpy.data.objects.new(name="TriLamp-Key", object_data=leftData)
        scene.objects.link(leftLamp)
        leftLamp.location = (leftx, lefty, self.height)
        trackToLeft=leftLamp.constraints.new(type="TRACK_TO")
        trackToLeft.target=obj
        trackToLeft.track_axis="TRACK_NEGATIVE_Z"
        trackToLeft.up_axis="UP_Y"


        return {'FINISHED'}


def panel_func(self, context):

    self.scn = context.scene
    self.layout.label(text="Tri-Lighting:")
    self.layout.operator("object.trilighting", text="Add Tri-Lighting")


def register():
    bpy.utils.register_class(TriLighting)

def unregister():
    bpy.utils.unregister_class(TriLighting)



#############################################################################################################################
#############################################################################################################################
#############  Topokit 2  ###################################################################################################
#############  Topokit 2  ###################################################################################################


#bl_info = {
#    "name": "Topokit 2",
#    "author": "dustractor",
#    "version": (2,0),
#    "blender": (2,6,0),
#    "api": 41935,
#    "location": "edit mesh vertices/edges/faces menus",
#    "description": "",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Mesh"}



# In between calls, this stores any data that is expensive or static,
# matched to the size of the mesh and the id of the operator that created it
cachedata = dict()
# and the object keeps the key to the cachedata
bpy.types.Object.tkkey = bpy.props.IntVectorProperty(size=4)

# just a mix-in for the operators...
class meshpoller:
    @classmethod
    def poll(self,context):
        try:
            assert context.active_object.type == "MESH"
        except:
            return False
        finally:
            return True

#BEGIN VERTICES SECTION

# This one works similarly to normal 'grow' (ctrl + NUMPAD_PLUS),
# except the original selection is not part of the result,
#
#   0--0--0         0--1--0
#   |  |  |         |  |  |
#   0--1--0  -->    1--0--1
#   |  |  |         |  |  |
#   0--0--0         0--1--0
#
class MESH_OT_vneighbors_edgewise(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.v2v_by_edge"
    bl_label = "Neighbors by Edge"
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        next_state = bytearray(meshkey[0])
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            vert_to_vert_map,prev_state = cachedata[meshkey]
        else:
            vert_to_vert_map = {i:{} for i in range(meshkey[0])}
            for a,b in mesh.edge_keys:
                vert_to_vert_map[a][b] = 1
                vert_to_vert_map[b][a] = 1
            obj.tkkey = meshkey
            prev_state = None
        if not prev_state:
            selected_vert_indices = filter(lambda _:mesh.vertices[_].select,range(len(mesh.vertices)))
        else:
            selected_vert_indices = filter(lambda _:mesh.vertices[_].select and not prev_state[_],range(len(mesh.vertices)))
        for v in selected_vert_indices:
            for neighbor_index in vert_to_vert_map[v]:
                next_state[neighbor_index] = True
        mesh.vertices.foreach_set("select",next_state)
        cachedata[meshkey] = (vert_to_vert_map,next_state)
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}

# This one is an alternate / counterpart to the previous.
# Think: diagonal opposite corners of a quad
# NOTE: does not apply to a triangle, since verts have no 'opposite'
#
#   0--0--0     1--0--1
#   |  |  |     |  |  |
#   0--1--0 --> 0--0--0
#   |  |  |     |  |  |
#   0--0--0     1--0--1
#
class MESH_OT_vneighbors_facewise(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.v2v_facewise"
    bl_label = "Neighbors by Face - Edge"
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        next_state = bytearray(meshkey[0])
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            vert_to_vert_map = cachedata[meshkey]
        else:
            vert_to_vert_map = {i:{} for i in range(meshkey[0])}
            for a,b in mesh.edge_keys:
                vert_to_vert_map[a][b] = 1
                vert_to_vert_map[b][a] = 1
            obj.tkkey = meshkey
        faces = filter(lambda face:(len(face.vertices)==4) and (face.select == False),mesh.polygons)
        for f in faces:
            has = False
            t = set()
            for v in f.vertices:
                if mesh.vertices[v].select:
                    has = True
                    t.update(vert_to_vert_map[v])
            if has:
                for v in f.vertices:
                    if not mesh.vertices[v].select:
                        if v not in t:
                            next_state[v]=1 
        mesh.vertices.foreach_set("select",next_state)
        cachedata[meshkey] = vert_to_vert_map
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}

def vvmenuitem(self,context):
    self.layout.operator(MESH_OT_vneighbors_edgewise.bl_idname)
    self.layout.operator(MESH_OT_vneighbors_facewise.bl_idname)
    #for the sake of completeness, yes there is one alg missing - one for both...

#END VERTICES SECTION
#BEGIN EDGES SECTION

#   +--0--+--0--+--0--+          +--0--+--0--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     1     1     0
#   |     |     |     |          |     |     |     |
#   +--0--+--1--+--0--+   --->   +--0--+--0--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     1     1     0
#   |     |     |     |          |     |     |     |
#   +--0--+--0--+--0--+          +--0--+--0--+--0--+
class MESH_OT_eneighbors_shared_v_f(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.e2e_evfe"
    bl_label = "Neighbors by Vert+Face"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        state_mask = bytearray(meshkey[1])
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_to_edges_dict = cachedata
        else:
            edge_key_to_index = {k:i for i,k in enumerate(mesh.edge_keys)}
            edge_to_edges_dict = {i:set() for i in range(len(mesh.edges))}
            for f in mesh.polygons:
                fed=[edge_key_to_index[k] for k in f.edge_keys]
                for k in f.edge_keys:
                    edge_to_edges_dict[edge_key_to_index[k]].update(fed)
            obj.tkkey = meshkey
        for e in filter(lambda _:mesh.edges[_].select,edge_to_edges_dict):
            k1 = set(mesh.edges[e].key)
            for n in edge_to_edges_dict[e]:
                k2 = set(mesh.edges[n].key)
                if not k1.isdisjoint(k2):
                    state_mask[n] = True
        for e in mesh.edges:
            e.select ^= state_mask[e.index]
        cachedata[meshkey] = edge_key_to_index
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


#   +--0--+--0--+--0--+          +--0--+--0--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     1     1     0
#   |     |     |     |          |     |     |     |
#   +--0--+--1--+--0--+   --->   +--1--+--0--+--1--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     1     1     0
#   |     |     |     |          |     |     |     |
#   +--0--+--0--+--0--+          +--0--+--0--+--0--+
class MESH_OT_eneighbors_shared_v(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.e2e_eve"
    bl_label = "Neighbors by Vert"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        bpy.ops.object.mode_set(mode="OBJECT")
        mesh = context.active_object.data
        state_mask = bytearray(len(mesh.edges))
        for e in mesh.edges:
            state_mask[e.index] = mesh.vertices[e.vertices[0]].select ^ mesh.vertices[e.vertices[1]].select
        mesh.edges.foreach_set('select',state_mask)
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


#   +--0--+--0--+--0--+          +--0--+--1--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     1     1     0
#   |     |     |     |          |     |     |     |
#   +--0--+--1--+--0--+   --->   +--0--+--0--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     1     1     0
#   |     |     |     |          |     |     |     |
#   +--0--+--0--+--0--+          +--0--+--1--+--0--+
class MESH_OT_eneighbors_shared_f(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.e2e_efe"
    bl_label = "Neighbors by Face"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_to_edges_dict = cachedata
        else:
            edge_key_to_index = {k:i for i,k in enumerate(mesh.edge_keys)}
            edge_to_edges_dict = {i:set() for i in range(len(mesh.edges))}
            for f in mesh.polygons:
                fed=[edge_key_to_index[k] for k in f.edge_keys]
                for k in f.edge_keys:
                    edge_to_edges_dict[edge_key_to_index[k]].update(fed)
            obj.tkkey = meshkey
        state_mask,esel = (bytearray(meshkey[1]),bytearray(meshkey[1]))
        mesh.edges.foreach_get('select',esel) 
        for e in filter(lambda _:mesh.edges[_].select,range(meshkey[1])):
            for n in edge_to_edges_dict[e]:
                state_mask[n] = 1
        for e in range(meshkey[1]):
            esel[e] ^= state_mask[e]
        mesh.edges.foreach_set('select',esel)
        cachedata[meshkey] = edge_to_edges_dict
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}

# notice that on these next two, the original selection stays
#   +--0--+--0--+--0--+          +--0--+--1--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     0     0     0
#   |     |     |     |          |     |     |     |
#   +--0--+--1--+--0--+   --->   +--0--+--1--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     0     0     0
#   |     |     |     |          |     |     |     |
#   +--0--+--0--+--0--+          +--0--+--1--+--0--+
class MESH_OT_eneighbors_shared_f_notv(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.e2e_efnve"
    bl_label = "Lateral Neighbors"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        state_mask = bytearray(meshkey[1])
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_to_face_map,edge_key_to_index = cachedata[meshkey]
        else:   
            edge_key_to_index = {}
            edge_to_face_map = {i:set() for i in range(meshkey[1])}
            for i,k in enumerate(mesh.edge_keys):
                edge_key_to_index[k] = i
            for f in mesh.polygons:
                for k in f.edge_keys:
                    edge_to_face_map[edge_key_to_index[k]].add(f.index)
            obj.tkkey = meshkey
        selected_edge_indices = filter(lambda _:mesh.edges[_].select,range(meshkey[1]))
        for e in selected_edge_indices:
            for f in edge_to_face_map[e]:
                for k in mesh.polygons[f].edge_keys:
                    hasv_in = False
                    for v in mesh.edges[e].key:
                        if v in k:
                            hasv_in = True
                    if hasv_in:
                        continue
                    else:
                        state_mask[edge_key_to_index[k]] = True
        for e in filter(lambda _:state_mask[_],range(meshkey[1])):
            mesh.edges[e].select |= state_mask[e]
        cachedata[meshkey] = (edge_to_face_map,edge_key_to_index)
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}



#   +--0--+--0--+--0--+          +--0--+--0--+--0--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     0     0     0
#   |     |     |     |          |     |     |     |
#   +--0--+--1--+--0--+   --->   +--1--+--1--+--1--+
#   |     |     |     |          |     |     |     |
#   0     0     0     0          0     0     0     0
#   |     |     |     |          |     |     |     |
#   +--0--+--0--+--0--+          +--0--+--0--+--0--+
class MESH_OT_eneighbors_shared_v_notf(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.e2e_evnfe"
    bl_label = "Longitudinal Edges"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        state_mask = bytearray(meshkey[1])
        vstate = bytearray(meshkey[0])
        mesh.vertices.foreach_get('select',vstate)
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_to_face_map,vert_to_vert_map,edge_key_to_index = cachedata[meshkey]
        else:
            edge_key_to_index = {}
            vert_to_vert_map = {i:set() for i in range(meshkey[0])}
            edge_to_face_map = {i:set() for i in range(meshkey[1])}
            for i,k in enumerate(mesh.edge_keys):
                edge_key_to_index[k] = i
                vert_to_vert_map[k[0]].add(k[1])
                vert_to_vert_map[k[1]].add(k[0])
            for f in mesh.polygons:
                for k in f.edge_keys:
                    edge_to_face_map[edge_key_to_index[k]].add(f.index)
            obj.tkkey = meshkey
        selected_edge_indices = filter(lambda _:mesh.edges[_].select,range(meshkey[1]))
        for e in selected_edge_indices:
            for v in mesh.edges[e].key:
                state_mask[v] ^=1
            for f in edge_to_face_map[e]:
                for v in mesh.polygons[f].vertices:
                    vstate[v] = 1
        for v in filter(lambda _:state_mask[_],range(meshkey[1])):
            for n in vert_to_vert_map[v]:
                if not vstate[n] and (n != v):
                    mesh.edges[edge_key_to_index[(min(v,n),max(v,n))]].select = True
        cachedata[meshkey] = (edge_to_face_map,vert_to_vert_map,edge_key_to_index)
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}
 
#deselects faces, leaving only edges selected
class MESH_OT_just_the_edges(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.je"
    bl_label = "Just the Edge Selection"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        state_mask = bytearray(meshkey[1])
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_key_to_index = cachedata[meshkey]
        else:
            edge_key_to_index = {k:i for i,k in enumerate(mesh.edge_keys)}
            obj.tkkey = meshkey
        for f in filter(lambda _:mesh.polygons[_].select,range(meshkey[2])):
            for k in mesh.polygons[f].edge_keys:
                state_mask[edge_key_to_index[k]] = 1
        for e in range(meshkey[1]):
            mesh.edges[e].select ^= state_mask[e]
        cachedata[meshkey] = edge_key_to_index
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}

# deselects edges which are at the edge of a face-selection,
# causing selection to 'shrink in'
class MESH_OT_inner_edges(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.ie"
    bl_label = "Inner Edge Selection"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        state_mask = bytearray(meshkey[1])
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_to_face_map = cachedata[meshkey]
        else:
            edge_key_to_index = {k:i for i,k in enumerate(mesh.edge_keys)}
            edge_to_face_map = {i:set() for i in range(meshkey[1])}
            for f in mesh.polygons:
                for k in f.edge_keys:
                    edge_to_face_map[edge_key_to_index[k]].add(f.index)
            obj.tkkey = meshkey
        for e in filter(lambda _:mesh.edges[_].select,range(meshkey[1])):
            for f in edge_to_face_map[e]:
                if mesh.polygons[f].select:
                    state_mask[e] ^=1
        for e in range(meshkey[1]):
            mesh.edges[e].select ^= state_mask[e]
        cachedata[meshkey] = edge_to_face_map
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


def eemenuitem(self,context):
    self.layout.operator(MESH_OT_eneighbors_shared_v_f.bl_idname)
    self.layout.operator(MESH_OT_eneighbors_shared_v.bl_idname)
    self.layout.operator(MESH_OT_eneighbors_shared_f.bl_idname)
    self.layout.operator(MESH_OT_eneighbors_shared_f_notv.bl_idname)
    self.layout.operator(MESH_OT_eneighbors_shared_v_notf.bl_idname)
    self.layout.operator(MESH_OT_just_the_edges.bl_idname)
    self.layout.operator(MESH_OT_inner_edges.bl_idname)

#END EDGES SECTION
#BEGIN FACES SECTION

# here is another one which functions very similarly to the ctrl+NUMPAD_PLUS 'growth'
# but it deselects the original selection, of course.
# This would be your checkerboard-type growth.
#   [0][0][0]          [0][1][0] 
#   [0][1][0]   --->   [1][0][1]
#   [0][0][0]          [0][1][0]
class MESH_OT_fneighbors_shared_e(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.f2f_fef"
    bl_label = "Neighbors by Edge"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            face_to_face_map = cachedata[meshkey]
        else:
            edge_key_to_index = {k:i for i,k in enumerate(mesh.edge_keys)}
            edge_to_face_map = {i:set() for i in range(meshkey[1])}
            for f in mesh.polygons:
                for k in f.edge_keys:
                    edge_to_face_map[edge_key_to_index[k]].add(f.index)
            face_to_face_map = {i:set() for i in range(meshkey[2])}
            for f in mesh.polygons:
                for k in f.edge_keys:
                    face_to_face_map[f.index].update(edge_to_face_map[edge_key_to_index[k]])
            obj.tkkey = meshkey
        mask_state = bytearray(meshkey[2])
        for f in filter(lambda _:mesh.polygons[_].select,range(meshkey[2])):
            for n in face_to_face_map[f]:
                mask_state[n] = True
        for f in range(meshkey[2]):
            mesh.polygons[f].select ^= mask_state[f]
        cachedata[meshkey] = face_to_face_map
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


#   [0][0][0]          [1][0][1] 
#   [0][1][0]   --->   [0][0][0]
#   [0][0][0]          [1][0][1]
class MESH_OT_fneighbors_shared_v_note(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.f2f_fvnef"
    bl_label = "Neighbors by Vert not Edge"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            edge_key_to_index = cachedata[meshkey]
        else:
            edge_key_to_index = {k:i for i,k in enumerate(mesh.edge_keys)}
            obj.tkkey = meshkey
        state_mask = bytearray(meshkey[2])
        face_verts = set()
        for f in filter(lambda _:mesh.polygons[_].select,range(meshkey[2])):
            face_verts.update(mesh.polygons[f].vertices)
        for f in filter(lambda _:not mesh.polygons[_].select,range(meshkey[2])):
            ct = 0
            for v in mesh.polygons[f].vertices:
                ct += (v in face_verts)
            if ct == 1:
                state_mask[f] = 1
        mesh.polygons.foreach_set('select',state_mask)
        cachedata[meshkey] = edge_key_to_index
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


# http://en.wikipedia.org/wiki/Conway's_Game_of_Life
class MESH_OT_conway(meshpoller,bpy.types.Operator):
    bl_idname = "mesh.conway"
    bl_label = "Conway"
    bl_options = {"REGISTER","UNDO"}
    def execute(self,context):
        global cachedata
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mesh = obj.data
        meshkey = (len(mesh.vertices),len(mesh.edges),len(mesh.polygons),id(self))
        if (meshkey == obj.tkkey) and (meshkey in cachedata):
            vert_to_face_map = cachedata[meshkey]
        else:
            vert_to_face_map = {i:set() for i in range(meshkey[0])}
            for f in mesh.polygons:
                for v in f.vertices:
                    vert_to_face_map[v].add(f.index)
            obj.tkkey = meshkey
        sel = set()
        uns = set()
        F = {i:set() for i in range(meshkey[2])}
        for f in range(meshkey[2]):
            for v in mesh.polygons[f].vertices:
                for n in filter(lambda _: mesh.polygons[_].select and (_ != f),vert_to_face_map[v]):
                    F[f].add(n)
        for f in F:
            if len(F[f]) == 3:
                sel.add(f)
            elif len(F[f]) != 2:
                uns.add(f)
        for f in range(meshkey[2]):
            if f in sel:
                mesh.polygons[f].select = True
            if f in uns:
                mesh.polygons[f].select = False
        cachedata[meshkey] = vert_to_face_map
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}

        

def ffmenuitem(self,context):
    self.layout.operator(MESH_OT_fneighbors_shared_e.bl_idname)
    self.layout.operator(MESH_OT_fneighbors_shared_v_note.bl_idname)
    self.layout.operator(MESH_OT_conway.bl_idname)

def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(vvmenuitem)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(eemenuitem)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(ffmenuitem)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(vvmenuitem)
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(eemenuitem)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(ffmenuitem)




##################################################################################################################################
##################################################################################################################################
#############  Snap to Center  ###################################################################################################
#############  Snap to Center  ###################################################################################################

#bl_info = {
#    "name": "Snap to Center (offset)",
#    "location": "Search tool",
#    "description": "Snap selected objects to center with offset.",
#    "author": "Spirou4D",
#    "version": (0,2),
#    "blender": (2, 6, 9),
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "3D View",
#    }


###------ Create Snapping Operators -------###
   
class snapcenteroffset(bpy.types.Operator):
    """Snap the currently selected objects to Center with offset"""
    bl_idname = "mesh.snapcenteroffset"
    bl_label = "Selection to center (offset)"
    bl_options = {'REGISTER', 'UNDO'}     
    
    
    @classmethod        
    def poll(cls, context):
        return len(context.selected_objects) > 0
    
    def execute(self, context):

        scene = bpy.context.scene
        #activeObj = context.active_object
        selected = context.selected_objects

        if selected:
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.ops.view3d.snap_selected_to_cursor()
        else:
            self.report({'INFO'}, "No objects selected") 

        return {"FINISHED"}     


###------  Functions Menu add -------###
def menu_display(self, context):
    self.layout.operator(snapcenteroffset.bl_idname, icon="PLUGIN")


################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


## -----------------------------------SELECT LEFT---------------------
def side (self, nombre, offset):

    bpy.ops.object.mode_set(mode="EDIT", toggle=0)
    OBJECT = bpy.context.active_object
    ODATA = bmesh.from_edit_mesh(OBJECT.data)
    MODE = bpy.context.mode
    bpy.context.tool_settings.mesh_select_mode = (True, False, False)
    for VERTICE in ODATA.verts[:]:
        VERTICE.select = False
    if nombre == False:
        for VERTICES in ODATA.verts[:]:
            if VERTICES.co[0] < (offset):
                VERTICES.select = 1
    else:
        for VERTICES in ODATA.verts[:]:
            if VERTICES.co[0] > (offset):
                VERTICES.select = 1
    ODATA.select_flush(False)
    bpy.ops.object.mode_set(mode="EDIT", toggle=0)

class SelectMenor (bpy.types.Operator):
    bl_idname = "mesh.select_side_osc"
    bl_label = "Select Side"
    bl_options = {"REGISTER", "UNDO"}

    side = bpy.props.BoolProperty(name="Greater than zero", default=False)
    offset = bpy.props.FloatProperty(name="Offset", default=0)
    def execute(self,context):

        side(self, self.side, self.offset)

        return {'FINISHED'}



#####################################################################################################################################
#####################################################################################################################################
########  MonogusaTools  ############################################################################################################
########  MonogusaTools  ############################################################################################################

#bl_info = {
#    "name": "Monogusa Tools",
#    "author": "isidourou",
#    "version": (1, 0),
#    "blender": (2, 65, 0),
#    "location": "View3D > Toolbar",
#    "description": "MonogusaTools",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": 'CTNAME'}
#  (c)isidourou 2013    
atobj = None

def mode_interpret(emode):
    if emode == 'PAINT_TEXTURE':
        return 'TEXTURE_PAINT'
    if emode == 'SCULPT':
        return 'SCULPT'
    if emode == 'PAINT_VERTEX':
        return 'VERTEX_PAINT'
    if emode == 'PAINT_WEIGHT':
        return 'WEIGHT_PAINT'
    if emode == 'OBJECT':
        return 'OBJECT'
    if emode == 'POSE':
        return 'POSE'
    if emode=='EDIT_MESH' or emode=='EDIT_ARMATURE' or emode=='EDIT_CURVE' or emode=='EDIT_TEXT' or emode=='EDIT_METABALL' or emode=='EDIT_SURFACE':
        return 'EDIT'
    
def check_active():
    count = 0
    slist = bpy.context.selected_objects
    for i in slist:
        count += 1
    return count

def check_mode():
    emode = bpy.context.mode
    if emode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    return emode
 
#    Menu in tools region
#class MonogusaToolsPanel(bpy.types.Panel):
 #   bl_category = "test"
  #  bl_label = "Monogusa Tools"
   # bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOLS"
 
 #   def draw(self, context):
  #      layout = self.layout

##
 #add mirror modifire
#        col = layout.column(align=True)
 #       col = layout.column(align=True)
  #      col.label(text="Add Mirror Modifier:")
   #     row = col.row(align=True)
    #    row.operator("add.mmx", text="X")
     #   row.operator("add.mmy", text="Y")     
      #  row.operator("add.mmz", text="Z")     
       # row = col.row(align=True)
        #row.operator("add.mmmx", text="-X")
        #row.operator("add.mmmy", text="-Y")     
        #row.operator("add.mmmz", text="-Z")     
   
#---- main ------

#add mirror modifier
def add_mm(direction):
    emode = bpy.context.mode
    emode = mode_interpret(emode)
    obj = bpy.ops.object
    cobj = bpy.context.object
    mesh = cobj.data
    obj.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    obj.mode_set(mode='OBJECT')
    ct = 0
    exist = False
    for i in cobj.modifiers:
        s = cobj.modifiers[ct].name
        if s.find('Mirror') != -1:
            exist = True
            break
    if exist == False:
        obj.modifier_add(type='MIRROR')

    if direction == 'X':
        for vertex in mesh.vertices:
            if (vertex.co.x < -0.000001):
                vertex.select = True
                cobj.modifiers["Mirror"].use_x = True
                if exist == False:
                    cobj.modifiers["Mirror"].use_y = False
                    cobj.modifiers["Mirror"].use_z = False
    if direction == '-X':
        for vertex in mesh.vertices:
            if (vertex.co.x > 0.000001):
                vertex.select = True
                cobj.modifiers["Mirror"].use_x = True
                if exist == False:
                    cobj.modifiers["Mirror"].use_y = False
                    cobj.modifiers["Mirror"].use_z = False
    if direction == 'Y':
        for vertex in mesh.vertices:
            if (vertex.co.y < -0.000001):
                vertex.select = True
                cobj.modifiers["Mirror"].use_y = True
                if exist == False:
                    cobj.modifiers["Mirror"].use_x = False
                    cobj.modifiers["Mirror"].use_z = False

    if direction == '-Y':
        for vertex in mesh.vertices:
            if (vertex.co.y > 0.000001):
                vertex.select = True
                cobj.modifiers["Mirror"].use_y = True
                if exist == False:
                    cobj.modifiers["Mirror"].use_x = False
                    cobj.modifiers["Mirror"].use_z = False
    if direction == 'Z':
        for vertex in mesh.vertices:
            if (vertex.co.z < -0.000001):
                vertex.select = True
                cobj.modifiers["Mirror"].use_z = True
                if exist == False:
                    cobj.modifiers["Mirror"].use_x = False
                    cobj.modifiers["Mirror"].use_y = False
    if direction == '-Z':
        for vertex in mesh.vertices:
            if (vertex.co.z > 0.000001):
                vertex.select = True
                cobj.modifiers["Mirror"].use_z = True
                if exist == False:
                    cobj.modifiers["Mirror"].use_x = False
                    cobj.modifiers["Mirror"].use_y = False
    cobj.modifiers["Mirror"].use_clip = True
    obj.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    
    bpy.ops.mesh.select_all(action='SELECT')
    obj.mode_set(mode='OBJECT')
    if emode != 'OBJECT':
        bpy.ops.object.mode_set(mode=emode)

class AddMmx(bpy.types.Operator):
    bl_idname = "add.mmx"
    bl_label = "AddMmx"
    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            add_mm('X')
        return{'FINISHED'}
class AddMm_x(bpy.types.Operator):
    bl_idname = "add.mmmx"
    bl_label = "AddMmx"
    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            add_mm('-X')
        return{'FINISHED'}
class AddMmy(bpy.types.Operator):
    bl_idname = "add.mmy"
    bl_label = "AddMmx"
    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            add_mm('Y')
        return{'FINISHED'}
class AddMm_y(bpy.types.Operator):
    bl_idname = "add.mmmy"
    bl_label = "AddMmx"
    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            add_mm('-Y')
        return{'FINISHED'}
class AddMmz(bpy.types.Operator):
    bl_idname = "add.mmz"
    bl_label = "AddMmx"
    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            add_mm('Z')
        return{'FINISHED'}
class AddMm_z(bpy.types.Operator):
    bl_idname = "add.mmmz"
    bl_label = "AddMmx"
    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            add_mm('-Z')
        return{'FINISHED'}

            
#	Registration

def register():
    #bpy.utils.register_class(MonogusaToolsPanel)
 

    bpy.utils.register_class(AddMmx)
    bpy.utils.register_class(AddMm_x)
    bpy.utils.register_class(AddMmy)
    bpy.utils.register_class(AddMm_y)
    bpy.utils.register_class(AddMmz)
    bpy.utils.register_class(AddMm_z)

    
def unregister():


    bpy.utils.unregister_class(AddMmx)
    bpy.utils.unregister_class(AddMm_x)
    bpy.utils.unregister_class(AddMmy)
    bpy.utils.unregister_class(AddMm_y)
    bpy.utils.unregister_class(AddMmz)
    bpy.utils.unregister_class(AddMm_z)



#####################################################################################################################################
#####################################################################################################################################
#############  MEXTRUDE  ############################################################################################################
#############  MEXTRUDE  ############################################################################################################

################################################################################
# Repeats extrusion + rotation + scale for one or more faces                   #
################################################################################

#bl_info = {
#    "name": "MExtrude",
#    "version": (1, 3, 0),
#    "blender": (2, 6, 8),
#    "location": "View3D > Tool Shelf",
#    "description": "Repeat extrusions from faces to create organic shapes",
#    'warning': '',
#    "category": "Mesh"}



def vloc(self, r):
    random.seed(self.ran + r)
    return self.off * (1 + random.gauss(0, self.var1 / 3))

def vrot(self,r):
    random.seed(self.ran + r)
    return Euler((radians(self.rotx) + random.gauss(0, self.var2 / 3), \
        radians(self.roty) + random.gauss(0, self.var2 / 3), \
        radians(self.rotz) + random.gauss(0,self.var2 / 3)), 'XYZ')

def vsca(self, r):
    random.seed(self.ran + r)
    return self.sca * (1 + random.gauss(0, self.var3 / 3))

class MExtrude(bpy.types.Operator):
    bl_idname = 'object.mextrude'
    bl_label = 'MExtrude'
    bl_description = 'Multi Extrude'
    bl_options = {'REGISTER', 'UNDO'}

    off = FloatProperty(name='Offset', min=-2, soft_min=0.001, \
        soft_max=2, max=5, default=.5, description='Translation')
    rotx = FloatProperty(name='Rot X', min=-85, soft_min=-30, \
        soft_max=30, max=85, default=0, description='X rotation')
    roty = FloatProperty(name='Rot Y', min=-85, soft_min=-30, \
        soft_max=30, max=85, default=0, description='Y rotation')
    rotz = FloatProperty(name='Rot Z', min=-85, soft_min=-30, \
        soft_max=30, max=85, default=-0, description='Z rotation')
    sca = FloatProperty(name='Scale', min=0.1, soft_min=0.5, \
        soft_max=1.2, max =2, default=.9, description='Scaling')
    var1 = FloatProperty(name='Offset Var', min=-5, soft_min=-1, \
        soft_max=1, max=5, default=0, description='Offset variation')
    var2 = FloatProperty(name='Rotation Var', min=-5, soft_min=-1, \
        soft_max=1, max=5, default=0, description='Rotation variation')
    var3 = FloatProperty(name='Scale Noise', min=-5, soft_min=-1, \
        soft_max=1, max=5, default=0, description='Scaling noise')
    num = IntProperty(name='Repeat', min=1, max=50, soft_max=100, \
        default=5, description='Repetitions')
    ran = IntProperty(name='Seed', min=-9999, max=9999, default=0, \
        description='Seed to feed random values')

    @classmethod
    def poll(cls, context):
        obj = context.object
        return (obj and obj.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        column.label(text='Transformations:')
        column.prop(self, 'off', slider=True)
        column.prop(self, 'rotx', slider=True)
        column.prop(self, 'roty', slider=True)
        column.prop(self, 'rotz', slider=True)
        column.prop(self, 'sca', slider=True)
        column = layout.column(align=True)
        column.label(text='Variation settings:')
        column.prop(self, 'var1', slider=True)
        column.prop(self, 'var2', slider=True)
        column.prop(self, 'var3', slider=True)
        column.prop(self, 'ran')
        column = layout.column(align=False)
        column.prop(self, 'num')

    def execute(self, context):
        obj = bpy.context.object
        data, om =  obj.data, obj.mode
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]

        # bmesh operations
        bpy.ops.object.mode_set()
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        sel = [f for f in bm.faces if f.select]

        # faces loop
        for i, of in enumerate(sel):
            rot = vrot(self, i)
            off = vloc(self, i)
            of.normal_update()

            # extrusion loop
            for r in range(self.num):
                nf = of.copy()
                nf.normal_update()
                no = nf.normal.copy()
                ce = nf.calc_center_bounds()
                s = vsca(self, i + r)

                for v in nf.verts:
                    v.co -= ce
                    v.co.rotate(rot)
                    v.co += ce + no * off
                    v.co = v.co.lerp(ce, 1 - s)

                # extrude code from TrumanBlending
                for a, b in zip(of.loops, nf.loops):
                    sf = bm.faces.new((a.vert, a.link_loop_next.vert, \
                        b.link_loop_next.vert, b.vert))
                    sf.normal_update()

                bm.faces.remove(of)
                nf.select_set(True)
                of = nf

        for v in bm.verts: v.select = False
        for e in bm.edges: e.select = False
        bm.to_mesh(obj.data)
        obj.data.update()

        # restore user settings
        bpy.ops.object.mode_set(mode=om)

        if not len(sel):
            self.report({'INFO'}, 'Select one or more faces...')
        return{'FINISHED'}


def register():
    bpy.utils.register_class(MExtrude)

def unregister():
    bpy.utils.unregister_class(MExtrude)


#########################################################################################################################################
#########################################################################################################################################
#########  Nikitron tools  ##############################################################################################################
#########  Nikitron tools  ##############################################################################################################



#bl_info = {
#    "name": "Nikitron tools",
#    "version": (0, 1, 3),
#    "blender": (2, 6, 9), 
#    "category": "Object",
#    "author": "Nikita Gorodetskiy",
#    "location": "object",
#    "description": "Nikitron tools - vertices and object names, curves to 3d, material to object mode, spread objects, bounding boxes",
#    "warning": "",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/Nikitron_tools",          
#    "tracker_url": "http://www.blenderartists.org/forum/showthread.php?272679-Addon-WIP-Sverchok-parametric-tool-for-architects",  
#}

# 2013-09-03 shift
# 2013-09-04 hooks



class CurvesTo3D (bpy.types.Operator):
    """Put curves to ground and turn to 3d mode (wiring them) for farthere spread to layout sheet"""
    bl_idname = "object.curv_to_3d"
    bl_label = "Curves to 3d"
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        if obj[0].type == 'CURVE':
            for o in obj:
                o.data.extrude = 0.0
                o.data.dimensions = '3D'
                #o.matrix_world.translation[2] = 0
        return {'FINISHED'}

class CurvesTo2D (bpy.types.Operator):
    """Curves turn to 2d mode (and thicken 0.03 mm)"""
    bl_idname = "object.curv_to_2d"
    bl_label = "Curves to 2d"
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        if obj[0].type == 'CURVE':
            for o in obj:
                o.data.extrude = 0.0016
                o.data.dimensions = '2D'
                nam = o.data.name
                # Я фанат группы "Сплин", ребята.
                for splin in bpy.data.curves[nam].splines:
                    splin.use_smooth = False
                    for point in splin.bezier_points:
                        point.radius = 1.0
        return {'FINISHED'}

class ObjectNames (bpy.types.Operator):
    """Make all objects show names in 3d"""      
    bl_idname = "object.name_objects" 
    bl_label = "Name objects"        
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        for ob in obj:
            mw = ob.matrix_world.translation
            name_all = re.match(r'(\w+)', ob.name)
            name = name_all.group(1)
            box = ob.bound_box
            v1 = Vector((box[0][0:]))
            v2 = Vector((box[6][0:]))
            len = Vector((v2-v1)).length
            self.run(mw,name,len)
        return {'FINISHED'}

    def run(self, origin,text,length):
       # Create and name TextCurve object
        bpy.ops.object.text_add(
        location=origin,
        rotation=(radians(0),radians(0),radians(0)))
        ob = bpy.context.object
        ob.name = 'lable_'+str(text)
        tcu = ob.data
        tcu.name = 'lable_'+str(text)
        # TextCurve attributes
        tcu.body = str(text)
        tcu.font = bpy.data.fonts[0]
        tcu.offset_x = 0
        tcu.offset_y = -0.25
        tcu.resolution_u = 2
        tcu.shear = 0
        if length < 0.0625:
            Tsize = 0.01*(5*length)
        else:
            Tsize = 0.0625
        tcu.size = Tsize
        tcu.space_character = 1
        tcu.space_word = 1
        tcu.align = 'CENTER'
        # Inherited Curve attributes
        tcu.extrude = 0.0
        tcu.fill_mode = 'NONE'
        
        
class VerticesNumbers3D (bpy.types.Operator):
    """make all vertices show numbers in 3D"""      
    bl_idname = "object.vertices_numbers3d"
    bl_label = "Vertices num."
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        obj1 = bpy.context.selected_objects[0]
        if obj1.type != 'MESH':
            print ("Select meshes, plase")
            return {'CANCELLED'}
        mw1 = obj1.matrix_world
        mesh1 = obj1.data
        mesh1.update()
        ver1 = mesh1.vertices
        for id in ver1:
            i = id.index
            coor = mw1 * ver1[i].co
            self.run(coor,i)
        return {'FINISHED'}
    
    def run(self, origin,text):
        # Create and name TextCurve object
        bpy.ops.object.text_add(
        location=origin,
        rotation=(radians(90),radians(0),radians(0)))
        ob = bpy.context.object
        ob.name = 'vert '+str(text)
        tcu = ob.data
        tcu.name = 'vert '+str(text)
        # TextCurve attributes
        tcu.body = str(text)
        tcu.font = bpy.data.fonts[0]
        tcu.offset_x = 0
        tcu.offset_y = 0
        tcu.shear = 0
        tcu.size = 0.3
        tcu.space_character = 1
        tcu.space_word = 1
        # Inherited Curve attributes
        tcu.extrude = 0
        tcu.fill_mode = 'BOTH'

vert_max = 0

class Connect2Meshes (bpy.types.Operator):
    """connect two objects by mesh edges with vertices shift and hooks to initial objects"""      
    bl_idname = "object.connect2objects"
    bl_label = "connect2objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def dis(self, x,y):
        vec = mathutils.Vector((x[0]-y[0], x[1]-y[1], x[2]-y[2]))
        return vec.length
    
    def maxObj(self, ver1, ver2, mw1, mw2):
        if len(ver1) > len(ver2):
            inverc = 0
            vert1 = ver1
            mworld1 = mw1
            vert2 = ver2
            mworld2 = mw2
        else:
            inverc = 1
            vert1 = ver2
            mworld1 = mw2
            vert2 = ver1
            mworld2 = mw1
        cache_max = [vert1, mworld1]
        cache_min = [vert2, mworld2]
        return cache_max, cache_min, inverc
    
    def points(self, ver1, ver2, mw1, mw2, shift):
        vert_new = []
        # choosing maximum vertex count in ver1/2, esteblish vert2 - mincount of vertex
        cache = self.maxObj(ver1, ver2, mw1, mw2)
        vert1 = cache[0][0]
        vert2 = cache[1][0]
        mworld1 = cache[0][1]
        mworld2 = cache[1][1]
        inverc = cache[2]
        # append new verts in new obj
        for v in vert2:
            v2 = mworld2 * v.co
            if len(vert2) > v.index + shift:
                v1 = mworld1 * vert1[v.index + shift].co
            else:
                v1 = mworld1 * vert1[v.index + shift - len(vert2)].co
            if inverc == True:
                m1 = mworld2.translation
                m2 = mworld2.translation
            else:
                m1 = mworld1.translation
                m2 = mworld1.translation
            vert_new.append(v2 - m2)
            vert_new.append(v1 - m1)
        return vert_new
    
    def edges(self, vert_new):
        edges_new = []
        i = -2
        for v in vert_new:
            # dis(vert_new[i],vert_new[i+1]) < 10 and 
            if i > -1 and i < (len(vert_new)):
                edges_new.append((i,i + 1))
            i += 2
        return edges_new
    
    def mk_me(self, name):
        me = bpy.data.meshes.new(name+'Mesh')
        return me
    
    def mk_ob(self, mesh, name, mw):
        loc = mw.translation.to_tuple()
        ob = bpy.data.objects.new(name, mesh)
        ob.location = loc
        ob.show_name = True
        bpy.context.scene.objects.link(ob)
        return ob
    
    def def_me(self, mesh, ver1, ver2, mw1, mw2, obj1, obj2, nam):
        ver = self.points(ver1, ver2, mw1, mw2, bpy.context.scene.shift_verts)
        edg = self.edges(ver)
        mesh.from_pydata(ver, edg, [])
        mesh.update(calc_edges=True)
        if bpy.context.scene.hook_or_not:
            self.hook_verts(ver, obj1, obj2, nam, ver1, ver2, mw1, mw2)
        return
    
    # preparations for hooking
    def hook_verts(self, ver, obj1, obj2, nam, ver1, ver2, mw1, mw2):
        # pull cache from maxObj
        cache = self.maxObj(ver1, ver2, mw1, mw2)
        vert1 = cache[0][0]
        vert2 = cache[1][0]
        mworld1 = cache[0][1]
        mworld2 = cache[1][1]
        inverc = cache[2]
        points_ev = []
        points_od = []
        # devide even/odd verts
        for v in ver:
            if (ver.index(v) % 2) == 0:
                points_ev.append(ver.index(v))
                # print ('чёт ' + str(ver.index(v)))
            else:
                points_od.append(ver.index(v))
                # print ('нечет ' + str(ver.index(v)))
        if bpy.context.selected_objects:
            bpy.ops.object.select_all(action='TOGGLE')
        # depend on bigger (more verts) object it hooks even or odd verts
        if inverc == False:
            # ob1 = obj1 ob2 = obj2, 1 - bigger
            self.hooking_action(obj2, nam, points_ev, ver)
            self.hooking_action(obj1, nam, points_od, ver)
        else:
            # ob1 = obj2 ob2 = obj1, 2 - bigger
            self.hooking_action(obj2, nam, points_od, ver)
            self.hooking_action(obj1, nam, points_ev, ver)
        
    # free hooks :-)
    def hooking_action(self, ob, nam, points, verts_of_object):
        # select 1st obj, second connection
        bpy.data.scenes[bpy.context.scene.name].objects[ob.name].select = True
        bpy.data.scenes[bpy.context.scene.name].objects[nam].select = True
        bpy.data.scenes[bpy.context.scene.name].objects.active = bpy.data.objects[nam]
        # deselect vertices
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.editmode_toggle()
        # select nearby vertices
        for vert in points:
            bpy.context.object.data.vertices[vert].select = True
        # hook itself
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.hook_add_selob(use_bone=False)
        #bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.editmode_toggle()
        # deselect all
        bpy.ops.object.select_all(action='TOGGLE')

    
    def execute(self, context):
        context.scene.update()
        obj1 = context.selected_objects[0]
        obj2 = context.selected_objects[1]
        mw1 = obj1.matrix_world
        mw2 = obj2.matrix_world
        mesh1 = obj1.data
        mesh1.update()
        mesh2 = obj2.data
        mesh2.update()
        ver1 = mesh1.vertices
        ver2 = mesh2.vertices
        nam = 'linked_' + str(obj1.name) + str(obj2.name)
        me = self.mk_me(nam)
        ob = self.mk_ob(me, nam, mw1)
        self.def_me(me, ver1, ver2, mw1, mw2, obj1, obj2, nam)
        print ('---- NIKITRON_connect2objects MADE CONNECTION BETWEEN: ' + str(obj1.name) + ' AND ' + str(obj2.name) + ' AND GOT ' + str(ob.name) + ' ----')
        return {'FINISHED'}


class MaterialToObjectAll (bpy.types.Operator):
    """all materials turned to object mode"""      
    bl_idname = "object.materials_to_object"
    bl_label = "Materials to object"
    bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):
        obj = bpy.context.selected_objects
        mode = 'OBJECT'
        for o in obj:
            materials = bpy.data.objects[o.name].material_slots
            for m in materials:
                m.link = mode
        return {'FINISHED'}
    
class MaterialToDataAll (bpy.types.Operator):
    """all materials turned to data mode"""      
    bl_idname = "object.materials_to_data"
    bl_label = "Materials to data"
    bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):
        obj = bpy.context.selected_objects
        mode = 'DATA'
        for o in obj:
            materials = bpy.data.objects[o.name].material_slots
            for m in materials:
                m.link = mode
        return {'FINISHED'}


class BoundingBox (bpy.types.Operator):
    """Make bound boxes for selected objects in mesh"""      
    bl_idname = "object.bounding_boxers"
    bl_label = "Bounding boxes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        i = 0
        for a in objects:
            self.make_it(i, a)
            i += 1
        return {'FINISHED'}
    
    def make_it(self, i, obj):
        box = bpy.context.selected_objects[i].bound_box
        mw = bpy.context.selected_objects[i].matrix_world
        name = (bpy.context.selected_objects[i].name + '_bounding_box')
        me = bpy.data.meshes.new(name+'Mesh')
        ob = bpy.data.objects.new(name, me)
        ob.location = mw.translation
        ob.scale = mw.to_scale()
        ob.rotation_euler = mw.to_euler()
        ob.show_name = True
        bpy.context.scene.objects.link(ob)
        loc = []
        for ver in box:
            loc.append(mathutils.Vector((ver[0],ver[1],ver[2])))
        me.from_pydata((loc), [], ((0,1,2,3),(0,1,5,4),(4,5,6,7), (6,7,3,2),(0,3,7,4),(1,2,6,5)))
        me.update(calc_edges=True)
        return

class SpreadObjects (bpy.types.Operator):
    """spread all objects on sheet for farthere use in dxf layout export"""
    bl_idname = "object.spread_objects"
    bl_label = "Spread objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        count = len(obj) - 1                # items number
        row = math.modf(math.sqrt(count))[1] or 1 #optimal number of rows and columns !!! temporery solution
        locata = mathutils.Vector()    # while veriable 
        dx, dy, ddy = 0, 0, 0                       # distance
        while count > -1:   # iterations X
            locata[2] = 0               # Z = 0
            row1 = row
            x_curr = []                     # X bounds collection
            locata[1] = 0              # Y = 0
            while row1:         # iteratiorns Y
                # counting bounds
                bb = obj[count].bound_box
                mwscale = obj[count].matrix_world.to_scale()
                mwscalex = mwscale[0]
                mwscaley = mwscale[1]
                x0 = bb[0][0]
                x1 = bb[4][0]
                y0 = bb[0][1]
                y1 = bb[2][1]
                ddy = dy            # secondary distance to calculate avverage
                dx = mwscalex*(max(x0,x1)-min(x0,x1)) + 0.03        # seek for distance !!! temporery solution
                dy = mwscaley*(max(y0,y1)-min(y0,y1)) + 0.03        # seek for distance !!! temporery solution
                # shift y
                locata[1] += ((dy + ddy) / 2)
                # append x bounds
                x_curr.append(dx)
                bpy.ops.object.rotation_clear()
                bpy.context.selected_objects[count].location = locata
                row1 -= 1
                count -= 1
            locata[0] += max(x_curr)        # X += 1
            dx, dy, ddy = 0, 0, 0
            del(x_curr)
        return {'FINISHED'}
    
from bpy.props import IntProperty, BoolProperty

# this def for connect2objects maximum shift (it cannot update scene's veriable somehow)
def maxim():
    if bpy.context.selected_objects[0].type == 'MESH':
        if len(bpy.context.selected_objects) >= 2:     
            len1 = len(bpy.context.selected_objects[0].data.vertices)
            len2 = len(bpy.context.selected_objects[1].data.vertices)
            maxim = min(len1, len2)
            #print (maxim)
    return maxim

def shift():
    bpy.types.Scene.shift_verts = IntProperty(
        name="shift_verts",
        description="shift vertices of smaller object, it can reach maximum (look right), to make patterns",
        min=0, max=1000,  #maxim(), - this cannot be updated
        default = 0, options={'ANIMATABLE', 'LIBRARY_EDITABLE'})
    return
shift()

# this flag for connetc2objects, hook or not?
def hook_or_not():
    bpy.types.Scene.hook_or_not = BoolProperty(
        name="hook_or_not",
        description="hook or not new connected vertices to parents objects? it will get spider's web's linkage effect",
        default = True)
    return
hook_or_not()

       
my_classes = [CurvesTo3D, CurvesTo2D, ObjectNames, VerticesNumbers3D, Connect2Meshes, MaterialToObjectAll, MaterialToDataAll, BoundingBox, SpreadObjects]
    
def register():
    for clas in my_classes:
        bpy.utils.register_class(clas)

def unregister():
    for clas in my_classes:
        bpy.utils.unregister_class(clas)
    


######################################################################################################################################
######################################################################################################################################
###########  Bevel/Taper Curve  ######################################################################################################
###########  Bevel/Taper Curve  ######################################################################################################

#bl_info = {
#    "name": "Bevel/Taper Curve",
#    "author": "Cmomoney",
#    "version": (1, 0),
#    "blender": (2, 69, 0),
#    "location": "View3D > Object > Bevel/Taper",
#    "description": "Adds bevel and/or taper curve to active curve",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Curve"}
 

def add_taper(self, context):

    scale_ends1 = self.scale_ends1
    scale_ends2 = self.scale_ends2
    scale_mid = self.scale_mid
    verts = [(-2.0, 1.0 * scale_ends1, 0.0, 1.0), (-1.0, 0.75 * scale_mid, 0.0, 1.0), (0.0, 1.5 * scale_mid, 0.0, 1.0), (1.0, 0.75 * scale_mid, 0.0, 1.0), (2.0, 1.0 * scale_ends2, 0.0, 1.0)]
    make_path(self, context, verts)

def add_type5(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[0.0 * scale_x, 0.049549 * scale_y, 0.0, 0.031603 * scale_x, 0.047013 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.031603 * scale_x, -0.047013 * scale_y, 0.0, 0.0 * scale_x, -0.049549 * scale_y, 0.0, -0.031603 * scale_x, -0.047013 * scale_y, 0.0, -0.05 * scale_x, -0.0 * scale_y, 0.0, -0.031603 * scale_x, 0.047013 * scale_y, 0.0]]
    lhandles = [[(-0.008804 * scale_x, 0.049549 * scale_y, 0.0), (0.021304 * scale_x, 0.02119 * scale_y, 0.0), (0.05 * scale_x, 0.051228 * scale_y, 0.0), (0.036552 * scale_x, -0.059423 * scale_y, 0.0), (0.008804 * scale_x, -0.049549 * scale_y, 0.0), (-0.021304 * scale_x, -0.02119 * scale_y, 0.0), (-0.05 * scale_x, -0.051228 * scale_y, 0.0), (-0.036552 * scale_x, 0.059423 * scale_y, 0.0)]]
    rhandles = [[(0.008803 * scale_x, 0.049549 * scale_y, 0.0), (0.036552 * scale_x, 0.059423 * scale_y, 0.0), (0.05 * scale_x, -0.051228 * scale_y, 0.0), (0.021304 * scale_x, -0.02119 * scale_y, 0.0), (-0.008803 * scale_x, -0.049549 * scale_y, 0.0), (-0.036552 * scale_x, -0.059423 * scale_y, 0.0), (-0.05 * scale_x, 0.051228 * scale_y, 0.0), (-0.021304 * scale_x, 0.02119 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type4(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.0 * scale_x, 0.017183 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.017183 * scale_y, 0.0, -0.05 * scale_x, -0.0 * scale_y, 0.0]]
    lhandles = [[(-0.017607 * scale_x, 0.017183 * scale_y, 0.0), (0.05 * scale_x, 0.102456 * scale_y, 0.0), (0.017607 * scale_x, -0.017183 * scale_y, 0.0), (-0.05 * scale_x, -0.102456 * scale_y, 0.0)]]
    rhandles = [[(0.017607 * scale_x, 0.017183 * scale_y, 0.0), (0.05 * scale_x, -0.102456 * scale_y, 0.0), (-0.017607 * scale_x, -0.017183 * scale_y, 0.0), (-0.05 * scale_x, 0.102456 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type3(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.017183 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, 0.05 * scale_y, 0.0, 0.017183 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.05 * scale_y, 0.0]]
    lhandles = [[(-0.017183 * scale_x, -0.017607 * scale_y, 0.0), (-0.102456 * scale_x, 0.05 * scale_y, 0.0), (0.017183 * scale_x, 0.017607 * scale_y, 0.0), (0.102456 * scale_x, -0.05 * scale_y, 0.0)]]
    rhandles = [[(-0.017183 * scale_x, 0.017607 * scale_y, 0.0), (0.102456 * scale_x, 0.05 * scale_y, 0.0), (0.017183 * scale_x, -0.017607 * scale_y, 0.0), (-0.102456 * scale_x, -0.05 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type2(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, 0.05 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.05 * scale_y, 0.0]]
    lhandles = [[(-0.05 * scale_x, -0.047606 * scale_y, 0.0), (-0.047606 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, 0.047607 * scale_y, 0.0), (0.047606 * scale_x, -0.05 * scale_y, 0.0)]]
    rhandles = [[(-0.05 * scale_x, 0.047607 * scale_y, 0.0), (0.047607 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, -0.047607 * scale_y, 0.0), (-0.047607 * scale_x, -0.05 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type1(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, 0.05 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.05 * scale_y, 0.0]]
    lhandles = [[(-0.05 * scale_x, -0.027606 * scale_y, 0.0), (-0.027606 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, 0.027606 * scale_y, 0.0), (0.027606 * scale_x, -0.05 * scale_y, 0.0)]]
    rhandles = [[(-0.05 * scale_x, 0.027607 * scale_y, 0.0), (0.027607 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, -0.027607 * scale_y, 0.0), (-0.027607 * scale_x, -0.05 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)

def make_path(self, context, verts):
    
    target = bpy.context.scene.objects.active
    bpy.ops.curve.primitive_nurbs_path_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
    target.data.taper_object = bpy.context.scene.objects.active
    taper = bpy.context.scene.objects.active
    taper.name = 'Taper_Curve'
    bpy.context.scene.objects.active = target
    points = taper.data.splines[0].points
    for i in range(len(verts)):
        points[i].co = verts[i]

def make_curve(self, context, verts, lh, rh):

    scale_x = self.scale_x
    scale_y = self.scale_y
    type = self.type
    target = bpy.context.scene.objects.active
    curve_data = bpy.data.curves.new(name='Bevel_Curve', type='CURVE')
    curve_data.dimensions = '3D'
    for p in range(len(verts)):
        c = 0
        spline = curve_data.splines.new(type='BEZIER')
        spline.use_cyclic_u = True
        spline.bezier_points.add( len(verts[p])/3-1 )
        spline.bezier_points.foreach_set('co', verts[p])
        for bp in spline.bezier_points:
            bp.handle_left_type = 'ALIGNED'
            bp.handle_right_type = 'ALIGNED'
            bp.handle_left.xyz = lh[p][c]
            bp.handle_right.xyz = rh[p][c]
            c += 1
    object_data_add(context, curve_data, operator=self)
    target.data.bevel_object = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = target

class add_tapercurve(Operator, AddObjectHelper):
    """Add taper curve to active curve"""
    bl_idname = "curve.tapercurve"
    bl_label = "Add Curve as Taper"
    bl_options = {'REGISTER', 'UNDO'}


    scale_ends1 = FloatProperty(name="End Width Left", description="Adjust left end taper", default=0.0, min=0.0)
    scale_ends2 = FloatProperty(name="End Width Right", description="Adjust right end taper", default=0.0, min=0.0)
    scale_mid = FloatProperty(name="Center Width", description="Adjust taper at center", default=1.0, min=0.0)
    link1 = BoolProperty(name='link ends', default=True)
    link2 = BoolProperty(name='link ends/center', default=False)
    if link2:
        diff = FloatProperty(name='Difference', default=1, description='Difference between ends and center while linked')

    def execute(self, context):
        if self.link1:
            self.scale_ends2 = self.scale_ends1
        if self.link2:
            self.scale_ends2 = self.scale_ends1 = self.scale_mid-self.diff
        add_taper(self, context)
        return {'FINISHED'}
    
class add_bevelcurve(Operator, AddObjectHelper):
    """Add bevel curve to active curve"""
    bl_idname = "curve.bevelcurve"
    bl_label = "Add Curve as Bevel"
    bl_options = {'REGISTER', 'UNDO'}

    type = IntProperty(name='Type', description='Type of bevel curve', default=1, min=1, max=5)
    scale_x = FloatProperty(name="scale x", description="scale on x axis", default=1.0)
    scale_y = FloatProperty(name="scale y", description="scale on y axis", default=1.0)
    link = BoolProperty(name='link xy', default=True)

    def execute(self, context):
        if self.link:
            self.scale_y = self.scale_x
        if self.type == 1:
            add_type1(self, context)
        if self.type == 2:
            add_type2(self, context)
        if self.type == 3:
            add_type3(self, context)
        if self.type == 4:
            add_type4(self, context)
        if self.type == 5:
            add_type5(self, context)
            
        return {'FINISHED'}


def menu_funcs(self, context):
    if bpy.context.scene.objects.active.type == "CURVE":
        self.layout.menu("OBJECT_MT_bevel_taper_curve_menu")




#####################################################################################################################################
#####################################################################################################################################
#############  Export Selected  #####################################################################################################
#############  Export Selected  #####################################################################################################

#bl_info = {
#    "name": "Export Selected",
#    "author": "dairin0d, rking",
#    "version": (1, 4),
#    "blender": (2, 6, 9),
#    "location": "File > Export > Selected",
#    "description": "Export selected objects to a chosen format",
#    "warning": "",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"\
#                "Scripts/Import-Export/Export_Selected",
#    "tracker_url": "http://projects.blender.org/tracker/"\
#                   "?func=detail&aid=30942",
#    "category": "Import-Export"}
#============================================================================#



join_before_export = {
    "export_mesh.ply",
}

bpy_props = {
    bpy.props.BoolProperty,
    bpy.props.BoolVectorProperty,
    bpy.props.IntProperty,
    bpy.props.IntVectorProperty,
    bpy.props.FloatProperty,
    bpy.props.FloatVectorProperty,
    bpy.props.StringProperty,
    bpy.props.EnumProperty,
    bpy.props.PointerProperty,
    bpy.props.CollectionProperty,
}

def is_bpy_prop(value):
    if isinstance(value, tuple) and (len(value) == 2):
        if (value[0] in bpy_props) and isinstance(value[1], dict):
            return True
    return False

def iter_public_bpy_props(cls, exclude_hidden=False):
    for key in dir(cls):
        if key.startswith("_"):
            continue
        value = getattr(cls, key)
        if is_bpy_prop(value):
            if exclude_hidden:
                options = value[1].get("options", "")
                if 'HIDDEN' in options:
                    continue
            yield (key, value)

def get_op(idname):
    category_name, op_name = idname.split(".")
    category = getattr(bpy.ops, category_name)
    return getattr(category, op_name)

class ToggleObjectMode:
    def __init__(self, mode='OBJECT', undo=False):
        if not isinstance(mode, str):
            mode = ('OBJECT' if mode else None)
        
        obj = bpy.context.object
        if obj and (obj.mode != mode):
            self.mode = mode
        else:
            self.mode = None
        self.undo = undo
    
    def __enter__(self):
        if self.mode:
            edit_preferences = bpy.context.user_preferences.edit
            
            self.global_undo = edit_preferences.use_global_undo
            self.prev_mode = bpy.context.object.mode
            
            if self.prev_mode != self.mode:
                if self.undo is not None:
                    edit_preferences.use_global_undo = self.undo
                bpy.ops.object.mode_set(mode=self.mode)
        
        return self
    
    def __exit__(self, type, value, traceback):
        if self.mode:
            edit_preferences = bpy.context.user_preferences.edit
            
            if self.prev_mode != self.mode:
                bpy.ops.object.mode_set(mode=self.prev_mode)
                edit_preferences.use_global_undo = self.global_undo

def iter_exporters():
    #categories = dir(bpy.ops)
    categories = ["export_anim", "export_mesh", "export_scene"]
    for category_name in categories:
        op_category = getattr(bpy.ops, category_name)
        
        for name in dir(op_category):
            total_name = category_name + "." + name
            
            if total_name == ExportSelected.bl_idname:
                continue
            
            if "export" in total_name:
                op = getattr(op_category, name)
                
                yield total_name, op

class CurrentFormatProperties(bpy.types.PropertyGroup):
    @classmethod
    def _clear_props(cls):
        keys_to_remove = list(cls._keys())
        
        for key in keys_to_remove:
            delattr(cls, key)
        
        CurrentFormatProperties.__dict = None
    
    @classmethod
    def _add_props(cls, template):
        for key, value in iter_public_bpy_props(template):
            setattr(cls, key, value)
        
        CurrentFormatProperties.__dict = {}
        for key in dir(template):
            value = getattr(template, key)
            if is_bpy_prop(value): continue
            CurrentFormatProperties.__dict[key] = value
    
    @classmethod
    def _keys(cls, exclude_hidden=False):
        for kv in iter_public_bpy_props(cls, exclude_hidden):
            yield kv[0]
    
    def __getattr__(self, name):
        return CurrentFormatProperties.__dict[name]
    
    def __setattr__(self, name, value):
        if hasattr(self.__class__, name) and (not name.startswith("_")):
            supercls = super(CurrentFormatProperties, self.__class__)
            supercls.__setattr__(self, name, value)
        else:
            CurrentFormatProperties.__dict[name] = value

class ColladaEmulator:
    # Special case: Collada (built-in) -- has no explicitly defined Python properties
    apply_modifiers = bpy.props.BoolProperty(name="Apply Modifiers", description="Apply modifiers to exported mesh (non destructive)", default=False)
    #export_mesh_type=0 # couldn't find correspondence in the UI
    export_mesh_type_selection = bpy.props.EnumProperty(name="Type of modifiers", description="Modifier resolution for export", default='view', items=[('render', "Render", "Apply modifier's render settings"), ('view', "View", "Apply modifier's view settings")])
    selected = bpy.props.BoolProperty(name="Selection Only", description="Export only selected elements", default=False)
    include_children = bpy.props.BoolProperty(name="Include Children", description="Export all children of selected objects (even if not selected)", default=False)
    include_armatures = bpy.props.BoolProperty(name="Include Armatures", description="Export related armatures (even if not selected)", default=False)
    include_shapekeys = bpy.props.BoolProperty(name="Include Shape Keys", description="Export all Shape Keys from Mesh Objects", default=True)
    deform_bones_only = bpy.props.BoolProperty(name="Deform Bones only", description="Only export deforming bones with armatures", default=False)
    active_uv_only = bpy.props.BoolProperty(name="Only Active UV layer", description="Export textures assigned to the object UV maps", default=False)
    include_uv_textures = bpy.props.BoolProperty(name="Include UV Textures", description="Export textures assigned to the object UV maps", default=False)
    include_material_textures = bpy.props.BoolProperty(name="Include Material Textures", description="Export textures assigned to the object Materials", default=False)
    use_texture_copies = bpy.props.BoolProperty(name="Copy Textures", description="Copy textures to the same folder where .dae file is exported", default=True)
    triangulate = bpy.props.BoolProperty(name="Triangulate", description="Export Polygons (Quads & NGons) as Triangles", default=True)
    use_object_instantiation = bpy.props.BoolProperty(name="Use Object Instances", description="Instantiate multiple Objects from same Data", default=True)
    sort_by_name = bpy.props.BoolProperty(name="Sort by Object name", description="Sort exported data by Object name", default=False)
    #export_transformation_type=0 # couldn't find correspondence in the UI
    export_transformation_type_selection = bpy.props.EnumProperty(name="Transformation Type", description="Transformation type for translation, scale and rotation", default='matrix', items=[('both', "Both", "Use <matrix> AND <translate>, <rotate>, <scale> to specify transformations"), ('transrotloc', "TransLocRot", "Use <translate>, <rotate>, <scale> to specify transformations"), ('matrix', "Matrix", "Use <matrix> to specify transformations")])
    open_sim = bpy.props.BoolProperty(name="Export for OpenSim", description="Compatibility mode for OpenSim and compatible online worlds", default=False)
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Export Data Options", icon='MESH_DATA')
        row = box.split(0.6)
        row.prop(self, "apply_modifiers")
        row.prop(self, "export_mesh_type_selection", text="")
        box.prop(self, "selected")
        box.prop(self, "include_children")
        box.prop(self, "include_armatures")
        box.prop(self, "include_shapekeys")
        
        box = layout.box()
        box.label(text="Texture Options", icon='TEXTURE')
        box.prop(self, "active_uv_only")
        box.prop(self, "include_uv_textures")
        box.prop(self, "include_material_textures")
        box.prop(self, "use_texture_copies", text="Copy")
        
        box = layout.box()
        box.label(text="Armature Options", icon='ARMATURE_DATA')
        box.prop(self, "deform_bones_only")
        box.prop(self, "open_sim")
        
        box = layout.box()
        box.label(text="Collada Options", icon='MODIFIER')
        box.prop(self, "triangulate")
        box.prop(self, "use_object_instantiation")
        row = box.split(0.6)
        row.label(text="Transformation Type")
        row.prop(self, "export_transformation_type_selection", text="")
        box.prop(self, "sort_by_name")

class ExportSelected(bpy.types.Operator, ExportHelper):
    '''Export selected objects to a chosen format'''
    bl_idname = "export_scene.selected"
    bl_label = "Export Selected"
    
    filename_ext = bpy.props.StringProperty(
        default="",
        options={'HIDDEN'},
        )
    
    filter_glob = bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        )
    
    selection_mode = bpy.props.EnumProperty(
        name="Selection Mode",
        description="Limit/expand the selection",
        default='SELECTED',
        items=[
            ('SELECTED', "Selected", ""),
            ('VISIBLE', "Visible", ""),
            ('ALL', "All", ""),
        ],
        )
    
    include_children = bpy.props.BoolProperty(
        name="Include Children",
        description="Keep children even if they're not selected",
        default=True,
        )
    
    remove_orphans = bpy.props.BoolProperty(
        name="Remove Orphans",
        description="Remove datablocks that have no users",
        default=True,
        )
    
    keep_materials = bpy.props.BoolProperty(
        name="Keep Materials",
        description="Keep Materials",
        default=True,
        )
    
    keep_textures = bpy.props.BoolProperty(
        name="Keep Textures",
        description="Keep Textures",
        default=True,
        )
    
    keep_world_textures = bpy.props.BoolProperty(
        name="Keep World Textures",
        description="Keep World Textures",
        default=False,
        )
    
    object_types = bpy.props.EnumProperty(
        name="Object types",
        description="Object type(s) to export",
        default={'ALL'},
        items=[
            ('ALL', "All", ""),
            ('MESH', "Mesh", ""),
            ('CURVE', "Curve", ""),
            ('SURFACE', "Surface", ""),
            ('META', "Meta", ""),
            ('FONT', "Font", ""),
            ('ARMATURE', "Armature", ""),
            ('LATTICE', "Lattice", ""),
            ('EMPTY', "Empty", ""),
            ('CAMERA', "Camera", ""),
            ('LAMP', "Lamp", ""),
            ('SPEAKER', "Speaker", ""),
        ],
        options={'ENUM_FLAG'},
        )
    
    visible_name = bpy.props.StringProperty(
        name="Visible name",
        description="Visible name",
        options={'HIDDEN'},
        )
    
    format = bpy.props.StringProperty(
        name="Format",
        description="Export format",
        options={'HIDDEN'},
        )
    
    format_props = bpy.props.PointerProperty(
        type=CurrentFormatProperties,
        options={'HIDDEN'},
        )
    
    props_initialized = bpy.props.BoolProperty(
        options={'HIDDEN'},
        default=False,
        )
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.objects) != 0
    
    def fill_props(self):
        if self.props_initialized: return
        
        CurrentFormatProperties._clear_props()
        
        if self.format:
            op = get_op(self.format)
            op_class = type(op.get_instance())
            
            if self.format == "wm.collada_export":
                op_class = ColladaEmulator
            
            CurrentFormatProperties._add_props(op_class)
        else:
            self.visible_name = "Blend"
            self.filename_ext = ".blend"
            self.filter_glob = "*.blend"
        
        self.props_initialized = True
    
    def invoke(self, context, event):
        self.fill_props()
        self.filepath = context.object.name + self.filename_ext
        return ExportHelper.invoke(self, context, event)
    
    def clear_world(self, context):
        bpy.ops.ed.undo_push(message="Delete unselected")
        
        for scene in bpy.data.scenes:
            if scene != context.scene:
                bpy.data.scenes.remove(scene)
        
        scene = context.scene
        
        objs = set()
        
        def add_obj(obj):
            if self.object_types.intersection({'ALL', obj.type}):
                objs.add(obj)
            
            if self.include_children:
                for child in obj.children:
                    add_obj(child)
        
        for obj in scene.objects:
            if (self.selection_mode == 'SELECTED') and obj.select:
                add_obj(obj)
            elif (self.selection_mode == 'VISIBLE') and obj.is_visible(scene):
                obj.hide_select = False
                add_obj(obj)
            elif (self.selection_mode == 'ALL'):
                obj.hide_select = False
                add_obj(obj)
        
        for obj in scene.objects:
            if obj in objs:
                obj.select = True
            else:
                scene.objects.unlink(obj)
                bpy.data.objects.remove(obj)
        scene.update()
        
        if not self.format:
            if not self.keep_materials:
                for material in bpy.data.materials:
                    material.user_clear()
                    bpy.data.materials.remove(material)
            
            if not self.keep_textures:
                for world in bpy.data.worlds:
                    for i in range(len(world.texture_slots)):
                        world.texture_slots.clear(i)
                for material in bpy.data.materials:
                    for i in range(len(material.texture_slots)):
                        material.texture_slots.clear(i)
                for brush in bpy.data.brushes:
                    brush.texture = None
                for texture in bpy.data.textures:
                    texture.user_clear()
                    bpy.data.textures.remove(texture)
            elif not self.keep_world_textures:
                for world in bpy.data.worlds:
                    for i in range(len(world.texture_slots)):
                        world.texture_slots.clear(i)
            
            if self.remove_orphans:
                datablocks_cleanup_order = [
                    #"window_managers",
                    #"screens",
                    "scenes",
                    "worlds",
                    
                    "grease_pencil",
                    "fonts",
                    "scripts",
                    "texts",
                    "movieclips",
                    "actions",
                    "speakers",
                    "sounds",
                    "brushes",
                    
                    "node_groups",
                    "groups",
                    "objects",
                    
                    "armatures",
                    "cameras",
                    "lamps",
                    "lattices",
                    "shape_keys",
                    "meshes",
                    "metaballs",
                    "particles",
                    "curves",
                    
                    "materials",
                    "textures",
                    "images",
                    
                    "libraries",
                ]
                for datablocks_name in datablocks_cleanup_order:
                    datablocks = getattr(bpy.data, datablocks_name)
                    if type(datablocks).__name__ == "bpy_prop_collection":
                        for datablock in datablocks:
                            if datablock.users == 0:
                                datablocks.remove(datablock)
        
        if self.format in join_before_export:
            bpy.ops.object.convert()
            bpy.ops.object.join()
    
    def execute(self, context):
        with ToggleObjectMode(undo=None):
            self.clear_world(context)
            
            if self.format:
                props = {}
                for key in CurrentFormatProperties._keys():
                    props[key] = getattr(self.format_props, key)
                props["filepath"] = self.filepath
                
                op = get_op(self.format)
                
                op(**props)
            else:
                bpy.ops.wm.save_as_mainfile(
                    filepath=self.filepath,
                    copy=True,
                )
            
            bpy.ops.ed.undo()
            bpy.ops.ed.undo_push(message="Export Selected")
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.label("Export " + self.visible_name)
        
        layout.prop(self, "selection_mode", text="")
        layout.prop(self, "include_children")
        layout.prop_menu_enum(self, "object_types")
        
        layout.box()
        
        if not self.format:
            layout.prop(self, "remove_orphans")
            layout.prop(self, "keep_materials")
            layout.prop(self, "keep_textures")
            sublayout = layout.row()
            sublayout.enabled = self.keep_textures
            sublayout.prop(self, "keep_world_textures")
            return
        
        op = get_op(self.format)
        op_class = type(op.get_instance())
        
        if self.format == "wm.collada_export":
            op_class = ColladaEmulator
        
        if hasattr(op_class, "draw"):
            self.format_props.layout = layout
            op_class.draw(self.format_props, context)
        else:
            for key in CurrentFormatProperties._keys(True):
                if key == 'filepath': continue
                layout.prop(self.format_props, key)

class OBJECT_MT_selected_export(bpy.types.Menu):
    bl_idname = "OBJECT_MT_selected_export"
    bl_label = "Selected"
    
    def draw(self, context):
        layout = self.layout
        
        def def_op(visible_name, total_name="", layout=layout):
            if visible_name.lower().startswith("export "):
                visible_name = visible_name[len("export "):]
            
            if total_name:
                op = get_op(total_name)
                if not op.poll():
                    layout = layout.row()
                    layout.enabled = False
            
            op_info = layout.operator(
                ExportSelected.bl_idname,
                text=visible_name,
                )
            op_info.format = total_name
            op_info.visible_name = visible_name
            
            return op_info
        
        # Special case: export to .blend (the default)
        def_op("Blend")
        
        # Special case: Collada is built-in, resides
        # in an unconventional category, and has no
        # explicit ext/glob properties defined
        op_info = def_op("Collada", "wm.collada_export")
        op_info.filename_ext = ".dae"
        op_info.filter_glob = "*.dae"
        
        for total_name, op in iter_exporters():
            op_class = type(op.get_instance())
            rna = op.get_rna()
            
            op_info = def_op(rna.rna_type.name, total_name)
            
            if hasattr(op_class, "filename_ext"):
                op_info.filename_ext = op_class.filename_ext
            
            if hasattr(rna, "filter_glob"):
                op_info.filter_glob = rna.filter_glob

def menu_func_export(self, context):
    self.layout.menu("OBJECT_MT_selected_export", text="Selected")

def register():
    bpy.utils.register_class(CurrentFormatProperties)
    bpy.utils.register_class(ExportSelected)
    bpy.utils.register_class(OBJECT_MT_selected_export)
    #bpy.types.INFO_MT_file_export.prepend(menu_func_export)

def unregister():
    #bpy.types.INFO_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(OBJECT_MT_selected_export)
    bpy.utils.unregister_class(ExportSelected)
    bpy.utils.unregister_class(CurrentFormatProperties)




#####################################################################################################################################
#####################################################################################################################################
##########  edges set length  #######################################################################################################
##########  edges set length  #######################################################################################################

#bl_info = {
#	'name': "edges set length", # and angle
#	'description': "edges set length", # and angle
#	'author': "Yi Danyang",
#	'version': (0, 0, 1, 1),
#	'blender': (2, 7, 0, 5),
#	'api': 'a8282da',
#	'location': 'Shit+Alt+E or [Toolbar][Tools][Mesh Tools] Edges Length', # and Angle
#	'warning': "",
#	'category': 'Mesh',
#	"wiki_url": "mailto:yidanyang@gmail.com",
#	"tracker_url": "mailto:yidanyang@gmail.com",
#}




#定义操作
class LengthChange(bpy.types.Operator):
	#操作名称(2.70.5 原本是mesh.edge，但现在工具栏是OT，要加入这个位置还只能是object，也许以后会修改)
	bl_idname = "object.mesh_edge_lengthchange"
	#标签
	bl_label = "length_change"
	#返回
	bl_options = {'REGISTER', 'UNDO'}
	#缩放中心
	pin_point = EnumProperty(
		name="pin",
		items=(("s", "start", "start"), 
			   ("c", "center", "center"), 
			   ("e", "end", "end")),
		default='s',
		description="center for scale")
	#目标长度
	target_length = FloatProperty( name = 'length', default = 1, min = 0.0000001, step = 1, precision = 3 )
	
	#中心
	@classmethod
	def poll(cls, context):
		return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

	#运行
	def execute(self, context):
		# message = "Popup Values: %s, %f" % \
			# (self.pin_point, self.target_length )
		# self.report({'INFO'}, message)
		
		
		ob = context.active_object
		if not ob or ob.type != 'MESH':
			self.report({'ERROR'}, '需要激活模型')
			return {'CANCELLED'}
		if ob.data.total_edge_sel == 1:
			# bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
			bpy.ops.object.editmode_toggle()
			bpy.ops.object.editmode_toggle()
			last_cursor_location = context.scene.cursor_location.copy()
			# ob.data.update(calc_edges=True)
			
			# 准备
			vts = ob.data.vertices
			vts_select_id = []
			for i,v in enumerate(vts):
				if v.select == True:
					vts_select_id.append(i)
			# 实现
			current_length = (vts[vts_select_id[0]].co - vts[vts_select_id[1]].co).magnitude
			if abs(current_length - self.target_length) > 0.00001:
				# 输入值 与 当前值 差的大
				if current_length == 0:
					self.report({'ERROR'}, '无法操作重叠点')
					return {'CANCELLED'}
				else:
					target_scale_size = self.target_length / current_length
					# print("%s / %s = %s" % (self.target_length, current_length, target_scale_size))

				# 缩放点
				if self.pin_point == 's':
					context.scene.cursor_location = ob.matrix_world * (vts[vts_select_id[0]].co)
				elif self.pin_point == 'e':
					context.scene.cursor_location = ob.matrix_world * (vts[vts_select_id[1]].co)
				else:
					context.scene.cursor_location = ob.matrix_world * ((vts[vts_select_id[0]].co + vts[vts_select_id[1]].co)/2)

				# 缩放中心
				last_pivot_point = context.space_data.pivot_point
				context.space_data.pivot_point = 'CURSOR'
				
				# 缩放
				bpy.ops.transform.resize(value=(target_scale_size, target_scale_size, target_scale_size))
				
				# 还原
				context.space_data.pivot_point = last_pivot_point
				
			else:
				# 差不多，算了
				pass
				
			# ob.data.update(calc_edges=True)
			context.scene.cursor_location = last_cursor_location
			
		else:
			self.report({'ERROR'}, '仅能操作 1 根线段')
			# 多线段 端点不好决定
			return {'CANCELLED'}	
		return {'FINISHED'}
		
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
		
		
## TODO 有空再做
# class AngleChange(bpy.types.Operator):
	# #操作名称
	# bl_idname = "mesh.edge_anglechange"
	# #标签
	# bl_label = "angle_change"
	# #返回
	# bl_options = {'REGISTER', 'UNDO'}
	# #角度
	# target_angle = FloatProperty( name = 'angle', default = 30, min = 0.00001, max = 360.0, step = 1, precision = 3 )
	# #目标长度
	# target_length = FloatProperty( name = 'length', default = 0.5, min = 0.00001, max = 10.0, step = 1, precision = 3 )
	
	# @classmethod
	# def poll(cls, context):
		# return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

	# #运行
	# def execute(self, context):
		# ob = context.active_object
		# if not ob:
			# self.report({'ERROR'}, 'missing active object')
			# return {'CANCELLED'}	
		# if ob.data.total_edge_sel == 2 and ob.data.total_vert_sel == 3:
			# # TODO
			# pass
		# else:
			# self.report({'ERROR'}, 'missing 2 edge and 3 point this time')
			# return {'CANCELLED'}	
		# return {'FINISHED'}

		
#定义面板
def menu_func(self, context):
	#位置
	self.layout.operator_context = 'INVOKE_DEFAULT'
	#按键
	self.layout.label(text="Edges Length:")	# and Angle
	row = self.layout.row(align=True)
	# row.operator(AngleChange.bl_idname, "Angle")
	row.operator(LengthChange.bl_idname, "Length")
	#分割
	#self.layout.separator()
		
def register():
	#注册操作方法
	bpy.utils.register_class(LengthChange)
	# bpy.utils.register_class(AngleChange)
	bpy.types.VIEW3D_PT_tools_meshedit.append(menu_func)


def unregister():
	#与register对应，卸载功能
	bpy.utils.unregister_class(LengthChange)
	# bpy.utils.unregister_class(AngleChange)
	bpy.types.VIEW3D_PT_tools_meshedit.remove(menu_func)



#####################################################################################################################################
#####################################################################################################################################
##########  Intersection  ###########################################################################################################
##########  Intersection  ###########################################################################################################


#bl_info = {
#    "name": "Intersection",
#    "author": "Witold Jaworski",
#    "version": (1, 2, 1),
#    "blender": (2, 6, 3),
#    "location": "View 3D > Specials [W-key] > Intersection",
#    "category": "Object",
#    "description": "Adds to the mesh of active object its intersection with another mesh object",
#    "warning": "",
#    "wiki_url": "http://airplanes3d.net/scripts-253_e.xml",
#    "tracker_url": "http://airplanes3d.net/track-253_e.xml"
#    }
#----- updates
#2011-09-22 (Witold Jaworski): reversed sequence of Vector*Matrix multiplication to proper Matrix*Vector    
#2012-04-29 (Witold Jaworski): adaptation for Blender 2.63 (BMesh): using the tessfaces instead of faces collection. 
#2012-09-28 (Witold Jaworski): correction (edges of tessfaces have not normalized edge keys, as faces in 2.49). It lead to discarding
#                              most of the founded points as "diagonals".
#2012-09-29 (Witold Jaworski): Further corrections of other errors (concerned with "gluing" the cross points into edges)
#2012-11-05 (Witold Jaworski): Refactoring the Intersect* operators to enable self-intersection of selected and unselected
#                              faces of a single mesh (invoked from Edit Mode).
#2013-10-05 (Andrew Ho): fixed error in CFace.Intersection method (wrong range() function arguments)
#----- imports

####general comments-------------------------------------------------------
#The algorithm for the crossing calculation is following:
#1. Prepare the data - use meshes of selected objects to create two CMesh
#   instances. There no special assumptions about the topology of selected 
#   meshes - they can be a multi-piece mesh, closed or open.
#   Each CMesh stores a list of all faces of assigned object. They are converted
#   into world coordinates and eventually split from quads to triangles. They
#   are the CFace class instances. 
#    We will refer to the CMesh representing the first selected object as mesh A,
#   and the second as mesh B.  
#
#2. For each face from A: check intersection with every face of B faces. Store
#   the found cross points in A.cpoints list. The crossing points are searched
#   first crossing each A's edges (CEdge) with B face triangle. Then the B's 
#      edges are crossed with A's face triangle. There should be always be a zero 
#   or two crossing points (CPoint) found. They are referred to each other, to 
#   allow arrange them into proper loop at the next stage. 
#   (They are found randomly, now, so it is not right place to discover the loop)
#
#3. Arrange the found cross points into properly ordered loops. To find a loop,
#   select the arbitrary (in implementation: first) point from list of found
#   points. Using the references created at 2. find all the ancestors of the 
#   selected point. Then find all precedensors, and connect this two lists
#   to get a complete loop.
#
#
#   In this implementation, to minimize the intersection calculations, first 
#   test is a "box" test: the extents of two faces are compared. Further 
#   calculations are performed only for the faces that have the "box" test 
#   passed.
#      The face's edges (CEdge) are created "on demand", when there is a need to
#   cross them with a face. Many faces will never demand their edges, so they
#   will be never created. Edges, during creation, are referenced by both faces
#   that share it. 
#      This will reduce greatly the number of edges.
#   Each edge "remembers" result of the crossing with each face, so also the
#   calculations with negative result will not be performed twice.
#   In general, this implementation uses heavily the memory, and minimizes
#   the CPU usage as much, as possible. 
#   
#   Below - definitions of four object classes, that take part in the intersection: 
#        CMesh, 
#        CFace, 
#        CEdge, 
#        CPoint (it is the result - cross point, not vertex!)
####constants---------------------------------------------------------------
EPSILON    = 0.00000001 #the tolerance of crossing faces (in world units)
BOX_EPSILON = 0*EPSILON #the tolerance of comparing 'boxes', containing
                        #faces. Actually it seems to have no influence
                        #on the final result.
PIXELS_PER_ICON = 16    #used in the formatting the message popup
PIXELS_PER_CHAR = 6        #used in the formatting the message popup
DEBUG = 1 # Debug level. When nonzero, some diagnostics texts are placed at 
        #   output, during processing. Level = 1 generates some genral
        #   statements, Level = 5 - intermediate, while Level = 9 is the most 
        #   detailed
####globals-----------------------------------------------------------------
_cpoints = []         #The result list of cross points (CPoint) found 
                     #It is a reference to one global result list, 
                     #(it resolved some algorithm problems for printing the CPoint representation)    

####classes-----------------------------------------------------------------

class CMesh:
    """Represents a mesh, one of two used to find the intersection"""

    #private instance fields:
    #__src => Mesh:            Blender's mesh object
    #
    #    working dictionaries, used during intersection:
    #__verts => {Vector}:     a dictionary of mesh vectors - in global space
    #                        coordinates. The key is the Mesh vertex ordinal.
    #__edges => {Edge}:        dictionary of edges, that will be tested.
    #                        The key is a tuple of begin and end vertices 
    #                        ordinals. The smaller ordinal is always the first 
    #                        element    of the tuple key. Initially all values are
    #                        plain indices (integers) to self.__src.edges[] list.                         
    #                        Then, while processing, some of these indices -
    #                        edges that are "suspected" to have a cross
    #                        point with the second mesh - will be replaced with 
    #                        CEdge instances.
    #                        This "suspect" is based on face's spatial
    #                        position. (When they pass the "box" test)
    #__neighbours=>{Face}    dictionary of faces, that form the mesh. In this
    #                        dictionary every face is registered 3 times. (for 
    #                        every edge). The key is a tuple of two edge's 
    #                        vertices ordinals. The sequence of these ordinals 
    #                        matches the direction of the edge along assigned.
    #                        Thus some of these keys will be a reversed version 
    #                        of the keys in the __edges dictionary, the others  
    #                        will be identical.
    #                        For all non-boundary edges there always are two keys,
    #                        one for each face that shares this particular edge.
    #                        The value tuples of such keys are a reversion of 
    #                        each other.
    
    #public instance fields:
    #faces => {Face}        dictionary of faces, that forms the mesh. In this
    #                        dictionary the key is a tuple containing 3 ordinals
    #                        of face vertices. The sequence of these ordinals 
    #                        describes the face direction.
    
    #instance methods:
    def __init__(self, object, use_selected, skip_hidden):
        """Initializes a mesh instance
            Arguments:
                object:         a Blender's object - a Mesh object
                use_selected:   int or Boolean: -1 when use NOT selected faces, 0 (False) when use all, 
                                1 (True) when use selected faces
                skip_hidden:    True to exclude the hidden faces from the intersection 
        """
        def is_selected(select, hide, use_selected, skip_hidden):
            """Helper function to determine vertices and faces to be incorporated into this object
                Arguments:
                    select:    value of the .select flag of a vertex or face
                    hide:      value of the .hide flag of a vertex or face
                    use_selected: int or Boolean: -1 when use NOT selected, 0 (False) when use all, 1 (True) when use selected
                    skip_hidden: True to exclude the hidden faces from the intersection 
            """
            if skip_hidden:
                if use_selected == -1:
                    return (not select and not hide)
                else:
                    if use_selected:
                        return (select and not hide)
                    else:
                        return not hide
            else:
                if use_selected == -1:
                    return (not select)
                else:
                    if use_selected:
                        return (select)
                    else:
                        return True
                
        self.__src = object.data 
        self.__src.calc_tessface()  #force to update the n-gons tesseleation
        self.__neighbours = {}
        self.faces = {}
        #Fill the __edges: dictionary 
        self.__edges = {}
        #we have to use edge_keys, because edges.items() can return edge objects instead of edge indices 
        #(and it can be switched in the middle of the returned list!)
        index = 0 
        for e in self.__src.edge_keys:
            v = e
            if v[0] > v[1] : v = (v[1], v[0]) #normalize the key!
            self.__edges[v] = index #initially all values in this dictionary are edge indices
            index += 1
        
        #fill the __verts dictionary (translate points to worldspace):
        self.__verts = {}
        m = object.matrix_world
        if DEBUG > 8: print("\nVertices %s:" % object.name)
        for v in self.__src.vertices:
            self.__verts[v.index] = m * v.co
            if DEBUG > 8:    print("%s: %s;" % \
                                    (repr(v.index), \
                                    repr(self.__verts[v.index])))                
        
        #register faces:
        #try to find the faces selected, and determine the use_all flag:
        #(this line gives proper result in Object Mode, only!:)
        if use_selected or skip_hidden:
            #verification: do not stick onto use_selected, when nothing is selected!
            if use_selected and not list(filter(lambda f: f.select, self.__src.tessfaces)):
                use_selected = False
                
            selected = list(filter(lambda f: is_selected(f.select, f.hide, use_selected, skip_hidden), self.__src.tessfaces))
        else:
            selected = self.__src.tessfaces #all

        for f in selected:
            if f.area > EPSILON :
                keys = list(f.vertices) #list of 3 or 4 vertex indices (n-gons are tesselated into trangles or quads!)
                if len(keys) == 3: #a triangle - no cut needed
                    self.AddFace(f, (keys[0],keys[1],keys[2]))
                elif len(keys) == 4: #a quad - cut it into two triangles
                    #l0, l2: the lengths of the dialgonals
                    l0 = self.vert(keys[2]) - self.vert(keys[0])
                    l2 = self.vert(keys[3]) - self.vert(keys[1])
                    if l2.length < l0.length: #cut along (1, 3) edge
                        self.AddFace(f, (keys[0],keys[1],keys[3]))
                        self.AddFace(f, (keys[1],keys[2],keys[3]))
                    else: #cut along (0, 2) edge
                        self.AddFace(f, (keys[0],keys[1],keys[2]))
                        self.AddFace(f, (keys[0],keys[2],keys[3]))
                        
    def name(self):
        """Returns the name of wrapped Blender Mesh object
            (useful for diagnostic messages)
        """        
        return self.__src.name
    
    def vert(self, index):
        """Returns one of the mesh vertices (a Vector, in world coordinates)
            Arguments:
                index:    the vertex index in the mesh 
        """
        return self.__verts[index]

    def neighbour(self, edgekey):
        """Returns the face that uses the same edge, but in opposite direction 
            Arguments:
                edgekey:    the key of the edge, along face direction (i.e.
                            NOT normalized: as it is in CFace.__edges dictionary
        """
        #the neighbour HAS to be registered in __neighbours under the 
        #reversed key:
        key = (edgekey[1],edgekey[0])
        if key in self.__neighbours: return self.__neighbours[key]
        else: return None
        
    def cpindex(self,cpoint):
        """Returns index of given cross point (CPoint), or None if not registered
            Arguments:
                cpoint:    a cross point (a CPoint instance) that is chcecked
            
            Used for diagnostics and debbuging, not especially fast.
            For some cross points can return None, because they have been
            discarded during calculations.
        """
        global _cpoints
        if cpoint in _cpoints : return _cpoints.index(cpoint)
        else: return None
        
    def GetEdge(self,key):
        """Returns an edge (CEdge instance) that matches the given key
            Arguments:
                key:    a tuple of 2 integers - vertex ordinals
        """
        key = CEdge.Normalize(key)  #the key may come in non-canonical order
                                    #(smaller ordinal as the second element)
                                    #so we have to get rid of it.
        if key in self.__edges:
            value = self.__edges[key]
            if type(value) == int: #this edge exists in source mesh:
                edge = CEdge(self, self.__src.edges[value], key, \
                                        self.vert(key[0]), self.vert(key[1]))
            else: #edge already prepared:
                return value
        else: #no edge found - this is a diagonal temporary edge:
            edge = CEdge(self, None, key, \
                                    self.vert(key[0]), self.vert(key[1]))

        #add the edge to the edge dictionary:
        self.__edges[key] = edge

        #assign it to two neighbour faces:
        fcount = 0 #count of the faces that share this edge
        if edge.key in self.__neighbours:
            self.__neighbours[edge.key].Assign(edge)
            fcount += 1

        #The other face is registered at inverted the key tuple:
        if edge.altkey() in self.__neighbours:
            self.__neighbours[edge.altkey()].Assign(edge)
            fcount += 1
            
        #edge is a boundary edge, when it is not shared by two faces:
        edge.boundary = (fcount < 2)

        return edge
    
    def AddFace(self, mface, key):
        """    Appends to faces, __neighbours dictionary  (of CFace instances) 
            the newly created face, based on source mesh
            Arguments:
                mface:    a source data - the MFace (may be a quad)
                key:    a tuple of 3 integers - vertex ordinals
        """
        face = CFace(self, mface, key)
        self.faces[key] = face
        
        #in the __neighbour dictionary every face is represented 3 times-
        #by its edges oridnals:
        for k in [(key[0],key[1]),(key[1],key[2]),(key[2],key[0])]:
            self.__neighbours[k] = face
            
    def Intersect(self, key, face):
        """Intersects the face from this mesh, identified by a key, with another
            Arguments:
                key:    tuple (3 integers - vertex ordinals) that identifies 
                        a face in this mesh (in faces dictionary)
                face:    a face from another mesh (CFace)
            
            Returns a list of 2 cross points, or empty list
        """
        global _cpoints
        a,b = self.faces[key],face #a, b are just a shortcuts for the full names
        result = a.Intersect(b)    #store in the list the cross points from a...
        result.extend(b.Intersect(a)) #... together with b.
        if result:
            if DEBUG > 8:    print("\n%s %s x %s %s (%d points):" % \
                                        (a.mesh.name(), repr(a.key), \
                                         b.mesh.name(),repr(b.key),len(result)))
                                        
            #Normally there should be always 2 cross points in the result,
            #but sometimes, when edge from one mesh crosses exactly the edge 
            #from the other mesh, there may appear 1 or 3 points. There may
            #be also, theoretically, 4 (two triangles crossing each other edges)
            #but I have never seen such case. (I have try to obtain it, but
            #there always were 3, 2 or 1 points). 
                                        
            if len(result) == 4: #I have never seen such case 
                if DEBUG:
                    print("4 cross points at crossing %s (%s) with %s (%s)" % \
                          (self.name(), repr(key), face.mesh.name(), repr(face.key)))                                            
            elif len(result) == 3:    #3 cross points
                #points 0 and 1 or 1 and 2 are from the same face:
                #(because we first cross edges A with face B, and 
                #then face A with edges B).
                #
                #Heuristics: put the single point from the other face
                #between the two that belong to the same face.
                #(If we will not give this way a chance to this single
                #additional edge to be assigned, they will often break
                #the prev:next sequence, used to find topological sequence
                #of the found cross points):
                if result[0].edge.mesh is result[1].edge.mesh:
                    #points 0 and 1 are from the same face:
                    r = result[0].vert() - result[1].vert()
                    if r.length > EPSILON: #put this single in the middle:
                        result = [result[0],result[2],result[1]]
                else:
                    #points 1 and 2 are from the same face:
                    r = result[1].vert() - result[2].vert()
                    if r.length > EPSILON: #put this single in the middle:
                        result = [result[1],result[0],result[2]]
            else: pass #len in 1,2: nothing special

            if len(result) > 1: #we will not append the single point to results
            
                #assign the found points into a topological chain:
                prev = result[0]
                for cp in result[1:]:
                    prev.Assign(cp)
                    cp.Assign(prev)
                    prev = cp
                    
                #Special case, when we have 3 cross points:
                #we will try to start collecting data from it.
                #So - let's put it into the unusual place: as the first
                #because the getLoop() function always start with the first
                #all the other points are placed at the end of cpoints[]
                if len(result) == 3: 
                    cp = result[1]
                    if cp not in _cpoints: _cpoints.insert(0,cp)
                    #because result[1] is already on the list, it will be 
                    #discarded in the loop below, and only the items from
                    #the same face will be added at the end of cpoints...

                #store the normal pair in the cpoints list:p
                for cp in result:
                    if cp not in _cpoints: _cpoints.append(cp)
                            
            if DEBUG > 8: #beware tab position: this will print also the discarded ones 
                for cp in result: print(cp)

        return result
    
class CFace:
    """Represents a triangle face, element of the mesh"""
    #instance fields:
    #src => MFace:        the Blender's face object. Because it may be a 
    #                    quad - two CFaces may refer to the same MFace.
    #                    They will differ by the key value
    #mesh =>CMesh        the parent object, that:
    #                                     (mesh.faces[self.key] is self) == True
    #key => (3 int):    the face id (matches the key in CMesh.faces dictionary).
    #                    It is a tuple of face vertices ordinals. It determines
    #                    direction of the face.
    #min =>[3 floats]:    minimum x,y,z face coordinates
    #max =>[3 floats]:    maximum x,y,z face coordinates
    #
    #    private fields
    #__edges=>{3 Edges}:a dictionary of 3 Edge instances. The face edges.
    #                    The key of this dictionary is a tuple of 2 vertex
    #                    ordinals. It should match a key in the parent 
    #                    CMesh.__neigbours dictionary key.
    #                    At the begining all elements are set to None. It is 
    #                    filled with objects when face is suspected to have 
    #                    a cross section with a face from the other mesh.
    #__boundary=>Bool:    True, when face contains a boundary edge. Used by
    #                    HasBoundaryEdge() function, calculated on first demand
    #__normal=>Vector:    normal to this face. Used by normal() function, calcu-
    #                    lated on first demand
    def __init__(self, cmesh, mface, key):
        """Creates a new traingular face, representing a part of a MeshFace
            Arguments:
                cmesh:    parent object (CMesh)
                mface:    a source face, from the original mesh (MeshFace)
                key:    a tuple of 3 vertex ordinals. They should be
                        contained in mface.ed
        """
        self.src = mface
        self.mesh = cmesh
        self.key = key
        v0,v1,v2 = self.vert(0),self.vert(1),self.vert(2)
        self.min = [min(v0.x,v1.x,v2.x)-BOX_EPSILON, \
                    min(v0.y,v1.y,v2.y)-BOX_EPSILON, \
                    min(v0.z,v1.z,v2.z)-BOX_EPSILON]
        self.max = [max(v0.x,v1.x,v2.x)+BOX_EPSILON, \
                    max(v0.y,v1.y,v2.y)+BOX_EPSILON, \
                    max(v0.z,v1.z,v2.z)+BOX_EPSILON]
        #__edges - empty places, for begining. Just to keep their keys
        self.__edges = {}
        for k in [(key[0],key[1]),(key[1],key[2]),(key[2],key[0])]:
            self.__edges[k] = None
            
        #currently unused:
        self.__boundary = None #will be calculated on first demand
        self.__normal = None #will be calculated on first demand
        
    def vert(self, index):
        """Returns one of the face's vertices (a Vector, in world coordinates)
            Arguments:
                index:    the vertex index on the face (0, 1, or 2)
            
            The index==i selects the mesh vertex having ordinal==face.key[i] 
        """
        return self.mesh.vert(self.key[index])

    def Assign(self, edge):
        """Assigns an edge to the face
            Arguments:
                edge:    an edge (CEdge), that has be placed in previously 
                        empty place in face's edge dictionary
        """
        key = edge.key
        #one of two faces that uses this edge has it under reversed tuple key:
        if key not in self.__edges: key = edge.altkey()
        
        if self.__edges[key] is None:
            self.__edges[key] = edge
        elif self.__edges[key] is not edge: 
            if DEBUG > 5:
                print("Attempt to reassign edge %s, in face %s" % \
                                                    (repr(key), repr(self.key)))

    def Intersect(self, face):
        """Intersects a face with another face, from different mesh
            Arguments:
                face:    a face (CFace) from different mesh, to be tested
            
            Returns a list of found crossed points (CPoints). The list may be 
            empty, or contain 1 or 2 points. Points found are the intersections
            of this face EDGES with the surface of the other face, ONLY!
        """
        #first, discard operation when the spatial limits are separate:
        for i in range(0,3): #returns [0,1,2]
            if (self.min[i] > face.max[i] or self.max[i] < face.min[i]): 
                return [] #no cross points
        #if the faces are suspected to have a cross point - check every edge:
        cpoints = []
        for k in self.__edges.keys():
            if not self.__edges[k]: self.__edges[k] = self.mesh.GetEdge(k)
            result = self.__edges[k].Intersect(face)
            if result: 
                cpoints.append(result)
            
        return cpoints

    
class CEdge:
    """Represents an edge - element of the mesh"""
    #instance fields:
    #src => MEdge:        the Blender's edge object. This field may be == None
    #                    for the diagonal edges, created solely for this 
    #                    calculation for quad MeshFaces. Such temporary diagonal
    #                    join two triangle Faces. The src attribute of these
    #                    faces refers to the same quad MeshFace.
    #mesh =>CMesh        the parent object, that:
    #                                 (mesh.__edges[self.key] is self) == True
    #key => (2 int):    the edge id (matches the key in CMesh.__edges dictionary).
    #                    It is a tuple of edge vertices ordinals. It determines
    #                    direction of the edge.
    #org => Vector:        beginning of the edge (world coordinates)
    #ray =>    Vector:        a vector from beginning to the end of the edge
    #boundary => Bool:    True, when it is a boundary edge.
    #
    #private instance fields:
    #__results=>{CPoint}: a dictionary of calculation results, that were already
    #                    performed. Its keys are the keys of the tested faces.
    #                    Presumably, most of the values will be None.
    def __init__(self, mesh, medge, key, v1, v2):
        """Creates a new edge
            Arguments:
            mesh:    the mesh (CMesh) that contains this edge
            medge:    the source edge (a MeshEdge) - may be None for diagonals
            key:    the tuple of two mesh vertex ordinals (integers)
                    that is used as a key in parent's CMesh.__edges dictionary
            v1:        the begining of the edge (a Vector, in worldspace)
            v2:        the end of the edge (a Vector, in worldspace)
            Be sure, that v1 is really the vertex(key[0]), and v2 - vertex(key[1])
        """
        self.mesh = mesh
        self.src = medge
        self.key = key
        self.org = v1
        self.ray = v2 - v1
        self.__results = {}
        self.boundary = False
        
    @staticmethod
    def Normalize(key):
        """Returns a canonical form of a edge key - smaller ordinal first
            Arguments:
                key:    a tuple of two vertex ordinals. They may be in any
                        order
            
            This function is used by CMesh to unify the edge keys, requested
            in a reversed form by faces that share the edge.
        """
        if key[0] < key[1]:    return key
        else: return (key[1],key[0])
    
    def altkey(self):
        """Returns an alternated (reversed) form of the edge key.
        Required by CFace, because it stores their edges in a non-canonical
        form. The order of vertex ordinals in keys of their local edge dictionary
        reflects the local face direction, not the normalized edge key. 
        """
        return (self.key[1], self.key[0])

    def Intersect(self, face):
        """    Calculates the intersection point of this edge and a face.
            Arguments:
                face:    a triangular face (CFace), that belongs to another mesh
                
            Returns a CPoint, if suceeds, or None, when there is no cross point.
            Stores the result in the internal cpoints dictionary.
        """
        if self.ray.length < EPSILON : return None #this edge hardly exists!
        #if we have already meet this face: return the result
        if face.key in self.__results: 
            return self.__results[face.key]
            #if p is None or p.disconnected(): return None #skip over discarded points
            #else: return p
        else: #it has been not tested, yet
            result = None 
            p = intersect_ray_tri(face.vert(0),face.vert(1),face.vert(2), self.ray, self.org)
            if p:
                v = (p - self.org) #result vector
                if v * self.ray > 0: #the ray and the result in the same direction
                    #is the point inside the segment?
                    if v.length <= (self.ray.length + EPSILON) : 
                        result = CPoint(self,face, v.length/self.ray.length)
            #we will also remember the cases which have failed:
            #(just to not repeat them:)
            self.__results[face.key] = result
            return result
        
class CPoint:
    """Represents a cross point of an edge of mesh A and a face of mesh B"""
    #instance fields:
    #edge => Edge:        the edge that contains this cross point
    #face => Face:        the face that contains this cross point
    #                    Beware: the edge the face always belong to different
    #                    CMeshes!
    #t => float:        the location on the edge (0.0-at the beginning, 1.0-at
    #                    the end)
    #prev: CPoint        previous point on the crossing line
    #next: CPoint        next point on the crossing line
    #
    #Beware: during first phase of the calculations - finding the crossing 
    #points, some points may have the next or prev field set to None.
    #The general arrangement of prev->prev->prev or next->next->next between
    #the cross points may be reversed in some places. This is checked and fixed 
    #during second phase of the calculations - the cross point arrangement -
    #by the getTail() global function.
    #In fact, the names "prev" and "next" are somewhat improper, They are,
    #in fact, the references to the neighbors, but the direction is unknown for
    #most of the CPoint instance's "life".
    def __init__(self, edge, face, t):
        """Creates a new instance of cross point
            Arguments:
            edge:    the edge that has this cross point (a CEdge)
            face:    the face that has this cross point (a CFace)
            t:        placement of the cross point (float: 0.0 means
                    'at the begining of the edge', 1.0 means 'at the end')
        """
        self.edge = edge
        self.face = face
        self.t = t
        self.next = self.prev = None #it will be set later
    
    def index(self):
        """Returns an ordinal of this cross point, or None for not registered
            Use for diagnostics or debugging. Some points can be not registered
            in the prent CMesh.cpoints list, because they duplicated the ones
            that are already registered.
        """
        return self.edge.mesh.cpindex(self)
        
    def __repr__(self):
        """Represents content of the instance in a human-readable form
            For the diagnostics and debugging purposes
        """
        #some shortcuts, first
        v = self.vert()
        if self.prev : p = self.prev.index()
        else: p = None
        if self.next : n = self.next.index()
        else: n = None
        if self.edge.src : type = 'Norm'
        else: type = 'Diag'
        #and finally - the result
        result =     "%s: (%1.2f, %1.2f, %1.2f) at %1.2f of '%s' %s (%s) x '%s' %s," % \
                    (repr(self.index()), v.x, v.y, v.z, self.t, \
                     self.edge.mesh.name(), repr(self.edge.key), type, \
                     self.face.mesh.name(), repr(self.face.key))
        if p and n :
            result += "btw: (%s, %s)" % (repr(min(p,n)),repr(max(p,n)))
        else:
            result += "btw: (%s, %s)" % (repr(p),repr(n))
        return result
        
    def Assign(self, cpoint):
        """Assigns a cpoint at free connection point (prev or next)
            Arguments:
                cpoint:    another cross point (CPoint) that has to be connected
        """
        if not cpoint: return #nothing to do
        if self.next is cpoint or self.prev is cpoint: return #already done
        else:
            if not self.next: self.next = cpoint
            elif not self.prev: self.prev = cpoint
            elif DEBUG > 5:
                #sometimes it may happen, when edge from one mesh crosses exactly
                #edge from the other mesh 
                print("Attempt to reassign %s, already assigned to (%s, %s), to %s" % \
                                        (repr(self.index()), repr(self.prev.index()), \
                                         repr(self.next.index()), repr(cpoint.index())))
            else: pass
    
    def GetOpposite(self, cpoint):
        """Returns an opposite cross point to the given one
            Arguments:
                cpoint:    one of two cross points: next or prev
        """
        if cpoint is self.next : return self.prev
        elif cpoint is self.prev: return self.next
        else:    
            if DEBUG > 5: #can happen for points that cross an edge from second mesh
                print("Cross point %d is not referenced by %d" % \
                                                (self.index(), cpoint.index()))

    def vert(self):
        """Returns the location of this point (a Vector, in worldspace)"""
        return self.edge.org + (self.t * self.edge.ray)
    
    def IsTemporary(self):
        """    Returns True, when this point lies on a temporary edge
        
            Some edges of the CMesh do not exists in the source Mesh - they
            are face diagonals, artifically created on quad faces. Such edges
            are temporary - created only for this crossing calculation. 
            Such cross points are usually not wanted in the final result.
        """
        return (self.edge.src is None)  #such edges do not have the source 
                                        #MEdge assigned.
    
    def BelongsTo(self, cmesh):
        """    Returns True, when this point belongs to this mesh
            Arguments:
                cmesh:    mesh (CMesh) to be tested
            
            Cross point belongs to the mesh, that is the owner of the edge that
            has been crossed, not the face.
        """
        return (self.edge.mesh is cmesh)

####module functions--------------------------------------------------------
def show(text, kind='DEBUG'):
    """Shows a popup message
        Arguments:
            text:    message text
            kind:    optional. kind of the information
                    (enumeration like from bpy.types.Operator.report())
    """
    #implemented by MessageReporter class (see below):
    bpy.ops.help.report('INVOKE_DEFAULT', icon=kind, msg=text)
        
def getTail(cpoints, cpoint):
    """Returns a sequence of cross points, that begins with the given point
        Arguments:
            cpioints:    the list of the crosspoints that will be searched;
            cpoint:        the the begin of the sequence - MUST NOT be in cpoints,
                        but cpoint.next or cpoint.prev - should be
        
        This function returns a list containing all successors of the cpoint,
        that are - topologically - on the same side.
        The side does not need to be specified in parameters, because this
        function is    removing from cpoints every element, that is placed in 
        the result list.
        getTail() always tries to find the sequence that begins with the 
        cpoint.next. When you will call it second time - it has no choice, but
        return the sequence that begins with cpoint.prev. 
    """
    result = []
    next = None #if cpoint has no next nor prev in cpoints, this will ensure,
                #that an empty list will be the result
    
    #check out, which direction we will take:
    if cpoint.next in cpoints:         next = cpoint.next
    elif cpoint.prev in cpoints:     next = cpoint.prev
    
    #the cross points reference each other via next and prev without any
    #special order (because they were found randomly). It may happen that
    #the cpoint.prev is the cpoint.prev.prev - when two neighbour cross points
    #have been created at reverse. One thing is sure: the opposite cross point
    #is one of the prev,next pair, so we have utilize the GetOpposite() function
    #to obtain from the next a point that is not the cpoint!
    while next in cpoints:
        cpoints.remove(next) #ensure, that this point will not be used again.
        
        #discard multipled points (they may happen in regular shapes, where 
        #cross points are exactly on face's boundary. For example: crossing of  
        #two identical cubes, where one was moved away by half of their size) 
        #if (next.vert()-cpoint.vert()).length > EPSILON: 
        result.append(next)        
        #proceed to the next one:     
        #give me the next that is on the opposite side than the one (cpoint)
        #that we just have came, and mark actual next as the cpoint:
        cpoint,next = next,next.GetOpposite(cpoint)
    return result

def getLoop(cpoints):
    """Returns from the cpoints points, that forms a continous sequence
        Arguments:
            cpoints: the sequence (a list of CPoints) to be sought
            
        This function removes every matching point from the CPoints seqence, and
        places it in the result list. When it has finished its run, the cpoints
        sequence is empty or contains a bunch of points that belong to another 
        loop. You should repeat call to this function, until you will collect
        all the loops.
    """
    result = []
    if cpoints : #if there is anything to do:
        point = cpoints[0] #we will take an arbitrary point to start with:
        cpoints.remove(point) 
        result.append(point)
        left = (getTail(cpoints,point)) # the "next" part of the loop
        right = getTail(cpoints,point) # the "prev" part of the loop
        
        if left : result.extend(left)
        if right: 
            right.reverse()
            right.extend(result)
            result = right

    return result

def intersect(A,B):
    """Calculates intersection of two mesh objects
        Arguments:
            a:    the first mesh (CMesh)
            b:    the second mesh (CMesh)
        
        Returns a list of the cross points loops found. Every element is a list
        of cross points (CPoint) objects, that represent a single topological 
        loop. These loops may be opened or closed.
    """
    global _cpoints
    _cpoints = [] #reset this class collection...
    for i in A.faces.keys():
        for j in B.faces.keys():
            A.Intersect(i, B.faces[j])
    result = []        
    cpoints = _cpoints[:]
    while cpoints:
        result.append(getLoop(cpoints))
    return result

def create(loop, object, allEdges=False, omit=None):
    """creates a new edge loop in the mesh of given object
        Arguments:
            loop:        list of cross points (CPoint)
            object:        object, which mesh will be used to add the cross edge
            allEdges:    optional. Use all cross points, also the temporary 
                        points that    belong to diagonals of quad faces (Boolean)
            omit:        optional. Cross points that lie on edges of this CMesh
                        should be omitted during drawing
    """
    m = object.matrix_world.copy()
    m.invert() #transformation to object's space
    mesh = object.data #mesh, that will be extended by the new loop
    verts = [] #temporary list of vertices (Vector, object's local space)
    edges = [] #temporary list of edges = two element lists of vertex ordinals
    prev = None #helper: a previously processed CPoint.
    i = 0        #actual vertex number
    base = len(mesh.vertices)     #ordinal of the first vertex, that will be added
                                #to the mesh. (We have use the absolute ordinals)
    for cp in loop:
        #if it is not a point on a non-existant edge, or from mesh to be omitted:
        if     (not cp.IsTemporary() or allEdges) and not cp.BelongsTo(omit):
            vertex = m * cp.vert()
            if prev is None: #Init: we are looking for the first valid point
                r = loop[-1].vert() - cp.vert() #distance from loop ends
                                                #it is = 0 for one element list
                if r.length > EPSILON: #if end and start point do not overlap:
                    verts.append(vertex.to_tuple())
                    prev = cp
                    if DEBUG > 5: print(cp) 
                else: pass #loop ends overlap, proceed to the next cp
            else: #Normal: prev exists!
                r = prev.vert() - cp.vert() #distance from the previous point
                if r.length > EPSILON:
                    verts.append(vertex.to_tuple())
                    i += 1
                    edges.append((base+i-1, base+i))
                    prev = cp
                    if DEBUG > 5: print(cp)
    
    if len(verts) > 1: #if there is sany segment to create:
        #if the loop is a closed loop: add closing edge
        if not (loop[0].edge.boundary or loop[-1].edge.boundary):
            edges.append((base+i, base)) #add the closing segment
            
        #deselect previously selected vertices
        #for v in mesh.vertices: v.select = False
        #and, finally, add new edges:
        count = len(verts)
        mesh.vertices.add(count)
        for v in mesh.vertices[-count:]: 
            v.co = verts[v.index - base]
        count = len(edges)
        base = len(mesh.edges)
        mesh.edges.add(count)
        for e in mesh.edges[-count:]: 
            e.vertices = edges[e.index - base] 
        mesh.update()
        
    
#--- ### Blender Operators
class MessageReporter(bpy.types.Operator):
    ''' Operator created just to have a global method bpy.ops.help.report() 
        for displaying messages to the user in a popup.
    '''
    bl_idname = "help.report"
    bl_label = "Display Message"
    bl_description = "Displays a message on the Info area header"
    
    #--- parameters
    icon = EnumProperty(items = [('DEBUG', 'Debug', 'Debugging message'), 
                                ('INFO', 'Info', 'Informational message'), 
                                ('ERROR', 'Error', 'An error message')
                                ], name = "Type", description = "The kind of the message", default = "DEBUG")
    msg = StringProperty(name="Message", description="Text that will be displayed") #you can use the newline characters, there!
    
    
    #--- Blender interface methods
    def draw(self, context):
        layout = self.layout
        layout.label(self.bl_label + ":", icon=self.icon)
        for txt in self.msg.split("\n"):
            layout.label(txt)
        
    def invoke(self, context, event):
        if self.icon == 'DEBUG':
            return self.execute(context)
        else:
            span = max(list(map(len, self.msg.split("\n"))))*PIXELS_PER_CHAR #maximum length of single row
            span = max(len(self.bl_label)*PIXELS_PER_CHAR + PIXELS_PER_ICON, span) #estimate required popup size
            return context.window_manager.invoke_popup(self, width=span)
    
    def execute(self, context):
        if self.icon == 'DEBUG':
            print(self.bl_label + ":",self.msg)
        else:
            self.report(self.icon, self.msg)
        return {'FINISHED'}
    
#the only reason of existence for this operator is that the "interactive" operators,
#which displays its parametres in Tool Properties pane, have to finish in the same
#mode, in which it has started its execution. 
#In this case we start in Object Mode, but finish in Edit Mode.     
class IntersectObjects(bpy.types.Operator):
    ''' Create an edge of intersection of active object with another one 
    '''
    bl_idname = "object.intersection"
    bl_label = "Intersection"
    bl_description = "Adds to active object (to its mesh) an edge of intersection with another mesh object"
    #--- parameters (copy of the IntersectMeshes parameters)
    use_both = BoolProperty(name="Use both meshes", description="Include points found on the edges of the second mesh", default=True)
    use_selected = BoolProperty(name="Use selected faces", description="Restrict processed area to the selected faces, only (ignored, when nothing is selected)", default=True)
    use_diagonals = BoolProperty(name="Use diagonals", description="Include points found on the diagonals of quad faces", default=False)
        
    #--- Blender interface methods
    @classmethod
    def poll(cls,context):
        return (context.mode == 'OBJECT' and context.object and context.object.type == 'MESH')
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"use_selected")
        layout.prop(self,"use_both")
        layout.prop(self,"use_diagonals")
        
    def invoke(self, context, event):
        #similar check, like in IntersectMeshes, but different way of communication:
        sel = context.selected_objects
        
        if len(sel) != 2:
            msg = "Select two mesh objects ({0} selected)"
            msg = msg.format(len(sel))
            self.report(type={'ERROR'}, message=msg)
            return {'CANCELLED'}
        
        if sel[0].type == sel[1].type == 'MESH':    
            if DEBUG: print("\nObjects that will be crossed: \n%s \nand \n%s." % (sel[0].name,sel[1].name))            
            return bpy.context.window_manager.invoke_props_dialog(self, width = 160)
        else:
            self.report(type = {'ERROR'}, message="Select two meshes to get their intersection")
            return {'CANCELLED'}
    
    def execute(self, context):
        #bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.intersect_meshes('INVOKE_DEFAULT', use_both = self.use_both, use_selected = self.use_selected, use_diagonals = self.use_diagonals)
        return {'FINISHED'}
        
class IntersectMeshes(bpy.types.Operator):
    ''' Calculates intersection of two selected mesh objects or a single mesh 
        Places the result as a new edge(s) in the mesh of active object
    '''
    bl_idname = "mesh.intersect_meshes"
    bl_label = "Intersection"
    bl_description = "Create an intersection (one or more edge loops) of selected and unselected faces (hidden elements are omitted)"
    bl_options = {'REGISTER', 'UNDO'} #Set this options, if you want to edit in Tools pane the properties of this operator
    
    #--- parameters
    use_both = BoolProperty(name="Use both faces", description="Include points found on the edges of the unselected faces", default=True)
    use_selected = BoolProperty(name="Use selected faces", description="Restrict processed area to the selected faces, only (ignored, when invoked in Edit Mode)", options={'HIDDEN'}, default=True)
    use_diagonals = BoolProperty(name="Use diagonals", description="Include points found on the diagonals of quad faces", default=False)
    skip_hidden = BoolProperty(name="Skip hidden faces", description="True, when in Edit Mode (single mesh cut), False when in Object Mode (two objects cut)", options={'HIDDEN'}, default=True)
    
    #--- Blender interface methods
    @classmethod
    def poll(cls,context):
        return (context.mode == 'EDIT_MESH' or context.mode == 'OBJECT') #It is invoked in Object mode by the IntersectObjects operator 
    
    def invoke(self, context, event):
        #input validation:
        #list(filter(lambda f: f.select, a.data.polygons))
        if context.mode == 'EDIT_MESH':
            self.skip_hidden = True
            self.use_selected = True

            a = context.active_object
            bpy.ops.object.mode_set(mode='OBJECT')
            if not list(filter(lambda f: f.select, a.data.polygons)): #Nothing selected?
                self.report(type = {'ERROR'}, message="Select the faces you want to intersect with the unselected ones")
                return {'CANCELLED'}
            return self.execute(context)
        else:
            self.skip_hidden = False
            sel = context.selected_objects
            if len(sel) != 2:
                if len(sel) == 1:
                    verb = "is"
                else:
                    verb = "are"
                    
                msg = "This operation requires exactly two selected objects ({0} {1} selected).\n - Switch to Object mode, and select two objects (the 'tool' mesh and this one).\n - Switch back to Edit Mode, and call again this command."
                msg = msg.format(len(sel), verb)
                show(msg, kind='ERROR')
                return {'CANCELLED'}
    
            if sel[0].type == sel[1].type == 'MESH':
                if DEBUG: print("\nObjects that will be crossed: \n%s \nand \n%s." % (sel[0].name,sel[1].name))            
                return self.execute(context)
            else:
                msg = "This operation requires two mesh objects.\nThe second object, you have selected in Object Mode,\nis of different kind ({0})."
                if context.active_object == sel[0]:
                    msg = msg.format(sel[1].type)
                else:
                    msg = msg.format(sel[0].type)
                show(msg, kind='ERROR')
                return {'CANCELLED'}
        
        
    def execute(self, context):
        #fmt="properties: use_selected={0}, use_both={1}, use_diagonals={2}"
        #show(fmt.format(self.use_selected, self.use_both, self.use_diagonals))

        #if we are in the edit mode: switch into 'OBJECT' mode 
        #(execute() can be called continously from the Tool Properties pane):
        global _cpoints
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='OBJECT')#bpy.ops.object.editmode_toggle()
            
        #in object mode we can idenify our objects:
        a = context.active_object
        
        if self.skip_hidden: #Invoked from IntersectMeshes (single mesh cut: selected faces against the unselected) 
            A = CMesh(a, 1, True)
            B = CMesh(a, -1, True)
        else: #Invoked from IntersectObjects 
            #b: the second one
            sel = context.selected_objects
            if a == sel[0]: b = sel[1] 
            else: b = sel[0]
                
            A = CMesh(a, self.use_selected, False)
            B = CMesh(b, self.use_selected, False)

        start = time()
        
        result = intersect(A,B) #main operation!
        
        if DEBUG: 
            seconds = time() - start
            print("\nIn %1.5f seconds created: %d edges, found: %d raw cross points\n" % \
                                        (seconds, len(A._CMesh__edges), len(_cpoints)))
        if DEBUG > 8: #let's look at the results:
            print("Raw result list:")
            for p in _cpoints:
                print(p)
            
            print("\nResult:")
        
        mesh = a.data #this mesh will be extended by the calls to create() function ....

        base = len(mesh.vertices) #first newly added vertex will have this index.
        i = 0
        
        for l in result:
            i += 1
            if DEBUG > 5: 
                print("Loop %d" % i)
                print("  all points ....")
                for p in l : print(p)
                print("  ... and points selected to create the edge:")
                
            #create a loop:    
            if self.use_both: 
                create(l, a, self.use_diagonals)
            else: 
                create(l, a, self.use_diagonals, B)
                
        if result: #any other method of unselecting did not work here: 
            bpy.ops.object.mode_set(mode='EDIT')#bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')#bpy.ops.object.editmode_toggle()
                
        #select the newly created vertices:
        for v in mesh.vertices: v.select = (v.index >= base)
                
        #enter edit mode (to let the user to evaluate the results):
        bpy.ops.object.mode_set(mode='EDIT')#bpy.ops.object.editmode_toggle()
            
        if not result:
            show("No intersection found between this and the other selected object.", kind='INFO')
                
        return {'FINISHED'}
    
def menu_object_draw(self, context):
    if (context.object and context.object.type == 'MESH'):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator(IntersectObjects.bl_idname, "Intersect")
    
def menu_mesh_draw(self, context):
    if (context.object and context.object.type == 'MESH'):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator(IntersectMeshes.bl_idname, "Intersect")

#--- ### Register
def register():
    register_module(__name__)

    bpy.types.VIEW3D_MT_object_specials.prepend(menu_object_draw)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_mesh_draw)
    
def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_mesh_draw)
    bpy.types.VIEW3D_MT_object_specials.remove(menu_object_draw)

    unregister_module(__name__)
    
#if DEBUG > 0:
 #   print("object_intersection.py: new version loaded!") #just to be sure, that we are testing what we should




#####################################################################################################################################
#####################################################################################################################################
##############  Datablock Tools  ####################################################################################################
##############  Datablock Tools #####################################################################################################

#bl_info = {
#    "name": "Datablock Tools",
#    "author": "Vitor Balbio",
#    "version": (1, 1),
#    "blender": (2, 69, 0),
#    "location": "View3D > Object > Datablock Tools",
#    "description": "Some tools to handle Datablocks ",
#    "warning": "",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Datablock_Tools",
#    "tracker_url": "",
#    "category": "3D View"}
	


def CleanImages():
    # Clean Derivative Images
    # para cada objeto selecionado, para cada face verifica se a textura ( com nome já tratado
    # para remover a extensao se necessario) possui "." então busca na lista de imagens a image
    # original e aplica
    
    ImageList = []
    # se o ultimo caracter nao for numero entao remove os ultimos 3 caracteres (formato da imagem)"
    for i in bpy.data.images:
        try:
            a = int(i.name[-1])
            imagename = i.name
        except ValueError:
            imagename, a = os.path.splitext(i.name)
       
        ImageList.append([imagename,i])
    
    
    for obj in bpy.context.selected_objects:
        for uv in obj.data.uv_textures.items():
            for faceTex in uv[1].data:
                image = faceTex.image          
                # se o ultimo caracter nao for numero entao remove os ultimos 3 caracteres (formato da imagem)"
                try:
                    a = int(image.name[-1])
                    imagename = image.name
                except ValueError:
                    imagename, a = os.path.splitext(image.name)
    
                if( ".0" in imagename):
                    for ima_name, ima in ImageList:
                        if((ima_name in imagename) and (".0" not in ima_name)):
                            faceTex.image.user_clear()
                            faceTex.image = ima


class CleanImagesOP(bpy.types.Operator):
    """Replace the ".0x" images with the original and mark this to remove in next load"""
    bl_idname = "object.clean_images"
    bl_label = "Clean Images Datablock"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        
        CleanImages()
        return {'FINISHED'}
    
    
def CleanMaterials():
    # Clean Derivative Materials 
    # para cada objeto da cena se ele tiver um material que contenha "." entao busca na lista
    # de materiais o material original e aplica
    
    matlist = bpy.data.materials
    for obj in bpy.context.selected_objects:
        for mat_slt in obj.material_slots:
            if(mat_slt.material != None): # se não tiver material associado
                if( ".0" in mat_slt.material.name):
                    for mat in matlist:
                        if((mat.name in mat_slt.material.name) and ("." not in  mat.name)):
                            mat_slt.material = mat


class CleanMaterialsOP(bpy.types.Operator):
    """Replace the ".0x" materials with the original and mark this to remove in next load"""
    bl_idname = "object.clean_materials"
    bl_label = "Clean Materials Datablock"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        CleanMaterials()
        return {'FINISHED'}

class SetInstanceOP(bpy.types.Operator):
    """Set all Seletect Objects as instance of Active Object"""
    bl_idname = "object.set_instance"
    bl_label = "Set as Instance"
    
    @classmethod
    def poll(cls, context):
        return ((context.selected_objects is not None) and (context.active_object is not None))
    
    def execute(self, context):
        active_obj = bpy.context.active_object
        for sel_obj in bpy.context.selected_objects:
            sel_obj.data = active_obj.data
        return {'FINISHED'}

class DatablockToolsMenu(bpy.types.Menu):
    bl_label = "Datablock Tools"
    bl_idname = "VIEW_MT_datablock_tools"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.clean_images")
        layout.operator("object.clean_materials")
        layout.operator("object.set_instance")


def draw_item(self, context):
    layout = self.layout
    layout.menu(DatablockToolsMenu.bl_idname)


def register():
    bpy.utils.register_class(CleanImagesOP)
    bpy.utils.register_class(CleanMaterialsOP)
    bpy.utils.register_class(SetInstanceOP)
    bpy.utils.register_class(DatablockToolsMenu)

    # lets add ourselves to the main header
    bpy.types.VIEW3D_MT_object.append(draw_item)


def unregister():
    bpy.utils.register_class(CleanImagesOP)
    bpy.utils.unregister_class(CleanMaterialsOP)
    bpy.utils.unregister_class(SetInstanceOP)
    bpy.utils.unregister_class(DatablockToolsMenu)
    bpy.types.VIEW3D_MT_object.remove(draw_item)




####################################################################################################
#####  Move UV  ####################################################################################
#####  Move UV  ####################################################################################
####################################################################################################


#bl_info = {
    #"name": "Move UV",
    #"description": "Move the UV from 3D view",
    #"author": "kgeogeo",
    #"version": (1, 0),
    #"blender": (2, 6, 3),
    #"category": "Paint"}
     

     
def find_uv(context):
    obj_data =  bmesh.from_edit_mesh(context.object.data)
    l = []
    first = 0
    diff = 0    
    for f,face in enumerate(obj_data.faces):
        for v,vertex in enumerate(face.verts):
            if vertex.select:
                l.append([f,v])                                            
                if first == 0:
                    v1 = vertex.link_loops[0].vert.co
                    sv1 = loc3d2d(context.region,context.space_data.region_3d,v1)
                    v2 = vertex.link_loops[0].link_loop_next.vert.co
                    sv2 = loc3d2d(context.region,context.space_data.region_3d,v2)
                    vres = sv2 - sv1
                    va = vres.angle(Vector((0.0,1.0)))
                    
                    uv1 = vertex.link_loops[0][obj_data.loops.layers.uv.active].uv
                    uv2 = vertex.link_loops[0].link_loop_next[obj_data.loops.layers.uv.active].uv
                    uvres = uv2 - uv1
                    uva = uvres.angle(Vector((0.0,1.0)))
                    diff = uva - va
                    first += 1
                       
    return l,diff  
     
# Oprerator Class to pan the view3D
class MoveUV(bpy.types.Operator):
    bl_idname = "view3d.move_uv"
    bl_label = "Move the UV from 3D view"
       
    l = []
    uva = 0
    first_mouse = FloatVectorProperty(name="OffsetUV", default=(0.0,0.0), subtype = 'XYZ', size=2)
    offsetuv = FloatVectorProperty(name="OffsetUV", default=(0.0,0.0), subtype = 'XYZ', size=2)
    old_offsetuv = FloatVectorProperty(name="old_OffsetUV", default=(0.0,0.0), subtype = 'XYZ', size=2)
    firstuv = FloatVectorProperty(name="FirstUV", default=(0.0,0.0), subtype = 'XYZ', size=2)
       
    @classmethod
    def poll(cls, context):
        return (context.edit_object)
                                                     
    def modal(self, context, event):
        ob = context.object
        obj_data =  bmesh.from_edit_mesh(ob.data)            
        div = 10000      
        self.offsetuv += Vector(((event.mouse_region_x - self.first_mouse.x)/div,
                                 (event.mouse_region_y - self.first_mouse.y)/div))
           
        o = self.offsetuv
        oo = self.old_offsetuv
        for i,j in self.l:
            d = obj_data.faces[i].loops[j][obj_data.loops.layers.uv.active]
            vec = Vector((o.x - o.y, o.x + o.y))
            d.uv = d.uv - Vector((oo.x , oo.y)) + vec  
          
        self.old_offsetuv = vec      
        self.first_mouse = Vector((event.mouse_region_x, event.mouse_region_y))        
        ob.data.update()
     
        if context.user_preferences.inputs.select_mouse == 'LEFT':
            mb = 'LEFTMOUSE'
        else:
            mb = 'RIGHTMOUSE'
           
        if event.type == mb and event.value == 'RELEASE':
            return {'FINISHED'}
        if event.type == 'ESC' and event.value == 'RELEASE':
            return {'CANCELLED'}      
        return {'RUNNING_MODAL'}
                   
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        self.first_mouse = Vector((event.mouse_region_x, event.mouse_region_y))  
        self.l,self.uva = find_uv(context)              
        return {'RUNNING_MODAL'}  
     
     
def register():
    bpy.utils.register_module(__name__)
       
    km = bpy.context.window_manager.keyconfigs.default.keymaps['3D View']
    kmi = km.keymap_items.new("view3d.move_uv", 'G', 'PRESS', alt=True)
     
def unregister():
    bpy.utils.unregister_module(__name__)
       
    km = bpy.context.window_manager.keyconfigs.default.keymaps['3D View']
    for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"view3d.move_uv", }):
        km.keymap_items.remove(kmi)
        
        
        
#######################################################################################################################################
#######################################################################################################################################
# SetTemplateCamera
#       v.2.1
#  (c)Ishidourou 2013
#######################################################################################################################################
#######################################################################################################################################

#name = SetTemplateCamera, exec_from_panel = set.tmpcamera

#bl_info = {
#    "name": "SetTemplateCamera",
#    "author": "ishidourou",
#    "version": (2, 1),
#    "blender": (2, 65, 0),
#    "location": "View3D > Toolbar and View3D",
#    "description": "SetTemplateCamera",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": '3D View'}

def objselect(objct,selection):
    if (selection == 'ONLY'):
        bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = objct
    objct.select = True

def makecamera(loc,rot):
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, 
                            location= loc,
                            rotation= rot,
                            layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True)
                            )

    camera = bpy.context.object
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 10
    camera.name = 'Template Camera'
    #camera.hide_select = True
    #camera.hide = True
    return camera

def makeempty(loc,rot):
    bpy.ops.object.empty_add(type='PLAIN_AXES',
                        view_align=False,
                        location= loc,
                        rotation= rot,
                        layers=(False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
                        )
    empty = bpy.context.object
    empty.empty_draw_type = 'IMAGE'
    empty.empty_draw_size = 10
    empty.name = 'Template Empty'
    empty.color[3] = 0.3   #Transparency
    empty.show_x_ray = True
    return empty
 
    


#---- main ------
class SetTemplateCamera(bpy.types.Operator):

    bl_idname = "set.tmpcamera"
    bl_label = "SetTemplateCamera"
    bl_options = {'REGISTER'}

    my_mode = EnumProperty(name="Template Mode:",
        items = [('SINGLE','Single','0'),
                 ('SEPARATE','3D Separate','1'),
                 ('CONTACT','3D Contact','2')],
                 default = 'SEPARATE')

    def execute(self, context):
        pi = 3.141595
        pq = pi/2
        #mq = -1*pi/2
        rtype = 'BUILTIN_KSI_LocRot'
        sn = bpy.context.scene
        mode = self.my_mode
         
        cloc = [(0, -10, 0),(10, 0, 0),(0, 0, 10)]
        crot = [(pq, 0, 0),(pq, 0, pq),(0, 0, 2*pq)]
        eloc = [(-5, 5, -5),(-5, -5, -5),(-5, -5, -5)]
        erot = [(pq, 0, 0),(pq, 0, pq),(0, 0, 0)]
        cname = ['Front','Side','Top']

        if mode != 'SEPARATE':
            eloc = [(-5, 0, -5),(0, -5, -5),(-5, -5, 0)]

        bpy.context.space_data.show_axis_z = True
        sn.layers[19] = True
        sn.layers[5] = True
        #sn.layers[0] = True

        sn.render.resolution_x = 1000
        sn.render.resolution_y = 1000
 
        camera = makecamera(cloc[0],crot[0])
        for i in range(3):
            sn.frame_set(i+1)
            objselect(camera,'ONLY')
            #cname[i] = camera.name
            camera.location = cloc[i]
            camera.rotation_euler = crot[i]
            bpy.ops.anim.keyframe_insert_menu(type=rtype) 

            empty = makeempty(eloc[i],erot[i])
            if i == 0:
                firstcamera = camera
                firstempty = empty
            objselect(empty,'ONLY')
            objselect(camera,'ADD')
            #bpy.ops.object.parent_set(type='OBJECT')
            if mode == 'SINGLE':
                break
        objselect(firstcamera,'ONLY')
        bpy.ops.view3d.object_as_camera()
        sn.frame_set(1)
        objselect(firstempty,'ONLY')
        
        #for i in range(3):
            #bpy.data.objects[cname[i]].hide = True

        sn.layers[19] = False
            
        print('Finished')
        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#	Registration

def register():
    bpy.utils.register_class(SetTemplateCameraPanel)
    bpy.utils.register_class(SetTemplateCamera)

def unregister():
    bpy.utils.unregister_class(SetTemplateCameraPanel)
    bpy.utils.unregister_class(SetTemplateCamera)




#####################################################################################################################################
#####################################################################################################################################
##############  Curve Split  ########################################################################################################
##############  Curve Split  ########################################################################################################


#bl_info = {
#    'name': "Bezier Curve Split",
#    'author': "luxuy blendercn",
#    'version': (1, 0, 0),
#    'blender': (2, 70, 0),
#    'location': "Property window-->Curve Data Tab-->Shape-->Bezier Curve Split",
#    'warning': "",
#    'category': 'Add Curve'}



#----------------------------------------------------------------------                       
class BezierCurveSplit(bpy.types.Operator):
    bl_idname = "bpt.bezier_curve_split"
    bl_label = "Bezier Curve Split"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        cv=context.object
        flag=1
        for spl in cv.data.splines:
            flag*=(spl.type=='BEZIER')
        if  cv.type=='CURVE' and context.mode=='EDIT_CURVE' and flag:
            return True
        return False

    def execute(self, context):
        
        cv=context.object
        spl_pts=[]
        sel_pts={}
        j=0
        for spl in cv.data.splines:
            pts={}
            sel_pts[j]=[len(spl.bezier_points)]
            for i in range(len(spl.bezier_points)):
                bpt=spl.bezier_points[i]
                
                pts[i]=[bpt.co[:],bpt.handle_left[:],bpt.handle_right[:]]
                
                
                if spl.bezier_points[i].select_control_point:
                    #print("sel pt !!")
                    
                    sel_pts[j].append(i)
            j+=1
            spl_pts.append(pts)

        cv.data.splines.clear()
        
        for key in sel_pts:
            
            num=0
            
            if sel_pts[key][-1]==sel_pts[key][0]-1:
                sel_pts[key].pop()
            for i in sel_pts[key][1:]+[sel_pts[key][0]-1]:
               
                if i!=0:
                    
                    spl=cv.data.splines.new('BEZIER')
                    spl.bezier_points.add(i-num)
                  
                    for j in range(num,i):
                        bpt=spl.bezier_points[j-num]
                       
                        bpt.co=spl_pts[key][j][0]
                        bpt.handle_left=spl_pts[key][j][1]
                        bpt.handle_right=spl_pts[key][j][2]
                    bpt=spl.bezier_points[-1]
                    bpt.co=spl_pts[key][i][0]
                    bpt.handle_left=spl_pts[key][i][1]
                    bpt.handle_right=spl_pts[key][i][2]
                    num=i
   
        return {'FINISHED'}
        
#==========================================================================================
def menu_func(self, context):

    self.layout.operator(BezierCurveSplit.bl_idname)
    




#####################################################################################################################################
#####################################################################################################################################
##############  1D_Scripts  #########################################################################################################
##############  1D_Scripts  #########################################################################################################

#bl_info = {
 #   "name": "1D_Scripts",                     
  #  "author": "Alexander Nedovizin, Paul Kotelevets aka 1D_Inc (concept design)",
   # "version": (0, 2, 15),
    #"blender": (2, 6, 8),
    #"location": "View3D > Toolbar",
    #"category": "Mesh"
#}  

# http://dl.dropboxusercontent.com/u/59609328/Blender-Rus/1D_Scripts.py




def find_index_of_selected_vertex(mesh):  
    selected_verts = [i.index for i in mesh.vertices if i.select]  
    verts_selected = len(selected_verts)  
    if verts_selected <1:  
        return None                            
    else:  
        return selected_verts  


def find_extreme_select_verts(mesh, verts_idx):
    res_vs = []
    edges = mesh.edges  
 
    for v_idx in verts_idx:
        connecting_edges = [i for i in edges if v_idx in i.vertices[:] and i.select]  
        if len(connecting_edges) == 1: 
            res_vs.append(v_idx)
    return res_vs
    

def find_connected_verts(me, found_index, not_list):  
    edges = me.edges  
    connecting_edges = [i for i in edges if found_index in i.vertices[:]]  
    if len(connecting_edges) == 0: 
        return []
    else:  
        connected_verts = []  
        for edge in connecting_edges:  
            cvert = set(edge.vertices[:])   
            cvert.remove(found_index)                            
            vert = cvert.pop()
            if not (vert in not_list) and me.vertices[vert].select:
                connected_verts.append(vert)  
        return connected_verts  
    
    
def find_all_connected_verts(me, active_v, not_list=[], step=0):
    vlist = [active_v]
    not_list.append(active_v)
    step+=1
    list_v_1 = find_connected_verts(me, active_v, not_list)              

    for v in list_v_1:
        list_v_2 = find_all_connected_verts(me, v, not_list, step) 
        vlist += list_v_2
    return vlist  


def bm_vert_active_get(bm):
    for elem in reversed(bm.select_history):
        if isinstance(elem, (bmesh.types.BMVert, bmesh.types.BMEdge, bmesh.types.BMFace)):
            return elem.index, str(elem)[3:4]     
    return None, None

def to_store(obj_name, bm):
    config = bpy.context.window_manager.paul_manager
    active_edge, el = bm_vert_active_get(bm)
    if active_edge != None and el=='E':
        config.object_name_store = obj_name
        config.edge_idx_store = active_edge
        verts = bm.edges[active_edge].verts
        config.vec_store = (verts[1].co - verts[0].co) * \
            bpy.data.objects[obj_name].matrix_world.to_3x3().transposed()
        return
    
    if active_edge != None and el=='V':
        obj_act = bpy.context.active_object
        mesh = obj_act.data
        v2_l = find_connected_verts(mesh, active_edge, [])
        
        if len(v2_l)>0:
            v1 = active_edge
            v2 = v2_l[0]
            edges_idx = [i.index for i in mesh.edges \
                if v1 in i.vertices[:] and v2 in i.vertices[:]] 
                
            if edges_idx:
                config.object_name_store = obj_name
                config.edge_idx_store = edges_idx[0]
                verts = bm.edges[edges_idx[0]].verts
                config.vec_store = (verts[1].co - verts[0].co) * \
                    bpy.data.objects[obj_name].matrix_world.to_3x3().transposed()
                return
                
    config.object_name_store = ''
    config.edge_idx_store = -1
    config.vec_store = mathutils.Vector((0,0,0))
    print_error('Active edge is not detected')
    print('Error: align 02')


def select_mesh_rot(me, matrix):
    verts = [v for v in me.verts if v.select==True]
    for v in verts:
        v.co = v.co*matrix


def store_align():
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    
    obj = bpy.context.active_object
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)  
    
    to_store(obj.name, bm)
    
    bm.free()   
    

def main_align_object(axe='X',project='XY'):
    #print('axe,project',axe,project)
    #bpy.ops.object.mode_set(mode='OBJECT')
    obj_res = bpy.context.active_object
    if obj_res.type=='MESH':
        bpy.ops.object.mode_set(mode='EDIT') 
        bpy.ops.object.mode_set(mode='OBJECT')
    
    config = bpy.context.window_manager.paul_manager
    if config.object_name_store == '':
        print_error('Stored Edge is required')
        print('Error: align 01')
        return False
    
    obj = bpy.data.objects[config.object_name_store]
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)  
    
    # Найдём диагональ Store
    edge_idx = config.edge_idx_store
    verts_edge_store = bm.edges[edge_idx].verts
    vec_diag_store = verts_edge_store[1].co - verts_edge_store[0].co
    
    #obj_res = bpy.context.active_object
    # Развернем объект
    dict_axe = {'X':(1.0,0.0,0.0), 'Y':(0.0,1.0,0.0), 'Z':(0.0,0.0,1.0)}
    aa_vec = dict_axe[axe]
    
    aa = mathutils.Vector(aa_vec) 
    bb = vec_diag_store.normalized()
    
    planes = set(project)
    if 'X' not in planes:
        aa.x=0
        bb.x=0
    if 'Y' not in planes:
        aa.y=0
        bb.y=0
    if 'Z' not in planes:
        aa.z=0
        bb.z=0        

    vec = aa
    q_rot = vec.rotation_difference(bb).to_matrix().to_4x4()
    obj_res.matrix_world *= q_rot
    for obj in bpy.context.scene.objects:
        if obj.select:
            if obj.name!=obj_res.name:
                orig_tmp = obj_res.location-obj.location
                mat_loc = mathutils.Matrix.Translation(orig_tmp)
                mat_loc2 = mathutils.Matrix.Translation(-orig_tmp)
        
                obj.matrix_world *= mat_loc*q_rot*mat_loc2
    return
    
  


def main_align():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT') 
    
    config = bpy.context.window_manager.paul_manager
    if config.object_name_store == '':
        print_error('Stored Edge is required')
        print('Error: align 01')
        return False
    
    obj = bpy.data.objects[config.object_name_store]
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)  
    
    # Найдём диагональ Store
    edge_idx = config.edge_idx_store
    verts_edge_store = bm.edges[edge_idx].verts
    vec_diag_store = verts_edge_store[1].co - verts_edge_store[0].co
    
    # Получим выделенное ребро
    obj_res = bpy.context.active_object
    mesh_act = obj_res.data
    bm_act = bmesh.new()
    bm_act.from_mesh(mesh_act)  
    
    edge_idx_act, el = bm_vert_active_get(bm_act)
    if edge_idx_act == None:
        print_error('Selection with active edge is required')
        print('Error: align 03')
        return False
    
    d_pos = bpy.context.scene.cursor_location - obj_res.location
    if not config.align_dist_z:  
        for v in bm_act.verts:
            if v.select:
                v.co -= d_pos
        
    
    verts_edge_act = bm_act.edges[edge_idx_act].verts
    vec_diag_act = verts_edge_act[1].co - verts_edge_act[0].co
    
    # Сравниваем
    aa = vec_diag_act 
    if config.align_lock_z:
        aa.z = 0
    aa.normalized()
    
    bb = vec_diag_store
    if config.align_lock_z:
        bb.z = 0
    bb.normalized()
    q_rot = bb.rotation_difference(aa).to_matrix().to_4x4()
    
    select_mesh_rot(bm_act, q_rot)
    verts = [v for v in bm_act.verts if v.select==True]
    pos = (verts_edge_store[0].co + obj.location)\
        - (verts_edge_act[0].co + obj_res.location)
        
    if not config.align_dist_z:
        pos = mathutils.Vector((0,0,0)) #bpy.context.scene.cursor_location
    for v in verts:
        pos_z = v.co.z
        v.co = v.co + pos
        if config.align_lock_z:
            v.co.z = pos_z
    
    if not config.align_dist_z:    
        for v in bm_act.verts:
            if v.select:
                v.co += d_pos
            
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bm_act.to_mesh(mesh_act)
    bm_act.free()
    
    bm.free()
    
    bpy.ops.object.mode_set(mode='EDIT') 
    return True
        

def main_spread(context, mode):
    bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.mode_set(mode='EDIT') 
    
    obj = bpy.context.active_object
    me = obj.data

    verts = find_index_of_selected_vertex(me)
    cou_vs = len(verts) - 1
    if verts != None and cou_vs>0:
        extreme_vs = find_extreme_select_verts(me, verts)
        
        if len(extreme_vs) != 2:
            print_error('Single Loop only')
            print('Error: 01')
            return False
        
        list_koeff = []
        
        if mode[0]:
            min_v = min([me.vertices[extreme_vs[0]].co.x,extreme_vs[0]], \
                        [me.vertices[extreme_vs[1]].co.x,extreme_vs[1]])
            max_v = max([me.vertices[extreme_vs[0]].co.x,extreme_vs[0]], \
                        [me.vertices[extreme_vs[1]].co.x,extreme_vs[1]])

            if (max_v[0]-min_v[0]) == 0:
                min_v = [me.vertices[extreme_vs[0]].co.x,extreme_vs[0]]
                max_v = [me.vertices[extreme_vs[1]].co.x,extreme_vs[1]]
            
            sort_list = find_all_connected_verts(me,min_v[1],[])
            
            if len(sort_list) != len(verts):
                print_error('Incoherent loop')
                print('Error: 020')
                return False
            
            step = []
            if mode[3]:
                list_length = []
                sum_length = 0.0
                x_sum = 0.0
                for sl in range(cou_vs):
                    subb = me.vertices[sort_list[sl+1]].co-me.vertices[sort_list[sl]].co
                    length = subb.length
                    sum_length += length
                    list_length.append(sum_length)
                    x_sum += subb.x
                
                for sl in range(cou_vs):
                    tmp = list_length[sl]/sum_length
                    list_koeff.append(tmp)
                    step.append(x_sum * tmp)
            else:
                diap = (max_v[0]-min_v[0])/cou_vs
                for sl in range(cou_vs):
                    step.append((sl+1)*diap)
            
            bpy.ops.object.mode_set(mode='OBJECT') 
            for idx in range(cou_vs):
                me.vertices[sort_list[idx+1]].co.x = me.vertices[sort_list[0]].co.x  + step[idx]

            bpy.ops.object.mode_set(mode='EDIT')  
            
        if mode[1]:
            min_v = min([me.vertices[extreme_vs[0]].co.y,extreme_vs[0]], \
                        [me.vertices[extreme_vs[1]].co.y,extreme_vs[1]])
            max_v = max([me.vertices[extreme_vs[0]].co.y,extreme_vs[0]], \
                        [me.vertices[extreme_vs[1]].co.y,extreme_vs[1]])

            if (max_v[0]-min_v[0]) == 0:
                min_v = [me.vertices[extreme_vs[0]].co.y,extreme_vs[0]]
                max_v = [me.vertices[extreme_vs[1]].co.y,extreme_vs[1]]
            
            sort_list = find_all_connected_verts(me,min_v[1],[])
            if len(sort_list) != len(verts):
                print_error('Incoherent loop')
                print('Error: 021')
                return False

            step = []
            if mode[3]:
                list_length = []
                sum_length = 0.0
                y_sum = 0.0
                if len(list_koeff)==0:
                    for sl in range(cou_vs):
                        subb = me.vertices[sort_list[sl+1]].co-me.vertices[sort_list[sl]].co
                        length = subb.length
                        sum_length += length
                        list_length.append(sum_length)
                        y_sum += subb.y
                    
                    for sl in range(cou_vs):
                        tmp = list_length[sl]/sum_length
                        list_koeff.append(tmp)
                        step.append(y_sum * tmp)
                else:
                    for sl in range(cou_vs):
                        subb = me.vertices[sort_list[sl+1]].co-me.vertices[sort_list[sl]].co
                        y_sum += subb.y
                        tmp = list_koeff[sl]
                        step.append(y_sum * tmp)
                    
            else:
                diap = (max_v[0]-min_v[0])/cou_vs
                for sl in range(cou_vs):
                    step.append((sl+1)*diap)

            bpy.ops.object.mode_set(mode='OBJECT') 
            for idx in range(cou_vs):
                me.vertices[sort_list[idx+1]].co.y = me.vertices[sort_list[0]].co.y  + step[idx]

            bpy.ops.object.mode_set(mode='EDIT')  
            
        if mode[2]:
            min_v = min([me.vertices[extreme_vs[0]].co.z,extreme_vs[0]], \
                        [me.vertices[extreme_vs[1]].co.z,extreme_vs[1]])
            max_v = max([me.vertices[extreme_vs[0]].co.z,extreme_vs[0]], \
                        [me.vertices[extreme_vs[1]].co.z,extreme_vs[1]])

            if (max_v[0]-min_v[0]) == 0:
                min_v = [me.vertices[extreme_vs[0]].co.z,extreme_vs[0]]
                max_v = [me.vertices[extreme_vs[1]].co.z,extreme_vs[1]]
            
            sort_list = find_all_connected_verts(me,min_v[1],[])
            if len(sort_list) != len(verts):
                print_error('Incoherent loop')
                print('Error: 022')
                return False
            
            step = []
            if mode[3]:
                list_length = []
                sum_length = 0.0
                z_sum = 0.0
                if len(list_koeff)==0:
                    for sl in range(cou_vs):
                        subb = me.vertices[sort_list[sl+1]].co-me.vertices[sort_list[sl]].co
                        length = subb.length
                        sum_length += length
                        list_length.append(sum_length)
                        z_sum += subb.z
                    
                    for sl in range(cou_vs):
                        step.append(z_sum * list_length[sl]/sum_length)
                else:
                    for sl in range(cou_vs):
                        subb = me.vertices[sort_list[sl+1]].co-me.vertices[sort_list[sl]].co
                        z_sum += subb.z
                        tmp = list_koeff[sl]
                        step.append(z_sum * tmp)
            else:
                diap = (max_v[0]-min_v[0])/cou_vs
                for sl in range(cou_vs):
                    step.append((sl+1)*diap)
            
            bpy.ops.object.mode_set(mode='OBJECT') 
            for idx in range(cou_vs):
                me.vertices[sort_list[idx+1]].co.z = me.vertices[sort_list[0]].co.z  + step[idx]

            bpy.ops.object.mode_set(mode='EDIT')  
            
    return True


def main_ss(context):
    obj = bpy.context.active_object
    me = obj.data
    
    bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.mode_set(mode='EDIT') 
    
    vs_idx = find_index_of_selected_vertex(me)
    if vs_idx:
        x_coos = [v.co.x for v in me.vertices if v.index in vs_idx]
        y_coos = [v.co.y for v in me.vertices if v.index in vs_idx]
        
        min_x = min(x_coos)
        max_x = max(x_coos)
        
        min_y = min(y_coos)
        max_y = max(y_coos)
        
        len_x = max_x-min_x
        len_y = max_y-min_y
        
        if len_y<len_x:
            bpy.ops.transform.resize(value=(1,0,1), constraint_axis=(False,True,False))
        else:
            bpy.ops.transform.resize(value=(0,1,1), constraint_axis=(True,False,False))


def main_offset(x):
    mode_obj=bpy.context.mode=='OBJECT'
    #print('mode_obj',mode_obj)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT') 
    
    config = bpy.context.window_manager.paul_manager
    if config.object_name_store == '':
        print_error('Stored Edge is required')
        print('Error: offset 01')
        return False
    
    obj = bpy.context.active_object
    obj_edge = bpy.data.objects[config.object_name_store]
    if obj:
        vec = mathutils.Vector(config.vec_store)
        
        if vec.length != 0:
            vec.normalize()
            vec *= x
        me = obj.data
        
        if not mode_obj:
            bm_act = bmesh.new()
            bm_act.from_mesh(me) 
            
            verts_act = find_index_of_selected_vertex(me)
            vec = vec * obj.matrix_local
            for v_idx in verts_act:
                if not config.shift_lockX:
                    bm_act.verts[v_idx].co.x += vec.x
                if not config.shift_lockY:
                    bm_act.verts[v_idx].co.y += vec.y
                if not config.shift_lockZ:
                    bm_act.verts[v_idx].co.z += vec.z
                
            bpy.ops.object.mode_set(mode='OBJECT')
            bm_act.to_mesh(me)
            bm_act.free()
            bpy.ops.object.mode_set(mode='EDIT') 
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            if config.shift_local:
                vec=vec*obj.matrix_world
            if not config.shift_lockX:
                if config.shift_local:
                    mat_loc = mathutils.Matrix.Translation((vec.x,0,0))
                else:
                    obj.location.x += vec.x
                    
            if not config.shift_lockY:
                if config.shift_local:
                    mat_loc = mathutils.Matrix.Translation((0,vec.y,0))
                else:
                    obj.location.y += vec.y
                    
            if not config.shift_lockZ:
                if config.shift_local:
                    mat_loc = mathutils.Matrix.Translation((0,0,vec.z))
                else:
                    obj.location.z += vec.z
                    
            if config.shift_local:
                obj.matrix_world*=mat_loc
                
                
def GetDistToCursor():
    mode = bpy.context.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    if obj:
        d_pos = bpy.context.scene.cursor_location - obj.location
        center = mathutils.Vector((0,0,0))
        
        if mode=='EDIT_MESH':
            me = obj.data
            mode = 'EDIT'
            bm = bmesh.new()
            bm.from_mesh(me) 
            elem, el = bm_vert_active_get(bm)
            if elem != None:
                if el=='V' and bm.verts[elem].select:
                    center = bm.verts[elem].co
                    #print('VERT')
                elif el=='E':
                    center = mathutils.Vector(bm.edges[elem].verts[1].co+bm.edges[elem].verts[0].co) / 2
                    #print('EDGE')
                elif el=='F':
                    center = bm.faces[elem].calc_center_median()
                    #print('FACE')
                center = center * obj.matrix_world.to_3x3().transposed()
    bpy.ops.object.mode_set(mode=mode)    
    return d_pos - center
        

def GetStoreVecLength():
    config = bpy.context.window_manager.paul_manager
    if config.object_name_store == '':
        print_error('Stored Edge is required')
        print('Error: offset 01')
        return False
    
    vec = mathutils.Vector(config.vec_store)
    return vec.length

        
class SSOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.simple_scale_operator"
    bl_label = "SScale operator"
    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main_ss(context)
        return {'FINISHED'}


class SpreadOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.spread_operator"
    bl_label = "Spread operator"
    bl_options = {'REGISTER', 'UNDO'} 
    
    spread_x = bpy.props.BoolProperty(name = 'spread_x', default = False, options = {'HIDDEN'})
    spread_y = bpy.props.BoolProperty(name = 'spread_y', default = False, options = {'HIDDEN'})
    spread_z = bpy.props.BoolProperty(name = 'spread_z', default = True, options = {'HIDDEN'})
    relation = bpy.props.BoolProperty(name = 'relation', default = False)
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if main_spread(context, (self.spread_x, self.spread_y, self.spread_z, self.relation)):
            pass
            #print('spread complete')
        return {'FINISHED'}


class AlignOperator(bpy.types.Operator):
    bl_idname = "mesh.align_operator"
    bl_label = "Align operator"
    bl_options = {'REGISTER', 'UNDO'} 
    
    type_op = bpy.props.IntProperty(name = 'type_op', default = 0, options = {'HIDDEN'})
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.type_op==1:
            store_align()
            config = bpy.context.window_manager.paul_manager
            config.step_len = GetStoreVecLength()
        elif self.type_op==0:
            main_align()
        else:
            scene = bpy.context.scene
            #for obj_a in bpy.context.selected_objects:
            #        bpy.context.scene.objects.active = obj_a
            main_align_object(scene.AxesProperty, scene.ProjectsProperty)
        
        return {'FINISHED'}


class OffsetOperator(bpy.types.Operator):
    bl_idname = "mesh.offset_operator"
    bl_label = "Offset operator"
    bl_options = {'REGISTER', 'UNDO'} 
    
    type_op = bpy.props.IntProperty(name = 'type_op', default = 0, options = {'HIDDEN'})
    sign_op = bpy.props.IntProperty(name = 'sign_op', default = 1, options = {'HIDDEN'})
    
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        config = bpy.context.window_manager.paul_manager
        if self.type_op==0:     # move left / right
            if config.shift_copy:
                if bpy.context.mode=='OBJECT':
                    l_obj=[]
                    ao=bpy.context.active_object.name
                    for obj_a in bpy.context.selected_objects:
                        l_obj.append(obj_a.name)
                    for obj_a in bpy.context.selected_objects:
                        bpy.context.scene.objects.active = obj_a
                        bpy.ops.object.duplicate(linked=config.instance)
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.ops.object.select_pattern(pattern=obj_a.name)
                    for obj_a_name in l_obj:
                        bpy.context.scene.objects[obj_a_name].select=True
                    bpy.context.scene.objects.active = bpy.data.objects[ao]
                    
                elif bpy.context.mode=='EDIT_MESH':                    
                    bpy.ops.mesh.duplicate()
                
            x = config.step_len * self.sign_op
            if bpy.context.mode=='OBJECT':
                for obj_a in bpy.context.selected_objects:
                    bpy.context.scene.objects.active = obj_a
                    main_offset(x)
            else:
                main_offset(x)
        
        elif self.type_op==1:   # get length
            config.step_len = GetStoreVecLength()
        
        elif self.type_op==2:                   # copy
            copy_offset()
        
        elif self.type_op==3: 
            if config.shift_copy:
                if bpy.context.mode=='OBJECT':
                    l_obj=[]
                    ao=bpy.context.active_object.name
                    for obj_a in bpy.context.selected_objects:
                        l_obj.append(obj_a.name)
                    for obj_a in bpy.context.selected_objects:
                        bpy.context.scene.objects.active = obj_a
                        bpy.ops.object.duplicate(linked=config.instance)
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.ops.object.select_pattern(pattern=obj_a.name)
                    for obj_a_name in l_obj:
                        bpy.context.scene.objects[obj_a_name].select=True
                    bpy.context.scene.objects.active = bpy.data.objects[ao]
                    
                elif bpy.context.mode=='EDIT_MESH':                    
                    bpy.ops.mesh.duplicate()
            
            vec = GetDistToCursor()
            config.object_name_store = bpy.context.active_object.name
            config.vec_store = vec
            config.step_len = vec.length
            x = config.step_len
            if bpy.context.mode=='OBJECT':
                ao=bpy.context.active_object.name
                for obj_a in bpy.context.selected_objects:
                    bpy.context.scene.objects.active = obj_a
                    main_offset(x)
                bpy.context.scene.objects.active = bpy.data.objects[ao]
            else:
                main_offset(x)
                
            config.step_len = GetStoreVecLength()
        
        elif self.type_op==4:
            act_obj = bpy.context.active_object
            bpy.ops.object.duplicate(linked=config.instance)
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=act_obj.name)
            bpy.context.scene.objects.active = bpy.data.objects[act_obj.name]
            
        else:
            pass
            
        self.type_op = 0
        self.sign_op = 1
        return {'FINISHED'}




#####################################################################################################################################
#####################################################################################################################################
##############  Sure UVW Map  #######################################################################################################
##############  Sure UVW Map  #######################################################################################################


#bl_info = {
#    "name": "Sure UVW Map v.0.5.1",
#    "author": "Alexander Milovsky (www.milovsky.ru)",
#    "version": (0, 5),
#    "blender": (2, 6, 3),
#    "api": 45093,
#    "location": "Properties > Object Data (below UV Maps), parameters in Tool Properties",
#    "description": "Box / Best Planar UVW Map (Make Material With Raster Texture First!)",
#    "warning": "",
#    "wiki_url": "http://blenderartists.org/forum/showthread.php?236631-Addon-Simple-Box-UVW-Map-Modifier",
#    "tracker_url": "https://projects.blender.org/tracker/index.php",
#    "category": "Mesh"}



# globals for Box Mapping
all_scale_def = 1
tex_aspect = 1.0
x_offset_def = 0
y_offset_def = 0
z_offset_def = 0
x_rot_def = 0
y_rot_def = 0
z_rot_def = 0


# globals for Best Planar Mapping
xoffset_def = 0
yoffset_def = 0
zrot_def = 0

# Preview flag
preview_flag = True

def show_texture():
    obj = bpy.context.active_object
    mesh = obj.data
    is_editmode = (obj.mode == 'EDIT')
    # if in EDIT Mode switch to OBJECT
    if is_editmode:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # if no UVtex - create it
    if not mesh.uv_textures:
        uvtex = bpy.ops.mesh.uv_texture_add()
    uvtex = mesh.uv_textures.active
    uvtex.active_render = True

    img = None    
    aspect = 1.0
    mat = obj.active_material

    try:
        if mat:
            img = mat.active_texture
            for f in mesh.polygons:  
                if not is_editmode or f.select:
                    uvtex.data[f.index].image = img.image
        else:
            img = None        
    except:
        pass

    # Back to EDIT Mode
    if is_editmode:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)


def box_map():    
    #print('** Boxmap **')
    global all_scale_def,x_offset_def,y_offset_def,z_offset_def,x_rot_def,y_rot_def,z_rot_def, tex_aspect
    obj = bpy.context.active_object
    mesh = obj.data

    is_editmode = (obj.mode == 'EDIT')

    # if in EDIT Mode switch to OBJECT
    if is_editmode:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # if no UVtex - create it
    if not mesh.uv_textures:
        uvtex = bpy.ops.mesh.uv_texture_add()
    uvtex = mesh.uv_textures.active
    #uvtex.active_render = True
    
    img = None    
    aspect = 1.0
    mat = obj.active_material
    try:
        if mat:
            img = mat.active_texture
            aspect = img.image.size[0]/img.image.size[1]
    except:
        pass
    aspect = aspect * tex_aspect

                
    
    #
    # Main action
    #
    if all_scale_def:
        sc = 1.0/all_scale_def
    else:
        sc = 1.0   

    sx = 1 * sc
    sy = 1 * sc
    sz = 1 * sc
    ofx = x_offset_def
    ofy = y_offset_def
    ofz = z_offset_def
    rx = x_rot_def / 180 * pi
    ry = y_rot_def / 180 * pi
    rz = z_rot_def / 180 * pi
    
    crx = cos(rx)
    srx = sin(rx)
    cry = cos(ry)
    sry = sin(ry)
    crz = cos(rz)
    srz = sin(rz)
    ofycrx = ofy * crx
    ofzsrx = ofz * srx
    
    ofysrx = ofy * srx
    ofzcrx = ofz * crx
    
    ofxcry = ofx * cry
    ofzsry = ofz * sry
    
    ofxsry = ofx * sry
    ofzcry = ofz * cry
    
    ofxcry = ofx * cry
    ofzsry = ofz * sry
    
    ofxsry = ofx * sry
    ofzcry = ofz * cry
    
    ofxcrz = ofx * crz
    ofysrz = ofy * srz
    
    ofxsrz = ofx * srz
    ofycrz = ofy * crz
    
    #uvs = mesh.uv_loop_layers[mesh.uv_loop_layers.active_index].data
    uvs = mesh.uv_layers.active.data
    for i, pol in enumerate(mesh.polygons):
        if not is_editmode or mesh.polygons[i].select:
            for j, loop in enumerate(mesh.polygons[i].loop_indices):
                v_idx = mesh.loops[loop].vertex_index
                #print('before[%s]:' % v_idx)
                #print(uvs[loop].uv)
                n = mesh.polygons[i].normal
                co = mesh.vertices[v_idx].co
                x = co.x * sx
                y = co.y * sy
                z = co.z * sz
                if abs(n[0]) > abs(n[1]) and abs(n[0]) > abs(n[2]):
                    # X
                    if n[0] >= 0:
                        uvs[loop].uv[0] =  y * crx + z * srx                    - ofycrx - ofzsrx
                        uvs[loop].uv[1] = -y * aspect * srx + z * aspect * crx  + ofysrx - ofzcrx
                    else:
                        uvs[loop].uv[0] = -y * crx + z * srx                    + ofycrx - ofzsrx
                        uvs[loop].uv[1] =  y * aspect * srx + z * aspect * crx  - ofysrx - ofzcrx
                elif abs(n[1]) > abs(n[0]) and abs(n[1]) > abs(n[2]):
                    # Y
                    if n[1] >= 0:
                        uvs[loop].uv[0] =  -x * cry + z * sry                   + ofxcry - ofzsry
                        uvs[loop].uv[1] =   x * aspect * sry + z * aspect * cry - ofxsry - ofzcry
                    else:
                        uvs[loop].uv[0] =   x * cry + z * sry                   - ofxcry - ofzsry
                        uvs[loop].uv[1] =  -x * aspect * sry + z * aspect * cry + ofxsry - ofzcry
                else:
                    # Z
                    if n[2] >= 0:
                        uvs[loop].uv[0] =   x * crz + y * srz +                 - ofxcrz - ofysrz
                        uvs[loop].uv[1] =  -x * aspect * srz + y * aspect * crz + ofxsrz - ofycrz
                    else:
                        uvs[loop].uv[0] =  -y * srz - x * crz                   + ofxcrz - ofysrz
                        uvs[loop].uv[1] =   y * aspect * crz - x * aspect * srz - ofxsrz - ofycrz
    
    # Back to EDIT Mode
    if is_editmode:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

# Best Planar Mapping
def best_planar_map():
    global all_scale_def,xoffset_def,yoffset_def,zrot_def, tex_aspect
    
    obj = bpy.context.active_object
    mesh = obj.data

    is_editmode = (obj.mode == 'EDIT')

    # if in EDIT Mode switch to OBJECT
    if is_editmode:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # if no UVtex - create it
    if not mesh.uv_textures:
        uvtex = bpy.ops.mesh.uv_texture_add()
    uvtex = mesh.uv_textures.active
    #uvtex.active_render = True
    
    img = None    
    aspect = 1.0
    mat = obj.active_material
    try:
        if mat:
            img = mat.active_texture
            aspect = img.image.size[0]/img.image.size[1]
    except:
        pass
    aspect = aspect * tex_aspect
                
    
    #
    # Main action
    #
    if all_scale_def:
        sc = 1.0/all_scale_def
    else:
        sc = 1.0   

    # Calculate Average Normal
    v = Vector((0,0,0))
    cnt = 0
    for f in mesh.polygons:  
        if f.select:
            cnt += 1
            v = v + f.normal
    
    zv = Vector((0,0,1))
    q = v.rotation_difference(zv)
            

    sx = 1 * sc
    sy = 1 * sc
    sz = 1 * sc
    ofx = xoffset_def
    ofy = yoffset_def
    rz = zrot_def / 180 * pi

    cosrz = cos(rz)
    sinrz = sin(rz)

    #uvs = mesh.uv_loop_layers[mesh.uv_loop_layers.active_index].data
    uvs = mesh.uv_layers.active.data
    for i, pol in enumerate(mesh.polygons):
        if not is_editmode or mesh.polygons[i].select:
            for j, loop in enumerate(mesh.polygons[i].loop_indices):
                v_idx = mesh.loops[loop].vertex_index

                n = pol.normal
                co = q * mesh.vertices[v_idx].co
                x = co.x * sx
                y = co.y * sy
                z = co.z * sz
                uvs[loop].uv[0] =  x * cosrz - y * sinrz + xoffset_def
                uvs[loop].uv[1] =  aspect*(- x * sinrz - y * cosrz) + yoffset_def



    # Back to EDIT Mode
    if is_editmode:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)


class SureUVWOperator(bpy.types.Operator):
    bl_idname = "object.sureuvw_operator"
    bl_label = "Sure UVW Map"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    
    bl_options = {'REGISTER', 'UNDO'}

    
    action = StringProperty()  

    size = FloatProperty(name="Size", default=1.0, precision=4)
    rot = FloatVectorProperty(name="XYZ Rotation")
    offset = FloatVectorProperty(name="XYZ offset", precision=4)

    zrot = FloatProperty(name="Z rotation", default=0.0)
    xoffset = FloatProperty(name="X offset", default=0.0, precision=4)
    yoffset = FloatProperty(name="Y offset", default=0.0, precision=4)
    texaspect = FloatProperty(name="Texture aspect", default=1.0, precision=4)

    flag90 = BoolProperty()
    flag90ccw = BoolProperty()


    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    def execute(self, context):
        #print('** execute **')
        #print(self.action)
        global all_scale_def,x_offset_def,y_offset_def,z_offset_def,x_rot_def,y_rot_def,z_rot_def, xoffset_def, yoffset_def, zrot_def, tex_aspect
                
        all_scale_def = self.size
        tex_aspect = self.texaspect
        
        x_offset_def = self.offset[0]
        y_offset_def = self.offset[1]
        z_offset_def = self.offset[2]
        x_rot_def = self.rot[0]
        y_rot_def = self.rot[1]
        z_rot_def = self.rot[2]

        xoffset_def = self.xoffset
        yoffset_def = self.yoffset
        zrot_def = self.zrot

        
        if self.flag90:
          self.zrot += 90
          zrot_def += 90
          self.flag90 = False

        if self.flag90ccw:
          self.zrot += -90
          zrot_def += -90
          self.flag90ccw = False

        
        if self.action == 'bestplanar':
            best_planar_map()
        elif self.action == 'box':
            box_map()
        elif self.action == 'showtex':
            show_texture()
        elif self.action == 'doneplanar':
            best_planar_map()
        elif self.action == 'donebox':
            box_map()
        
        #print('finish execute')
        return {'FINISHED'}

    def invoke(self, context, event):
        #print('** invoke **')
        #print(self.action)
        global all_scale_def,x_offset_def,y_offset_def,z_offset_def,x_rot_def,y_rot_def,z_rot_def, xoffset_def, yoffset_def, zrot_def, tex_aspect

        self.size = all_scale_def
        self.texaspect = tex_aspect
        self.offset[0] = x_offset_def
        self.offset[1] = y_offset_def
        self.offset[2] = z_offset_def
        self.rot[0] = x_rot_def
        self.rot[1] = y_rot_def
        self.rot[2] = z_rot_def

        
        self.xoffset = xoffset_def
        self.yoffset = yoffset_def
        self.zrot = zrot_def
        
            

        if self.action == 'bestplanar':
            best_planar_map()
        elif self.action == 'box':
            box_map()
        elif self.action == 'showtex':
            show_texture()
        elif self.action == 'doneplanar':
            best_planar_map()
        elif self.action == 'donebox':
            box_map()
            
        #print('finish invoke')
        return {'FINISHED'}


    def draw(self, context):
        if self.action == 'bestplanar' or self.action == 'rotatecw' or self.action == 'rotateccw':
            self.action = 'bestplanar'
            layout = self.layout
            layout.label("Size - "+self.action)
            layout.prop(self,'size',text="")
            layout.label("Z rotation")
            col = layout.column()
            col.prop(self,'zrot',text="")
            row = layout.row()
            row.prop(self,'flag90ccw',text="-90 (CCW)")
            row.prop(self,'flag90',text="+90 (CW)")
            layout.label("XY offset")
            col = layout.column()
            col.prop(self,'xoffset', text="")
            col.prop(self,'yoffset', text="")

            layout.label("Texture aspect")
            layout.prop(self,'texaspect', text="")

            #layout.prop(self,'preview_flag', text="Interactive Preview")
            #layout.operator("object.sureuvw_operator",text="Done").action='doneplanar'
            
        elif self.action == 'box':          
            layout = self.layout
            layout.label("Size")
            layout.prop(self,'size',text="")
            layout.label("XYZ rotation")
            col = layout.column()
            col.prop(self,'rot', text="")
            layout.label("XYZ offset")
            col = layout.column()
            col.prop(self,'offset', text="")
            layout.label("Texture squash (optional)")
            layout.label("Always must be 1.0 !!!")
            layout.prop(self,'texaspect', text="")

            #layout.prop(self,'preview_flag', text="Interactive Preview")        
            #layout.operator("object.sureuvw_operator",text="Done").action='donebox'


def register():
    bpy.utils.register_class(SureUVWOperator)


def unregister():
    bpy.utils.unregister_class(SureUVWOperator)




#####################################################################################################################################
#####################################################################################################################################
##############  Sure UVW Map  #######################################################################################################
##############  Sure UVW Map  #######################################################################################################

#bl_info = {
#    "name": "UV Utility",
#    "author": "Paul Geraskin",
#    "version": (0, 1),
#    "blender": (2, 69, 0),
#    "location": "View3D > ToolBar",
#    "description": "Change Index Of UVMap.",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "UV"}


class UV_IC_Panel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


class UV_IC_TexIndex(PropertyGroup):
    bpy.types.Scene.UVTexIndex = IntProperty(
        name="UVIndexToGet",
        description="get UVIndex of selected objects",
        min=1,
        max=8,
        default=1)

    bpy.types.Scene.UVTexGetName = StringProperty(
        name="UVNameToGet",
             description="get new UVName of selected objects",
             default="UVMap")

    bpy.types.Scene.UVTexRenderActive = BoolProperty(
        name="Set Render Active",
        description="Set Render Active...",
        default=False
    )



class UV_IC_ChangeIndex(UV_IC_Panel, Operator):
    bl_idname = "uvutil.change_index"
    bl_label = "Change Index"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data

            if theObj.type == 'MESH':
                if len(meshData.uv_textures) > meshData.uv_textures.active_index and meshData.uv_textures:
                    # meshData.uv_textures.active_index = 0
                    tmpuvmap = meshData.uv_textures.active
                    tmpuvmap_name = tmpuvmap.name

                    newuvmap = meshData.uv_textures.new()
                    meshData.uv_textures.remove(tmpuvmap)

                    droppedUV = meshData.uv_textures[
                        len(meshData.uv_textures) - 1]
                    droppedUV.name = tmpuvmap_name
                    # droppedUV.active = True
                    # if scene.UVTexRenderActive == True:
                      # droppedUV.active_render = True

        return{'FINISHED'}


class UV_IC_SelectIndex(UV_IC_Panel, Operator):
    bl_idname = "uvutil.select_index"
    bl_label = "Select Index"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data
            indexNew = scene.UVTexIndex - 1

            if theObj.type == 'MESH':
                if len(meshData.uv_textures) > indexNew and meshData.uv_textures:
                    meshData.uv_textures.active_index = indexNew

                    if scene.UVTexRenderActive:
                        meshData.uv_textures[indexNew].active_render = True

        return{'FINISHED'}


class UV_IC_SelectName(UV_IC_Panel, Operator):
    bl_idname = "uvutil.select_name"
    bl_label = "Select Name"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data
            uvName = scene.UVTexGetName

            if theObj.type == 'MESH':
                if meshData.uv_textures:
                    uvToGet = meshData.uv_textures.get(uvName)

                    if uvToGet is not None:
                        uvToGet.active = True

                        if scene.UVTexRenderActive:
                            uvToGet.active_render = True

        return{'FINISHED'}


class UV_IC_RemoveActiveUV(UV_IC_Panel, Operator):
    bl_idname = "uvutil.remove_active"
    bl_label = "Remove Active UV"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data

            if theObj.type == 'MESH':
                if meshData.uv_textures:
                    activeIndex = meshData.uv_textures.active_index

                    if len(meshData.uv_textures) > activeIndex:
                        meshData.uv_textures.remove(
                            meshData.uv_textures[activeIndex])

        return{'FINISHED'}




#####################################################################################################################################
#####################################################################################################################################
##############  Slope2vgroup  #######################################################################################################
##############  Slope2vgroup  #######################################################################################################



#bl_info = {
#    "name": "Slope",
#    "author": "Michel Anders (varkenvarken)",
#    "version": (0, 0, 4),
#    "blender": (2, 68, 0),
#    "location": "View3D > Weights > Slope  and  View3D > Paint > Slope",
#    "description": "Replace active vertex group or vertex color layer with values representing the slope of a face",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Mesh"}


class Slope:

    def weight(self, normal, reference=Vector((0, 0, 1))):
        angle = normal.angle(reference)
        if self.mirror and angle > pi / 2:
            angle = pi - angle
        weight = 0.0
        if angle <= self.low:
            weight = 1.0
        elif angle <= self.high:
            weight = 1 - (angle - self.low) / (self.high - self.low)
            weight = pow(weight, self.power)
        return weight


class Slope2VGroup(bpy.types.Operator, Slope):
    """replace active vertex group or vertex color layer with values representing the slope of a face"""
    bl_idname = "mesh.slope2vgroup"
    bl_label = "Slope2VGroup"
    bl_options = {'REGISTER', 'UNDO'}

    low = bpy.props.FloatProperty(name="Lower limit", description="Angles smaller than this get a unit weight", subtype="ANGLE", default=0, max=pi, min=0)
    high = bpy.props.FloatProperty(name="Upper limit", description="Angles larger than this get a zero weight", subtype="ANGLE", default=pi / 2, max=pi, min=0.01)
    power = bpy.props.FloatProperty(name="Power", description="Shape of mapping curve", default=1, min=0, max=10)
    mirror = bpy.props.BoolProperty(name="Mirror", description="Limit angle to 90 degrees", default=False)
    worldspace = bpy.props.BoolProperty(name="World space", description="Use world space instead of object space coordinates", default=False)

    @classmethod
    def poll(self, context):
        p = (context.mode == 'PAINT_WEIGHT' and
             isinstance(context.scene.objects.active, bpy.types.Object) and
             isinstance(context.scene.objects.active.data, bpy.types.Mesh))
        return p

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        ob = context.active_object
        wmat = ob.matrix_world
        vertex_group = ob.vertex_groups.active
        if vertex_group is None:
            bpy.ops.object.vertex_group_add()
            vertex_group = ob.vertex_groups.active
        mesh = ob.data
        reference = Vector((0, 0, 1))
        if self.worldspace:
            reference = reference * wmat
        for v in mesh.vertices:
            vertex_group.add([v.index], self.weight(v.normal, reference), 'REPLACE')
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        context.scene.update()
        return {'FINISHED'}


class Slope2VCol(bpy.types.Operator, Slope):
    bl_idname = "mesh.slope2vcol"
    bl_label = "Slope2Vcol"
    bl_options = {'REGISTER', 'UNDO'}

    low = bpy.props.FloatProperty(name="Lower limit", description="Angles smaller than this get a unit weight", subtype="ANGLE", default=0, max=pi, min=0)
    high = bpy.props.FloatProperty(name="Upper limit", description="Angles larger than this get a zero weight", subtype="ANGLE", default=pi / 2, max=pi, min=0.01)
    power = bpy.props.FloatProperty(name="Power", description="Shape of mapping curve", default=1, min=0, max=10)
    mirror = bpy.props.BoolProperty(name="Mirror", description="Limit angle to 90 degrees", default=False)
    curve = bpy.props.BoolProperty(name="Use brush curve", description="Apply brush curve after calculculating values", default=False)
    normal = bpy.props.BoolProperty(name="Map normal", description="Convert face normal to vertex colors instead of slope angle", default=False)
    worldspace = bpy.props.BoolProperty(name="World space", description="Use world space instead of object space coordinates", default=False)

    @classmethod
    def poll(self, context):
        p = (context.mode == 'PAINT_VERTEX' and
             isinstance(context.scene.objects.active, bpy.types.Object) and
             isinstance(context.scene.objects.active.data, bpy.types.Mesh))
        return p

    def execute(self, context):
        if self.curve:
            # see: https://projects.blender.org/tracker/index.php?func=detail&aid=36688
            bcurvemap = context.tool_settings.vertex_paint.brush.curve
            bcurvemap.initialize()
            bcurve = bcurvemap.curves[0]
        wmat = context.scene.objects.active.matrix_world
        mesh = context.scene.objects.active.data
        vertex_colors = mesh.vertex_colors.active.data
        for poly in mesh.polygons:
            for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                pnormal = poly.normal
                if self.normal:
                    if self.worldspace:
                        pnormal = wmat * pnormal
                    vertex_colors[loop_index].color = list(map(lambda x: (x + 1) / 2, pnormal.normalized()))  # afaik a normal is not necessarily normalized
                else:
                    if self.worldspace:
                        weight = self.weight(pnormal, Vector((0, 0, 1)) * wmat)
                    else:
                        weight = self.weight(pnormal)
                    if self.curve:
                        weight = bcurve.evaluate(1.0 - weight)
                    vertex_colors[loop_index].color = [weight, weight, weight]
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        context.scene.update()
        return {'FINISHED'}

    def draw(self, context):  # provide a draw function here to show use brush option only with versions that have the new initialize function
        layout = self.layout
        if not self.curve and not self.normal:
            layout.prop(self, 'low')
            layout.prop(self, 'high')
            layout.prop(self, 'power')
        if not self.curve:
            layout.prop(self, 'normal')
        if not self.normal:
            layout.prop(self, 'mirror')
        layout.prop(self, 'worldspace')
        # checking for a specific build is a bit tricky as it may contain other chars than just digits
        if int(search(r'\d+', str(bpy.app.build_revision)).group(0)) > 60054:
            if not self.normal:
                layout.prop(self, 'curve')
                if self.curve:
                    layout.label('Click Paint -> Slope to see effect after changing brush curve')


def menu_func_weight(self, context):
    self.layout.operator(Slope2VGroup.bl_idname, text="Slope",
                         icon='PLUGIN')


def menu_func_vcol(self, context):
    self.layout.operator(Slope2VCol.bl_idname, text="Slope",
                         icon='PLUGIN')


def register():
    bpy.utils.register_class(Slope2VCol)
    bpy.utils.register_class(Slope2VGroup)
    bpy.types.VIEW3D_MT_paint_weight.append(menu_func_weight)
    bpy.types.VIEW3D_MT_paint_vertex.append(menu_func_vcol)


def unregister():
    bpy.types.IVIEW3D_MT_paint_weight.remove(menu_func_weight)
    bpy.types.IVIEW3D_MT_paint_vertex.remove(menu_func_vcol)
    bpy.utils.unregister_class(Slope2VCol)
    bpy.utils.unregister_class(Slope2VGroup)
    


#######################################################################################################################################
#######################################################################################################################################
##############  VisibleVertices #######################################################################################################
##############  VisibleVertices  ######################################################################################################


#bl_info = {
#	"name": "VisibleVertices",
#	"author": "Michel Anders (varkenvarken)",
#	"version": (0, 0, 2),
#	"blender": (2, 70, 0),
#	"location": "View3D > Weight Paint > Weights > Visible Vertices",
#	"description": "Replace active vertex group with weight > 0.0 if visible from active camera, 0.0 otherwise",
#	"warning": "",
#	"wiki_url": "",
#	"tracker_url": "",
#	"category": "Mesh"}


def intersect_ray_quad_3d(quad, origin, destination):
	ray = destination - origin
	p = intersect_ray_tri(quad[0],quad[1],quad[2],ray,origin)
	if p is None:
		p = intersect_ray_tri(quad[2],quad[3],quad[0],ray,origin)
	return p

def intersect_ray_scene(scene, origin, destination):
	direction = destination - origin
	result, object, matrix, location, normal = scene.ray_cast(origin + direction*0.0001, destination)
	if result:
		if object.type == 'Camera': # if have no idea if a camera can return true but just to play safe
			result = False
	return result		
	
class VisibleVertices(bpy.types.Operator):
	bl_idname = "mesh.visiblevertices"
	bl_label = "VisibleVertices"
	bl_options = {'REGISTER', 'UNDO'}


	fullScene = BoolProperty(name="Full Scene", default=True, description="Check wether the view is blocked by objects in the scene.")
	distWeight = BoolProperty(name="Distance Weight", default=True, description="Give less weight to vertices further away from the camera.")
	addModifier = BoolProperty(name="Add Modifier", default=True, description="Add a vertex weight modifier for additional control.")
	margin = FloatProperty(name="Camera Margin", default=0.0, description="Add extra margin to the visual area from te camera (might be negative as well).")

	@classmethod
	def poll(self, context):
		p = (context.mode == 'PAINT_WEIGHT' and
			isinstance(context.scene.objects.active, bpy.types.Object) and
			isinstance(context.scene.objects.active.data, bpy.types.Mesh))
		return p
		
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')

		ob = context.active_object
		vertex_group = ob.vertex_groups.active
		if vertex_group is None:
			bpy.ops.object.vertex_group_add()
			vertex_group = ob.vertex_groups.active
		scene = context.scene
		cam_ob = scene.camera
		cam = bpy.data.cameras[cam_ob.name] # camera in scene is object type, not a camera type
		cam_mat = cam_ob.matrix_world
		view_frame = cam.view_frame(scene)	# without a scene the aspect ratio of the camera is not taken into account
		view_frame = [cam_mat * v for v in view_frame]
		cam_pos = cam_mat * Vector((0,0,0))
		view_center = sum(view_frame, Vector((0,0,0)))/len(view_frame)
		view_normal = (view_center - cam_pos).normalized()

		if self.margin != 0.0:
			view_frame = [((v - view_center)*(1+self.margin))+view_center for v in view_frame] 
		
		mesh_mat = ob.matrix_world
		mesh = ob.data
		distances = []
		max_distance = 0
		min_distance = None
		for v in mesh.vertices:
			vertex_coords = mesh_mat * v.co
			d = None
			intersection = intersect_ray_quad_3d(view_frame, vertex_coords, cam_pos) # check intersection with the camera frame
			print(intersection, end=" | ")
			if intersection is not None:
				d = (intersection - vertex_coords).length
				if self.fullScene:
					if intersect_ray_scene(scene, vertex_coords, cam_pos):	# check intersection with all other objects in scene. We revert the direction, ie. look from the camera to avoid self intersection
						d = None
			if d is not None:
				if d > max_distance :
					max_distance = d
				if min_distance is None or d < min_distance:
					min_distance = d
			distances.append((v.index, d))

		drange = max_distance - min_distance
		print(min_distance, max_distance, drange)
		if self.distWeight and drange > 1e-7:
			print("weighted")
			for vindex, d in distances:
				print(d, end=' ')
				if d is None:
					vertex_group.add([vindex], 0.0, 'REPLACE')
				else:
					vertex_group.add([vindex], 1.0 - ((d - min_distance) / drange), 'REPLACE')
		else:
			print("not weighted")
			for vindex, d in distances:
				print(d, end='')
				if d is None:
					vertex_group.add([vindex], 0.0, 'REPLACE')
				else:
					vertex_group.add([vindex], 1.0 if d > 0.0 else 0.0, 'REPLACE')

		bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
		context.scene.update()
		
		if self.addModifier:
			bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_EDIT')
			ob.modifiers[-1].vertex_group = ob.vertex_groups.active.name
			ob.modifiers[-1].falloff_type = 'CURVE'
			# make modifier panel visible to atract some attention because this is a lesser known modifier
			ws = context.window_manager.windows
			for a in ws[0].screen.areas:
				if(a.type == 'PROPERTIES'):
					for s in a.spaces:
						if s.type == 'PROPERTIES':
							s.context = 'MODIFIER'

		return {'FINISHED'}


def menu_func(self, context):
	self.layout.operator(VisibleVertices.bl_idname, text="Visible Vertices", icon='PLUGIN')

def register():
	bpy.types.VIEW3D_MT_paint_weight.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_paint_weight.remove(menu_func)




#######################################################################################################################################
#######################################################################################################################################
##############  Height  ###############################################################################################################
##############  Height  ###############################################################################################################



#bl_info = {
#    "name": "Height",
#    "author": "Michel Anders (varkenvarken)",
#    "version": (0, 0, 2),
#    "blender": (2, 68, 0),
#    "location": "View3D > Weights > Height  and  View3D > Paint > Height",
#    "description": "Replace active vertex group or vertex color layer with values representing the coordinates or height of the vertices",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Mesh"}




class Height:

    def extremes(self, mesh, wmat):
        i = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        if self.abs:
            if self.worldspace:
                mind = min([abs((wmat * v.co)[i]) for v in mesh.vertices])
                maxd = max([abs((wmat * v.co)[i]) for v in mesh.vertices])
            else:
                mind = min([abs(v.co[i]) for v in mesh.vertices])
                maxd = max([abs(v.co[i]) for v in mesh.vertices])
        else:
            if self.worldspace:
                mind = min([(wmat * v.co)[i] for v in mesh.vertices])
                maxd = max([(wmat * v.co)[i] for v in mesh.vertices])
            else:
                mind = min([v.co[i] for v in mesh.vertices])
                maxd = max([v.co[i] for v in mesh.vertices])
        return mind, maxd

    def map(self, coords, mind, maxd, wmat):
        i = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        if self.worldspace:
            d = (wmat * coords)[i]
        else:
            d = coords[i]
        if self.abs:
            d = abs(d)
        w = pow((d - mind) / (maxd - mind), self.power)
        if w < self.low:
            w = 0
        elif w > self.high:
            w = 1
        if self.invert:
            w = 1 - w
        return w


class Height2VGroup(bpy.types.Operator, Height):
    """replace active vertex group or vertex color layer with values representing the coordinates or height of the vertices"""
    bl_idname = "mesh.height2vgroup"
    bl_label = "Height2VGroup"
    bl_options = {'REGISTER', 'UNDO'}

    low = bpy.props.FloatProperty(name="Lower limit", description="Relative distances smaller than this get a zero weight", unit='LENGTH', subtype="DISTANCE", default=0, min=0, max=1)
    high = bpy.props.FloatProperty(name="Upper limit", description="Relative distances greater than this get a unit weight", unit='LENGTH', subtype="DISTANCE", default=1, min=0, max=1)
    power = bpy.props.FloatProperty(name="Power", description="Shape of mapping curve", default=1, min=0, max=10)
    abs = bpy.props.BoolProperty(name="Absolute", description="Treat negative distances as positive", default=False)
    invert = bpy.props.BoolProperty(name="Invert", description="Invert the resulting values", default=False)
    axis = bpy.props.EnumProperty(name="Axis", description="Axis along which the distance is measured",
                                  items=[("X", "X-axis", "X-Axis"), ("Y", "Y-axis", "Y-Axis"), ("Z", "Z-axis", "Z-Axis")], default="Z")
    worldspace = bpy.props.BoolProperty(name="World space", description="Use world space instead of object space coordinates", default=False)

    @classmethod
    def poll(self, context):
        p = (context.mode == 'PAINT_WEIGHT' and
             isinstance(context.scene.objects.active, bpy.types.Object) and
             isinstance(context.scene.objects.active.data, bpy.types.Mesh))
        return p

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        ob = context.active_object
        wmat = ob.matrix_world
        vertex_group = ob.vertex_groups.active
        if vertex_group is None:
            bpy.ops.object.vertex_group_add()
            vertex_group = ob.vertex_groups.active
        mesh = ob.data

        mind, maxd = self.extremes(mesh, wmat)
        for v in mesh.vertices:
            w = self.map(v.co, mind, maxd, wmat)
            vertex_group.add([v.index], w, 'REPLACE')

        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        context.scene.update()
        return {'FINISHED'}


class Height2VCol(bpy.types.Operator, Height):
    bl_idname = "mesh.height2vcol"
    bl_label = "Height2VCol"
    bl_options = {'REGISTER', 'UNDO'}

    low = bpy.props.FloatProperty(name="Lower limit", description="Relative distances smaller than this get a zero weight", unit='LENGTH', subtype="DISTANCE", default=0, min=0, max=1)
    high = bpy.props.FloatProperty(name="Upper limit", description="Relative distances greater than this get a unit weight", unit='LENGTH', subtype="DISTANCE", default=1, min=0, max=1)
    power = bpy.props.FloatProperty(name="Power", description="Shape of mapping curve", default=1, min=0, max=10)
    abs = bpy.props.BoolProperty(name="Absolute", description="Treat negative distances as positive", default=False)
    invert = bpy.props.BoolProperty(name="Invert", description="Invert the resulting values", default=False)
    axis = bpy.props.EnumProperty(name="Axis", description="Axis along which the distance is measured",
                                  items=[("X", "X-axis", "X-Axis"), ("Y", "Y-axis", "Y-Axis"), ("Z", "Z-axis", "Z-Axis")], default="Z")
    worldspace = bpy.props.BoolProperty(name="World space", description="Use world space instead of object space coordinates", default=False)
    curve = bpy.props.BoolProperty(name="Use brush curve", description="Apply brush curve after calculculating values", default=False)

    @classmethod
    def poll(self, context):
        p = (context.mode == 'PAINT_VERTEX' and
             isinstance(context.scene.objects.active, bpy.types.Object) and
             isinstance(context.scene.objects.active.data, bpy.types.Mesh))
        return p

    def draw(self, context):  # provide a draw function here to show use brush option only with versions that have the new initialize function
        layout = self.layout
        if not self.curve:
            layout.prop(self, 'low')
            layout.prop(self, 'high')
            layout.prop(self, 'power')
            layout.prop(self, 'abs')
            layout.prop(self, 'invert')
        layout.prop(self, 'axis')
        layout.prop(self, 'worldspace')
        # checking for a specific build is a bit tricky as it may contain other chars than just digits
        if int(search(r'\d+', str(bpy.app.build_revision)).group(0)) > 60054:
            layout.prop(self, 'curve')
            if self.curve:
                layout.label('Click Paint -> Height to see effect after changing brush curve')

    def execute(self, context):
        if self.curve:
            # see: https://projects.blender.org/tracker/index.php?func=detail&aid=36688
            bcurvemap = context.tool_settings.vertex_paint.brush.curve
            bcurvemap.initialize()
            bcurve = bcurvemap.curves[0]
        wmat = context.scene.objects.active.matrix_world
        mesh = context.scene.objects.active.data
        vertex_colors = mesh.vertex_colors.active.data

        mind, maxd = self.extremes(mesh, wmat)
        for poly in mesh.polygons:
            for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                # use average coordinate of face. Why Vector()? well sometimes Blender's Pyhthon API
                # is not very orthogonal. It beats me why Vertex.co is a vector and MeshPolygon.center isn't ...
                weight = self.map(Vector(poly.center), mind, maxd, wmat)
                if self.curve:
                    weight = bcurve.evaluate(1.0 - weight)
                vertex_colors[loop_index].color = [weight, weight, weight]
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        context.scene.update()
        return {'FINISHED'}


def menu_func_weight(self, context):
    self.layout.operator(Height2VGroup.bl_idname, text="Height",
                         icon='PLUGIN')


def menu_func_vcol(self, context):
    self.layout.operator(Height2VCol.bl_idname, text="Height",
                         icon='PLUGIN')


def register():
    bpy.utils.register_class(Height2VGroup)
    bpy.utils.register_class(Height2VCol)
    bpy.types.VIEW3D_MT_paint_vertex.append(menu_func_vcol)
    bpy.types.VIEW3D_MT_paint_weight.append(menu_func_weight)


def unregister():
    bpy.types.IVIEW3D_MT_paint_weight.remove(menu_func_weight)
    bpy.types.VIEW3D_MT_paint_vertex.remove(menu_func_vcol)
    bpy.utils.unregister_class(Height2VGroup)
    bpy.utils.unregister_class(Height2VCol)



#######################################################################################################################################
#######################################################################################################################################
##############  Setup Wire Materials  #################################################################################################
##############  Setup Wire Materials  #################################################################################################



#bl_info = {
#    "name": "Setup Wire Materials",
#    "autor:" "liero"
#    "version": (0, 4, 0),
#    "blender": (2, 6, 4),
#    "location": "View3D > Tool Shelf",
#    "description": "Set up materials for a Wire Render.",
#    "category": "Material",
#    "url": "http://www.blenderheads.org/forums/es/viewtopic.php?t=932",
#}


def wire_add(mallas):
    if mallas:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = mallas[0]
        for o in mallas: o.select = True
        bpy.ops.object.duplicate()
        obj, sce = bpy.context.object, bpy.context.scene
        for mod in obj.modifiers: obj.modifiers.remove(mod)
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.wireframe(thickness=0.005)
        bpy.ops.object.mode_set()
        for mat in obj.material_slots: bpy.ops.object.material_slot_remove()
        if 'wire_object' in sce.objects.keys():
            sce.objects.get('wire_object').data = obj.data
            sce.objects.get('wire_object').matrix_world = mallas[0].matrix_world
            sce.objects.unlink(obj)
        else:
            obj.name = 'wire_object'
        obj.data.materials.append(bpy.data.materials.get('mat_wireobj'))

    return{'FINISHED'}

class WireMaterials(bpy.types.Operator):
    bl_idname = 'scene.wire_render'
    bl_label = 'Apply Materials'
    bl_description = 'Set Up Materials for a Wire Render'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wm = bpy.context.window_manager
        sce = bpy.context.scene

        if 'mat_clay' not in bpy.data.materials:
            mat = bpy.data.materials.new('mat_clay')
            mat.specular_intensity = 0
        else: mat = bpy.data.materials.get('mat_clay')
        mat.diffuse_color = wm.col_clay
        mat.use_shadeless = wm.shadeless_mat

        if 'mat_wire' not in bpy.data.materials:
            mat = bpy.data.materials.new('mat_wire')
            mat.specular_intensity = 0
            mat.use_transparency = True
            mat.type = 'WIRE'
            mat.offset_z = 0.05
        else: mat = bpy.data.materials.get('mat_wire')
        mat.diffuse_color = wm.col_wire
        mat.use_shadeless = wm.shadeless_mat

        try: bpy.ops.object.mode_set()
        except: pass

        if wm.selected_meshes: objetos = bpy.context.selected_objects
        else: objetos = sce.objects

        mallas = [o for o in objetos if o.type == 'MESH' and o.is_visible(sce) and o.name != 'wire_object']

        for obj in mallas:
            sce.objects.active = obj
            print ('procesando >', obj.name)
            obj.show_wire = wm.wire_view
            for mat in obj.material_slots:
                bpy.ops.object.material_slot_remove()
            obj.data.materials.append(bpy.data.materials.get('mat_wire'))
            obj.data.materials.append(bpy.data.materials.get('mat_clay'))
            obj.material_slots.data.active_material_index = 1
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.object.mode_set()

        if wm.wire_object:
            if 'mat_wireobj' not in bpy.data.materials:
                mat = bpy.data.materials.new('mat_wireobj')
                mat.specular_intensity = 0
            else: mat = bpy.data.materials.get('mat_wireobj')
            mat.diffuse_color = wm.col_wire
            mat.use_shadeless = wm.shadeless_mat
            wire_add(mallas)

        return{'FINISHED'}

bpy.types.WindowManager.selected_meshes = bpy.props.BoolProperty(name='Selected Meshes', default=False, description='Apply materials to Selected Meshes / All Visible Meshes')
bpy.types.WindowManager.shadeless_mat = bpy.props.BoolProperty(name='Shadeless', default=False, description='Generate Shadeless Materials')
bpy.types.WindowManager.col_clay = bpy.props.FloatVectorProperty(name='', description='Clay Color', default=(1.0, 0.9, 0.8), min=0, max=1, step=1, precision=3, subtype='COLOR_GAMMA', size=3)
bpy.types.WindowManager.col_wire = bpy.props.FloatVectorProperty(name='', description='Wire Color', default=(0.1 ,0.0 ,0.0), min=0, max=1, step=1, precision=3, subtype='COLOR_GAMMA', size=3)
bpy.types.WindowManager.wire_view = bpy.props.BoolProperty(name='Viewport Wires', default=False, description='Overlay wires display over solid in Viewports')
bpy.types.WindowManager.wire_object = bpy.props.BoolProperty(name='Create Wire Object', default=False, description='Very slow! - Add a Wire Object to scene to be able to render wires in Cycles')


def register():
    bpy.utils.register_class(WireMaterials)
    bpy.utils.register_class(PanelWMat)

def unregister():
    bpy.utils.unregister_class(WireMaterials)
    bpy.utils.unregister_class(PanelWMat)



#######################################################################################################################################
#######################################################################################################################################
##############  Random Face Material Assigner  ########################################################################################
##############  Random Face Material Assigner  ########################################################################################








########################################################################################################################
########################################################################################################################
##############  Material Utils  ########################################################################################
##############  Material Utils  ########################################################################################


#bl_info = {
#    "name": "Material Utils",
#    "author": "michaelw",
#    "version": (1, 6),
#    "blender": (2, 66, 6),
#    "location": "View3D > Q key",
#    "description": "Menu of material tools (assign, select..)  in the 3D View",
#    "warning": "Buggy, Broken in Cycles mode",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
#                "Scripts/3D interaction/Materials Utils",
#    "tracker_url": "https://projects.blender.org/tracker/index.php?"
#                   "func=detail&aid=22140",
#    "category": "Material"}

"""
This script has several functions and operators, grouped for convenience:

* assign material:
    offers the user a list of ALL the materials in the blend file and an
    additional "new" entry the chosen material will be assigned to all the
    selected objects in object mode.

    in edit mode the selected polygons get the selected material applied.

    if the user chose "new" the new material can be renamed using the
    "last operator" section of the toolbox.
    After assigning the material "clean material slots" and
    "material to texface" are auto run to keep things tidy
    (see description bellow)


* select by material
    in object mode this offers the user a menu of all materials in the blend
    file any objects using the selected material will become selected, any
    objects without the material will be removed from selection.

    in edit mode:  the menu offers only the materials attached to the current
    object. It will select the polygons that use the material and deselect those
    that do not.

* clean material slots
    for all selected objects any empty material slots or material slots with
    materials that are not used by the mesh polygons will be removed.

* remove material slots
    removes all material slots of the active object.

* material to texface
    transfers material assignments to the UV editor. This is useful if you
    assigned materials in the properties editor, as it will use the already
    set up materials to assign the UV images per-face. It will use the first
    enabled image texture it finds.

* texface to materials
    creates texture materials from images assigned in UV editor.

* replace materials
    lets your replace one material by another. Optionally for all objects in
    the blend, otherwise for selected editable objects only. An additional
    option allows you to update object selection, to indicate which objects
    were affected and which not.

* set fake user
    enable/disable fake user for materials. You can chose for which materials
    it shall be set, materials of active / selected / objects in current scene
    or used / unused / all materials.

"""



def fake_user_set(fake_user='ON', materials='UNUSED'):
    if materials == 'ALL':
        mats = (mat for mat in bpy.data.materials if mat.library is None)
    elif materials == 'UNUSED':
        mats = (mat for mat in bpy.data.materials if mat.library is None and mat.users == 0)
    else:
        mats = []
        if materials == 'ACTIVE':
            objs = [bpy.context.active_object]
        elif materials == 'SELECTED':
            objs = bpy.context.selected_objects
        elif materials == 'SCENE':
            objs = bpy.context.scene.objects
        else: # materials == 'USED'
            objs = bpy.data.objects
            # Maybe check for users > 0 instead?

        """ more reable than the following generator:
        for ob in objs:
            if hasattr(ob.data, "materials"):
                for mat in ob.data.materials:
                    if mat.library is None: #and not in mats:
                        mats.append(mat)
        """
        mats = (mat for ob in objs if hasattr(ob.data, "materials") for mat in ob.data.materials if mat.library is None)

    for mat in mats:
        mat.use_fake_user = fake_user == 'ON'

    for area in bpy.context.screen.areas:
        if area.type in ('PROPERTIES', 'NODE_EDITOR'):
            area.tag_redraw()


def replace_material(m1, m2, all_objects=False, update_selection=False):
    # replace material named m1 with material named m2
    # m1 is the name of original material
    # m2 is the name of the material to replace it with
    # 'all' will replace throughout the blend file

    matorg = bpy.data.materials.get(m1)
    matrep = bpy.data.materials.get(m2)

    if matorg != matrep and None not in (matorg, matrep):
        #store active object
        scn = bpy.context.scene

        if all_objects:
            objs = bpy.data.objects

        else:
            objs = bpy.context.selected_editable_objects

        for ob in objs:
            if ob.type == 'MESH':

                match = False

                for m in ob.material_slots:
                    if m.material == matorg:
                        m.material = matrep
                        # don't break the loop as the material can be
                        # ref'd more than once

                        # Indicate which objects were affected
                        if update_selection:
                            ob.select = True
                            match = True

                if update_selection and not match:
                    ob.select = False

    #else:
    #    print('Replace material: nothing to replace')


def select_material_by_name(find_mat_name):
    #in object mode selects all objects with material find_mat_name
    #in edit mode selects all polygons with material find_mat_name

    find_mat = bpy.data.materials.get(find_mat_name)

    if find_mat is None:
        return

    #check for editmode
    editmode = False

    scn = bpy.context.scene

    #set selection mode to polygons
    scn.tool_settings.mesh_select_mode = False, False, True

    actob = bpy.context.active_object
    if actob.mode == 'EDIT':
        editmode = True
        bpy.ops.object.mode_set()

    if not editmode:
        objs = bpy.data.objects
        for ob in objs:
            if ob.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                ms = ob.material_slots
                for m in ms:
                    if m.material == find_mat:
                        ob.select = True
                        # the active object may not have the mat!
                        # set it to one that does!
                        scn.objects.active = ob
                        break
                    else:
                        ob.select = False

            #deselect non-meshes
            else:
                ob.select = False

    else:
        #it's editmode, so select the polygons
        ob = actob
        ms = ob.material_slots

        #same material can be on multiple slots
        slot_indeces = []
        i = 0
        # found = False  # UNUSED
        for m in ms:
            if m.material == find_mat:
                slot_indeces.append(i)
                # found = True  # UNUSED
            i += 1
        me = ob.data
        for f in me.polygons:
            if f.material_index in slot_indeces:
                f.select = True
            else:
                f.select = False
        me.update()
    if editmode:
        bpy.ops.object.mode_set(mode='EDIT')


def mat_to_texface():
    # assigns the first image in each material to the polygons in the active
    # uvlayer for all selected objects

    #check for editmode
    editmode = False

    actob = bpy.context.active_object
    if actob.mode == 'EDIT':
        editmode = True
        bpy.ops.object.mode_set()

    for ob in bpy.context.selected_editable_objects:
        if ob.type == 'MESH':
            #get the materials from slots
            ms = ob.material_slots

            #build a list of images, one per material
            images = []
            #get the textures from the mats
            for m in ms:
                if m.material is None:
                    continue
                gotimage = False
                textures = zip(m.material.texture_slots, m.material.use_textures)
                for t, enabled in textures:
                    if enabled and t is not None:
                        tex = t.texture
                        if tex.type == 'IMAGE':
                            img = tex.image
                            images.append(img)
                            gotimage = True
                            break

                if not gotimage:
                    print('noimage on', m.name)
                    images.append(None)

            # now we have the images
            # applythem to the uvlayer

            me = ob.data
            #got uvs?
            if not me.uv_textures:
                scn = bpy.context.scene
                scn.objects.active = ob
                bpy.ops.mesh.uv_texture_add()
                scn.objects.active = actob

            #get active uvlayer
            for t in  me.uv_textures:
                if t.active:
                    uvtex = t.data
                    for f in me.polygons:
                        #check that material had an image!
                        if images[f.material_index] is not None:
                            uvtex[f.index].image = images[f.material_index]
                        else:
                            uvtex[f.index].image = None

            me.update()

    if editmode:
        bpy.ops.object.mode_set(mode='EDIT')


def assignmatslots(ob, matlist):
    #given an object and a list of material names
    #removes all material slots form the object
    #adds new ones for each material in matlist
    #adds the materials to the slots as well.

    scn = bpy.context.scene
    ob_active = bpy.context.active_object
    scn.objects.active = ob

    for s in ob.material_slots:
        bpy.ops.object.material_slot_remove()

    # re-add them and assign material
    i = 0
    for m in matlist:
        mat = bpy.data.materials[m]
        ob.data.materials.append(mat)
        i += 1

    # restore active object:
    scn.objects.active = ob_active


def cleanmatslots():
    #check for edit mode
    editmode = False
    actob = bpy.context.active_object
    if actob.mode == 'EDIT':
        editmode = True
        bpy.ops.object.mode_set()

    objs = bpy.context.selected_editable_objects

    for ob in objs:
        if ob.type == 'MESH':
            mats = ob.material_slots.keys()

            #check the polygons on the mesh to build a list of used materials
            usedMatIndex = []  # we'll store used materials indices here
            faceMats = []
            me = ob.data
            for f in me.polygons:
                #get the material index for this face...
                faceindex = f.material_index

                #indices will be lost: Store face mat use by name
                currentfacemat = mats[faceindex]
                faceMats.append(currentfacemat)

                # check if index is already listed as used or not
                found = 0
                for m in usedMatIndex:
                    if m == faceindex:
                        found = 1
                        #break

                if found == 0:
                #add this index to the list
                    usedMatIndex.append(faceindex)

            #re-assign the used mats to the mesh and leave out the unused
            ml = []
            mnames = []
            for u in usedMatIndex:
                ml.append(mats[u])
                #we'll need a list of names to get the face indices...
                mnames.append(mats[u])

            assignmatslots(ob, ml)

            # restore face indices:
            i = 0
            for f in me.polygons:
                matindex = mnames.index(faceMats[i])
                f.material_index = matindex
                i += 1

    if editmode:
        bpy.ops.object.mode_set(mode='EDIT')


def assign_mat(matname="Default"):
    # get active object so we can restore it later
    actob = bpy.context.active_object

    # check if material exists, if it doesn't then create it
    found = False
    for m in bpy.data.materials:
        if m.name == matname:
            target = m
            found = True
            break
    if not found:
        target = bpy.data.materials.new(matname)

    # if objectmode then set all polygons
    editmode = False
    allpolygons = True
    if actob.mode == 'EDIT':
        editmode = True
        allpolygons = False
        bpy.ops.object.mode_set()

    objs = bpy.context.selected_editable_objects

    for ob in objs:
        # set the active object to our object
        scn = bpy.context.scene
        scn.objects.active = ob

        if ob.type in {'CURVE', 'SURFACE', 'FONT', 'META'}:
            found = False
            i = 0
            for m in bpy.data.materials:
                if m.name == matname:
                    found = True
                    index = i
                    break
                i += 1
                if not found:
                    index = i - 1
            targetlist = [index]
            assignmatslots(ob, targetlist)

        elif ob.type == 'MESH':
            # check material slots for matname material
            found = False
            i = 0
            mats = ob.material_slots
            for m in mats:
                if m.name == matname:
                    found = True
                    index = i
                    #make slot active
                    ob.active_material_index = i
                    break
                i += 1

            if not found:
                index = i
                #the material is not attached to the object
                ob.data.materials.append(target)

            #now assign the material:
            me = ob.data
            if allpolygons:
                for f in me.polygons:
                    f.material_index = index
            elif allpolygons == False:
                for f in me.polygons:
                    if f.select:
                        f.material_index = index
            me.update()

    #restore the active object
    bpy.context.scene.objects.active = actob
    if editmode:
        bpy.ops.object.mode_set(mode='EDIT')


def check_texture(img, mat):
    #finds a texture from an image
    #makes a texture if needed
    #adds it to the material if it isn't there already

    tex = bpy.data.textures.get(img.name)

    if tex is None:
        tex = bpy.data.textures.new(name=img.name, type='IMAGE')

    tex.image = img

    #see if the material already uses this tex
    #add it if needed
    found = False
    for m in mat.texture_slots:
        if m and m.texture == tex:
            found = True
            break
    if not found and mat:
        mtex = mat.texture_slots.add()
        mtex.texture = tex
        mtex.texture_coords = 'UV'
        mtex.use_map_color_diffuse = True


def texface_to_mat():
    # editmode check here!
    editmode = False
    ob = bpy.context.object
    if ob.mode == 'EDIT':
        editmode = True
        bpy.ops.object.mode_set()

    for ob in bpy.context.selected_editable_objects:

        faceindex = []
        unique_images = []

        # get the texface images and store indices
        if (ob.data.uv_textures):
            for f in ob.data.uv_textures.active.data:
                if f.image:
                    img = f.image
                    #build list of unique images
                    if img not in unique_images:
                        unique_images.append(img)
                    faceindex.append(unique_images.index(img))

                else:
                    img = None
                    faceindex.append(None)

        # check materials for images exist; create if needed
        matlist = []
        for i in unique_images:
            if i:
                try:
                    m = bpy.data.materials[i.name]
                except:
                    m = bpy.data.materials.new(name=i.name)
                    continue

                finally:
                    matlist.append(m.name)
                    # add textures if needed
                    check_texture(i, m)

        # set up the object material slots
        assignmatslots(ob, matlist)

        #set texface indices to material slot indices..
        me = ob.data

        i = 0
        for f in faceindex:
            if f is not None:
                me.polygons[i].material_index = f
            i += 1
    if editmode:
        bpy.ops.object.mode_set(mode='EDIT')

def remove_materials():

	for ob in bpy.data.objects:
		print (ob.name)
		try:
			bpy.ops.object.material_slot_remove()
			print ("removed material from " + ob.name)
		except:
			print (ob.name + " does not have materials.")
# -----------------------------------------------------------------------------
# operator classes:

class VIEW3D_OT_texface_to_material(bpy.types.Operator):
    """Create texture materials for images assigned in UV editor"""
    bl_idname = "view3d.texface_to_material"
    bl_label = "Texface Images to Material/Texture (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if context.selected_editable_objects:
            texface_to_mat()
            return {'FINISHED'}
        else:
            self.report({'WARNING'},
                        "No editable selected objects, could not finish")
            return {'CANCELLED'}


class VIEW3D_OT_assign_material(bpy.types.Operator):
    """Assign a material to the selection"""
    bl_idname = "view3d.assign_material"
    bl_label = "Assign Material (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    matname = StringProperty(
            name='Material Name',
            description='Name of Material to Assign',
            default="",
            maxlen=63,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        mn = self.matname
        print(mn)
        assign_mat(mn)
        cleanmatslots()
        mat_to_texface()
        return {'FINISHED'}


class VIEW3D_OT_clean_material_slots(bpy.types.Operator):
    """Removes any material slots from selected objects """ \
    """that are not used by the mesh"""
    bl_idname = "view3d.clean_material_slots"
    bl_label = "Clean Material Slots (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        cleanmatslots()
        return {'FINISHED'}


class VIEW3D_OT_material_to_texface(bpy.types.Operator):
    """Transfer material assignments to UV editor"""
    bl_idname = "view3d.material_to_texface"
    bl_label = "Material Images to Texface (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        mat_to_texface()
        return {'FINISHED'}

class VIEW3D_OT_material_remove(bpy.types.Operator):
    """Remove all material slots from active objects"""
    bl_idname = "view3d.material_remove"
    bl_label = "Remove All Material Slots (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        remove_materials()
        return {'FINISHED'}


class VIEW3D_OT_select_material_by_name(bpy.types.Operator):
    """Select geometry with this material assigned to it"""
    bl_idname = "view3d.select_material_by_name"
    bl_label = "Select Material By Name (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}
    matname = StringProperty(
            name='Material Name',
            description='Name of Material to Select',
            maxlen=63,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        mn = self.matname
        select_material_by_name(mn)
        return {'FINISHED'}


class VIEW3D_OT_replace_material(bpy.types.Operator):
    """Replace a material by name"""
    bl_idname = "view3d.replace_material"
    bl_label = "Replace Material (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    matorg = StringProperty(
            name="Original",
            description="Material to replace",
            maxlen=63,
            )
    matrep = StringProperty(name="Replacement",
            description="Replacement material",
            maxlen=63,
            )
    all_objects = BoolProperty(
            name="All objects",
            description="Replace for all objects in this blend file",
            default=True,
            )
    update_selection = BoolProperty(
            name="Update Selection",
            description="Select affected objects and deselect unaffected",
            default=True,
            )

    # Allow to replace all objects even without a selection / active object
    #@classmethod
    #def poll(cls, context):
    #    return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        layout.prop_search(self, "matorg", bpy.data, "materials")
        layout.prop_search(self, "matrep", bpy.data, "materials")
        layout.prop(self, "all_objects")
        layout.prop(self, "update_selection")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        replace_material(self.matorg, self.matrep, self.all_objects, self.update_selection)
        return {'FINISHED'}


class VIEW3D_OT_fake_user_set(bpy.types.Operator):
    """Enable / disable fake user for materials"""
    bl_idname = "view3d.fake_user_set"
    bl_label = "Set Fake User (Material Utils)"
    bl_options = {'REGISTER', 'UNDO'}

    fake_user = EnumProperty(
            name="Fake User",
            description="Turn fake user on or off",
            items=(('ON', "On", "Enable fake user"),('OFF', "Off", "Disable fake user")),
            default='ON'
            )

    materials = EnumProperty(
            name="Materials",
            description="Which materials of objects to affect",
            items=(('ACTIVE', "Active object", "Materials of active object only"),
                   ('SELECTED', "Selected objects", "Materials of selected objects"),
                   ('SCENE', "Scene objects", "Materials of objects in current scene"),
                   ('USED', "Used", "All materials used by objects"),
                   ('UNUSED', "Unused", "Currently unused materials"),
                   ('ALL', "All", "All materials in this blend file")),
            default='UNUSED'
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "fake_user", expand=True)
        layout.prop(self, "materials")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        fake_user_set(self.fake_user, self.materials)
        return {'FINISHED'}


# -----------------------------------------------------------------------------
# menu classes

class VIEW3D_MT_master_material(bpy.types.Menu):
    bl_label = "Material Utils Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'


        layout.operator("view3d.assign_material", text="Add New", icon='ZOOMIN')
        layout.operator("object.material_slot_remove", text="Delete", icon='ZOOMOUT')         

        layout.separator()
        layout.menu("VIEW3D_MT_assign_material", icon='ZOOMIN')
        layout.menu("VIEW3D_MT_select_material", icon='HAND')
        
        layout.separator()
        layout.operator("view3d.clean_material_slots",
                        text="Clean Slots",
                        icon='CANCEL')
        layout.operator("view3d.material_remove",
                        text="Delet until 1 Slots",
                        icon='CANCEL')
        layout.operator("view3d.material_to_texface",
                        text="Material to Texface",
                        icon='MATERIAL_DATA')
        layout.operator("view3d.texface_to_material",
                        text="Texface to Material",
                        icon='MATERIAL_DATA')

        layout.separator()
        layout.operator("view3d.replace_material",
                        text='Replace Material',
                        icon='ARROW_LEFTRIGHT')

        layout.operator("view3d.fake_user_set",
                        text='Set Fake User',
                        icon='UNPINNED')


class VIEW3D_MT_assign_material(bpy.types.Menu):
    """assign exiting material"""
    bl_label = "Assign Material"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        for material_name in bpy.data.materials.keys():
            layout.operator("view3d.assign_material",
                text=material_name,
                icon='MATERIAL_DATA').matname = material_name



class VIEW3D_MT_select_material(bpy.types.Menu):
    """select by material"""
    bl_label = "Select by Material"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        ob = context.object
        layout.label
        if ob.mode == 'OBJECT':
            #show all used materials in entire blend file
            for material_name, material in bpy.data.materials.items():
                if material.users > 0:
                    layout.operator("view3d.select_material_by_name",
                                    text=material_name,
                                    icon='MATERIAL_DATA',
                                    ).matname = material_name

        elif ob.mode == 'EDIT':
            #show only the materials on this object
            mats = ob.material_slots.keys()
            for m in mats:
                layout.operator("view3d.select_material_by_name",
                    text=m,
                    icon='MATERIAL_DATA').matname = m


###  keyconfigs  ###

#        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
#        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS')
#        kmi.properties.name = "VIEW3D_MT_master_material"




##################################################################################################################################
##################################################################################################################################
##############  RGBCMYW Material Creator  ########################################################################################
##############  RGBCMYW Material Creator  ########################################################################################

#bl_info = {
#    "name": "RGBCMYW Material Creator",
#    "description": "Creates RGBCMYW Materials for use as selection masks",
#    "author": "Andy Davies (metalliandy)",
#    "version": (0,1),
#    "blender": (2, 6, 3),
#    "api": 50372,
#    "location": "Tool Shelf",
#    "warning": '', # used for warning icon and text in addons panel
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "3D View"}
    
"""About this script:-
This script enables the fast creation of RGBCMYW Materials for use as selection masks during texturing.

Usage:-
1)Click the Make RGBCMYW Mats button on the Tool Shelf to activate the tool.
2)Assign the materials to your meshes.
2)Done! :)

Related Links:-

http://www.metalliandy.com

Thanks to:-

Version history:-
v0.1 - Initial revision."""


def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.0
    mat.alpha = alpha
    mat.ambient = 1
    return mat
    
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)


class OBJECT_OT_RGBCMYW(bpy.types.Operator):
    """create rgb & cmyk materials"""
    bl_idname = "materials.rgbcmyw"
    bl_label = "Make RGBCMYW Mats"
    
    def execute(self, context):
        # Create materials
        red = makeMaterial('Red', (1,0,0), (1,1,1), 1)
        green = makeMaterial('Green', (0,1,0), (1,1,1), 1)
        blue = makeMaterial('Blue', (0,0,1), (1,1,1), 1)
        cyan = makeMaterial('Cyan', (0,1,1), (1,1,1), 1)
        magenta = makeMaterial('Magenta', (1,0,1), (1,1,1), 1)
        yellow = makeMaterial('Yellow', (1,1,0), (1,1,1), 1)
        white = makeMaterial('White', (1,1,1), (1,1,1), 1)
         
        return{'FINISHED'}

script_classes = [OBJECT_OT_RGBCMYW]



#######################################################################################################################################
#######################################################################################################################################
##############  Random Face Material Assigner  ########################################################################################
##############  Random Face Material Assigner  ########################################################################################


#bl_info = {
#    "name" : "Random Face Material Assigner",
#    "author" : "Tamir Lousky",
#    "version" : (2, 0, 0),
#    "blender" : (2, 66, 0),
#    "category" : "Materials",
#    "location" : "3D View >> Tools",
#    "wiki_url" : "http://bioblog3d.wordpress.com/2013/03/20/random-material-assigner-v2/",
#    "tracker_url": "https://github.com/Tlousky/blender_scripts/blob/master/random_material_assigners/random_material_assigner_per_face_new_features.py",
#    "description": "Assign random materials to mesh faces, vertex groups or loose parts."}




class rand_mat_assigner(bpy.types.PropertyGroup):

    def get_verts_and_groups( self ):
        """ function name: get_verts_and_groups
description: iterates over all vertex groups, and aggregates
the vertex indices if each vgroup.
return value: dict with this info
"""
        ob = bpy.context.object

        groups = {}
        
        for group in ob.vertex_groups:
            groups[str(group.index)] = []

        for v in ob.data.vertices:
            # iterate over this particular vertex's vgroups
            for group in v.groups:
                # And add the vert index to the group dictionary and each group's list of verts
                groups[str(group.group)].append( v.index )

        return groups

    def randomize( self, context ):
        """ function name: randomize
description: This function assigns a random material to each face on the selected
object's mesh, from its list of materials (filtered by the mat_prefix)
"""
        random.seed(self.rand_seed) # Set the randomization seed
    
        all_materials = bpy.context.object.data.materials
        filtered_materials = []

        if self.mat_prefix != "": # IF the user entered a prefix
            for material in all_materials: # Iterate over all the object's materials
                if self.mat_prefix in material.name: # Look for materials with the prefix
                    filtered_materials.append(material) # And filter them in
        else:
            filtered_materials = all_materials # If there's no prefix, use all materials
        
        no_of_materials = len(filtered_materials) # Count all/filtered materials on object

        bpy.ops.object.mode_set(mode = 'EDIT') # Go to edit mode to create bmesh
        ob = bpy.context.object

        bm = bmesh.from_edit_mesh(ob.data) # Create bmesh object from object mesh

        ## Distribute materials based on vertex groups
        if self.assign_method == 'Vertex Group':
            
            vgroups = self.get_verts_and_groups() # Get vgroups
            if vgroups and len( vgroups.keys() ) > 0: # make sure that there are actually vgroups on this mesh
                
                for vgroup in list( vgroups.keys() ):
                    # get random material index
                    rand_mat_index = random.randint(0, no_of_materials - 1)

                    # Go to vertex selection mode
                    bpy.ops.mesh.select_mode(
                        use_extend=False,
                        use_expand=False,
                        type='VERT')

                    bpy.ops.mesh.select_all(action='DESELECT') # Deselect all verts
                    
                    # Select all the vertices in the vertex group
                    for vert in vgroups[vgroup]:
                        bm.verts[vert].select_set(True)

                    # Go to face selection mode
                    bm.select_mode = {'FACE'}
                    bm.select_flush(True)
                    
                    # iterate over all selected faces and assign vgroup material
                    for face in bm.faces:
                        if face.select:
                            face.material_index = rand_mat_index # Assign random material to face
            else:
                print( "No vertex groups on this mesh, cannot distribute materials!" )

        ## Distribute a rand material to each face
        elif self.assign_method == 'Face':
            for face in bm.faces: # Iterate over all of the object's faces
                face.material_index = random.randint(0, no_of_materials - 1) # Assign random material to face

        ## Distribute materials by loose parts
        elif self.assign_method == 'Loose Parts':
            vert_indices = [ vert.index for vert in bm.verts ] # Reference all vertex indices

            for vert in vert_indices:
                bpy.ops.mesh.select_all(action='DESELECT') # Deselect all verts
                
                bm.verts[vert].select = True
                
                # Select all verts linked to this one (on the same island or "loose part")
                bpy.ops.mesh.select_linked( limit=False )
                
                # Go to face selection mode
                bm.select_mode = {'FACE'}
                bm.select_flush(True)

                rand_mat_index = random.randint(0, no_of_materials - 1)
            
                # iterate over all selected (linked) faces and assign material
                for face in bm.faces:
                    if face.select:
                        face.material_index = rand_mat_index # Assign random material to face
                    
                # remove selected vertices from list
                for vert in bm.verts:
                    if vert.select:
                        removed = vert_indices.pop( vert_indices.index(vert.index) )
        
        ob.data.update() # Update the mesh from the bmesh data
        bpy.ops.object.mode_set(mode = 'OBJECT') # Return to object mode

        return None

    rand_seed = bpy.props.IntProperty( # Randomization seed
        name = "rand_seed",
        description = "Randomization seed",
        options = {'ANIMATABLE'},
        update = randomize
    )

    mat_prefix = bpy.props.StringProperty( # Prefix to filter materials by
        name = "mat_prefix",
        description = "Material name filter",
        default = "",
        update = randomize
    )

    items = [
        ('Face', 'Face', ''),
        ('Vertex Group', 'Vertex Group', ''),
        ('Loose Parts', 'Loose Parts', '')
    ]

    assign_method = bpy.props.EnumProperty( # Material distribution method
        name = "Material distribution method",
        items = items,
        default = 'Face'
    )
    


########################################################################################################################
########################################################################################################################
##############  Tube UV Unwrap  ########################################################################################
##############  Tube UV Unwrap  ########################################################################################



#bl_info = {"name": "Tube UV Unwrap",
#           "description": "UV unwrap tube like meshes (all quads, no caps, fixed number of vertices in each ring)",
#           "author": "Jakub Uhlik",
#           "version": (0, 1, 0),
#           "blender": (2, 69, 0),
#           "location": "Edit mode > Mesh > UV Unwrap... > Tube UV Unwrap",
#           "warning": "",
#           "wiki_url": "",
#           "tracker_url": "",
#           "category": "UV", }


# notes:
#   - Works only on tube like meshes, all quads, no caps, fixed number of vertices
#     in each ring. Best example of such mesh is mesh circle extruded several times
#     or beveled curve converted to mesh.
#   - Result is right-angled UV for easy texturing
#   - Single selected vertex on boundary ring is required before running operator.
#     This vertex marks loop, along which tube will be cut.
#   - Distances of vertices in next tube ring are averaged.
#   - UV is scaled to fit area.
#   - Seam will be marked on mesh automatically.

# usage:
#   1 tab to Edit mode
#   2 select single vertex on boundary ring
#   3 hit "U" and select "Tube UV Unwrap"

# changelog:
# 2014.06.13 fixed accidential freeze on messy geometry
#            fixed first loop vertex order (also on messy geometry)
#            uv creation part completely rewritten from scratch
# 2014.06.12 first release


def tube_unwrap(operator, context):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    ob = context.active_object
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    
    vert = bm.select_history.active
    if(not vert):
        operator.report({'ERROR'}, "Select one boundary vertex. Seam will be placed there.")
        return False
    else:
        if(vert.is_boundary is False):
            operator.report({'ERROR'}, "Select one boundary vertex. Seam will be placed there.")
            return False
    
    def get_seam_and_rings(vert):
        if(vert.is_boundary):
            def get_boundary_edge_loop(vert):
                def get_next_boundary_vertices(vert):
                    lf = vert.link_faces
                    fa = lf[0]
                    fb = lf[1]
                    a = None
                    b = None
                    for i, v in enumerate(fa.verts):
                        if(v.is_boundary and v is not vert):
                            a = v
                    for i, v in enumerate(fb.verts):
                        if(v.is_boundary and v is not vert):
                            b = v
                    return a, b
                
                def walk_verts(v, path):
                    path.append(v)
                    a, b = get_next_boundary_vertices(v)
                    if(len(path) == 1):
                        # i need a second vert, decide one direction..
                        path = walk_verts(a, path)
                    if(a in path):
                        if(b not in path):
                            path = walk_verts(b, path)
                        else:
                            return path
                    elif(b in path):
                        if(a not in path):
                            path = walk_verts(a, path)
                        else:
                            return path
                    else:
                        raise RuntimeError("Something very bad happened. Please contact support immediately.")
                    return path
                
                verts = walk_verts(vert, [])
                return verts
            
            boundary_ring = get_boundary_edge_loop(vert)
            
            if(len(bm.verts) % len(boundary_ring) != 0):
                # abort
                operator.report({'ERROR'}, "This is not a simple tube. Number of vertices != number of rings * number of ring vertices.")
                return (None, None)
            num_loops = int(len(bm.verts) / len(boundary_ring))
            
            def is_in_rings(vert, rings):
                for r in rings:
                    for v in r:
                        if(v == vert):
                            return True
                return False
            
            def get_next_ring(rings):
                prev_ring = rings[len(rings) - 1]
                nr = []
                for v in prev_ring:
                    le = v.link_edges
                    for e in le:
                        for v in e.verts:
                            if(v not in prev_ring and is_in_rings(v, rings) is False):
                                nr.append(v)
                return nr
            
            rings = [boundary_ring, ]
            for i in range(num_loops - 1):
                r = get_next_ring(rings)
                rings.append(r)
            
            seam = [vert, ]
            for i in range(num_loops - 1):
                for v in rings[i + 1]:
                    sle = seam[i].link_edges
                    for e in sle:
                        if(v in e.verts):
                            if(e.verts[0] == seam[i]):
                                seam.append(e.verts[1])
                            else:
                                seam.append(e.verts[0])
            return (seam, rings)
    
    seam, rings = get_seam_and_rings(vert)
    if(seam is None or rings is None):
        # abort
        return False
    
    def walk_face_ring(vert, ring, next_vert, next_ring):
        edges = []
        for i, v in enumerate(ring):
            le = v.link_edges
            for e in le:
                if(next_ring[i] in e.verts):
                    break
            edges.append(e)
        faces = []
        for i, e in enumerate(edges):
            lf = e.link_faces
            for f in lf:
                ni = i + 1
                if(ni >= len(edges)):
                    ni = 0
                if(f in edges[ni].link_faces and f not in faces):
                    faces.append(f)
                    # here i have to decide in first iteration in which direction walk through faces
                    # i do not know yet how to do it. so i am taking the first face
                    # in hope the second (last) will be get in next iteration..
                    break
        return faces
    
    def make_face_rings(seam, rings):
        face_rings = []
        for i, v in enumerate(seam):
            if(i < len(seam) - 1):
                next_vert = seam[i + 1]
                fr = walk_face_ring(v, rings[i], next_vert, rings[i + 1])
                face_rings.append(fr)
        return face_rings
    
    face_rings = make_face_rings(seam, rings)
    
    def calc_seam_length(seam):
        l = 0
        for i in range(len(seam) - 1):
            v = seam[i]
            le = v.link_edges
            for e in le:
                if(seam[i + 1] in e.verts):
                    l += e.calc_length()
        return l
    
    seam_length = calc_seam_length(seam)
    
    def calc_circumference(r):
        def get_edge(av, bv):
            for e in bm.edges:
                if(av in e.verts and bv in e.verts):
                    return e
            return None
        
        l = 0
        for i in range(len(r)):
            ei = i + 1
            if(ei >= len(r)):
                ei = 0
            e = get_edge(r[i], r[ei])
            l += e.calc_length()
        return l
    
    def calc_sizes(rings, seam_length, seam):
        ac = 0
        for r in rings:
            ac += calc_circumference(r)
        ac = ac / len(rings)
        
        if(ac > seam_length):
            scale_ratio = 1 / ac
            w = 0
            h = (seam_length / len(seam)) * scale_ratio
        else:
            scale_ratio = 1 / seam_length
            w = (ac / len(rings[0])) * scale_ratio
            h = 0
        return scale_ratio, w, h
    
    scale_ratio, w, h = calc_sizes(rings, seam_length, seam)
    
    def make_uvmap(bm, name):
        uvs = bm.loops.layers.uv
        if(uvs.active is None):
            uvs.new(name)
        uv_lay = uvs.active
        return uv_lay
    
    uv_lay = make_uvmap(bm, "UVMap")
    
    def make_uvs(uv_lay, scale_ratio, w, h, rings, seam, ):
        def get_edge(av, bv):
            for e in bm.edges:
                if(av in e.verts and bv in e.verts):
                    return e
            return None
        
        def get_face(verts):
            a = set(verts[0].link_faces)
            b = a.intersection(verts[1].link_faces, verts[2].link_faces, verts[3].link_faces)
            return list(b)[0]
        
        def get_face_loops(f, vo):
            lo = []
            for i, v in enumerate(vo):
                for j, l in enumerate(f.loops):
                    if(l.vert == v):
                        lo.append(j)
            return lo
        
        x = 0
        y = 0
        for ir, ring in enumerate(rings):
            if(len(rings) > ir + 1):
                if(w == 0):
                    # circumference <= length
                    fw = 1 / len(rings[0])
                    fh = get_edge(seam[ir], seam[ir + 1]).calc_length() * scale_ratio
                else:
                    # circumference > length
                    fw = w
                    fh = get_edge(seam[ir], seam[ir + 1]).calc_length() * scale_ratio
            
            for iv, vert in enumerate(ring):
                if(len(rings) > ir + 1):
                    next_ring = rings[ir + 1]
                    # d - c
                    # |   |
                    # a - b
                    if(len(ring) == iv + 1):
                        poly = (vert, ring[0], next_ring[0], next_ring[iv])
                    else:
                        poly = (vert, ring[iv + 1], next_ring[iv + 1], next_ring[iv])
                    
                    face = get_face(poly)
                    loops = get_face_loops(face, poly)
                    
                    face.loops[loops[0]][uv_lay].uv = Vector((x, y))
                    x += fw
                    face.loops[loops[1]][uv_lay].uv = Vector((x, y))
                    y += fh
                    face.loops[loops[2]][uv_lay].uv = Vector((x, y))
                    x -= fw
                    face.loops[loops[3]][uv_lay].uv = Vector((x, y))
                    
                x += fw
                y -= fh
            x = 0
            y += fh
            fw = 0
            fh = 0
    
    make_uvs(uv_lay, scale_ratio, w, h, rings, seam, )
    
    def mark_seam(seam):
        def get_edge(av, bv):
            for e in bm.edges:
                if(av in e.verts and bv in e.verts):
                    return e
            return None
        
        for i, v in enumerate(seam):
            if(i < len(seam) - 1):
                nv = seam[i + 1]
                e = get_edge(v, nv)
                e.seam = True
    
    mark_seam(seam)
    me.show_edge_seams = True
    
    bm.to_mesh(me)
    bm.free()
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    return True


class TubeUVUnwrapOperator(bpy.types.Operator):
    bl_idname = "uv.tube_uv_unwrap"
    bl_label = "Tube UV Unwrap"
    bl_description = "UV unwrap tube like meshes. Mesh have to be all quads and cannot have caps."
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        r = tube_unwrap(self, context)
        if(r is False):
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}
        return {'FINISHED'}


def menu_func(self, context):
    l = self.layout
    l.separator()
    l.operator(TubeUVUnwrapOperator.bl_idname, text=TubeUVUnwrapOperator.bl_label)



#############------------------------------------------------------------------------------------------######################
#############------------------------------------------------------------------------------------------######################
#############------------------------------------------------------------------------------------------######################
#############------------------------------------------------------------------------------------------######################
#############################################################################################################################
#############################################################################################################################
##############  Window Manager  #############################################################################################
##############  Window Manager  #############################################################################################



class paul_managerProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.paul_manager
    """
    display = bpy.props.BoolProperty(name = 'display')
    display_align = bpy.props.BoolProperty(name = 'display_align')
    display_offset = bpy.props.BoolProperty(name = 'display_offset')
    
    display_unwrap = bpy.props.BoolProperty(name = 'display_unwrap')
    display_rotface= bpy.props.BoolProperty(name = 'display_rotfac')
    display_cad = bpy.props.BoolProperty(name = 'display_cad')
    display_merge = bpy.props.BoolProperty(name = 'display_merge')
    
    display_addextras = bpy.props.BoolProperty(name = 'display_addextras') 
    display_origin = bpy.props.BoolProperty(name = 'display_origin')
    
    display_cleanup = bpy.props.BoolProperty(name = 'display_cleanup')
    display_location = bpy.props.BoolProperty(name = 'display_location')
    display_rotation = bpy.props.BoolProperty(name = 'display_rotation')
    display_scale = bpy.props.BoolProperty(name = 'display_scale')
        
     
    display_shade = bpy.props.BoolProperty(name = 'display_shade')
    display_modi = bpy.props.BoolProperty(name = 'display_modi')
    display_circle = bpy.props.BoolProperty(name = 'display_circle')
    display_grid = bpy.props.BoolProperty(name = 'display_grid')    
    display_bezcurve = bpy.props.BoolProperty(name = 'display_bezcurve')
    
    display_selection = bpy.props.BoolProperty(name = 'display_selection')
    display_extension = bpy.props.BoolProperty(name = 'display_extension')

    display_relationsOB = bpy.props.BoolProperty(name = 'display_relationsOB')
    display_relationsARMA = bpy.props.BoolProperty(name = 'display_relationsARMA')
    display_poseparent = bpy.props.BoolProperty(name = 'display_poseparent')
    display_relationsPose = bpy.props.BoolProperty(name = 'display_relationsPose')

    display_uvnext = bpy.props.BoolProperty(name = 'display_uvnext')
    display_uvsure = bpy.props.BoolProperty(name = 'display_uvsure')    
    display_uvut = bpy.props.BoolProperty(name = 'display_uvut')
    
    
    display_relations = bpy.props.BoolProperty(name = 'display_relations')
    display_hook = bpy.props.BoolProperty(name = 'display_hook')    
    display_parent = bpy.props.BoolProperty(name = 'display_parent')
    display_bonetool = bpy.props.BoolProperty(name = 'display_bonetool')
    
    display_mirrorcut = bpy.props.BoolProperty(name = 'display_mirrorcut')    
    display_freeze = bpy.props.BoolProperty(name = 'display_freeze')
    display_extrude = bpy.props.BoolProperty(name = 'display_extrude')
    display_placer = bpy.props.BoolProperty(name = 'display_placer')
    display_constraint = bpy.props.BoolProperty(name = 'display_constraint')     
    display_tempmodi = bpy.props.BoolProperty(name = 'display_tempmodi')     
    display_group = bpy.props.BoolProperty(name = 'display_group')        
    display_selection = bpy.props.BoolProperty(name = 'display_selection')
    display_editselect = bpy.props.BoolProperty(name = 'display_editselect')
    display_selectcurve = bpy.props.BoolProperty(name = 'display_selectcurve')
    display_selectsurface = bpy.props.BoolProperty(name = 'display_selectsurface')
    display_selectmball = bpy.props.BoolProperty(name = 'display_selectmball')
    display_selectlattice = bpy.props.BoolProperty(name = 'display_selectlattice')
    display_selectarmature = bpy.props.BoolProperty(name = 'display_selectarmature')    
    display_inexport = bpy.props.BoolProperty(name = 'display_inexport') 

    display_normals = bpy.props.BoolProperty(name = 'display_normals') 
    display_originsnap = bpy.props.BoolProperty(name = 'display_originsnap')         
    display_cadtools = bpy.props.BoolProperty(name = 'display_cadtools') 
    display_obarray = bpy.props.BoolProperty(name = 'display_obarray') 

    display_poselib = bpy.props.BoolProperty(name = 'display_poselib') 
    display_material = bpy.props.BoolProperty(name = 'display_material')
    display_wireset = bpy.props.BoolProperty(name = 'display_wireset')
    display_cleanmat = bpy.props.BoolProperty(name = 'display_cleanmat')
    display_matoption = bpy.props.BoolProperty(name = 'display_matoption')
    display_matrandom = bpy.props.BoolProperty(name = 'display_matrandom')                
    
    
    spread_x = bpy.props.BoolProperty(name = 'spread_x', default = False)
    spread_y = bpy.props.BoolProperty(name = 'spread_y', default = False)
    spread_z = bpy.props.BoolProperty(name = 'spread_z', default = True)
    relation = bpy.props.BoolProperty(name = 'relation', default = False)
    edge_idx_store = bpy.props.IntProperty(name="edge_idx_store")   
    object_name_store = bpy.props.StringProperty(name="object_name_store") 
    align_dist_z = bpy.props.BoolProperty(name = 'align_dist_z')
    align_lock_z = bpy.props.BoolProperty(name = 'align_lock_z')
    step_len = bpy.props.FloatProperty(name="step_len")
    vec_store = bpy.props.FloatVectorProperty(name="vec_store")
    instance = bpy.props.BoolProperty(name="instance")
    
    shift_lockX = bpy.props.BoolProperty(name = 'shift_lockX', default = False)
    shift_lockY = bpy.props.BoolProperty(name = 'shift_lockY', default = False)
    shift_lockZ = bpy.props.BoolProperty(name = 'shift_lockZ', default = False)
    shift_copy = bpy.props.BoolProperty(name = 'shift_copy', default = False)
    shift_local = bpy.props.BoolProperty(name = 'shift_local', default = False)


class MessageOperator(bpy.types.Operator):
    from bpy.props import StringProperty
    
    bl_idname = "error.message"
    bl_label = "Message"
    type = StringProperty()
    message = StringProperty()
 
    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=200)
 
    def draw(self, context):
        self.layout.label(self.message, icon='BLENDER')


def print_error(message):
    bpy.ops.error.message('INVOKE_DEFAULT', 
        type = "Message",
        message = message)   




classes = [SSOperator, SpreadOperator, AlignOperator, LayoutSSPanel, MessageOperator, \
    OffsetOperator, paul_managerProps, rand_mat_assigner]


addon_keymaps = []  
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.paul_manager = \
        bpy.props.PointerProperty(type = paul_managerProps) 
    bpy.context.window_manager.paul_manager.display = False
    bpy.context.window_manager.paul_manager.display_align = False
    
    bpy.context.window_manager.paul_manager.display_rotface = False
    bpy.context.window_manager.paul_manager.display_cad = False
    bpy.context.window_manager.paul_manager.display_unwrap = False
    bpy.context.window_manager.paul_manager.display_merge = False
    bpy.context.window_manager.paul_manager.display_addextras = False
    bpy.context.window_manager.paul_manager.display_origin = False
    bpy.context.window_manager.paul_manager.display_cleanup = False    
    bpy.context.window_manager.paul_manager.display_location = False 
    bpy.context.window_manager.paul_manager.display_rotation = False 
    bpy.context.window_manager.paul_manager.display_scale = False 
    
    bpy.context.window_manager.paul_manager.display_shade = False
    bpy.context.window_manager.paul_manager.display_modi = False  
    bpy.context.window_manager.paul_manager.display_circle = False  
    bpy.context.window_manager.paul_manager.display_grid = False 
    bpy.context.window_manager.paul_manager.display_bezcurve = False 
  
    bpy.context.window_manager.paul_manager.display_extension = False 
    bpy.context.window_manager.paul_manager.display_relationsOB = False
    bpy.context.window_manager.paul_manager.display_relationsARMA = False
    bpy.context.window_manager.paul_manager.display_bonetools = False
    bpy.context.window_manager.paul_manager.display_relationsPose = False
    bpy.context.window_manager.paul_manager.display_poseparent = False                 
    
    bpy.context.window_manager.paul_manager.display_relations = False      
    bpy.context.window_manager.paul_manager.display_group = False 
    bpy.context.window_manager.paul_manager.display_hook = False 
    bpy.context.window_manager.paul_manager.display_parent = False 

    bpy.context.window_manager.paul_manager.display_uvnext = False 
    bpy.context.window_manager.paul_manager.display_uvsure = False 
    bpy.context.window_manager.paul_manager.display_uvut = False             
    
    
    bpy.context.window_manager.paul_manager.display_mirrorcut = False 
    bpy.context.window_manager.paul_manager.display_freeze = False 

    bpy.context.window_manager.paul_manager.display_extrude = False 
    bpy.context.window_manager.paul_manager.display_placer = False 
    bpy.context.window_manager.paul_manager.display_constraint = False  
    bpy.context.window_manager.paul_manager.display_tempmodi = False 
    bpy.context.window_manager.paul_manager.display_selection = False     
    
    bpy.context.window_manager.paul_manager.display_editselect = False 
    bpy.context.window_manager.paul_manager.display_selectcurve = False
    bpy.context.window_manager.paul_manager.display_selectsurface = False
    bpy.context.window_manager.paul_manager.display_mball = False
    bpy.context.window_manager.paul_manager.display_armature = False    
    
    bpy.context.window_manager.paul_manager.display_inexport = False        
    bpy.context.window_manager.paul_manager.display_normals = False  

    bpy.context.window_manager.paul_manager.display_originsnap = False     
    bpy.context.window_manager.paul_manager.display_cadtools = False
    bpy.context.window_manager.paul_manager.display_obarray = False 

    bpy.context.window_manager.paul_manager.display_poselib = False 
    bpy.context.window_manager.paul_manager.display_material = False
    bpy.context.window_manager.paul_manager.display_wireset = False  
    bpy.context.window_manager.paul_manager.display_cleanmat = False 
    bpy.context.window_manager.paul_manager.display_matoption = False
    bpy.context.window_manager.paul_manager.display_matrandom = False         
        
    bpy.context.window_manager.paul_manager.spread_x = False
    bpy.context.window_manager.paul_manager.spread_y = False
    bpy.context.window_manager.paul_manager.spread_z = True
    bpy.context.window_manager.paul_manager.edge_idx_store = -1
    bpy.context.window_manager.paul_manager.object_name_store = ''
    bpy.context.window_manager.paul_manager.align_dist_z = False
    bpy.context.window_manager.paul_manager.align_lock_z = False
    bpy.context.window_manager.paul_manager.step_len = 1.0
    bpy.context.window_manager.paul_manager.instance = False
    
    bpy.utils.register_module(__name__)
    bpy.types.Scene.face_assigner = bpy.props.PointerProperty(type=rand_mat_assigner)
    bpy.types.IMAGE_MT_uvs.append(menu_func)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='offset', space_type='VIEW_3D')
    kmi = km.keymap_items.new(OffsetOperator.bl_idname, 'R', 'PRESS', ctrl=False, shift=True)
    addon_keymaps.append((km, kmi))  
    
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear() 
    
    del bpy.types.WindowManager.paul_manager
    for c in reversed(classes):  
        bpy.utils.unregister_class(c)
    
    bpy.utils.unregister_module(__name__)
    bpy.types.Scene.face_assigner = bpy.props.PointerProperty(type=rand_mat_assigner)
    bpy.types.IMAGE_MT_uvs.remove(menu_func)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)   

if __name__ == "__main__":
    register()

