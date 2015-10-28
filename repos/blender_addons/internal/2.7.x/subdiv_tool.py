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
    "name": "Subdiv Modifier Tool",
    "author": "conrad dueck",
    "version": (0,1,0),
    "blender": (2, 73, 0),
    "location": "View3D > Tool Shelf > Addons",
    "description": "ON/OFF/DELETE and subdiv levels control for scene or selection Subdivision Surface modifiers",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy

#define button operators
class BUTTON_OT_sbdvmodon(bpy.types.Operator):
    '''Turn subdivision modifiers ON.'''
    bl_idname = "sbdvmod.on"
    bl_label = "ON"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.sbdvmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'SUBSURF':
                    if bpy.context.scene.sbdvmodview:
                        c.show_viewport = 1
                    if bpy.context.scene.sbdvmodrender:
                        c.show_render = 1
        return{'FINISHED'}

class BUTTON_OT_sbdvmodoff(bpy.types.Operator):
    '''Turn subdivision modifiers OFF.'''
    bl_idname = "sbdvmod.off"
    bl_label = "OFF"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.sbdvmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'SUBSURF':
                    if bpy.context.scene.sbdvmodview:
                        c.show_viewport = 0
                    if bpy.context.scene.sbdvmodrender:
                        c.show_render = 0
        return{'FINISHED'}

class BUTTON_OT_sbdvmodadd(bpy.types.Operator):
    '''Add sub-division level'''
    bl_idname = "sbdvmod.add"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.sbdvmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'SUBSURF':
                    if bpy.context.scene.sbdvmodview:
                        c.levels += 1
                    if bpy.context.scene.sbdvmodrender:
                        c.render_levels += 1
        return{'FINISHED'}

class BUTTON_OT_sbdvmodsubtract(bpy.types.Operator):
    '''Subtract sub-division level'''
    bl_idname = "sbdvmod.subtract"
    bl_label = "Subtract"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.sbdvmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'SUBSURF':
                    if bpy.context.scene.sbdvmodview:
                        c.levels -= 1
                    if bpy.context.scene.sbdvmodrender:
                        c.render_levels -= 1
        return{'FINISHED'}

class BUTTON_OT_sbdvmodset(bpy.types.Operator):
    '''Set sub-division levels'''
    bl_idname = "sbdvmod.set"
    bl_label = "Set"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.sbdvmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'SUBSURF':
                    if bpy.context.scene.sbdvmodview:
                        c.levels = bpy.context.scene.sbdvmodvalue
                    if bpy.context.scene.sbdvmodrender:
                        c.render_levels = bpy.context.scene.sbdvmodvalue
        return{'FINISHED'}

class BUTTON_OT_sbdvmoddelete(bpy.types.Operator):
    '''Delete subdivision surface modifiers'''
    bl_idname = "sbdvmod.delete"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.sbdvmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'SUBSURF':
                    a.modifiers.remove(c)
        return{'FINISHED'}

#define panel
class VIEW3D_OT_sbdvmodtool(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Subdiv Surface Tool"
    bl_context = "objectmode"
    bl_category = 'Addons'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "sbdvmodsel")
        layout.prop(context.scene, "sbdvmodview")
        layout.prop(context.scene, "sbdvmodrender")
        layout.operator("sbdvmod.on", text=(BUTTON_OT_sbdvmodon.bl_label))
        layout.operator("sbdvmod.off", text=(BUTTON_OT_sbdvmodoff.bl_label))
        layout.operator("sbdvmod.add", text=(BUTTON_OT_sbdvmodadd.bl_label))
        layout.operator("sbdvmod.subtract", text=(BUTTON_OT_sbdvmodsubtract.bl_label))
        layout.prop(context.scene, "sbdvmodvalue")
        layout.operator("sbdvmod.set", text=(BUTTON_OT_sbdvmodset.bl_label))
        layout.operator("sbdvmod.delete", text=(BUTTON_OT_sbdvmoddelete.bl_label))
        row = layout.row()

#register
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.sbdvmodsel = bpy.props.BoolProperty \
        (
          name = "Only Selected",
          description = "Only act on selected objects",
          default = False
        )
    bpy.types.Scene.sbdvmodview = bpy.props.BoolProperty \
        (
          name = "Viewport",
          description = "Affect viewport subdivision levels",
          default = True
        )
    bpy.types.Scene.sbdvmodrender = bpy.props.BoolProperty \
        (
          name = "Render",
          description = "Affect render subdivision levels",
          default = True
        )
    bpy.types.Scene.sbdvmodvalue= bpy.props.IntProperty \
        (
          name = "Levels",
          description = "Subdivision levels",
        )

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.sbdvmodsel
    del bpy.types.Scene.sbdvmodview
    del bpy.types.Scene.sbdvmodrender
    del bpy.types.Scene.sbdvmodvalue

if __name__ == "__main__":
    register()
