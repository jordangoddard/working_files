import bpy 
import math 
import mathutils




####################
## Move Functions ##
####################

#Get the name of the rig
sceneRig = bpy.context.selected_objects 
#change rig to edit mode
bpy.ops.object.mode_set(mode='EDIT')

print("")
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
        #print(r) 
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
        print("%s could not be found" % (defBone_1)) 
              
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
        c = characterRig.data.edit_bones[defBone].center
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
        elif headTail == 'center': 
            characterRig.data.edit_bones[auxBone].head = c
            characterRig.data.edit_bones[auxBone].tail = c
            if XYZ == "Y":              
                characterRig.data.edit_bones[auxBone].tail.y += conSize 
            elif XYZ == "Z":
                characterRig.data.edit_bones[auxBone].tail.z += conSize 
            else:
                characterRig.data.edit_bones[auxBone].tail.x += conSize      
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
            #print("custom")
            characterRig.data.edit_bones[auxBone].head = h
            characterRig.data.edit_bones[auxBone].tail = t
            characterRig.data.edit_bones[auxBone].head.z -= characterRig.data.edit_bones[auxBone].head.z
        elif bonePos == 'headMain':
            characterRig.data.edit_bones[auxBone].head = h    
        elif bonePos == 'tailMain':
            characterRig.data.edit_bones[auxBone].head = t    
        elif bonePos == 'eye':
             characterRig.data.edit_bones[auxBone].head.x -= characterRig.data.edit_bones[auxBone].head.x   
             characterRig.data.edit_bones[auxBone].tail.x -= characterRig.data.edit_bones[auxBone].tail.x   
        elif bonePos == 'eyeMid': 
            #print("custom")
            characterRig.data.edit_bones[auxBone].head = h
            characterRig.data.edit_bones[auxBone].tail = t
            characterRig.data.edit_bones[auxBone].head.x -= characterRig.data.edit_bones[auxBone].head.x  
            characterRig.data.edit_bones[auxBone].tail.x -= characterRig.data.edit_bones[auxBone].tail.x   
        #else: 
            #print("Nothing happened for this bone, make sure you entered a value.")            
    except: 
        print("%s could not be found" % (auxBone))


## This will move the initial IK Control bone. ## 
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
        #print(h)
        t = characterRig.data.edit_bones[defBone].tail.xyz
        #print(t)
        a = (t[0] - h[0]) * mul + t[0]
        b = (t[1] - h[1]) * mul + t[1]
        c = (t[2] - h[2]) * mul + t[2]
        nt = mathutils.Vector((a, b, c))
        #print(nt)
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
        #print(r) 
        characterRig.data.edit_bones[auxBone].roll = r    
    except: 
        print("%s did not roll" % (auxBone))     

## This will match a bones roll to another bones roll ## 
def rollBone(characterRig, defBone, auxBone):
    # Find roll 
    try:
        r = characterRig.data.edit_bones[defBone].roll 
        characterRig.data.edit_bones[auxBone].roll = r
    except: 
        print("%s did not roll" % (auxBone))
        
        
 
######################
## Head ORG and MCH ##
######################

####################
## Org Bones Move ##
####################

## Ear Org Bones Move ## 
moveBoneCenter(sceneRig[0], "def.ear_00.L", "org.ear_00.L")
moveBoneCenter(sceneRig[0], "def.ear_01.L", "org.ear_01.L")
moveBoneCenter(sceneRig[0], "def.ear_02.L", "org.ear_02.L")
moveBoneCenter(sceneRig[0], "def.ear_03.L", "org.ear_03.L")
moveBoneCenter(sceneRig[0], "def.ear_04.L", "org.ear_04.L")

moveBoneCenter(sceneRig[0], "def.ear_00.R", "org.ear_00.R")
moveBoneCenter(sceneRig[0], "def.ear_01.R", "org.ear_01.R")
moveBoneCenter(sceneRig[0], "def.ear_02.R", "org.ear_02.R")
moveBoneCenter(sceneRig[0], "def.ear_03.R", "org.ear_03.R")
moveBoneCenter(sceneRig[0], "def.ear_04.R", "org.ear_04.R")

## Forehead Org Bones ## 
moveBoneCenter(sceneRig[0], "def.forehead_00.L", "org.forehead_00.L")
moveBoneCenter(sceneRig[0], "def.forehead_01.L", "org.forehead_01.L")
moveBoneCenter(sceneRig[0], "def.forehead_02.L", "org.forehead_02.L")

moveBoneCenter(sceneRig[0], "def.forehead_00.R", "org.forehead_00.R")
moveBoneCenter(sceneRig[0], "def.forehead_01.R", "org.forehead_01.R")
moveBoneCenter(sceneRig[0], "def.forehead_02.R", "org.forehead_02.R")

## Nose Org Bones ## 
moveBoneCenter(sceneRig[0], "def.nose_00.C", "org.nose_00.C")
moveBoneCenter(sceneRig[0], "def.nose_01.C", "org.nose_01.C")
moveBoneCenter(sceneRig[0], "def.nose_02.C", "org.nose_02.C")
moveBoneCenter(sceneRig[0], "def.nose_03.C", "org.nose_03.C")
moveBoneCenter(sceneRig[0], "def.nose_04.C", "org.nose_04.C")

moveBoneCenter(sceneRig[0], "def.nose_00.L", "org.nose_00.L")
moveBoneCenter(sceneRig[0], "def.nose_01.L", "org.nose_01.L")
moveBoneCenter(sceneRig[0], "def.nose_02.L", "org.nose_02.L")

moveBoneCenter(sceneRig[0], "def.nose_00.R", "org.nose_00.R")
moveBoneCenter(sceneRig[0], "def.nose_01.R", "org.nose_01.R")
moveBoneCenter(sceneRig[0], "def.nose_02.R", "org.nose_02.R")

## Eyebrow Upper Org Bones ## 
moveBoneCenter(sceneRig[0], "def.eb_ring_00.L", "org.eb_ring_00.L")
moveBoneCenter(sceneRig[0], "def.eb_ring_01.L", "org.eb_ring_01.L")
moveBoneCenter(sceneRig[0], "def.eb_ring_02.L", "org.brow_t.L")
moveBoneCenter(sceneRig[0], "def.eb_ring_03.L", "org.brow_t_01.L")
moveBoneCenter(sceneRig[0], "def.eb_ring_04.L", "org.brow_t_02.L")
moveBoneCenter(sceneRig[0], "def.eb_ring_05.L", "org.brow_t_03.L")

moveBoneCenter(sceneRig[0], "def.eb_ring_00.R", "org.eb_ring_00.R")
moveBoneCenter(sceneRig[0], "def.eb_ring_01.R", "org.eb_ring_01.R")
moveBoneCenter(sceneRig[0], "def.eb_ring_02.R", "org.brow_t.R")
moveBoneCenter(sceneRig[0], "def.eb_ring_03.R", "org.brow_t_01.R")
moveBoneCenter(sceneRig[0], "def.eb_ring_04.R", "org.brow_t_02.R")
moveBoneCenter(sceneRig[0], "def.eb_ring_05.R", "org.brow_t_03.R")

## Eyebrow Lower Org Bones ## 
moveBoneCenter(sceneRig[0], "def.brow_b_00.L", "org.brow_b_00.L")
moveBoneCenter(sceneRig[0], "def.brow_b_01.L", "org.brow_b_01.L")
moveBoneCenter(sceneRig[0], "def.brow_b_02.L", "org.brow_b_02.L")
moveBoneCenter(sceneRig[0], "def.brow_b_03.L", "org.brow_b_03.L")

moveBoneCenter(sceneRig[0], "def.brow_b_00.R", "org.brow_b_00.R")
moveBoneCenter(sceneRig[0], "def.brow_b_01.R", "org.brow_b_01.R")
moveBoneCenter(sceneRig[0], "def.brow_b_02.R", "org.brow_b_02.R")
moveBoneCenter(sceneRig[0], "def.brow_b_03.R", "org.brow_b_03.R")

## Eye Lids Org Bones ## 
moveBoneBasic(sceneRig[0], "def.lid_t_00.L", "org.lid_t_00.L")
moveBoneBasic(sceneRig[0], "def.lid_t_01.L", "org.lid_t_01.L")
moveBoneBasic(sceneRig[0], "def.lid_t_02.L", "org.lid_t_02.L")
moveBoneBasic(sceneRig[0], "def.lid_t_03.L", "org.lid_t_03.L")

moveBoneBasic(sceneRig[0], "def.lid_t_00.R", "org.lid_t_00.R")
moveBoneBasic(sceneRig[0], "def.lid_t_01.R", "org.lid_t_01.R")
moveBoneBasic(sceneRig[0], "def.lid_t_02.R", "org.lid_t_02.R")
moveBoneBasic(sceneRig[0], "def.lid_t_03.R", "org.lid_t_03.R")

moveBoneBasic(sceneRig[0], "def.lid_b_00.L", "org.lid_b_00.L")
moveBoneBasic(sceneRig[0], "def.lid_b_01.L", "org.lid_b_01.L")
moveBoneBasic(sceneRig[0], "def.lid_b_02.L", "org.lid_b_02.L")
moveBoneBasic(sceneRig[0], "def.lid_b_03.L", "org.lid_b_03.L")

moveBoneBasic(sceneRig[0], "def.lid_b_00.R", "org.lid_b_00.R")
moveBoneBasic(sceneRig[0], "def.lid_b_01.R", "org.lid_b_01.R")
moveBoneBasic(sceneRig[0], "def.lid_b_02.R", "org.lid_b_02.R")
moveBoneBasic(sceneRig[0], "def.lid_b_03.R", "org.lid_b_03.R")

## Cheek Upper Org Bones ## 
moveBoneCenter(sceneRig[0], "def.cheek_t_00.L", "org.cheek_t_00.L")
moveBoneCenter(sceneRig[0], "def.cheek_t_01.L", "org.cheek_t_01.L")
moveBoneCenter(sceneRig[0], "def.cheek_t_02.L", "org.cheek_t_02.L")
moveBoneCenter(sceneRig[0], "def.cheek_t_03.L", "org.cheek_t_03.L")

moveBoneCenter(sceneRig[0], "def.cheek_t_00.R", "org.cheek_t_00.R")
moveBoneCenter(sceneRig[0], "def.cheek_t_01.R", "org.cheek_t_01.R")
moveBoneCenter(sceneRig[0], "def.cheek_t_02.R", "org.cheek_t_02.R")
moveBoneCenter(sceneRig[0], "def.cheek_t_03.R", "org.cheek_t_03.R")

## Temple Org Bones ## 
moveBoneCenter(sceneRig[0], "def.temple.L", "org.temple.L")
moveBoneCenter(sceneRig[0], "def.temple.R", "org.temple.R")

## Jaw Org Bones ## 
moveBoneCenter(sceneRig[0], "def.jaw_00.L", "org.jaw_00.L")
moveBoneCenter(sceneRig[0], "def.jaw_01.L", "org.jaw_01.L")
moveBoneCenter(sceneRig[0], "def.jaw_02.L", "org.jaw_02.L")
moveBoneCenter(sceneRig[0], "def.jaw_03.L", "org.jaw_03.L")

moveBoneCenter(sceneRig[0], "def.jaw_00.R", "org.jaw_00.R")
moveBoneCenter(sceneRig[0], "def.jaw_01.R", "org.jaw_01.R")
moveBoneCenter(sceneRig[0], "def.jaw_02.R", "org.jaw_02.R")
moveBoneCenter(sceneRig[0], "def.jaw_03.R", "org.jaw_03.R")

moveBoneCenter(sceneRig[0], "def.jaw_lower_01.L", "org.jaw_lower_01.L")
moveBoneCenter(sceneRig[0], "def.jaw_lower_01.R", "org.jaw_lower_01.R")

moveBoneCenter(sceneRig[0], "def.jaw.C", "org.jaw.C")

## Cheek Ring Org Bones ## 
moveBoneCenter(sceneRig[0], "def.cheek_ring_t_00.L", "org.cheek_ring_t_00.L")
moveBoneCenter(sceneRig[0], "def.cheek_ring_t_01.L", "org.cheek_ring_t_01.L")
moveBoneCenter(sceneRig[0], "def.cheek_ring_t_02.L", "org.cheek_ring_t_02.L")

moveBoneCenter(sceneRig[0], "def.cheek_ring_t_00.R", "org.cheek_ring_t_00.R")
moveBoneCenter(sceneRig[0], "def.cheek_ring_t_01.R", "org.cheek_ring_t_01.R")
moveBoneCenter(sceneRig[0], "def.cheek_ring_t_02.R", "org.cheek_ring_t_02.R")

