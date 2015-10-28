# Class wrapper for Snapshot objects

# Show related decoder
def decode_show(values):
    from core.shows import Show
    pk = values['pk']
    url = values['url']
    #pk = values['pk']
    code = values['code']
    name = values['name']
    #code_client = values['code_client']
    #title = values['title']
    #sequences = values['sequences']
    created = values['created']
    modified = values['modified']
    #res_render_x = values['res_render_x']
    #res_render_y = values['res_render_y']
    #res_playblast_x = values['res_playblast_x']
    #res_playblast_y = values['res_playblast_y']
    #timebase = values['timebase']
    return Show(
            pk,
            url, 
            code, 
            name, 
            created, 
            modified
        )
    #        url, pk, code, name, sequences, 
    #        res_render_x, res_render_y, res_playblast_x, res_playblast_y,
    #        timebase)


# Asset decoder
def decode_asset(values):
    from core.assets import Asset
    pk = values['pk']
    url = values['url']
    type_primary = values['type_primary']
    type_secondary = values['type_secondary']
    type_tertiary = values['type_tertiary']
    code = values['code']
    #code_client = values['code_client']
    show = values['show']
    data = values['data']
    #shots = values['shots']
    parents = values['parents']
    children = values['children']
    images = values['images']
    groups = values['groups']
    created = values['created']
    modified = values['modified']
    start_frame = values['start_frame']
    end_frame = values['end_frame']
    comment = "<No Comment>"
    if "comment" in values.keys():
        comment = values['comment']
    versions = []
    if "versions" in values.keys():
        versions = values['versions']
    path = None
    if "path" in values.keys():
        path = values['path']
    file = None
    if "file" in values.keys():
        file = values['file']
    filename = None
    if "filename" in values.keys():
        filename = values['filename']
    return Asset(
            pk,
            url, 
            type_primary,
            type_secondary,
            type_tertiary,
            code, 
            #code_client, 
            created, 
            modified, 
            show,
            parents,
            children,
            images,
            groups,
            data,
            start_frame,
            end_frame,
            comment=comment,
            versions=versions,
            path=path,
            file=file,
            filename=filename,
        )

# User decoder
def decode_group(values):
    from core.nodes import Group
    pk = values['pk']
    url = values['url']
    name = values['name']
    asset = values['asset']

    return Group(
            pk,
            url,
            name,
            asset,
        )

# User decoder
def decode_image(values):
    from core.images import Image
    pk = values['pk']
    url = values['url']
    name = values['name']
    filepath = values['filepath']
    assets = values['assets']
    width = None  # values['is_staff']
    height = None  # values['is_superuser']
    created = values['created']
    modified = values['modified']

    return Image(
            pk,
            url,
            name,
            filepath,
            assets,
            width,
            height,
            created,
            modified,
        )

# User decoder
def decode_user(values):
    from core.users import User
    pk = values['pk']
    url = values['url']
    username = values['username']
    email = values['email']
    is_staff = values['is_staff']
    is_superuser = values['is_superuser']

    return User(
        pk,
        url,
        username,
        email,
        is_staff,
        is_superuser
    )
