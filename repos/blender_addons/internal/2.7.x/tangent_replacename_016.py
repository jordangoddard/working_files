#
#    Copyright (c) 2015 Tangent Animation
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
# Artist request for a select-by-name tool and text search/replace functionality on object names
# Also ty[es functionality to search/replace text on vertex groups, groups, armatures/bones, shape keys, etc...

bl_info = {
    "name": "Replace Names",
    "author": "conrad dueck",
    "version": (0,1,11),
    "blender": (2, 74, 0),
    "location": "View3D > Tool Shelf > Addons",
    "description": "Replace one string with another in scene or selected objects, materials, uvs.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tangent"}

import bpy
from bpy import context

#define button operators
class BUTTON_OT_replacenamereplace(bpy.types.Operator):
    '''Replace Source string with Target string'''
    bl_idname = "replacename.replace"
    bl_label = "Replace"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #set testing object and group arrays based on Only Selected user option
        if bpy.context.scene.replacenameselected:
            theobjs = bpy.context.selected_objects
            thegroups = []
            for thisgroup in bpy.data.groups:
                allin = 0
                for theobj in bpy.context.selected_objects:
                    if theobj.name in thisgroup.objects:
                        allin += 1
                if len(bpy.context.selected_objects) == allin:
                    thegroups.append(thisgroup)
        else:
            theobjs = bpy.context.scene.objects
            thegroups = bpy.data.groups
        
        #groups
        if bpy.context.scene.replacenamegroups:
            for thegroup in thegroups:
                if bpy.context.scene.replacenameuseobject:
                    if (len(bpy.context.scene.replacenamenew)>=1):
                        thenewstring = (bpy.context.scene.replacenamenew+"."+thegroup.name)
                    else:
                        thenewstring = (thegroup.name)
                else:
                    thenewstring = bpy.context.scene.replacenamenew
                if bpy.context.scene.replacenameprefix:
                    if thenewstring[:3].casefold() == "grp":
                        thenewstring = thenewstring.replace("grp", "grp")
                    else:
                        thenewstring = ("grp."+thenewstring)
                if bpy.context.scene.replacenameprefix:
                    thenewstring = ("grp."+thenewstring)
                if bpy.context.scene.replacenamecase:
                    thenamestr = thegroup.name
                    theteststr = bpy.context.scene.replacenameold
                else:
                    thenamestr = thegroup.name.casefold()
                    theteststr = bpy.context.scene.replacenameold.casefold()
                if (len(theteststr) <= 0):
                    thegroup.name = thenewstring
                if (len(theteststr) >= 1) and (theteststr in thenamestr):
                    thegroup.name = thenamestr.replace(theteststr, thenewstring)
                if bpy.context.scene.replacenamelowsuffix:
                        thegroup.name = thegroup.name + "_LOW"
        
        for theobj in theobjs:
            #reset thenewstring
            thenewstring = ""
            
            #if use object name is on, thenewstring = 'Replace with' string + the object name
            #otherwise, thenewstring = 'Replace with' string
            #'Replace with' accepts a blank string to remove the search string
            if bpy.context.scene.replacenameuseobject:
                if (len(bpy.context.scene.replacenamenew)>=1):
                    thenewstring = (bpy.context.scene.replacenamenew+"_"+theobj.name)
                else:
                    thenewstring = (theobj.name)
            else:
                thenewstring = bpy.context.scene.replacenamenew
                
            #objects
            if ((theobj.type == "MESH") or (theobj.type == "EMPTY")) and bpy.context.scene.replacenameobjects:
                if bpy.context.scene.replacenameprefix:
                    if thenewstring[:3].casefold() == "geo":
                        thenewstring = thenewstring.replace("geo", "geo")
                    else:
                        thenewstring = ("geo."+thenewstring)
                if bpy.context.scene.replacenamecase:
                    thenamestr = theobj.name
                    theteststr = bpy.context.scene.replacenameold
                else:
                    thenamestr = theobj.name.casefold()
                    theteststr = bpy.context.scene.replacenameold.casefold()
                if (len(theteststr) <= 0):
                    theobj.name = thenewstring
                if (len(theteststr) >= 1) and (theteststr in thenamestr):
                    theobj.name = thenamestr.replace(theteststr, thenewstring)
            
            #armatures
            if (theobj.type == "ARMATURE") and bpy.context.scene.replacenamebones:
                if bpy.context.scene.replacenameprefix:
                    if thenewstring[:3].casefold() == "rig":
                        thenewstring = thenewstring.replace("rig", "rig")
                    else:
                        thenewstring = ("rig."+thenewstring)
                if bpy.context.scene.replacenamecase:
                    thenamestr = theobj.name
                    thearmstr = theobj.data.name
                    theteststr = bpy.context.scene.replacenameold
                else:
                    thenamestr = theobj.name.casefold()
                    thearmstr = theobj.data.name.casefold()
                    theteststr = bpy.context.scene.replacenameold.casefold()
                if (len(theteststr) <= 0):
                    theobj.name = thenewstring
                if (len(theteststr) >= 1) and (theteststr in thenamestr):
                    theobj.name = thenamestr.replace(theteststr, thenewstring)
                if (len(theteststr) >= 1) and (theteststr in thearmstr):
                    theobj.data.name = thearmstr.replace(theteststr, thenewstring)
                   
                if (len(theobj.data.bones) >= 1):
                    for thebone in theobj.data.bones:
                        if bpy.context.scene.replacenamecase:
                            thenamestr = thebone.name
                            theteststr = bpy.context.scene.replacenameold
                        else:
                            thenamestr = thebone.name.casefold()
                            theteststr = bpy.context.scene.replacenameold.casefold()
                        if (len(theteststr) <= 0):
                            thebone.name = thenewstring
                        if (len(theteststr) >= 1) and (theteststr in thenamestr):
                            thebone.name = thenamestr.replace(theteststr, thenewstring)
                        if bpy.context.scene.replacenamelowsuffix:
                            thebone.name = thebone.name + "_LOW"
                            
            #empties and lattices
            if ((theobj.type == "LATTICE") or (theobj.type == "EMPTY")) and bpy.context.scene.replacenameemptylattice:
                if bpy.context.scene.replacenameprefix:
                    if thenewstring[:3].casefold() == "geo":
                        thenewstring = thenewstring.replace("geo", "geo")
                    else:
                        thenewstring = ("geo."+thenewstring)
                if bpy.context.scene.replacenamecase:
                    thenamestr = theobj.name
                    theteststr = bpy.context.scene.replacenameold
                else:
                    thenamestr = theobj.name.casefold()
                    theteststr = bpy.context.scene.replacenameold.casefold()
                if (len(theteststr) <= 0):
                    theobj.name = thenewstring
                if (len(theteststr) >= 1) and (theteststr in thenamestr):
                    theobj.name = thenamestr.replace(theteststr, thenewstring)
        
            #lights
            if (theobj.type == "LAMP") and bpy.context.scene.replacenamelights:
                if bpy.context.scene.replacenameprefix:
                    thenewstring = ("lit."+thenewstring)
                if bpy.context.scene.replacenamecase:
                    thenamestr = theobj.name
                    theteststr = bpy.context.scene.replacenameold
                else:
                    thenamestr = theobj.name.casefold()
                    theteststr = bpy.context.scene.replacenameold.casefold()
                if (len(theteststr) <= 0):
                    theobj.name = thenewstring
                if (len(theteststr) >= 1) and (theteststr in thenamestr):
                    theobj.name = thenamestr.replace(theteststr, thenewstring)
            
            #cameras
            if (theobj.type == "CAMERA") and bpy.context.scene.replacenamecameras:
                if bpy.context.scene.replacenameprefix:
                    thenewstring = ("cam."+thenewstring)
                if bpy.context.scene.replacenamecase:
                    thenamestr = theobj.name
                    theteststr = bpy.context.scene.replacenameold
                else:
                    thenamestr = theobj.name.casefold()
                    theteststr = bpy.context.scene.replacenameold.casefold()
                if (len(theteststr) <= 0):
                    theobj.name = thenewstring
                if (len(theteststr) >= 1) and (theteststr in thenamestr):
                    theobj.name = thenamestr.replace(theteststr, thenewstring)
            
            #materials
            if (theobj.type != 'ARMATURE') and bpy.context.scene.replacenamematerials and (len(theobj.material_slots) >=1 ):
                if bpy.context.scene.replacenameprefix:
                    thenewstring = ("mtl."+thenewstring)
                thesemats = theobj.material_slots
                themats = []
                for themat in thesemats:
                    themats.append(themat.material)
                for thismat in themats:
                    if (thismat) and (thismat.type != 'NoneType'):
                        if bpy.context.scene.replacenamecase:
                            thenamestr = thismat.name
                            theteststr = bpy.context.scene.replacenameold
                        else:
                            thenamestr = thismat.name.casefold()
                            theteststr = bpy.context.scene.replacenameold.casefold()
                        if (len(theteststr) <= 0):
                            thismat.name = thenewstring
                        if (len(theteststr) >= 1) and (theteststr in thenamestr):
                            thismat.name = thenamestr.replace(theteststr, thenewstring)
                        if bpy.context.scene.replacenamelowsuffix:
                            thismat.name = thismat.name + "_LOW"
        
            #uv maps
            if (theobj.type == 'MESH') and bpy.context.scene.replacenameuvs and (len(theobj.data.uv_layers) >= 1):
                if bpy.context.scene.replacenameprefix:
                    thenewstring = ("uvs."+thenewstring)
                for thisuvs in theobj.data.uv_layers:
                    if bpy.context.scene.replacenamecase:
                        thenamestr = thisuvs.name
                        theteststr = bpy.context.scene.replacenameold
                    else:
                        thenamestr = thisuvs.name.casefold()
                        theteststr = bpy.context.scene.replacenameold.casefold()
                    if (len(theteststr) <= 0):
                        thisuvs.name = thenewstring
                    if (len(theteststr) >= 1) and (theteststr in thenamestr):
                        thisuvs.name = thenamestr.replace(theteststr, thenewstring)
        
            #vertex groups
            if (theobj.type == 'MESH') and bpy.context.scene.replacenamevertexgroups and (len(theobj.vertex_groups) >= 1):
                if bpy.context.scene.replacenameprefix:
                    thenewstring = ("vtx."+thenewstring)
                for thisvertexgroups in theobj.vertex_groups:
                    if bpy.context.scene.replacenamecase:
                        thenamestr = thisvertexgroups.name
                        theteststr = bpy.context.scene.replacenameold
                    else:
                        thenamestr = thisvertexgroups.name.casefold()
                        theteststr = bpy.context.scene.replacenameold.casefold()
                    if (len(theteststr) <= 0):
                        thisvertexgroups.name = thenewstring
                    if (len(theteststr) >= 1) and (theteststr in thenamestr):
                        thisvertexgroups.name = thenamestr.replace(theteststr, thenewstring)
        
            #shape keys
            try:
                if (theobj.type == 'MESH') and bpy.context.scene.replacenameshapekeys and (len(theobj.data.shape_keys.key_blocks) >= 1):
                    if bpy.context.scene.replacenameprefix:
                        thenewstring = ("shp."+thenewstring)
                    for thiskey in theobj.data.shape_keys.key_blocks:
                        if bpy.context.scene.replacenamecase:
                            thenamestr = thiskey.name
                            theteststr = bpy.context.scene.replacenameold
                        else:
                            thenamestr = thiskey.name.casefold()
                            theteststr = bpy.context.scene.replacenameold.casefold()
                        if (len(theteststr) <= 0):
                            thiskey.name = thenewstring
                        if (len(theteststr) >= 1) and (theteststr in thenamestr):
                            thiskey.name = thenamestr.replace(theteststr, thenewstring)
            except:
                print('failed shape keys')
            #add '_LOW' suffix
            if bpy.context.scene.replacenamelowsuffix:
                theobj.name = theobj.name + "_LOW"
            
        
        return{'FINISHED'}
    
