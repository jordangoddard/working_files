"""
Tangent Animation blender startup script.  Sets parameters for the Studio
"""
__author__ = 'Jeff.Bell'

import bpy
from core.log import Log

# Initialize the log
log = Log()
log.info("Starting Tangent Animation pipeline configuration")

log.info("Setting some UI defaults")
bpy.data.use_autopack = False  # Turn off auto-packing of images, etc
bpy.context.user_preferences.filepaths.use_relative_paths = False  # Don't use relative paths
bpy.context.user_preferences.system.use_scripts_auto_execute = True  # Auto-execute python scripts
bpy.context.user_preferences.system.use_scripts_auto_execute = True  # Auto-execute python scripts
bpy.context.user_preferences.system.audio_sample_rate = "RATE_48000"  # Default audio sampling rate

# Toggle system console off to prevent user from accidentally closing Blender
log.info("Toggling the system console")
bpy.ops.wm.console_toggle()

# Auto load some addons at startup
addon_startup_list = [
    #"amaranth",
    "animation_motion_trail",
    "bone_selection_groups",
    "dynamic_parent",
    "mesh_summary_102",
    "meshlint",
    "mirror_vertex_groups",
    "multi_rename_dom",
    #"space_view3d_Meta-Tools_0-3_tab",
    "mass_align",
    "modifier_tool",
    "subdiv_tool",
    "wireframe_toggle",
    "DeadlineBlenderClient",
    "custom_file_tab", #turns off remap relative. *Addon's cannot be unregistered. Remove the file to permanently remove the addon
    "cubesurfer",
]

import addon_utils
for addon in addon_startup_list:
    try:
        addon_utils.enable(addon, default_set=True)
    except:
        log.warning("Could not enable addon %s - skipped" % addon)
    else:
        log.info("Loaded addon %s" % addon)


# Setup defaults - base this on the show.  TODO: un-hardcode this

# Basic render settings
bpy.context.scene.render.fps = 24
bpy.context.scene.render.resolution_x = 1440
bpy.context.scene.render.resolution_y = 810
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.pixel_aspect_x = 1.0
bpy.context.scene.render.pixel_aspect_y = 1.0

# Store the current render engine - we need to restore this after
render_engine = bpy.context.scene.render.engine
bpy.context.scene.render.engine = "CYCLES"

# Default scene audio
bpy.context.scene.render.ffmpeg.audio_mixrate = 48000

# Image output settings
bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
bpy.context.scene.render.image_settings.color_depth = '32'
bpy.context.scene.render.image_settings.exr_codec = 'ZIP'

# Cycles sampling and light path settings
# TODO: store default from blender, and only change if
# the setting matches the default - if it's NOT default
# then the user or some other script has changed the value
"""
bpy.context.scene.cycles.use_square_samples = True
bpy.context.scene.cycles.progressive = 'BRANCHED_PATH'
bpy.context.scene.cycles.aa_samples = 6
bpy.context.scene.cycles.preview_aa_samples = 4
bpy.context.scene.cycles.glossy_samples = 1
bpy.context.scene.cycles.glossy_samples = 2
bpy.context.scene.cycles.ao_samples = 4
bpy.context.scene.cycles.mesh_light_samples = 1
bpy.context.scene.cycles.max_bounces = 4
bpy.context.scene.cycles.min_bounces = 4
bpy.context.scene.cycles.diffuse_bounces = 0
bpy.context.scene.cycles.glossy_bounces = 1
bpy.context.scene.cycles.transmission_bounces = 4
bpy.context.scene.cycles.volume_bounces = 0
bpy.context.scene.cycles.blur_glossy = 3
bpy.context.scene.cycles.max_bounces = 4
bpy.context.scene.cycles.sample_clamp_direct = 3
bpy.context.scene.cycles.sample_clamp_indirect = 3
bpy.context.scene.cycles.aa_samples = 6
"""

# Restore the render engine
bpy.context.scene.render.engine = render_engine

# Setup various properties
log.info("Setting up Snapshot Properties")
class SnapshotDBInfo(bpy.types.PropertyGroup):
    """ Defines properties for a Snapshot asset - enables
    tools to determine what file is currently open.
    """
    show_code = bpy.props.StringProperty(name="Show Code")
    type_primary = bpy.props.StringProperty(name="Type Primary")
    type_secondary = bpy.props.StringProperty(name="Type Secondary")
    code = bpy.props.StringProperty(name="Code")

bpy.utils.register_class(SnapshotDBInfo)

# NOTE: we may need to add additional types to this list in order to properly catalog items in the blend files
bpy.types.WindowManager.snapshot_db_info = bpy.props.PointerProperty(name="Snapshot DB Info", type=SnapshotDBInfo)
bpy.types.Object.snapshot_db_info = bpy.props.PointerProperty(name="Snapshot DB Info", type=SnapshotDBInfo)
bpy.types.Group.snapshot_db_info = bpy.props.PointerProperty(name="Snapshot DB Info", type=SnapshotDBInfo)
bpy.types.Scene.snapshot_db_info = bpy.props.PointerProperty(name="Snapshot DB Info", type=SnapshotDBInfo)

log.info("Completed Tangent Animation pipeline configuration")




