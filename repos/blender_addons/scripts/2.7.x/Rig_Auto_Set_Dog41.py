import bpy 
import math 
import mathutils

##########################################################################################
### Once script is run you will have to do fix the directional mch bone layer (blue).  ###
### Select the Left leg and leg arm and change roll to positive X Global.              ###
### This should fix any issues with the bone roll.                                     ###
##########################################################################################

############################################################################################
### clt.lowerJaw.C has to be moved into the correct place before starting script.        ###
### mch.jaw_hinge.C has to be moved into the correct place before starting the script    ###
############################################################################################



####################
## Move Functions ##
####################

#Get the name of the rig
sceneRig = bpy.context.selected_objects 
#change rig to edit mode
bpy.ops.object.mode_set(mode='EDIT')

print(sceneRig[0])


## Bone Main Move ## 
def moveBoneBasic(characterRig, defBone, auxBone):
    
    #find out def bone location
    try:
        h = characterRig.data.edit_bones[defBone].head.xyz
        t = characterRig.data.edit_bones[defBone].tail.xyz
        #print("%s has been found successfully" % defBone)
        
    except: 
        print("%s could not be found" % (defBone)) 
              
     # Match location of new bone to def bone 
    try:        
        characterRig.data.edit_bones[auxBone].head.xyz = h
        characterRig.data.edit_bones[auxBone].tail.xyz = t
        #print("%s has been moved successfully" % auxBone)
    except: 
        print("%s could not be found" % (auxBone))
    
    #Fixes the role of bones that are the same     
    try: 
        r = characterRig.data.edit_bones[defBone].roll
        print(r) 
        characterRig.data.edit_bones[auxBone].roll = r    
    except: 
        print("%s did not roll" % (auxBone))     
    
## Bone Move Two Bones ## 
def moveBoneTwoBoneBasic(characterRig, defBone_1, defBone_2, auxBone):
    
    #find out def bone location
    try:
        h = characterRig.data.edit_bones[defBone_1].head.xyz
        t = characterRig.data.edit_bones[defBone_2].head.xyz
        #print("%s has been found successfully" % defBone_1)
        #print("%s has been found successfully" % defBone_2)
        
    except: 
        print("%s could not be found" % (defBone)) 
              
     # Match location of new bone to def bone 
    try:        
        characterRig.data.edit_bones[auxBone].head.xyz = h
        characterRig.data.edit_bones[auxBone].tail.xyz = t
        #print("%s has been moved successfully" % auxBone)
    except: 
        print("%s could not be found" % (auxBone))    
          
## Bone Main Center ## 
def moveBoneCenter(characterRig, defBone, auxBone):
    
    #find out def bone location with center
    try:
        h1 = characterRig.data.edit_bones[defBone].head.xyz
        h2 = characterRig.data.edit_bones[defBone].center.xyz
        #print("%s has been found successfully" % defBone)
    except: 
        print("%s could not be found" % (defBone)) 
              
     # Match location of new bone to def bone 
    try:        
        characterRig.data.edit_bones[auxBone].head.xyz = h1
        characterRig.data.edit_bones[auxBone].tail.xyz = h2
        #print("%s has been moved successfully" % auxBone)
    except: 
        print("%s could not be found" % (auxBone))
                    

## Bone Control Move Global XYZ ##    
def moveBoneConXYZ(characterRig, defBone, auxBone, headTail, XYZ, conSize):
    
    #find location of def bone head
    try: 
        h = characterRig.data.edit_bones[defBone].head.xyz
        t = characterRig.data.edit_bones[defBone].tail.xyz
        #print("%s has been found successfully" % defBone)
    except: 
        print("%s could not be found" % (defBone)) 
    
    #Move control bone to new location with a new length
    try:
        if headTail == 'head':
            characterRig.data.edit_bones[auxBone].head = h
            characterRig.data.edit_bones[auxBone].tail = h
            if XYZ == "Y":              
                characterRig.data.edit_bones[auxBone].tail.y += conSize 
            elif XYZ == "Z":
                characterRig.data.edit_bones[auxBone].tail.z += conSize 
            else:
                characterRig.data.edit_bones[auxBone].tail.x += conSize             
            #print("%s has been moved successfully" % auxBone)
        else: 
            characterRig.data.edit_bones[auxBone].head = t
            characterRig.data.edit_bones[auxBone].tail = t
            if XYZ == "Y":
                
                characterRig.data.edit_bones[auxBone].tail.y += conSize 
            elif XYZ == "Z":
                characterRig.data.edit_bones[auxBone].tail.z += conSize 
            else:
                characterRig.data.edit_bones[auxBone].tail.x += conSize             
            #print("%s has been moved successfully" % auxBone)
    except: 
        print("%s could not be found" % (auxBone))

## Bone Move Exact ##       
def moveBoneExt(characterRig, defBone, auxBone, bonePos, locTail, locHead):
    
    #find location of def bone head
    try: 
        h = characterRig.data.edit_bones[defBone].head.xyz
        t = characterRig.data.edit_bones[defBone].tail.xyz
        #print("%s has been found successfully" % defBone)
    except: 
        print("%s could not be found" % (defBone)) 
    
    #Move control bone to new location with a new length
      
    try:
        if bonePos == 'head':
            characterRig.data.edit_bones[auxBone].head = h
            characterRig.data.edit_bones[auxBone].tail = t
            characterRig.data.edit_bones[auxBone].tail.xyz += mathutils.Vector(locTail)
            characterRig.data.edit_bones[auxBone].head.xyz += mathutils.Vector(locHead)
            #print("%s has been moved successfully" % auxBone)
        elif bonePos == 'tail':
            characterRig.data.edit_bones[auxBone].head = t
            characterRig.data.edit_bones[auxBone].tail = h
            characterRig.data.edit_bones[auxBone].tail.xyz += mathutils.Vector(locTail)
            characterRig.data.edit_bones[auxBone].head.xyz += mathutils.Vector(locHead)
            #print("%s has been moved successfully" % auxBone)
        elif bonePos == 'custom': 
            print("custom")
            characterRig.data.edit_bones[auxBone].head = h
            characterRig.data.edit_bones[auxBone].tail = t
            characterRig.data.edit_bones[auxBone].head.z -= characterRig.data.edit_bones[auxBone].head.z
        elif bonePos == 'headMain':
            characterRig.data.edit_bones[auxBone].head = h    
        elif bonePos == 'eye':
             characterRig.data.edit_bones[auxBone].head.x -= characterRig.data.edit_bones[auxBone].head.x   
             characterRig.data.edit_bones[auxBone].tail.x -= characterRig.data.edit_bones[auxBone].tail.x   
        #else: 
            #print("Nothing happened for this bone, make sure you entered a value.")
            
            
    except: 
        print("%s could not be found" % (auxBone))

## This will move the initial IK Control bone. The screen will redraw and all other IK related bones will use the simple move to this point ## 
def moveBoneIKCon(characterRig, defBone_1, defBone_2, conIK):
    
    #find location of def bones top
    try:
        h = characterRig.data.edit_bones[defBone_1].head.xyz
        t = characterRig.data.edit_bones[defBone_2].tail.xyz
        a = (h[0] + t[0])/2
        b = (h[1] + t[1])/2
        c = (h[2] + t[2])/2
        nh = mathutils.Vector((a, b, c))
        d = (nh[0] + t[0])/2
        e = (nh[1] + t[1])/2
        f = (nh[2] + t[2])/2
        nt = mathutils.Vector((d, e, f))
        #print("%s and %s has found center successfully" % (defBone_1, defBone_2))
    except: 
        print("%s or %s were missing" % (defBone_1, defBone_2)) 
      
    try:    
        characterRig.data.edit_bones[conIK].head = nh   
        characterRig.data.edit_bones[conIK].tail = nt
        #print("%s has been moved successfully" % conIK)
    except: 
        print("%s could not be found" % (conIK))   

## This will make a bone (control) a little bigger than the def bone
def moveBoneScale(characterRig, defBone, auxBone, mul):
    
    #find location of def bones top
    try:
        h = characterRig.data.edit_bones[defBone].head.xyz
        print(h)
        t = characterRig.data.edit_bones[defBone].tail.xyz
        print(t)
        a = (t[0] - h[0]) * mul + t[0]
        b = (t[1] - h[1]) * mul + t[1]
        c = (t[2] - h[2]) * mul + t[2]
        nt = mathutils.Vector((a, b, c))
        print(nt)
        #print("%s has found scale successfully" % (defBone))
    except: 
        print("%s were missing" % (defBone)) 
      
    try:    
        characterRig.data.edit_bones[auxBone].head = h
        characterRig.data.edit_bones[auxBone].tail = nt
        #print("%s has been moved successfully" % auxBone)
    except: 
        print("%s could not be found" % (auxBone))      
        
    #Fixes the roll of bones that are the same.         
    try: 
        r = characterRig.data.edit_bones[defBone].roll
        print(r) 
        characterRig.data.edit_bones[auxBone].roll = r    
    except: 
        print("%s did not roll" % (auxBone))     
 

##########
## Body ##
##########

###############
## Mch Bones ##
###############

## Tail Mch Bones ## 
moveBoneBasic(sceneRig[0], "def.tail_01.C", "mch.tail_01.C")
moveBoneBasic(sceneRig[0], "def.tail_02.C", "mch.tail_02.C")
moveBoneBasic(sceneRig[0], "def.tail_03.C", "mch.tail_03.C")
moveBoneBasic(sceneRig[0], "def.tail_04.C", "mch.tail_04.C")
moveBoneBasic(sceneRig[0], "def.tail_05.C", "mch.tail_05.C")

## Spine Mch Bones ##
moveBoneConXYZ(sceneRig[0], "def.spine.C", "mch.spine.C", "head", "Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_01.C", "mch.spine_01.C", "head","Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.pivot", "head", "Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.spine_02_b.C", "head", "Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.spine_02_a.C", "head", "Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_03.C", "mch.spine_03.C", "head", "Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_04.C", "mch.spine_04.C", "head", "Z", 0.1)
moveBoneTwoBoneBasic(sceneRig[0], "def.spine_04.C", "def.head.C", "mch.neck_stretch")
moveBoneBasic(sceneRig[0], "def.spine_03.C", "wgt.chest_01.C")
moveBoneConXYZ(sceneRig[0], "def.head.C", "mch.head_orient.C", "head", "Y", 0.1)
moveBoneBasic(sceneRig[0], "def.head.C", "mch.head.C")

## Ear Mch Left ## 
moveBoneBasic(sceneRig[0], "def.ear_00.L", "ear_base_offset.L")
moveBoneBasic(sceneRig[0], "def.ear_01.L", "mch.ear_01.L")
moveBoneBasic(sceneRig[0], "def.ear_02.L", "mch.ear_02.L")
moveBoneBasic(sceneRig[0], "def.ear_03.L", "mch.ear_03.L")
moveBoneBasic(sceneRig[0], "def.ear_04.L", "mch.ear_04.L")

## Ear Mch Righ ## 
moveBoneBasic(sceneRig[0], "def.ear_00.R", "ear_base_offset.R")
moveBoneBasic(sceneRig[0], "def.ear_01.R", "mch.ear_01.R")
moveBoneBasic(sceneRig[0], "def.ear_02.R", "mch.ear_02.R")
moveBoneBasic(sceneRig[0], "def.ear_03.R", "mch.ear_03.R")
moveBoneBasic(sceneRig[0], "def.ear_04.R", "mch.ear_04.R")

## Leg Mch Left ## 
moveBoneBasic(sceneRig[0], "def.upperLeg_01.L", "mch.upperLeg_01.L")
moveBoneBasic(sceneRig[0], "def.lowerLeg_01.L", "mch.lowerLeg_01.L")
moveBoneBasic(sceneRig[0], "def.lowerLeg_02.L", "mch.lowerLeg_02.L")
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.ankle_position.L", "head", "Y", -0.08)

## Leg Mch Right ## 
moveBoneBasic(sceneRig[0], "def.upperLeg_01.R", "mch.upperLeg_01.R")
moveBoneBasic(sceneRig[0], "def.lowerLeg_01.R", "mch.lowerLeg_01.R")
moveBoneBasic(sceneRig[0], "def.lowerLeg_02.R", "mch.lowerLeg_02.R")
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.ankle_position.R", "head", "Y", -0.08)

## Foot Mch Left ##
moveBoneBasic(sceneRig[0], "def.toe_pinky_01.L", "mch.toe_pinky_01.L")
moveBoneBasic(sceneRig[0], "def.toe_pinky_02.L", "mch.toe_pinky_02.L")
moveBoneBasic(sceneRig[0], "def.toe_ring_01.L", "mch.toe_ring_01.L")
moveBoneBasic(sceneRig[0], "def.toe_ring_02.L", "mch.toe_ring_02.L")
moveBoneBasic(sceneRig[0], "def.toe_index_01.L", "mch.toe_index_01.L")
moveBoneBasic(sceneRig[0], "def.toe_index_02.L", "mch.toe_index_02.L")
moveBoneBasic(sceneRig[0], "def.toe_thumb_01.L", "mch.toe_thumb_01.L")
moveBoneBasic(sceneRig[0], "def.toe_thumb_02.L", "mch.toe_thumb_02.L")
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.foot.L", "tail", "Y", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.foot_IKLock_world.L", "tail", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.paw_back.L", "tail", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.foot_IKLock_hips.L", "tail", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_toes_horizontal.L", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_toes_vertical.L", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_toes_center.L", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_foot.L", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_rel.L", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_heel_horizontal.L", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.reverse_ankle_pivot_heel_vertical.L", "tail", "Z", -0.04)

