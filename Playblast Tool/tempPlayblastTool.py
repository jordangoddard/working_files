#from core import log, asset
import bpy

def run_stuff():
    print("\n\nI am running the first class\n\n")
    return Preferences()


class Movies(object):
    def __init__(self,playblast):
        self.playblast = playblast
        self.filepath = self.playblast.filepath
        self.execute()

    def execute(self):
        self.create_rvio()

    def create_rvio(self):
        return RvioInfo(self)


class log(object):
    def info(log_info):
        """
        Write temporary log file
        """
        log = log_info
        import time
        from datetime import datetime
        date_stamp = time.strftime("%Y-%m-%d")
        try:
            fileread = open("C:\\Temp\\working.log", "r")
            fileread.close()
        except:
            file = open("C:\\Temp\\working.log", "w")
            file.write("%s------------------Working Log------------------\n\n\n"%(date_stamp))
            file.write("%s --> %s\n" %(datetime.now(), log))
            print(log)
            file.close()
        else:
            file = open("C:\\Temp\\working.log", "a")
            file.write("%s --> %s\n" %(datetime.now(), log))
            print(log)
            file.close()

    def error(log_info):
        """
        Write temporary log file
        """
        log = log_info
        import time
        from datetime import datetime
        date_stamp = time.strftime("%Y-%m-%d")
        try:
            fileread = open("C:\\Temp\\workingerror.log", "r")
            fileread.close()
        except:
            file = open("C:\\Temp\\workingerror.log", "w")
            file.write("%s------------------Working Error Log------------------\n\n\n"%(date_stamp))
            file.write("%s --> %s\n" %(datetime.now(), log))
            print(log)
            file.close()
        else:
            file = open("C:\\Temp\\workingerror.log", "a")
            file.write("%s --> %s\n" %(datetime.now(), log))
            print(log)
            file.close()


