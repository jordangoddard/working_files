# <pep8 compliant>
# -*- coding: utf-8 -*-
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
    "name": "Mirror Vertex Groups",
    "description": "Mirror the vertex groups on the X-Axis. Useful to copy the vertex weight from Left to Right or from Right to Left.",
    "author": "LWH (Loewenguth Pascal)",
    "tooltip": "Mirror the vertex groups on the X-Axis",
    "usage": " ",
    "version": (0, 1),
    "blender": (2, 73, 0),
    "location": "Properties > Object Data > Mirror Vertex Groups",
    "warning": "",
    "wiki_url": ""
                "",
    "category": "Mesh"
}

import bpy
import sys
import mathutils
import re
import unittest

MIN = 0.0001

# *****************************************************************************
#
# *****************************************************************************


class exVertex:
    def __init__(self, v):
        self.index = v.index
        self.co = v.co
        self.side = '?'
        self.normal = v.normal
        if v.co.x > MIN:
            self.side = 'L'
        elif v.co.x < -MIN:
            self.side = 'R'
        self.mirror_index = -1
        self.edges = list()
        self.selected = v.select

    def find_edges(self, e):
        for edge in e:
            if edge.vertices[0] == self.index:
                self.edges.append(edge.vertices[1])
            elif edge.vertices[1] == self.index:
                self.edges.append(edge.vertices[0])

# *****************************************************************************
#
# *****************************************************************************


