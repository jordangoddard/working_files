#
#    Copyright (c) 2014 Shane Ambler
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
# from http://blender.stackexchange.com/q/13757/935
#

# modified by Conrad Dueck as follows:
# - updated default and maximum object count values
# - isolated faces before and after mods
# - removed full list for only totals
#


bl_info = {
    "name": "Mesh Summary",
    "author": "sambler",
    "version": (1,2),
    "blender": (2, 74, 0),
    "location": "Properties > Scene > Object Info Panel",
    "description": "Summarize details about the mesh objects in this file.",
    "warning": "",
    "wiki_url": "https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py",
    "tracker_url": "https://github.com/sambler/addonsByMe/issues",
    "category": "System",
}

import bpy
import bmesh
from bpy.props import IntProperty, BoolProperty
from operator import itemgetter

class MeshSummaryPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    display_limit = IntProperty(name="Display limit",
                        description="Maximum number of meshes to check",
                        default=100, min=2, max=1000000)
    calculate_modifier_faces = BoolProperty(name="Calculate mod. faces",
                        description="Calculate face count after applying modifiers.",
                        default=False)
    scene_or_visible = BoolProperty(name="Only visible",
                        description="Restrict to only visible objects.",
                        default=True)
    selected_only = BoolProperty(name="Only Selected",
                        description="Restrict to only selected objects.",
                        default=True)
    listmeshes = BoolProperty(name="List meshes",
                        description="List meshes and details.",
                        default=True)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row()
        row.prop(self,"calculate_modifier_faces")
        row = col.row()
        row.prop(self,"scene_or_visible")
        row = col.row()
        row.prop(self,"selected_only")
        row = col.row()
        row.prop(self,"listmeshes")
        row = col.row()
        row.prop(self, "display_limit")
        col = row.column() # this stops the button stretching

def us(qty):
    return str(qty)

class Properties_meshinfo(bpy.types.Panel):
    bl_label = "Mesh Information"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        prefs = bpy.context.user_preferences.addons[__name__].preferences
        layout = self.layout

        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        if prefs.scene_or_visible and not prefs.selected_only:
            meshes = [o for o in bpy.context.visible_objects if o.type == 'MESH']
        elif prefs.selected_only and not prefs.scene_or_visible:
            meshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']
        elif prefs.selected_only and prefs.scene_or_visible:
            meshes = [o for o in bpy.context.visible_objects if o.select and o.type == 'MESH']
        row = layout.row()
        if len(meshes) == 1:
            row.label(text="1 mesh object.", icon='OBJECT_DATA')
        else:
            if prefs.scene_or_visible and not prefs.selected_only:
                row.label(text=us(len(meshes))+" visible mesh objects.", icon='OBJECT_DATA')
                row = layout.row()
                if len(meshes) > prefs.display_limit:
                    row.label(text="%d visible mesh objects." % prefs.display_limit)
                else:
                    row.label(text="%d visible mesh objects." % len(meshes))
            elif prefs.scene_or_visible and prefs.selected_only:
                row.label(text=us(len(meshes))+" visible and selected mesh objects.", icon='OBJECT_DATA')
                row = layout.row()
                if len(meshes) > prefs.display_limit:
                    row.label(text="%d visible and selected mesh objects." % prefs.display_limit)
                else:
                    row.label(text="%d visible and selected mesh objects." % len(meshes))
            elif prefs.selected_only and not prefs.scene_or_visible:
                row.label(text=us(len(meshes))+" selected mesh objects.", icon='OBJECT_DATA')
                row = layout.row()
                if len(meshes) > prefs.display_limit:
                    row.label(text="%d selected mesh objects." % prefs.display_limit)
                else:
                    row.label(text="%d selected mesh objects." % len(meshes))
            elif not prefs.scene_or_visible and not prefs.selected_only:
                row.label(text=us(len(meshes))+" mesh objects.", icon='OBJECT_DATA')
                row = layout.row()
                if len(meshes) > prefs.display_limit:
                    row.label(text="%d mesh objects." % prefs.display_limit)
                else:
                    row.label(text="%d mesh objects." % len(meshes))

        row = layout.row()
        row.prop(prefs,"calculate_modifier_faces")
        row = layout.row()
        row.prop(prefs,"scene_or_visible")
        row.prop(prefs,"selected_only")
        row = layout.row()
        row.prop(prefs,"listmeshes")
        if len(meshes) > 0:
            dataCols = []
            row = layout.row()
            dataCols.append(row.column()) # name
            dataCols.append(row.column()) # faces
            dataCols.append(row.column()) # faces after modifiers

            topMeshes = [(o, o.name, len(o.data.polygons)) for o in meshes]
            topMeshes = sorted(topMeshes, key=itemgetter(2), reverse=True)[:prefs.display_limit]

            headRow = dataCols[0].row()
            headRow.label(text="Name")
            headRow = dataCols[1].row()
            headRow.label(text="Faces")
            headRow = dataCols[2].row()
            headRow.label(text="Mod. Faces")

            finalvTotal = 0
            for mo in topMeshes:
                if prefs.listmeshes:
                    detailRow = dataCols[0].row()
                if prefs.listmeshes:
                    detailRow.label(text=mo[1])
                if prefs.calculate_modifier_faces:
                    if prefs.listmeshes:
                        detailRow = dataCols[2].row()
                    bm = bmesh.new()
                    bm.from_object(mo[0], context.scene)
                    finalvTotal += (len(bm.faces))
                    if prefs.listmeshes:
                        detailRow.label(text=str(len(bm.faces)))
                    bm.free()
                if prefs.listmeshes:
                    detailRow = dataCols[1].row()
                if prefs.listmeshes:
                    detailRow.label(text=us(mo[2]))

            vTotal = sum([len(o.data.vertices) for o in meshes])
            fTotal = sum([len(o.data.polygons) for o in meshes])

            totRow = dataCols[0].row()
            totRow.label(text="Totals:")
            totRow = dataCols[2].row()
            totRow.label(text=str(finalvTotal))
            totRow = dataCols[1].row()
            totRow.label(text=us(fTotal))

def register():
    bpy.utils.register_class(MeshSummaryPreferences)
    bpy.utils.register_class(Properties_meshinfo)

def unregister():
    bpy.utils.unregister_class(MeshSummaryPreferences)
    bpy.utils.unregister_class(Properties_meshinfo)

if __name__ == "__main__":
    register()