## Foot Mch Right ##
moveBoneBasic(sceneRig[0], "def.toe_pinky_01.R", "mch.toe_pinky_01.R")
moveBoneBasic(sceneRig[0], "def.toe_pinky_02.R", "mch.toe_pinky_02.R")
moveBoneBasic(sceneRig[0], "def.toe_ring_01.R", "mch.toe_ring_01.R")
moveBoneBasic(sceneRig[0], "def.toe_ring_02.R", "mch.toe_ring_02.R")
moveBoneBasic(sceneRig[0], "def.toe_index_01.R", "mch.toe_index_01.R")
moveBoneBasic(sceneRig[0], "def.toe_index_02.R", "mch.toe_index_02.R")
moveBoneBasic(sceneRig[0], "def.toe_thumb_01.R", "mch.toe_thumb_01.R")
moveBoneBasic(sceneRig[0], "def.toe_thumb_02.R", "mch.toe_thumb_02.R")
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.foot.R", "tail", "Y", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.foot_IKLock_world.R", "tail", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.paw_back.R", "tail", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.foot_IKLock_hips.R", "tail", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_toes_horizontal.R", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_toes_vertical.R", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_toes_center.R", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_foot.R", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_rel.R", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_heel_horizontal.R", "tail", "Z", -0.04)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.reverse_ankle_pivot_heel_vertical.R", "tail", "Z", -0.04)

## Arm Mch Left ## 
moveBoneBasic(sceneRig[0], "def.upperArm_01.L", "mch.upperArm_01.L")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.L", "mch.lowerArm_01.L")

## Arm Mch Right ## 
moveBoneBasic(sceneRig[0], "def.upperArm_01.R", "mch.upperArm_01.R")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.R", "mch.lowerArm_01.R")

## Hand Mch Left ## 
moveBoneBasic(sceneRig[0], "def.finger_pinky_01.L", "mch.finger_pinky_01.L")
moveBoneBasic(sceneRig[0], "def.finger_pinky_02.L", "mch.finger_pinky_02.L")
moveBoneBasic(sceneRig[0], "def.finger_ring_01.L", "mch.finger_ring_01.L")
moveBoneBasic(sceneRig[0], "def.finger_ring_02.L", "mch.finger_ring_02.L")
moveBoneBasic(sceneRig[0], "def.finger_index_01.L", "mch.finger_index_01.L")
moveBoneBasic(sceneRig[0], "def.finger_index_02.L", "mch.finger_index_02.L")
moveBoneBasic(sceneRig[0], "def.finger_thumb_01.L", "mch.finger_thumb_01.L")
moveBoneBasic(sceneRig[0], "def.finger_thumb_02.L", "mch.finger_thumb_02.L")
moveBoneConXYZ(sceneRig[0], "def.hand.L", "mch.sdk_paw_front_pivot_center.L", "tail", "Z", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "mch.hand_IKLock_head.L", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "mch.hand_IKLock_chest.L", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "mch.hand_IKLock_hips.L", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "mch.hand_IKLock_world.L", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "mch.paw_front.L", "tail", "Y", -0.075)
moveBoneBasic(sceneRig[0], "def.wrist.L", "mch.hand.L")
moveBoneBasic(sceneRig[0], "def.wrist.L", "mch.wrist.L")

## Hand Mch Right ## 
moveBoneBasic(sceneRig[0], "def.finger_pinky_01.R", "mch.finger_pinky_01.R")
moveBoneBasic(sceneRig[0], "def.finger_pinky_02.R", "mch.finger_pinky_02.R")
moveBoneBasic(sceneRig[0], "def.finger_ring_01.R", "mch.finger_ring_01.R")
moveBoneBasic(sceneRig[0], "def.finger_ring_02.R", "mch.finger_ring_02.R")
moveBoneBasic(sceneRig[0], "def.finger_index_01.R", "mch.finger_index_01.R")
moveBoneBasic(sceneRig[0], "def.finger_index_02.R", "mch.finger_index_02.R")
moveBoneBasic(sceneRig[0], "def.finger_thumb_01.R", "mch.finger_thumb_01.R")
moveBoneBasic(sceneRig[0], "def.finger_thumb_02.R", "mch.finger_thumb_02.R")
moveBoneConXYZ(sceneRig[0], "def.hand.R", "mch.sdk_paw_front_pivot_center.R", "tail", "Z", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "mch.hand_IKLock_head.R", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "mch.hand_IKLock_chest.R", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "mch.hand_IKLock_hips.R", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "mch.hand_IKLock_world.R", "tail", "Y", -0.075)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "mch.paw_front.R", "tail", "Y", -0.075)
moveBoneBasic(sceneRig[0], "def.wrist.R", "mch.hand.R")
moveBoneBasic(sceneRig[0], "def.wrist.R", "mch.wrist.R")

###############
## Ctl Bones ##
###############

## Tail Ctl Bones ## 
moveBoneBasic(sceneRig[0], "def.tail_01.C", "ctl.tail_01.C")
moveBoneBasic(sceneRig[0], "def.tail_02.C", "ctl.tail_02.C")
moveBoneBasic(sceneRig[0], "def.tail_03.C", "ctl.tail_03.C")
moveBoneBasic(sceneRig[0], "def.tail_04.C", "ctl.tail_04.C")
moveBoneBasic(sceneRig[0], "def.tail_05.C", "ctl.tail_05.C")
moveBoneExt(sceneRig[0], "def.tail_05.C", "ctl.body_config.C", "tail", [0.0, 0.1, -0.1], [0.0, 0.1, -0.1]) 

## Spine Ctl Bones ## 
moveBoneBasic(sceneRig[0], "def.spine.C", "ctl.hips_02.C")
moveBoneConXYZ(sceneRig[0], "def.spine.C", "ctl.root.C", "tail", "Z", 0.4)
moveBoneScale(sceneRig[0], "def.spine_01.C", "ctl.spine_01.C", .3   )
moveBoneCenter(sceneRig[0], "def.spine_02.C", "ctl.spine_02.C")
moveBoneConXYZ(sceneRig[0], "def.spine_01.C", "ctl.hips_01.C", "tail", "Z", 0.3)
moveBoneConXYZ(sceneRig[0], "def.spine_01.C", "ctl.chest_01.C", "tail", "Z", 0.2)
moveBoneCenter(sceneRig[0], "def.spine_03.C", "ctl.chest_02.C")
moveBoneCenter(sceneRig[0], "def.spine_04.C", "ctl.spine_04.C")
moveBoneCenter(sceneRig[0], "def.spine_05.C", "ctl.spine_05.C")
moveBoneTwoBoneBasic(sceneRig[0], "def.spine_04.C", "def.head.C", "ctl.neck.C")
moveBoneCenter(sceneRig[0], "def.head.C", "ctl.head.C")
moveBoneConXYZ(sceneRig[0], "ctl.root.C", "ctl.body.C", "head", "Y", .8 )
moveBoneExt(sceneRig[0], "ctl.body.C", "ctl.body.C", "head", [0.0, -0.1, -0.1], [0.0, -0.1, -0.1]) 

## Ears Ctl Bones Left ## 
moveBoneConXYZ(sceneRig[0], "def.ear_00.L", "ctl.ear_base.L", "head", "Z", 0.03)
moveBoneBasic(sceneRig[0], "def.ear_01.L", "ctl.ear_01.L")
moveBoneBasic(sceneRig[0], "def.ear_02.L", "ctl.ear_02.L")
moveBoneBasic(sceneRig[0], "def.ear_03.L", "ctl.ear_03.L")
moveBoneBasic(sceneRig[0], "def.ear_04.L", "ctl.ear_04.L")

## Ears Ctl Bones Right ## 
moveBoneConXYZ(sceneRig[0], "def.ear_00.R", "ctl.ear_base.R", "head", "Z", 0.03)
moveBoneBasic(sceneRig[0], "def.ear_01.R", "ctl.ear_01.R")
moveBoneBasic(sceneRig[0], "def.ear_02.R", "ctl.ear_02.R")
moveBoneBasic(sceneRig[0], "def.ear_03.R", "ctl.ear_03.R")
moveBoneBasic(sceneRig[0], "def.ear_04.R", "ctl.ear_04.R")

## Chest Controls ##
moveBoneBasic(sceneRig[0], "def.chest_mass_01.C", "ctl.chest_mass_01.C")
moveBoneBasic(sceneRig[0], "def.chest_mass_02.C", "ctl.chest_mass_02.C")

## Leg Ctl Bones Left ##
moveBoneBasic(sceneRig[0], "def.upperLeg_01.L", "ctl.upperLeg_01.L")
moveBoneBasic(sceneRig[0], "def.upperLeg_02.L", "ctl.upperLeg_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.L", "def.lowerLeg_01.L", "ctl.thigh.L")
moveBoneBasic(sceneRig[0], "def.lowerLeg_01.L", "ctl.lowerLeg_01.L")
moveBoneBasic(sceneRig[0], "def.lowerLeg_02.L", "ctl.lowerLeg_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.L", "def.ankle.L", "ctl.knee_ik_stretch.L")
moveBoneCenter(sceneRig[0], "def.ankle.L", "ctl.ankle_ik_stretch.L")

## Foot Ctl Bones Left ##
moveBoneBasic(sceneRig[0], "def.toe_pinky_01.L", "ctl.toe_pinky_01.L")
moveBoneBasic(sceneRig[0], "def.toe_pinky_02.L", "ctl.toe_pinky_02.L")
moveBoneBasic(sceneRig[0], "def.toe_ring_01.L", "ctl.toe_ring_01.L")
moveBoneBasic(sceneRig[0], "def.toe_ring_02.L", "ctl.toe_ring_02.L")
moveBoneBasic(sceneRig[0], "def.toe_index_01.L", "ctl.toe_index_01.L")
moveBoneBasic(sceneRig[0], "def.toe_index_02.L", "ctl.toe_index_02.L")
moveBoneBasic(sceneRig[0], "def.toe_thumb_01.L", "ctl.toe_thumb_01.L")
moveBoneBasic(sceneRig[0], "def.toe_thumb_02.L", "ctl.toe_thumb_02.L")
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "ctl.reverse_ankle.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "ctl.foot_pivot.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "ctl.paw_back.R", "tail", "Y", -0.15)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "ctl.foot.R", "tail", "Y", -0.08)
moveBoneExt(sceneRig[0], "mch.toes.R", "ctl.leg_config.R", "head", [0.0, 0.1, -0.02], [0.0, 0.1, -0.02])
moveBoneIKCon(sceneRig[0], "def.upperLeg_01.R", "def.ankle.R", "ctl.leg_pole.R")

## Leg Ctl Bones Right ## 
moveBoneBasic(sceneRig[0], "def.upperLeg_01.R", "ctl.upperLeg_01.R")
moveBoneBasic(sceneRig[0], "def.upperLeg_02.R", "ctl.upperLeg_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.R", "def.lowerLeg_01.R", "ctl.thigh.R")
moveBoneBasic(sceneRig[0], "def.lowerLeg_01.R", "ctl.lowerLeg_01.R")
moveBoneBasic(sceneRig[0], "def.lowerLeg_02.R", "ctl.lowerLeg_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.R", "def.ankle.R", "ctl.knee_ik_stretch.R")
moveBoneCenter(sceneRig[0], "def.ankle.R", "ctl.ankle_ik_stretch.R")

## Foot Ctl Bones Right ##
moveBoneBasic(sceneRig[0], "def.toe_pinky_01.R", "ctl.toe_pinky_01.R")
moveBoneBasic(sceneRig[0], "def.toe_pinky_02.R", "ctl.toe_pinky_02.R")
moveBoneBasic(sceneRig[0], "def.toe_ring_01.R", "ctl.toe_ring_01.R")
moveBoneBasic(sceneRig[0], "def.toe_ring_02.R", "ctl.toe_ring_02.R")
moveBoneBasic(sceneRig[0], "def.toe_index_01.R", "ctl.toe_index_01.R")
moveBoneBasic(sceneRig[0], "def.toe_index_02.R", "ctl.toe_index_02.R")
moveBoneBasic(sceneRig[0], "def.toe_thumb_01.R", "ctl.toe_thumb_01.R")
moveBoneBasic(sceneRig[0], "def.toe_thumb_02.R", "ctl.toe_thumb_02.R")
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "ctl.reverse_ankle.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "ctl.foot_pivot.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "ctl.paw_back.L", "tail", "Y", -0.15)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "ctl.foot.L", "tail", "Y", -0.08)
moveBoneExt(sceneRig[0], "mch.toes.L", "ctl.leg_config.L", "head", [0.0, 0.1, -0.02], [0.0, 0.1, -0.02])
moveBoneIKCon(sceneRig[0], "def.upperLeg_01.L", "def.ankle.L", "ctl.leg_pole.L")

