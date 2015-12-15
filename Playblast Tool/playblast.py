from core import log, files
from core.classes import api_helpers
from core.gui.animation import playblast_window
from pymel.core import *
import os
import sys
import shutil
from time import localtime
from time import strftime
import requests
import json


## class RvioInfo
class RvioInfo:
    def __init__(self, shotfile, shot, sequence, show):
        self.shotfile = shotfile
        self.shot = shot
        self.sequence = sequence
        self.show = show

        self.matte_aspect = 1.785
        self.matte_opacity = 1.0

        self.opacity = 0.35
        self.grey = 1.0
        self.font_size = 70
        self.client_shot_code = None
        if not self.client_shot_code:
            self.client_shot_code = "..."
        self.show_code = self.show.code.lower()
        self.shot_code = "%s.%s" % (self.sequence.code, self.shot.code)
        self.artist = api_helpers.get_current_user()
        self.revision = self.shot.current_version
        self.status = '---'
        self.rank = ''
        self.pass_number = ''
        self.fov = self.shotfile.fov
        self.fps = self.shotfile.get_fps()
        self.curr_date = strftime("%m-%d-%y_%H:%M:%S", localtime()) 


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


class MovieFile:                                                              # This is the MovieFile class                                         # Main MovieFile Class                                              # MovieFile()                                               
    def __init__(self, **kwargs""", asset"""):                                # This should be passed the asset.                                    # Main __init__ function run on intatiation of the class 'MovieFile'                                                            
#       self.asset = asset                                                                                                                          # This is the asset that is passed from the asset manager           # self. asset = asset                                       
        ''' Required '''
        self.url = kwargs.get('url','')                                                                                                             # This is a property of the asset                                   # self.url = self.asset.url                                 *SAME
        self.pk = kwargs.get('pk','')                                         # What is a 'pk'?                                                     # This is a property of the movie class on the asset                # self.pk = self.asset.movie.pk                             
        #self.daily = kwargs.get('daily','')                                   # What is a 'daily'?                                                  # This is a property of the movie class on the asset                # self.daily = self.asset.movie.daily                       
        #self.approved = kwargs.get('approved','')                             # Is this a bool of wether or not the asset has been aproved?         # This is a property of the movie class on the asset                # self.approved = self.asset.movie.approved                 
        ''' Not required for POST '''
        self.version_number = kwargs.get('version_number','')                                                                                       # This is a property of the movie class on the asset                # self.version_number = self.asset.movie.version_number     
        self.path = kwargs.get('path','')                                                                                                           # This is a property of the movie class on the asset                # self.path = self.asset.movie.path                         
        self.movie_file = kwargs.get('movie_file','')                                                                                               # This is a property of the movie class on the asset                # self.movie_file = self.asset.movie.file                   
        self.movie_file_url = kwargs.get('movie_file_url','')                                                                                       # This is a property of the movie class on the asset                # self.movie_file_url = self.asset.movie.url                
        self._shotfile_url = kwargs.get('shotfile')                                                                                                 # This is a property of the asset                                   # self._shotfile_url = self.asset.url                       *SAME
        self.thumbnail = kwargs.get('thumbnail','')                                                                                                 # This is a property of the movie class on the asset                # self.thumbnail = self.asset.movie.thumb                   
        self.thumbnail_url = kwargs.get('thumbnail_url','')                                                                                         # This is a property of the movie class on the asset                # self.thumbnail_url = self.asset.movie.thum.url            
        self.created = kwargs.get('created','')                               # What is this? TIme created                                                      # This is a property of the movie class on the asset                # self.created = self.asset.movie.created                   
        self.process = kwargs.get('process')                                  # What is this? Animation versus Layout versus ??                                                       # This is a property of the movie class on the asset                # self.process = self.asset.movie.process                   

    def shotfile():                                                           # Is this necesary?                                                   # Will all this data be handled by the asset manager?               # self.shotfile = self.asset.file                           **SAME
        def fget(self):                                                                                                                                                                                                                                                             
            print "URL: ", self._shotfile_url                                                                                                                                                                                                                                       
            response = requests.get(self._shotfile_url)                                                                                                                                                                                                                             
            return json.loads(response.text, object_hook = api_helpers.decode_shotfile)                                                                                                                                                                                             
        return locals()                                                                                                                                                                                                                                                             
    shotfile = property(**shotfile())                                                                                                               # This will come from the asset manager                             # self.shotfile = self.asset.file                           **SAME

    def encode(self):                                                          # This will encode the data from python to json for the database                                                                
        '''
        Encode for API - only the list view URL and some small pieces of info required.
        '''
        encoded = {}
        encoded['daily'] = self.daily
        encoded['approved'] = self.approved
        encoded['shotfile'] = self._shotfile_url ''' asset needs to be URL for API to find FK relationship '''
        print 'VERSION_NUMBER: ', self.shotfile.current_version_number
        encoded['version_number'] = self.shotfile.current_version_number
        return json.dumps(encoded)    

    def create(self):
        '''
        Create a new version:  skip pk and url, as those will be generated on the post
        '''
        data = self.encode()
        headers = {'content-type': 'application/json'}
        response = requests.post(self.shotfile._movies_url, data=data, headers=headers)
        return json.loads(response.text, object_hook = api_helpers.decode_shotfile_movie)


