#Title: mesh_tools Module
#Publisher: Tangent Animation
#Author: Wayne Wu

import bpy 


def put_dummy():
    """
    Add a dummy simpledeform modifier at the end of every mesh 
    """
    mesh_list = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers: 
                if modifier.type == 'SUBSURF' or modifier.type == 'MULTIRES':
                    mesh_list.append(obj)
                if modifier.type == 'SIMPLE_DEFORM' and modifier.name == 'SimpleDeform_Dummy':
                    obj.modifiers_remove(modifier)
     
    for obj in mesh_list: 
        index = len(obj.modifiers) - 1
        if not obj.modifiers[index].type == 'SIMPLE_DEFORM': 
            simple_deform = obj.modifiers.new("SimpleDeform_Dummy", 'SIMPLE_DEFORM')
            simple_deform.limits[0] = 0
            simple_deform.limits[1] = 0
            simple_deform.angle = 0
       
def remove_modifiers():
    """
    Remove all modifiers and particle_systems
    """
    for obj in bpy.context.selected_objects:
        bpy.context.scene.objects.active = obj
        for mod in bpy.context.object.modifiers:
            bpy.context.object.modifiers.remove(mod)  
        for particle in obj.particle_systems: 
            bpy.ops.object.particle_system_remove()

def object_ray_viz(state):
    """
    Change ray visibility in cycles render
    """
    for object in bpy.context.selected_objects: 
        object.cycles_visibility.camera = state
        object.cycles_visibility.diffuse = state
        object.cycles_visibility.glossy = state
        object.cycles_visibility.transmission = state
        object.cycles_visibility.scatter = state
        object.cycles_visibility.shadow = state            

