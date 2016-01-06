#
#    Copyright (c) 2015 Conrad Dueck
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
# The production notes requiring overscan renders for composite based camera shake



bl_info = {
    "name": "Overscan Camera",
    "author": "conrad dueck",
    "version": (0,1,0),
    "blender": (2, 75, 2),
    "location": "View3D > Tool Shelf > Addons",
    "description": "Make Overscan Camera",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tangent"}

import bpy, math
from math import tan, atan, pi


#define functions
def FOVupdate(origFOV, origWIDTH, newWIDTH):
    #return(2 * atan(tan(origFOV/2) * newWIDTH/origWIDTH))
    return(2 * atan((tan(origFOV/2)) * (newWIDTH/origWIDTH)))

def FLupdate(origFOV, theFactor, sensorSize):
    return((sensorSize/(tan((origFOV+(origFOV*theFactor))/(2*(180/pi)))))/2)

def FOVcalc(focalLength, sensorSize):
    return(2 * atan(sensorSize/(2*focalLength)) * 180/pi)

def FLcalc(theFOV, sensorSize):
    return((sensorSize/(tan(theFOV/(2*(180/pi)))))/2)

def updateNew(self, context):
    try:
        bpy.context.scene.overScanNewX = bpy.context.scene.render.resolution_x + (bpy.context.scene.render.resolution_x * (bpy.context.scene.overScanPct * 0.01))
        bpy.context.scene.overScanNewY = bpy.context.scene.render.resolution_y + (bpy.context.scene.render.resolution_y * (bpy.context.scene.overScanPct * 0.01))
        bpy.context.scene.overScanOrigX = bpy.context.scene.render.resolution_x
        bpy.context.scene.overScanOrigY = bpy.context.scene.render.resolution_y
    except:
        print('failed to update new resolution')
    
def updateOld(self, context):
    try:
        bpy.context.scene.overScanOrigX = bpy.context.scene.render.resolution_x
        bpy.context.scene.overScanOrigY = bpy.context.scene.render.resolution_y
    except:
        print('failed to update old resolution')


#define button operators
class BUTTON_OT_overscanSet(bpy.types.Operator):
    bl_idname = "overscan.set"
    bl_label = "Create Overscan"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        origWidth = bpy.context.scene.render.resolution_x
        origHeight = bpy.context.scene.render.resolution_y
        if len(bpy.context.selected_objects) >= 1:
            for thisobj in bpy.context.selected_objects:
                if thisobj.type == 'CAMERA':
                    thiscam = thisobj
                    bpy.context.scene.overScanOrigCam = thiscam.name
                    bpy.context.scene.overScanOrigX = origWidth
                    bpy.context.scene.overScanOrigY = origHeight
                    thisFOV = (FOVcalc(thiscam.data.lens, thiscam.data.sensor_width))
                    thePct = (bpy.context.scene.overScanPct * 0.01)
                    newWidth = origWidth + (origWidth * thePct)
                    newHeight = origHeight * (newWidth/origWidth)
                    #newFOV = FOVupdate(thisFOV, origWidth, newWidth)
                    #newFocalLength = FLupdate(thisFOV, thePct, thiscam.data.sensor_width)
                    newSensor = thiscam.data.sensor_width + (thiscam.data.sensor_width * thePct)
                    newcam = thiscam.copy()
                    newcam.data = thiscam.data.copy()
                    newcam.data.sensor_width = newSensor
                    #newcam.data.lens = newFocalLength
                    newcam.name = (thiscam.name + '_Overscan' + str(int(bpy.context.scene.overScanPct)) + '%')
                    bpy.context.scene.objects.link(newcam)
                    bpy.context.scene.camera = newcam
                    bpy.context.scene.render.resolution_x = newWidth
                    bpy.context.scene.render.resolution_y = newHeight
                    bpy.context.scene.overScanNewX = newWidth
                    bpy.context.scene.overScanNewY = newHeight
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.ops.object.select_pattern(pattern=newcam.name)
        else:
            print('There is nothing selected')
        print('finished')
        return{'FINISHED'}

class BUTTON_OT_overscanRevert(bpy.types.Operator):
    bl_idname = "overscan.revert"
    bl_label = "Restore Original"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.scene.camera = bpy.data.objects[bpy.context.scene.overScanOrigCam]
            bpy.context.scene.render.resolution_x = bpy.context.scene.overScanOrigX
            bpy.context.scene.render.resolution_y = bpy.context.scene.overScanOrigY
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=bpy.context.scene.overScanOrigCam)
        except:
            pass
        print('Finished Restore')
        return{'FINISHED'}

#define panel
class VIEW3D_OT_overscan(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "OverScan Cam"
    bl_context = "objectmode"
    bl_category = 'Addons'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "overScanPct")
        layout.operator("overscan.set", text=(BUTTON_OT_overscanSet.bl_label))
        layout.operator("overscan.revert", text=(BUTTON_OT_overscanRevert.bl_label))
        layout.label('Original:')
        #layout.label(str(bpy.context.scene.overScanOrigCam))
        layout.label(str(bpy.context.scene.overScanOrigX) + " x " + str(bpy.context.scene.overScanOrigY))
        layout.label('New Resolution:')
        layout.label(str(bpy.context.scene.overScanNewX) + " x " + str(bpy.context.scene.overScanNewY))
        row = layout.row()

#register
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.overScanPct = bpy.props.FloatProperty \
        (
          name = "Percent",
          description = "Set percentage of frame size for border size",
          default = 10.0,
          min = 0.0,
          max = 1000.0,
          update = updateNew
        )
    bpy.types.Scene.overScanOrigCam = bpy.props.StringProperty \
        (
          name = "Source Camera",
          default = "",
        )
    bpy.types.Scene.overScanOrigX = bpy.props.IntProperty()
    bpy.types.Scene.overScanOrigY = bpy.props.IntProperty()
    bpy.types.Scene.overScanNewX = bpy.props.IntProperty()
    bpy.types.Scene.overScanNewY = bpy.props.IntProperty()
    
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.overScanPct
    del bpy.types.Scene.overScanOrigCam
    del bpy.types.Scene.overScanOrigX
    del bpy.types.Scene.overScanOrigY
    

if __name__ == "__main__":
    register()
