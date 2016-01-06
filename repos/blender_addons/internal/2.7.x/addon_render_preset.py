# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Render Finaling",
    "author": "Tangent Animation",
    "version": (1, 2, 3),
    "blender": (2, 75, 0),
    "location": "View3D > Tools",
    "description": "Prepares a scene for publishing",
    "warning": "The addon still in progress! Make a backup!",
    "wiki_url": "https://tangentanimation.sharepoint.com/wiki/Pages/Render%20Finaling.aspx",
    "tracker_url": "",
    "category": "Tangent"}

import bpy
import cycles


class MasterProperties(bpy.types.PropertyGroup):
    """
    Property Used for the whole GUI in general
    """
    def set_usesimplify(self, value):
        """ Set Blender UI selection """
        current_scene_name = bpy.context.scene.name
        render = bpy.data.scenes[current_scene_name].render
        if value == 1:
            render.use_simplify = False
        else:
            render.use_simplify = True

    def get_usesimplify(self):
        """ Set list (aka button) Panel selection """
        current_scene_name = bpy.context.scene.name
        render = bpy.data.scenes[current_scene_name].render
        button_state = render.use_simplify
        if button_state:
            return 0
        else:
            return 1

    bpy.types.Scene.usesimplify = bpy.props.EnumProperty(name = "usesimplifystates", 
                                                         items = (('True', "On", "Enable quick preview render"),('False', "Off", "Disable quick preview render")), 
                                                         set = set_usesimplify,
                                                         get = get_usesimplify)

    def set_usessao(self, value):
        """ Set Blender UI selection """
        current_scene_area = bpy.context.screen.areas

        if value == 1:
            for area in current_scene_area:
                if area.type == 'VIEW_3D':
                    area.spaces[0].fx_settings.use_ssao = False
        else:
            for area in current_scene_area:
                if area.type == 'VIEW_3D':
                    area.spaces[0].fx_settings.use_ssao = True

    def get_usessao(self):
        """ Set list (aka button) Panel selection """
        current_scene_area = bpy.context.screen.areas
        for area in current_scene_area:
            if area.type == 'VIEW_3D':
                button_state = area.spaces[0].fx_settings.use_ssao
        if button_state:
            return 0
        else:
            return 1

    bpy.types.Scene.usessao = bpy.props.EnumProperty(name = "usessaostates", 
                                                     items = (('SSAO_ON', "On", "Enable screen space AO"),('SSAO_OFF', "Off", "Disable screen space AO")), 
                                                         set = set_usessao,
                                                         get = get_usessao)

    def set_useonlyrender(self, value):
        """ Set Blender UI selection """
        current_scene_area = bpy.context.screen.areas

        if value == 1:
            for area in current_scene_area:
                if area.type == 'VIEW_3D':
                    area.spaces[0].show_only_render = False
        else:
            for area in current_scene_area:
                if area.type == 'VIEW_3D':
                    area.spaces[0].show_only_render = True

    def get_useonlyrender(self):
        """ Set list (aka button) Panel selection """
        current_scene_area = bpy.context.screen.areas
        for area in current_scene_area:
            if area.type == 'VIEW_3D':
                button_state = area.spaces[0].show_only_render
        if button_state:
            return 0
        else:
            return 1

    bpy.types.Scene.useonlyrender = bpy.props.EnumProperty(name = "useonlyrenderstates", 
                                                           items = (('ONLYRENDER_ON', "On", "Display only renderable objects"),('ONLYRENDER_OFF', "Off", "Display all objects")), 
                                                           set = set_useonlyrender,
                                                           get = get_useonlyrender)

    def set_usedof(self, value):
        """ Set Blender UI selection """
        current_scene_area = bpy.context.screen.areas

        if value == 1:
            for area in current_scene_area:
                if area.type == 'VIEW_3D':
                    area.spaces[0].fx_settings.use_dof = False
        else:
            for area in current_scene_area:
                if area.type == 'VIEW_3D':
                    area.spaces[0].fx_settings.use_dof = True

    def get_usedof(self):
        """ Set list (aka button) Panel selection """
        current_scene_area = bpy.context.screen.areas
        for area in current_scene_area:
            if area.type == 'VIEW_3D':
                button_state = area.spaces[0].fx_settings.use_dof
        if button_state:
            return 0
        else:
            return 1

    bpy.types.Scene.usedof = bpy.props.EnumProperty(name = "usedofstates", 
                                                    items = (('USEDOF_ON', "On", "Enable depth of field on active camera"),('USEDOF_OFF', "Off", "Disable depth of field on active camera")), 
                                                    set = set_usedof,
                                                    get = get_usedof)

    bpy.types.Scene.renderpresets = bpy.props.EnumProperty(name = "renderpresettypes",
                                                           items = [('Shot Finaling Preview', "Shot Finaling Preview", "Shot Finaling Preview", 'NONE', 0),
                                                                    ('Shot Finaling Render', "Shot Finaling Render", "Shot Finaling Render", 'NONE', 1),
                                                                    ('Layout Review', "Layout Review", "Layout Review", 'NONE', 2),
                                                                    ('Blender Default', "Blender Default", "Blender Default", 'NONE', 3)],
                                                           default = 'Shot Finaling Preview')


class ApplyRenderSettingsButton(bpy.types.Operator):
    bl_idname = "render.apply_render_settings_button"
    bl_label = "Apply Render Settings"
    bl_options = {"UNDO"} 

    def invoke (self, context, event):
        """
        Invoke apply render settings
        """
        ars = ApplyRenderSettings(context.scene.renderpresets)
        ars.execute()

        reportpreset = context.scene.renderpresets
        self.report({'INFO'}, "Applied '%s' render preset." %reportpreset)                              # Send output to Blender Info header

        return {"FINISHED"}