## Cheek Ring and Con Org Bones ## 
moveBoneCenter(sceneRig[0], "def.lip_con_00.L", "org.lip_con_00.L")
moveBoneCenter(sceneRig[0], "def.lip_con_01.L", "org.lip_con_01.L")

moveBoneCenter(sceneRig[0], "def.lip_con_00.R", "org.lip_con_00.R")
moveBoneCenter(sceneRig[0], "def.lip_con_01.R", "org.lip_con_01.R")

moveBoneCenter(sceneRig[0], "def.chin_con_00.L", "org.chin_con_00.L")
moveBoneCenter(sceneRig[0], "def.chin_con_00.R", "org.chin_con_00.R")

moveBoneCenter(sceneRig[0], "def.jaw_con_00.L", "org.jaw_con_00.L")
moveBoneCenter(sceneRig[0], "def.jaw_con_00.R", "org.jaw_con_00.R")


moveBoneCenter(sceneRig[0], "def.chin_00.C", "org.chin_00.C")
moveBoneCenter(sceneRig[0], "def.chin_01.C", "org.chin_01.C")
moveBoneCenter(sceneRig[0], "def.chin_02.C", "org.chin_02.C")
moveBoneCenter(sceneRig[0], "def.chin_03.C", "org.chin_03.C")

moveBoneCenter(sceneRig[0], "def.chin_ring_b_00.L", "org.chin_ring_b_00.L")
moveBoneCenter(sceneRig[0], "def.chin_ring_b_01.L", "org.chin_ring_b_01.L")
moveBoneCenter(sceneRig[0], "def.chin_ring_b_02.L", "org.chin_ring_b_02.L")

moveBoneCenter(sceneRig[0], "def.chin_ring_b_00.L", "org.chin_ring_b_00.L")
moveBoneCenter(sceneRig[0], "def.chin_ring_b_01.L", "org.chin_ring_b_01.L")
moveBoneCenter(sceneRig[0], "def.chin_ring_b_02.L", "org.chin_ring_b_02.L")

moveBoneCenter(sceneRig[0], "def.chin_ring_b_00.R", "org.chin_ring_b_00.R")
moveBoneCenter(sceneRig[0], "def.chin_ring_b_01.R", "org.chin_ring_b_01.R")
moveBoneCenter(sceneRig[0], "def.chin_ring_b_02.R", "org.chin_ring_b_02.R")

## Lip Ring Outer Org Bones ## 
moveBoneCenter(sceneRig[0], "def.lip_ring_b_00.L", "org.lip_ring_b_00.L")
moveBoneCenter(sceneRig[0], "def.lip_ring_b_01.L", "org.lip_ring_b_01.L")
moveBoneCenter(sceneRig[0], "def.lip_ring_b_02.L", "org.lip_ring_b_02.L")

moveBoneCenter(sceneRig[0], "def.lip_ring_b_00.R", "org.lip_ring_b_00.R")
moveBoneCenter(sceneRig[0], "def.lip_ring_b_01.R", "org.lip_ring_b_01.R")
moveBoneCenter(sceneRig[0], "def.lip_ring_b_02.R", "org.lip_ring_b_02.R")

moveBoneCenter(sceneRig[0], "def.lip_ring_t_00.L", "org.lip_ring_t_00.L")
moveBoneCenter(sceneRig[0], "def.lip_ring_t_01.L", "org.lip_ring_t_01.L")
moveBoneCenter(sceneRig[0], "def.lip_ring_t_02.L", "org.lip_ring_t_02.L")

moveBoneCenter(sceneRig[0], "def.lip_ring_t_00.R", "org.lip_ring_t_00.R")
moveBoneCenter(sceneRig[0], "def.lip_ring_t_01.R", "org.lip_ring_t_01.R")
moveBoneCenter(sceneRig[0], "def.lip_ring_t_02.R", "org.lip_ring_t_02.R")


## Lips Org Bones ##
moveBoneCenter(sceneRig[0], "def.lip_t_00.L", "org.lip_t_00.L")
moveBoneCenter(sceneRig[0], "def.lip_t_01.L", "org.lip_t_01.L")
moveBoneCenter(sceneRig[0], "def.lip_t_02.L", "org.lip_t_02.L")
moveBoneCenter(sceneRig[0], "def.lip_t_03.L", "org.lip_t_03.L")

moveBoneCenter(sceneRig[0], "def.lip_t_00.R", "org.lip_t_00.R")
moveBoneCenter(sceneRig[0], "def.lip_t_01.R", "org.lip_t_01.R")
moveBoneCenter(sceneRig[0], "def.lip_t_02.R", "org.lip_t_02.R")
moveBoneCenter(sceneRig[0], "def.lip_t_03.R", "org.lip_t_03.R")

moveBoneCenter(sceneRig[0], "def.lip_b_00.L", "org.lip_b_00.L")
moveBoneCenter(sceneRig[0], "def.lip_b_01.L", "org.lip_b_01.L")
moveBoneCenter(sceneRig[0], "def.lip_b_02.L", "org.lip_b_02.L")
moveBoneCenter(sceneRig[0], "def.lip_b_03.L", "org.lip_b_03.L")

moveBoneCenter(sceneRig[0], "def.lip_b_00.R", "org.lip_b_00.R")
moveBoneCenter(sceneRig[0], "def.lip_b_01.R", "org.lip_b_01.R")
moveBoneCenter(sceneRig[0], "def.lip_b_02.R", "org.lip_b_02.R")
moveBoneCenter(sceneRig[0], "def.lip_b_03.R", "org.lip_b_03.R")

## Teeth Org Bones ## 
moveBoneBasic(sceneRig[0], "def.teeth_t.C", "org.teeth_t.C")
moveBoneBasic(sceneRig[0], "def.teeth_b.C", "org.teeth_b.C")

## Tongue Org Bones ## 
moveBoneBasic(sceneRig[0], "def.tongue_00.C", "org.tongue_00.C")
moveBoneBasic(sceneRig[0], "def.tongue_01.C", "org.tongue_01.C")
moveBoneBasic(sceneRig[0], "def.tongue_02.C", "org.tongue_02.C")

####################
## Org Bones Roll ##
####################


## Ear Org Bones Move ## 
rollBone(sceneRig[0], "def.ear_00.L", "org.ear_00.L")
rollBone(sceneRig[0], "def.ear_01.L", "org.ear_01.L")
rollBone(sceneRig[0], "def.ear_02.L", "org.ear_02.L")
rollBone(sceneRig[0], "def.ear_03.L", "org.ear_03.L")
rollBone(sceneRig[0], "def.ear_04.L", "org.ear_04.L")

rollBone(sceneRig[0], "def.ear_00.R", "org.ear_00.R")
rollBone(sceneRig[0], "def.ear_01.R", "org.ear_01.R")
rollBone(sceneRig[0], "def.ear_02.R", "org.ear_02.R")
rollBone(sceneRig[0], "def.ear_03.R", "org.ear_03.R")
rollBone(sceneRig[0], "def.ear_04.R", "org.ear_04.R")

## Forehead Org Bones ## 
rollBone(sceneRig[0], "def.forehead_00.L", "org.forehead_00.L")
rollBone(sceneRig[0], "def.forehead_01.L", "org.forehead_01.L")
rollBone(sceneRig[0], "def.forehead_02.L", "org.forehead_02.L")

rollBone(sceneRig[0], "def.forehead_00.R", "org.forehead_00.R")
rollBone(sceneRig[0], "def.forehead_01.R", "org.forehead_01.R")
rollBone(sceneRig[0], "def.forehead_02.R", "org.forehead_02.R")

## Nose Org Bones ## 
rollBone(sceneRig[0], "def.nose_00.C", "org.nose_00.C")
rollBone(sceneRig[0], "def.nose_01.C", "org.nose_01.C")
rollBone(sceneRig[0], "def.nose_02.C", "org.nose_02.C")
rollBone(sceneRig[0], "def.nose_03.C", "org.nose_03.C")
rollBone(sceneRig[0], "def.nose_04.C", "org.nose_04.C")

rollBone(sceneRig[0], "def.nose_00.L", "org.nose_00.L")
rollBone(sceneRig[0], "def.nose_01.L", "org.nose_01.L")
rollBone(sceneRig[0], "def.nose_02.L", "org.nose_02.L")

rollBone(sceneRig[0], "def.nose_00.R", "org.nose_00.R")
rollBone(sceneRig[0], "def.nose_01.R", "org.nose_01.R")
rollBone(sceneRig[0], "def.nose_02.R", "org.nose_02.R")

## Eyebrow Upper Org Bones ## 
rollBone(sceneRig[0], "def.eb_ring_00.L", "org.eb_ring_00.L")
rollBone(sceneRig[0], "def.eb_ring_01.L", "org.eb_ring_01.L")
rollBone(sceneRig[0], "def.eb_ring_02.L", "org.brow_t.L")
rollBone(sceneRig[0], "def.eb_ring_03.L", "org.brow_t_01.L")
rollBone(sceneRig[0], "def.eb_ring_04.L", "org.brow_t_02.L")
rollBone(sceneRig[0], "def.eb_ring_05.L", "org.brow_t_03.L")

rollBone(sceneRig[0], "def.eb_ring_00.R", "org.eb_ring_00.R")
rollBone(sceneRig[0], "def.eb_ring_01.R", "org.eb_ring_01.R")
rollBone(sceneRig[0], "def.eb_ring_02.R", "org.brow_t.R")
rollBone(sceneRig[0], "def.eb_ring_03.R", "org.brow_t_01.R")
rollBone(sceneRig[0], "def.eb_ring_04.R", "org.brow_t_02.R")
rollBone(sceneRig[0], "def.eb_ring_05.R", "org.brow_t_03.R")

## Eyebrow Lower Org Bones ## 
rollBone(sceneRig[0], "def.brow_b_00.L", "org.brow_b_00.L")
rollBone(sceneRig[0], "def.brow_b_01.L", "org.brow_b_01.L")
rollBone(sceneRig[0], "def.brow_b_02.L", "org.brow_b_02.L")
rollBone(sceneRig[0], "def.brow_b_03.L", "org.brow_b_03.L")

rollBone(sceneRig[0], "def.brow_b_00.R", "org.brow_b_00.R")
rollBone(sceneRig[0], "def.brow_b_01.R", "org.brow_b_01.R")
rollBone(sceneRig[0], "def.brow_b_02.R", "org.brow_b_02.R")
rollBone(sceneRig[0], "def.brow_b_03.R", "org.brow_b_03.R")

## Eye Lids Org Bones ## 
rollBone(sceneRig[0], "def.lid_t_00.L", "org.lid_t_00.L")
rollBone(sceneRig[0], "def.lid_t_01.L", "org.lid_t_01.L")
rollBone(sceneRig[0], "def.lid_t_02.L", "org.lid_t_02.L")
rollBone(sceneRig[0], "def.lid_t_03.L", "org.lid_t_03.L")

rollBone(sceneRig[0], "def.lid_t_00.R", "org.lid_t_00.R")
rollBone(sceneRig[0], "def.lid_t_01.R", "org.lid_t_01.R")
rollBone(sceneRig[0], "def.lid_t_02.R", "org.lid_t_02.R")
rollBone(sceneRig[0], "def.lid_t_03.R", "org.lid_t_03.R")

rollBone(sceneRig[0], "def.lid_b_00.L", "org.lid_b_00.L")
rollBone(sceneRig[0], "def.lid_b_01.L", "org.lid_b_01.L")
rollBone(sceneRig[0], "def.lid_b_02.L", "org.lid_b_02.L")
rollBone(sceneRig[0], "def.lid_b_03.L", "org.lid_b_03.L")

rollBone(sceneRig[0], "def.lid_b_00.R", "org.lid_b_00.R")
rollBone(sceneRig[0], "def.lid_b_01.R", "org.lid_b_01.R")
rollBone(sceneRig[0], "def.lid_b_02.R", "org.lid_b_02.R")
rollBone(sceneRig[0], "def.lid_b_03.R", "org.lid_b_03.R")

## Cheek Upper Org Bones ## 
rollBone(sceneRig[0], "def.cheek_t_00.L", "org.cheek_t_00.L")
rollBone(sceneRig[0], "def.cheek_t_01.L", "org.cheek_t_01.L")
rollBone(sceneRig[0], "def.cheek_t_02.L", "org.cheek_t_02.L")
rollBone(sceneRig[0], "def.cheek_t_03.L", "org.cheek_t_03.L")

rollBone(sceneRig[0], "def.cheek_t_00.R", "org.cheek_t_00.R")
rollBone(sceneRig[0], "def.cheek_t_01.R", "org.cheek_t_01.R")
rollBone(sceneRig[0], "def.cheek_t_02.R", "org.cheek_t_02.R")
rollBone(sceneRig[0], "def.cheek_t_03.R", "org.cheek_t_03.R")

