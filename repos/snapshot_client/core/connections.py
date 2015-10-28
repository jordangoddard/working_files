# Class wrapper for CAM communication and connections

import os
import requests
import json
from core import deserializers
from core.log import Log

class Connector(object):
    class __Connector:
        """
        Singleton
        """
        def __init__(self, api_url = None):
            self.api_url = api_url
            if not self.api_url:
                try:
                    self.api_url = os.environ['SNAPSHOT']
                    if not self.api_url.endswith("/"):
                        self.api_url = "%s/" % self.api_url
                    self.log.info("SNAPSHOT IP address: %s" % self.api_url)
                except:
                    self.api_url = "10.1.1.50/"
            #self.assets_url = "%sassets/" % self.api_url
            self.shows_url = "%sshows/" % self.api_url
            self.sequences_url = "%ssequences/" % self.api_url
            self.shots_url = "%sshots/" % self.api_url
            self.images_url = "%simages/" % self.api_url
            self.users_url = "%susers/" % self.api_url
            self.groups_url = "%sgroups/" % self.api_url
            self.session = requests.Session()
            self.log = Log()
            # Set other requests info, like auth, headers, etc

        def __str__(self):
            return self.api_url

        @property
        def assets_url(self):
            return "%sassets/" % self.api_url

        def save(self, item):
            """
            Saves an encoded node to the Snapshot database
            :param item:
            :return:
            """
            pass

        def assets(self, show=None, code=None, type_primary=None, type_secondary=None):
            assets_url = self.assets_url

            query_strings = []
            if show: query_strings.append("show=%s" % show)
            if code: query_strings.append("code=%s" % code)
            if type_primary: query_strings.append("type_primary=%s" % type_primary)
            if type_secondary: query_strings.append("type_secondary=%s" % type_secondary)
            if query_strings:
                assets_url = "%s?%s" % (assets_url, "&".join(query_strings))

            self.log.info("Getting: %s" % assets_url)
            response = self.session.get(assets_url)
            if response.status_code == 200:
                assets = json.loads(response.text, object_hook = deserializers.decode_asset)
                return assets
            else:
                self.log.info(assets_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def asset(self, code=None, asset_url=None, show=None, type_primary=None, type_secondary=None):
            if asset_url:
                response = self.session.get(asset_url)
                if response.status_code == 200:
                    asset = json.loads(response.text, object_hook = deserializers.decode_asset)
                    return asset
                else:
                    self.log.info(asset_url)
                    self.log.info(response.reason, response.status_code)
                    self.log.info(response.text[0:100])
                    return None
            elif code:
                # This should only return one item - slice, if we get something other than []
                result = self.assets(code=code, show=show, type_primary=type_primary, type_secondary=type_secondary)
                if result:
                    if len(result) > 1:
                        self.log.warning("Got more than one entry for %s - %s - %s - %s" % \
                                         (show, type_primary, type_secondary, code))

                    return result[0]
                else:
                    return None
            else:
                msg = "Either an asset_url or an asset code must be provided"
                self.log.error(msg)
                raise Exception(msg)

        def images(self, code=None):
            images_url = self.images_url
            if code:
                images_url = "%s/?code=%s" % code
            response = self.session.get(images_url)
            if response.status_code == 200:
                images = json.loads(response.text, object_hook = deserializers.decode_image)
                #return shows.json()
                return images
            else:
                return None

        def image(self, image_url):
            response = self.session.get(image_url)
            if response.status_code == 200:
                image = json.loads(response.text, object_hook = deserializers.decode_image)
                return image
            else:
                self.log.info(image_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def shows(self, code=None):
            shows_url = self.shows_url
            if code:
                shows_url = "%s/?code=%s" % code
            response = self.session.get(shows_url)
            if response.status_code == 200:
                shows = json.loads(response.text, object_hook = deserializers.decode_show)
                #return shows.json()
                return shows
            else:
                return None

        def show(self, show_url):
            response = self.session.get(show_url)
            if response.status_code == 200:
                show = json.loads(response.text, object_hook = deserializers.decode_show)
                return show
            else:
                self.log.info(show_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def users(self, code=None):
            users_url = self.users_url
            if code:
                users_url = "%s/?code=%s" % code
            response = self.session.get(users_url)
            if response.status_code == 200:
                users = json.loads(response.text, object_hook = deserializers.decode_user)
                #return shows.json()
                return users
            else:
                return None

        def user(self, user_url):
            response = self.session.get(user_url)
            if response.status_code == 200:
                user = json.loads(response.text, object_hook = deserializers.decode_user)
                return user
            else:
                self.log.info(user_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def groups(self, code=None):
            groups_url = self.groups_url
            if code:
                groups_url = "%s/?code=%s" % code
            response = self.session.get(groups_url)
            if response.status_code == 200:
                groups = json.loads(response.text, object_hook = deserializers.decode_group)
                #return shows.json()
                return groups
            else:
                return None

        def group(self, group_url):
            response = self.session.get(group_url)
            if response.status_code == 200:
                group = json.loads(response.text, object_hook = deserializers.decode_group)
                return group
            else:
                self.log.info(group_url)
                self.log.info(response.reason, response.status_code)
                self.log.info(response.text[0:100])
                return None

        def get_current_asset(self):
            """
            Get the asset that's currently loaded, or return None
            """
            import bpy
            asset = None
            scene = bpy.context.screen.scene

            try:
                url = scene.snapshot.url
            except:
                # Create the asset info required?
                self.log.error("No asset defined for the current scene '%s'" % scene.name)
            else:
                asset = self.asset(asset_url=url)
            return asset

    instance = None
    def __new__(cls, *args, **kwargs): # __new__ always a classmethod
        if not Connector.instance:
            Connector.instance = Connector.__Connector(*args, **kwargs)
        return Connector.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)
