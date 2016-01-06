#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "Cube Surfer script",
    "author": "Jean-Francois Gallant(PyroEvil)",
    "version": (0, 0, 1),
    "blender": (2, 7, 1),
    "location": "Properties > Object Tab",
    "description": ("Cube Surfer script"),
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "http://pyroevil.com/",
    "tracker_url": "http://pyroevil.com/" ,
    "category": "Object"}
    
import bpy
from math import ceil,floor
from bpy.types import Operator,Panel, UIList
from bpy.props import FloatVectorProperty,IntProperty,StringProperty,FloatProperty,BoolProperty, CollectionProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
import sys
from cubesurfer import mciso
import time
import ctypes

tmframe = 'init'

def add_isosurf(self, context):

    mesh = bpy.data.meshes.new(name="IsoSurface")
    obj = bpy.data.objects.new("IsoSurface",mesh)
    bpy.context.scene.objects.link(obj)
    obj['IsoSurfer'] = True
    obj.IsoSurf_res = True
    obj.shape_key_add(name="Base")


class OBJECT_OT_add_isosurf(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_isosurf"
    bl_label = "Add IsoSurface Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale = FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )

    def execute(self, context):

        add_isosurf(self, context)

        return {'FINISHED'}


# Registration

def add_isosurf_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_isosurf.bl_idname,
        text="IsoSurface",
        icon='OUTLINER_DATA_META')


# This allows you to right click on a button and link to the manual
def add_isosurf_manual_map():
    url_manual_prefix = "http://pyroevil.com"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping    

    
def isosurf_prerender(context):
    scn = bpy.context.scene
    scn.IsoSurf_context = "RENDER"
    isosurf(context)

def isosurf_postrender(context):
    scn = bpy.context.scene    
    scn.IsoSurf_context = "WINDOW"
        
def isosurf_frame(context):
    scn = bpy.context.scene
    #print(scn.IsoSurf_context)
    if scn.IsoSurf_context == "WINDOW":
        isosurf(context)

        
