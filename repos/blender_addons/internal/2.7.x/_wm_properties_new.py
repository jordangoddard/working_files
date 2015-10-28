bl_info = {
    "name": "WM_OT_properties",
    "author": "Wayne Wu",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "",
    "description": "Customized operator for ops.wm.properties_add and ops.wm.properties_edit",
    "warning": "",
    "category": "Operator"}
     
import bpy 
from bpy.types import Operator
from bpy.props import (StringProperty, FloatProperty, IntProperty)


rna_path = StringProperty(
        name="Property Edit",
        description="Property data_path edit",
        maxlen=1024,
        options={'HIDDEN'},
        )

rna_value = StringProperty(
        name="Property Value",
        description="Property value edit",
        maxlen=1024,
        )

rna_property = StringProperty(
        name="New Property Name",
        default = "",
        description="Property name edit",
        maxlen=1024,
        )

rna_min = FloatProperty(
        name="Min",
        default=-10000.0,
        precision=3,
        )

rna_max = FloatProperty(
        name="Max",
        default=10000.0,
        precision=3,
        )

class WM_OT_properties_new_edit(Operator):
    bl_idname = "wm.properties_new_edit"
    bl_label = "Edit Custom Property"
    bl_options = {'UNDO'}

    current_prop_name = StringProperty(name = "property name to be edited") #mandatory
    data_path = rna_path #mandatory   
    new_prop_name = rna_property #optional
    value = rna_value #mandatory
    min = rna_min #optional
    max = rna_max #optional
    description = StringProperty(
            name="Tooltip",
            )

    def execute(self, context):
        from rna_prop_ui import rna_idprop_ui_prop_get, rna_idprop_ui_prop_clear

        data_path = self.data_path
        value = self.value
        prop = self.new_prop_name

        prop_old = self.current_prop_name
        _last_prop = [prop_old]
            
        if prop_old is None:
            self.report({'ERROR'}, "Direct execution not supported")
            return {'CANCELLED'}

        try:
            value_eval = eval(value)
            # assert else None -> None, not "None", see [#33431]
            assert(type(value_eval) in {str, float, int, bool, tuple, list})
        except:
            value_eval = value

        if not prop: 
            prop = prop_old #Keep the same name
            
        # First remove
        item = eval("context.%s" % data_path)
        prop_type_old = type(item[prop_old])

        rna_idprop_ui_prop_clear(item, prop_old)
        exec_str = "del item[%r]" % prop_old
        # print(exec_str)
        exec(exec_str)

        # Reassign
        exec_str = "item[%r] = %s" % (prop, repr(value_eval))
        # print(exec_str)
        exec(exec_str)
        
        _last_prop[:] = [prop]

        prop_type = type(item[prop])

        prop_ui = rna_idprop_ui_prop_get(item, prop)

        if prop_type in {float, int}:
            prop_ui["soft_min"] = prop_ui["min"] = prop_type(self.min)
            prop_ui["soft_max"] = prop_ui["max"] = prop_type(self.max)

        prop_ui["description"] = self.description

        # If we have changed the type of the property, update its potential anim curves!
        if prop_type_old != prop_type:
            data_path = '["%s"]' % bpy.utils.escape_identifier(prop)
            done = set()

            def _update(fcurves):
                for fcu in fcurves:
                    if fcu not in done and fcu.data_path == data_path:
                        fcu.update_autoflags(item)
                        done.add(fcu)

            def _update_strips(strips):
                for st in strips:
                    if st.type == 'CLIP' and st.action:
                        _update(st.action.fcurves)
                    elif st.type == 'META':
                        _update_strips(st.strips)

            adt = getattr(item, "animation_data", None)
            if adt is not None:
                if adt.action:
                    _update(adt.action.fcurves)
                if adt.drivers:
                    _update(adt.drivers)
                if adt.nla_tracks:
                    for nt in adt.nla_tracks:
                        _update_strips(nt.strips)

        # otherwise existing buttons which reference freed
        # memory may crash blender [#26510]
        # context.area.tag_redraw()
        for win in context.window_manager.windows:
            for area in win.screen.areas:
                area.tag_redraw()

        return {'FINISHED'}    
               
class WM_OT_properties_new_add(Operator):
    bl_idname = "wm.properties_new_add"
    bl_label = "Add Custom Property"
    bl_options = {'UNDO'}

    data_path = rna_path #string property
    prop_name = StringProperty(name= "name of property", default = "prop")
    default_value = StringProperty(name = "default num", default = "1.0")
    default_max = FloatProperty(name = "default max", default = 1.0)
    default_min = FloatProperty(name = "default min", default = 0.0)
    
    def execute(self, context):
        from rna_prop_ui import rna_idprop_ui_prop_get

        data_path = self.data_path
        item = eval("context.%s" % data_path)

        def unique_name(names):
            prop = self.prop_name
            prop_new = prop
            i = 1
            while prop_new in names:
                prop_new = prop + str(i)
                i += 1

            return prop_new

        prop = unique_name(item.keys())

        item[prop] = eval(self.default_value)

        prop_type = type(item[prop])
        
        # not essential, but without this we get [#31661]
        prop_ui = rna_idprop_ui_prop_get(item, prop) #create the prop_ui
       
        if prop_type in {float, int}:
            prop_ui["soft_min"] = prop_ui["min"] = prop_type(self.default_min)
            prop_ui["soft_max"] = prop_ui["max"] = prop_type(self.default_max)
        
        return {'FINISHED'}
    
def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
     
if __name__ == "__main__":
    register()