## Arm Ctl Bones Left ## 
moveBoneBasic(sceneRig[0], "def.scapula.L", "ctl.scapula.L")
moveBoneBasic(sceneRig[0], "def.upperArm_01.L", "ctl.upperArm_01.L")
moveBoneBasic(sceneRig[0], "def.upperArm_02.L", "ctl.upperArm_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.L", "def.lowerArm_01.L", "ctl.shoulder.L")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.L", "ctl.lowerArm_01.L")
moveBoneScale(sceneRig[0], "def.lowerArm_01.L", "ctl.elbow_ik_stretch.L", .5)
moveBoneBasic(sceneRig[0], "def.lowerArm_02.L", "ctl.lowerArm_02.L")
moveBoneConXYZ(sceneRig[0], "def.wrist.L", "ctl.paw_front.L", "head", "Y", -0.17)
moveBoneConXYZ(sceneRig[0], "def.wrist.L", "ctl.reverse_wrist.L", "tail", "Z", -0.03)
moveBoneConXYZ(sceneRig[0], "def.wrist.L", "ctl.hand_pivot.L", "tail", "Z", -0.02)
moveBoneBasic(sceneRig[0], "def.wrist.L", "ctl.wrist.L")
moveBoneConXYZ(sceneRig[0], "def.wrist.L", "ctl.hand.L", "tail", "Y", -0.1)
moveBoneIKCon(sceneRig[0], "def.upperArm_01.L", "def.lowerArm_02.L", "ctl.arm_pole.L")

## Hand Ctl Bones Left ## 
moveBoneBasic(sceneRig[0], "def.finger_pinky_01.L", "ctl.finger_pinky_01.L")
moveBoneBasic(sceneRig[0], "def.finger_pinky_02.L", "ctl.finger_pinky_02.L")
moveBoneBasic(sceneRig[0], "def.finger_ring_01.L", "ctl.finger_ring_01.L")
moveBoneBasic(sceneRig[0], "def.finger_ring_02.L", "ctl.finger_ring_02.L")
moveBoneBasic(sceneRig[0], "def.finger_index_01.L", "ctl.finger_index_01.L")
moveBoneBasic(sceneRig[0], "def.finger_index_02.L", "ctl.finger_index_02.L")
moveBoneBasic(sceneRig[0], "def.finger_thumb_01.L", "ctl.finger_thumb_01.L")
moveBoneBasic(sceneRig[0], "def.finger_thumb_02.L", "ctl.finger_thumb_02.L")
moveBoneConXYZ(sceneRig[0], "ctl.reverse_wrist.L", "ctl.paw_attach.L", "tail", "Y", -0.08)
moveBoneExt(sceneRig[0], "ctl.paw_attach.L", "ctl.arm_config.L", "head", [0.0, 0.1, 0.0], [0.0, 0.05, 0.0])

## Arm Ctl Bones Right ## 
moveBoneBasic(sceneRig[0], "def.scapula.R", "ctl.scapula.R")
moveBoneBasic(sceneRig[0], "def.upperArm_01.R", "ctl.upperArm_01.R")
moveBoneBasic(sceneRig[0], "def.upperArm_02.R", "ctl.upperArm_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.R", "def.lowerArm_01.R", "ctl.shoulder.R")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.R", "ctl.lowerArm_01.R")
moveBoneScale(sceneRig[0], "def.lowerArm_01.R", "ctl.elbow_ik_stretch.R", .5)
moveBoneBasic(sceneRig[0], "def.lowerArm_02.R", "ctl.lowerArm_02.R")
moveBoneConXYZ(sceneRig[0], "def.wrist.R", "ctl.paw_front.R", "head", "Y", -0.17)
moveBoneConXYZ(sceneRig[0], "def.wrist.R", "ctl.reverse_wrist.R", "tail", "Z", -0.03)
moveBoneConXYZ(sceneRig[0], "def.wrist.R", "ctl.hand_pivot.R", "tail", "Z", -0.02)
moveBoneBasic(sceneRig[0], "def.wrist.R", "ctl.wrist.R")
moveBoneConXYZ(sceneRig[0], "def.wrist.R", "ctl.hand.R", "tail", "Y", -0.1)
moveBoneIKCon(sceneRig[0], "def.upperArm_01.R", "def.lowerArm_02.R", "ctl.arm_pole.R")


## Hand Ctl Bones Right ## 
moveBoneBasic(sceneRig[0], "def.finger_pinky_01.R", "ctl.finger_pinky_01.R")
moveBoneBasic(sceneRig[0], "def.finger_pinky_02.R", "ctl.finger_pinky_02.R")
moveBoneBasic(sceneRig[0], "def.finger_ring_01.R", "ctl.finger_ring_01.R")
moveBoneBasic(sceneRig[0], "def.finger_ring_02.R", "ctl.finger_ring_02.R")
moveBoneBasic(sceneRig[0], "def.finger_index_01.R", "ctl.finger_index_01.R")
moveBoneBasic(sceneRig[0], "def.finger_index_02.R", "ctl.finger_index_02.R")
moveBoneBasic(sceneRig[0], "def.finger_thumb_01.R", "ctl.finger_thumb_01.R")
moveBoneBasic(sceneRig[0], "def.finger_thumb_02.R", "ctl.finger_thumb_02.R")
moveBoneConXYZ(sceneRig[0], "ctl.reverse_wrist.R", "ctl.paw_attach.R", "tail", "Y", -0.08)
moveBoneExt(sceneRig[0], "ctl.paw_attach.R", "ctl.arm_config.R", "head", [0.0, 0.1, 0.0], [0.0, 0.05, 0.0])

##############
## IK Bones ##
##############

## Leg IK Bones Left ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.L", "def.lowerLeg_01.L", "mch.upperLeg_twist_ik.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.L", "def.lowerLeg_01.L", "mch.upperLeg_ik_stretch.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.L", "def.lowerLeg_01.L", "ikk.upperLeg.L")
moveBoneConXYZ(sceneRig[0], "def.upperLeg_02.L", "mch.upperLeg_twist.L", "tail", "Y", -0.04)
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.L", "def.ankle.L", "ikk.lowerLeg.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.L", "def.ankle.L", "mch.knee_ik_stretch.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.L", "def.ankle.L", "mch.lowerLeg_ik_stretch.L")
moveBoneConXYZ(sceneRig[0], "def.lowerLeg_02.L", "ikh.leg.L", "tail", "Y", -0.05)
moveBoneConXYZ(sceneRig[0], "def.lowerLeg_02.L", "ikk.leg_end.L", "tail", "Y", -0.02)
moveBoneBasic(sceneRig[0], "def.ankle.L", "mch.ankle_ik_stretch.L")
moveBoneBasic(sceneRig[0], "def.ankle.L", "ikk.ankle.L")

## Foot IK Bones Left ## 
moveBoneBasic(sceneRig[0], "def.foot.L", "ikk.foot.L")
moveBoneBasic(sceneRig[0], "def.ankle.L", "ikk.ankle.L")
moveBoneConXYZ(sceneRig[0], "mch.toes.L", "ikk.heel_back.L", "tail", "Y", 0.105)
moveBoneConXYZ(sceneRig[0], "mch.toes.L", "ikh.toes.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "ikk.heel_back.L", "ikh.heel_back.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.foot.L", "mch.sdk_paw_back_pivot_center.L", "tail", "Z", -0.035)
moveBoneConXYZ(sceneRig[0], "def.foot.L", "ikh.foot.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.foot.L", "mch.sdk_ikh_foot.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.foot_pivot.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "ikh.ankle.L", "tail", "Z", -0.02)


## Foot IK Position Bones Left## 
moveBoneExt(sceneRig[0], "ikh.toes.L", "mch.sdk_ikh_toes_vertical.L", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_toes_vertical.L", "mch.sdk_ikh_toes_vertical.L", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_toes_vertical.L", "mch.sdk_ikh_toes_horizontal.L")

moveBoneExt(sceneRig[0], "ikh.ankle.L", "mch.sdk_ikh_heel_back_vertical.L", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_heel_back_vertical.L", "mch.sdk_ikh_heel_back_vertical.L", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_heel_back_vertical.L", "mch.sdk_ikh_heel_back_horizontal.L")

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_toes_vertical.L", "mch.sdk_ikh_heel_back_bank_posterior.L")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_back_bank_posterior.L", "mch.sdk_ikh_heel_back_bank_posterior.L", "head", [-0.04, 0.03, 0.0], [-0.04, 0.03, 0.0])

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_toes_vertical.L", "mch.sdk_ikh_heel_back_bank_interior.L")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_back_bank_interior.L", "mch.sdk_ikh_heel_back_bank_interior.L", "head", [0.04, 0.03, 0.0], [0.04, 0.03, 0.0])


## Leg IK Bones Right ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.R", "def.lowerLeg_01.R", "mch.upperLeg_twist_ik.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.R", "def.lowerLeg_01.R", "mch.upperLeg_ik_stretch.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_01.R", "def.lowerLeg_01.R", "ikk.upperLeg.R")
moveBoneConXYZ(sceneRig[0], "def.upperLeg_02.R", "mch.upperLeg_twist.R", "tail", "Y", -0.04)
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.R", "def.ankle.R", "ikk.lowerLeg.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.R", "def.ankle.R", "mch.knee_ik_stretch.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerLeg_01.R", "def.ankle.R", "mch.lowerLeg_ik_stretch.R")
moveBoneConXYZ(sceneRig[0], "def.lowerLeg_02.R", "ikh.leg.R", "tail", "Y", -0.05)
moveBoneConXYZ(sceneRig[0], "def.lowerLeg_02.R", "ikk.leg_end.R", "tail", "Y", -0.02)
moveBoneBasic(sceneRig[0], "def.ankle.R", "mch.ankle_ik_stretch.R")
moveBoneBasic(sceneRig[0], "def.ankle.R", "ikk.ankle.R")

## Foot IK Bones Right ## 
moveBoneBasic(sceneRig[0], "def.foot.R", "ikk.foot.R")
moveBoneBasic(sceneRig[0], "def.ankle.R", "ikk.ankle.R")
moveBoneConXYZ(sceneRig[0], "mch.toes.R", "ikk.heel_back.R", "tail", "Y", 0.105)
moveBoneConXYZ(sceneRig[0], "mch.toes.R", "ikh.toes.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "ikk.heel_back.R", "ikh.heel_back.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.foot.R", "mch.sdk_paw_back_pivot_center.R", "tail", "Z", -0.035)
moveBoneConXYZ(sceneRig[0], "def.foot.R", "ikh.foot.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.foot.R", "mch.sdk_ikh_foot.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.foot_pivot.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "ikh.ankle.R", "tail", "Z", -0.02)


## Foot IK Position Bones Right ## 
moveBoneExt(sceneRig[0], "ikh.toes.R", "mch.sdk_ikh_toes_vertical.R", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_toes_vertical.R", "mch.sdk_ikh_toes_vertical.R", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_toes_vertical.R", "mch.sdk_ikh_toes_horizontal.R")

moveBoneExt(sceneRig[0], "ikh.ankle.R", "mch.sdk_ikh_heel_back_vertical.R", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_heel_back_vertical.R", "mch.sdk_ikh_heel_back_vertical.R", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_heel_back_vertical.R", "mch.sdk_ikh_heel_back_horizontal.R")

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_toes_vertical.R", "mch.sdk_ikh_heel_back_bank_posterior.R")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_back_bank_posterior.R", "mch.sdk_ikh_heel_back_bank_posterior.R", "head", [-0.04, 0.03, 0.0], [-0.04, 0.03, 0.0])

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_toes_vertical.R", "mch.sdk_ikh_heel_back_bank_interior.R")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_back_bank_interior.R", "mch.sdk_ikh_heel_back_bank_interior.R", "head", [0.04, 0.03, 0.0], [0.04, 0.03, 0.0])

