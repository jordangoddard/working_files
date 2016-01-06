#Title: bone_tools Module
#Publisher: Tangent Animation
#Author: Wayne Wu

import bpy
import re    
    
def bone_shape(shape = None, state = False):
    """
    Assign or remove bone_shape for the selected bones
    """
    if bpy.context.active_object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')
    selected = bpy.context.selected_pose_bones
    for item in selected: 
        if shape:
            item.custom_shape = bpy.context.scene.objects[shape]
        else:
            item.custom_shape = shape  
        try:
            bpy.context.object.data.bones[item.name].show_wire = state
        except: 
            #not allowed
            pass 
            
    return {'FINISHED'}
    
def bone_flip(exception):         
    """
    Flip selected bones upside down
    """
    
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
        
    for bone in bpy.context.selected_editable_bones:
        if not bone.name.startswith(exception):
            a = bone.tail.xyz
            b = bone.head.xyz 
            bone.tail.xyz = b
            bone.head.xyz = a    
                
def bone_lock(exception, state):
    """
    Lock the transformation for the selected bones
    """
    
    if bpy.context.active_object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')    

    for bone in bpy.context.selected_pose_bones:
        if not bone.name.startswith(exception):
            #Lock the location 
            bone.lock_location[0] = state
            bone.lock_location[1] = state
            bone.lock_location[2] = state
            
            #Lock the scale
            bone.lock_scale[0] = state
            bone.lock_scale[1] = state
            bone.lock_scale[2] = state
            
            #Lock the Rotation main
            bone.lock_rotation[0] = state
            bone.lock_rotation[1] = state
            bone.lock_rotation[2] = state
            
            #Lock the Rotation if other two types
            bone.lock_rotation_w = state
            bone.lock_rotations_4d = state
                               
def remove_dependencies():
    """
    Remove all dependencies at the armature level
    """
    error =[]
    for armature in bpy.data.armatures: 
        if armature.name.startswith('rig'):
            try: 
                armature.animation_data
            except: 
                print("ERROR: no animation data(driver)")
            else:
                try:
                    for d in armature.animation_data.drivers:
                        if d.data_path.endswith('.hide') or d.data_path.endswith('.bbone_in') or d.data_path.endswith('.bbone_out'):
                            try:
                                armature.driver_remove(d.data_path)
                                #print("%s removed" %d.data_path)
                            except TypeError: #driver path is broken
                                for var in d.driver.variables:
                                    d.driver.variables.remove(var)
                                d.data_path = 'bones[\"ctl.god.C\"].hide'      #change data_path target to ctl.god.C so that it's deletable                
                                armature.driver_remove(d.data_path)              
                        else:
                            error.append("Driver(Armature %s) pointed to %s will not be removed" %(armature.name, d.data_path)) 
                except AttributeError: 
                    print("No driver")
                for layer in armature.layers: 
                   layer = True
                try: 
                    for b in bpy.data.objects[armature.name].pose.bones:
                        b.bone.hide = False
                except KeyError:
                    pass                
                i = 0
                while (i < 32):
                    if 7 < i < 16 or i > 23:
                        armature.layers[i] = False
                    i = i + 1
                
    for obj in bpy.data.objects: 
        if obj.name.startswith('rig'):
            try:
                for d in obj.animation_data.drivers:
                    if not d.is_valid:
                        error.append("Driver(Object %s) Datapath %s is broken" %(obj.name, d.data_path))     
            except AttributeError:
                pass
    return error

def bone_parenting(change_name, new_bone_prefix, old_bone_prefix, size_scale):
    """
    Duplicate bone and keep offset for the current one to the duplicate
    """

    import re
    #User Input
    #None User input var 
    armature_name = None
    new_bone_name = None
    #Check if in edit mode
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    #Retrieve armature name
    for obj in bpy.context.selected_objects: 
        if obj.type == 'ARMATURE':
            armature_name = obj.name
    #Copy bone parenting
    for bone in bpy.context.selected_bones:     
        parent_bone = bone.parent
        tail_location = bone.tail     
        amt = bpy.data.armatures[armature_name] 
        if change_name:
            match = re.match("%s(\S+)" %old_bone_prefix, bone.name)
            if match:
                new_bone_name = "%s%s" %(new_bone_prefix, match.group(1))   
        else: 
            new_bone_name = bone.name
        new_bone = amt.edit_bones.new(new_bone_name)
        new_bone.head = bone.head
        new_bone.tail = bone.tail
        directional_vector = new_bone.tail - new_bone.head
        directional_vector = (size_scale-1)*directional_vector
        new_bone.tail = new_bone.tail + directional_vector
        if bone.parent: 
            new_bone.parent = bone.parent
            new_bone.parent.use_connect = False
        new_bone.use_inherit_rotation = True
        new_bone.use_inherit_scale = True
        new_bone.use_local_location = True
        new_bone.use_deform = False
        bone.parent = new_bone
    return {'FINISHED'}