class Playblast:
    def __init__(self, shotfile):
        self.shotfile = shotfile
        self.shot = self.shotfile.shot
        self.sequence = self.shot.sequence
        self.movie = None
        self.min_frame = 0
        self.max_frame = 0
        self.width = self.shotfile.shot.sequence.show.res_playblast_x
        self.height = self.shotfile.shot.sequence.show.res_playblast_y

        # Path to RV executables
        self.rv_path = "C:/Program Files (x86)/Tweak/RV-3.10/bin"
        if not os.path.exists(self.rv_path):
            self.rv_path = "C:/Program Files (x86)/Tweak/RV-3.8/bin"
        if not os.path.exists(self.rv_path):
            self.rv_path = "C:/Program Files (x86)/Tweak/RV-3.12.19-32/bin"
        if not os.path.exists(self.rv_path):
            log.error("Can't find the path to RV or RVIO - contact support")
            
    def execute(self, local=True):
        # Shotfile needs to save itself first, then we can create a movie file
        # that we use to save the resulting playblast to

        currentTime(self.shot.start)

        # Deselect everything
        selected = ls(selection=True)
        select(deselect=True)

        if not local:
            # Create a movie file for this shot - this gives us the filenames, paths, and
            # everything else we require to do a playblast

            self.movie = MovieFile(shotfile=self.shotfile.url, approved=False, daily=False)
            self.movie = self.movie.create()

        # Setup options
        textured = menuItem("op_PlayblastTexturesChk", query=True, checkBox=True)
        editorial_range = menuItem("op_PlayblastEditorialRangeChk", query=True, checkBox=True)

        # Bring up the playblast window to capture a single frame thumbnail
        thumb_win, viewport_name = playblast_window(process=self.shotfile.process,
                width=int( self.width * 0.15), height=int(self.height * 0.15), textured=textured)
        thumb_image = self.screen_capture(local=local)

        # Bring up the playblast window
        pb_win, viewport_name = playblast_window(process=self.shotfile.process, textured=textured)
        if local:
            movie_file = self.local_movie_file()
        else:
            movie_file = files.local_file(files.dm(self.movie.movie_file))

        # Get the soundfile in the timeline
        sound_file = timeControl("timeControl1", query=True, sound=True)
        
        if editorial_range:
            output_movie = playblast(
                    format="qt", filename=movie_file,
                    sound=sound_file,   
                    sequenceTime=0, clearCache=0, viewer=1, 
                    showOrnaments=0, fp=4, percent=100, compression="Motion JPEG A", quality=70,
                    forceOverwrite=True, startTime=self.shot.start, endTime=self.shot.end+1 )
        else:
            # Just playblast what's in the timeline
            output_movie = playblast(
                    format="qt", filename=movie_file,
                    sequenceTime=0, clearCache=0, viewer=1, 
                    showOrnaments=0, fp=4, percent=100, compression="Motion JPEG A", quality=70,
                    forceOverwrite=True)
        evalDeferred('from pymel.core import deleteUI; deleteUI("%s")' % pb_win)

        if not local:
            # This goes to the server - setup server based paths, and copy files
            self.shotfile = self.shotfile.save()


            # Move the thumbnail and the movie file to the appropriate place(s)

            log.info("Copying thumbnail from %s to %s" % (thumb_image, files.dm(self.movie.thumbnail)))
            log.info("Copying playblast movie from %s to %s" % (output_movie, files.dm(self.movie.movie_file)))
            shutil.copy(thumb_image, files.dm(self.movie.thumbnail))
            shutil.copy(movie_file, files.dm(self.movie.movie_file))

        # Reset the selected items
        select(selected)

        # Finally, playback the resulting movie file
        self.playback(local=local)

    def local_movie_file(self):
        return "C:/Temp/%s.%s_%s.mov" % (self.sequence.code, self.shot.code, self.shotfile.process)

    def server_movie_file(self):
        return files.dm(self.movie.movie_file)

    def screen_capture(self, local=True):
        # Import api modules
        import maya.OpenMaya as api
        import maya.OpenMayaUI as apiUI

        # Grab the last active 3d viewport
        view = apiUI.M3dView.active3dView()

        # Change the current time to get the view to refresh
        import time
        current_time = currentTime(query=True)
        time.sleep(0.25)
        currentTime(current_time+1, edit=True)
        time.sleep(0.25)
        currentTime(current_time, edit=True)

        # Read the color buffer from the view, and save the MImage to disk
        image = api.MImage()
        view.readColorBuffer(image, True)

        if local:
            file_path = "C:/Temp/%s.%s_%s.png" % (self.sequence.code, self.shot.code, self.shotfile.process)
        else:
            file_path = files.local_file(files.dm(self.movie.thumbnail))
            # Make sure the directory is created first
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except:
                    log.warning("Couldn't create directory %s" % os.path.dirname(file_path))
                    return None

        image.writeToFile(file_path, 'png')
        return file_path

    def playback(self, local=True):
        # Playback the image files output by the playblast - "fix" the gamma,
        # and set the FPS based on the show
        import subprocess
        if local:
            movie_file = self.local_movie_file()
        else:
            movie_file = self.server_movie_file()
        # Playback the movie file that was saved to the server
        subprocess.Popen('"%s/rv" %s -fps %i -l -rthreads 2 -play' % 
                (self.rv_path, movie_file, 24.0)) # TODO: get the FPS from the shot