## Floating IK Position Leg Bones Left ## 
moveBoneConXYZ(sceneRig[0], "def.upperLeg_02.L", "thigh_rotate_pole.L", "tail", "Y", 0.05)
moveBoneExt(sceneRig[0], "thigh_rotate_pole.L", "thigh_rotate_pole.L", "head", [-0.00, 0.4, 0.0], [-0.00, 0.4, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.toes.L", "mch.ankle_ik_pole.L", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.ankle_ik_pole.L", "mch.ankle_ik_pole.L", "head", [-0.00, -0.3, 0.0], [-0.00, -0.3, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.toes.L", "mch.foot_ik_pole.L", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.foot_ik_pole.L", "mch.foot_ik_pole.L", "head", [-0.00, -0.3, 0.1], [-0.00, -0.3, 0.1])

moveBoneConXYZ(sceneRig[0], "mch.toes.L", "mch.toes_ik_pole.L", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.toes_ik_pole.L", "mch.toes_ik_pole.L", "head", [-0.00, -0.32, 0.1], [-0.00, -0.32, 0.1])

moveBoneScale(sceneRig[0], "ctl.leg_pole.L", "mch.leg_ik_pole.L", 4.5)
moveBoneConXYZ(sceneRig[0], "mch.leg_ik_pole.L", "mch.leg_ik_pole.L", "tail", "Y", -0.035)
moveBoneExt(sceneRig[0], "mch.leg_ik_pole.L", "mch.leg_ik_pole.L", "head", [-0.00, -0.8, 0.1], [-0.00, -0.8, 0.1])

## Floating IK Position Leg Bones Right ## 
moveBoneConXYZ(sceneRig[0], "def.upperLeg_02.R", "thigh_rotate_pole.R", "tail", "Y", 0.05)
moveBoneExt(sceneRig[0], "thigh_rotate_pole.R", "thigh_rotate_pole.R", "head", [-0.00, 0.4, 0.0], [-0.00, 0.4, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.toes.R", "mch.ankle_ik_pole.R", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.ankle_ik_pole.R", "mch.ankle_ik_pole.R", "head", [-0.00, -0.3, 0.0], [-0.00, -0.3, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.toes.R", "mch.foot_ik_pole.R", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.foot_ik_pole.R", "mch.foot_ik_pole.R", "head", [-0.00, -0.3, 0.1], [-0.00, -0.3, 0.1])

moveBoneConXYZ(sceneRig[0], "mch.toes.R", "mch.toes_ik_pole.R", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.toes_ik_pole.R", "mch.toes_ik_pole.R", "head", [-0.00, -0.32, 0.1], [-0.00, -0.32, 0.1])

moveBoneScale(sceneRig[0], "ctl.leg_pole.R", "mch.leg_ik_pole.R", 4.5)
moveBoneConXYZ(sceneRig[0], "mch.leg_ik_pole.R", "mch.leg_ik_pole.R", "tail", "Y", -0.035)
moveBoneExt(sceneRig[0], "mch.leg_ik_pole.R", "mch.leg_ik_pole.R", "head", [-0.00, -0.8, 0.1], [-0.00, -0.8, 0.1])

## Arm IK Bones Left ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.L", "def.lowerArm_01.L", "ikk.upperArm.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.L", "def.lowerArm_01.L", "mch.upperArm_ik_stretch.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.L", "def.lowerArm_01.L", "mch.upperArm_twist_ik.L")
moveBoneConXYZ(sceneRig[0], "def.upperArm_02.L", "mch.upperArm_twist.L", "tail", "Y", -0.05)
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_01.L", "def.wrist.L", "mch.elbow_ik_stretch.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_01.L", "def.wrist.L", "ikk.lowerArm.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_01.L", "def.wrist.L", "mch.lowerArm_ik_stretch.L")
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "ikh.arm.L", "tail", "Y", -0.05)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.L", "ikk.arm_end.L", "tail", "Y", -0.08)
moveBoneConXYZ(sceneRig[0], "def.wrist.L", "mch.sdk_ikh_wrist.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.wrist.L", "ikh.wrist.L", "tail", "Z", -0.02)

## Hand IK Bones Left ## 
moveBoneBasic(sceneRig[0], "def.wrist.L", "ikk.wrist.L")
moveBoneBasic(sceneRig[0], "def.hand.L", "ikk.hand.L")
moveBoneBasic(sceneRig[0], "mch.fingers.L", "ikk.fingers.L")
moveBoneConXYZ(sceneRig[0], "mch.fingers.L", "ikk.heel_front.L", "tail", "Y", 0.11)
moveBoneConXYZ(sceneRig[0], "mch.fingers.L", "ikh.fingers.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "ikk.heel_front.L", "ikh.heel_front.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.hand.L", "mch.sdk_ikh_hand.L", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.hand.L", "ikh.hand.L", "tail", "Z", -0.02)

## Arm IK Bones Right ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.R", "def.lowerArm_01.R", "ikk.upperArm.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.R", "def.lowerArm_01.R", "mch.upperArm_ik_stretch.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_01.R", "def.lowerArm_01.R", "mch.upperArm_twist_ik.R")
moveBoneConXYZ(sceneRig[0], "def.upperArm_02.R", "mch.upperArm_twist.R", "tail", "Y", -0.05)
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_01.R", "def.wrist.R", "mch.elbow_ik_stretch.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_01.R", "def.wrist.R", "ikk.lowerArm.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_01.R", "def.wrist.R", "mch.lowerArm_ik_stretch.R")
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "ikh.arm.R", "tail", "Y", -0.05)
moveBoneConXYZ(sceneRig[0], "def.lowerArm_02.R", "ikk.arm_end.R", "tail", "Y", -0.08)
moveBoneConXYZ(sceneRig[0], "def.wrist.R", "mch.sdk_ikh_wrist.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.wrist.R", "ikh.wrist.R", "tail", "Z", -0.02)

## Hand IK Bones Right ## 
moveBoneBasic(sceneRig[0], "def.wrist.R", "ikk.wrist.R")
moveBoneBasic(sceneRig[0], "def.hand.R", "ikk.hand.R")
moveBoneBasic(sceneRig[0], "mch.fingers.R", "ikk.fingers.R")
moveBoneConXYZ(sceneRig[0], "mch.fingers.R", "ikk.heel_front.R", "tail", "Y", 0.11)
moveBoneConXYZ(sceneRig[0], "mch.fingers.R", "ikh.fingers.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "ikk.heel_front.R", "ikh.heel_front.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.hand.R", "mch.sdk_ikh_hand.R", "tail", "Z", -0.02)
moveBoneConXYZ(sceneRig[0], "def.hand.R", "ikh.hand.R", "tail", "Z", -0.02)

## Hand IK Bones Float Left ## 
moveBoneExt(sceneRig[0], "ikh.fingers.L", "mch.sdk_ikh_fingers_horizontal.L", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.L", "mch.sdk_ikh_fingers_horizontal.L", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.L", "mch.sdk_ikh_fingers_vertical.L")

moveBoneExt(sceneRig[0], "ikh.wrist.L", "mch.sdk_ikh_heel_front_horizontal.L", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_heel_front_horizontal.L", "mch.sdk_ikh_heel_front_horizontal.L", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_heel_front_horizontal.L", "mch.sdk_ikh_heel_front_vertical.L")

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.L", "mch.sdk_ikh_heel_front_bank_posterior.L")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_front_bank_posterior.L", "mch.sdk_ikh_heel_front_bank_posterior.L", "head", [-0.04, 0.03, 0.0], [-0.04, 0.03, 0.0])

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.L", "mch.sdk_ikh_heel_front_bank_interior.L")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_front_bank_interior.L", "mch.sdk_ikh_heel_front_bank_interior.L", "head", [0.04, 0.03, 0.0], [0.04, 0.03, 0.0])

## Hand IK Bones Float Right ## 
moveBoneExt(sceneRig[0], "ikh.fingers.R", "mch.sdk_ikh_fingers_horizontal.R", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.R", "mch.sdk_ikh_fingers_horizontal.R", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.R", "mch.sdk_ikh_fingers_vertical.R")

moveBoneExt(sceneRig[0], "ikh.wrist.R", "mch.sdk_ikh_heel_front_horizontal.R", "custom", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "mch.sdk_ikh_heel_front_horizontal.R", "mch.sdk_ikh_heel_front_horizontal.R", "head", "Z", -0.02)
moveBoneBasic(sceneRig[0], "mch.sdk_ikh_heel_front_horizontal.R", "mch.sdk_ikh_heel_front_vertical.R")

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.R", "mch.sdk_ikh_heel_front_bank_posterior.R")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_front_bank_posterior.R", "mch.sdk_ikh_heel_front_bank_posterior.R", "head", [-0.04, 0.03, 0.0], [-0.04, 0.03, 0.0])

moveBoneBasic(sceneRig[0], "mch.sdk_ikh_fingers_horizontal.R", "mch.sdk_ikh_heel_front_bank_interior.R")
moveBoneExt(sceneRig[0], "mch.sdk_ikh_heel_front_bank_interior.R", "mch.sdk_ikh_heel_front_bank_interior.R", "head", [0.04, 0.03, 0.0], [0.04, 0.03, 0.0])

## Floating IK Position Arm Bones Left ## 
moveBoneConXYZ(sceneRig[0], "def.upperArm_02.L", "arm_pole.L", "tail", "Y", 0.05)
moveBoneExt(sceneRig[0], "arm_pole.L", "arm_pole.L", "head", [-0.00, 0.7, 0.0], [-0.00, 0.7, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.fingers.L", "mch.wrist_ik_pole.L", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.wrist_ik_pole.L", "mch.wrist_ik_pole.L", "head", [-0.00, -0.25, 0.0], [-0.00, -0.25, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.fingers.L", "mch.hand_ik_pole.L", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.hand_ik_pole.L", "mch.hand_ik_pole.L", "head", [-0.00, -0.25, 0.1], [-0.00, -0.25, 0.1])

moveBoneConXYZ(sceneRig[0], "mch.fingers.L", "mch.fingers_ik_pole.L", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.fingers_ik_pole.L", "mch.fingers_ik_pole.L", "head", [-0.00, -0.28, 0.1], [-0.00, -0.28, 0.1])

## Floating IK Position Arm Bones Right ## 
moveBoneConXYZ(sceneRig[0], "def.upperArm_02.R", "arm_pole.R", "tail", "Y", 0.05)
moveBoneExt(sceneRig[0], "arm_pole.R", "arm_pole.R", "head", [-0.00, 0.7, 0.0], [-0.00, 0.7, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.fingers.R", "mch.wrist_ik_pole.R", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.wrist_ik_pole.R", "mch.wrist_ik_pole.R", "head", [-0.00, -0.25, 0.0], [-0.00, -0.25, 0.0])

moveBoneConXYZ(sceneRig[0], "mch.fingers.R", "mch.hand_ik_pole.R", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.hand_ik_pole.R", "mch.hand_ik_pole.R", "head", [-0.00, -0.25, 0.1], [-0.00, -0.25, 0.1])

moveBoneConXYZ(sceneRig[0], "mch.fingers.R", "mch.fingers_ik_pole.R", "tail", "Z", -0.02)
moveBoneExt(sceneRig[0], "mch.fingers_ik_pole.R", "mch.fingers_ik_pole.R", "head", [-0.00, -0.28, 0.1], [-0.00, -0.28, 0.1])


#########################
## MCH Secondary Bones ##
#########################

## Spine Mch Secondary ## 
moveBoneBasic(sceneRig[0], "def.spine_04.C", "mch.spine_05_twist_b_target.C")
moveBoneBasic(sceneRig[0], "def.spine_05.C", "mch.spine_05_twist_a.C")
moveBoneBasic(sceneRig[0], "def.spine_05.C", "mch.spine_05.C")
moveBoneTwoBoneBasic(sceneRig[0], "def.spine_05.C", "def.spine_04.C", "mch.spine_05_twist_b.C")
moveBoneScale(sceneRig[0], "def.spine_05.C", "mch.spine_05_twist_a_target.C", 1)
moveBoneExt(sceneRig[0], "def.head.C", "mch.spine_05_twist_a_target.C", "headMain", [0], [0])

## Leg Mch Secondary Left ##
moveBoneBasic(sceneRig[0], "def.upperLeg_01.L", "mch.upperLeg_02_twist_a_target.L")
moveBoneBasic(sceneRig[0], "def.upperLeg_02.L", "mch.upperLeg_02_twist_b.L")
moveBoneBasic(sceneRig[0], "def.upperLeg_02.L", "mch.upperLeg_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_02.L", "def.upperLeg_01.L", "mch.upperLeg_02_twist_a.L")
moveBoneScale(sceneRig[0], "def.upperLeg_02.L", "mch.upperLeg_02_twist_b_target.L", .6)
moveBoneExt(sceneRig[0], "def.lowerLeg_01.L", "mch.upperLeg_02_twist_b_target.L", "headMain", [0], [0])
moveBoneBasic(sceneRig[0], "ctl.leg_pole.L", "mch.leg_pole_hipLock.L")
moveBoneBasic(sceneRig[0], "ctl.leg_pole.L", "mch.leg_pole.L")
moveBoneScale(sceneRig[0], "def.ankle.L", "mch.ankle_rotate.L", -.5)
moveBoneConXYZ(sceneRig[0], "def.ankle.L", "mch.ankle_rotate_up.L", "tail", "Z", -0.04)
moveBoneScale(sceneRig[0], "ctl.leg_pole.L", "mch.leg_pole_rotate_up.L", 1.5)
moveBoneExt(sceneRig[0], "def.foot.L", "mch.leg_pole_rotate_up.L", "headMain", [0], [0])

## Leg Mch Secondary Right ## 
moveBoneBasic(sceneRig[0], "def.upperLeg_01.R", "mch.upperLeg_02_twist_a_target.R")
moveBoneBasic(sceneRig[0], "def.upperLeg_02.R", "mch.upperLeg_02_twist_b.R")
moveBoneBasic(sceneRig[0], "def.upperLeg_02.R", "mch.upperLeg_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperLeg_02.R", "def.upperLeg_01.R", "mch.upperLeg_02_twist_a.R")
moveBoneScale(sceneRig[0], "def.upperLeg_02.R", "mch.upperLeg_02_twist_b_target.R", .6)
moveBoneExt(sceneRig[0], "def.lowerLeg_01.R", "mch.upperLeg_02_twist_b_target.R", "headMain", [0], [0])
moveBoneBasic(sceneRig[0], "ctl.leg_pole.R", "mch.leg_pole_hipLock.R")
moveBoneBasic(sceneRig[0], "ctl.leg_pole.R", "mch.leg_pole.R")
moveBoneScale(sceneRig[0], "def.ankle.R", "mch.ankle_rotate.R", -.5)
moveBoneConXYZ(sceneRig[0], "def.ankle.R", "mch.ankle_rotate_up.R", "tail", "Z", -0.04)
moveBoneScale(sceneRig[0], "ctl.leg_pole.R", "mch.leg_pole_rotate_up.R", 1.5)
moveBoneExt(sceneRig[0], "def.foot.R", "mch.leg_pole_rotate_up.R", "headMain", [0], [0])

## Arm Mch Secondary Left ## 
moveBoneBasic(sceneRig[0], "def.upperArm_01.L", "mch.upperArm_02_twist_a_target.L")
moveBoneBasic(sceneRig[0], "def.upperArm_02.L", "mch.upperArm_02.L")
moveBoneBasic(sceneRig[0], "def.upperArm_02.L", "mch.upperArm_02_twist_b.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_02.L", "def.upperArm_01.L", "mch.upperArm_02_twist_a.L")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.L", "mch.lowerArm_02_twist_a_target.L")
moveBoneScale(sceneRig[0], "def.upperArm_02.L", "mch.upperArm_02_twist_b_target.L", .6)
moveBoneExt(sceneRig[0], "def.lowerArm_01.L", "mch.upperArm_02_twist_b_target.L", "headMain", [0], [0])
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_02.L", "def.lowerArm_01.L", "mch.lowerArm_02_twist_a.L")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.L", "mch.lowerArm_02_twist_a_target.L")
moveBoneBasic(sceneRig[0], "ctl.arm_pole.L", "mch.arm_pole_chestLock.L")
moveBoneBasic(sceneRig[0], "ctl.arm_pole.L", "mch.arm_pole.L")
moveBoneBasic(sceneRig[0], "def.lowerArm_02.L", "mch.lowerArm_02.L")
moveBoneBasic(sceneRig[0], "def.lowerArm_02.L", "mch.lowerArm_twist_b.L")
moveBoneScale(sceneRig[0], "mch.arm_stretch_pin.L", "mch.lowerArm_02_twist_b_target.L", -.2)
moveBoneScale(sceneRig[0], "ctl.arm_pole.L", "mch.arm_pole_rotate_up.L", 1.9)
moveBoneExt(sceneRig[0], "def.wrist.L", "mch.arm_pole_rotate_up.L", "headMain", [0], [0])

## Arm Mch Secondary Right ## 
moveBoneBasic(sceneRig[0], "def.upperArm_01.R", "mch.upperArm_02_twist_a_target.R")
moveBoneBasic(sceneRig[0], "def.upperArm_02.R", "mch.upperArm_02.R")
moveBoneBasic(sceneRig[0], "def.upperArm_02.R", "mch.upperArm_02_twist_b.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upperArm_02.R", "def.upperArm_01.R", "mch.upperArm_02_twist_a.R")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.R", "mch.lowerArm_02_twist_a_target.R")
moveBoneScale(sceneRig[0], "def.upperArm_02.R", "mch.upperArm_02_twist_b_target.R", .6)
moveBoneExt(sceneRig[0], "def.lowerArm_01.R", "mch.upperArm_02_twist_b_target.R", "headMain", [0], [0])
moveBoneTwoBoneBasic(sceneRig[0], "def.lowerArm_02.R", "def.lowerArm_01.R", "mch.lowerArm_02_twist_a.R")
moveBoneBasic(sceneRig[0], "def.lowerArm_01.R", "mch.lowerArm_02_twist_a_target.R")
moveBoneBasic(sceneRig[0], "ctl.arm_pole.R", "mch.arm_pole_chestLock.R")
moveBoneBasic(sceneRig[0], "ctl.arm_pole.R", "mch.arm_pole.R")
moveBoneBasic(sceneRig[0], "def.lowerArm_02.R", "mch.lowerArm_02.R")
moveBoneBasic(sceneRig[0], "def.lowerArm_02.R", "mch.lowerArm_twist_b.R")
moveBoneScale(sceneRig[0], "mch.arm_stretch_pin.R", "mch.lowerArm_02_twist_b_target.R", -.2)
moveBoneScale(sceneRig[0], "ctl.arm_pole.R", "mch.arm_pole_rotate_up.R", 1.9)
moveBoneExt(sceneRig[0], "def.wrist.R", "mch.arm_pole_rotate_up.R", "headMain", [0], [0])


################
## Face Bones ##
################

###############
## MCH Bones ##
###############

## Tounge Mch Bones ## 
moveBoneBasic(sceneRig[0], "def.tongue_03.C", "mch.tongue_03.C")
moveBoneBasic(sceneRig[0], "def.tongue_04.C", "mch.tongue_04.C")
moveBoneBasic(sceneRig[0], "def.tongue_05.C", "mch.tongue_05.C")
moveBoneBasic(sceneRig[0], "def.tongue_06.C", "mch.tongue_06.C")
moveBoneBasic(sceneRig[0], "def.tongue_01.C", "mch.tongue_offset_01.C")
moveBoneTwoBoneBasic(sceneRig[0], "def.tongue_02.C", "def.tongue_01.C", "mch.tongue_01.C")
moveBoneBasic(sceneRig[0], "mch.tongue_01.C", "ctl.tongue_01.C")

## Bottom Lip MCH Bones Left ## 
moveBoneBasic(sceneRig[0], "def.lip_bot_00.L", "mch.lip_bot_offset_00.L")
moveBoneBasic(sceneRig[0], "def.lip_bot_01.L", "mch.lip_bot_offset_01.L")
moveBoneBasic(sceneRig[0], "def.lip_bot_02.L", "mch.lip_bot_offset_02.L")
moveBoneBasic(sceneRig[0], "def.lip_bot_03.L", "mch.lip_bot_offset_03.L")
moveBoneBasic(sceneRig[0], "def.lip_bot_04.L", "mch.lip_bot_offset_04.L")
moveBoneBasic(sceneRig[0], "def.lip_bot_05.L", "mch.lip_bot_offset_05.L")

## Top Lip MCH Bones Left ## 
moveBoneBasic(sceneRig[0], "def.lip_top_00.L", "mch.lip_top_offset_00.L")
moveBoneBasic(sceneRig[0], "def.lip_top_01.L", "mch.lip_top_offset_01.L")
moveBoneBasic(sceneRig[0], "def.lip_top_02.L", "mch.lip_top_offset_02.L")
moveBoneBasic(sceneRig[0], "def.lip_top_03.L", "mch.lip_top_offset_03.L")
moveBoneBasic(sceneRig[0], "def.lip_top_04.L", "mch.lip_top_offset_04.L")
moveBoneBasic(sceneRig[0], "def.lip_top_05.L", "mch.lip_top_offset_05.L")

## Bottom Lip MCH Bones Right ## 
moveBoneBasic(sceneRig[0], "def.lip_bot_00.R", "mch.lip_bot_offset_00.R")
moveBoneBasic(sceneRig[0], "def.lip_bot_01.R", "mch.lip_bot_offset_01.R")
moveBoneBasic(sceneRig[0], "def.lip_bot_02.R", "mch.lip_bot_offset_02.R")
moveBoneBasic(sceneRig[0], "def.lip_bot_03.R", "mch.lip_bot_offset_03.R")
moveBoneBasic(sceneRig[0], "def.lip_bot_04.R", "mch.lip_bot_offset_04.R")
moveBoneBasic(sceneRig[0], "def.lip_bot_05.R", "mch.lip_bot_offset_05.R")

## Top Lip MCH Bones Right ## 
moveBoneBasic(sceneRig[0], "def.lip_top_00.R", "mch.lip_top_offset_00.R")
moveBoneBasic(sceneRig[0], "def.lip_top_01.R", "mch.lip_top_offset_01.R")
moveBoneBasic(sceneRig[0], "def.lip_top_02.R", "mch.lip_top_offset_02.R")
moveBoneBasic(sceneRig[0], "def.lip_top_03.R", "mch.lip_top_offset_03.R")
moveBoneBasic(sceneRig[0], "def.lip_top_04.R", "mch.lip_top_offset_04.R")
moveBoneBasic(sceneRig[0], "def.lip_top_05.R", "mch.lip_top_offset_05.R")

## Bottom Lip MCH Ring Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lip_bot_00.C", "mch.lip_ring_bot_00.C", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.lip_bot_01.L", "mch.lip_ring_bot_01.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_02.L", "mch.lip_ring_bot_02.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_03.L", "mch.lip_ring_bot_03.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_04.L", "mch.lip_ring_bot_04.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_05.L", "mch.lip_ring_bot_05.L", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.lip_bot_01.R", "mch.lip_ring_bot_01.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_02.R", "mch.lip_ring_bot_02.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_03.R", "mch.lip_ring_bot_03.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_04.R", "mch.lip_ring_bot_04.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_05.R", "mch.lip_ring_bot_05.R", "head", "Y", 0.01)

## Top Lip MCH Ring Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lip_top_00.C", "mch.lip_ring_top_00.C", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.lip_top_01.L", "mch.lip_ring_top_01.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_02.L", "mch.lip_ring_top_02.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_03.L", "mch.lip_ring_top_03.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_04.L", "mch.lip_ring_top_04.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_05.L", "mch.lip_ring_top_05.L", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.lip_top_01.R", "mch.lip_ring_top_01.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_02.R", "mch.lip_ring_top_02.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_03.R", "mch.lip_ring_top_03.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_04.R", "mch.lip_ring_top_04.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_top_05.R", "mch.lip_ring_top_05.R", "head", "Y", 0.01)

## Corner Lip MCH Ring Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lip_corner_pin.L", "mch.lip_ring_corner.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.lip_corner_pin.R", "mch.lip_ring_corner.R", "head", "Y", 0.01)

## Nose MCH Bones ## 
moveBoneConXYZ(sceneRig[0], "def.nose_03.C", "mch.lip_top_00.C", "tail", "Y", 0.05)
moveBoneScale(sceneRig[0], "def.nose_01.C", "mch.lip_nose_pivot_top_00.C", -.1)
moveBoneScale(sceneRig[0], "def.nose_01.C", "mch.lip_nose_pivot_top_01.C", -.2)
moveBoneScale(sceneRig[0], "def.nose_01.C", "mch.lip_nose_pivot_top_02.C", -.3)
moveBoneScale(sceneRig[0], "def.nose_01.C", "mch.lip_nose_pivot_top_03.C", -.4)
moveBoneScale(sceneRig[0], "def.nose_01.C", "mch.lip_nose_pivot_top_04.C", -.5)
moveBoneScale(sceneRig[0], "def.nose_01.C", "mch.lip_nose_pivot_top_05.C", -.6)
moveBoneBasic(sceneRig[0], "def.nose_01.C", "nose_01_offset.C")
moveBoneBasic(sceneRig[0], "def.nose_01.C", "nose_02_offset.C")
moveBoneScale(sceneRig[0], "ctl.nose_02.C", "ctl.nose_01.C", .5)

moveBoneBasic(sceneRig[0], "def.noseBridge_02.C", "mch.noseBridge_offset_02.C")
moveBoneBasic(sceneRig[0], "def.noseBridge_02.C", "mch.noseBridge_offset_02.C")

## Cheek MCH Bones Left ## 
moveBoneBasic(sceneRig[0], "def.lip_corner.L", "mch.lip_corner_offset.L")
moveBoneBasic(sceneRig[0], "def.cheek_side_01.L", "mch.cheek_side_01.L")
moveBoneBasic(sceneRig[0], "def.cheek_side_01.L", "mch.cheek_side_offset_01.L")
moveBoneBasic(sceneRig[0], "def.cheek_front_01.L", "mch.cheek_front_01.L")
moveBoneBasic(sceneRig[0], "def.cheek_front_02.L", "mch.cheek_front_offset_02.L")
moveBoneBasic(sceneRig[0], "def.cheek_front_02.L", "mch.cheek_front_02.L")
moveBoneBasic(sceneRig[0], "def.cheek_front_03.L", "mch.cheek_front_03.L")
moveBoneScale(sceneRig[0], "def.cheek_front_03.L", "mch.cheek_front_offset_03.L", -.5)

## Cheek MCH Bones Right ## 
moveBoneBasic(sceneRig[0], "def.lip_corner.R", "mch.lip_corner_offset.R")
moveBoneBasic(sceneRig[0], "def.cheek_side_01.R", "mch.cheek_side_01.R")
moveBoneBasic(sceneRig[0], "def.cheek_side_01.R", "mch.cheek_side_offset_01.R")
moveBoneBasic(sceneRig[0], "def.cheek_front_01.R", "mch.cheek_front_01.R")
moveBoneBasic(sceneRig[0], "def.cheek_front_02.R", "mch.cheek_front_offset_02.R")
moveBoneBasic(sceneRig[0], "def.cheek_front_02.R", "mch.cheek_front_02.R")
moveBoneBasic(sceneRig[0], "def.cheek_front_03.R", "mch.cheek_front_03.R")
moveBoneScale(sceneRig[0], "def.cheek_front_03.R", "mch.cheek_front_offset_03.R", -.5)

## EyeBrow Top Mch Left ## 
moveBoneBasic(sceneRig[0], "def.eyebrow_00.L", "mch.eyebrow_00.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_01.L", "mch.eyebrow_01.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_02.L", "mch.eyebrow_02.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_03.L", "mch.eyebrow_03.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_04.L", "mch.eyebrow_04.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_05.L", "mch.eyebrow_05.L")

moveBoneBasic(sceneRig[0], "def.eyebrow_00.L", "mch.eyebrow_offset_00.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_01.L", "mch.eyebrow_offset_01.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_02.L", "mch.eyebrow_offset_02.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_03.L", "mch.eyebrow_offset_03.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_04.L", "mch.eyebrow_offset_04.L")
moveBoneBasic(sceneRig[0], "def.eyebrow_05.L", "mch.eyebrow_offset_05.L")

## EyeBrow Top Mch Right## 
moveBoneBasic(sceneRig[0], "def.eyebrow_00.R", "mch.eyebrow_00.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_01.R", "mch.eyebrow_01.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_02.R", "mch.eyebrow_02.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_03.R", "mch.eyebrow_03.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_04.R", "mch.eyebrow_04.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_05.R", "mch.eyebrow_05.R")

moveBoneBasic(sceneRig[0], "def.eyebrow_00.R", "mch.eyebrow_offset_00.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_01.R", "mch.eyebrow_offset_01.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_02.R", "mch.eyebrow_offset_02.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_03.R", "mch.eyebrow_offset_03.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_04.R", "mch.eyebrow_offset_04.R")
moveBoneBasic(sceneRig[0], "def.eyebrow_05.R", "mch.eyebrow_offset_05.R")

## Eye Mch Bones Left ## 
moveBoneScale(sceneRig[0], "def.eyelid_top.L", "mch.eyelid_top.L", 1)

moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_01.L", "mch.eyelid_top_01.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_02.L", "mch.eyelid_top_02.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_03.L", "mch.eyelid_top_03.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_04.L", "mch.eyelid_top_04.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_05.L", "mch.eyelid_top_05.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_06.L", "mch.eyelid_top_06.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_06.L", "mch.eyelid_corner_01.L", "tail", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_01.L", "mch.eyelid_bot_01.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_02.L", "mch.eyelid_bot_02.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_03.L", "mch.eyelid_bot_03.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_04.L", "mch.eyelid_bot_04.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_05.L", "mch.eyelid_bot_05.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_06.L", "mch.eyelid_bot_06.L", "head", "Y", 0.01)

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_01.L", "mch.eyelid_top_a_offset_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_01.L", "mch.eyelid_top_b_offset_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_01.L", "mch.eyelid_SDK1_top_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_01.L", "mch.eyelid_SDK2_top_01.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_02.L", "mch.eyelid_top_a_offset_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_02.L", "mch.eyelid_top_b_offset_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_02.L", "mch.eyelid_SDK1_top_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_02.L", "mch.eyelid_SDK2_top_02.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_03.L", "mch.eyelid_top_a_offset_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_03.L", "mch.eyelid_top_b_offset_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_03.L", "mch.eyelid_SDK1_top_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_03.L", "mch.eyelid_SDK2_top_03.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_04.L", "mch.eyelid_top_a_offset_04.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_04.L", "mch.eyelid_top_b_offset_04.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_04.L", "mch.eyelid_SDK1_top_04.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_04.L", "mch.eyelid_SDK2_top_04.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_05.L", "mch.eyelid_top_a_offset_05.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_05.L", "mch.eyelid_top_b_offset_05.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_05.L", "mch.eyelid_SDK1_top_05.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_05.L", "mch.eyelid_SDK2_top_05.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_06.L", "mch.eyelid_top_a_offset_06.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_06.L", "mch.eyelid_top_b_offset_06.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_06.L", "mch.eyelid_SDK1_top_06.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_top_a_06.L", "mch.eyelid_SDK2_top_06.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "mch.eyelid_corner_01.L", "mch.eyelid_corner_a_offset_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "mch.eyelid_corner_01.L", "mch.eyelid_corner_b_offset_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "mch.eyelid_corner_01.L", "mch.eyelid_SDK1_corner_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "mch.eyelid_corner_01.L", "mch.eyelid_SDK2_corner_01.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_01.L", "mch.eyelid_bot_a_offset_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_01.L", "mch.eyelid_bot_b_offset_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_01.L", "mch.eyelid_SDK1_bot_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_01.L", "mch.eyelid_SDK2_bot_01.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_02.L", "mch.eyelid_bot_a_offset_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_02.L", "mch.eyelid_bot_b_offset_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_02.L", "mch.eyelid_SDK1_bot_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_02.L", "mch.eyelid_SDK2_bot_02.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_03.L", "mch.eyelid_bot_a_offset_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_03.L", "mch.eyelid_bot_b_offset_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_03.L", "mch.eyelid_SDK1_bot_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_03.L", "mch.eyelid_SDK2_bot_03.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_04.L", "mch.eyelid_bot_a_offset_04.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_04.L", "mch.eyelid_bot_b_offset_04.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_04.L", "mch.eyelid_SDK1_bot_04.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_04.L", "mch.eyelid_SDK2_bot_04.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_05.L", "mch.eyelid_bot_a_offset_05.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_05.L", "mch.eyelid_bot_b_offset_05.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_05.L", "mch.eyelid_SDK1_bot_05.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_05.L", "mch.eyelid_SDK2_bot_05.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_06.L", "mch.eyelid_bot_a_offset_06.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_06.L", "mch.eyelid_bot_b_offset_06.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_06.L", "mch.eyelid_SDK1_bot_06.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.L", "def.eyelid_bot_a_06.L", "mch.eyelid_SDK2_bot_06.L")

moveBoneScale(sceneRig[0], "def.eyelid_bot.L", "mch.eyelid_bot.L", 1)

## Eye Mch Bones Right ## 
moveBoneScale(sceneRig[0], "def.eyelid_top.R", "mch.eyelid_top.R", 1)

moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_01.R", "mch.eyelid_top_01.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_02.R", "mch.eyelid_top_02.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_03.R", "mch.eyelid_top_03.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_04.R", "mch.eyelid_top_04.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_05.R", "mch.eyelid_top_05.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_06.R", "mch.eyelid_top_06.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_06.R", "mch.eyelid_corner_01.R", "tail", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_01.R", "mch.eyelid_bot_01.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_02.R", "mch.eyelid_bot_02.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_03.R", "mch.eyelid_bot_03.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_04.R", "mch.eyelid_bot_04.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_05.R", "mch.eyelid_bot_05.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_06.R", "mch.eyelid_bot_06.R", "head", "Y", 0.01)

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_01.R", "mch.eyelid_top_a_offset_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_01.R", "mch.eyelid_top_b_offset_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_01.R", "mch.eyelid_SDK1_top_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_01.R", "mch.eyelid_SDK2_top_01.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_02.R", "mch.eyelid_top_a_offset_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_02.R", "mch.eyelid_top_b_offset_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_02.R", "mch.eyelid_SDK1_top_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_02.R", "mch.eyelid_SDK2_top_02.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_03.R", "mch.eyelid_top_a_offset_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_03.R", "mch.eyelid_top_b_offset_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_03.R", "mch.eyelid_SDK1_top_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_03.R", "mch.eyelid_SDK2_top_03.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_04.R", "mch.eyelid_top_a_offset_04.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_04.R", "mch.eyelid_top_b_offset_04.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_04.R", "mch.eyelid_SDK1_top_04.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_04.R", "mch.eyelid_SDK2_top_04.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_05.R", "mch.eyelid_top_a_offset_05.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_05.R", "mch.eyelid_top_b_offset_05.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_05.R", "mch.eyelid_SDK1_top_05.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_05.R", "mch.eyelid_SDK2_top_05.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_06.R", "mch.eyelid_top_a_offset_06.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_06.R", "mch.eyelid_top_b_offset_06.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_06.R", "mch.eyelid_SDK1_top_06.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_top_a_06.R", "mch.eyelid_SDK2_top_06.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "mch.eyelid_corner_01.R", "mch.eyelid_corner_a_offset_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "mch.eyelid_corner_01.R", "mch.eyelid_corner_b_offset_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "mch.eyelid_corner_01.R", "mch.eyelid_SDK1_corner_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "mch.eyelid_corner_01.R", "mch.eyelid_SDK2_corner_01.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_01.R", "mch.eyelid_bot_a_offset_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_01.R", "mch.eyelid_bot_b_offset_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_01.R", "mch.eyelid_SDK1_bot_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_01.R", "mch.eyelid_SDK2_bot_01.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_02.R", "mch.eyelid_bot_a_offset_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_02.R", "mch.eyelid_bot_b_offset_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_02.R", "mch.eyelid_SDK1_bot_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_02.R", "mch.eyelid_SDK2_bot_02.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_03.R", "mch.eyelid_bot_a_offset_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_03.R", "mch.eyelid_bot_b_offset_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_03.R", "mch.eyelid_SDK1_bot_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_03.R", "mch.eyelid_SDK2_bot_03.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_04.R", "mch.eyelid_bot_a_offset_04.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_04.R", "mch.eyelid_bot_b_offset_04.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_04.R", "mch.eyelid_SDK1_bot_04.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_04.R", "mch.eyelid_SDK2_bot_04.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_05.R", "mch.eyelid_bot_a_offset_05.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_05.R", "mch.eyelid_bot_b_offset_05.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_05.R", "mch.eyelid_SDK1_bot_05.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_05.R", "mch.eyelid_SDK2_bot_05.R")

moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_06.R", "mch.eyelid_bot_a_offset_06.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_06.R", "mch.eyelid_bot_b_offset_06.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_06.R", "mch.eyelid_SDK1_bot_06.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.eye.R", "def.eyelid_bot_a_06.R", "mch.eyelid_SDK2_bot_06.R")

moveBoneScale(sceneRig[0], "def.eyelid_bot.R", "mch.eyelid_bot.R", 1)

## Jaw MCH Bones ##
moveBoneTwoBoneBasic(sceneRig[0], "ctl.lowerJaw.C", "def.lower_jaw.C", "mch.jaw_hinge.C")
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_bot_05.C", -.7)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_top_05.C", -.6)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_bot_04.C", -.5)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_top_04.C", -.4)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_bot_03.C", -.3)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_top_03.C", -.2)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_bot_02.C", -.1)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_top_02.C", .1)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_bot_01.C", .2)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_top_01.C", .3)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_bot_00.C", .4)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_top_00.C", .5)
moveBoneScale(sceneRig[0], "mch.jaw_hinge.C", "mch.lip_corner.C", .6)


