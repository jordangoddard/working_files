import bpy
import re



###SETTINGS####

amt = "rig.ted" #Armature Name
acc_driver = "none" #Driver Bone

def CopyDriver():
    
    
    #Determines The Driver Details
	
    copy_bone = "acc.lips_top.C" #Name of bone to be copied
    
    for copy_action in bpy.data.objects[amt].pose.bones[copy_bone].constraints:
        
        action = copy_action.name
	
        for current_driver in bpy.data.objects[amt].animation_data.drivers:
                    
            path = current_driver.data_path
            driver_bone = re.match('pose\.bones\[\"(\S+)\"\]\.constraints\[\"(\S+)\"\]\.influence', path)
            
            if driver_bone:
                driver_bone_name = driver_bone.group(1)
                action_name = driver_bone.group(2)
            	
                if (driver_bone_name==copy_bone) and (action_name==action):
                    
                    print("match")    
                        
                    b = current_driver.driver
        			
                    exp = b.expression        
        		
                    var = b.variables[0]
                    var_name = var.name  
                    var_type = var.type

                    target = var.targets[0]
                    target_id = target.id
                    target_data = target.data_path
                    
            else:
                print("no match")
                 
    					
    	
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
                bpy.context.object.driver_add(constraint).driver
                
      
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

                        else: 
                            print("no match")
                            
                        
    					
    		    #Deselect Bone
                bone.select = False
    
    
    
#RUN HERE
CopyDriver()

