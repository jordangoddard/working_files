from .. import connections

class Preferences(object):
    def __init__(
            self,
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
        ):
        self.url = url
        self.pk = pk
        self.res_render_x = res_render_x
        self.res_render_y = res_render_y
        self.res_playblast_x = res_playblast_x
        self.res_playblast_y = res_playblast_y
        self.timebase = timebase
        self.codec = codec
        self.p_drive = p_drive
        self.p_drive_linux = p_drive_linux
        self.p_project = p_project
        self.p_render = p_render
        self.p_review = p_review
        self.p_comp = p_comp
        self.p_media = p_media
        self.p_publish = p_publish
        self.p_sandbox = p_sandbox
        self.path_drive = path_drive
        self.path_project = path_project
        self.path_sandbox = path_sandbox
        self.path_render = path_render
        self.path_media = path_media
        self.path_publish = path_publish
        self.path_review = path_review

        #Foreign Key related data - cache this using properties setters/getters 
        self._show = None 
        self._show_urls = None 
        self.show = show

        self.snapshot = connections.Connector()

    @property
    def show(self):
        if self._show_urls and not self._show:
            self._show = self.snapshot.show(show_url = self._show_urls)
        return self._show

    @show.setter
    def show(self, value):
        self._show_urls = value
        self._show = None

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['res_render_x'] = self.res_render_x
        data['res_render_y'] = self.res_render_y
        data['res_playblast_x'] = self.res_playblast_x
        data['res_playblast_y'] = self.res_playblast_y
        data['timebase'] = self.timebase
        data['codec'] = self.codec
        data['p_drive'] = self.p_drive
        data['p_drive_linux'] = self.p_drive_linux
        data['p_project'] = self.p_project
        data['p_render'] = self.p_render
        data['p_review'] = self.p_review
        data['p_comp'] = self.p_comp
        data['p_media'] = self.p_media
        data['p_publish'] = self.p_publish
        data['p_sandbox'] = self.p_sandbox
        data['path_drive'] = self.path_drive
        data['path_project'] = self.path_project
        data['path_sandbox'] = self.path_sandbox
        data['path_render'] = self.path_render
        data['path_media'] = self.path_media
        data['path_publish'] = self.path_publish
        data['path_review'] = self.path_review
        data['show'] = None
        if self.show: data['show'] = self.show.url
        return data

    def _update(self, data):
        for key, value in data.__dict__.items():
            setattr(self, key, value)

    def save(self):
        if self.pk:
            response = self.snapshot.session.put(self.url, self.encode())
        else:
            response = self.snapshot.session.post(self.url, self.encode())
        if response.status_code in [200, 201]:
            from ..deserializers import decode_preferences
            import json
            self._update(json.loads(response.text, object_hook=decode_preferences))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

class Show(object):
    def __init__(
            self,
            url,
            pk,
            code,
            name,
            created,
            modified,
            company,
            preferences,
            assets,
        ):
        self.url = url
        self.pk = pk
        self.code = code
        self.name = name
        self.created = created
        self.modified = modified

        #Foreign Key related data - cache this using properties setters/getters 
        self._company = None 
        self._company_urls = None 
        self.company = company

        self._preferences = None 
        self._preferences_urls = None 
        self.preferences = preferences

        self._assets = [] 
        self._assets_urls = None 
        self.assets = assets

        self.snapshot = connections.Connector()

    @property
    def company(self):
        if self._company_urls and not self._company:
            self._company = self.snapshot.companies(companies_url = self._company_urls)
        return self._company

    @company.setter
    def company(self, value):
        self._company_urls = value
        self._company = None

    @property
    def preferences(self):
        if self._preferences_urls and not self._preferences:
            self._preferences = self.snapshot.preferences(preferences_url = self._preferences_urls)
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences_urls = value
        self._preferences = None

    @property
    def assets(self):
        if self._assets_urls and not self._assets:
            for assets_url in self._assets_urls:
                self._assets.append(self.snapshot.assets(assets_url = assets_url))
        return self._assets

    @assets.setter
    def assets(self, value):
        self._assets_urls = value
        self._assets = []

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['code'] = self.code
        data['name'] = self.name
        data['created'] = self.created
        data['modified'] = self.modified
        data['company'] = None
        if self.company: data['company'] = self.company.url
        data['preferences'] = None
        if self.preferences: data['preferences'] = self.preferences.url
        data['assets'] = None
        if self.assets: data['assets'] = [item.url for item in self.assets]
        return data

    def _update(self, data):
        for key, value in data.__dict__.items():
            setattr(self, key, value)

    def save(self):
        if self.pk:
            response = self.snapshot.session.put(self.url, self.encode())
        else:
            response = self.snapshot.session.post(self.url, self.encode())
        if response.status_code in [200, 201]:
            from ..deserializers import decode_show
            import json
            self._update(json.loads(response.text, object_hook=decode_show))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