## Nose Mch Bones ## 
moveBoneBasic(sceneRig[0], "def.noseBridge_02.C", "mch.noseBridge_offset_02.C")
moveBoneBasic(sceneRig[0], "def.noseBridge_01.C", "mch.noseBridge_offset_01.C")


###############
## CTL BONES ##
###############

## Tounge Ctl Bones  ## 
moveBoneBasic(sceneRig[0], "def.tongue_03.C", "ctl.tongue_03.C")
moveBoneBasic(sceneRig[0], "def.tongue_04.C", "ctl.tongue_04.C")
moveBoneBasic(sceneRig[0], "def.tongue_05.C", "ctl.tongue_05.C")
moveBoneBasic(sceneRig[0], "def.tongue_06.C", "ctl.tongue_06.C")

## Lip Corner Ctl 
moveBoneConXYZ(sceneRig[0], "def.lip_top_05.L", "ctl.lip_corner.L", "tail", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_05.R", "ctl.lip_corner.R", "tail", "Y", 0.05)

##Top Lip Ctl ## 
moveBoneConXYZ(sceneRig[0], "def.nose_03.C", "ctl.lip_top_00.C", "tail", "Y", 0.05)

moveBoneConXYZ(sceneRig[0], "def.lip_top_01.L", "ctl.lip_top_01.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_02.L", "ctl.lip_top_02.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_03.L", "ctl.lip_top_03.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_04.L", "ctl.lip_top_04.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_05.L", "ctl.lip_top_05.L", "head", "Y", 0.05)

moveBoneConXYZ(sceneRig[0], "def.lip_top_01.R", "ctl.lip_top_01.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_02.R", "ctl.lip_top_02.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_03.R", "ctl.lip_top_03.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_04.R", "ctl.lip_top_04.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_top_05.R", "ctl.lip_top_05.R", "head", "Y", 0.05)

##Bottom Lip Ctl ## 
moveBoneConXYZ(sceneRig[0], "def.lip_bot_00.R", "ctl.lip_bot_00.C", "head", "Y", 0.05)

moveBoneConXYZ(sceneRig[0], "def.lip_bot_01.L", "ctl.lip_bot_01.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_02.L", "ctl.lip_bot_02.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_03.L", "ctl.lip_bot_03.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_04.L", "ctl.lip_bot_04.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_05.L", "ctl.lip_bot_05.L", "head", "Y", 0.05)

moveBoneConXYZ(sceneRig[0], "def.lip_bot_01.R", "ctl.lip_bot_01.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_02.R", "ctl.lip_bot_02.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_03.R", "ctl.lip_bot_03.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_04.R", "ctl.lip_bot_04.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.lip_bot_05.R", "ctl.lip_bot_05.R", "head", "Y", 0.05)

## Lip Master Ctl ## 
moveBoneConXYZ(sceneRig[0], "def.lip_top_04.L", "ctl.lip_master_top.L", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "ctl.lip_master_top.L", "ctl.lip_master_top.L", "head", [0.05, -0.0, 0.0], [0.05, -0.0, 0.00])

moveBoneConXYZ(sceneRig[0], "def.lip_corner_pin.L", "ctl.lip_master_corner.L", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "ctl.lip_master_corner.L", "ctl.lip_master_corner.L", "head", [0.05, -0.0, 0.0], [0.05, -0.0, 0.00])

moveBoneConXYZ(sceneRig[0], "def.lip_bot_02.L", "ctl.lip_master_bot.L", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "ctl.lip_master_bot.L", "ctl.lip_master_bot.L", "head", [0.05, -0.0, 0.0], [0.05, -0.0, 0.00])

moveBoneConXYZ(sceneRig[0], "def.lip_top_04.R", "ctl.lip_master_top.R", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "ctl.lip_master_top.R", "ctl.lip_master_top.R", "head", [0.05, -0.0, 0.0], [0.05, -0.0, 0.00])

moveBoneConXYZ(sceneRig[0], "def.lip_corner_pin.R", "ctl.lip_master_corner.R", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "ctl.lip_master_corner.R", "ctl.lip_master_corner.R", "head", [0.05, -0.0, 0.0], [0.05, -0.0, 0.00])

moveBoneConXYZ(sceneRig[0], "def.lip_bot_02.R", "ctl.lip_master_bot.R", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "ctl.lip_master_bot.R", "ctl.lip_master_bot.R", "head", [0.05, -0.0, 0.0], [0.05, -0.0, 0.00])


## Cheek Ctl Left ## 
moveBoneConXYZ(sceneRig[0], "def.cheek_side_01.L", "ctl.cheek_side_01.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.cheek_front_02.L", "ctl.cheek_front_02.L", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.cheek_front_03.L", "ctl.cheek_front_03.L", "head", "Y", 0.05)

## Cheek Ctl Right ## 
moveBoneConXYZ(sceneRig[0], "def.cheek_side_01.R", "ctl.cheek_side_01.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.cheek_front_02.R", "ctl.cheek_front_02.R", "head", "Y", 0.05)
moveBoneConXYZ(sceneRig[0], "def.cheek_front_03.R", "ctl.cheek_front_03.R", "head", "Y", 0.05)

## Mouth Ctl ## 
moveBoneBasic(sceneRig[0], "def.teeth_top.C", "ctl.teeth_top.C")
moveBoneBasic(sceneRig[0], "def.teeth_bot.C", "ctl.teeth_bot.C")

## Nose Ctl ## 
moveBoneConXYZ(sceneRig[0], "def.nose_01.C", "ctl.nose_02.C", "head", "Z", -0.06)
moveBoneConXYZ(sceneRig[0], "def.noseBridge_01.C", "ctl.noseBridge_01.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.noseBridge_02.C", "ctl.noseBridge_02.C", "head", "Y", 0.02)

## EyeBrow Top Ctl Left ## 
moveBoneConXYZ(sceneRig[0], "def.eyebrow_00.L", "ctl.eyebrow_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_01.L", "ctl.eyebrow_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_02.L", "ctl.eyebrow_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_03.L", "ctl.eyebrow_03.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_04.L", "ctl.eyebrow_04.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_05.L", "ctl.eyebrow_05.L", "head", "Y", 0.02)

## EyeBrow Top Ctl Right ## 
moveBoneConXYZ(sceneRig[0], "def.eyebrow_00.R", "ctl.eyebrow_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_01.R", "ctl.eyebrow_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_02.R", "ctl.eyebrow_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_03.R", "ctl.eyebrow_03.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_04.R", "ctl.eyebrow_04.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eyebrow_05.R", "ctl.eyebrow_05.R", "head", "Y", 0.02)

## EyeBrow Master Ctl ## 
moveBoneBasic(sceneRig[0], "ctl.eyebrow_02.L", "ctl.eyebrow_main.L")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_02.R", "ctl.eyebrow_main.R")


## Eye Ctl Left ## 
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_01.L", "ctl.eyelid_top_01.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_02.L", "ctl.eyelid_top_02.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_03.L", "ctl.eyelid_top_03.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_04.L", "ctl.eyelid_top_04.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_05.L", "ctl.eyelid_top_05.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_06.L", "ctl.eyelid_top_06.L", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_01.L", "ctl.eyelid_bot_01.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_02.L", "ctl.eyelid_bot_02.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_03.L", "ctl.eyelid_bot_03.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_04.L", "ctl.eyelid_bot_04.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_05.L", "ctl.eyelid_bot_05.L", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_06.L", "ctl.eyelid_bot_06.L", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.eyelid_corner_a_01.L", "ctl.eyelid_corner_01.L", "head", "Y", 0.01)

## Eye Ctl Right ## 
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_01.R", "ctl.eyelid_top_01.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_02.R", "ctl.eyelid_top_02.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_03.R", "ctl.eyelid_top_03.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_04.R", "ctl.eyelid_top_04.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_05.R", "ctl.eyelid_top_05.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_top_a_06.R", "ctl.eyelid_top_06.R", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_01.R", "ctl.eyelid_bot_01.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_02.R", "ctl.eyelid_bot_02.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_03.R", "ctl.eyelid_bot_03.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_04.R", "ctl.eyelid_bot_04.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_05.R", "ctl.eyelid_bot_05.R", "head", "Y", 0.01)
moveBoneConXYZ(sceneRig[0], "def.eyelid_bot_a_06.R", "ctl.eyelid_bot_06.R", "head", "Y", 0.01)