class ObjectMirrorVertexGroups(bpy.types.Operator):
    """Object Mirror Vertex groups"""
    bl_idname = "object.mirror_vertexgroups"
    bl_label = "Mirror Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    action = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        self.obj = scene.objects.active
        nb_g, nb_v = 0, 0

        if self.obj is None:
            self.obj = bpy.context.object
        if self.obj.type != 'MESH':
            self.obj = None

        if self.obj is not None:
            if len(self.obj.vertex_groups) <= 0:
                self.report({'WARNING'}, 'No Vertex group to work with')
                return {'FINISHED'}
            #Sort the Vertex groups list regardless of the side
            if self.action == 'SORT_SIDE':
                lst = []
                error = False
                for g in self.obj.vertex_groups:
                    s = self.sort_side(g)
                    lst.append((s, g.name))
                    g.name = s
                    nb_g += 1
                try:
                    bpy.ops.object.vertex_group_sort(sort_type='NAME')
                except:
                    error = True
                for g in self.obj.vertex_groups:
                    for (a, b) in lst:
                            if a == g.name:
                                g.name = b
                                break
                if error:
                    self.report({'WARNING'}, 'The vertex groups could nt be sorted.')
                else:
                    self.report({'INFO'}, '{} group(s) sorted.'.format(nb_g))
            #Sort the Vertex groups list accordless to the Z position
            elif self.action == 'SORT_POSITION':
                lst = []
                error = False
                for g in self.obj.vertex_groups:
                    s = self.sort_position(g)
                    lst.append((s, g.name))
                    g.name = s
                    nb_g += 1
                try:
                    bpy.ops.object.vertex_group_sort(sort_type='NAME')
                except:
                    error = True
                for g in self.obj.vertex_groups:
                    for (a, b) in lst:
                            if a == g.name:
                                g.name = b
                                break
                if error:
                    self.report({'WARNING'}, 'The vertex groups could nt be sorted.')
                else:
                    self.report({'INFO'}, '{} group(s) sorted.'.format(nb_g))
            else:
                m = self.obj.mode
                bpy.ops.object.mode_set(mode='OBJECT')
                self.liste = self.load_vertex(self.obj)
                self.find_mirror(self.liste)
                #Mirror the selected vertex group, if the side is indicated
                #(Head.L or L_Head or Left Head...)
                if self.action == 'MIRROR':
                    if self.obj.vertex_groups.active is not None:
                        name = self.obj.vertex_groups.active.name
                        side = self.getSide(name)
                        if (side == 'L') or (side == 'R'):
                            (nb_g, nb_v) = self.mirroredvertices(side, name)
                            self.report({'INFO'}, '{} vertice(s) mirrored.'.format(nb_v))
                #Creates a vertex group hat contains all the vertices that do
                #not have a mirror
                elif self.action == 'UNM':
                    nb_v = self.unmirroredvertices()
                    self.report({'INFO'}, '{} vertice(s) can not be mirrored.'.format(nb_v))
                #Mirror all the vertex group from left to right
                #(Head-L->Head-R)
                elif self.action == 'L2R':
                    (nb_g, nb_v) = self.mirroredvertices(self.action)
                    self.report({'INFO'}, '{0} group(s) and {1} vertice(s) mirrored.'.format(nb_g, nb_v))
                #Mirror all the vertex group from right to left
                #(HeadRight -> HeadLeft)
                elif self.action == 'R2L':
                    (nb_g, nb_v) = self.mirroredvertices(self.action)
                    self.report({'INFO'}, '{0} group(s) and {1} vertice(s) mirrored.'.format(nb_g, nb_v))
                else:
                    raise Exception('Unknow action', self.action)
                if m != 'OBJECT':
                    bpy.ops.object.mode_set(mode=m)
        else:
            self.report({'WARNING'}, 'No mesh object selected')
        return {'FINISHED'}

    # Creates the group "Unmirrored_vertices" that contains all the vertices
    #with no mirror vertice
    def unmirroredvertices(self):
        nb_v = 0
        vg = self.obj.vertex_groups
        index_dest = self.getIndex(vg, 'Unmirrored_vertices')
        if index_dest != -1:
            vg.remove(vg[index_dest])
        found = False
        for v in self.liste:
            if v.mirror_index == -1:
                found = True
                break
        if found:
            vg.new(name='Unmirrored_vertices')
            index_dest = self.getIndex(vg, 'Unmirrored_vertices')
            if index_dest != -1:
                for v in [v1 for v1 in self.liste if v1.mirror_index == -1]:
                    vg[index_dest].add([v.index], 1, 'ADD')
                    nb_v += 1
        return nb_v

    #Get the index of the item in the collection
    def getIndex(self, col, oname):
        for i in range(len(col)):
            name = getattr(col[i], 'name')
            if name == oname:
                return i
        return -1

    #Used to sort the vertex groups regardless of the side.
    #Return the name without the side indication (sort_side('Head.L') -> Head)
    def sort_side(self, item):
        n = item.name
        s = self.getSide(n)
        if s == '?':
            n = '0 ' + n
        else:
            n = '1 ' + self.getName(n) + s
        return n

    #used to sort the vertex groups accordless to the Z position
    def sort_position(self, item):
        i = item.index
        s = self.getSide(item.name)
        maxi = sys.float_info.min
        x, y, z, nb = 0, 0, 0, 0
        for v in self.obj.data.vertices:
            if v.co.z > maxi:
                    maxi = v.co.z
            for g in v.groups:
                if g.group == i:
                    nb += 1
                    x, y, z = x + v.co.x, y + v.co.y, z + v.co.z
                break
        if nb > 1:
            x, y, z = x / nb, y / nb, maxi - (z / nb)
        n = '{0:0=+10.5f}{1:0=+10.5f}{2:0=+10.5f}'.format(z, x, y)
        if s == '?':
            n = n + ' '+item.name
        else:
            n = n + s + item.name
        return n

    #Mirror the vertex groups
    def mirroredvertices(self, action, group_name=''):
        nb_v, nb_g = 0, 0
        vg = self.obj.vertex_groups
        fname = getattr(self.obj, 'VG_filter')
        for i in range(len(vg)):
            name = getattr(vg[i], 'name')
            if (fname <= ' ') or (fname == '*') or (fname == '%'):
                filterok = True
            elif (name.find(fname) > 0) or (name.upper().find(fname.upper()) > 0):
                filterok = True
            elif (re.match(fname, name)):
                filterok = True
            elif (re.search(fname, name)):
                filterok = True
            else:
                filterok = False
            if (name > ' ') and (filterok) and ((name == group_name) or (group_name == '')):
                side = self.getSide(name)
                if side == action[0]:
                    invname = self.getFlippedName(name)
                    index_dest = self.getIndex(vg, invname)
                    if invname != '?':
                        #If the vertex group does'nt exist, it would be created
                        if index_dest != -1:
                            vg.remove(vg[index_dest])
                        vg.new(name=invname)
                        nb_g += 1
                        nb_v += self.copyVerts(name, invname)
        return (nb_g, nb_v)

    #Copy the source vertex group to dest.Return the number or vertices mirrored
    def copyVerts(self, source, dest):
        nb = 0
        vg = self.obj.vertex_groups
        index_source = self.getIndex(vg, source)
        index_dest = self.getIndex(vg, dest)
        verts = self.liste
        if (index_source >= 0) and (index_dest >= 0):
            for v in verts:
                if (v.mirror_index != -1):
                    for g in self.obj.data.vertices[v.index].groups:
                        if g.group == index_source:
                            vg[index_dest].add([v.mirror_index], g.weight, 'ADD')
                            nb += 1
                            break
        return nb

    #Return the side of the vertex group according to its name
    #getSide(Head.L)->L)
    def getSide(self, oname):
        side = '?'
        if (oname[-2:] == '.L') or (oname[-2:] == '.l') or (oname[-2:] == '_L') or (oname[-2:] == '_l') or (oname[-2:] == '-L') or (oname[-2:] == '-l'):
            side = 'L'
        elif (oname[:2] == 'L.') or (oname[:2] == 'l.') or (oname[:2] == 'L_') or (oname[:2] == 'l_') or (oname[:2] == 'L-') or (oname[:2] == 'l-'):
            side = 'L'
        elif (oname[-2:] == ' L') or (oname[-2:] == ' l') or (oname[:2] == 'L ') or (oname[:2] == 'l '):
            side = 'L'
        elif (oname[:4] == 'LEFT') or (oname[:4] == 'Left') or (oname[:4] == 'left') or (oname[-4:] == 'LEFT') or (oname[-4:] == 'Left') or (oname[-4:] == 'left'):
            side = 'L'
        elif (oname[-2:] == '.R') or (oname[-2:] == '.r') or (oname[-2:] == '_R') or (oname[-2:] == '_r') or (oname[-2:] == '-R') or (oname[-2:] == '-r'):
            side = 'R'
        elif (oname[:2] == 'R.') or (oname[:2] == 'r.') or (oname[:2] == 'R_') or (oname[:2] == 'r_') or (oname[:2] == 'R-') or (oname[:2] == 'r-'):
            side = 'R'
        elif (oname[-2:] == ' R') or (oname[-2:] == ' r') or (oname[:2] == 'R ') or (oname[:2] == 'r '):
            side = 'R'
        elif (oname[:5] == 'RIGHT') or (oname[:5] == 'Right') or (oname[:5] == 'right') or (oname[-5:] == 'RIGHT') or (oname[-5:] == 'Right') or (oname[-5:] == 'right'):
            side = 'R'
        return side

    #Return the name of the vertex group without the side
    #(getName(Head.L)->Head)
    def getName(self, oname):
        name = '?'
        if (oname[-2:] == '.L') or (oname[-2:] == '.l') or (oname[-2:] == '_L') or (oname[-2:] == '_l') or (oname[-2:] == '-L') or (oname[-2:] == '-l'):
            name = oname[:-2]
        elif (oname[:2] == 'L.') or (oname[:2] == 'l.') or (oname[:2] == 'L_') or (oname[:2] == 'l_') or (oname[:2] == 'L-') or (oname[:2] == 'l-'):
            name = oname[2:]
        elif (oname[-2:] == ' L') or (oname[-2:] == ' l') or (oname[:2] == 'L ') or (oname[:2] == 'l '):
            name = oname[:-2]
        elif (oname[:4] == 'LEFT') or (oname[:4] == 'Left') or (oname[:4] == 'left'):
            name = oname[-4:]
        elif (oname[-4:] == 'LEFT') or (oname[-4:] == 'Left') or (oname[-4:] == 'left'):
            name = oname[:4]
        elif (oname[-2:] == '.R') or (oname[-2:] == '.r') or (oname[-2:] == '_R') or (oname[-2:] == '_r') or (oname[-2:] == '-R') or (oname[-2:] == '-r'):
            name = oname[:-2]
        elif (oname[:2] == 'R.') or (oname[:2] == 'r.') or (oname[:2] == 'R_') or (oname[:2] == 'r_') or (oname[:2] == 'R-') or (oname[:2] == 'r-'):
            name = oname[2:]
        elif (oname[-2:] == ' R') or (oname[-2:] == ' r') or (oname[:2] == 'R ') or (oname[:2] == 'r '):
            name = oname[:-2]
        elif (oname[:5] == 'RIGHT') or (oname[:5] == 'Right') or (oname[:5] == 'right') or (oname[-5:] == 'RIGHT') or (oname[-5:] == 'Right') or (oname[-5:] == 'right'):
            name = oname[-4]
        return name

    #Prepare all the vertex of the selected mesh
    def load_vertex(self, o):
        list = []
        verts = o.data.vertices
        for v in verts:
            myvert = exVertex(v)
            myvert.find_edges(o.data.edges)
            list.append(myvert)
        return list

    #For each vertices of the mesh, try to find the mirror
    def find_mirror(self, l):
        nb_inconnus = 0
        for v in l:
            if (v.mirror_index == -1):
                if (v.side == '?'):
                    v.mirror_index = v.index
                else:
                    nb_inconnus += 1
        # 1st pass : exactly mirrored position
        for v in l:
            if (v.mirror_index == -1) and (v.side != '?') and (len(v.edges) > 0):
                for i in range(len(v.edges)):
                    vm = l[v.edges[i]]
                    if (vm.index != v.index) and (vm.co.y == v.co.y) and (vm.co.z == v.co.z) and (vm.co.x == -v.co.x) and (vm.mirror_index == -1) and (len(v.edges) == len(vm.edges)):
                        vm.mirror_index = v.index
                        v.mirror_index = vm.index
                        nb_inconnus = nb_inconnus - 2
                        break
        if (nb_inconnus > 0):
            for v in l:
                if (v.mirror_index == -1) and (v.side != '?'):
                    for vm in l:
                        if (vm.index != v.index) and (vm.co.x == -v.co.x) and (vm.co.z == v.co.z) and (vm.co.y == v.co.y) and (vm.mirror_index == -1) and (len(v.edges) == len(vm.edges)):
                            vm.mirror_index = v.index
                            v.mirror_index = vm.index
                            nb_inconnus -= 2
                            break
        if (nb_inconnus > 0):
            for v in l:
                if (v.mirror_index == -1) and (v.side != '?'):
                    for vm in l:
                        if (vm.index != v.index) and (vm.co.x == -v.co.x) and (vm.co.z == v.co.z) and (vm.co.y == v.co.y) and (vm.mirror_index == -1):
                            vm.mirror_index = v.index
                            v.mirror_index = vm.index
                            nb_inconnus = nb_inconnus - 2
        # 2nd pass
        mini = MIN / 5
        while (nb_inconnus > 0) and (mini <= MIN):
            mini += MIN / 5
            for v in l:
                if (v.mirror_index == -1) and (v.side != '?') and (len(v.edges) > 0):
                    for i in range(len(v.edges)):
                        vm = l[v.edges[i]]
                        if (vm.index != v.index) and (abs(vm.co.y - v.co.y) < mini) and (abs(vm.co.z - v.co.z) < mini) and (abs(vm.co.x + v.co.x) < mini) and (vm.mirror_index == -1) and (len(v.edges) == len(vm.edges)):
                            vm.mirror_index = v.index
                            v.mirror_index = vm.index
                            nb_inconnus = nb_inconnus - 2
        # 3rd
        mini = MIN / 5
        while (nb_inconnus > 0) and (mini <= MIN):
            mini += MIN / 5
            for v in l:
                if (v.mirror_index == -1) and (v.side != '?'):
                    for vm in l:
                        if (vm.index != v.index) and (abs(vm.co.x + v.co.x) < mini) and (abs(vm.co.z - v.co.z) < mini) and (abs(vm.co.y - v.co.y) < mini) and (vm.mirror_index == -1) and (len(v.edges) == len(vm.edges)):
                            vm.mirror_index = v.index
                            v.mirror_index = vm.index
                            nb_inconnus = nb_inconnus - 2
        # 4th
        change = True
        while (change) and (nb_inconnus > 0):
            change = False
            if nb_inconnus > 0:
                for v in l:
                    if (v.mirror_index == -1) and (v.side == '?') and (len(v.edges) > 0):
                        max = 0
                        sommet = -1
                        nco = mathutils.Vector()
                        nco[:] = v.co
                        nco.x = - nco.x
                        dist = -1
                        for vm in l:
                            if (vm.index != v.index) and (vm.mirror_index == -1) and (vm.side != '?') and (vm.side != v.side):
                                nb_sommets = 0
                                d = (vm.co - nco).length
                                if (len(v.edges) == len(vm.edges)):
                                    for i in range(len(v.edges)):
                                        j = l[v.edges[i]].mirror_index
                                        if (j != -1) and (j in vm.edges):
                                            nb_sommets = nb_sommets + 1
                                if (nb_sommets > max):
                                    max = nb_sommets
                                    sommet = vm.index
                                elif (nb_sommets == max) and (d < dist):
                                    sommet = vm.index
                                    dist = d
                        if sommet != -1:
                            change = True
                            vm = l[sommet]
                            vm.mirror_index = v.index
                            v.mirror_index = vm.index
                            nb_inconnus = nb_inconnus - 2
        # 5th
        change = True
        while (change) and (nb_inconnus > 0):
            change = False
            if nb_inconnus > 0:
                for v in l:
                    if (v.mirror_index == -1) and (v.side != '?') and (len(v.edges) > 0):
                        max = 0
                        sommet = -1
                        nco = mathutils.Vector()
                        nco[:] = v.co
                        nco.x = - nco.x
                        dist = -1
                        for vm in l:
                            if (vm.index != v.index) and (vm.mirror_index == -1) and (vm.side != '?') and (vm.side != v.side):
                                nb_sommets = 0
                                d = (vm.co - nco).length
                                if (len(v.edges) == len(vm.edges)):
                                    for i in range(len(v.edges)):
                                        j = l[v.edges[i]].mirror_index
                                        if (j != -1) and (j in vm.edges):
                                            nb_sommets = nb_sommets + 1
                                if (nb_sommets > max):
                                    max = nb_sommets
                                    sommet = vm.index
                                elif (nb_sommets == max) and (d < dist):
                                    sommet = vm.index
                                    dist = d
                        if sommet != -1:
                            change = True
                            vm = l[sommet]
                            vm.mirror_index = v.index
                            v.mirror_index = vm.index
                            nb_inconnus = nb_inconnus - 2

    # Return the flippedName.
    #For example :  getFlippedName('Hand.L') returns 'Hand.R'
    def getFlippedName(self, oname):
        nname = '?'
        #.L  ->  .R
        if (oname[-2:] == '.L'):
            nname = oname[:-2] + '.R'
        elif (oname[-2:] == '.R'):
            nname = oname[:-2] + '.L'
        elif (oname[-2:] == '.l'):
            nname = oname[:-2] + '.r'
        elif (oname[-2:] == '.r'):
            nname = oname[:-2] + '.l'
        #-L   ->   -R
        elif (oname[-2:] == '-L'):
            nname = oname[:-2] + '-R'
        elif (oname[-2:] == '.R'):
            nname = oname[:-2] + '.L'
        elif (oname[-2:] == '-l'):
            nname = oname[:-2] + '-r'
        elif (oname[-2:] == '.r'):
            nname = oname[:-2] + '.l'
        #_L  ->  _R
        if (oname[-2:] == '_L'):
            nname = oname[:-2] + '_R'
        elif (oname[-2:] == '_R'):
            nname = oname[:-2] + '_L'
        elif (oname[-2:] == '_l'):
            nname = oname[:-2] + '_r'
        elif (oname[-2:] == '_r'):
            nname = oname[:-2] + '_l'
        # L  ->   R
        if (oname[-2:] == ' L'):
            nname = oname[:-2] + ' R'
        elif (oname[-2:] == ' R'):
            nname = oname[:-2] + ' L'
        elif (oname[-2:] == ' l'):
            nname = oname[:-2] + ' r'
        elif (oname[-2:] == ' r'):
            nname = oname[:-2] + ' l'
        #L.  ->  R.
        if (oname[:2] == 'L.'):
            nname = 'R.' + oname[2:]
        elif (oname[:2] == 'R.'):
            nname = 'L.' + oname[2:]
        elif (oname[:2] == 'l.'):
            nname = 'r.' + oname[2:]
        elif (oname[:2] == 'r.'):
            nname = 'l.' + oname[2:]
        #L-  ->  R-
        if (oname[:2] == 'L-'):
            nname = 'R-' + oname[2:]
        elif (oname[:2] == 'R-'):
            nname = 'L-' + oname[2:]
        elif (oname[:2] == 'l-'):
            nname = 'r-' + oname[2:]
        elif (oname[:2] == 'r-'):
            nname = 'l-'+oname[2:]
        #L_  ->  R_
        if (oname[:2] == 'L_'):
            nname = 'R_' + oname[2:]
        elif (oname[:2] == 'R_'):
            nname = 'L_' + oname[2:]
        elif (oname[:2] == 'l_'):
            nname = 'r_' + oname[2:]
        elif (oname[:2] == 'r_'):
            nname = 'l_' + oname[2:]
        #L   ->  R
        if (oname[:2] == 'L '):
            nname = 'R ' + oname[2:]
        elif (oname[:2] == 'R '):
            nname = 'L ' + oname[2:]
        elif (oname[:2] == 'l '):
            nname = 'r ' + oname[2:]
        elif (oname[:2] == 'r '):
            nname = 'l ' + oname[2:]
        #LEFT xxx
        if (oname[:4] == 'LEFT'):
            nname = 'RIGHT' + oname[4:]
        elif (oname[:4] == 'Left'):
            nname = 'Right' + oname[4:]
        elif (oname[:4] == 'left'):
            nname = 'right' + oname[4:]
        elif (oname[:5] == 'RIGHT'):
            nname = 'LEFT' + oname[5:]
        elif (oname[:5] == 'Right'):
            nname = 'Left' + oname[5:]
        elif (oname[:5] == 'right'):
            nname = 'left' + oname[5:]
        #xxx LEFT
        if (oname[-4:] == 'LEFT'):
            nname = oname[:-4] + 'RIGHT'
        elif (oname[-4:] == 'Left'):
            nname = oname[:-4] + 'Right'
        elif (oname[-4:] == 'left'):
            nname = oname[:-4] + 'right'
        elif (oname[-5:] == 'RIGHT'):
            nname = oname[:-5] + 'LEFT'
        elif (oname[-5:] == 'Right'):
            nname = oname[:-5] + 'Left'
        elif (oname[-5:] == 'right'):
            nname = oname[:-5] + 'left'
        return nname


