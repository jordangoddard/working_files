from core import log, asset

class asset(object):
    def _init_(self, asset, log):
        self.asset = asset
        self.log = log

class playblast(object):
    def _init_(self, asset):
        pass
    
    def execute(self):
        '''
        This will call all the moduels of the class
        '''
        pass

    def encode(self):
        pass

    def create(self):
        pass

    def create_playblast_window(self):
        area = bpy.context.area
        screen_ops = bpy.ops.screen
        area.type = 'VIEW_3D'                                                                           # Changes Current area to 3D View
        screen_ops.screen_full_area()                                                                   # Make active screen fill the window.
        pass

    def set_output_settings(self):
        pass

    def render_open_gl(self):
        pass

    



    def encode_via_rvio(self):
        pass


