moveBoneConXYZ(sceneRig[0], "def.eyelid_corner_a_01.R", "ctl.eyelid_corner_01.R", "head", "Y", 0.01)

## Eye Top Bottom Master Ctl ## 
moveBoneConXYZ(sceneRig[0], "mch.eyelid_top.L", "ctl.eyelid_top.L", "tail", "Y", -0.03)

moveBoneConXYZ(sceneRig[0], "mch.eyelid_bot.L", "ctl.eyelid_bot.L", "tail", "Y", -0.03)

moveBoneConXYZ(sceneRig[0], "mch.eyelid_top.R", "ctl.eyelid_top.R", "tail", "Y", -0.03)

moveBoneConXYZ(sceneRig[0], "mch.eyelid_bot.R", "ctl.eyelid_bot.R", "tail", "Y", -0.03)

## Eye look At ctl Bones ## 
moveBoneBasic(sceneRig[0], "def.eye.L", "ctl.eye.L")
moveBoneExt(sceneRig[0], "ctl.eye.L", "ctl.eye.L", "head", [-0.00, -0.5, 0], [-0.00, -0.45, 0])

moveBoneBasic(sceneRig[0], "def.eye.R", "ctl.eye.R")
moveBoneExt(sceneRig[0], "ctl.eye.R", "ctl.eye.R", "head", [-0.00, -0.5, 0], [-0.00, -0.45, 0])

