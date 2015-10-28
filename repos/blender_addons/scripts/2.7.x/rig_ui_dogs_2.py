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

bl_info = {
    "name": "Tangent Dog Rig",
    "author": "David Hearn",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Cutsom rig UI layers",
    "warning": "beta",
    "category": "Rigging"}

import bpy

class RigLayerPanel(bpy.types.Panel):
    """Creates a custom Rig UI layers panel"""
    bl_label = "Rig UI"
    bl_idname = "Rig_dog_layer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Rigs'

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
     

        #dog: search for tail 
        #human: search for breast     
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        rig_id = self.classify_rig()
        
        if rig_id == 'dog':
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Body')
            
            row = col.row()
            row.separator()
           
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Torso')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Head Neck')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=3, toggle=True, text='Front Left Leg')
            row.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Front Right Leg')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='Back Left Leg')
            row.prop(context.active_object.data, 'layers', index=6, toggle=True, text='Back Right Leg')

            row = col.row()
            row.prop(context.active_object.data, 'layers', index=7, toggle=True, text='Tail')
            
            row = col.row()
            row.separator()
            
            row = col.row()
            row.separator()
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Face')
            
            row = col.row()
            row.separator()
           
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Upper Face Primary')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=18, toggle=True, text='Upper Face Secondary')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=19, toggle=True, text='Lower Face Primary')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=20, toggle=True, text='Lower Face Secondary')

            row = col.row()
            row.prop(context.active_object.data, 'layers', index=21, toggle=True, text='Toungue and Teeth')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Left Ear')
            
            row = col.row()
            row.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Right Ear')

            
    def classify_rig(self):
        rig = None
        obj = bpy.context.object.proxy
        for bones in obj.pose.bones:
            if bones.name.startswith('ctl.tail'):
                print(bones.name)
                rig = "dog"
                break
        return rig
 
 
 
"""
class ClassifyRig(bpy.types.Operator):
    bl_idname = "object.classify_rig"
    bl_label = "Classify"
    bl_options = {"UNDO"}
    
    def execute(self, context, event):
        AddTempProp()
        return {"FINISHED"}
 

class PropSliders(bpy.types.Panel):
    bl_label = "Rig Properties"
    bl_idname = "Rig_Props"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Rigs'

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE' 
        
    def draw(self, context):
        layout = self.layout

        obj = context.object
        for bone in obj.pose.bones: 
            for prop in bone.keys():
                row = layout.row()
                row.prop(bone, '["{}"]'.format(prop), slider = True)
""" 
                
def register():
    bpy.utils.register_class(RigLayerPanel)
    #bpy.utils.register_class(PropSliders)

def unregister():
    bpy.utils.unregister_class(RigLayerPanel)
    #bpy.utils.unregister_class(PropSliders)

if __name__ == "__main__":
    register()
                    