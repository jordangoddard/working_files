from .. import connections

class User(object):
    def __init__(
            self,
            url,
            pk,
            is_superuser,
            username,
            email,
            is_staff,
        ):
        self.url = url
        self.pk = pk
        self.is_superuser = is_superuser
        self.username = username
        self.email = email
        self.is_staff = is_staff
        self.snapshot = connections.Connector()

    def encode(self):
        data = {}
        data['url'] = self.url
        data['pk'] = self.pk
        data['is_superuser'] = self.is_superuser
        data['username'] = self.username
        data['email'] = self.email
        data['is_staff'] = self.is_staff
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
            from ..deserializers import decode_users
            import json
            self._update(json.loads(response.text, object_hook=decode_users))
        else:
            print("Error while trying to save file to the database: %s" %response.text)

