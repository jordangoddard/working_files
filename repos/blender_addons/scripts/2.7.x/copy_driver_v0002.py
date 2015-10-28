

import bpy
import re


###CHANGE SETTINGS HERE####

amt = "rig.ted" #Armature Name
copy_bone = "acc.lips_top.C" #Bone to be coppied 
acc_driver = "none" #Driver Bone if in the same layer

############################


def CopyDriver():
    
    #Determines The Driver Details
	    
    for copy_action in bpy.data.objects[amt].pose.bones[copy_bone].constraints:
        
        action = copy_action.name
        
        b = None
	
        for current_driver in bpy.data.objects[amt].animation_data.drivers:
                    
            path = current_driver.data_path
            driver_bone = re.match('pose\.bones\[\"(\S+)\"\]\.constraints\[\"(\S+)\"\]\.influence', path)
            
            if driver_bone:
                driver_bone_name = driver_bone.group(1)
                action_name = driver_bone.group(2)
            	
                if (driver_bone_name==copy_bone) and (action_name==action):
                    
                    print("match")    
                        
                    b = current_driver.driver
                    exp = b.expression #driver expression  
					
                    break 
					    
            else:
                print("no match")
    
	
	
        i = 0
        run = True
		
        while run: 
			
            print("it's in")
            
            try:
                b.variables[i]
                print("in range")
                
            except:
                print("out of range")
                run = False
			
            if run == True:	
            
                var = b.variables[i]
                var_name = var.name  #variable name
                var_type = var.type	#variable name
                target = var.targets[0]
                target_id = target.id #target object
                target_data = target.data_path	#target data_path			
        	
                for visible_bone in bpy.context.visible_pose_bones:
    			
                    bone = bpy.data.armatures[amt].bones[visible_bone.name]
    				
                    if bone.name == acc_driver: 
    					#THIS IS THE DRIVER, DO NOTHING
                        print("nothing")
    					
                    elif bone.name == copy_bone:
    		 
                        bone.select = False
    					
                    else: 
    				  
                        #Select Bone
                        bone.select = True
    					
                        bone_name = bone.name
    					
                        #Create Driver for influence
    				
                        constraint = "pose.bones[\"" + bone_name + "\"].constraints[\"" + action + "\"].influence"
    					
                        try:
                            bpy.context.object.driver_add(constraint).driver
    						
                        except:
                            print("No such constraint")
    					
    		  
    					#Determine the corresponding driver
                        for current_driver in bpy.data.objects[amt].animation_data.drivers:
    						
                            path = current_driver.data_path
                            driver_bone = re.match('pose\.bones\[\"(\S+)\"\]\.constraints\[\"(\S+)\"\]\.influence', path)
    						
                            if driver_bone:
    							
                                driver_bone_name = driver_bone.group(1)
                                action_name = driver_bone.group(2)
    		
                                if driver_bone_name == bone_name and action_name== action:
    								
                                    print("match")
    								
    								#Add new variable for driver
                                    current_driver.driver.expression = exp
    			
                                    var = current_driver.driver.variables.new()
    								
                                    var.name = var_name
                                    var.type = var_type
                                    var.targets[0].id = target_id
                                    var.targets[0].data_path = target_data

                                    i = i + 1

                            else: 
                                print("no match")
    								
    								
    					#Deselect Bone
                        bone.select = False
            
				
    
def DeselectAllBones():
	
	for visible_bone in bpy.context.visible_pose_bones:
    	
		bone = bpy.data.armatures[amt].bones[visible_bone.name]
		bone.select = False
		
			
    
#RUN HERE
DeselectAllBones()
CopyDriver()

