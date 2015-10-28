

bl_info = {
    "name": "MassAlign",
    "author": "Conrad Dueck",
    "version": (0,6),
    "blender": (2, 73, 0),
    "location": "View3D > Tool Shelf > Addons",
    "description": "Align one set of objects to another.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "http://www.blender.org/api/blender_python_api_2_73a_release/",
    "category": "3D View"}


import bpy
from bpy import context
import random
from random import randint

### Property Classes
bpy.types.Scene.cdma_add = bpy.props.BoolProperty \
    (
    name = "Add Instances",
    description = "Generate instanced copies of source array objects to align all targets",
    default = False
    )
bpy.types.Scene.cdma_cycle = bpy.props.BoolProperty \
    (
      name = "Cycle",
      description = "ON cycles through array for instances, OFF adds random source instances",
      default = False
    )
bpy.types.Scene.cdma_random = bpy.props.BoolProperty \
    (
      name = "Random Targets",
      description = "Align to random targets vs using array order. WARNING: this can target the same object mulitiple times.",
      default = False
    )
bpy.types.Scene.cdma_location = bpy.props.BoolProperty \
    (
      name = "Location",
      description = "Align Location",
      default = True
    )
bpy.types.Scene.cdma_rotation = bpy.props.BoolProperty \
    (
      name = "Rotation",
      description = "Align Rotation",
      default = True
    )
bpy.types.Scene.cdma_scale = bpy.props.BoolProperty \
    (
      name = "Scale",
      description = "Align Scale",
      default = True
    )

class OBJECT_PT_mass_align(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="test prop", default="unknown")
 
bpy.utils.register_class(OBJECT_PT_mass_align)

bpy.types.Scene.thesource = bpy.props.CollectionProperty(type=OBJECT_PT_mass_align)
bpy.types.Scene.thetarget = bpy.props.CollectionProperty(type=OBJECT_PT_mass_align)


### Panel Operators
## Tools/Addons Panel
class OBJECT_OT_MassAlignPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Mass Align"
    bl_context = "objectmode"
    bl_category = 'Addons'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        obj = context.selected_objects
        
        layout = self.layout
        
        split = layout.split(percentage=0.75, align=True)
        
        col = split.column()
        col.label(text="Sel. Count:", icon='OBJECT_DATA')
        col = split.column()
        col.label(text=str(len(obj)))
        
        split = layout.split(percentage=0.85, align=True)
        
        col = split.column(align=True)
        col.operator("massalign.source", text=(OBJECT_OT_SourceButton.bl_label))
        col = split.column(align=True)
        col.operator("massalign.clearsrc", text=(OBJECT_OT_ClearSRCButton.bl_label))
        col = layout.column()
        col.prop(context.scene, "cdma_add")
        col.prop(context.scene, "cdma_cycle")
        
        layout.separator()
        
        split = layout.split(percentage=0.85, align=True)
        
        col = split.column(align=True)
        col.operator("massalign.target", text=(OBJECT_OT_TargetButton.bl_label))
        col = split.column(align=True)
        col.operator("massalign.cleartgt", text=(OBJECT_OT_ClearTGTButton.bl_label))
        col = layout.column()
        col.prop(context.scene, "cdma_random")
        
        layout.separator()
        
        col = layout.column()
        col.label(text="Align:")
        col.prop(context.scene, "cdma_location")
        col.prop(context.scene, "cdma_rotation")
        col.prop(context.scene, "cdma_scale")
        
        layout.separator()
        
        layout.operator("massalign.go", text=(OBJECT_OT_GoButton.bl_label))

## Buttons
### Clear Tags Buttons
class OBJECT_OT_ClearSRCButton(bpy.types.Operator):
    '''Clear any previously tagged objects.'''
    bl_idname = "massalign.clearsrc"
    bl_label = "X"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        tempsel = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.massalign.source()
        #bpy.ops.massalign.target()
        for a in tempsel:
            bpy.ops.object.select_pattern(pattern=(a.name))
        return{'FINISHED'}

class OBJECT_OT_ClearTGTButton(bpy.types.Operator):
    '''Clear any previously tagged objects.'''
    bl_idname = "massalign.cleartgt"
    bl_label = "X"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        tempsel = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.massalign.target()
        for a in tempsel:
            bpy.ops.object.select_pattern(pattern=(a.name))
        return{'FINISHED'}