moveBoneConXYZ(sceneRig[0], "ctl.eye.L", "ctl.eye.C", "head", "Y", -0.1)
moveBoneExt(sceneRig[0], "ctl.eye.C", "ctl.eye.C", "eye", [-0.00, -0.0, 0], [-0.00, -0.0, 0])

moveBoneBasic(sceneRig[0], "def.eye.L", "ctl.eye_hightlite.L")
moveBoneExt(sceneRig[0], "ctl.eye_hightlite.L", "ctl.eye_hightlite.L", "head", [-0.00, -0.5, 0.04], [-0.00, -0.45, 0.04])

moveBoneBasic(sceneRig[0], "def.eye.R", "ctl.eye_hightlite.R")
moveBoneExt(sceneRig[0], "ctl.eye_hightlite.R", "ctl.eye_hightlite.R", "head", [-0.00, -0.5, 0.04], [-0.00, -0.45, 0.04])

moveBoneConXYZ(sceneRig[0], "ctl.eye_hightlite.L", "ctl.eye_hightlite.C", "head", "Y", -0.1)
moveBoneExt(sceneRig[0], "ctl.eye_hightlite.C", "ctl.eye_hightlite.C", "eye", [-0.00, -0.0, 0], [-0.00, -0.0, 0])

moveBoneBasic(sceneRig[0], "ctl.eye.C", "mch.eye_world.C")
moveBoneBasic(sceneRig[0], "ctl.eye.C", "mch.eye.C")
moveBoneBasic(sceneRig[0], "ctl.eye_hightlite.C", "mch.eye_hightlite_world.C")
moveBoneBasic(sceneRig[0], "ctl.eye_hightlite.C", "mch.eye_hightlite.C")


###############
## WGT Bones ##
###############