def isosurf(context):
    global tmframe
    scn = bpy.context.scene
    

    
    stime = time.clock()
    global a
    
    SurfList = []
    i = 0
    for object in bpy.context.scene.objects:
        if 'IsoSurfer' in object:
            obsurf = object
            mesurf = object.data
            res = object.IsoSurf_res
            preview = object.IsoSurf_preview
            SurfList.append([(obsurf,mesurf,res,preview)])
            for item in object.IsoSurf:
                if item.active == True:
                    if item.obj != '':
                        if item.psys != '':
                            SurfList[i].append((item.obj,item.psys,item.sizem))
            i += 1
                            
    for surfobj in SurfList:
        print("Start calculation of isosurface...frame:",bpy.context.scene.frame_current)
        #print(bpy.context)
        #print(bpy.context.screen)
        #print(bpy.context.window)
        #print(bpy.context.area)
        #print(surfobj)
        obsurf,mesurf,res,preview = surfobj[0]
        #print(obsurf,mesurf)
        #print(surfobj[1][0])
        ploc = []
        psize = []
        pprop = []
        stime = time.clock()
        xmin = 10000000000
        xmax = -10000000000
        ymin = 10000000000
        ymax = -10000000000
        zmin = 10000000000
        zmax = -10000000000
        for obj,psys,sizem in surfobj[1:]:
            #print(obj,psys,res,sizem)
            psys = bpy.data.objects[obj].particle_systems[psys]
            #print(psys)
            psysize = len(psys.particles)
            for par in range(psysize):
                if psys.particles[par].alive_state == 'ALIVE':
                    size = psys.particles[par].size * sizem
                    ploc.append(psys.particles[par].location)
                    uvx = psys.settings['IsoLocalUV'][par*3]#psys.particles[par].location.x - 
                    uvy = psys.settings['IsoLocalUV'][par*3+1]#psys.particles[par].location.y - 
                    uvz = psys.settings['IsoLocalUV'][par*3+2]#psys.particles[par].location.z - 
                    pprop.append(psys.particles[par].velocity.to_tuple() + (uvx,uvy,uvz))
                    psize.append(size)
                    
        if len(psize) > 0:
        
            isolevel=0.0
            print('  pack particles:',time.clock() - stime,'sec')
            
            a,b = mciso.isosurface(res,isolevel,ploc,psize,pprop)
            print('  mciso:',time.clock() - stime,'sec')
            stime = time.clock()
            
            #if "myMesh" in bpy.data.meshes:
                #mesurf = bpy.data.meshes['myMesh']
            #else:
                #mesurf = bpy.data.meshes.new('myMesh')

            #if "myObject" in bpy.data.objects:
                #obsurf = bpy.data.objects['myObject']
            #else:
                #obsurf = bpy.data.objects.new('myObject', mesurf)
                #bpy.context.scene.objects.link(obsurf)


            #obsurf.show_name = True

            bm = bmesh.new()

            bm.from_mesh(mesurf)
            bm.clear()
            sh = bm.verts.layers.shape.new("IsoSurf_mb")
            p1 = bm.loops.layers.uv.new("IsoSurf_prop1")
            p2 = bm.loops.layers.uv.new("IsoSurf_prop2")
            lprop = 3 * 6
            for i in range(int(len(a)/9)):

                vertex1 = bm.verts.new( (a[i*9], a[i*9+1], a[i*9+2]) )
                vertex2 = bm.verts.new( (a[i*9+3], a[i*9+4], a[i*9+5]) )
                vertex3 = bm.verts.new( (a[i*9+6], a[i*9+7], a[i*9+8]) )
                
                #vertex1[sh] = (a[i*9] + b[i*lprop], a[i*9+1] + b[i*lprop+1], a[i*9+2] + b[i*lprop+2])
                #vertex2[sh] = (a[i*9+3] + b[i*lprop+6], a[i*9+4] + b[i*lprop+7], a[i*9+5] + b[i*lprop+8])
                #vertex3[sh] = (a[i*9+6] + b[i*lprop+12], a[i*9+7] + b[i*lprop+13], a[i*9+8] + b[i*lprop+14])
                
                #vertex1[sh] = (a[i*9]-b[i*lprop+3],a[i*9+1]-b[i*lprop+4],a[i*9+2]-b[i*lprop+5])
                #vertex2[sh] = (a[i*9+3]-b[i*lprop+9], a[i*9+4]-b[i*lprop+10],a[i*9+5]-b[i*lprop+11])
                #vertex3[sh] = (a[i*9+6]-b[i*lprop+15],a[i*9+7]-b[i*lprop+16],a[i*9+8]-b[i*lprop+17])
                
                vertex1[sh] = (b[i*lprop+3],b[i*lprop+4],b[i*lprop+5])
                vertex2[sh] = (b[i*lprop+9], b[i*lprop+10],b[i*lprop+11])
                vertex3[sh] = (b[i*lprop+15],b[i*lprop+16],b[i*lprop+17])
                
                bm.faces.new( (vertex1, vertex2, vertex3) ).smooth = True
                
            #print(preview)
            bm.verts.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            for i in range(int(len(a)/9)):
                bm.faces[i].loops[0][p1].uv = (b[i*lprop+3],b[i*lprop+4])
                bm.faces[i].loops[0][p2].uv = (b[i*lprop+5],0.0)
                bm.faces[i].loops[1][p1].uv = (b[i*lprop+9], b[i*lprop+10])
                bm.faces[i].loops[1][p2].uv = (b[i*lprop+11], 0.0)
                bm.faces[i].loops[2][p1].uv = (b[i*lprop+15],b[i*lprop+16])
                bm.faces[i].loops[2][p2].uv = (b[i*lprop+17],0.0)
                #bm.faces[i].loops[0][p1].uv = (a[i*9]-b[i*lprop+3],a[i*9+1]-b[i*lprop+4])
                #bm.faces[i].loops[0][p2].uv = (a[i*9+2]-b[i*lprop+5],0.0)
                #bm.faces[i].loops[1][p1].uv = (a[i*9+3]-b[i*lprop+9], a[i*9+4]-b[i*lprop+10])
                #bm.faces[i].loops[1][p2].uv = (a[i*9+5]-b[i*lprop+11], 0.0)
                #bm.faces[i].loops[2][p1].uv = (a[i*9+6]-b[i*lprop+15],a[i*9+7]-b[i*lprop+16])
                #bm.faces[i].loops[2][p2].uv = (a[i*9+8]-b[i*lprop+17],0.0)
            if preview == False:
                #print(preview)
                bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=res/100)

            bm.to_mesh(mesurf)
            scn.update()
            bm.free()
            mesurf.shape_keys.animation_data_clear()
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].slider_min = -1.0
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].value = 1/scn.render.fps
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].keyframe_insert("value",frame=scn.frame_current + 1)
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].value = -1/scn.render.fps
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].keyframe_insert("value",frame=scn.frame_current - 1)
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].value = 0.0
            mesurf.shape_keys.key_blocks['IsoSurf_mb'].keyframe_insert("value",frame=scn.frame_current)
            
            
            
            print('  Bmesh:',time.clock() - stime,'sec')

            #bpy.context.scene.objects.unlink(obsurf)
            #bpy.data.objects.remove(obsurf)
            #bpy.data.meshes.remove(mesurf)