class BUTTON_OT_replacenameselect(bpy.types.Operator):
    '''Replace Source string with Target string'''
    bl_idname = "replacename.select"
    bl_label = "Select"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thenewsel = []
        themats = []
        if bpy.context.scene.replacenameselected:
            theobjs = bpy.context.selected_objects
        else:
            theobjs = bpy.context.scene.objects
            themats = bpy.data.materials
        if bpy.context.scene.replacenamecase:
            theteststr = bpy.context.scene.replacenameold
        else:
            theteststr = bpy.context.scene.replacenameold.casefold()
        
        for theobj in theobjs:
            if bpy.context.scene.replacenamecase:
                thenamestr = theobj.name
            else:
                thenamestr = theobj.name.casefold()
            #objects
            if bpy.context.scene.replacenameobjects:
                if (theteststr in thenamestr) and (theobj.type == "MESH"):
                    thenewsel.append(theobj.name)
            #bones
            if bpy.context.scene.replacenamebones:
                if (theteststr in thenamestr) and (theobj.type == "ARMATURE"):
                    thenewsel.append(theobj.name)
            #empty lattice
            if bpy.context.scene.replacenameemptylattice:
                if (theteststr in thenamestr) and ((theobj.type == "EMPTY") or (theobj.type == "LATTICE")):
                    thenewsel.append(theobj.name)
            #lights
            if bpy.context.scene.replacenamelights:
                if (theteststr in thenamestr) and (theobj.type == "LAMP"):
                    thenewsel.append(theobj.name)
            #cameras
            if bpy.context.scene.replacenamecameras:
                if (theteststr in thenamestr) and (theobj.type == "CAMERA"):
                    thenewsel.append(theobj.name)
            #materials
            if bpy.context.scene.replacenamematerials:
                for theslot in theobj.material_slots:
                    themat = theslot.material
                    if bpy.context.scene.replacenamecase:
                        thematstr = themat.name
                    else:
                        thematstr = themat.name.casefold()
                    if theteststr in thematstr:
                        if theobj.name not in thenewsel:
                            thenewsel.append(theobj.name)
            #uv maps
            if bpy.context.scene.replacenameuvs:
                for theobj in theobjs:
                    if (theobj.type == 'MESH') and (len(theobj.data.uv_layers) >= 1):
                        for thisuvs in theobj.data.uv_layers:
                            if bpy.context.scene.replacenamecase:
                                thenamestr = thisuvs.name
                                theteststr = bpy.context.scene.replacenameold
                            else:
                                thenamestr = thisuvs.name.casefold()
                                theteststr = bpy.context.scene.replacenameold.casefold()
                            if theteststr in thenamestr:
                                thenewsel.append(theobj.name)
            #vertex groups
            if bpy.context.scene.replacenamevertexgroups:
                for theobj in theobjs:
                    if (theobj.type == 'MESH') and (len(theobj.vertex_groups) >= 1):
                        for thisvertexgroups in theobj.vertex_groups:
                            if bpy.context.scene.replacenamecase:
                                thenamestr = thisvertexgroups.name
                                theteststr = bpy.context.scene.replacenameold
                            else:
                                thenamestr = thisvertexgroups.name.casefold()
                                theteststr = bpy.context.scene.replacenameold.casefold()
                            if theteststr in thenamestr:
                                thenewsel.append(theobj.name)
            #shape keys
            if bpy.context.scene.replacenameshapekeys:
                for theobj in theobjs:
                    if (theobj.type == 'MESH') and (len(theobj.data.shape_keys.key_blocks) >= 1):
                        for thiskey in theobj.data.shape_keys.key_blocks:
                            if bpy.context.scene.replacenamecase:
                                thenamestr = thiskey.name
                                theteststr = bpy.context.scene.replacenameold
                            else:
                                thenamestr = thiskey.name.casefold()
                                theteststr = bpy.context.scene.replacenameold.casefold()
                            if theteststr in thenamestr:
                                thenewsel.append(theobj.name)
        bpy.ops.object.select_all(action='DESELECT')
        for a in thenewsel:
            bpy.ops.object.select_pattern(pattern=a)
        return{'FINISHED'}