## Spine WGT Bones 
moveBoneConXYZ(sceneRig[0], "def.spine.C", "wgt.hips.C", "head", "Z", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_03.C", "wgt.chest.C", "head", "Z", 0.1)

## Left Foot WGT Bones ## 
moveBoneBasic(sceneRig[0], "def.toe_pinky_01.L", "wgt.toe_pinky.L")
moveBoneExt(sceneRig[0], "wgt.toe_pinky.L", "wgt.toe_pinky.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_pinky_02.L", "wgt.toe_pinky_02.L")
moveBoneExt(sceneRig[0], "wgt.toe_pinky_02.L", "wgt.toe_pinky_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_ring_01.L", "wgt.toe_ring.L")
moveBoneExt(sceneRig[0], "wgt.toe_ring.L", "wgt.toe_ring.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_ring_02.L", "wgt.toe_ring_02.L")
moveBoneExt(sceneRig[0], "wgt.toe_ring_02.L", "wgt.toe_ring_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_index_01.L", "wgt.toe_index.L")
moveBoneExt(sceneRig[0], "wgt.toe_index.L", "wgt.toe_index.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_index_02.L", "wgt.toe_index_02.L")
moveBoneExt(sceneRig[0], "wgt.toe_index_02.L", "wgt.toe_index_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_thumb_01.L", "wgt.toe_thumb.L")
moveBoneExt(sceneRig[0], "wgt.toe_thumb.L", "wgt.toe_thumb.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_thumb_02.L", "wgt.toe_thumb_02.L")
moveBoneExt(sceneRig[0], "wgt.toe_thumb_02.L", "wgt.toe_thumb_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

## Right Foot WGT Bones ## 
moveBoneBasic(sceneRig[0], "def.toe_pinky_01.R", "wgt.toe_pinky.R")
moveBoneExt(sceneRig[0], "wgt.toe_pinky.R", "wgt.toe_pinky.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_pinky_02.R", "wgt.toe_pinky_02.R")
moveBoneExt(sceneRig[0], "wgt.toe_pinky_02.R", "wgt.toe_pinky_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_ring_01.R", "wgt.toe_ring.R")
moveBoneExt(sceneRig[0], "wgt.toe_ring.R", "wgt.toe_ring.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_ring_02.R", "wgt.toe_ring_02.R")
moveBoneExt(sceneRig[0], "wgt.toe_ring_02.R", "wgt.toe_ring_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_index_01.R", "wgt.toe_index.R")
moveBoneExt(sceneRig[0], "wgt.toe_index.R", "wgt.toe_index.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_index_02.R", "wgt.toe_index_02.R")
moveBoneExt(sceneRig[0], "wgt.toe_index_02.R", "wgt.toe_index_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_thumb_01.R", "wgt.toe_thumb.R")
moveBoneExt(sceneRig[0], "wgt.toe_thumb.R", "wgt.toe_thumb.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.toe_thumb_02.R", "wgt.toe_thumb_02.R")
moveBoneExt(sceneRig[0], "wgt.toe_thumb_02.R", "wgt.toe_thumb_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

## Left Hand WGT Bones ## 
moveBoneBasic(sceneRig[0], "def.finger_pinky_01.L", "wgt.finger_pinky.L")
moveBoneExt(sceneRig[0], "wgt.finger_pinky.L", "wgt.finger_pinky.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_pinky_02.L", "wgt.finger_pinky_02.L")
moveBoneExt(sceneRig[0], "wgt.finger_pinky_02.L", "wgt.finger_pinky_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_ring_01.L", "wgt.finger_ring.L")
moveBoneExt(sceneRig[0], "wgt.finger_ring.L", "wgt.finger_ring.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_ring_02.L", "wgt.finger_ring_02.L")
moveBoneExt(sceneRig[0], "wgt.finger_ring_02.L", "wgt.finger_ring_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_index_01.L", "wgt.finger_index.L")
moveBoneExt(sceneRig[0], "wgt.finger_index.L", "wgt.finger_index.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_index_02.L", "wgt.finger_index_02.L")
moveBoneExt(sceneRig[0], "wgt.finger_index_02.L", "wgt.finger_index_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_thumb_01.L", "wgt.finger_thumb.L")
moveBoneExt(sceneRig[0], "wgt.finger_thumb.L", "wgt.finger_thumb.L", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_thumb_02.L", "wgt.finger_thumb_02.L")
moveBoneExt(sceneRig[0], "wgt.finger_thumb_02.L", "wgt.finger_thumb_02.L", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

## Right Hand WGT Bones ## 
moveBoneBasic(sceneRig[0], "def.finger_pinky_01.R", "wgt.finger_pinky.R")
moveBoneExt(sceneRig[0], "wgt.finger_pinky.R", "wgt.finger_pinky.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_pinky_02.R", "wgt.finger_pinky_02.R")
moveBoneExt(sceneRig[0], "wgt.finger_pinky_02.R", "wgt.finger_pinky_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_ring_01.R", "wgt.finger_ring.R")
moveBoneExt(sceneRig[0], "wgt.finger_ring.R", "wgt.finger_ring.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_ring_02.R", "wgt.finger_ring_02.R")
moveBoneExt(sceneRig[0], "wgt.finger_ring_02.R", "wgt.finger_ring_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_index_01.R", "wgt.finger_index.R")
moveBoneExt(sceneRig[0], "wgt.finger_index.R", "wgt.finger_index.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_index_02.R", "wgt.finger_index_02.R")
moveBoneExt(sceneRig[0], "wgt.finger_index_02.R", "wgt.finger_index_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_thumb_01.R", "wgt.finger_thumb.R")
moveBoneExt(sceneRig[0], "wgt.finger_thumb.R", "wgt.finger_thumb.R", "head", [-0.00, -0.0, 0.03], [-0.00, -0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.finger_thumb_02.R", "wgt.finger_thumb_02.R")
moveBoneExt(sceneRig[0], "wgt.finger_thumb_02.R", "wgt.finger_thumb_02.R", "head", [-0.00, -0.01, 0.03], [-0.00, -0.01, 0.03])


## Chest WGT Bones ## 
moveBoneConXYZ(sceneRig[0], "def.chest_mass_02.C", "wgt.chest_mass_02.C", "head", "Z", -0.1)
moveBoneExt(sceneRig[0], "wgt.chest_mass_02.C", "wgt.chest_mass_02.C", "head", [-0.00, 0.03, -0.03], [-0.00, 0.03, -0.03])

moveBoneConXYZ(sceneRig[0], "def.chest_mass_01.C", "wgt.chest_mass_01.C", "head", "Z", -0.1)
moveBoneExt(sceneRig[0], "wgt.chest_mass_01.C", "wgt.chest_mass_01.C", "head", [-0.00, 0.03, -0.03], [-0.00, 0.03, -0.03])

## Face WGT Bones ## 
## Cheek WGT Bones Left ## 
moveBoneBasic(sceneRig[0], "ctl.cheek_side_01.L", "wgt.cheek_side_01.L")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.L", "wgt.cheek_front_02.L")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.L", "wgt.cheek_front_02.L")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.L", "wgt.cheek_front_02.L")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_03.L", "wgt.cheek_front_03.L")

## Cheek WGT Bones Right ## 
moveBoneBasic(sceneRig[0], "ctl.cheek_side_01.R", "wgt.cheek_side_01.R")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.R", "wgt.cheek_front_02.R")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.R", "wgt.cheek_front_02.R")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.R", "wgt.cheek_front_02.R")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_03.R", "wgt.cheek_front_03.R")

## Nose WGT Bones ## 
moveBoneConXYZ(sceneRig[0], "def.nose_01.C", "wgt.nose_02.C", "tail", "Y", -0.05)
moveBoneConXYZ(sceneRig[0], "def.nose_01.C", "wgt.nose_01.C", "tail", "Y", -0.08)

moveBoneBasic(sceneRig[0], "ctl.noseBridge_02.C", "wgt.noseBridge_02.C")
moveBoneExt(sceneRig[0], "wgt.noseBridge_02.C", "wgt.noseBridge_02.C", "head", [-0.00, -0.01, 0.01], [-0.00, -0.01, 0.01])

moveBoneBasic(sceneRig[0], "ctl.noseBridge_01.C", "wgt.noseBridge_01.C")
moveBoneExt(sceneRig[0], "wgt.noseBridge_01.C", "wgt.noseBridge_01.C", "head", [-0.00, -0.01, 0.01], [-0.00, -0.01, 0.01])


## Lip WGT ## 
moveBoneBasic(sceneRig[0], "ctl.lip_top_00.C", "wgt.lip_top_00.C")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_00.C", "wgt.lip_bot_00.C")

moveBoneBasic(sceneRig[0], "ctl.lip_top_01.L", "wgt.lip_top_01.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_02.L", "wgt.lip_top_02.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_03.L", "wgt.lip_top_03.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_04.L", "wgt.lip_top_04.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_05.L", "wgt.lip_top_05.L")

moveBoneBasic(sceneRig[0], "ctl.lip_top_01.R", "wgt.lip_top_01.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_02.R", "wgt.lip_top_02.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_03.R", "wgt.lip_top_03.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_04.R", "wgt.lip_top_04.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_05.R", "wgt.lip_top_05.R")

moveBoneBasic(sceneRig[0], "ctl.lip_bot_01.L", "wgt.lip_bot_01.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_02.L", "wgt.lip_bot_02.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_03.L", "wgt.lip_bot_03.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_04.L", "wgt.lip_bot_04.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_05.L", "wgt.lip_bot_05.L")

moveBoneBasic(sceneRig[0], "ctl.lip_bot_01.R", "wgt.lip_bot_01.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_02.R", "wgt.lip_bot_02.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_03.R", "wgt.lip_bot_03.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_04.R", "wgt.lip_bot_04.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_05.R", "wgt.lip_bot_05.R")

moveBoneBasic(sceneRig[0], "ctl.lip_corner.L", "wgt.lip_corner.L")
moveBoneBasic(sceneRig[0], "ctl.lip_corner.R", "wgt.lip_corner.R")

## Eye Brow WGT ## 
moveBoneBasic(sceneRig[0], "ctl.eyebrow_00.L", "wgt.eyebrow_00.L")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_01.L", "wgt.eyebrow_01.L")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_02.L", "wgt.eyebrow_02.L")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_03.L", "wgt.eyebrow_03.L")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_04.L", "wgt.eyebrow_04.L")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_05.L", "wgt.eyebrow_05.L")

moveBoneBasic(sceneRig[0], "ctl.eyebrow_00.R", "wgt.eyebrow_00.R")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_01.R", "wgt.eyebrow_01.R")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_02.R", "wgt.eyebrow_02.R")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_03.R", "wgt.eyebrow_03.R")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_04.R", "wgt.eyebrow_04.R")
moveBoneBasic(sceneRig[0], "ctl.eyebrow_05.R", "wgt.eyebrow_05.R")

moveBoneBasic(sceneRig[0], "ctl.eyebrow_main.R", "wgt.eyebrow_main.R")
moveBoneExt(sceneRig[0], "wgt.eyebrow_main.R", "wgt.eyebrow_main.R", "head", [-0.00, -0.01, 0.02], [-0.00, -0.01, 0.02])

moveBoneBasic(sceneRig[0], "ctl.eyebrow_main.L", "wgt.eyebrow_main.L")
moveBoneExt(sceneRig[0], "wgt.eyebrow_main.L", "wgt.eyebrow_main.L", "head", [-0.00, -0.01, 0.02], [-0.00, -0.01, 0.02])


## Eye Lid WGT Bones ## 
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_01.L", "wgt.eyelid_top_01.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_02.L", "wgt.eyelid_top_02.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_03.L", "wgt.eyelid_top_03.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_04.L", "wgt.eyelid_top_04.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_05.L", "wgt.eyelid_top_05.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_06.L", "wgt.eyelid_top_06.L")

moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_01.L", "wgt.eyelid_bot_01.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_02.L", "wgt.eyelid_bot_02.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_03.L", "wgt.eyelid_bot_03.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_04.L", "wgt.eyelid_bot_04.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_05.L", "wgt.eyelid_bot_05.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_06.L", "wgt.eyelid_bot_06.L")

moveBoneBasic(sceneRig[0], "ctl.eyelid_top_01.R", "wgt.eyelid_top_01.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_02.R", "wgt.eyelid_top_02.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_03.R", "wgt.eyelid_top_03.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_04.R", "wgt.eyelid_top_04.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_05.R", "wgt.eyelid_top_05.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_top_06.R", "wgt.eyelid_top_06.R")

moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_01.R", "wgt.eyelid_bot_01.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_02.R", "wgt.eyelid_bot_02.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_03.R", "wgt.eyelid_bot_03.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_04.R", "wgt.eyelid_bot_04.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_05.R", "wgt.eyelid_bot_05.R")
moveBoneBasic(sceneRig[0], "ctl.eyelid_bot_06.R", "wgt.eyelid_bot_06.R")

moveBoneBasic(sceneRig[0], "ctl.eyelid_corner_01.L", "wgt.eyelid_corner_01.L")
moveBoneBasic(sceneRig[0], "ctl.eyelid_corner_01.R", "wgt.eyelid_corner_01.R")


#################
### ACC Bones ###
#################

moveBoneBasic(sceneRig[0], "ctl.lip_bot_00.C", "acc.lip_bot_00.C")
moveBoneBasic(sceneRig[0], "ctl.lip_top_00.C", "acc.lips_top.C")
moveBoneBasic(sceneRig[0], "ctl.nose_02.C", "acc.nose_02.C")
moveBoneBasic(sceneRig[0], "ctl.nose_01.C", "acc.nose_01.C")
moveBoneBasic(sceneRig[0], "ctl.lowerJaw.C", "acc.lowerJaw.C")

moveBoneBasic(sceneRig[0], "ctl.cheek_front_03.L", "acc.cheek_front_03.L")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.L", "acc.cheek_front_02.L")
moveBoneBasic(sceneRig[0], "ctl.cheek_side_01.L", "acc.cheek_side_01.L")
moveBoneBasic(sceneRig[0], "ctl.lip_corner.L", "acc.lip_corner.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_05.L", "acc.lip_bot_05.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_05.L", "acc.lip_top_05.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_04.L", "acc.lip_bot_04.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_03.L", "acc.lip_bot_03.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_04.L", "acc.lip_top_04.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_02.L", "acc.lip_bot_02.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_03.L", "acc.lip_top_03.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_02.L", "acc.lip_top_02.L")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_01.L", "acc.lip_bot_01.L")
moveBoneBasic(sceneRig[0], "ctl.lip_top_01.L", "acc.lip_top_01.L")

moveBoneBasic(sceneRig[0], "ctl.cheek_front_03.R", "acc.cheek_front_03.R")
moveBoneBasic(sceneRig[0], "ctl.cheek_front_02.R", "acc.cheek_front_02.R")
moveBoneBasic(sceneRig[0], "ctl.cheek_side_01.R", "acc.cheek_side_01.R")
moveBoneBasic(sceneRig[0], "ctl.lip_corner.R", "acc.lip_corner.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_05.R", "acc.lip_bot_05.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_05.R", "acc.lip_top_05.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_04.R", "acc.lip_bot_04.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_03.R", "acc.lip_bot_03.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_04.R", "acc.lip_top_04.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_02.R", "acc.lip_bot_02.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_03.R", "acc.lip_top_03.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_02.R", "acc.lip_top_02.R")
moveBoneBasic(sceneRig[0], "ctl.lip_bot_01.R", "acc.lip_bot_01.R")
moveBoneBasic(sceneRig[0], "ctl.lip_top_01.R", "acc.lip_top_01.R")