### Build Source Array Button
class OBJECT_OT_SourceButton(bpy.types.Operator):
    '''SET/SELECT current source array'''
    bl_idname = "massalign.source"
    bl_label = "Tag Source(s)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        numsel = 0
        numsel = len(context.selected_objects)
        numstored = len(context.scene.thesource)
        
        # ignoreobjects in thetargetarray
        if (numstored > 0) and (numsel > 0):
            bpy.ops.object.select_all(action='DESELECT')
            for a in range(numstored):
                bpy.ops.object.select_pattern(pattern=context.scene.thesource[a].name)
        elif (numstored == 0) and (numsel >= 1):
            for a in context.selected_objects:
                if not a.name in context.scene.thetarget.keys():
                    newitem = context.scene.thesource.add()
                    newitem.name = a.name
        else:
            context.scene.thesource.clear()
        
        # update source button label
        if (len(context.scene.thesource)) >= 1:
            self.__class__.bl_label = (str(len(context.scene.thesource))+" source(s)")
        else:
            self.__class__.bl_label = "Tag Source(s)"
        self.report({'INFO'}, self.__class__.bl_label)
        
        return{'FINISHED'}

### Build Target Array
class OBJECT_OT_TargetButton(bpy.types.Operator):
    '''SET/SELECT current target array'''
    bl_idname = "massalign.target"
    bl_label = "Tag Target(s)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        numsel = 0
        numsel = len(context.selected_objects)
        numstored = len(context.scene.thetarget)
        
        # ignore objects in thesource array
        if (numstored > 0) and (numsel > 0):
            bpy.ops.object.select_all(action='DESELECT')
            for a in range(numstored):
                bpy.ops.object.select_pattern(pattern=context.scene.thetarget[a].name)
        elif (numstored == 0) and (numsel >= 1):
            for a in context.selected_objects:
                if not a.name in context.scene.thesource.keys():
                    newitem = context.scene.thetarget.add()
                    newitem.name = a.name
        else:
            context.scene.thetarget.clear()\
        
        # update target button label
        if (len(context.scene.thetarget)) >= 1:
            self.__class__.bl_label = (str(len(context.scene.thetarget))+" target(s)")
        else:
            self.__class__.bl_label = "Tag Target(s)"
        self.report({'INFO'}, self.__class__.bl_label)
        
        return{'FINISHED'}

### Align thesource/thetarget, add instances
class OBJECT_OT_GoButton(bpy.types.Operator):
    '''Align the source tagged objects to the target tagged objects.'''
    bl_idname = "massalign.go"
    bl_label = "Go!"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        thematched = 0
        thesourcecount = (len(context.scene.thesource)-1)
        
        if (len(context.scene.thesource) >= 1) and (len(context.scene.thetarget) >= 1):
            # Set therange based on source/target array lengths and add instances toggle
            if bpy.context.scene.cdma_add:
                therange = len(context.scene.thetarget)
            else:
                therange = len(context.scene.thesource)
            
            # Cycle thru therange
            for a in range(0, therange):
                # Set thissource
                if a > thesourcecount:
                    if bpy.context.scene.cdma_cycle:
                        thisrand = int(x=(a-((int(a/(thesourcecount + 1)))*(thesourcecount + 1))))
                    else:
                        thisrand = randint(0, (len(context.scene.thesource)-1))
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.ops.object.select_pattern(pattern=(context.scene.thesource[thisrand].name))
                    bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                    thissource = bpy.context.selected_objects[0]
                    newitem = context.scene.thesource.add()
                    newitem.name = thissource.name
                else:
                    thissource = bpy.data.objects[context.scene.thesource[a].name]
                
                # Set thistarget
                if (not bpy.context.scene.cdma_random) and (len(context.scene.thetarget) >= len(context.scene.thesource)):
                    thistarget = bpy.data.objects[context.scene.thetarget[a].name]
                elif (not bpy.context.scene.cdma_random) and (len(context.scene.thetarget) < len(context.scene.thesource)):
                    if thematched >= len(context.scene.thetarget):
                        thematched = 0
                        thistarget = bpy.data.objects[context.scene.thetarget[thematched].name]
                        thematched += 1
                    else:
                        thistarget = bpy.data.objects[context.scene.thetarget[thematched].name]
                        thematched += 1
                else:
                    b = randint(0, (len(context.scene.thetarget)-1))
                    thistarget = bpy.data.objects[context.scene.thetarget[b].name]
                    while thistarget == thissource and (thematched < therange):
                        b = randint(0, (len(context.scene.thetarget)-1))
                        thistarget = bpy.data.objects[context.scene.thetarget[b].name]
                        thematched += 1
                
                # Align thissource to thistarget
                if bpy.context.scene.cdma_location:
                    thissource.location = thistarget.location
                if bpy.context.scene.cdma_rotation:
                    thissource.rotation_euler = thistarget.rotation_euler
                if bpy.context.scene.cdma_scale:
                    thissource.scale = thistarget.scale
        else:
            print('Ensure objects are tagged for BOTH source and target')
        return{'FINISHED'}
    

## Registration/Simple Properties
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.cdma_add
    del bpy.types.Scene.cdma_random
    del bpy.types.Scene.cdma_cycle
    del bpy.types.Scene.cdma_location
    del bpy.types.Scene.cdma_rotation
    del bpy.types.Scene.cdma_scale
    

if __name__ == "__main__":
    register()
    
