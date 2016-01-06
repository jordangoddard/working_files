

#DJANGO APP: users
def decode_users(values):
    from ..users import User
    url = values['url']
    pk = values['pk']
    is_superuser = values['is_superuser']
    username = values['username']
    email = values['email']
    is_staff = values['is_staff']
    return User(
            url,
            pk,
            is_superuser,
            username,
            email,
            is_staff,
        )

#DJANGO APP: shows
def decode_preferences(values):
    from ..shows import Preferences
    url = values['url']
    pk = values['pk']
    res_render_x = values['res_render_x']
    res_render_y = values['res_render_y']
    res_playblast_x = values['res_playblast_x']
    res_playblast_y = values['res_playblast_y']
    timebase = values['timebase']
    codec = values['codec']
    p_drive = values['p_drive']
    p_drive_linux = values['p_drive_linux']
    p_project = values['p_project']
    p_render = values['p_render']
    p_review = values['p_review']
    p_comp = values['p_comp']
    p_media = values['p_media']
    p_publish = values['p_publish']
    p_sandbox = values['p_sandbox']
    path_drive = values['path_drive']
    path_project = values['path_project']
    path_sandbox = values['path_sandbox']
    path_render = values['path_render']
    path_media = values['path_media']
    path_publish = values['path_publish']
    path_review = values['path_review']
    show = values['show']
    return Preferences(
            url,
            pk,
            res_render_x,
            res_render_y,
            res_playblast_x,
            res_playblast_y,
            timebase,
            codec,
            p_drive,
            p_drive_linux,
            p_project,
            p_render,
            p_review,
            p_comp,
            p_media,
            p_publish,
            p_sandbox,
            path_drive,
            path_project,
            path_sandbox,
            path_render,
            path_media,
            path_publish,
            path_review,
            show,
        )

def decode_show(values):
    from ..shows import Show
    url = values['url']
    pk = values['pk']
    code = values['code']
    name = values['name']
    created = values['created']
    modified = values['modified']
    company = values['company']
    preferences = values['preferences']
    assets = values['assets']
    return Show(
            url,
            pk,
            code,
            name,
            created,
            modified,
            company,
            preferences,
            assets,
        )

#DJANGO APP: assets
def decode_assets(values):
    from ..assets import Asset
    url = values['url']
    pk = values['pk']
    type_primary = values['type_primary']
    type_secondary = values['type_secondary']
    type_tertiary = None
    try:
        type_tertiary = values['type_tertiary']
    except:
        pass
    code = values['code']
    description = None
    try:
        description = values['description']
    except:
        pass
    comment = None
    try:
        comment = values['comment']
    except:
        pass
    start_frame = values['start_frame']
    end_frame = values['end_frame']
    data = None
    try:
        data = values['data']
    except:
        pass
    stats_version = values['stats_version']
    stats_verts = values['stats_verts']
    stats_faces = values['stats_faces']
    stats_tris = values['stats_tris']
    stats_objects = values['stats_objects']
    stats_lamps = values['stats_lamps']
    stats_memory = values['stats_memory']
    created = values['created']
    modified = values['modified']
    current_version = values['current_version']
    file = values['file']
    filename = values['filename']
    path = values['path']
    images = values['images']
    parents = values['parents']
    layers = values['layers']
    children = values['children']
    movies = values['movies']
    renders = values['renders']
    show = values['show']
    versions = values['versions']
    groups = values['groups']
    return Asset(
            url,
            pk,
            type_primary,
            type_secondary,
            type_tertiary,
            code,
            description,
            comment,
            start_frame,
            end_frame,
            data,
            stats_version,
            stats_verts,
            stats_faces,
            stats_tris,
            stats_objects,
            stats_lamps,
            stats_memory,
            created,
            modified,
            current_version,
            file,
            filename,
            path,
            images,
            parents,
            layers,
            children,
            movies,
            renders,
            show,
            versions,
            groups,
        )

#DJANGO APP: versions
def decode_versions(values):
    from ..versions import AssetVersion
    url = values['url']
    pk = values['pk']
    version = values['version']
    comment = values['comment']
    created = values['created']
    file = values['file']
    version_string = values['version_string']
    filename = values['filename']
    path = values['path']
    asset = values['asset']
    return AssetVersion(
            url,
            pk,
            version,
            comment,
            created,
            file,
            version_string,
            filename,
            path,
            asset,
        )

#DJANGO APP: movies
def decode_movies(values):
    from ..movies import Movie
    url = values['url']
    pk = values['pk']
    name = values['name']
    filepath = values['filepath']
    created = values['created']
    modified = values['modified']
    asset = values['asset']
    return Movie(
            url,
            pk,
            name,
            filepath,
            created,
            modified,
            asset,
        )

#DJANGO APP: images
def decode_images(values):
    from ..images import Image
    url = values['url']
    pk = values['pk']
    name = values['name']
    filepath = values['filepath']
    created = values['created']
    modified = values['modified']
    assets = values['assets']
    return Image(
            url,
            pk,
            name,
            filepath,
            created,
            modified,
            assets,
        )