## Temple Org Bones ## 
rollBone(sceneRig[0], "def.temple.L", "org.temple.L")
rollBone(sceneRig[0], "def.temple.R", "org.temple.R")

## Jaw Org Bones ## 
rollBone(sceneRig[0], "def.jaw_00.L", "org.jaw_00.L")
rollBone(sceneRig[0], "def.jaw_01.L", "org.jaw_01.L")
rollBone(sceneRig[0], "def.jaw_02.L", "org.jaw_02.L")
rollBone(sceneRig[0], "def.jaw_03.L", "org.jaw_03.L")

rollBone(sceneRig[0], "def.jaw_00.R", "org.jaw_00.R")
rollBone(sceneRig[0], "def.jaw_01.R", "org.jaw_01.R")
rollBone(sceneRig[0], "def.jaw_02.R", "org.jaw_02.R")
rollBone(sceneRig[0], "def.jaw_03.R", "org.jaw_03.R")

rollBone(sceneRig[0], "def.jaw_lower_01.L", "org.jaw_lower_01.L")
rollBone(sceneRig[0], "def.jaw_lower_01.R", "org.jaw_lower_01.R")

rollBone(sceneRig[0], "def.jaw.C", "org.jaw.C")

## Cheek Ring Org Bones ## 
rollBone(sceneRig[0], "def.cheek_ring_t_00.L", "org.cheek_ring_t_00.L")
rollBone(sceneRig[0], "def.cheek_ring_t_01.L", "org.cheek_ring_t_01.L")
rollBone(sceneRig[0], "def.cheek_ring_t_02.L", "org.cheek_ring_t_02.L")

rollBone(sceneRig[0], "def.cheek_ring_t_00.R", "org.cheek_ring_t_00.R")
rollBone(sceneRig[0], "def.cheek_ring_t_01.R", "org.cheek_ring_t_01.R")
rollBone(sceneRig[0], "def.cheek_ring_t_02.R", "org.cheek_ring_t_02.R")

## Cheek Ring and Con Org Bones ## 
rollBone(sceneRig[0], "def.lip_con_00.L", "org.lip_con_00.L")
rollBone(sceneRig[0], "def.lip_con_01.L", "org.lip_con_01.L")

rollBone(sceneRig[0], "def.lip_con_00.R", "org.lip_con_00.R")
rollBone(sceneRig[0], "def.lip_con_01.R", "org.lip_con_01.R")

rollBone(sceneRig[0], "def.chin_con_00.L", "org.chin_con_00.L")
rollBone(sceneRig[0], "def.chin_con_00.R", "org.chin_con_00.R")

rollBone(sceneRig[0], "def.jaw_con_00.L", "org.jaw_con_00.L")
rollBone(sceneRig[0], "def.jaw_con_00.R", "org.jaw_con_00.R")


rollBone(sceneRig[0], "def.chin_00.C", "org.chin_00.C")
rollBone(sceneRig[0], "def.chin_01.C", "org.chin_01.C")
rollBone(sceneRig[0], "def.chin_02.C", "org.chin_02.C")
rollBone(sceneRig[0], "def.chin_03.C", "org.chin_03.C")

rollBone(sceneRig[0], "def.chin_ring_b_00.L", "org.chin_ring_b_00.L")
rollBone(sceneRig[0], "def.chin_ring_b_01.L", "org.chin_ring_b_01.L")
rollBone(sceneRig[0], "def.chin_ring_b_02.L", "org.chin_ring_b_02.L")

rollBone(sceneRig[0], "def.chin_ring_b_00.L", "org.chin_ring_b_00.L")
rollBone(sceneRig[0], "def.chin_ring_b_01.L", "org.chin_ring_b_01.L")
rollBone(sceneRig[0], "def.chin_ring_b_02.L", "org.chin_ring_b_02.L")

rollBone(sceneRig[0], "def.chin_ring_b_00.R", "org.chin_ring_b_00.R")
rollBone(sceneRig[0], "def.chin_ring_b_01.R", "org.chin_ring_b_01.R")
rollBone(sceneRig[0], "def.chin_ring_b_02.R", "org.chin_ring_b_02.R")

## Lip Ring Outer Org Bones ## 
rollBone(sceneRig[0], "def.lip_ring_b_00.L", "org.lip_ring_b_00.L")
rollBone(sceneRig[0], "def.lip_ring_b_01.L", "org.lip_ring_b_01.L")
rollBone(sceneRig[0], "def.lip_ring_b_02.L", "org.lip_ring_b_02.L")

rollBone(sceneRig[0], "def.lip_ring_b_00.R", "org.lip_ring_b_00.R")
rollBone(sceneRig[0], "def.lip_ring_b_01.R", "org.lip_ring_b_01.R")
rollBone(sceneRig[0], "def.lip_ring_b_02.R", "org.lip_ring_b_02.R")

rollBone(sceneRig[0], "def.lip_ring_t_00.L", "org.lip_ring_t_00.L")
rollBone(sceneRig[0], "def.lip_ring_t_01.L", "org.lip_ring_t_01.L")
rollBone(sceneRig[0], "def.lip_ring_t_02.L", "org.lip_ring_t_02.L")

rollBone(sceneRig[0], "def.lip_ring_t_00.R", "org.lip_ring_t_00.R")
rollBone(sceneRig[0], "def.lip_ring_t_01.R", "org.lip_ring_t_01.R")
rollBone(sceneRig[0], "def.lip_ring_t_02.R", "org.lip_ring_t_02.R")


## Lips Org Bones ##
rollBone(sceneRig[0], "def.lip_t_00.L", "org.lip_t_00.L")
rollBone(sceneRig[0], "def.lip_t_01.L", "org.lip_t_01.L")
rollBone(sceneRig[0], "def.lip_t_02.L", "org.lip_t_02.L")
rollBone(sceneRig[0], "def.lip_t_03.L", "org.lip_t_03.L")

rollBone(sceneRig[0], "def.lip_t_00.R", "org.lip_t_00.R")
rollBone(sceneRig[0], "def.lip_t_01.R", "org.lip_t_01.R")
rollBone(sceneRig[0], "def.lip_t_02.R", "org.lip_t_02.R")
rollBone(sceneRig[0], "def.lip_t_03.R", "org.lip_t_03.R")

rollBone(sceneRig[0], "def.lip_b_00.L", "org.lip_b_00.L")
rollBone(sceneRig[0], "def.lip_b_01.L", "org.lip_b_01.L")
rollBone(sceneRig[0], "def.lip_b_02.L", "org.lip_b_02.L")
rollBone(sceneRig[0], "def.lip_b_03.L", "org.lip_b_03.L")

rollBone(sceneRig[0], "def.lip_b_00.R", "org.lip_b_00.R")
rollBone(sceneRig[0], "def.lip_b_01.R", "org.lip_b_01.R")
rollBone(sceneRig[0], "def.lip_b_02.R", "org.lip_b_02.R")
rollBone(sceneRig[0], "def.lip_b_03.R", "org.lip_b_03.R")

## Teeth Org Bones ## 
rollBone(sceneRig[0], "def.teeth_t.C", "org.teeth_t.C")
rollBone(sceneRig[0], "def.teeth_b.C", "org.teeth_b.C")

## Tongue Org Bones ## 
rollBone(sceneRig[0], "def.tongue_00.C", "org.tongue_00.C")
rollBone(sceneRig[0], "def.tongue_01.C", "org.tongue_01.C")
rollBone(sceneRig[0], "def.tongue_02.C", "org.tongue_02.C")


####################
## MCH Face Bones ##
####################

## MCH Eye Bones ## 
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_t_00.L", "mch.lid_t_00.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_t_01.L", "mch.lid_t_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_t_02.L", "mch.lid_t_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_t_03.L", "mch.lid_t_03.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_b_00.L", "mch.lid_b_00.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_b_01.L", "mch.lid_b_01.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_b_02.L", "mch.lid_b_02.L")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.L", "def.lid_b_03.L", "mch.lid_b_03.L")

moveBoneBasic(sceneRig[0], "org.eye.L", "mch.eye_00.L")
moveBoneConXYZ(sceneRig[0], "org.eye.L", "mch.eye_01.L", "tail", "Z", 0.01)

moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_t_00.R", "mch.lid_t_00.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_t_01.R", "mch.lid_t_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_t_02.R", "mch.lid_t_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_t_03.R", "mch.lid_t_03.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_b_00.R", "mch.lid_b_00.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_b_01.R", "mch.lid_b_01.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_b_02.R", "mch.lid_b_02.R")
moveBoneTwoBoneBasic(sceneRig[0], "org.eye.R", "def.lid_b_03.R", "mch.lid_b_03.R")

moveBoneBasic(sceneRig[0], "org.eye.R", "mch.eye_00.R")
moveBoneConXYZ(sceneRig[0], "org.eye.R", "mch.eye_01.R", "tail", "Z", 0.01)

## MCH Jaw Bones ## 

moveBoneTwoBoneBasic(sceneRig[0], "def.tongue_01.C", "def.tongue_00.C", "mch.tongue_01.C")
moveBoneTwoBoneBasic(sceneRig[0], "def.tongue_01.C", "def.tongue_00.C", "mch.tongue_02.C")

moveBoneTwoBoneBasic(sceneRig[0], "mch.jaw_master_04.C", "def.chin_00.C", "mch.mouth_lock.C") 

moveBoneScale(sceneRig[0], "mch.mouth_lock.C", "mch.jaw_master_04.C", -.8)  
moveBoneScale(sceneRig[0], "mch.mouth_lock.C", "mch.jaw_master_03.C", -.7)  
moveBoneScale(sceneRig[0], "mch.mouth_lock.C", "mch.jaw_master_02_1.C", -.6)  
moveBoneScale(sceneRig[0], "mch.mouth_lock.C", "mch.jaw_master_02.C", -.5)  
moveBoneScale(sceneRig[0], "mch.mouth_lock.C", "mch.jaw_master_01.C", -.4) 
moveBoneScale(sceneRig[0], "mch.mouth_lock.C", "mch.jaw_master_00.C", -.3) 

## MCH Face ## 
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_02.L", "mch.lip_ring_t_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_b_02.L", "mch.lip_ring_b_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_03.L", "mch.lips_top_02.L", "head", "Y", 0.005)
moveBoneConXYZ(sceneRig[0], "def.lip_b_03.L", "mch.lips_bot_02.L", "head", "Y", 0.005)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_b_01.L", "mch.lip_ring_b_01.L", "head", "Y", 0.02)

moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_02.R", "mch.lip_ring_t_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_b_02.R", "mch.lip_ring_b_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_03.R", "mch.lips_top_02.R", "head", "Y", 0.005)
moveBoneConXYZ(sceneRig[0], "def.lip_b_03.R", "mch.lips_bot_02.R", "head", "Y", 0.005)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_b_01.R", "mch.lip_ring_b_01.R", "head", "Y", 0.02)

moveBoneConXYZ(sceneRig[0], "def.cheek_t_02.R", "mch.sub_cheek_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_02.L", "mch.sub_cheek_01.R", "head", "Y", 0.02)

moveBoneConXYZ(sceneRig[0], "def.chin_03.C", "mch.chin_03.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_00.L", "mch.lips_bot.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_00.L", "mch.lips_top.C", "head", "Y", 0.02)

############################
### Body MCH, IK and ORG ###
############################

### ORG ### 

## Spine ORG Bones ## 
moveBoneBasic(sceneRig[0], "def.spine_00.C", "org.spine_00.C")
moveBoneBasic(sceneRig[0], "def.spine_01.C", "org.spine_01.C")
moveBoneBasic(sceneRig[0], "def.spine_02.C", "org.spine_02.C")
moveBoneBasic(sceneRig[0], "def.spine_03.C", "org.spine_03.C")
moveBoneBasic(sceneRig[0], "def.spine_04.C", "org.spine_04.C")
moveBoneBasic(sceneRig[0], "def.spine_05.C", "org.spine_05.C")
moveBoneBasic(sceneRig[0], "def.spine_06.C", "org.spine_06.C")

moveBoneScale(sceneRig[0], "def.spine_06.C", "org.face.C", -.5)    

## Shoulder ORG Bone ## 
moveBoneBasic(sceneRig[0], "def.shoulder.L", "org.shoulder.L")
moveBoneBasic(sceneRig[0], "def.shoulder.R", "org.shoulder.R")

## Arm ORG Bone ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.L", "def.forarm_00.L", "org.upper_arm.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.L", "def.forarm_00.L", "org.upper_arm.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.R", "def.forarm_00.R", "org.upper_arm.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.R", "def.forarm_00.R", "org.upper_arm.R")