class WeightMirroring(object):
    """
    Mirror Weight
    """
    
    def __init__(self,side,prefix = 'def.'):

        #global variables
        self.prefix = prefix
        if side == 'LEFT':
            self.left = True
        else: 
            self.left = False
        self.right_vertices = []
        self.left_vertices = []
        self.vgroup_opp_index = [] #copy to: list of vertex group index to be copy to (R)
        self.vgroup_index = [] #copy from: list of vertex group index to be copy from (L)
        vertices_index = [] #list of vertices' index(L)
        vertices_opp_index = [] #list of vertices' index(R)
        self.opp_group_index = []
        self.group_index = []
        self.debug_num = []
        self.obj = bpy.context.object

    def execute(self):
        import re
        import time
         
        start_time = time.time()
        
        self.split_vertices()
        self.find_corresponding_vertex_group()
        #Check if in Weight Paint Mode
       
        if bpy.context.active_object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')    
        #Turn off x mirroring    
        self.obj.data.use_mirror_x = False 
        
        if self.left: 
            for vertex in self.left_vertices: 
                #print("IT'S A LEFT VERTEX")
                opp_vertex = self.find_opposite_vertex(vertex.co) #return the mirrored vertex    

                num = 0 #for group index
                if opp_vertex:
                    for groups in opp_vertex.groups: 
                        groups.weight = 0.0 #Set everything to zero first
                        
                    for g in vertex.groups:
                        if g.weight: #if it has weight
                            self.group_index = self.find_group_index(self.vgroup_index, vertex) #find L self.group_index
                            self.opp_group_index = self.find_group_index(self.vgroup_opp_index, opp_vertex) #find R self.group_index
                            if num in self.group_index: #it's a side vertex group eg. def._.L
                                opp_index = self.opp_group_index[self.group_index.index(num)] #index of the opposite group
                                print(g.weight)
                                opp_vertex.groups[opp_index].weight = g.weight
                                print(opp_vertex.groups[opp_index].weight)
                                #opp_vertex.groups[num].weight = 0.0                            
                            elif num in self.opp_group_index: #same side, do not copy
                                pass #do nothing                     
                            else:
                                #neutral, copy same value as the self.left side
                                for mg in opp_vertex.groups: 
                                    if mg.group == g.group:
                                        mg.weight = g.weight                                 
                        num = num + 1
                else: 
                    self.debug_num.append(vertex.index) #vertex has no opposite
                    
        if not self.left:
            for vertex in self.right_vertices: 
                    #print("IT'S A LEFT VERTEX")
                    opp_vertex = self.find_opposite_vertex(vertex.co) #return the mirrored vertex    

                    num = 0 #for group index
                    if opp_vertex:
                        for groups in opp_vertex.groups: 
                            groups.weight = 0.0 #Set everything to zero first
                            
                        for g in vertex.groups:
                            if g.weight: #if it has weight
                                self.group_index = self.find_group_index(self.vgroup_index, vertex) #find L self.group_index
                                self.opp_group_index = self.find_group_index(self.vgroup_opp_index, opp_vertex) #find R self.group_index
                                if num in self.group_index: #it's a side vertex group eg. def._.L
                                    opp_index = self.opp_group_index[self.group_index.index(num)] #index of the opposite group
                                    print(g.weight)
                                    opp_vertex.groups[opp_index].weight = g.weight
                                    print(opp_vertex.groups[opp_index].weight)
                                    #opp_vertex.groups[num].weight = 0.0
                                    
                                elif num in self.opp_group_index: #same side, do not copy
                                    pass #do nothing
                                
                                else:
                                    #neutral, copy same value as the self.left side
                                    for mg in opp_vertex.groups: 
                                        if mg.group == g.group:
                                            mg.weight = g.weight                                 
                            num = num + 1
                    else: 
                        self.debug_num.append(vertex.index) #vertex has no opposite
                        
        print(self.debug_num)
        print(len(self.debug_num))
        print('FINISHED')
        print(time.time() - start_time)    
        
    def find_corresponding_vertex_group(self):
        #Find the needed vertex groups to be copied and put it into a list 
        end = None
        opp = None

        if self.left:
            end = ".L"
            opp = ".R"
        if not self.left: 
            end = ".R"
            opp = ".L"
        import re
        for vgroup in self.obj.vertex_groups:
            if vgroup.name.startswith(self.prefix) and vgroup.name.endswith(end): #starts with 'def' ends with L
                match = re.match("(%s\S+)%s" %(self.prefix, end), vgroup.name) #find the whole name
                if match: 
                        print(match.group(1))
                        match_name = match.group(1) + opp
                        self.vgroup_opp_index.append(self.obj.vertex_groups[match_name].index)
                self.vgroup_index.append(vgroup.index) #this is the vertex group you want for to deal with
        if len(self.vgroup_index) == len(self.vgroup_opp_index):
            print("True")
         
    def find_group_index(self, vgroup_index, vertex):
        temp_index = []
        for i in vgroup_index: 
            num = 0
            for g in vertex.groups:
                if g.group == i:
                    temp_index.append(num)
                    break
                num = num + 1           
        return temp_index
           
    def find_opposite_vertex(self, vertex_co):
        """
        Find the opposite vertex of the param vertex 
        """
        
        found = False
        x = 1
        y = 1
        z = 1
        closest_vertex = None
        
        if self.left:
            for opp_vertex in self.right_vertices: 
                #Filter #1
                #if round(opp_vertex.co[0],2) == round(-(vertex_co[0]),2) and round(opp_vertex.co[1],2) == round(vertex_co[1],2) and round(opp_vertex.co[2],2) == round(vertex_co[2],2):
                min_x = abs(opp_vertex.co[0] + vertex_co[0])
                min_y = abs(opp_vertex.co[1] - vertex_co[1])
                min_z = abs(opp_vertex.co[2] - vertex_co[2])
                #filter #2
                if min_x < x and min_y < y and min_z < z:
                    x = min_x
                    y = min_y 
                    z = min_z
                    closest_vertex = opp_vertex
                    
        if not self.left: 
            for opp_vertex in self.left_vertices: 
                #Filter #1
                #if round(opp_vertex.co[0],2) == round(-(vertex_co[0]),2) and round(opp_vertex.co[1],2) == round(vertex_co[1],2) and round(opp_vertex.co[2],2) == round(vertex_co[2],2):
                min_x = abs(opp_vertex.co[0] + vertex_co[0])
                min_y = abs(opp_vertex.co[1] - vertex_co[1])
                min_z = abs(opp_vertex.co[2] - vertex_co[2])
                #filter #2
                if min_x < x and min_y < y and min_z < z:
                    x = min_x
                    y = min_y 
                    z = min_z
                    closest_vertex = opp_vertex
            
        return closest_vertex
        
    def split_vertices(self):
        """
        Split vertices for right vertices and left vertices 
        """
        for vertex in self.obj.data.vertices: 
            if round(vertex.co.x, 5) > 0: 
                self.left_vertices.append(vertex)
            if round(vertex.co.x, 5) < 0: 
                self.right_vertices.append(vertex)