class OBJECT_UL_IsoSurf(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.1)
        split.label(str(index))
        split.prop(item, "name", text="", emboss=False, translate=False, icon='OUTLINER_OB_META')
        split.prop(item,"active",text = "")


class UIListPanelExample(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "CubeSurfer Panel"
    bl_idname = "OBJECT_PT_ui_list_example"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        obj = context.object
        if 'IsoSurfer' in obj:
            layout = self.layout
            box = layout.box()
            row = box.row()
            row.operator("object.iso_local_uv",icon = 'GROUP_UVS',text = "Set Local UV at this time")
            row = box.row()
            row.prop(obj,"IsoSurf_res",text = "Voxel size:")
            row = box.row()
            #row.prop(obj,"IsoSurf_preview",text = "Preview Mode")
            #row = box.row()
            row.template_list("OBJECT_UL_IsoSurf", "", obj, "IsoSurf", obj, "IsoSurf_index")
            col = row.column(align=True)
            col.operator("op.isosurfer_item_add", icon="ZOOMIN", text="").add = True
            col.operator("op.isosurfer_item_add", icon="ZOOMOUT", text="").add = False    
            if obj.IsoSurf and obj.IsoSurf_index < len(obj.IsoSurf):
                row = box.row()
                row.prop(obj.IsoSurf[obj.IsoSurf_index],"active",text = "Active")
                row = box.row()
                row.label('Object: ')
                row.prop_search(obj.IsoSurf[obj.IsoSurf_index], "obj",context.scene, "objects", text="")
                if obj.IsoSurf[obj.IsoSurf_index].obj != '':
                    if bpy.data.objects[obj.IsoSurf[obj.IsoSurf_index].obj].type != 'MESH':
                        obj.IsoSurf[obj.IsoSurf_index].obj = ''
                    else:
                        row = box.row()
                        row.label('Particles: ')
                        row.prop_search(obj.IsoSurf[obj.IsoSurf_index], "psys",bpy.data.objects[obj.IsoSurf[obj.IsoSurf_index].obj], "particle_systems", text="")
                        if obj.IsoSurf[obj.IsoSurf_index].psys != '':
                            row = box.row()
                            row.prop(obj.IsoSurf[obj.IsoSurf_index],"sizem",text = "Particles Size Multiplier:")
                            row = box.row()
                            #row.prop(obj.IsoSurf[obj.IsoSurf_index],"res",text = "Voxel size:")
            row = box.row()
            box = box.box()
            box.active = False
            box.alert = False
            row = box.row()
            row.alignment = 'CENTER'
            row.label(text = "THANKS TO ALL DONATORS !")
            row = box.row()
            row.alignment = 'CENTER'
            row.label(text = "If you want donate to support my work")
            row = box.row()
            row.alignment = 'CENTER'
            row.operator("wm.url_open", text=" click here to Donate ", icon='URL').url = "www.pyroevil.com/donate/"
            row = box.row()
            row.alignment = 'CENTER'
            row.label(text = "or visit: ")
            row = box.row()
            row.alignment = 'CENTER'
            row.label(text = "www.pyroevil.com/donate/")
                            
        else:
            layout = self.layout
            box = layout.box()
            row = box.row()
            row.label('Please,select a IsoSurface object!',icon='ERROR')
                        
            

                
class OBJECT_OT_isosurfer_add(bpy.types.Operator):
    bl_label = "Add/Remove items from IsoSurf obj"
    bl_idname = "op.isosurfer_item_add"
    add = bpy.props.BoolProperty(default = True)

    def invoke(self, context, event):
        add = self.add
        ob = context.object
        if ob != None:
            item = ob.IsoSurf
            if add:
                item.add()
                l = len(item)
                item[-1].name = ("IsoSurf." +str(l))
                item[-1].active = True
                item[-1].sizem = 1.0
                #item[-1].res = 0.25
                item[-1].id = l
            else:
                index = ob.IsoSurf_index
                item.remove(index)

        return {'FINISHED'}                 
                

class IsoSurf(bpy.types.PropertyGroup):
    # name = StringProperty()
    active = BoolProperty()
    id = IntProperty()
    obj = StringProperty()
    psys = StringProperty()
    #res = FloatProperty()
    sizem = FloatProperty()
    weight = FloatProperty()    

class IsoLocalUV(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.iso_local_uv"
    bl_label = "Iso local UV"

    def execute(self, context):
        SurfList = []
        print("Transfert UV start")
        for item in context.object.IsoSurf:
            if item.active == True:
                if item.obj != '':
                    if item.psys != '':
                        SurfList.append([item.obj,item.psys])
        for obj,psys in SurfList:
            print("   ... UV transfert from:",obj,psys)
            bpy.data.objects[obj].particle_systems[psys].settings['IsoLocalUV'] = [0.0] * len(bpy.data.objects[obj].particle_systems[psys].particles) * 3
            bpy.data.objects[obj].particle_systems[psys].particles.foreach_get("location",bpy.data.objects[obj].particle_systems[psys].settings['IsoLocalUV'])
        print("Transfert UV end")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_add_isosurf)
    bpy.utils.register_manual_map(add_isosurf_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_isosurf_button)
    bpy.utils.register_module(__name__)
    bpy.types.Object.IsoSurf = CollectionProperty(type=IsoSurf)
    bpy.types.Object.IsoSurf_index = IntProperty()
    bpy.types.Object.IsoSurf_res = FloatProperty()
    bpy.types.Object.IsoSurf_preview = BoolProperty()
    bpy.types.Scene.IsoSurf_context = StringProperty(default = "WINDOW")
    #bpy.utils.register_class(IsoLocalUV)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_isosurf)
    bpy.utils.unregister_manual_map(add_isosurf_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_isosurf_button)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.IsoSurf
    #bpy.utils.register_class(IsoLocalUV)

    
if isosurf not in bpy.app.handlers.frame_change_post:
    print('create isosurfer handlers...')
    bpy.app.handlers.persistent(isosurf_frame)
    bpy.app.handlers.frame_change_post.append(isosurf_frame)
    bpy.app.handlers.persistent(isosurf_prerender)
    #bpy.app.handlers.render_init.append(isosurf_prerender)
    bpy.app.handlers.render_pre.append(isosurf_prerender)
    bpy.app.handlers.persistent(isosurf_postrender)
    bpy.app.handlers.render_post.append(isosurf_postrender)
    bpy.app.handlers.render_cancel.append(isosurf_postrender)
    bpy.app.handlers.render_complete.append(isosurf_postrender)
    print('isosurfer handler created successfully!')