## Hand ORG Bone 
moveBoneBasic(sceneRig[0], "def.hand.L", "org.hand.L")
moveBoneBasic(sceneRig[0], "def.palm_01.L", "org.palm_01.L")
moveBoneBasic(sceneRig[0], "def.palm_02.L", "org.palm_02.L")
moveBoneBasic(sceneRig[0], "def.palm_03.L", "org.palm_03.L")
moveBoneBasic(sceneRig[0], "def.palm_04.L", "org.palm_04.L")

moveBoneBasic(sceneRig[0], "def.thumb_01.L", "org.thumb_01.L")
moveBoneBasic(sceneRig[0], "def.thumb_02.L", "org.thumb_02.L")
moveBoneBasic(sceneRig[0], "def.thumb_03.L", "org.thumb_03.L")

moveBoneBasic(sceneRig[0], "def.f_index_01.L", "org.f_index_01.L")
moveBoneBasic(sceneRig[0], "def.f_index_02.L", "org.f_index_02.L")
moveBoneBasic(sceneRig[0], "def.f_index_03.L", "org.f_index_03.L")

moveBoneBasic(sceneRig[0], "def.f_middle_01.L", "org.f_middle_01.L")
moveBoneBasic(sceneRig[0], "def.f_middle_02.L", "org.f_middle_02.L")
moveBoneBasic(sceneRig[0], "def.f_middle_03.L", "org.f_middle_03.L")

moveBoneBasic(sceneRig[0], "def.f_ring_01.L", "org.f_ring_01.L")
moveBoneBasic(sceneRig[0], "def.f_ring_02.L", "org.f_ring_02.L")
moveBoneBasic(sceneRig[0], "def.f_ring_03.L", "org.f_ring_03.L")

moveBoneBasic(sceneRig[0], "def.f_pinky_01.L", "org.f_pinky_01.L")
moveBoneBasic(sceneRig[0], "def.f_pinky_02.L", "org.f_pinky_02.L")
moveBoneBasic(sceneRig[0], "def.f_pinky_03.L", "org.f_pinky_03.L")

moveBoneBasic(sceneRig[0], "def.hand.R", "org.hand.R")
moveBoneBasic(sceneRig[0], "def.palm_01.R", "org.palm_01.R")
moveBoneBasic(sceneRig[0], "def.palm_02.R", "org.palm_02.R")
moveBoneBasic(sceneRig[0], "def.palm_03.R", "org.palm_03.R")
moveBoneBasic(sceneRig[0], "def.palm_04.R", "org.palm_04.R")

moveBoneBasic(sceneRig[0], "def.thumb_01.R", "org.thumb_01.R")
moveBoneBasic(sceneRig[0], "def.thumb_02.R", "org.thumb_02.R")
moveBoneBasic(sceneRig[0], "def.thumb_03.R", "org.thumb_03.R")

moveBoneBasic(sceneRig[0], "def.f_index_01.R", "org.f_index_01.R")
moveBoneBasic(sceneRig[0], "def.f_index_02.R", "org.f_index_02.R")
moveBoneBasic(sceneRig[0], "def.f_index_03.R", "org.f_index_03.R")

moveBoneBasic(sceneRig[0], "def.f_middle_01.R", "org.f_middle_01.R")
moveBoneBasic(sceneRig[0], "def.f_middle_02.R", "org.f_middle_02.R")
moveBoneBasic(sceneRig[0], "def.f_middle_03.R", "org.f_middle_03.R")

moveBoneBasic(sceneRig[0], "def.f_ring_01.R", "org.f_ring_01.R")
moveBoneBasic(sceneRig[0], "def.f_ring_02.R", "org.f_ring_02.R")
moveBoneBasic(sceneRig[0], "def.f_ring_03.R", "org.f_ring_03.R")

moveBoneBasic(sceneRig[0], "def.f_pinky_01.R", "org.f_pinky_01.R")
moveBoneBasic(sceneRig[0], "def.f_pinky_02.R", "org.f_pinky_02.R")
moveBoneBasic(sceneRig[0], "def.f_pinky_03.R", "org.f_pinky_03.R")

## Breast ORG Bone ## 
moveBoneBasic(sceneRig[0], "def.breast.L", "org.breast.L")
moveBoneBasic(sceneRig[0], "def.breast.R", "org.breast.R")

## Leg Bone ORG ## 
moveBoneBasic(sceneRig[0], "def.pelvis.L", "org.pelvis.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.L", "def.shin_00.L", "org.thigh.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.shin_00.L", "def.foot.L", "org.shin.L")
moveBoneBasic(sceneRig[0], "def.foot.L", "org.foot.L")
moveBoneBasic(sceneRig[0], "def.toe.L", "org.toe.L")

moveBoneBasic(sceneRig[0], "def.pelvis.R", "org.pelvis.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.R", "def.shin_00.R", "org.thigh.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.shin_00.R", "def.foot.R", "org.shin.R")
moveBoneBasic(sceneRig[0], "def.foot.R", "org.foot.R")
moveBoneBasic(sceneRig[0], "def.toe.R", "org.toe.R")

## MCH Bones ## 

## Spine MCH Bones  ## 
moveBoneConXYZ(sceneRig[0], "def.spine_06.C", "mch.eyes_parent.C", "head", "Z", 0.02)
moveBoneConXYZ(sceneRig[0], "def.spine_06.C", "mch.rot_head.C", "head", "Y", 0.1)
moveBoneTwoBoneBasic(sceneRig[0],  "def.spine_04.C", "def.spine_06.C", "mch.str_neck.C")
moveBoneScale(sceneRig[0], "def.spine_05.C", "mch.spine_05.C", -.5)   
moveBoneConXYZ(sceneRig[0], "def.spine_04.C", "mch.rot_neck.C", "head", "Y", 0.1)
moveBoneBasic(sceneRig[0], "def.spine_03.C", "mch.wgt_chest")
moveBoneConXYZ(sceneRig[0], "def.spine_03.C", "mch.spine_03.C", "head", "Y", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.pivot.C", "head", "Y", 0.1)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.spine_02.C", "head", "Y", 0.12)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.spine_01.C", "head", "Y", 0.12)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "mch.spine_01", "head", "Y", 0.12)
moveBoneConXYZ(sceneRig[0], "def.spine_01.C", "mch.spine_00.C", "head", "Y", 0.1)
moveBoneBasic(sceneRig[0], "def.spine_00.C", "wgt.hips.C")

## Arm MCH Bones ## 
moveBoneConXYZ(sceneRig[0], "def.upper_arm_00.L", "mch.upper_arm_parent.L", "head", "Y", 0.05)
moveBoneScale(sceneRig[0], "def.upper_arm_00.L", "mch.upper_arm_tweak_00.L", -.6) 
moveBoneScale(sceneRig[0], "def.upper_arm_01.L", "mch.upper_arm_tweak_01.L", -.6) 
moveBoneScale(sceneRig[0], "def.forarm_00.L", "mch.forearm_tweak_00.L", -.6) 
moveBoneScale(sceneRig[0], "def.forarm_01.L", "mch.forearm_tweak_01.L", -.6) 
moveBoneScale(sceneRig[0], "def.hand.L", "mch.upper_arm_ik_target.L", -.7) 
moveBoneScale(sceneRig[0], "def.hand.L", "mch.hand_fk.L", -.7)
moveBoneScale(sceneRig[0], "def.hand.L", "mch.hand_tweak.L", -.9)
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.L", "def.hand.L", "mch.upper_arm_ik_stretch.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.forarm_00.L", "def.hand.L", "ikk.upper_arm_ik.L")

moveBoneConXYZ(sceneRig[0], "def.upper_arm_00.R", "mch.upper_arm_parent.R", "head", "Y", 0.05)
moveBoneScale(sceneRig[0], "def.upper_arm_00.R", "mch.upper_arm_tweak_00.R", -.6) 
moveBoneScale(sceneRig[0], "def.upper_arm_01.R", "mch.upper_arm_tweak_01.R", -.6) 
moveBoneScale(sceneRig[0], "def.forarm_00.R", "mch.forearm_tweak_00.R", -.6) 
moveBoneScale(sceneRig[0], "def.forarm_01.R", "mch.forearm_tweak_01.R", -.6) 
moveBoneScale(sceneRig[0], "def.hand.R", "mch.upper_arm_ik_target.R", -.7) 
moveBoneScale(sceneRig[0], "def.hand.R", "mch.hand_fk.R", -.7)
moveBoneScale(sceneRig[0], "def.hand.R", "mch.hand_tweak.R", -.9)
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.R", "def.hand.R", "mch.upper_arm_ik_stretch.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.forarm_00.R", "def.hand.R", "ikk.upper_arm_ik.R")