#define panel
class VIEW3D_OT_replacenamereplacename(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Replace Names"
    bl_context = "objectmode"
    bl_category = 'Addons'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        split = layout.split(percentage=0.5, align=True)
        col = split.column(align=True)
        col.prop(context.scene, "replacenameobjects")
        col.prop(context.scene, "replacenamelights")
        col.prop(context.scene, "replacenamecameras")
        col.prop(context.scene, "replacenamegroups")
        col.prop(context.scene, "replacenamebones")
        col.prop(context.scene, "replacenameemptylattice")
        col = split.column(align=True)
        col.prop(context.scene, "replacenamematerials")
        col.prop(context.scene, "replacenameuvs")
        col.prop(context.scene, "replacenamevertexgroups")
        col.prop(context.scene, "replacenameshapekeys")
        layout.separator()
        split = layout.split(percentage=0.5, align=True)
        col = split.column(align=True)
        col.label("Search for:")
        col = split.column(align=True)
        col.prop(context.scene, "replacenamecase")
        layout.prop(context.scene, "replacenameold")
        layout.label("Replace with:")
        layout.prop(context.scene, "replacenamenew")
        layout.prop(context.scene, "replacenameuseobject")
        layout.prop(context.scene, "replacenameprefix")
        layout.prop(context.scene, "replacenamelowsuffix")
        layout.separator()
        layout.prop(context.scene, "replacenameselected")
        layout.operator("replacename.replace", text=(BUTTON_OT_replacenamereplace.bl_label))
        layout.operator("replacename.select", text=(BUTTON_OT_replacenameselect.bl_label))
        

#register    
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.replacenameobjects = bpy.props.BoolProperty \
        (
          name = "Objects",
          description = "Search and Replace on Objects",
          default = True
        )
    bpy.types.Scene.replacenamelights = bpy.props.BoolProperty \
        (
          name = "Lights",
          description = "Search and Replace on Lights",
          default = False
        )
    bpy.types.Scene.replacenamecameras = bpy.props.BoolProperty \
        (
          name = "Cameras",
          description = "Search and Replace on Cameras",
          default = False
        )
    bpy.types.Scene.replacenamegroups = bpy.props.BoolProperty \
        (
          name = "Groups",
          description = "Search and Replace on Groups",
          default = True
        )
    bpy.types.Scene.replacenamebones = bpy.props.BoolProperty \
        (
          name = "Bones",
          description = "Search and Replace on Armatures and Bones",
          default = True
        )
    bpy.types.Scene.replacenameemptylattice = bpy.props.BoolProperty \
        (
          name = "Empty/Lattice",
          description = "Search and Replace on Empty and Lattice objects",
          default = True
        )
    bpy.types.Scene.replacenamematerials = bpy.props.BoolProperty \
        (
          name = "Materials",
          description = "Search and Replace on Materials",
          default = True
        )
    bpy.types.Scene.replacenameuvs = bpy.props.BoolProperty \
        (
          name = "UV Maps",
          description = "Search and Replace on UV Maps",
          default = True
        )
    bpy.types.Scene.replacenamevertexgroups = bpy.props.BoolProperty \
        (
          name = "Vertex Groups",
          description = "Search and Replace on Vertex Groups",
          default = True
        )
    bpy.types.Scene.replacenameshapekeys = bpy.props.BoolProperty \
        (
          name = "Shape Keys",
          description = "Search and Replace on Shape Keys",
          default = True
        )
    bpy.types.Scene.replacenameselected = bpy.props.BoolProperty \
        (
          name = "Only Selected",
          description = "Only act on selected objects and/or their materials",
          default = False
        )
    bpy.types.Scene.replacenamecase = bpy.props.BoolProperty \
        (
          name = "Case Sensitive",
          description = "",
          default = False
        )
    bpy.types.Scene.replacenameold = bpy.props.StringProperty \
        (
          name = "",
          description = "Search string",
        )
    bpy.types.Scene.replacenamenew = bpy.props.StringProperty \
        (
          name = "",
          description = "New string",
        )
    bpy.types.Scene.replacenameuseobject = bpy.props.BoolProperty \
        (
          name = "Use Object Name",
          description = "Append the object/users name to the new string",
          default = False
        )
    bpy.types.Scene.replacenameprefix = bpy.props.BoolProperty \
        (
          name = "Smart Prefix",
          description = "Add a prefix based on object type automatically (geo,lit,cam,grp,mtl,uvs,vtx,shp)",
          default = False
        )
    bpy.types.Scene.replacenamelowsuffix = bpy.props.BoolProperty \
        (
          name = "Add \"_LOW\" Suffix",
          description = "Add the \"_LOW\" suffix to low resolution geometry",
          default = False
        )
    
    

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.replacenameobjects
    del bpy.types.Scene.replacenamelights
    del bpy.types.Scene.replacenamecameras
    del bpy.types.Scene.replacenamegroups
    del bpy.types.Scene.replacenamebones
    del bpy.types.Scene.replacenamematerials
    del bpy.types.Scene.replacenameuvs
    del bpy.types.Scene.replacenamevertexgroups
    del bpy.types.Scene.replacenameshapekeys
    del bpy.types.Scene.replacenameselected
    del bpy.types.Scene.replacenamecase
    del bpy.types.Scene.replacenameold
    del bpy.types.Scene.replacenamenew
    del bpy.types.Scene.replacenameuseobject
    del bpy.types.Scene.replacenameprefix
    del bpy.types.Scene.replacenamelowsuffix
    
    
if __name__ == "__main__":
    register()