class RvioInfo(object):
    def __init__(self, movies):
        from datetime import datetime
        print("Entered RVIO")
        self.movies = movies
        end_resolution_x = 960
        end_resolution_y = 720
        
        self.font_size = 17
        self.client_shot_code = self.movies.playblast.asset.code
        self.shot_code = self.client_shot_code
        self.show_code = self.movies.playblast.asset.show.code
        self.artist = "Just for testing"
        self.revision = 1
        self.status = "Complete"
        self.rank = 10
        self.pass_number = 7
        self.fov = 50
        self.fps = 24 # self.movies.playblast.asset.show.prefrences.timebase
        self.curr_date = datetime.now()
        
        self.rv_support_path = "C:\\pipeline\\rv\\rv-win64-x86-64-current\\rv-win64-x86-64-6.2.2\\bin"
        self.rv_path = self.rv_support_path
        '''
        self.local_pblast_name = 
        self.min_frame = 
        self.max_frame = 
        self.local_file = 
        burn_in = None
        self.fps = 
        threads = 
        '''
        #self.execute()
    
    def execute(self):
        #self.open_rvio()
        self.dosomething()

    def open_rvio(self):
        import subprocess
        pb_path = self.movies.filepath
        subprocess.Popen('"%s/rv" [ %s ]' %(self.rv_support_path, pb_path))

    def __str__(self):
        log.info("Running main RVIO string generation")
        #return self.burn_in_string()

    # Spit out the information required to do an RVIO encode with the overlay information
    def burn_in_string(self):
        matte = " -overlay matte %s %s" % (self.matte_aspect, self.matte_opacity)
        tangent_burnin = ' -overlay tangent_burnin %s %s %s %s %s %s %s %s %s %s %s %s' % (
                self.font_size,
                self.client_shot_code,
                self.shot_code,
                self.show_code,
                self.artist,
                self.revision,
                self.status,
                self.rank,
                self.pass_number,
                self.fov,
                "%sfps" % self.fps,
                self.curr_date
                )
        return "%s %s" % (matte, tangent_burnin)

    def encode(self): #this should be in playblast
        import subprocess, re
        self.shot = self.movies.playblast.asset.code
        log.info("Encoding movie to send to snapshot")
        # Encode movie file with RVIO to send to the snapshot
        # @note: progressWindow is bogus - can't set the size, to have to fake the ultimate size by setting the
        # status message really large, then overwriting it with the real status.  
        try:
            log.info("Getting local and server paths for %s" % self.movies.playblast.asset.code)
            self.local_path = ("C:/temp/%s.mov" %(self.movies.playblast.asset.show.code))
            self.local_file = "%s.mov" % (self.movies.playblast.asset.show.code)

            encode_sp = None
            burn_in = ""
            if self.rv_support_path:
                burn_in = RvioInfo(self.shotfile, self.shot, self.sequence, self.show).burn_in_string()

            # RVIO can fail if there's not enough memory - @todo : this needs to be
            # tuned over time.
            threads = 4
            free_memory = memory(freeMemory=True)
            frames = self.shot.frame_out - self.shot.frame_in
            if free_memory < 2000 and frames > 50:
                threads = 1
            elif free_memory < 3000 and frames > 50:
                threads = 2

            log.info("Utilizing %s cores to playblast and encode" % threads)
            if not self.shot.audio.exists():
                log.info("Playblasting to snapshot without audio")
                encode_sp = subprocess.Popen(
                                ('"%s/rvio" %s.%s-%s@@@@.iff -o %s \
                                    %s \
                                    -codec avc1 -quality .75 \
                                    -outgamma 0.65 -v -outfps %i \
                                    -rthreads %s' %
                                    (   self.rv_path, 
                                        self.local_pblast_name, 
                                        self.min_frame, 
                                        self.max_frame, 
                                        self.local_file, 
                                        burn_in,
                                        self.shot.get_fps(),
                                        threads)),
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
            else:
                log.info("Playblasting to snapshot with audio")
                log.info("Audio path: %s" % self.shot.audio.path)
                encode_sp = subprocess.Popen(
                                ('"%s/rvio" [ %s.%s-%s@@@@.iff %s ] -o %s \
                                    %s \
                                    -codec avc1 -quality .75 \
                                    -outgamma 0.65 -v -outfps %i \
                                    -rthreads %s' %
                                    (   self.rv_path, 
                                        self.local_pblast_name, 
                                        self.min_frame, 
                                        self.max_frame, 
                                        self.shot.audio.path, 
                                        self.local_file, 
                                        burn_in,
                                        self.fps,
                                        threads)),
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)

            log.info("Encoding playblast with RVIO for %s" % self.shot)
            while True and encode_sp:
                # Continue reading from stdout until RVIO is finished, then break
                next_line = encode_sp.stdout.readline()
                if not next_line:
                    break

                # Search for a % marker in the RVIO output, then "decode" it to get the % done
                if re.search("%", next_line):
                    tmp = next_line.split("(")[1]
                    tmp = tmp.split("%")[0]

                progressWindow( edit=True, progress=progress, status=('Encode: ' + next_line))
                log.info(next_line.strip())

        except:
            log.error("Something failed during playblast of %s : %s" % (self.shot, sys.exc_info()[0]))
            raise
        finally:
            # Ensure that we close the progressWindow, and unlock Maya for use
            pass


    def dosomething(self):
        pass


class Preferences(object):
    def __init__(self, show=None):
        log.info("I got to the preferences class")
        self.pk = 1
        self.url = "http://10.1.1.50:8000/api/shows/1/"
        self.show = "MOVIE NAME GOES HERE"
        self.p_drive = "c:/temp"
        self.p_drive_linux = "/dfs"
        self.res_render_x = 1920
        self.res_render_y = 1080
        self.timebase = 24 # not yet in the asset manager
        self.codec = "mp4"
        
        self.run_show()
        
        

    def run_show(self):
        return Show(self)


class Show(object):
    def __init__(self, preferences):
        # this is the group
        log.info("I got to the show class")
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
        log.info("I got to the asset class")
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
        from datetime import datetime
        end_resolution_x = 960
        end_resolution_y = 720
        
        self.matte_aspect = 1.785
        self.matte_opacity = 1.0
        
        self.frame_start = 1                                        # self.asset.start_frame
        self.frame_end = 10                                         # self.asset.end_frame
        
        self.rv_support_path = "C:\\pipeline\\rv\\rv-win64-x86-64-current\\rv-win64-x86-64-6.2.2\\bin"
        render_x_size = 960
        render_y_size = 540
        self.asset = asset
        log.info("I got to the playblast class")
        print(self.asset.code)
        print(self.asset.show.code)
        print(self.asset.show.preferences.show)
        
        self.font_size = 17
        self.client_shot_code = self.asset.code
        self.shot_code = self.client_shot_code
        self.show_code = self.asset.show.code
        self.artist = "Just for testing"
        self.revision = 1
        self.status = "Complete"
        self.rank = 10
        self.pass_number = 7
        self.fov = 50
        self.fps = 24                                               # self.movies.playblast.asset.show.prefrences.timebase
        self.curr_date = datetime.now()
        
        self.rv_path = self.rv_support_path
        self.local_pblast_name = self.asset.code
        self.min_frame = self.frame_start
        self.max_frame = self.frame_end
        self.local_file = self.asset.filename
        burn_in = None
        threads = ""
        
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
        self.encode()

    def movie_create(self):
        return Movies(self)

    def burn_in_string(self):
        matte = " -overlay matte %s %s" % (self.matte_aspect, self.matte_opacity)
        tangent_burnin = ' -overlay tangent_burnin %s %s %s %s %s %s %s %s %s %s %s %s' % (
                self.font_size,
                self.client_shot_code,
                self.shot_code,
                self.show_code,
                self.artist,
                self.revision,
                self.status,
                self.rank,
                self.pass_number,
                self.fov,
                "%sfps" % self.fps,
                self.curr_date
                )
        return "%s %s" % (matte, tangent_burnin)

    def encode(self):   # json
        '''
        This will...
        '''
        threads = 4
        import subprocess, re
        self.shot = self.asset.code
        log.info("Encoding movie to send to snapshot")
        # Encode movie file with RVIO to send to the snapshot
        # @note: progressWindow is bogus - can't set the size, to have to fake the ultimate size by setting the
        # status message really large, then overwriting it with the real status.  
        try:
            log.info("Getting local and server paths for %s" % self.asset.code)
            self.local_path = ("C:/temp/%s.mov" %(self.asset.show.code))
            self.local_file = "%s.mov" % (self.asset.show.code)

            encode_sp = None
            burn_in = ""
            if self.rv_support_path:
                burn_in = self.burn_in_string()

            # RVIO can fail if there's not enough memory - @todo : this needs to be
            # tuned over time.
            '''
            threads = 4
            free_memory = memory(freeMemory=True)
            frames = self.shot.frame_out - self.shot.frame_in
            if free_memory < 2000 and frames > 50:
                threads = 1
            elif free_memory < 3000 and frames > 50:
                threads = 2
            log.info("Utilizing %s cores to playblast and encode" % threads)
            '''
            
            '''
            if not self.shot.audio.exists():
                log.info("Playblasting to snapshot without audio")
                encode_sp = subprocess.Popen(
                                ('"%s/rvio" %s.%s-%s@@@@.iff -o %s \
                                    %s \
                                    -codec avc1 -quality .75 \
                                    -outgamma 0.65 -v -outfps %i \
                                    -rthreads %s' %
                                    (   self.rv_path, 
                                        self.local_pblast_name, 
                                        self.min_frame, 
                                        self.max_frame, 
                                        self.local_file, 
                                        burn_in,
                                        self.shot.get_fps(),
                                        threads)),
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
            
            else:
                log.info("Playblasting to snapshot with audio")
                log.info("Audio path: %s" % self.shot.audio.path)
                encode_sp = subprocess.Popen(
                                ('"%s/rvio" [ %s.%s-%s@@@@.iff %s ] -o %s \
                                    %s \
                                    -codec avc1 -quality .75 \
                                    -outgamma 0.65 -v -outfps %i \
                                    -rthreads %s' %
                                    (   self.rv_path, 
                                        self.local_pblast_name, 
                                        self.min_frame, 
                                        self.max_frame, 
                                        self.shot.audio.path, 
                                        self.local_file, 
                                        burn_in,
                                        self.shot.get_fps(),
                                        threads)),
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
            '''
            
            log.info("Playblasting to snapshot with audio")
            # log.info("Audio path: %s" % self.shot.audio.path)
            print("\n\n\n\nOpen RV\n\n\n\n")
            '''
            encode_sp = subprocess.Popen(
                            ('"%s/rv" [ %s.%s-%s@@@@.iff ] -o %s \
                                %s \
                                -codec avc1 -quality .75 \
                                -outgamma 0.65 -v -outfps %i \
                                -rthreads %s' %
                                (   self.rv_path, 
                                    self.local_pblast_name, 
                                    self.min_frame, 
                                    self.max_frame, 
                                    self.local_file, 
                                    burn_in,
                                    self.fps,
                                    threads)),
                            shell=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT)
            '''
            
            subprocess.Popen(
                            ('"%s/rv" [ %s ] -play - fullscreen-o %s -outgamma 0.65 -v -outfps %i -rthreads %s' %
                                (   self.rv_path, 
                                    self.filepath, 
                                    burn_in,
                                    self.fps,
                                    threads)))
            
            #subprocess.Popen('"%s/rv" [ %s ]' %(self.rv_path, self.filepath))
            
            '''
            log.info("Encoding playblast with RVIO for %s" % self.shot)
            while True and encode_sp:
                # Continue reading from stdout until RVIO is finished, then break
                next_line = encode_sp.stdout.readline()
                if not next_line:
                    break

                # Search for a % marker in the RVIO output, then "decode" it to get the % done
                if re.search("%", next_line):
                    tmp = next_line.split("(")[1]
                    tmp = tmp.split("%")[0]

                progressWindow( edit=True, progress=progress, status=('Encode: ' + next_line))
                log.info(next_line.strip())
            '''
        except:
            log.error("Something failed during playblast of %s." % (self.asset.code))
            raise
        finally:
            # Ensure that we close the progressWindow, and unlock Maya for use
            pass
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
        Set all the output settings for blender to render in OpenGL
        '''
        scene = bpy.data.scenes[self.asset.code]                        # Set 'scene' to the current scene data
        self.filepath = "C:\\Temp\\%s.mov"%scene.name
        render = bpy.data.scenes[scene.name].render                     # Set 'render' to the current scene render settings
        
        # render contorls.
        render.filepath = self.filepath
        render.stamp_font_size = 17                                     # Set stamp size to '17'
        render.stamp_background = (0,0,0,1)                             # Set stamp background to '0,0,0,1'
        render.use_stamp = False                                        # Set render stamp to 'ON'
        render.use_stamp_time = False                                   # Set render stamp time to 'OFF'
        render.use_stamp_date = False                                   # Set render stamp date to 'OFF'
        render.use_stamp_render_time = False                            # Set render stamp render time to 'OFF'
        render.use_stamp_frame = False                                  # Set render stamp frame to 'ON'
        render.use_stamp_scene = False                                  # Set render stamp scene to 'ON'
        render.use_stamp_camera = False                                 # Set render stamp camera to 'OFF'
        render.use_stamp_lens = False                                   # Set render stamp lens to 'ON'
        render.use_stamp_filename = False                               # Set render stamp file name to 'OFF'
        render.use_stamp_marker = False                                 # Set render stamp marker to 'OFF'
        render.use_stamp_sequencer_strip = False                        # Set render stamp sequence strip to 'OFF'
        render.image_settings.file_format = 'FFMPEG'                    # Set image file format for render to 'FFMPEG'
        render.ffmpeg.format = 'QUICKTIME'                              # Set render format to 'Quicktime'
        render.ffmpeg.codec = 'MPEG4'                                   # Set render codec to 'MPEG4'
        render.ffmpeg.audio_codec = 'PCM'                               # Set render audio codec to 'PCM'
        render.resolution_x = self.asset.show.preferences.res_render_x  # Set render resolution to 1920x1080
        render.resolution_y = self.asset.show.preferences.res_render_y  # Set render resolution to 1920x1080
        render.resolution_percentage = 50                               # Set render percentage to 50%
        render.fps = self.asset.show.preferences.timebase               # Set framerate to 24fps
        render.antialiasing_samples = '8'                               # Set render samples
        render.pixel_aspect_x = 1.0                                     # Set aspect ratio
        render.pixel_aspect_y = 1.0                                     # Set aspect ratio
        render.pixel_filter_type = 'MITCHELL'                           # Set filter type
        render.filter_size = 1.0                                        # Set filter size
        render.use_motion_blur = False                                  # Set motion blur to 'OFF'
        render.motion_blur_samples = 1                                  # Set motion blur samples
        render.motion_blur_shutter = 0.5                                # Set motion blur shutter speed
        
        # scene controls
        scene.frame_current = 1                                         # Set current fram to '1' (not necesary, just good form)
        scene.frame_start = self.frame_start                            # Set the start frame (from asset manager)
        scene.frame_end = self.frame_end                                # Set the end frame (from the asset manager)
        scene.frame_step = 1                                            # Set frame step to '1'
        
        # space controls
        for area in bpy.context.screen.areas:                           # Itterate through all screen types
            if area.type == 'VIEW_3D':                                  # Open only if the screen type is 'VIEW_3D'
                space = area.spaces[0]                                  # Set space to the current space
                space.region_3d.view_perspective = 'CAMERA'             # Set the perspective to 'CAMERA' view
                space.show_only_render = True                           # Set 'Only Render' to 'ON'
                space.fx_settings.use_dof = True                        # Set 'Use DOF' to 'ON'
                space.fx_settings.use_ssao = True                       # Set 'Ambient Occlusion' to 'ON'

    def render_open_gl(self):
        '''
        Playblast from OpenGL
        '''
        bpy.ops.render.opengl(animation=True)                           # Playblast from 'OpenGL'

print("Script begining")
run_stuff()