## Leg MCH Bones ##
moveBoneConXYZ(sceneRig[0], "def.thigh_00.L", "mch.thigh_parent.L", 'head', "Y", 0.07)
moveBoneScale(sceneRig[0], "def.thigh_00.L", "mch.thigh_tweak_00.L", -.7) 
moveBoneScale(sceneRig[0], "def.thigh_01.L", "mch.thigh_tweak_01.L", -.7) 
moveBoneScale(sceneRig[0], "def.shin_00.L", "mch.shin_tweak_00.L", -.7) 
moveBoneScale(sceneRig[0], "def.shin_01.L", "mch.shin_tweak_01.L", -.7) 
moveBoneScale(sceneRig[0], "def.shin_01.L", "mch.foot_tweak.L", .2) 
moveBoneExt(sceneRig[0], "def.foot.L", "mch.foot_tweak.L", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneTwoBoneBasic(sceneRig[0], "def.shin_00.L", "def.foot.L", "ikk.thigh_ik.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.L", "def.foot.L", "mch.thigh_ik_stretch.L")
moveBoneScale(sceneRig[0], "def.foot.L", "mch.thigh_ik_target.L", -.8) 
moveBoneScale(sceneRig[0], "def.foot.L", "mch.foot_fk.L", -.8) 
moveBoneTwoBoneBasic(sceneRig[0], "def.toe.L", "def.foot.L", "mch.heel_02_roll.L")
moveBoneConXYZ(sceneRig[0], "org.heel.L", "mch.heel_02_rock.L", "tail", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "org.heel.L", "mch.heel_02_rock_01.L", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "org.heel.L", "mch.heel_02_roll_01.L", "center", "Y", -0.03)

moveBoneConXYZ(sceneRig[0], "def.thigh_00.R", "mch.thigh_parent.R", "head", "Y", 0.07)
moveBoneScale(sceneRig[0], "def.thigh_00.R", "mch.thigh_tweak_00.R", -.7) 
moveBoneScale(sceneRig[0], "def.thigh_01.R", "mch.thigh_tweak_01.R", -.7) 
moveBoneScale(sceneRig[0], "def.shin_00.R", "mch.shin_tweak_00.R", -.7) 
moveBoneScale(sceneRig[0], "def.shin_01.R", "mch.shin_tweak_01.R", -.7) 
moveBoneScale(sceneRig[0], "def.shin_01.R", "mch.foot_tweak.R", .2) 
moveBoneExt(sceneRig[0], "def.foot.R", "mch.foot_tweak.R", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneTwoBoneBasic(sceneRig[0], "def.shin_00.R", "def.foot.R", "ikk.thigh_ik.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.R", "def.foot.R", "mch.thigh_ik_stretch.R")
moveBoneScale(sceneRig[0], "def.foot.R", "mch.thigh_ik_target.R", -.8) 
moveBoneScale(sceneRig[0], "def.foot.R", "mch.foot_fk.R", -.8) 
moveBoneTwoBoneBasic(sceneRig[0], "def.toe.R", "def.foot.R", "mch.heel_02_roll.R")
moveBoneConXYZ(sceneRig[0], "org.heel.R", "mch.heel_02_rock_00.R", "tail", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "org.heel.R", "mch.heel_02_rock_01.R", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "org.heel.R", "mch.heel_02_roll_01.R", "center", "Y", -0.03)

####################
### Secondary IK ###
####################

## Leg Secondary IK Bones ## 
moveBoneScale(sceneRig[0], "def.foot.L", "mch.pole_trans_change.L", -.7) 
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.L", "def.shin_00.L", "mch.ik_thigh.L")
moveBoneIKCon(sceneRig[0], "def.thigh_00.L", "def.shin_01.L", "mch.leg_pole_point.L") 
moveBoneScale(sceneRig[0], "mch.leg_pole_point.L", "mch.pole_trans_bot.L", 1.7) 
moveBoneExt(sceneRig[0], "def.foot.L", "mch.pole_trans_bot.L", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneScale(sceneRig[0], "mch.leg_pole_point.L", "mch.pole_trans_top.L", -.7) 
moveBoneExt(sceneRig[0], "def.thigh_00.L", "mch.pole_trans_top.L", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneScale(sceneRig[0], "mch.pole_trans_top.L", "mch.pole_trans_top.L", -.7) 
moveBoneConXYZ(sceneRig[0], "org.heel.L", "mch.ik_foot_cog.L", "center", "Y", -0.045)
moveBoneExt(sceneRig[0], "mch.ik_foot_cog.L", "mch.ik_foot_cog.L", "head", [0.0, -0.03, -0.0], [0.0, -0.03, -0.0]) 
moveBoneConXYZ(sceneRig[0], "mch.ik_foot_cog.L", "mch.ik_foot_hip.L", "head", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "mch.ik_foot_cog.L", "mch.ik_foot_parent.L", "head", "Y", -0.09)

moveBoneScale(sceneRig[0], "def.foot.R", "mch.pole_trans_change.R", -.7) 
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.R", "def.shin_00.R", "mch.ik_thigh.R")
moveBoneIKCon(sceneRig[0], "def.thigh_00.R", "def.shin_01.R", "mch.leg_pole_point.R") 
moveBoneScale(sceneRig[0], "mch.leg_pole_point.R", "mch.pole_trans_bot.R", 1.7) 
moveBoneExt(sceneRig[0], "def.foot.R", "mch.pole_trans_bot.R", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0]) 
moveBoneScale(sceneRig[0], "mch.leg_pole_point.R", "mch.pole_trans_top.R", -.7) 
moveBoneExt(sceneRig[0], "def.thigh_00.R", "mch.pole_trans_top.R", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneScale(sceneRig[0], "mch.pole_trans_top.R", "mch.pole_trans_top.R", -.7) 
moveBoneConXYZ(sceneRig[0], "org.heel.R", "mch.ik_foot_cog.R", "center", "Y", -0.045)
moveBoneExt(sceneRig[0], "mch.ik_foot_cog.R", "mch.ik_foot_cog.R", "head", [0.0, -0.03, -0.0], [0.0, -0.03, -0.0]) 
moveBoneConXYZ(sceneRig[0], "mch.ik_foot_cog.R", "mch.ik_foot_hip.R", "head", "Y", -0.1)
moveBoneConXYZ(sceneRig[0], "mch.ik_foot_cog.R", "mch.ik_foot_parent.R", "head", "Y", -0.09)

## Foot WGT Bones ##
moveBoneConXYZ(sceneRig[0], "def.toe.L", "wgt.ik_foot.L", "head", "Y", 0.15)
moveBoneConXYZ(sceneRig[0], "def.toe.R", "wgt.ik_foot.R", "head", "Y", 0.15)

moveBoneConXYZ(sceneRig[0], "def.toe.L", "wgt.foot_down_ik.L", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "wgt.foot_down_ik.L", "wgt.foot_down_ik.L", "head", [0.0, 0.15, 0.04], [0.0, 0.15, 0.04]) 

moveBoneConXYZ(sceneRig[0], "def.toe.R", "wgt.foot_down_ik.R", "head", "Y", 0.05)
moveBoneExt(sceneRig[0], "wgt.foot_down_ik.R", "wgt.foot_down_ik.R", "head", [0.0, 0.15, 0.04], [0.0, 0.15, 0.04]) 

## Arm Secondart IK Bones ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.L", "def.forarm_00.L", "ikk.upperarm.ik.L")
moveBoneBasic(sceneRig[0], "ikk.upperarm.ik.L", "mch.ik_arm_upper.L")
moveBoneScale(sceneRig[0], "ikk.upperarm.ik.L", "mch.IKH-upperarm.L", .4) 
moveBoneExt(sceneRig[0], "def.forarm_00.L", "mch.IKH-upperarm.L", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0]) 
moveBoneIKCon(sceneRig[0], "def.upper_arm_00.L", "def.forarm_01.L", "mch.arm_pole_point.L") 
moveBoneScale(sceneRig[0], "mch.arm_pole_point.L", "mch.pole_top_trans.L", -.7) 
moveBoneExt(sceneRig[0], "def.upper_arm_00.L", "mch.pole_top_trans.L", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneScale(sceneRig[0], "mch.pole_top_trans.L", "mch.pole_top_trans.L", -.7) 

moveBoneScale(sceneRig[0], "mch.arm_pole_point.L", "mch.pole_bot_trans.L", 2) 
moveBoneExt(sceneRig[0], "def.hand.L", "mch.pole_bot_trans.L", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.R", "def.forarm_00.R", "ikk.upperarm.ik.R")
moveBoneBasic(sceneRig[0], "ikk.upperarm.ik.R", "mch.ik_arm_upper.R")
moveBoneScale(sceneRig[0], "ikk.upperarm.ik.R", "mch.IKH-upperarm.R", .4) 
moveBoneExt(sceneRig[0], "def.forarm_00.R", "mch.IKH-upperarm.R", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0]) 
moveBoneIKCon(sceneRig[0], "def.upper_arm_00.R", "def.forarm_01.R", "mch.arm_pole_point.R") 
moveBoneScale(sceneRig[0], "mch.arm_pole_point.R", "mch.pole_top_trans.R", -.7) 
moveBoneExt(sceneRig[0], "def.upper_arm_00.R", "mch.pole_top_trans.R", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])
moveBoneScale(sceneRig[0], "mch.pole_top_trans.R", "mch.pole_top_trans.R", -.7) 

moveBoneScale(sceneRig[0], "mch.arm_pole_point.R", "mch.pole_bot_trans.R", 2) 
moveBoneExt(sceneRig[0], "def.hand.R", "mch.pole_bot_trans.R", "headMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

## Hand secondary MCH Bones ## 
moveBoneScale(sceneRig[0], "def.hand.L", "mch.hand_space_change.L", -.2) 
moveBoneScale(sceneRig[0], "def.hand.L", "mch.hand_cog_space.L", -.3) 
moveBoneScale(sceneRig[0], "def.hand.L", "mch.hand_chest_space.L", -.4) 

moveBoneScale(sceneRig[0], "def.thumb_01.L", "mch.thumb_01.L", -.4) 
moveBoneScale(sceneRig[0], "def.f_index_01.L", "mch.f_index_01.L", -.4) 
moveBoneScale(sceneRig[0], "def.f_middle_01.L", "mch.f_middle_01.L", -.4) 
moveBoneScale(sceneRig[0], "def.f_ring_01.L", "mch.f_ring_01.L", -.4) 
moveBoneScale(sceneRig[0], "def.f_pinky_01.L", "mch.f_pinky_01.L", -.4) 

moveBoneScale(sceneRig[0], "def.hand.R", "mch.hand_space_change.R", -.2) 
moveBoneScale(sceneRig[0], "def.hand.R", "mch.hand_cog_space.R", -.3) 
moveBoneScale(sceneRig[0], "def.hand.R", "mch.hand_chest_space.R", -.4) 

moveBoneScale(sceneRig[0], "def.thumb_01.R", "mch.thumb_01.R", -.4) 
moveBoneScale(sceneRig[0], "def.f_index_01.R", "mch.f_index_01.R", -.4) 
moveBoneScale(sceneRig[0], "def.f_middle_01.R", "mch.f_middle_01.R", -.4) 
moveBoneScale(sceneRig[0], "def.f_ring_01.R", "mch.f_ring_01.R", -.4) 
moveBoneScale(sceneRig[0], "def.f_pinky_01.R", "mch.f_pinky_01.R", -.4) 

######################
### CTL Bones Body ###
######################

## Arm CTL IK Bones ## 
moveBoneBasic(sceneRig[0], "def.hand.L", "ctl.ik_hand.L")
moveBoneConXYZ(sceneRig[0], "mch.arm_pole_point.L", "ctl.arm_pole.L", "head", "Y", 0.1)
moveBoneExt(sceneRig[0], "ctl.arm_pole.L", "ctl.arm_pole.L", "head", [0.0, 0.45, 0.0], [0.0, 0.45, 0.0]) 
moveBoneConXYZ(sceneRig[0], "def.hand.L", "ctl.arm_config.L", "head", "Y", 0.1)
moveBoneExt(sceneRig[0], "ctl.arm_config.L", "ctl.arm_config.L", "head", [0.3, -0.2, -0.15], [0.3, -0.2, -0.15]) 

moveBoneBasic(sceneRig[0], "def.hand.R", "ctl.ik_hand.R")
moveBoneConXYZ(sceneRig[0], "mch.arm_pole_point.R", "ctl.arm_pole.R", "head", "Y", 0.1)
moveBoneExt(sceneRig[0], "ctl.arm_pole.R", "ctl.arm_pole.R", "head", [0.0, 0.45, 0.0], [0.0, 0.45, 0.0]) 
moveBoneConXYZ(sceneRig[0], "def.hand.R", "ctl.arm_config.R", "head", "Y", 0.1)
moveBoneExt(sceneRig[0], "ctl.arm_config.R", "ctl.arm_config.R", "head", [-0.3, -0.2, -0.15], [-0.3, -0.2, -0.15]) 

## Arm CTL FK Bones ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.L", "def.forarm_00.L", "ctl.fk_arm_upper.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.forarm_00.L", "def.hand.L", "ctl.fk_forarm.L")
moveBoneBasic(sceneRig[0], "def.hand.L", "ctl.fk_hand.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.upper_arm_00.R", "def.forarm_00.R", "ctl.fk_arm_upper.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.forarm_00.R", "def.hand.R", "ctl.fk_forarm.R")
moveBoneBasic(sceneRig[0], "def.hand.R", "ctl.fk_hand.R")

## Arm CTL Tweaker Bones ## 
moveBoneScale(sceneRig[0], "def.upper_arm_00.L", "ctl.twk_arm_upper_01.L", -.6)
moveBoneScale(sceneRig[0], "def.upper_arm_01.L", "ctl.twk_arm_upper_02.L", -.6)
moveBoneScale(sceneRig[0], "def.forarm_00.L", "ctl.twk_forarm_02.L", -.6)
moveBoneScale(sceneRig[0], "def.forarm_01.L", "ctl.twk_forarm_01.L", -.6)
moveBoneScale(sceneRig[0], "def.hand.L", "ctl.twk_hand.L", -.6)

moveBoneScale(sceneRig[0], "def.upper_arm_00.R", "ctl.twk_arm_upper_01.R", -.6)
moveBoneScale(sceneRig[0], "def.upper_arm_01.R", "ctl.twk_arm_upper_02.R", -.6)
moveBoneScale(sceneRig[0], "def.forarm_00.R", "ctl.twk_forarm_02.R", -.6)
moveBoneScale(sceneRig[0], "def.forarm_01.R", "ctl.twk_forarm_01.R", -.6)
moveBoneScale(sceneRig[0], "def.hand.R", "ctl.twk_hand.R", -.6)

## Arm CTL Tweaker Bones WGT Add ons ## 
moveBoneBasic(sceneRig[0], "ctl.twk_arm_upper_01.L", "wgt.twk_arm_upper_01.L")
moveBoneExt(sceneRig[0], "wgt.twk_arm_upper_01.L", "wgt.twk_arm_upper_01.L", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_arm_upper_02.L", "wgt.twk_arm_upper_02.L")
moveBoneExt(sceneRig[0], "wgt.twk_arm_upper_02.L", "wgt.twk_arm_upper_02.L", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_forarm_02.L", "wgt.twk_forarm_02.L")
moveBoneExt(sceneRig[0], "wgt.twk_forarm_02.L", "wgt.twk_forarm_02.L", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_forarm_01.L", "wgt.twk_forarm_01.L")
moveBoneExt(sceneRig[0], "wgt.twk_forarm_01.L", "wgt.twk_forarm_01.L", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_hand.L", "wgt.twk_hand.L")
moveBoneExt(sceneRig[0], "wgt.twk_hand.L", "wgt.twk_hand.L", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])

moveBoneBasic(sceneRig[0], "ctl.twk_arm_upper_01.R", "wgt.twk_arm_upper_01.R")
moveBoneExt(sceneRig[0], "wgt.twk_arm_upper_01.R", "wgt.twk_arm_upper_01.R", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_arm_upper_02.R", "wgt.twk_arm_upper_02.R")
moveBoneExt(sceneRig[0], "wgt.twk_arm_upper_02.R", "wgt.twk_arm_upper_02.R", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_forarm_02.R", "wgt.twk_forarm_02.R")
moveBoneExt(sceneRig[0], "wgt.twk_forarm_02.R", "wgt.twk_forarm_02.R", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_forarm_01.R", "wgt.twk_forarm_01.R")
moveBoneExt(sceneRig[0], "wgt.twk_forarm_01.R", "wgt.twk_forarm_01.R", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])
moveBoneBasic(sceneRig[0], "ctl.twk_hand.R", "wgt.twk_hand.R")
moveBoneExt(sceneRig[0], "wgt.twk_hand.R", "wgt.twk_hand.R", "head", [-0.0, -0.0, 0.1], [-0.0, 0.0, 0.1])

## Leg CTL IK Bones ## 
moveBoneConXYZ(sceneRig[0], "def.shin_01.L", "ctl.ik_foot.L", "tail", "Y", 0.1)
moveBoneConXYZ(sceneRig[0], "def.shin_01.L", "ctl.ik_heel.L", "tail", "Y", 0.08)
moveBoneBasic(sceneRig[0], "def.toe.L", "ctl.toe.L")
moveBoneConXYZ(sceneRig[0], "def.toe.L", "ctl.foot_down_ik.L", "head", "Y", 0.08)
moveBoneConXYZ(sceneRig[0], "def.toe.L", "ctl.toeIK.L", "tail", "Y", 0.09)

moveBoneConXYZ(sceneRig[0], "def.toe.L", "ctl.leg_config.L", "tail", "Y", 0.09)
moveBoneExt(sceneRig[0], "ctl.leg_config.L", "ctl.leg_config.L", "head", [-0.0, -0.2, -0.0], [-0.0, -0.2, -0.0])

moveBoneConXYZ(sceneRig[0], "mch.leg_pole_point.L", "ctl.leg_pole.L", "head", "Y", -0.1)
moveBoneExt(sceneRig[0], "ctl.leg_pole.L", "ctl.leg_pole.L", "head", [-0.0, -0.35, -0.0], [-0.0, -0.35, -0.0])

moveBoneConXYZ(sceneRig[0], "def.shin_01.R", "ctl.ik_foot.R", "tail", "Y", 0.1)
moveBoneConXYZ(sceneRig[0], "def.shin_01.R", "ctl.ik_heel.R", "tail", "Y", 0.08)
moveBoneBasic(sceneRig[0], "def.toe.R", "ctl.toe.R")
moveBoneConXYZ(sceneRig[0], "def.toe.R", "ctl.foot_down_ik.R", "head", "Y", 0.08)
moveBoneConXYZ(sceneRig[0], "def.toe.R", "ctl.toeIK.R", "tail", "Y", 0.09)

moveBoneConXYZ(sceneRig[0], "def.toe.R", "ctl.leg_config.R", "tail", "Y", 0.09)
moveBoneExt(sceneRig[0], "ctl.leg_config.R", "ctl.leg_config.R", "head", [-0.0, -0.2, -0.0], [-0.0, -0.2, -0.0])

moveBoneConXYZ(sceneRig[0], "mch.leg_pole_point.R", "ctl.leg_pole.R", "head", "Y", -0.1)
moveBoneExt(sceneRig[0], "ctl.leg_pole.R", "ctl.leg_pole.R", "head", [-0.0, -0.35, -0.0], [-0.0, -0.35, -0.0])

## Leg CTL FK Bones ## 
moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.L", "def.shin_00.L", "ctl.fk_thigh.L")
moveBoneTwoBoneBasic(sceneRig[0], "def.shin_00.L","def.foot.L", "ctl.fk_shin.L")
moveBoneBasic(sceneRig[0], "def.foot.L", "ctl.fk_foot.L")

moveBoneTwoBoneBasic(sceneRig[0], "def.thigh_00.R", "def.shin_00.R", "ctl.fk_thigh.R")
moveBoneTwoBoneBasic(sceneRig[0], "def.shin_00.R","def.foot.R", "ctl.fk_shin.R")
moveBoneBasic(sceneRig[0], "def.foot.R", "ctl.fk_foot.R")

## Leg CTL tweaker Bones ## 
moveBoneScale(sceneRig[0], "def.thigh_00.L", "ctl.twk_thigh_02.L", -.45)
moveBoneScale(sceneRig[0], "def.thigh_01.L", "ctl.twk_thigh_01.L", -.45)
moveBoneScale(sceneRig[0], "def.shin_00.L", "ctl.twk_shin_02.L", -.45)
moveBoneScale(sceneRig[0], "def.shin_01.L", "ctl.twk_shin_01.L", -.45)
moveBoneScale(sceneRig[0], "def.foot.L", "ctl.twk_foot.L", -.45)

moveBoneScale(sceneRig[0], "def.thigh_00.R", "ctl.twk_thigh_02.R", -.45)
moveBoneScale(sceneRig[0], "def.thigh_01.R", "ctl.twk_thigh_01.R", -.45)
moveBoneScale(sceneRig[0], "def.shin_00.R", "ctl.twk_shin_02.R", -.45)
moveBoneScale(sceneRig[0], "def.shin_01.R", "ctl.twk_shin_01.R", -.45)
moveBoneScale(sceneRig[0], "def.foot.R", "ctl.twk_foot.R", -.45)

## Hand Ctl and Ctl Tweaker bones ## 

## Left Hand ##
moveBoneBasic(sceneRig[0], "def.hand.L", "ctl.handGrab.L")
moveBoneExt(sceneRig[0], "ctl.handGrab.L", "ctl.handGrab.L", "head", [0.0, 0.05, 0.05], [0.0, 0.05, 0.05])
moveBoneBasic(sceneRig[0], "def.palm_04.L", "ctl.palm.L")

moveBoneBasic(sceneRig[0], "def.thumb_01.L", "ctl.thumb_01.L")
moveBoneBasic(sceneRig[0], "def.thumb_02.L", "ctl.thumb_02.L")
moveBoneBasic(sceneRig[0], "def.thumb_03.L", "ctl.thumb_03.L")
moveBoneScale(sceneRig[0], "ctl.thumb_03.L", "ctl.twk_thumb_04.L", .6)
moveBoneExt(sceneRig[0], "ctl.thumb_03.L", "ctl.twk_thumb_04.L", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "ctl.thumb_01.L", "ctl.twk_thumb_01.L", -.6)
moveBoneScale(sceneRig[0], "ctl.thumb_02.L", "ctl.twk_thumb_02.L", -.6)
moveBoneScale(sceneRig[0], "ctl.thumb_03.L", "ctl.twk_thumb_03.L", -.6)

moveBoneBasic(sceneRig[0], "def.thumb_01.L", "ctl.thumbRoll.L")
moveBoneExt(sceneRig[0], "ctl.thumbRoll.L", "ctl.thumbRoll.L", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.f_index_01.L", "ctl.f_index_01.L")
moveBoneBasic(sceneRig[0], "def.f_index_02.L", "ctl.f_index_02.L")
moveBoneBasic(sceneRig[0], "def.f_index_03.L", "ctl.f_index_03.L")
moveBoneScale(sceneRig[0], "ctl.f_index_03.L", "ctl.twk_index_04.L", .6)
moveBoneExt(sceneRig[0], "ctl.f_index_03.L", "ctl.twk_index_04.L", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_index_01.L", "ctl.twk_index_01.L", -.6)
moveBoneScale(sceneRig[0], "def.f_index_02.L", "ctl.twk_index_02.L", -.6)
moveBoneScale(sceneRig[0], "def.f_index_03.L", "ctl.twk_index_03.L", -.6)

moveBoneBasic(sceneRig[0], "def.f_index_01.L", "ctl.indexRoll.L")
moveBoneExt(sceneRig[0], "ctl.indexRoll.L", "ctl.indexRoll.L", "head", [0.0, 0.0, 0.035], [0.0, 0.0, 0.035])

moveBoneBasic(sceneRig[0], "def.f_middle_01.L", "ctl.f_middle_01.L")
moveBoneBasic(sceneRig[0], "def.f_middle_02.L", "ctl.f_middle_02.L")
moveBoneBasic(sceneRig[0], "def.f_middle_03.L", "ctl.f_middle_03.L")
moveBoneScale(sceneRig[0], "ctl.f_middle_03.L", "ctl.twk_mid_04.L", .6)
moveBoneExt(sceneRig[0], "ctl.f_middle_03.L", "ctl.twk_mid_04.L", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_middle_01.L", "ctl.twk_mid_01.L", -.6)
moveBoneScale(sceneRig[0], "def.f_middle_02.L", "ctl.twk_mid_02.L", -.6)
moveBoneScale(sceneRig[0], "def.f_middle_03.L", "ctl.twk_mid_03.L", -.6)

moveBoneBasic(sceneRig[0], "def.f_middle_01.L", "ctl.middleRoll.L")
moveBoneExt(sceneRig[0], "ctl.middleRoll.L", "ctl.middleRoll.L", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.f_ring_01.L", "ctl.f_ring_01.L")
moveBoneBasic(sceneRig[0], "def.f_ring_02.L", "ctl.f_ring_02.L")
moveBoneBasic(sceneRig[0], "def.f_ring_03.L", "ctl.f_ring_03.L")
moveBoneScale(sceneRig[0], "ctl.f_ring_03.L", "ctl.twk_ring_04.L", .6)
moveBoneExt(sceneRig[0], "ctl.f_ring_03.L", "ctl.twk_ring_04.L", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_ring_01.L", "ctl.twk_ring_01.L", -.6)
moveBoneScale(sceneRig[0], "def.f_ring_02.L", "ctl.twk_ring_02.L", -.6)
moveBoneScale(sceneRig[0], "def.f_ring_03.L", "ctl.twk_ring_03.L", -.6)

moveBoneBasic(sceneRig[0], "def.f_ring_01.L", "ctl.ringRoll.L")
moveBoneExt(sceneRig[0], "ctl.ringRoll.L", "ctl.ringRoll.L", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.f_pinky_01.L", "ctl.f_pinky_01.L")
moveBoneBasic(sceneRig[0], "def.f_pinky_02.L", "ctl.f_pinky_02.L")
moveBoneBasic(sceneRig[0], "def.f_pinky_03.L", "ctl.f_pinky_03.L")
moveBoneScale(sceneRig[0], "ctl.f_pinky_03.L", "ctl.twk_pinky_04.L", .6)
moveBoneExt(sceneRig[0], "ctl.f_pinky_03.L", "ctl.twk_pinky_04.L", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_pinky_01.L", "ctl.twk_pinky_01.L", -.6)
moveBoneScale(sceneRig[0], "def.f_pinky_02.L", "ctl.twk_pinky_02.L", -.6)
moveBoneScale(sceneRig[0], "def.f_pinky_03.L", "ctl.twk_pinky_03.L", -.6)

moveBoneBasic(sceneRig[0], "def.f_pinky_01.L", "ctl.pinkyRoll.L")
moveBoneExt(sceneRig[0], "ctl.pinkyRoll.L", "ctl.pinkyRoll.L", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])


## Right Hand ##
moveBoneBasic(sceneRig[0], "def.hand.R", "ctl.handGrab.R")
moveBoneExt(sceneRig[0], "ctl.handGrab.R", "ctl.handGrab.R", "head", [0.0, 0.05, 0.05], [0.0, 0.05, 0.05])
moveBoneBasic(sceneRig[0], "def.palm_04.R", "ctl.palm.R")

moveBoneBasic(sceneRig[0], "def.thumb_01.R", "ctl.thumb_01.R")
moveBoneBasic(sceneRig[0], "def.thumb_02.R", "ctl.thumb_02.R")
moveBoneBasic(sceneRig[0], "def.thumb_03.R", "ctl.thumb_03.R")
moveBoneScale(sceneRig[0], "ctl.thumb_03.R", "ctl.twk_thumb_04.R", .6)
moveBoneExt(sceneRig[0], "ctl.thumb_03.R", "ctl.twk_thumb_04.R", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "ctl.thumb_01.R", "ctl.twk_thumb_01.R", -.6)
moveBoneScale(sceneRig[0], "ctl.thumb_02.R", "ctl.twk_thumb_02.R", -.6)
moveBoneScale(sceneRig[0], "ctl.thumb_03.R", "ctl.twk_thumb_03.R", -.6)

moveBoneBasic(sceneRig[0], "def.thumb_01.R", "ctl.thumbRoll.R")
moveBoneExt(sceneRig[0], "ctl.thumbRoll.R", "ctl.thumbRoll.R", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.f_index_01.R", "ctl.f_index_01.R")
moveBoneBasic(sceneRig[0], "def.f_index_02.R", "ctl.f_index_02.R")
moveBoneBasic(sceneRig[0], "def.f_index_03.R", "ctl.f_index_03.R")
moveBoneScale(sceneRig[0], "ctl.f_index_03.R", "ctl.twk_index_04.R", .6)
moveBoneExt(sceneRig[0], "ctl.f_index_03.R", "ctl.twk_index_04.R", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_index_01.R", "ctl.twk_index_01.R", -.6)
moveBoneScale(sceneRig[0], "def.f_index_02.R", "ctl.twk_index_02.R", -.6)
moveBoneScale(sceneRig[0], "def.f_index_03.R", "ctl.twk_index_03.R", -.6)

moveBoneBasic(sceneRig[0], "def.f_index_01.R", "ctl.indexRoll.R")
moveBoneExt(sceneRig[0], "ctl.indexRoll.R", "ctl.indexRoll.R", "head", [0.0, 0.0, 0.035], [0.0, 0.0, 0.035])

moveBoneBasic(sceneRig[0], "def.f_middle_01.R", "ctl.f_middle_01.R")
moveBoneBasic(sceneRig[0], "def.f_middle_02.R", "ctl.f_middle_02.R")
moveBoneBasic(sceneRig[0], "def.f_middle_03.R", "ctl.f_middle_03.R")
moveBoneScale(sceneRig[0], "ctl.f_middle_03.R", "ctl.twk_mid_04.R", .6)
moveBoneExt(sceneRig[0], "ctl.f_middle_03.R", "ctl.twk_mid_04.R", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_middle_01.R", "ctl.twk_mid_01.R", -.6)
moveBoneScale(sceneRig[0], "def.f_middle_02.R", "ctl.twk_mid_02.R", -.6)
moveBoneScale(sceneRig[0], "def.f_middle_03.R", "ctl.twk_mid_03.R", -.6)

moveBoneBasic(sceneRig[0], "def.f_middle_01.R", "ctl.middleRoll.R")
moveBoneExt(sceneRig[0], "ctl.middleRoll.R", "ctl.middleRoll.R", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.f_ring_01.R", "ctl.f_ring_01.R")
moveBoneBasic(sceneRig[0], "def.f_ring_02.R", "ctl.f_ring_02.R")
moveBoneBasic(sceneRig[0], "def.f_ring_03.R", "ctl.f_ring_03.R")
moveBoneScale(sceneRig[0], "ctl.f_ring_03.R", "ctl.twk_ring_04.R", .6)
moveBoneExt(sceneRig[0], "ctl.f_ring_03.R", "ctl.twk_ring_04.R", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_ring_01.R", "ctl.twk_ring_01.R", -.6)
moveBoneScale(sceneRig[0], "def.f_ring_02.R", "ctl.twk_ring_02.R", -.6)
moveBoneScale(sceneRig[0], "def.f_ring_03.R", "ctl.twk_ring_03.R", -.6)

moveBoneBasic(sceneRig[0], "def.f_ring_01.R", "ctl.ringRoll.R")
moveBoneExt(sceneRig[0], "ctl.ringRoll.R", "ctl.ringRoll.R", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])

moveBoneBasic(sceneRig[0], "def.f_pinky_01.R", "ctl.f_pinky_01.R")
moveBoneBasic(sceneRig[0], "def.f_pinky_02.R", "ctl.f_pinky_02.R")
moveBoneBasic(sceneRig[0], "def.f_pinky_03.R", "ctl.f_pinky_03.R")
moveBoneScale(sceneRig[0], "ctl.f_pinky_03.R", "ctl.twk_pinky_04.R", .6)
moveBoneExt(sceneRig[0], "ctl.f_pinky_03.R", "ctl.twk_pinky_04.R", "tailMain", [0.0, 0.0, -0.0], [0.0, 0.0, -0.0])

moveBoneScale(sceneRig[0], "def.f_pinky_01.R", "ctl.twk_pinky_01.R", -.6)
moveBoneScale(sceneRig[0], "def.f_pinky_02.R", "ctl.twk_pinky_02.R", -.6)
moveBoneScale(sceneRig[0], "def.f_pinky_03.R", "ctl.twk_pinky_003.R", -.6)

moveBoneBasic(sceneRig[0], "def.f_pinky_01.R", "ctl.pinkyRoll.R")
moveBoneExt(sceneRig[0], "ctl.pinkyRoll.R", "ctl.pinkyRoll.R", "head", [0.0, 0.0, 0.03], [0.0, 0.0, 0.03])



## Spine Tweak CTL Bones ## 
moveBoneScale(sceneRig[0], "def.spine_00.C", "ctl.twk_spine_01.C", -.6)
moveBoneScale(sceneRig[0], "def.spine_01.C", "ctl.twk_spine_02.C", -.6)
moveBoneScale(sceneRig[0], "def.spine_02.C", "ctl.twk_spine_03.C", -.6)
moveBoneScale(sceneRig[0], "def.spine_03.C", "ctl.twk_spine_04.C", -.6)
moveBoneScale(sceneRig[0], "def.spine_04.C", "ctl.twk_neck_01.C", -.6)
moveBoneScale(sceneRig[0], "def.spine_05.C", "ctl.twk_neck_02.C", -.6)

## Main Body CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.spine_00.C", "ctl.root.C", "center", "Y", 0.5)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "ctl.chest.C", "head", "Y", 0.4)
moveBoneConXYZ(sceneRig[0], "def.spine_02.C", "ctl.hips.C", "head", "Y", 0.3)

moveBoneBasic(sceneRig[0], "def.breast.L", "ctl.breast.L")
moveBoneBasic(sceneRig[0], "def.breast.R", "ctl.breast.R")

moveBoneScale(sceneRig[0], "def.shoulder.L", "ctl.clavicle.L", 1)
moveBoneScale(sceneRig[0], "def.shoulder.R", "ctl.clavicle.R", 1)

moveBoneTwoBoneBasic(sceneRig[0], "def.spine_04.C", "def.spine_06.C", "ctl.neck.C")
moveBoneBasic(sceneRig[0], "def.spine_06.C", "ctl.head.C")


######################
### Face CTL Bones ###
######################

## Nose CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.nose_00.C", "ctl.sub_nose_00.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_01.C", "ctl.sub_nose_00.C.001", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_02.C", "ctl.nose_02.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_03.C", "ctl.sub_nose_01.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_04.C", "ctl.nose_01.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_04.C", "ctl.nose_04.C", "head", "Y", 0.02)

## Left Ear CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.ear_00.L", "ctl.ear.L", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.ear_01.L", "ctl.sub_ear_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.ear_02.L", "ctl.sub_ear_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.ear_03.L", "ctl.sub_ear_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.ear_04.L", "ctl.sub_ear_03.L", "head", "Y", 0.02)

## Right Ear CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.ear_00.R", "ctl.ear.R", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.ear_01.R", "ctl.sub_ear_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.ear_02.R", "ctl.sub_ear_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.ear_03.R", "ctl.sub_ear_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.ear_04.R", "ctl.sub_ear_03.R", "head", "Y", 0.02)

## Left Brow CTL Bones ##
moveBoneConXYZ(sceneRig[0], "def.eb_ring_00.L", "ctl.sub_cheek_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_01.L", "ctl.sub_temple_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_02.L", "ctl.brow_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_03.L", "ctl.brow_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_04.L", "ctl.brow_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_05.L", "ctl.brow_03.L", "head", "Y", 0.02)

moveBoneConXYZ(sceneRig[0], "def.brow_b_00.L", "ctl.sub_brow_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_01.L", "ctl.sub_brow_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_02.L", "ctl.sub_brow_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_03.L", "ctl.sub_brow_03.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_03.L", "ctl.sub_brow_04.L", "tail", "Y", 0.02)

## Right Brow CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.eb_ring_00.R", "ctl.sub_cheek_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_01.R", "ctl.sub_temple_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_02.R", "ctl.brow_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_03.R", "ctl.brow_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_04.R", "ctl.brow_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.eb_ring_05.R", "ctl.brow_03.R", "head", "Y", 0.02)

moveBoneConXYZ(sceneRig[0], "def.brow_b_00.R", "ctl.sub_brow_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_01.R", "ctl.sub_brow_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_02.R", "ctl.sub_brow_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_03.R", "ctl.sub_brow_03.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.brow_b_03.R", "ctl.sub_brow_04.R", "tail", "Y", 0.02)

## Left Eye Lip CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lid_t_00.L", "ctl.sub_eyelid_03.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_t_01.L", "ctl.sub_eyelid_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_t_02.L", "ctl.eyelid_top.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_t_03.L", "ctl.sub_eyelid_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_00.L", "ctl.sub_eyelid_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_01.L", "ctl.sub_eyelid_05.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_02.L", "ctl.eyelid_bot.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_03.L", "ctl.sub_eyelid_04.L", "head", "Y", 0.02)

## Right Eye Lip CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lid_t_00.R", "ctl.sub_eyelid_03.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_t_01.R", "ctl.sub_eyelid_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_t_02.R", "ctl.eyelid_top.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_t_03.R", "ctl.sub_eyelid_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_00.R", "ctl.sub_eyelid_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_01.R", "ctl.sub_eyelid_05.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_02.R", "ctl.eyelid_bot.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lid_b_03.R", "ctl.sub_eyelid_04.R", "head", "Y", 0.02)

## Left Cheek CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.temple.L", "ctl.temple.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_00.L", "ctl.jaw_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_01.L", "ctl.sub_temple_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_02.L", "ctl.sub_cheek_00.L", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_03.L", "ctl.sub_cheek_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_00.L", "ctl.sub_nose_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_02.L", "ctl.sub_cheek_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_03.L", "ctl.sub_cheek_00.L", "head", "Y", 0.02)


## Right Cheek CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.temple.R", "ctl.temple.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_00.R", "ctl.jaw_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_01.R", "ctl.sub_temple_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_02.R", "ctl.sub_cheek_00.R", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_03.R", "ctl.sub_cheek_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.nose_00.R", "ctl.sub_nose_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_02.R", "ctl.sub_cheek_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_t_03.R", "ctl.sub_cheek_00.R", "head", "Y", 0.02)

## Cen Jaw CTl Bones ## 
moveBoneConXYZ(sceneRig[0], "def.chin_00.C", "ctl.chin_00.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw.C", "ctl.jaw_01.C", "head", "Y", 0.02)


## Left Jaw CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.jaw_00.L", "ctl.chin_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.L", "ctl.jaw_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.L", "ctl.jaw_03.L", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_01.L", "ctl.chin_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_00.L", "ctl.chin_01.L", "head", "Y", 0.02)

## Right Jaw CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.jaw_00.R", "ctl.chin_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.R", "ctl.jaw_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.R", "ctl.jaw_03.R", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_01.R", "ctl.chin_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.jaw_00.R", "ctl.chin_01.R", "head", "Y", 0.02)

## Center Lip Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lip_t_00.L", "ctl.lips_top.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_00.L", "ctl.lips_bot.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_03.C", "ctl.chin_03.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_02.C", "ctl.chin_02.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_01.C", "ctl.chin_01.C", "head", "Y", 0.02)

## Left Outer Lip Ring CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.nose_01.L", "ctl.nose.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_02.L", "ctl.lip_ring_t_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_con_00.L", "ctl.lip_con_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_b_02.L", "ctl.lip_ring_b_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_con_00.L", "ctl.lip_ring_b_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_01.L", "ctl.lip_ring_t_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_02.L", "ctl.cheek_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_01.L", "ctl.cheek_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_01.L", "ctl.chin_ring_b_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_00.L", "ctl.chin_ring_b_00.L", "head", "Y", 0.02)

## Right Outer Lip Ring CTL  Bones ## 
moveBoneConXYZ(sceneRig[0], "def.nose_01.R", "ctl.nose.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_02.R", "ctl.lip_ring_t_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_con_00.R", "ctl.lip_con_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_b_02.R", "ctl.lip_ring_b_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_con_00.R", "ctl.lip_ring_b_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_01.R", "ctl.lip_ring_t_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_02.R", "ctl.cheek_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_01.R", "ctl.cheek_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_01.R", "ctl.chin_ring_b_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_00.R", "ctl.chin_ring_b_00.R", "head", "Y", 0.02)

## Left Inner Ring CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lip_t_01.L", "ctl.lips_top_00.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_02.L", "ctl.lips_top_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_03.L", "ctl.lips_top_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_03.L", "ctl.lips.L", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_03.L", "ctl.lips_bot_02.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_02.L", "ctl.lips_bot_01.L", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_01.L", "ctl.lips_bot_00.L", "head", "Y", 0.02)


## Right Inner Ring CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.lip_t_01.R", "ctl.lips_top_00.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_02.R", "ctl.lips_top_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_03.R", "ctl.lips_top_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_t_03.R", "ctl.lips.R", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_03.R", "ctl.lips_bot_02.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_02.R", "ctl.lips_bot_01.R", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.lip_b_01.R", "ctl.lips_bot_00.R", "head", "Y", 0.02)

## Tongue CTL Bones ## 
moveBoneConXYZ(sceneRig[0], "def.tongue_02.C", "ctl.tongue_04.C", "tail", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.tongue_02.C", "ctl.tongue_03.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.tongue_01.C", "ctl.tongue_02.C", "head", "Y", 0.02)
moveBoneConXYZ(sceneRig[0], "def.tongue_00.C", "ctl.tongue_01.C", "head", "Y", 0.02)

## Face Main CTL Bones Cen ## 
moveBoneConXYZ(sceneRig[0], "def.nose_00.C", "ctl.sub_nose_00.C", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.nose_02.C", "ctl.nose_02.C", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.nose_04.C", "ctl.nose_04.C", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.chin_01.C", "ctl.chin_master.C", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.chin_master.C", "ctl.chin_master.C", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneExt(sceneRig[0], "def.teeth_t.C", "ctl.teeth_top.C", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneExt(sceneRig[0], "def.teeth_b.C", "ctl.teeth_bot.C", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneTwoBoneBasic(sceneRig[0], "def.tongue_01.C", "def.tongue_00.C", "ctl.tongue_master.C")
moveBoneBasic(sceneRig[0], "mch.mouth_lock.C", "ctl.jaw_master.C")
moveBoneConXYZ(sceneRig[0], "def.chin_01.C", "ctl.chin_master.C", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.chin_master.C", "ctl.chin_master.C", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])

moveBoneConXYZ(sceneRig[0], "def.spine_06.C", "ctl.mouth_blendshapes.C", "tail", "Y", 0.1)
moveBoneExt(sceneRig[0], "ctl.mouth_blendshapes.C", "ctl.mouth_blendshapes.C", "head", [0.0, -0.05, 0.05], [0.0, -0.05, 0.05])

moveBoneConXYZ(sceneRig[0], "def.spine_06.C", "ctl.head_blink.C", "tail", "Y", 0.1)
moveBoneExt(sceneRig[0], "ctl.head_blink.C", "ctl.head_blink.C", "head", [0.0, -0.05, 0.07], [0.0, -0.05, 0.07])

## Face Main Ctl Bones Left ## 
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.L", "ctl.jaw_02.L", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.L", "ctl.jaw_03.L", "tail", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_02.L", "ctl.cheek_03.L", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_01.L", "ctl.upper_cheek_master.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.upper_cheek_master.L", "ctl.upper_cheek_master.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.lid_b_02.L", "ctl.eyelid_bot_master.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyelid_bot_master.L", "ctl.eyelid_bot_master.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.lid_t_02.L", "ctl.eyelid_top_master.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyelid_top_master.L", "ctl.eyelid_top_master.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.brow_b_02.L", "ctl.eyebrow_upper_master.L.001", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyebrow_upper_master.L.001", "ctl.eyebrow_upper_master.L.001", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.eb_ring_04.L", "ctl.eyebrow_upper_master.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyebrow_upper_master.L", "ctl.eyebrow_upper_master.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.nose_00.L", "ctl.sub_nose_00.L", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_00.L", "ctl.nose.L", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_01.L", "ctl.lip_master_top.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lip_master_top.L", "ctl.lip_master_top.L", "head", [0.0, -0.05, 0.005], [0.00, -0.05, 0.005])
moveBoneConXYZ(sceneRig[0], "def.lip_b_01.L", "ctl.lip_master_bot.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lip_master_bot.L", "ctl.lip_master_bot.L", "head", [0.0, -0.05, -0.005], [0.0, -0.05, -0.005])
moveBoneConXYZ(sceneRig[0], "def.lip_con_00.L", "ctl.lips.L", "tail", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.lip_con_00.L", "ctl.lip_master_corner.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lip_master_corner.L", "ctl.lip_master_corner.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "org.eye.L", "ctl.eye_master.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eye_master.L", "ctl.eye_master.L", "head", [0.0, -0.06, 0.0], [0.0, -0.06, 0.0])
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_01.L", "ctl.lower_cheek_master.L", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lower_cheek_master.L", "ctl.lower_cheek_master.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])


## Face Main Ctl Bones Right## 
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.R", "ctl.jaw_02.R", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.jaw_lower_01.R", "ctl.jaw_03.R", "tail", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_02.R", "ctl.cheek_03.R", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_01.R", "ctl.upper_cheek_master.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.upper_cheek_master.R", "ctl.upper_cheek_master.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.lid_b_02.R", "ctl.eyelid_bot_master.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyelid_bot_master.R", "ctl.eyelid_bot_master.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.lid_t_02.R", "ctl.eyelid_top_master.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyelid_top_master.R", "ctl.eyelid_top_master.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.brow_b_02.R", "ctl.eyebrow_upper_master.R.001", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyebrow_upper_master.R.001", "ctl.eyebrow_upper_master.R.001", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.eb_ring_04.R", "ctl.eyebrow_upper_master.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eyebrow_upper_master.R", "ctl.eyebrow_upper_master.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "def.nose_00.R", "ctl.sub_nose_00.R", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.cheek_ring_t_00.R", "ctl.nose.R", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.lip_ring_t_01.R", "ctl.lip_master_top.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lip_master_top.R", "ctl.lip_master_top.R", "head", [0.0, -0.05, 0.005], [0.00, -0.05, 0.005])
moveBoneConXYZ(sceneRig[0], "def.lip_b_01.R", "ctl.lip_master_bot.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lip_master_bot.R", "ctl.lip_master_bot.R", "head", [0.0, -0.05, -0.005], [0.0, -0.05, -0.005])
moveBoneConXYZ(sceneRig[0], "def.lip_con_00.R", "ctl.lips.R", "tail", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "def.lip_con_00.R", "ctl.lip_master_corner.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lip_master_corner.R", "ctl.lip_master_corner.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])
moveBoneConXYZ(sceneRig[0], "org.eye.R", "ctl.eye_master.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.eye_master.R", "ctl.eye_master.R", "head", [0.0, -0.06, 0.0], [0.0, -0.06, 0.0])
moveBoneConXYZ(sceneRig[0], "def.chin_ring_b_01.R", "ctl.lower_cheek_master.R", "head", "Y", 0.03)
moveBoneExt(sceneRig[0], "ctl.lower_cheek_master.R", "ctl.lower_cheek_master.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])




#############################
### Eye CTL and MCH Bones ###
#############################

moveBoneConXYZ(sceneRig[0], "org.eye.L", "ctl.eye.L", "head", "Y", 0.02)
moveBoneExt(sceneRig[0], "ctl.eye.L", "ctl.eye.L", "head", [0.0, -0.2, 0.0], [0.0, -0.2, 0.0])
moveBoneConXYZ(sceneRig[0], "org.eye.R", "ctl.eye.R", "head", "Y", 0.02)
moveBoneExt(sceneRig[0], "ctl.eye.R", "ctl.eye.R", "head", [0.0, -0.2, 0.0], [0.0, -0.2, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eye.L", "ctl.eye_lid_bottom.L", "head", "Y", 0.04)
moveBoneExt(sceneRig[0], "ctl.eye_lid_bottom.L", "ctl.eye_lid_bottom.L", "head", [0.0, -0.0, -0.03], [0.0, -0.0, -0.03])

moveBoneConXYZ(sceneRig[0], "ctl.eye.R", "ctl.eye_lid_bottom.R", "head", "Y", 0.04)
moveBoneExt(sceneRig[0], "ctl.eye_lid_bottom.R", "ctl.eye_lid_bottom.R", "head", [0.0, -0.0, -0.03], [0.0, -0.0, -0.03])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom.L", "ctl.eye_lid_bottom_M.L", "head", "Y", 0.01)    
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom_M.L", "ctl.eye_lid_bottom_I.L", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_bottom_I.L", "ctl.eye_lid_bottom_I.L", "head", [-0.015, -0.0, 0.0], [-0.015, -0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom_M.L", "ctl.eye_lid_bottom_O.L", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_bottom_O.L", "ctl.eye_lid_bottom_O.L", "head", [0.015, -0.0, 0.0], [0.015, -0.0, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom.R", "ctl.eye_lid_bottom_M.R", "head", "Y", 0.01)    
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom_M.R", "ctl.eye_lid_bottom_I.R", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_bottom_I.R", "ctl.eye_lid_bottom_I.R", "head", [-0.015, -0.0, 0.0], [-0.015, -0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom_M.R", "ctl.eye_lid_bottom_O.R", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_bottom_O.R", "ctl.eye_lid_bottom_O.R", "head", [0.015, -0.0, 0.0], [0.015, -0.0, 0.0])    

moveBoneConXYZ(sceneRig[0], "ctl.eye.L", "ctl.eye_lid_top.L", "head", "Y", 0.04)
moveBoneExt(sceneRig[0], "ctl.eye_lid_top.L", "ctl.eye_lid_top.L", "head", [0.0, -0.0, 0.05], [0.0, -0.0, 0.05])

moveBoneConXYZ(sceneRig[0], "ctl.eye.R", "ctl.eye_lid_top.R", "head", "Y", 0.04)
moveBoneExt(sceneRig[0], "ctl.eye_lid_top.R", "ctl.eye_lid_top.R", "head", [0.0, -0.0, 0.05], [0.0, -0.0, 0.05])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top.L", "ctl.eye_lid_top_M.L", "head", "Y", 0.01)    
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top_M.L", "ctl.eye_lid_top_I.L", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_top_I.L", "ctl.eye_lid_top_I.L", "head", [-0.015, -0.0, 0.0], [-0.015, -0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top_M.L", "ctl.eye_lid_top_O.L", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_top_O.L", "ctl.eye_lid_top_O.L", "head", [0.015, -0.0, 0.0], [0.015, -0.0, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top.R", "ctl.eye_lid_top_M.R", "head", "Y", 0.01)    
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top_M.R", "ctl.eye_lid_top_I.R", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_top_I.R", "ctl.eye_lid_top_I.R", "head", [-0.015, -0.0, 0.0], [-0.015, -0.0, 0.0])
moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top_M.R", "ctl.eye_lid_top_O.R", "head", "Y", 0.01)
moveBoneExt(sceneRig[0], "ctl.eye_lid_top_O.R", "ctl.eye_lid_top_O.R", "head", [0.015, -0.0, 0.0], [0.015, -0.0, 0.0])  

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom.L", "mch.eye_lid_bottom.L", "head", "Y", 0.03)    
moveBoneExt(sceneRig[0], "mch.eye_lid_bottom.L", "mch.eye_lid_bottom.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_bottom.R", "mch.eye_lid_bottom.R", "head", "Y", 0.03)    
moveBoneExt(sceneRig[0], "mch.eye_lid_bottom.R", "mch.eye_lid_bottom.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top.L", "mch.eye_lid_top.L", "head", "Y", 0.03)    
moveBoneExt(sceneRig[0], "mch.eye_lid_top.L", "mch.eye_lid_top.L", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eye_lid_top.R", "mch.eye_lid_top.R", "head", "Y", 0.03)    
moveBoneExt(sceneRig[0], "mch.eye_lid_top.R", "mch.eye_lid_top.R", "head", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])

moveBoneExt(sceneRig[0],"ctl.eye.L", "ctl.eyes.C", "eyeMid", [0.0, -0.05, 0.0], [0.0, -0.05, 0.0])

moveBoneConXYZ(sceneRig[0], "ctl.eyes.C", "mch.eyes_god.C", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "ctl.eyes.C", "mch.eyes.C", "head", "Y", 0.02)

moveBoneConXYZ(sceneRig[0], "ctl.eyes.C", "ctl.eyes_highlite.C", "head", "Y", 0.02)
moveBoneExt(sceneRig[0], "ctl.eyes_highlite.C", "ctl.eyes_highlite.C", "head", [0.0, -0.0, 0.03], [0.0, -0.0, 0.03])   

moveBoneConXYZ(sceneRig[0], "ctl.eye.L", "ctl.eye_highlite.L", "head", "Y", 0.02)
moveBoneExt(sceneRig[0], "ctl.eye_highlite.L", "ctl.eye_highlite.L", "head", [0.0, -0.0, 0.03], [0.0, -0.0, 0.03])   

moveBoneConXYZ(sceneRig[0], "ctl.eye.R", "ctl.eye_highlite.R", "head", "Y", 0.02)
moveBoneExt(sceneRig[0], "ctl.eye_highlite.R", "ctl.eye_highlite.R", "head", [0.0, -0.0, 0.03], [0.0, -0.0, 0.03])   

moveBoneConXYZ(sceneRig[0], "ctl.eyes_highlite.C", "mch.eyes_highlite_world.C", "head", "Y", 0.03)
moveBoneConXYZ(sceneRig[0], "ctl.eyes_highlite.C", "mch.eyes_highlite.C", "head", "Y", 0.02)