## class Playblast
#
#  @brief Gets the playblast information from MSSQL, and creates member 
#  variables on the class for easy access
class PlayblastOld:
    def __init__(self, shotfile):
        self.shotfile = shotfile
        self.shot = shotfile.shot
        self.show = shot.sequence.show
        log.info( "Getting data for playblast for %s.%s" % (self.sequence, self.shot))

        self.min_frame = 0
        self.max_frame = 0
        self.local_pblast_name = "C:/temp/banzai_data/temp_playblast"
        
        # Path to RV executables
        self.rv_path = "C:/Program Files (x86)/Tweak/RV-3.10/bin"
        if not os.path.exists(self.rv_path):
            self.rv_path = "C:/Program Files (x86)/Tweak/RV-3.8/bin"
        if not os.path.exists(self.rv_path):
            log.error("Can't find the path to RV or RVIO - email maya@hawaiianimation.com")

        self.rv_support_path = os.getenv('RV_SUPPORT_PATH')

        # Local storage used for caching multiple hits


    def __str__(self):
        return 'Playblast for %s.%s' % (self.sequence, self.shot)

    def create_dirs(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except:
                log.error("Can't create playblast path %s for shot %s.%s" % 
                       (dir_path, self.sequence, self.shot))
                return False
        return True

    '''
    def server_path():
        def fget(self):
            if not self._server_path:
                #row = sql.create_playblast_version(self.shot.show.code, self.shot.sequence.code, 
                                                    self.shot.code, self.shot.process, 0)
                self._server_path = None
                #if row.MovieFilePath:
                #    self._server_path = row.MovieFilePath.replace("\\","/")
            return self._server_path
        return locals()
    server_path = property(**server_path())

    def server_path_version():
        def fget(self):
            if not self._server_path_version:
                row = sql.create_playblast_version(self.shot.show.code, self.shot.sequence.code, 
                                                    self.shot.code, self.shot.process, 0)
                self._server_path_version = None
                if row.MovieFilePathVersion:
                    self._server_path_version = row.MovieFilePathVersion.replace("\\","/")
            return self._server_path_version
        return locals()
    server_path_version = property(**server_path_version())
    '''

    def movie_file():
        def fget(self):
            if not self._movie_file:
                row = sql.create_playblast_version(self.shot.show.code, self.shot.sequence.code, 
                                                    self.shot.code, self.shot.process, 0)
                self._movie_file = row.MovieFileName
            return self._movie_file
        return locals()
    movie_file = property(**movie_file())


    ## Perform a playblast of this shot - creates an icon for it at the same 
    #  time, using the midframe
    #  playblasting, otherwise use what's in Maya
    #  @param percent Scale of playblast window vs what's in the DB
    #  @param textured Perform playblast with textures on?
    #  @param dynamics_enabled Playblast with dynamics on?
    def execute(self, percent=100, textured=False, dynamics_enabled=False, create_version=False, comment=None, batch=False):
        debug = 0
        # First, make sure we're in GUI mode - can't playblast otherwise
        from pymel.core.general import about
        if about(batch=True):
            log.warning( "Can't perform playblast in batch mode - requires GUI to run")
            return
        # We're in GUI mode, continue with playblast
        log.info( "Performing playblast of shot %s" % self.shot)
        # Create version if we're playblasting to snapshot for approvals
        if create_version:
            log.info( "Publishing shot %s prior to playblast" % self.shot)
            if not debug:
                if comment or batch:
                    self.shot.vault()
                else:
                    from internal.publishing import gui as publish_gui
                    published = publish_gui.publish_shot_gui(self.shot)
                    if not published:
                        log.warning( "Playblast of %s was cancelled" % self.shot)
                        return False
        # Store a list of selected objects, to restore at the end
        # Deselect all objects, so that no wireframes show
        selected = ls(selection=True)
        select(deselect=True)
        # Set the start and end timerange appropriately
        self.set_timerange(create_version = create_version)
        # Construct the window to playblast through - this stuff is in the 
        # core.gui.animation module
        from core.gui import animation as anim_gui
        playblast_window, model_editor = anim_gui.playblast_window( self.shot.process, self.width, self.height, textured=textured, dynamics_enabled=dynamics_enabled)
        # Need to set then reset the image format in the render globals - for some stupid reason, Autodesk
        # uses this setting for playblasts as of 2011 - didn't for the last 15 years.
        default_render_globals = ls('defaultRenderGlobals')[0]
        prev_image_format = None
        if default_render_globals:
            log.info("Setting render globals to IFF for playblast")
            prev_image_format = default_render_globals.imageFormat.get()
            default_render_globals.imageFormat.set(7) # 7 == IFF
        # Do the actual playblast - have to defer the evaluation of the 
        # command, to give the window time to draw
        playblast_finished = playblast(format="iff", filename=self.local_pblast_name, viewer=False, 
                showOrnaments=False, fp=4, percent=100, fo=True, quality=100)
        # Reset the render globals to what the user had it set to before
        if prev_image_format:
            log.info("Resetting render globals to user defined value: %s" % prev_image_format)
            default_render_globals.imageFormat.set(prev_image_format)
        if not playblast_finished:
            log.warning("User cancelled the playblast for %s - not saving to snapshot" % self.shot)
            if selected:
                select(selected)
            return
        if create_version:
            # Publish the movie file to snapshot
            self.encode()
            self.publish()
        # Delete the playblast window now that we're done with it - 
        # use deferred to ensure that the playblast is done before 
        # deleting the window
        evalDeferred('from pymel.core import deleteUI; deleteUI("%s")' % playblast_window)
        # Restore selection
        if selected:
            select(selected)
        # Run RV on the resulting images - if we're in batch mode,
        # skip this, and if we're not creating a version in the DB,
        # then it's a local playblast - run RV on the local images
        # instead of on the movie in snapshot
        if not batch:
            if create_version:
                self.playback(movie=True)
            else:
                self.playback()


    def publish(self):
        log.info("Publishing movie for %s to snapshot" % self.shot)

        # Get paths for the playblast from MSSQL
        log.info( "Getting playblast paths")

        self.local_file = "%s/%s" % (self.local_path, self.movie_file)
        self.server_file = "%s/%s" % (self.shotfile.playblast_server_path, self.movie_file)

        # Copy the movie file to the database, and log it with MSSQL
        log.info( "Saving movie for shot %s to snapshot and network file storage" % self.shot)
        try:
            from_file = "%s/%s" % (self.local_path, self.movie_file)
            to_file = "%s/%s" % (self.server_path, self.movie_file)
            log.info("Copying %s > %s" % (from_file, to_file))
            shutil.copy(from_file, to_file)
            log.info( "Copied %s > %s" % (from_file, to_file))

            from_file = "%s/%s" % (self.local_path, self.movie_file)
            to_file = "%s/%s" % (self.server_path_version, self.movie_file)
            log.info("Copying %s > %s" % (from_file, to_file))
            shutil.copy(from_file, to_file)
            log.info( "Copied %s > %s" % (from_file, to_file))

        except:
            log.error( "Could not copy playblast for shot %s to server paths %s and/or %s" % 
                    (self.shot, self.server_path, self.server_path_version))
        else:
            # Store info in MSSQL
            sql.create_playblast_version(self.shot.show.code, self.shot.sequence.code, 
                                        self.shot.code, self.shot.process, 1)

    def local_path(self):
        return files.local_file("C:/temp") # TODO: this should return a local version of the server version

    def local_file(self):
        return "%s/%s.%s_%s.mov" % (files.local_file(self.local_path, self.sequence, self.shot, self.shotfile.process))

    def encode(self):
        import subprocess, re

        # Encode movie file with RVIO to send to the snapshot
        log.info("Encoding movie to send to snapshot")
        progress = 0

        # @note: progressWindow is bogus - can't set the size, to have to fake the ultimate size by setting the
        # status message really large, then overwriting it with the real status.  
        progressWindow(
                title = "Playblast Movie Encode",
                progress = progress,
                status = "---------------------------------------------------------------------------------------------------",
                isInterruptable=False)

        try:

            log.info("Getting local and server paths for %s" % self.shot)
            self.local_path = ("C:/temp/banzai_data/projects/%s/movies/%s" % (self.shot.show.code, self.shot.sequence.code))
            self.local_file = "%s/%s" % (self.local_path, self.movie_file)

            # Make sure the directories exist first - create it if not, and bail if we fail
            if not self.create_dirs(self.local_path): 
                log.error("Could not create local %s dir for playblast of %s" % (self.local_path, self.shot))
                return
            if not self.create_dirs(self.server_path): 
                log.error("Could not create server %s dir for playblast of %s" % (self.server_path, self.shot))
                return
            log.info("Created local and server paths for the playblast of %s" % self.shot)

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
                                        self.shot.get_fps(),
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
                    progress = int(float(tmp))

                progressWindow( edit=True, progress=progress, status=('Encode: ' + next_line))
                log.info(next_line.strip())
                progress += 1

        except:
            log.error("Something failed during playblast of %s : %s" % (self.shot, sys.exc_info()[0]))
            raise
        finally:
            # Ensure that we close the progressWindow, and unlock Maya for use
            progressWindow(endProgress=True)


    def set_timerange(self, create_version=False):
        # Set time range to that in MSSQL if we are creating a version for snapshot and the check
        # box for the menu entry that controls this is true otherwise, use the current frame range
        if create_version == True and menuItem("bz_PlayblastEditorialRangeChk", query=True, checkBox=True):
            log.info("Setting timerange to Editorial range stored in database")
            self.shot.set_timeline()
        else:
            log.info("Playblasting timerange currently set in Maya")

        self.min_frame = int(playbackOptions(minTime=True, query=True))
        self.max_frame = int(playbackOptions(maxTime=True, query=True))

    def playback(self, movie=False):
        # Playback the image files output by the playblast - "fix" the gamma,
        # and set the FPS based on the show
        import subprocess
        if not movie:
            if self.shot.audio.path:
                subprocess.Popen('"%s/rv" [ %s.%s-%s@@@@.iff %s ] -fps %i -gamma 1.01 \
                                    -audiofs 512 -l -rthreads 2 -play' % 
                        (self.rv_path, self.local_pblast_name, self.min_frame, 
                            self.max_frame, self.shot.audio.path, self.shot.get_fps()))
            else:
                subprocess.Popen('"%s/rv" [ %s.%s-%s@@@@.iff ] -fps %i -l -gamma 1.01 -rthreads 2 -play' % 
                        (self.rv_path, self.local_pblast_name, self.min_frame, self.max_frame, self.shot.get_fps()))
        else:

            # Playback the movie file that was saved to the server
            subprocess.Popen('"%s/rv" %s/%s -fps %i -l -rthreads 2 -play' % 
                    (self.rv_path, self.server_path, self.movie_file, self.shot.get_fps()))



