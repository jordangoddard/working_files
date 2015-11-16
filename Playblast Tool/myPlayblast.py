#from core import log, asset
import bpy

def run_stuff():
    print("\n\nI am running the first class\n\n")
    return Preferences()


class Movie(object):
    def __init__(self):
        pass

    def dosomething(self):
        pass


class RvioInfo(object):
    def __init__(self):
        end_resolution_x = 960
        end_resolution_y = 720
        pass

    def open_rvio(self):
        import subprocess
        rv_path = "C:\\pipeline\\rv\\rv-win64-x86-64-current\\rv-win64-x86-64-6.2.2\\bin"
        pb_path = "C:\\Temp\\test.mov" # self.movie.file
        subprocess.Popen('"%s/rv" [ %s ]' %(rv_path, pb_path))
    def __str__(self):
        return self.burn_in_string()

    # Spit out the information required to do an RVIO encode with the overlay information
    def burn_in_string(self):
        matte = " -overlay matte %s %s" % (self.matte_aspect, self.matte_opacity)
        opus_burnin = ' -overlay opus_burnin %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (
                self.opacity,
                self.grey,
                self.font_size,
                self.client_shot_code,
                self.shot_code,
                self.show_code,
                self.artist,
                self.shot.process,
                self.revision,
                self.status,
                self.rank,
                self.pass_number,
                self.fov,
                "%sfps" % self.fps,
                self.curr_date
                )
        return "%s %s" % (matte, opus_burnin)

    def dosomething(self):
        pass


class Preferences(object):
    def __init__(self, show=None):
        print("I got to the preferences class")
        self.pk = 1
        self.url = "http://10.1.1.50:8000/api/shows/1/"
        self.show = "MOVIE NAME GOES HERE"
        self.p_drive = "c:/temp"
        self.p_drive_linux = "/dfs"
        self.res_render_x = 1920
        self.res_render_y = 1080
        self.codec = "mp4"
        
        self.run_show()

    def run_show(self):
        return Show(self)


class Show(object):
    def __init__(self, preferences):
        # this is the group
        print("I got to the show class")
        self.pk = 1
        self.url = "http://10.1.1.50:8000/api/shows/1/"
        self.code = "0043_ozzy"
        self.name = "Run Ozzy Run!"
        self.company = "http://10.1.1.50:8000/api/companies/1/"
        self.created = "2015-10-28T14:08:26.058309Z"
        self.modified = "2015-10-28T14:11:53.604197Z"
        self.preferences = preferences
        
        self.run_asset()

    def run_asset(self):
        return Asset(self)


class Asset(object):
    '''
    This is the main asset class that will pull the asset data from the asset manager.
    '''
    def __init__(self, show):
        '''
        This will run on instantiate of the Asset class
        '''
        print("I got to the asset class")
        # Begin fake asset data
        
        self.pk = 474
        self.url = "http://10.1.1.50:8000/api/assets/474/"
        self.type_primary = "shot"
        self.type_secondary = "010"
        self.type_tertiary = None
        self.code = "010.0010"
        self.comment = None
        self.description = None
        self.show = show
        self.parents = []
        self.children = []
        self.groups = []
        self.versions = []
        self.data = None
        self.movie = None
        self.images = []
        self.start_frame = 1
        self.end_frame = 377
        self.created = "2015-10-28T14:08:34.118980Z"
        self.modified = "2015-10-28T14:11:57.653306Z"
        self.path = "C:/tst/"
        self.file = "C:/tst/010.0010.blend"
        self.filename = "010.0010.blend"
        
        self.run_playblast()
        
        # self.asset = snapshot.get_current_asset()
        # self.log = snapshot.get_current_log()

    def run_playblast(self):
        '''
        Run playblast class with asset information
        '''
        return Playblast(self)


class Playblast(object):
    def __init__(self, asset):
        '''
        This will run on instantiate of the Plablast class
        '''
        render_x_size = 960
        render_y_size = 540
        self.asset = asset
        print("I got to the playblast class")
        print(self.asset.code)
        print(self.asset.show.code)
        print(self.asset.show.preferences.show)
        self.execute()
    
    def execute(self):
        '''
        This will call all the moduels of the class.
        '''
        import time
        self.create_playblast_window()
        self.set_render_settings()
        #time.sleep(10)
        self.render_open_gl()
        self.movie_create()

    def movie_create(self):
        return Movie(self)

    def encode(self):   # json
        '''
        This will...
        '''
        pass

    def create(self):   # json
        '''
        This will...
        '''
        pass

    def create_playblast_window(self):
        '''
        This will create a window for the playblast to occur in.
        '''
        area = bpy.context.area
        screen_ops = bpy.ops.screen
        area.type = 'VIEW_3D'                                           # Changes Current area to 3D View
        screen_ops.screen_full_area()                                   # Make active screen fill the window.

    def set_render_settings(self):
        '''
        This will...
        '''
        scene = bpy.data.scenes[self.asset.code]                        # Set 'scene' to the current scene data
        render = bpy.context.scene.render                               # Set 'render' to the current scene render settings
        render.stamp_font_size = 17                                     # Set stamp size to '17'
        render.stamp_background = (0,0,0,1)                             # Set stamp background to '0,0,0,1'
        render.use_stamp = True                                         # Set render stamp to 'ON'
        render.use_stamp_time = False                                   # Set render stamp time to 'OFF'
        render.use_stamp_date = False                                   # Set render stamp date to 'OFF'
        render.use_stamp_render_time = False                            # Set render stamp render time to 'OFF'
        render.use_stamp_frame = True                                   # Set render stamp frame to 'ON'
        render.use_stamp_scene = True                                   # Set render stamp scene to 'ON'
        render.use_stamp_camera = False                                 # Set render stamp camera to 'OFF'
        render.use_stamp_lens = True                                    # Set render stamp lens to 'ON'
        render.use_stamp_filename = False                               # Set render stamp file name to 'OFF'
        render.use_stamp_marker = False                                 # Set render stamp marker to 'OFF'
        render.use_stamp_sequencer_strip = False                        # Set render stamp sequence strip to 'OFF'
        render.image_settings.file_format = 'FFMPEG'                    # Set image file format for render to 'FFMPEG'
        render.ffmpeg.format = 'QUICKTIME'                              # Set render format to 'Quicktime'
        render.ffmpeg.codec = 'MPEG4'                                   # Set render codec to 'MPEG4'
        render.ffmpeg.audio_codec = 'PCM'                               # Set render audio codec to 'PCM'
        scene.frame_current = 1                                         # Set current fram to '1' (not necesary, just good form)
        scene.frame_start = self.asset.start_frame                      # Set the start frame (from asset manager)
        scene.frame_end = self.asset.end_frame                          # Set the end frame (from the asset manager)
        scene.frame_step = 1                                            # Set frame step to '1'
        for area in bpy.context.screen.areas:                           # Itterate through all screen types
            if area.type == 'VIEW_3D':                                  # Open only if the screen type is 'VIEW_3D'
                space = area.spaces[0]                                  # Set space to the current space
                space.region_3d.view_perspective = 'CAMERA'             # Set the perspective to 'CAMERA' view
                space.show_only_render = True                           # Set 'Only Render' to 'ON'
                space.fx_settings.use_dof = True                        # Set 'Use DOF' to 'ON'
                space.fx_settings.use_ssao = True                       # Set 'Ambient Occlusion' to 'ON'

    def render_open_gl(self):
        '''
        
        '''
        bpy.ops.render.opengl(animation=True)                                         # Playblast from 'OpenGL'

print("Script begining")
run_stuff()