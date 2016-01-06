bl_info = {
    "name": "Refresh Proxy",
    "author": "Wayne Wu",
    "version": (1, 0, 2),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Refresh Proxy",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Refresh%20Proxy.aspx",
    "category": "Tangent"}
    
import bpy

# class ProxyToolGUI(bpy.types.Panel):
#     bl_label = "Proxy Tools"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'TOOLS'
#     bl_category = 'Tangent'
# 
#     def draw(self, context):
# 
#         layout = self.layout
#         row = layout.row(align = True)
#         row.label(icon = 'OUTLINER_OB_ARMATURE')
#         row.operator("object.proxy_refresh", text = "Refresh Proxy", icon = 'FILE_REFRESH')


class RefreshProxy(bpy.types.Operator):
    bl_label = "Refresh_proxy"
    bl_idname = "object.proxy_refresh"
    bl_description = "Refresh (Update) the selected proxies"
    bl_options = {'UNDO'}    
    
    
    def execute(self, context):
    
        for obj in bpy.context.selected_objects: 
            if obj.proxy:
                self.refresh_proxy(obj)
                
        return {'FINISHED'}
    
    
    def invoke(self, context, event):
    
        return self.execute(context)
 
    
    def refresh_proxy(self, obj):
                     
        index_list = []
        i = 0
        for layer in obj.data.layers_protected: 
            if layer: 
                index_list.append(i)
            i = i + 1
        
        #Must to explicit call to turn off layers_protected
        for i in index_list:
            obj.data.layers_protected[i] = False
            
        
        #Update proxy from linked groups
        rig_object_name = obj.proxy.name            
        new_data = obj.proxy_group.dupli_group.objects[rig_object_name].data
        obj.data = new_data
        
        #Turn the protected layers back on
        for i in index_list: 
            obj.data.layers_protected[i] = True
                    

def menu_draw(self, context):
    """
    Menu ShortCut for refreshing the proxy, under object tab
    """
    self.layout.operator("object.proxy_refresh", text = "Refresh Proxy", icon = 'FILE_REFRESH')
    
                    
def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_object.prepend(menu_draw)
    
    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_object.remove(menu_draw)
    
    
if __name__ == "__main__":
    register()
    