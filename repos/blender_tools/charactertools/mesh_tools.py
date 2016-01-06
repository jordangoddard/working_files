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
                    obj.modifiers.remove(modifier)
     
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

def lock_objects(state):
    for obj in bpy.context.selected_objects: 
        obj.lock_location[0] = state
        obj.lock_location[1] = state
        obj.lock_location[2] = state
        obj.lock_rotation[0] = state
        obj.lock_rotation[1] = state
        obj.lock_rotation[2] = state
        obj.lock_scale[0] = state
        obj.lock_scale[1] = state
        obj.lock_scale[2] = state
        
class WeightMirroring(object):
    """
    Mirror Weight
    """
    
    def __init__(self, side = 'LEFT'):

        #global variables
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
        self.selected_vertices = []

    def execute(self):
        import time
         
        start_time = time.time()
        
        symmetric = self.split_vertices()
        if not symmetric: 
            print("Not symmetric")
        else: 
            print("Symmetric")
        #self.find_corresponding_vertex_group()
       
        if bpy.context.active_object.mode != 'WEIGHT_PAINT':
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')    
            
        #Turn off x mirroring    
        self.obj.data.use_mirror_x = False 
        
        selected_vertices = self.find_selected_vertices()
        for vertex in self.left_vertices: 
            #print("IT'S A LEFT VERTEX")
            opp_vertex = self.find_opposite_vertex(vertex.co) #return the mirrored vertex                     
            if opp_vertex:
                for group in opp_vertex.groups: 
                    group.weight = 0.0 #Set everything to zero first
                for v_group in bpy.context.object.vertex_groups: 
                    _name = None
                    try: 
                        v_group.weight(vertex.index)
                    except RuntimeError:
                        pass #Not in group 
                    else:
                        import re
                        if v_group.weight(vertex.index):
                            if v_group.name.endswith('.L') or v_group.name.endswith('.R'):
                                #find opposite vertex group
                                if v_group.name.endswith('.L'):
                                    _name = str(v_group.name[:-1] + 'R')
                                elif v_group.name.endswith('.R'):
                                    _name = str(v_group.name[:-1] + 'L')
                            else:
                                _name = v_group.name
                            try:
                                bpy.context.object.vertex_groups[_name].add([opp_vertex.index], v_group.weight(vertex.index), 'REPLACE')
                            except KeyError: 
                                vgroup = bpy.context.object.vertex_groups.new(name = _name)
                                vgroup.add([opp_vertex.index], v_group.weight(vertex.index), 'REPLACE')

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
            if vgroup.name.endswith(end): #starts with 'def' ends with L
                match = re.match("(\w+\.\S+)%s" %end, vgroup.name) #find the whole name
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
          
    def split_vertices(self):
        """
        Split vertices for right vertices and left vertices 
        """
        for vertex in self.obj.data.vertices: 
            if round(vertex.co.x, 5) > 0: 
                self.left_vertices.append(vertex)
            if round(vertex.co.x, 5) < 0: 
                self.right_vertices.append(vertex)
        
        if len(self.left_vertices) == len(self.right_vertices):
            return True
        else:
            return False
                       
    def find_selected_vertices(self):
    
        selected_vertices = []
        
        obj = bpy.context.object
        for vertex in obj.data.vertices:
            if vertex.select:
                selected_vertices.append(vertex)
                
        return selected_vertices
                
    def find_opposite_vertex(self, vertex_co):
        """
        Find the opposite vertex of the param vertex 
        """
        from mathutils import Vector
        found = False
        x = 1
        y = 1
        z = 1
        max_distance = 0.5
        closest_vertex = None
        
        if self.left:
        #search for right
            for opp_vertex in self.right_vertices: 
         
                min_x = abs(opp_vertex.co[0] + vertex_co[0])
                min_y = abs(opp_vertex.co[1] - vertex_co[1])
                min_z = abs(opp_vertex.co[2] - vertex_co[2])
                num = Vector((min_x, min_y, min_z))
                distance = num.magnitude
                print(distance)
                if distance < max_distance:
                    max_distance = distance
                    closest_vertex = opp_vertex
                    
        if not self.left: 
        #search for left
            for opp_vertex in self.left_vertices: 
                min_x = abs(opp_vertex.co[0] + vertex_co[0])
                min_y = abs(opp_vertex.co[1] - vertex_co[1])
                min_z = abs(opp_vertex.co[2] - vertex_co[2])
                num = Vector((min_x, min_y, min_z))
                distance = num.magnitude
                print(distance)
                if distance < max_distance:
                    max_distance = distance
                    closest_vertex = opp_vertex
                        
        return closest_vertex