#DJANGO APP: companies
def decode_companies(values):
    from ..companies import Company
    url = values['url']
    pk = values['pk']
    name = values['name']
    project_root = values['project_root']
    source_root = values['source_root']
    render_root = values['render_root']
    created = values['created']
    modified = values['modified']
    shows = values['shows']
    return Company(
            url,
            pk,
            name,
            project_root,
            source_root,
            render_root,
            created,
            modified,
            shows,
        )

#DJANGO APP: renders
def decode_layer(values):
    from ..renders import Layer
    url = values['url']
    pk = values['pk']
    name = values['name']
    layer_type = None
    try:
        layer_type = values['layer_type']
    except:
        pass
    start = None
    try:
        start = values['start']
    except:
        pass
    end = None
    try:
        end = values['end']
    except:
        pass
    created = values['created']
    modified = values['modified']
    deadline = values['deadline']
    duration = values['duration']
    render_path_linux = values['render_path_linux']
    path = values['path']
    render_path_windows = values['render_path_windows']
    layer_file = values['layer_file']
    jobs = values['jobs']
    asset = values['asset']
    return Layer(
            url,
            pk,
            name,
            layer_type,
            start,
            end,
            created,
            modified,
            deadline,
            duration,
            render_path_linux,
            path,
            render_path_windows,
            layer_file,
            jobs,
            asset,
        )

def decode_render(values):
    from ..renders import Render
    url = values['url']
    pk = values['pk']
    start = None
    try:
        start = values['start']
    except:
        pass
    end = None
    try:
        end = values['end']
    except:
        pass
    created = values['created']
    modified = values['modified']
    comp_file = values['comp_file']
    department = values['department']
    quicktime_render_movie_windows = values['quicktime_render_movie_windows']
    quicktime_render_movie_linux = values['quicktime_render_movie_linux']
    deadline = values['deadline']
    duration = values['duration']
    render_path_linux = values['render_path_linux']
    quicktime_render_path_windows = values['quicktime_render_path_windows']
    path = values['path']
    render_path_windows = values['render_path_windows']
    quicktime_render_path_linux = values['quicktime_render_path_linux']
    jobs = values['jobs']
    asset = values['asset']
    return Render(
            url,
            pk,
            start,
            end,
            created,
            modified,
            comp_file,
            department,
            quicktime_render_movie_windows,
            quicktime_render_movie_linux,
            deadline,
            duration,
            render_path_linux,
            quicktime_render_path_windows,
            path,
            render_path_windows,
            quicktime_render_path_linux,
            jobs,
            asset,
        )

#DJANGO APP: renderfarm
def decode_renderfarm(values):
    from ..renderfarm import DeadlineJob
    url = values['url']
    pk = values['pk']
    job = values['job']
    duration = None
    try:
        duration = values['duration']
    except:
        pass
    jobtask_total_time = None
    try:
        jobtask_total_time = values['jobtask_total_time']
    except:
        pass
    jobtask_average_time = None
    try:
        jobtask_average_time = values['jobtask_average_time']
    except:
        pass
    jobtask_total_time_norm = None
    try:
        jobtask_total_time_norm = values['jobtask_total_time_norm']
    except:
        pass
    jobtask_average_time_norm = None
    try:
        jobtask_average_time_norm = values['jobtask_average_time_norm']
    except:
        pass
    created = values['created']
    modified = values['modified']
    render = values['render']
    layer = values['layer']
    return DeadlineJob(
            url,
            pk,
            job,
            duration,
            jobtask_total_time,
            jobtask_average_time,
            jobtask_total_time_norm,
            jobtask_average_time_norm,
            created,
            modified,
            render,
            layer,
        )

#DJANGO APP: nodes
def decode_action(values):
    from ..nodes import Action
    url = values['url']
    pk = values['pk']
    name = values['name']
    return Action(
            url,
            pk,
            name,
        )

def decode_camera(values):
    from ..nodes import Camera
    url = values['url']
    pk = values['pk']
    name = values['name']
    clip_start = values['clip_start']
    clip_end = values['clip_end']
    camera_type = values['camera_type']
    focal_length = values['focal_length']
    sensor_width = values['sensor_width']
    return Camera(
            url,
            pk,
            name,
            clip_start,
            clip_end,
            camera_type,
            focal_length,
            sensor_width,
        )

def decode_group(values):
    from ..nodes import Group
    url = values['url']
    pk = values['pk']
    name = values['name']
    asset = values['asset']
    return Group(
            url,
            pk,
            name,
            asset,
        )

def decode_material(values):
    from ..nodes import Material
    url = values['url']
    pk = values['pk']
    name = values['name']
    return Material(
            url,
            pk,
            name,
        )

def decode_scene(values):
    from ..nodes import Scene
    url = values['url']
    pk = values['pk']
    name = values['name']
    camera = values['camera']
    world = values['world']
    frame_start = values['frame_start']
    frame_end = values['frame_end']
    frame_current = values['frame_current']
    return Scene(
            url,
            pk,
            name,
            camera,
            world,
            frame_start,
            frame_end,
            frame_current,
        )

def decode_world(values):
    from ..nodes import World
    url = values['url']
    pk = values['pk']
    name = values['name']
    return World(
            url,
            pk,
            name,
        )

