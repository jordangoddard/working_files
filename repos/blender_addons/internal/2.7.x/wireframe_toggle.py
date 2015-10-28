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
    "name": "WireFrame Modifier Tool",
    "author": "conrad dueck",
    "version": (0,1,1),
    "blender": (2, 73, 0),
    "location": "View3D > Tool Shelf > Addons",
    "description": "Turn OFF or ON all wireframe modifiers in the scene.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy

#define button operators
class BUTTON_OT_wfmodon(bpy.types.Operator):
    '''Turn all scene wireframe modifiers ON.'''
    bl_idname = "wfmod.on"
    bl_label = "ON"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.wfmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'WIREFRAME':
                    c.show_render = 1
                    c.show_viewport = 1
        return{'FINISHED'}

class BUTTON_OT_wfmodoff(bpy.types.Operator):
    '''Turn all scene wireframe modifiers OFF.'''
    bl_idname = "wfmod.off"
    bl_label = "OFF"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.wfmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'WIREFRAME':
                    c.show_render = 0
                    c.show_viewport = 0
        return{'FINISHED'}

class BUTTON_OT_wfmodreplace(bpy.types.Operator):
    '''Toggle Replace Original checkbox.'''
    bl_idname = "wfmod.replace"
    bl_label = "Replace Toggle"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.wfmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'WIREFRAME':
                    if c.use_replace == 0:
                        c.use_replace = 1
                    else:
                        c.use_replace = 0
        return{'FINISHED'}

class BUTTON_OT_wfmoddelete(bpy.types.Operator):
    '''Delete wireframe modifiers'''
    bl_idname = "wfmod.delete"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.scene.wfmodsel:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
        for a in theobjs:
            b = a.modifiers
            for c in b:
                if c.type == 'WIREFRAME':
                    a.modifiers.remove(c)
        return{'FINISHED'}

#define panel
class VIEW3D_OT_wfmodtool(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Wireframe Tool"
    bl_context = "objectmode"
    bl_category = 'Addons'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "wfmodsel")
        layout.operator("wfmod.on", text=(BUTTON_OT_wfmodon.bl_label))
        layout.operator("wfmod.off", text=(BUTTON_OT_wfmodoff.bl_label))
        layout.operator("wfmod.replace", text=(BUTTON_OT_wfmodreplace.bl_label))
        layout.operator("wfmod.delete", text=(BUTTON_OT_wfmoddelete.bl_label))
        row = layout.row()

#register
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.wfmodsel = bpy.props.BoolProperty \
        (
          name = "Only Selected",
          description = "Only act on selected objects",
          default = False
        )

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.wfmodsel

if __name__ == "__main__":
    register()