def mute_bone_constraint(value):
    """
    Mute or unmute constraints for the selected bones
    """
    
    for bone in bpy.context.selected_pose_bones: 
        for constraint in bone.constraints: 
            constraint.mute = value
   
    #Refresh Screen
    bpy.ops.object.mode_set(mode ='EDIT')
    bpy.ops.object.mode_set(mode ='POSE')

def copy_driver(source_bone, copy_over = True):
    """
    Copy Driver from source bone to selected bones
    """

    import re
    
    copy_bone = source_bone #Bone to be coppied 
    acc_driver = "none" #Driver Bone if in the same layer
    #Determines The Driver Details
    armature_name = bpy.context.object.name
    for copy_action in bpy.context.object.pose.bones[copy_bone].constraints:
        action = copy_action.name
        driver_data = None
        expr = None
        for current_driver in bpy.data.objects[armature_name].animation_data.drivers:  
            path = current_driver.data_path
            driver_bone = re.match('pose\.bones\[\"(\S+)\"\]\.constraints\[\"(\S+)\"\]\.influence', path)         
            if driver_bone:
                driver_bone_name = driver_bone.group(1)
                action_name = driver_bone.group(2)      	
                if (driver_bone_name==copy_bone) and (action_name==action):                       
                    driver_data = current_driver.driver
                    expr = driver_data.expression #driver expression  
                    break 		    
        i = 0
        run = True	
        while run: 
            try:
                driver_data.variables[i]  #read variables 
            except: #out of range 
                run = False
            else:	
                var = driver_data.variables[i]
                
                #############################
                var_name = var.name  #variable name
                var_type = var.type	#variable name
                target = var.targets[0]
                target_id = target.id #target object
                target_data = target.data_path	#target data_path
                #############################
                
                for selected_bone in bpy.context.selected_pose_bones:
                    bone = bpy.data.armatures[armature_name].bones[selected_bone.name]
                    if bone.name is acc_driver or bone.name is copy_bone: 
                        pass
                    else: 
                        #Create Driver for influence
                        constraint = "pose.bones[\"" + bone.name + "\"].constraints[\"" + action + "\"].influence"
                        try:
                            bpy.context.object.driver_add(constraint).driver
                        except:
                            print("No such constraint")
                        #Determine the corresponding driver
                        for current_driver in bpy.data.objects[armature_name].animation_data.drivers:
                            if current_driver.data_path == constraint:
                                    #Add new variable for driver
                                    current_driver.driver.expression = expr
                                    #remove variables 
                                    if copy_over: 
                                        try: 
                                            for var in current_driver.driver.variables: 
                                                current_driver.driver.variables.remove(var)
                                        except:
                                            pass
                                    var = current_driver.driver.variables.new()
                                    var.name = var_name
                                    var.type = var_type
                                    var.targets[0].id = target_id
                                    var.targets[0].data_path = target_data
                                    i = i + 1

def reset_stretch_constraint(type = None):
    """
    Reset Stretch To Constraints for selected bones
    """
    
    if bpy.context.active_object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')
    if type == 'ALL':
        for bone in bpy.context.object.pose.bones:
            try:
                for constraint in bone.constraints:
                    if constraint.type == "STRETCH_TO":
                        constraint.rest_length = 0
            except AttributeError:
                pass #no constraints          
    else:
        for bone in bpy.context.selected_pose_bones:
            try:
                for constraint in bone.constraints:
                    if constraint.type == "STRETCH_TO":
                        constraint.rest_length = 0
            except AttributeError: 
                pass #no constraints

def change_stretch_volume(input, type = None):
    """
    Change Stretch To Volume
    """
    
    if bpy.context.active_object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')
    if type == 'ALL':
        for bone in bpy.context.object.pose.bones:
            try:
                for constraint in bone.constraints:
                    if constraint.type == 'STRETCH_TO':
                        constraint.volume = input
            except AttributeError:
                pass #no constraints
    else:
        for bone in bpy.context.selected_pose_bones:    
            try:
                for constraint in bone.constraints:
                    if constraint.type == 'STRETCH_TO':
                        constraint.volume = input
            except AttributeError:
                pass #no constraints 
                