# *****************************************************************************
# INTERFACE
# *****************************************************************************


class DataPanel(bpy.types.Panel):
    bl_label = "Mirror Vertex groups"
    bl_idname = "DATA_PT_CVGlayout"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bpy.types.Object.VG_filter = bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        self.mpath = ''
        scene = context.scene
        self.filter = bpy.props.StringProperty()

        # Create a simple row.
        layout.prop(context.active_object, "VG_filter", text="Filter:")
        row = layout.row(align=True)
        row.operator("object.mirror_vertexgroups", text='From left to right').action = 'L2R'
        row.operator("object.mirror_vertexgroups", text='From right to left').action = 'R2L'
        row = layout.row(align=True)
        row.operator("object.mirror_vertexgroups", text='Unmirrored vertices').action = 'UNM'


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator("object.mirror_vertexgroups", text="Mirror active group", icon='ARROW_LEFTRIGHT').action = 'MIRROR'
    self.layout.operator("object.mirror_vertexgroups", text="Sort by side", icon='NONE').action = 'SORT_SIDE'
    self.layout.operator("object.mirror_vertexgroups", text="Sort by position", icon='NONE').action = 'SORT_POSITION'


# *****************************************************************************
# REGISTER / UNREGISTER
# *****************************************************************************

def register():
    bpy.utils.register_class(ObjectMirrorVertexGroups)
    bpy.utils.register_class(DataPanel)
    bpy.types.MESH_MT_vertex_group_specials.append(menu_func)


def unregister():
    bpy.types.MESH_MT_vertex_group_specials.remove(menu_func)
    bpy.utils.unregister_class(DataPanel)
    bpy.utils.unregister_class(ObjectMirrorVertexGroups)

# *****************************************************************************
# *****************************************************************************

if __name__ == "__main__":
    register()
