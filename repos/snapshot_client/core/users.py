# User object from Snapshot

class User(object):
    def __init__(self, pk, url, username, email, is_staff, is_superuser):
        self.pk = pk
        self.url = url
        self.username = username
        self.email = email
        self.is_staff = is_staff
        self.is_superuser = is_superuser

    def __str__(self):
        return "%s - %s" % (username, email)
