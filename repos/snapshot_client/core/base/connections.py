import os
import requests
import json
from .. import deserializers
from core.log import Log
from config import settings

class Connector(object):
    class __Connector:

        def __init__(self, root_url = settings.ROOT_URL):
            self.root_url = root_url
            self.urls = settings.URLS
            self.users_url = "%s%susers/" %(self.root_url, find_key(self.urls, "users"))
            self.preferences_url = "%s%spreferences/" %(self.root_url, find_key(self.urls, "preferences"))
            self.show_url = "%s%sshow/" %(self.root_url, find_key(self.urls, "show"))
            self.assets_url = "%s%sassets/" %(self.root_url, find_key(self.urls, "assets"))
            self.versions_url = "%s%sversions/" %(self.root_url, find_key(self.urls, "versions"))
            self.movies_url = "%s%smovies/" %(self.root_url, find_key(self.urls, "movies"))
            self.images_url = "%s%simages/" %(self.root_url, find_key(self.urls, "images"))
            self.companies_url = "%s%scompanies/" %(self.root_url, find_key(self.urls, "companies"))
            self.layer_url = "%s%slayer/" %(self.root_url, find_key(self.urls, "layer"))
            self.render_url = "%s%srender/" %(self.root_url, find_key(self.urls, "render"))
            self.renderfarm_url = "%s%srenderfarm/" %(self.root_url, find_key(self.urls, "renderfarm"))
            self.action_url = "%s%saction/" %(self.root_url, find_key(self.urls, "action"))
            self.camera_url = "%s%scamera/" %(self.root_url, find_key(self.urls, "camera"))
            self.group_url = "%s%sgroup/" %(self.root_url, find_key(self.urls, "group"))
            self.material_url = "%s%smaterial/" %(self.root_url, find_key(self.urls, "material"))
            self.scene_url = "%s%sscene/" %(self.root_url, find_key(self.urls, "scene"))
            self.world_url = "%s%sworld/" %(self.root_url, find_key(self.urls, "world"))
            self.session = requests.Session()
            self.log = Log()

        def __str__(self):
            return self.root_url

        #DJANGO APP: users
        def users(
                self,
                users_url = None,
            ):
            if not users_url:
                users_url = self.users_url
            query_strings = []
            if query_strings:
                users_url = "%s?%s" % (users_url, "&".join(query_strings))

            self.log.info("Getting: %s" %users_url)
            response = self.session.get(users_url)
            if response.status_code == 200:
                users = json.loads(response.text, object_hook = deserializers.decode_users)
                return users
            else:
                self.log.info(users_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: shows
        def preferences(
                self,
                preferences_url = None,
                res_render_x = None,
                res_render_y = None,
                res_playblast_x = None,
                res_playblast_y = None,
                timebase = None,
                codec = None,
                p_drive = None,
                p_drive_linux = None,
                p_project = None,
                p_render = None,
                p_review = None,
                p_comp = None,
                p_media = None,
                p_publish = None,
                p_sandbox = None,
                show = None,
            ):
            if not preferences_url:
                preferences_url = self.preferences_url
            query_strings = []
            if res_render_x: query_strings.append("res_render_x=%s" % res_render_x)
            if res_render_y: query_strings.append("res_render_y=%s" % res_render_y)
            if res_playblast_x: query_strings.append("res_playblast_x=%s" % res_playblast_x)
            if res_playblast_y: query_strings.append("res_playblast_y=%s" % res_playblast_y)
            if timebase: query_strings.append("timebase=%s" % timebase)
            if codec: query_strings.append("codec=%s" % codec)
            if p_drive: query_strings.append("p_drive=%s" % p_drive)
            if p_drive_linux: query_strings.append("p_drive_linux=%s" % p_drive_linux)
            if p_project: query_strings.append("p_project=%s" % p_project)
            if p_render: query_strings.append("p_render=%s" % p_render)
            if p_review: query_strings.append("p_review=%s" % p_review)
            if p_comp: query_strings.append("p_comp=%s" % p_comp)
            if p_media: query_strings.append("p_media=%s" % p_media)
            if p_publish: query_strings.append("p_publish=%s" % p_publish)
            if p_sandbox: query_strings.append("p_sandbox=%s" % p_sandbox)
            if show: query_strings.append("show=%s" % show)
            if query_strings:
                preferences_url = "%s?%s" % (preferences_url, "&".join(query_strings))

            self.log.info("Getting: %s" %preferences_url)
            response = self.session.get(preferences_url)
            if response.status_code == 200:
                preferences = json.loads(response.text, object_hook = deserializers.decode_preferences)
                return preferences
            else:
                self.log.info(preferences_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def show(
                self,
                show_url = None,
                code = None,
                name = None,
                created = None,
                modified = None,
                company = None,
                preferences = None,
                assets = None,
            ):
            if not show_url:
                show_url = self.show_url
            query_strings = []
            if code: query_strings.append("code=%s" % code)
            if name: query_strings.append("name=%s" % name)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if company: query_strings.append("company=%s" % company)
            if preferences: query_strings.append("preferences=%s" % preferences)
            if assets: query_strings.append("assets=%s" % assets)
            if query_strings:
                show_url = "%s?%s" % (show_url, "&".join(query_strings))

            self.log.info("Getting: %s" %show_url)
            response = self.session.get(show_url)
            if response.status_code == 200:
                show = json.loads(response.text, object_hook = deserializers.decode_show)
                return show
            else:
                self.log.info(show_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: assets
        def assets(
                self,
                assets_url = None,
                type_primary = None,
                type_secondary = None,
                type_tertiary = None,
                code = None,
                description = None,
                comment = None,
                start_frame = None,
                end_frame = None,
                data = None,
                stats_version = None,
                stats_verts = None,
                stats_faces = None,
                stats_tris = None,
                stats_objects = None,
                stats_lamps = None,
                stats_memory = None,
                created = None,
                modified = None,
                images = None,
                parents = None,
                layers = None,
                children = None,
                movies = None,
                renders = None,
                show = None,
                versions = None,
                groups = None,
            ):
            if not assets_url:
                assets_url = self.assets_url
            query_strings = []
            if type_primary: query_strings.append("type_primary=%s" % type_primary)
            if type_secondary: query_strings.append("type_secondary=%s" % type_secondary)
            if type_tertiary: query_strings.append("type_tertiary=%s" % type_tertiary)
            if code: query_strings.append("code=%s" % code)
            if description: query_strings.append("description=%s" % description)
            if comment: query_strings.append("comment=%s" % comment)
            if start_frame: query_strings.append("start_frame=%s" % start_frame)
            if end_frame: query_strings.append("end_frame=%s" % end_frame)
            if data: query_strings.append("data=%s" % data)
            if stats_version: query_strings.append("stats_version=%s" % stats_version)
            if stats_verts: query_strings.append("stats_verts=%s" % stats_verts)
            if stats_faces: query_strings.append("stats_faces=%s" % stats_faces)
            if stats_tris: query_strings.append("stats_tris=%s" % stats_tris)
            if stats_objects: query_strings.append("stats_objects=%s" % stats_objects)
            if stats_lamps: query_strings.append("stats_lamps=%s" % stats_lamps)
            if stats_memory: query_strings.append("stats_memory=%s" % stats_memory)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if images: query_strings.append("images=%s" % images)
            if parents: query_strings.append("parents=%s" % parents)
            if layers: query_strings.append("layers=%s" % layers)
            if children: query_strings.append("children=%s" % children)
            if movies: query_strings.append("movies=%s" % movies)
            if renders: query_strings.append("renders=%s" % renders)
            if show: query_strings.append("show=%s" % show)
            if versions: query_strings.append("versions=%s" % versions)
            if groups: query_strings.append("groups=%s" % groups)
            if query_strings:
                assets_url = "%s?%s" % (assets_url, "&".join(query_strings))

            self.log.info("Getting: %s" %assets_url)
            response = self.session.get(assets_url)
            if response.status_code == 200:
                assets = json.loads(response.text, object_hook = deserializers.decode_assets)
                return assets
            else:
                self.log.info(assets_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: versions
        def versions(
                self,
                versions_url = None,
                version = None,
                comment = None,
                created = None,
                asset = None,
            ):
            if not versions_url:
                versions_url = self.versions_url
            query_strings = []
            if version: query_strings.append("version=%s" % version)
            if comment: query_strings.append("comment=%s" % comment)
            if created: query_strings.append("created=%s" % created)
            if asset: query_strings.append("asset=%s" % asset)
            if query_strings:
                versions_url = "%s?%s" % (versions_url, "&".join(query_strings))

            self.log.info("Getting: %s" %versions_url)
            response = self.session.get(versions_url)
            if response.status_code == 200:
                versions = json.loads(response.text, object_hook = deserializers.decode_versions)
                return versions
            else:
                self.log.info(versions_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: movies
        def movies(
                self,
                movies_url = None,
                name = None,
                filepath = None,
                created = None,
                modified = None,
                asset = None,
            ):
            if not movies_url:
                movies_url = self.movies_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if filepath: query_strings.append("filepath=%s" % filepath)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if asset: query_strings.append("asset=%s" % asset)
            if query_strings:
                movies_url = "%s?%s" % (movies_url, "&".join(query_strings))

            self.log.info("Getting: %s" %movies_url)
            response = self.session.get(movies_url)
            if response.status_code == 200:
                movies = json.loads(response.text, object_hook = deserializers.decode_movies)
                return movies
            else:
                self.log.info(movies_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: images
        def images(
                self,
                images_url = None,
                name = None,
                filepath = None,
                created = None,
                modified = None,
                assets = None,
            ):
            if not images_url:
                images_url = self.images_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if filepath: query_strings.append("filepath=%s" % filepath)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if assets: query_strings.append("assets=%s" % assets)
            if query_strings:
                images_url = "%s?%s" % (images_url, "&".join(query_strings))

            self.log.info("Getting: %s" %images_url)
            response = self.session.get(images_url)
            if response.status_code == 200:
                images = json.loads(response.text, object_hook = deserializers.decode_images)
                return images
            else:
                self.log.info(images_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: companies
        def companies(
                self,
                companies_url = None,
                name = None,
                project_root = None,
                source_root = None,
                render_root = None,
                created = None,
                modified = None,
                shows = None,
            ):
            if not companies_url:
                companies_url = self.companies_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if project_root: query_strings.append("project_root=%s" % project_root)
            if source_root: query_strings.append("source_root=%s" % source_root)
            if render_root: query_strings.append("render_root=%s" % render_root)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if shows: query_strings.append("shows=%s" % shows)
            if query_strings:
                companies_url = "%s?%s" % (companies_url, "&".join(query_strings))

            self.log.info("Getting: %s" %companies_url)
            response = self.session.get(companies_url)
            if response.status_code == 200:
                companies = json.loads(response.text, object_hook = deserializers.decode_companies)
                return companies
            else:
                self.log.info(companies_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: renders
        def layer(
                self,
                layer_url = None,
                name = None,
                layer_type = None,
                start = None,
                end = None,
                created = None,
                modified = None,
                jobs = None,
                asset = None,
            ):
            if not layer_url:
                layer_url = self.layer_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if layer_type: query_strings.append("layer_type=%s" % layer_type)
            if start: query_strings.append("start=%s" % start)
            if end: query_strings.append("end=%s" % end)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if jobs: query_strings.append("jobs=%s" % jobs)
            if asset: query_strings.append("asset=%s" % asset)
            if query_strings:
                layer_url = "%s?%s" % (layer_url, "&".join(query_strings))

            self.log.info("Getting: %s" %layer_url)
            response = self.session.get(layer_url)
            if response.status_code == 200:
                layer = json.loads(response.text, object_hook = deserializers.decode_layer)
                return layer
            else:
                self.log.info(layer_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def render(
                self,
                render_url = None,
                start = None,
                end = None,
                created = None,
                modified = None,
                jobs = None,
                asset = None,
            ):
            if not render_url:
                render_url = self.render_url
            query_strings = []
            if start: query_strings.append("start=%s" % start)
            if end: query_strings.append("end=%s" % end)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if jobs: query_strings.append("jobs=%s" % jobs)
            if asset: query_strings.append("asset=%s" % asset)
            if query_strings:
                render_url = "%s?%s" % (render_url, "&".join(query_strings))

            self.log.info("Getting: %s" %render_url)
            response = self.session.get(render_url)
            if response.status_code == 200:
                render = json.loads(response.text, object_hook = deserializers.decode_render)
                return render
            else:
                self.log.info(render_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: renderfarm
        def renderfarm(
                self,
                renderfarm_url = None,
                job = None,
                duration = None,
                jobtask_total_time = None,
                jobtask_average_time = None,
                jobtask_total_time_norm = None,
                jobtask_average_time_norm = None,
                created = None,
                modified = None,
                render = None,
                layer = None,
            ):
            if not renderfarm_url:
                renderfarm_url = self.renderfarm_url
            query_strings = []
            if job: query_strings.append("job=%s" % job)
            if duration: query_strings.append("duration=%s" % duration)
            if jobtask_total_time: query_strings.append("jobtask_total_time=%s" % jobtask_total_time)
            if jobtask_average_time: query_strings.append("jobtask_average_time=%s" % jobtask_average_time)
            if jobtask_total_time_norm: query_strings.append("jobtask_total_time_norm=%s" % jobtask_total_time_norm)
            if jobtask_average_time_norm: query_strings.append("jobtask_average_time_norm=%s" % jobtask_average_time_norm)
            if created: query_strings.append("created=%s" % created)
            if modified: query_strings.append("modified=%s" % modified)
            if render: query_strings.append("render=%s" % render)
            if layer: query_strings.append("layer=%s" % layer)
            if query_strings:
                renderfarm_url = "%s?%s" % (renderfarm_url, "&".join(query_strings))

            self.log.info("Getting: %s" %renderfarm_url)
            response = self.session.get(renderfarm_url)
            if response.status_code == 200:
                renderfarm = json.loads(response.text, object_hook = deserializers.decode_renderfarm)
                return renderfarm
            else:
                self.log.info(renderfarm_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        #DJANGO APP: nodes
        def action(
                self,
                action_url = None,
                name = None,
            ):
            if not action_url:
                action_url = self.action_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if query_strings:
                action_url = "%s?%s" % (action_url, "&".join(query_strings))

            self.log.info("Getting: %s" %action_url)
            response = self.session.get(action_url)
            if response.status_code == 200:
                action = json.loads(response.text, object_hook = deserializers.decode_action)
                return action
            else:
                self.log.info(action_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def camera(
                self,
                camera_url = None,
                name = None,
                clip_start = None,
                clip_end = None,
                camera_type = None,
                focal_length = None,
                sensor_width = None,
            ):
            if not camera_url:
                camera_url = self.camera_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if clip_start: query_strings.append("clip_start=%s" % clip_start)
            if clip_end: query_strings.append("clip_end=%s" % clip_end)
            if camera_type: query_strings.append("camera_type=%s" % camera_type)
            if focal_length: query_strings.append("focal_length=%s" % focal_length)
            if sensor_width: query_strings.append("sensor_width=%s" % sensor_width)
            if query_strings:
                camera_url = "%s?%s" % (camera_url, "&".join(query_strings))

            self.log.info("Getting: %s" %camera_url)
            response = self.session.get(camera_url)
            if response.status_code == 200:
                camera = json.loads(response.text, object_hook = deserializers.decode_camera)
                return camera
            else:
                self.log.info(camera_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def group(
                self,
                group_url = None,
                name = None,
                asset = None,
            ):
            if not group_url:
                group_url = self.group_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if asset: query_strings.append("asset=%s" % asset)
            if query_strings:
                group_url = "%s?%s" % (group_url, "&".join(query_strings))

            self.log.info("Getting: %s" %group_url)
            response = self.session.get(group_url)
            if response.status_code == 200:
                group = json.loads(response.text, object_hook = deserializers.decode_group)
                return group
            else:
                self.log.info(group_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def material(
                self,
                material_url = None,
                name = None,
            ):
            if not material_url:
                material_url = self.material_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if query_strings:
                material_url = "%s?%s" % (material_url, "&".join(query_strings))

            self.log.info("Getting: %s" %material_url)
            response = self.session.get(material_url)
            if response.status_code == 200:
                material = json.loads(response.text, object_hook = deserializers.decode_material)
                return material
            else:
                self.log.info(material_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def scene(
                self,
                scene_url = None,
                name = None,
                camera = None,
                world = None,
                frame_start = None,
                frame_end = None,
                frame_current = None,
            ):
            if not scene_url:
                scene_url = self.scene_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if camera: query_strings.append("camera=%s" % camera)
            if world: query_strings.append("world=%s" % world)
            if frame_start: query_strings.append("frame_start=%s" % frame_start)
            if frame_end: query_strings.append("frame_end=%s" % frame_end)
            if frame_current: query_strings.append("frame_current=%s" % frame_current)
            if query_strings:
                scene_url = "%s?%s" % (scene_url, "&".join(query_strings))

            self.log.info("Getting: %s" %scene_url)
            response = self.session.get(scene_url)
            if response.status_code == 200:
                scene = json.loads(response.text, object_hook = deserializers.decode_scene)
                return scene
            else:
                self.log.info(scene_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def world(
                self,
                world_url = None,
                name = None,
            ):
            if not world_url:
                world_url = self.world_url
            query_strings = []
            if name: query_strings.append("name=%s" % name)
            if query_strings:
                world_url = "%s?%s" % (world_url, "&".join(query_strings))

            self.log.info("Getting: %s" %world_url)
            response = self.session.get(world_url)
            if response.status_code == 200:
                world = json.loads(response.text, object_hook = deserializers.decode_world)
                return world
            else:
                self.log.info(world_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

    instance = None
    def __new__(cls, *args, **kwargs):
        if not Connector.instance:
            Connector.instance = Connector.__Connector(*args, **kwargs)
        return Connector.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


#Useful Global Functions
def find_key(dict, value):
    for key in dict.keys():
        if isinstance(dict[key], tuple):
            for item in dict[key]:
                if item == value:
                    return key
        elif dict[key] == value:
            return key
    return None

