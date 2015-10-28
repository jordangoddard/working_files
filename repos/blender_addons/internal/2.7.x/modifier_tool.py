#
#    Copyright (c) 2015 Conrad Dueck
#
#    All rights reserved.
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are met:
#
#    1.  Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#    2.  Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# made in response to --
# Andy Carney request for an easy toggle for all scene wireframe modifiers
#



bl_info = {
    "name": "Modifier Tool",
    "author": "conrad dueck",
    "version": (0,1,0),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Shelf > Addons",
    "description": "Affect multiple scene or selected modifiers en masse.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy import context

#define button operators
class BUTTON_OT_modtooldelete(bpy.types.Operator):
    '''Delete all these modifiers.'''
    bl_idname = "modtool.delete"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for theobj in theobjs:
            themods = theobj.modifiers
            for themod in themods:
                if themod.type == thetype:
                    theobj.modifiers.remove(themod)
        return{'FINISHED'}

class BUTTON_OT_modtoolonview(bpy.types.Operator):
    '''Turn ON these modifiers in viewport.'''
    bl_idname = "modtool.onview"
    bl_label = "On"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for theobj in theobjs:
            themods = theobj.modifiers
            for themod in themods:
                if themod.type == thetype:
                    themod.show_viewport = 1
        return{'FINISHED'}

class BUTTON_OT_modtooloffview(bpy.types.Operator):
    '''Turn OFF these modifiers in viewport.'''
    bl_idname = "modtool.offview"
    bl_label = "Off"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for theobj in theobjs:
            themods = theobj.modifiers
            for themod in themods:
                if themod.type == thetype:
                    themod.show_viewport = 0
        return{'FINISHED'}

class BUTTON_OT_modtoolonrender(bpy.types.Operator):
    '''Turn ON these modifiers in render.'''
    bl_idname = "modtool.onrender"
    bl_label = "On"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for theobj in theobjs:
            themods = theobj.modifiers
            for themod in themods:
                if themod.type == thetype:
                    themod.show_render = 1
        return{'FINISHED'}

class BUTTON_OT_modtooloffrender(bpy.types.Operator):
    '''Turn OFF these modifiers in render.'''
    bl_idname = "modtool.offrender"
    bl_label = "Off"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for theobj in theobjs:
            themods = theobj.modifiers
            for themod in themods:
                if themod.type == thetype:
                    themod.show_render = 0
        
        return{'FINISHED'}

class BUTTON_OT_modtoolapply(bpy.types.Operator):
    '''Apply these modifiers.'''
    bl_idname = "modtool.apply"
    bl_label = "Apply"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        bpy.ops.object.select_all(action='DESELECT')
        for theobj in theobjs:
            themods = theobj.modifiers
            for themod in themods:
                if themod.type == thetype:
                    bpy.context.scene.objects.active = theobj
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=themod.name)
        #bpy.ops.object.select_pattern(pattern=(a.name))
        
        return{'FINISHED'}

class BUTTON_OT_modtoolselect(bpy.types.Operator):
    '''Select just objects with these modifiers.'''
    bl_idname = "modtool.select"
    bl_label = "Select"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thetype = bpy.context.scene.modtoolsel
        if bpy.context.scene.modtoolmode:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        bpy.ops.object.select_all(action='DESELECT')
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == thetype:
                    bpy.ops.object.select_pattern(pattern=(a.name))
        
        return{'FINISHED'}


#define panel
class VIEW3D_OT_modtoolmodtool(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Modifier Tool"
    bl_context = "objectmode"
    bl_category = 'Addons'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.scene, "modtoolmode")
        
        layout.separator()
        
        layout.prop(context.scene, "modtoolsel")
        
        layout.separator()
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.label("View")
        row.operator("modtool.onview", text=(BUTTON_OT_modtoolonview.bl_label))
        row.operator("modtool.offview", text=(BUTTON_OT_modtooloffview.bl_label))
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.label("Render")
        row.operator("modtool.onrender", text=(BUTTON_OT_modtoolonrender.bl_label))
        row.operator("modtool.offrender", text=(BUTTON_OT_modtooloffrender.bl_label))
        
        layout.separator()
        
        layout.operator("modtool.apply", text=(BUTTON_OT_modtoolapply.bl_label))
        layout.operator("modtool.select", text=(BUTTON_OT_modtoolselect.bl_label))
        layout.operator("modtool.delete", text=(BUTTON_OT_modtooldelete.bl_label))
        

#register

#def modtoolupdate(self, context):
    

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.modtoolsel = bpy.props.EnumProperty \
        (
          name = "",
          description = "Pick a modifier type",
          items = [("ARRAY","Array",""),("BEVEL","Bevel",""),("BOOLEAN","Boolean",""),("CLOTH","Cloth",""),("MIRROR","Mirror",""),("MULTIRES","MultiResolution",""),("SKIN","Skin",""),("SOLIDIFY","Solidify",""),("SUBSURF","Subdivision Surface",""),("WIREFRAME","WireFrame","")]
          #update = modtoolupdate
        )
    bpy.types.Scene.modtoolmode = bpy.props.BoolProperty \
        (
          name = "Only Selected",
          description = "Only act on selected objects",
          default = False
        )

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.modtoolsel
    del bpy.types.Scene.modtoolmode

if __name__ == "__main__":
    register()