class ApplyRenderSettings(object):
    """
    Apply render settings based on preset selected
    """

    def __init__(self, render_preset_selection):
        """
        Initialize
        """
        self.selected_preset = render_preset_selection
        self.current_scene_name=bpy.context.scene.name

        try:
            bpy.data.scenes[self.current_scene_name].world.name
        except AttributeError:
            self.current_scene_world = None                                                             # No world properties in scene
        else:
            self.current_scene_world=bpy.data.scenes[self.current_scene_name].world.name                # Set world properties name

    def execute(self):
        """
        Process actions
        """

        """Retrieve master presets and apply overrides"""
        self.AM_presets_common()
        if self.selected_preset == "Shot Finaling Preview":
            self.AM_presets_finaling_preview()
        elif self.selected_preset == "Shot Finaling Render":
            self.AM_presets_finaling_render()
        elif self.selected_preset == "Layout Review":
            self.AM_presets_layout_review()
        elif self.selected_preset == "Blender Default":
            self.AM_presets_blender()
        elif self.AM_blender_background == "Blender Background":
            print("Came in via Blender Background mode")
            self.AM_presets_common()
        else:
            print("Received: %s, unhandled condition" %self.selected_preset)

        """ Change Rendering Engine """
        self.global_renderengine()

        """ Viewport AO """
        self.global_ssao()

        """ Change Render Properties """
        self.global_render()
        self.blender_render()
        self.cycles_render()

        """ Change Render Layers Properties """
        self.global_render_layers()
        self.blender_render_layers()
        self.cycles_render_layers()

        """ Change Scene Properties """
        self.global_scene()
        self.blender_scene()
        self.cycles_scene()

        """ Change World Properties """
        if self.current_scene_world is not None:                                                        # World properties exist
            self.global_world()
            self.blender_world()
            self.cycles_world()

        """ Change Object Properties """
        self.global_object()
        self.blender_object()
        self.cycles_object()

        """ Change Texture Properties """
        self.global_texture()
        self.blender_texture()
        self.cycles_texture()

    def invoke (self, context, event):
        """
        Execute apply render settings
        """
        return {"FINISHED"}

    def AM_presets_common(self):
        """
        Master presets; eventually retrieved from Asset Manager (AM)
        """

        self.area_spaces_region_3d_view_perspective = 'CAMERA'                                          # ViewSpace3D Camera
        self.area_spaces_viewport_shade = 'SOLID'                                                       # ViewSpace3D Display Object/Shade Method, required for AO
        self.area_spaces_show_only_render = False                                                       # ViewSpace3D Display Show Only Render

        self.area_spaces_fx_settings_ssao_use_ssao = False                                              # ViewSpace3D AO
        self.area_spaces_fx_settings_ssao_factor = 1.0                                                  # ViewSpace3D AO Strength
        self.area_spaces_fx_settings_ssao_distance_max = 0.02                                           # ViewSpace3D AO Distance
        self.area_spaces_fx_settings_ssao_attenuation = 1.0                                             # ViewSpace3D AO Attenuation
        self.area_spaces_fx_settings_ssao_samples = 20                                                  # ViewSpace3D AO Samples

        self.cycles_aa_samples = 8                                                                      # Branched Path Tracing
        self.cycles_ao_samples = 1                                                                      # Branched Path Tracing
        self.cycles_caustics_reflective = False                                                         # Blender Preset: Direct Light
        self.cycles_caustics_refractive = False                                                         # Blender Preset: Direct Light
        self.cycles_diffuse_bounces = 0                                                                 # Blender Preset: Direct Light
        self.cycles_diffuse_samples =1                                                                  # Branched Path Tracing
        self.cycles_glossy_bounces = 1                                                                  # Blender Preset: Direct Light
        self.cycles_glossy_samples = 1                                                                  # Branched Path Tracing
        self.cycles_max_bounces = 8                                                                     # Blender Preset: Direct Light
        self.cycles_mesh_light_samples = 1                                                              # Branched Path Tracing
        self.cycles_min_bounces = 8                                                                     # Blender Preset: Direct Light
        self.cycles_preview_aa_samples = 8                                                              # Branched Path Tracing
        self.cycles_preview_samples = 10                                                                # Path Tracing
        self.cycles_progressive = 'BRANCHED_PATH'                                                       # Branched Path Tracing
        self.cycles_sample_all_lights_direct = True                                                     # Branched Path Tracing
        self.cycles_sample_all_lights_indirect = True                                                   # Branched Path Tracing
        self.cycles_sample_clamp_direct = 0.0
        self.cycles_sample_clamp_indirect = 0.0
        self.cycles_samples = 10                                                                        # Path Tracing
        self.cycles_sampling_pattern = 'SOBOL'
        self.cycles_seed = 0
        self.cycles_subsurface_samples = 1                                                              # Branched Path Tracing
        self.cycles_transmission_bounces = 2                                                            # Blender Preset: Direct Light
        self.cycles_transmission_samples = 1                                                            # Branched Path Tracing
        self.cycles_transparent_max_bounces = 8                                                         # Blender Preset: Direct Light
        self.cycles_transparent_min_bounces = 8                                                         # Blender Preset: Direct Light
        self.cycles_use_square_samples = True
        self.cycles_use_transparent_shadows = True                                                      # Blender Preset: Direct Light
        self.cycles_volume_bounces = 0                                                                  # Blender Preset: Direct Light
        self.cycles_volume_samples = 1                                                                  # Branched Path Tracing

        self.render_engine = 'BLENDER_RENDER'                                                           # Blender Default
        self.render_filepath = '/tmp\\'                                                                 # Blender Default
        self.render_image_settings_color_depth = '16'                                                   # EXR specific
        self.render_image_settings_color_mode = 'RGBA'                                                  # EXR specific
        self.render_image_settings_compression = 0                                                      # EXR specific
        self.render_image_settings_exr_codec = 'ZIP'                                                    # EXR specific
        self.render_image_settings_file_format = 'OPEN_EXR_MULTILAYER'                                  # Blender Default
        self.render_resolution_percentage = 100                                                         # Blender Default
        self.render_resolution_x = 1440                                                                 # Blender Default
        self.render_resolution_y = 810                                                                  # Blender Default

        self.render_simplify_shadow_samples = 16                                                        # Blender Render Simplify
        self.render_simplify_ao_sss = 1                                                                 # Blender Render Simplify
        self.render_use_simplify_triangulate = False                                                    # Blender Render Simplify

        self.render_simplify_subdivision = 6                                                            # Simplify
        self.render_simplify_child_particles = 1                                                        # Simplify
        self.render_simplify_subdivision_render = 6                                                     # Simplify
        self.render_simplify_child_particles_render = 0                                                 # Simplify

        self.render_use_compositing = True                                                              # Post Processing
        self.render_use_sequencer = True                                                                # Post Processing
        self.render_use_simplify = False                                                                # Simplify

        self.render_use_stamp = True                                                                    # Metadata
        self.render_stamp_font_size = 12                                                                # Metadata
        self.render_stamp_foreground = (0.8, 0.8, 0.8, 1.0)                                             # Metadata
        self.render_stamp_background = (0.0, 0.0, 0.0, 0.25)                                            # Metadata
        self.render_use_stamp_time = False                                                              # Metadata
        self.render_use_stamp_date = False                                                              # Metadata
        self.render_use_stamp_render_time = False                                                       # Metadata
        self.render_use_stamp_frame = True                                                              # Metadata
        self.render_use_stamp_scene = True                                                              # Metadata
        self.render_use_stamp_camera = False                                                            # Metadata
        self.render_use_stamp_lens = False                                                              # Metadata
        self.render_use_stamp_filename = False                                                          # Metadata
        self.render_use_stamp_marker = False                                                            # Metadata
        self.render_use_stamp_sequencer_strip = False                                                   # Metadata
        self.render_use_stamp_strip_meta = False                                                        # Metadata
        self.render_use_stamp_note = False                                                              # Metadata
        self.render_stamp_note_text = ''                                                                # Metadata

        self.world_horizon_color = (0.05,0.05,0.05)                                                     # Blender Default
        self.world_light_settings_ao_factor = 1                                                         # Blender Default
        self.world_light_settings_distance = 10                                                         # Blender Default
        self.world_light_settings_use_ambient_occlusion = False                                         # Blender Default

    def AM_presets_blender(self):
        """
        Master presets; eventually retrieved from Asset Manager (AM)
        """
        self.render_use_simplify = False                                                                # Blender Default

    def AM_presets_layout_review(self):
        """
        Override master presets
        """
        self.area_spaces_show_only_render = True                                                        # ViewSpace3D Display Show Only Render

        self.area_spaces_fx_settings_ssao_use_ssao = True                                               # ViewSpace3D AO
        self.area_spaces_fx_settings_ssao_factor = 1.5                                                  # ViewSpace3D AO Strength
        self.area_spaces_fx_settings_ssao_distance_max = 0.02                                           # ViewSpace3D AO Distance
        self.area_spaces_fx_settings_ssao_attenuation = 2.5                                             # ViewSpace3D AO Attenuation
        self.area_spaces_fx_settings_ssao_samples = 20                                                  # ViewSpace3D AO Samples

        self.cycles_use_square_samples = True                                                           # Post Processing

        self.render_engine = 'CYCLES'                                                                   # Rendering engine

        self.render_filepath = "T:\\Projects\\0043_Ozzy\\Media\\Layout\\"                               # Root location, sub-folder varies

        self.render_ffmpeg_format = 'QUICKTIME'                                                         # FFMPEG specific
        self.render_ffmpeg_codec = 'MPEG4'                                                              # FFMPEG specific
        self.render_ffmpeg_video_bitrate = 6000                                                         # FFMPEG specific
        self.render_ffmpeg_gopsize = 18                                                                 # FFMPEG specific
        self.render_ffmpeg_use_autosplit = False                                                        # FFMPEG specific
        self.render_ffmpeg_minrate = 0                                                                  # FFMPEG specific
        self.render_ffmpeg_maxrate = 9000                                                               # FFMPEG specific
        self.render_ffmpeg_buffersize = 1792                                                            # FFMPEG specific
        self.render_ffmpeg_muxrate = 10080000                                                           # FFMPEG specific
        self.render_ffmpeg_packetsize = 2048                                                            # FFMPEG specific
        self.render_ffmpeg_audio_codec = 'PCM'                                                          # FFMPEG specific
        self.render_ffmpeg_audio_bitrate = 192                                                          # FFMPEG specific
        self.render_ffmpeg_audio_volume = 1                                                             # FFMPEG specific
        self.render_image_settings_color_depth = '8'                                                    # FFMPEG specific, required
        self.render_image_settings_color_mode = 'RGB'                                                   # FFMPEG specific, required
        self.render_image_settings_file_format = 'FFMPEG'                                               # FFMPEG specific
        self.render_resolution_x = 1920
        self.render_resolution_y = 1080
        self.render_resolution_percentage = 50

        self.render_simplify_subdivision = 6
        self.render_simplify_child_particles = 0
        self.render_simplify_subdivision_render = 6
        self.render_simplify_child_particles_render = 0

        self.render_use_compositing = False                                                             # Post Processing
        self.render_use_simplify = False                                                                # Simplify
        self.render_use_sequencer = False                                                               # Post Processing

        self.render_use_stamp = True                                                                    # Metadata
        self.render_stamp_font_size = 17                                                                # Metadata
        self.render_stamp_foreground = (0.8, 0.8, 0.8, 1.0)                                             # Metadata
        self.render_stamp_background = (0.0, 0.0, 0.0, 1.0)                                             # Metadata
        self.render_use_stamp_time = False                                                              # Metadata
        self.render_use_stamp_date = False                                                              # Metadata
        self.render_use_stamp_render_time = False                                                       # Metadata
        self.render_use_stamp_frame = True                                                              # Metadata
        self.render_use_stamp_scene = True                                                              # Metadata
        self.render_use_stamp_camera = False                                                            # Metadata
        self.render_use_stamp_lens = True                                                               # Metadata
        self.render_use_stamp_filename = False                                                          # Metadata
        self.render_use_stamp_marker = False                                                            # Metadata
        self.render_use_stamp_sequencer_strip = False                                                   # Metadata
        self.render_use_stamp_strip_meta = False                                                        # Metadata
        self.render_use_stamp_note = False                                                              # Metadata
        self.render_stamp_note_text = ''                                                                # Metadata

        self.world_horizon_color = (0, 0, 0)
        self.world_light_settings_use_ambient_occlusion = True
        self.world_light_settings_ao_factor = 1
        self.world_light_settings_distance = 2.5

    def AM_presets_finaling_preview(self):
        """
        Override master presets
        """
        self.area_spaces_show_only_render = True                                                        # ViewSpace3D Display Show Only Render

        self.area_spaces_fx_settings_ssao_use_ssao = True                                               # ViewSpace3D AO
        self.area_spaces_fx_settings_ssao_factor = 1.5                                                  # ViewSpace3D AO Strength
        self.area_spaces_fx_settings_ssao_distance_max = 0.02                                           # ViewSpace3D AO Distance
        self.area_spaces_fx_settings_ssao_attenuation = 2.5                                             # ViewSpace3D AO Attenuation
        self.area_spaces_fx_settings_ssao_samples = 20                                                  # ViewSpace3D AO Samples

        self.cycles_use_square_samples = True                                                           # Post Processing

        self.render_engine = 'CYCLES'                                                                   # Rendering engine

        self.render_filepath = 'USE_FILENAME'                                                           # Generate from file path/name

        self.render_ffmpeg_format = 'QUICKTIME'                                                         # FFMPEG specific
        self.render_ffmpeg_codec = 'MPEG4'                                                              # FFMPEG specific
        self.render_ffmpeg_video_bitrate = 6000                                                         # FFMPEG specific
        self.render_ffmpeg_gopsize = 18                                                                 # FFMPEG specific
        self.render_ffmpeg_use_autosplit = False                                                        # FFMPEG specific
        self.render_ffmpeg_minrate = 0                                                                  # FFMPEG specific
        self.render_ffmpeg_maxrate = 9000                                                               # FFMPEG specific
        self.render_ffmpeg_buffersize = 1792                                                            # FFMPEG specific
        self.render_ffmpeg_muxrate = 10080000                                                           # FFMPEG specific
        self.render_ffmpeg_packetsize = 2048                                                            # FFMPEG specific
        self.render_ffmpeg_audio_codec = 'PCM'                                                          # FFMPEG specific
        self.render_ffmpeg_audio_bitrate = 192                                                          # FFMPEG specific
        self.render_ffmpeg_audio_volume = 1                                                             # FFMPEG specific
        self.render_image_settings_color_depth = '8'                                                    # FFMPEG specific, required
        self.render_image_settings_color_mode = 'RGB'                                                   # FFMPEG specific, required
        self.render_image_settings_file_format = 'FFMPEG'                                               # FFMPEG specific
        self.render_resolution_x = 1920
        self.render_resolution_y = 1080
        self.render_resolution_percentage = 50

        self.render_simplify_subdivision = 6
        self.render_simplify_child_particles = 0
        self.render_simplify_subdivision_render = 6
        self.render_simplify_child_particles_render = 1

        self.render_use_compositing = False                                                             # Post Processing
        self.render_use_simplify = False                                                                # Simplify
        self.render_use_sequencer = False                                                               # Post Processing
        self.render_use_stamp = True                                                                    # Metadata

        self.world_horizon_color = (0, 0, 0)
        self.world_light_settings_use_ambient_occlusion = True
        self.world_light_settings_ao_factor = 1
        self.world_light_settings_distance = 2.5

    def AM_presets_finaling_render(self):
        """
        Override master presets
        """
        self.area_spaces_show_only_render = True                                                        # ViewSpace3D Display Show Only Render

        self.area_spaces_fx_settings_ssao_use_ssao = True                                               # ViewSpace3D AO
        self.area_spaces_fx_settings_ssao_factor = 1.5                                                  # ViewSpace3D AO Strength
        self.area_spaces_fx_settings_ssao_distance_max = 0.02                                           # ViewSpace3D AO Distance
        self.area_spaces_fx_settings_ssao_attenuation = 2.5                                             # ViewSpace3D AO Attenuation
        self.area_spaces_fx_settings_ssao_samples = 20                                                  # ViewSpace3D AO Samples

        self.cycles_use_square_samples = True                                                           # Post Processing

        self.render_engine = 'CYCLES'                                                                   # Rendering engine

        self.render_filepath = 'USE_FILENAME'                                                           # Generate from file path/name

        self.render_resolution_x = 1920
        self.render_resolution_y = 1080
        self.render_resolution_percentage = 50
        self.render_image_settings_file_format = 'PNG'                                                  # PNG specific
        self.render_image_settings_compression = 0                                                      # PNG specific
        self.render_image_settings_color_depth = '16'                                                   # PNG specific
        self.render_image_settings_color_mode = 'RGBA'                                                  # PNG specific

        self.render_simplify_subdivision = 6
        self.render_simplify_child_particles = 0
        self.render_simplify_subdivision_render = 6
        self.render_simplify_child_particles_render = 1

        self.render_use_compositing = False                                                             # Post Processing
        self.render_use_simplify = True                                                                 # Simplify
        self.render_use_sequencer = False                                                               # Post Processing
        self.render_use_stamp = False                                                                   # Metadata

        self.world_horizon_color = (0, 0, 0)
        self.world_light_settings_use_ambient_occlusion = True
        self.world_light_settings_ao_factor = 1
        self.world_light_settings_distance = 2.5

    def global_ssao(self):
        """
        Screen Space Ambient Occlusion In Viewport
        """
        current_scene_area = bpy.context.screen.areas

        """ SpaceView 3D """
        for area in current_scene_area:
            if area.type == 'VIEW_3D':
                """ Viewport Camera """
                area.spaces[0].region_3d.view_perspective = self.area_spaces_region_3d_view_perspective

                """ Display Object/Shade Method """
                area.spaces[0].viewport_shade = self.area_spaces_viewport_shade

                """ Display """
                area.spaces[0].show_only_render = self.area_spaces_show_only_render

                """ Ambient Occlusion """
                area.spaces[0].fx_settings.use_ssao = self.area_spaces_fx_settings_ssao_factor
                area.spaces[0].fx_settings.ssao.factor = self.area_spaces_fx_settings_ssao_distance_max
                area.spaces[0].fx_settings.ssao.distance_max = self.area_spaces_fx_settings_ssao_distance_max
                area.spaces[0].fx_settings.ssao.attenuation = self.area_spaces_fx_settings_ssao_attenuation
                area.spaces[0].fx_settings.ssao.samples = self.area_spaces_fx_settings_ssao_samples

    def global_renderengine(self):
        """
        Global Render Engine (Blender/Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.RenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render

        """ Set Blender render engine """
        render.engine = self.render_engine

    def global_render(self):
        """
        Global Render Setting (Blender/Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.RenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render

        """ Render """
        render.display_mode = 'AREA'

        """ Dimensions, contains preset dropdown: bpy.ops.render.preset_add() """
        render.resolution_x = self.render_resolution_x
        render.resolution_y = self.render_resolution_y
        render.resolution_percentage = self.render_resolution_percentage
        render.pixel_aspect_x = 1
        render.pixel_aspect_y = 1
        render.frame_map_old = 100
        render.frame_map_new = 100
        render.use_border = False

        """ Metadata """
        render.use_stamp = self.render_use_stamp
        render.stamp_font_size = self.render_stamp_font_size
        render.stamp_foreground = self.render_stamp_foreground
        render.stamp_background = self.render_stamp_background
        render.use_stamp_time = self.render_use_stamp_time
        render.use_stamp_date = self.render_use_stamp_date
        render.use_stamp_render_time = self.render_use_stamp_render_time
        render.use_stamp_frame = self.render_use_stamp_frame
        render.use_stamp_scene = self.render_use_stamp_scene
        render.use_stamp_camera = self.render_use_stamp_camera
        render.use_stamp_lens = self.render_use_stamp_lens
        render.use_stamp_filename = self.render_use_stamp_filename
        render.use_stamp_marker = self.render_use_stamp_marker
        render.use_stamp_sequencer_strip = self.render_use_stamp_sequencer_strip
        render.use_stamp_strip_meta = self.render_use_stamp_strip_meta
        render.use_stamp_note = self.render_use_stamp_note
        render.stamp_note_text = self.render_stamp_note_text

        """ Output """
        if self.render_filepath == 'USE_FILENAME':                                                      # Generate from file path/name
            self.filepath = bpy.path.abspath('//')
            self.current_filename = bpy.path.display_name_from_filepath(bpy.data.filepath)
            self.new_suffix = ""

            """ Set extension based on render file format """
            if self.render_image_settings_file_format == 'FFMPEG':                                      # MOV: Render file format extension
                self.new_suffix = "mov"
            if self.render_image_settings_file_format == 'EXR':                                         # EXR: Render file format extension
                self.new_suffix = "exr"
            if self.render_image_settings_file_format == 'PNG':                                         # PNG: Render file format extension
                self.new_suffix = "png"

            if len(self.filepath) > 0 and len(self.current_filename) > 0 and len(self.new_suffix) > 0:  # Check for empty result
                self.render_filepath = ("%s%s.%s" % (self.filepath, 
                                                     self.current_filename, 
                                                     self.new_suffix))
            else: 
                self.render_filepath = '/tmp\\'                                                         # Blender Default
        render.filepath = self.render_filepath
        render.use_overwrite = True
        render.use_placeholder = False
        render.use_file_extension = True

        render.use_render_cache = False
        render.image_settings.file_format = self.render_image_settings_file_format
        render.image_settings.color_depth = self.render_image_settings_color_depth
        render.image_settings.color_mode = self.render_image_settings_color_mode
        if self.render_image_settings_file_format == 'EXR':                                             # .EXR specific
            render.image_settings.exr_codec = self.render_image_settings_exr_codec
        if self.render_image_settings_file_format == 'PNG':                                             # .PNG specific
            render.image_settings.compression = self.render_image_settings_compression
        if self.render_image_settings_file_format == 'FFMPEG':                                          # .FFMPEG specific
            render.ffmpeg.format = self.render_ffmpeg_format
            render.ffmpeg.codec = self.render_ffmpeg_codec
            render.ffmpeg.video_bitrate = self.render_ffmpeg_video_bitrate
            render.ffmpeg.gopsize = self.render_ffmpeg_gopsize
            render.ffmpeg.use_autosplit = self.render_ffmpeg_use_autosplit
            render.ffmpeg.minrate =self.render_ffmpeg_minrate
            render.ffmpeg.maxrate = self.render_ffmpeg_maxrate
            render.ffmpeg.buffersize = self.render_ffmpeg_buffersize
            render.ffmpeg.muxrate = self.render_ffmpeg_muxrate
            render.ffmpeg.packetsize = self.render_ffmpeg_packetsize
            render.ffmpeg.audio_codec = self.render_ffmpeg_audio_codec
            render.ffmpeg.audio_bitrate = self.render_ffmpeg_audio_bitrate
            render.ffmpeg.audio_volume = self.render_ffmpeg_audio_volume

        """
        Performance
        """
        render.threads_mode = 'AUTO'
        render.use_save_buffers = False
        render.use_free_image_textures = False
        render.use_free_unused_nodes = False
        render.raytrace_method = 'AUTO'
        render.use_local_coords = False
        render.tile_x = 64
        render.tile_y = 64

        """ Post Processing """
        render.use_compositing = self.render_use_compositing
        render.use_sequencer = self.render_use_sequencer
        render.dither_intensity = 0.0

        """ Freestyle """
        render.use_freestyle = False
        render.line_thickness_mode = 'ABSOLUTE'
        render.line_thickness = 1.0

    def blender_render(self):
        """
        Render Setting (Blender)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.RenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render

        """ Performance """
        render.use_instances = True
        render.preview_start_resolution = 64

        """ Post Processing """
        render.use_fields = False
        render.use_edge_enhance = False
        render.edge_color = (0.0, 0.0, 0.0)

        """ Bake """
        render.bake_type = 'FULL'
        render.use_bake_to_vertex_color = False
        render.use_bake_clear = True
        render.bake_margin = 16
        render.bake_quad_split = 'AUTO'
        render.use_bake_selected_to_active = False

        """ Shading """
        render.use_textures = True
        render.use_shadows = True
        render.use_sss = True
        render.use_envmaps = True
        render.use_raytrace = True
        render.alpha_mode = 'SKY'

        """ Sampled Motion Blur """
        render.use_motion_blur = False
        render.motion_blur_samples = 1
        render.motion_blur_shutter = 0.5

        """ Anti-Aliasing """
        render.use_antialiasing = True
        render.antialiasing_samples = '8'
        render.pixel_filter_type = 'MITCHELL'
        render.use_full_sample = False
        render.filter_size = 1.0

    def cycles_render(self):
        """
        Render Setting (Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.CyclesRenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render
        cycles = bpy.data.scenes[self.current_scene_name].cycles

        """ Dimensions, contains preset dropdown: bpy.ops.render.preset_add() """
        cycles.feature_set = 'SUPPORTED'

        """ Performance """
        render.use_persistent_data = False
        cycles.preview_start_resolution = 64
        cycles.debug_bvh_type = 'DYNAMIC_BVH'
        cycles.tile_order = 'CENTER'
        cycles.use_progressive_refine = False
        cycles.use_cache = False
        cycles.debug_use_spatial_splits = False

        """ Bake """
        cycles.bake_type = 'COMBINED'
        render.bake.margin = 16
        render.bake.use_clear = True
        render.bake.use_selected_to_active = False
        render.bake.use_clear = False

        """ Sampling, contains preset dropdown: bpy.ops.render.cycles_sampling_preset_add() """
        cycles.progressive = self.cycles_progressive
        cycles.use_square_samples = self.cycles_use_square_samples
        cycles.seed = self.cycles_seed
        cycles.sample_clamp_direct = self.cycles_sample_clamp_direct
        cycles.sample_clamp_indirect = self.cycles_sample_clamp_indirect
        cycles.sampling_pattern = self.cycles_sampling_pattern

        cycles.samples = self.cycles_samples                                                            # Path Tracing
        cycles.preview_samples = self.cycles_preview_samples                                            # Path Tracing
        
        cycles.aa_samples = self.cycles_aa_samples                                                      # Branched Path Tracing
        cycles.preview_aa_samples = self.cycles_preview_aa_samples                                      # Branched Path Tracing
        cycles.diffuse_samples =self.cycles_diffuse_samples                                             # Branched Path Tracing
        cycles.glossy_samples = self.cycles_glossy_samples                                              # Branched Path Tracing
        cycles.transmission_samples = self.cycles_transmission_samples                                  # Branched Path Tracing
        cycles.ao_samples = self.cycles_ao_samples                                                      # Branched Path Tracing
        cycles.mesh_light_samples = self.cycles_mesh_light_samples                                      # Branched Path Tracing
        cycles.subsurface_samples = self.cycles_subsurface_samples                                      # Branched Path Tracing
        cycles.volume_samples = self.cycles_volume_samples                                              # Branched Path Tracing
        cycles.sample_all_lights_direct = self.cycles_sample_all_lights_direct                          # Branched Path Tracing
        cycles.sample_all_lights_indirect = self.cycles_sample_all_lights_indirect                      # Branched Path Tracing

        """ Volume Sampling """
        cycles.volume_step_size = 0.1
        cycles.volume_max_steps = 1024

        """ Motion Blur """
        render.use_motion_blur = False
        render.motion_blur_shutter = 0.5

        """ Light Paths """
        cycles.transparent_max_bounces = self.cycles_transparent_max_bounces
        cycles.transparent_min_bounces = self.cycles_transparent_min_bounces
        cycles.max_bounces = self.cycles_max_bounces
        cycles.min_bounces = self.cycles_min_bounces
        cycles.diffuse_bounces = self.cycles_diffuse_bounces
        cycles.glossy_bounces = self.cycles_glossy_bounces
        cycles.transmission_bounces = self.cycles_transmission_bounces
        cycles.volume_bounces = self.cycles_volume_bounces
        cycles.use_transparent_shadows = self.cycles_use_transparent_shadows
        cycles.caustics_reflective = self.cycles_caustics_reflective
        cycles.caustics_refractive = self.cycles_caustics_refractive
        cycles.blur_glossy = 0

        """ Film """
        cycles.film_exposure = 1
        cycles.filter_type = 'GAUSSIAN'
        cycles.filter_width = 1.5
        cycles.film_transparent = False

    def global_render_layers(self):
        """
        Global Render Layers Setting (Blender/Cycles)
        """
        pass

    def blender_render_layers(self):
        """
        Render Layers Setting (Blender)
        """
        pass

    def cycles_render_layers(self):
        """
        Render Layers Setting (Cycles)
        """
        pass

    def global_scene(self):
        """
        Global Scene Setting (Blender/Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.RenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render

        """ Simplify """
        render.use_simplify = self.render_use_simplify
        render.simplify_subdivision = self.render_simplify_subdivision
        render.simplify_child_particles = self.render_simplify_child_particles
        render.simplify_subdivision_render = self.render_simplify_subdivision_render
        render.simplify_child_particles_render = self.render_simplify_child_particles_render

    def blender_scene(self):
        """
        Scene Setting (Blender)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.RenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render

        """ Simplify """
        render.simplify_shadow_samples = self.render_simplify_shadow_samples
        render.simplify_ao_sss = self.render_simplify_ao_sss
        render.use_simplify_triangulate = self.render_use_simplify_triangulate

    def cycles_scene(self):
        """
        Scene Setting (Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.RenderSettings.html
        """
        render = bpy.data.scenes[self.current_scene_name].render

        """ Simplify """
        pass

    def global_world(self):
        """
        Global World Setting (Blender/Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.WorldLighting.html
        """
        world = bpy.data.worlds[self.current_scene_world]

        """ World """
        world.horizon_color = self.world_horizon_color

        """ Ambient Occlusion/Gather """
        world.light_settings.use_ambient_occlusion = self.world_light_settings_use_ambient_occlusion
        world.light_settings.ao_factor = self.world_light_settings_ao_factor
        world.light_settings.distance = self.world_light_settings_distance

    def blender_world(self):
        """
        Global World Setting (Blender)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.WorldLighting.html
        
        Contains preset dropdown: bpy.ops.world.new()
        """
        world = bpy.data.worlds[self.current_scene_world]

        """ World """
        world.use_sky_paper = False
        world.use_sky_blend = False
        world.use_sky_real = False
        world.zenith_color = (0.1,0.1,0.1)
        world.ambient_color = (0,0,0)
        world.exposure = 0
        world.color_range = 1

        """ Ambient Occlusion """
        world.light_settings.ao_blend_type = 'ADD'
        
        """ Environment Lighting """
        world.light_settings.use_environment_light = False

        """ Indirect Lighting """
        world.light_settings.use_indirect_light = False

        """ Gather """
        world.light_settings.gather_method = 'RAYTRACE'
        world.light_settings.sample_method = 'CONSTANT_QMC'
        world.light_settings.samples = 20

        """ Falloff """
        world.light_settings.use_falloff = True
        world.light_settings.falloff_strength = 2

        """ Mist """
        world.mist_settings.use_mist = False

    def cycles_world(self):
        """
        Global World Setting (Cycles)
        https://www.blender.org/api/blender_python_api_2_75a_release/bpy.types.CyclesWorldSettings.html
        """
        world = bpy.data.worlds[self.current_scene_world]

        """ Ray Visibility """
        world.cycles_visibility.camera = True
        world.cycles_visibility.diffuse = True
        world.cycles_visibility.glossy = True
        world.cycles_visibility.transmission = True
        world.cycles_visibility.scatter = True

        """ Multiple Importance """
        world.cycles.sample_as_light = False

        """ Volume """
        world.cycles.volume_sampling = 'EQUIANGULAR'
        world.cycles.volume_interpolation = 'LINEAR'
        world.cycles.homogeneous_volume = False

    def global_object(self):
        """
        Global Object Setting (Blender/Cycles)
        """
        pass

    def blender_object(self):
        """
        Render Object (Blender)
        """
        pass

    def cycles_object(self):
        """
        Render Object (Cycles)
        """
        pass

    def global_texture(self):
        """
        Global Texture Setting (Blender/Cycles)
        """
        pass

    def blender_texture(self):
        """
        Render Texture (Blender)
        """
        pass

    def cycles_texture(self):
        """
        Render Texture (Cycles)
        """
        pass


class RenderFinalingPanel(bpy.types.Panel):
    """
    Create master panel
    """
    bl_label= "Render Finaling"
    bl_idname = "object.renderfinalingpanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "TA - Finaling"

    @classmethod
    def poll(cls, context):
        return (True) 

    def draw(self, context):
        layout = self.layout
        col = layout.column()                                                                           # Initial column

        """ Render Presets """
        row = col.row()                                                                                 # Create first row in column
        row.label(text = "Shot Finaling Preset")

        row = col.row(align = True)                                                                     # New row with two elements
        split = row.split(percentage = 1, align = True)
        split.prop_menu_enum(context.scene, "renderpresets", text = context.scene.renderpresets, icon='NONE')
        split = row.split(percentage = 1, align = True)
        split.operator("render.apply_render_settings_button", text = "Apply Preset", icon = 'RENDERLAYERS')

        """ Use depth of field on viewport using the values from active camera """
        col.separator()                                                                                 # Add spacer
        col.separator()                                                                                 # Add spacer
        row = col.row()
        row.label(text = "3D Viewport", icon = 'SPLITSCREEN')

        box = col.box()
        row = box.row(align = True)                                                                     # UI text
        row.label(text = "Active Camera Depth Of Field")
        row = box.row(align = True)                                                                     # New row with two elements
        row.prop(context.scene, "usedof", text = context.scene.usedof, expand = True)

        """ Display only objects which will be rendered """
        row = box.row(align = True)                                                                     # UI text
        row.label(text = "Renderable Objects Display")
        row = box.row(align = True)                                                                     # New row with two elements
        row.prop(context.scene, "useonlyrender", text = context.scene.useonlyrender, expand = True)

        """ Enable screen space ambient occlusion of field on viewport """
        row = box.row(align = True)                                                                     # UI text
        row.label(text = "Screen Space Ambient Occlusion")
        row = box.row(align = True)                                                                     # New row with two elements
        row.prop(context.scene, "usessao", text = context.scene.usessao, expand = True)

        """ Enable simplification of scene for quicker preview renders """
        col.separator()                                                                                 # Add spacer
        col.separator()                                                                                 # Add spacer
        row = col.row()
        row.label(text = "Scene Properties", icon = 'SCENE_DATA')

        box = col.box()
        row = box.row(align = True)                                                                     # UI text
        row.label(text = "Quick Preview Render")
        row = box.row(align = True)                                                                     # New row with two elements
        row.prop(context.scene, "usesimplify", text = context.scene.usesimplify, expand = True)

        """ Directory/name to save animation """
        col.separator()                                                                                 # Add spacer
        col.separator()                                                                                 # Add spacer
        row = col.row()
        row.label(text = "Render Properties", icon = 'SCENE')

        box = col.box()
        row = box.row(align = True)                                                                     # UI text
        row.label(text = "Output Directory/Name")
        row = box.row(align = True)  
        row.prop(bpy.context.scene.render, "filepath", text="")


class SaveIncrementalFile(object):
    """
    Save incremental version of file
    """

    def __init__(self):
        """
        Initialize
        """
        self.filepath = bpy.path.abspath('//')
        self.current_filename = bpy.path.display_name_from_filepath(bpy.data.filepath)
        self.current_filename = current_filename.rsplit('.', 1)

        self.does_file_exist = None
        self.file_exists = True
        self.next_numeric = 0
        self.new_filename = ""
        self.new_suffix = ""
        self.non_numerics = ""
        self.numerics = ""

    def execute(self):
        """
        Execute
        """
        # Check if current filename is versioned (ex: .0000).  If not, use Blender
        # numbering convention
        if len(self.current_filename) < 2:
            self.current_filename.append('0000')

        # Filter the version information for non-numerics.  
        chars = set('0123456789')
        for strval in self.current_filename[1]:
            if strval in chars:
                self.numerics += strval
            else:
                self.non_numerics += strval

        # If non-numerics value is greater than one (ex: .v0000), give up and create 
        # the Blender numbering convention
        if len(self.non_numerics) > 1:
            self.current_filename[0] = ("%s.%s" % (self.current_filename[0], self.current_filename[1]))
            self.current_filename[1] = '0000'
            self.numerics = self.current_filename[1]
            self.non_numerics = ""

        # Set the version number starting value equal to the current file version (ex: 0050)
        # and increment to the next potential version number.  Assemble the file path and 
        # check to see if a file with the incremented version exists.  If a file with the
        # new name already exists, rinse-and-repeat.
        self.next_numeric = int(self.numerics)
        while (self.file_exists == True):
            self.next_numeric += 1
            self.new_suffix = str(self.next_numeric).zfill(len(self.numerics))
            self.new_filename = ("%s%s.%s%s.blend" % (self.filepath, self.current_filename[0], self.non_numerics, self.new_suffix))
            try:
                self.does_file_exist = open(self.new_filename,'r')
            except:
                bpy.ops.wm.save_as_mainfile(filepath=self.new_filename)
                self.file_exists = False

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    """
    https://www.blender.org/api/blender_python_api_2_75a_release/bpy.app.html
    """
    # print("\n\n--------------------------------------------------\n\n")

    if bpy.app.background:
        # http://blender.stackexchange.com/questions/39641/how-to-enable-an-addon-on-startup-via-script
        # 
        # Blender launched in background mode; run relevant functions
        # UI panel classes/functions might have to be skipped or coded to accept passed parameters from here
        # Logic to iterate through all scenes in .blend file may be required

        print("Blender running in background mode: %s" %(bpy.app.background))
        register()

        aps = ApplyRenderSettings("Blender Background")
        aps.execute()

        sif = SaveIncrementalFile()
        sif.execute()

    else:
        # Blender launched in foreground mode; wait for user interaction
        register()
