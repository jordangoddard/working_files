import bpy
from core.log import Log
from core import connections

class Library(object):
    def __init__(self, library):
        self._library = library
        self._asset = None  # Asset cache
        self.log = Log()
        self.snapshot = connections.Connector()

    def __repr__(self):
        return self._library.filepath

    @property
    def asset(self):
        import os
        # Figure out what asset this library refers to
        if not self._asset:
            filepath = os.path.split(self._library.filepath)[0]

            # Get the asset data associated with this linked library
            code = os.path.normpath(filepath).split(os.path.sep)[-1:][0]
            type_secondary = os.path.normpath(filepath).split(os.path.sep)[-2:-1][0]
            type_primary = os.path.normpath(filepath).split(os.path.sep)[-3:-2][0]
            show = os.path.normpath(filepath).split(os.path.sep)[-4:-3][0]
            self.log.info(", ".join([show, type_primary, type_secondary, code]))
            self._asset = self.snapshot.asset(
                code=code, type_primary=type_primary, type_secondary=type_secondary, show=show
            )
        return self._asset

    @property
    def filepath(self):
        return self._library.filepath


class ObjectLibrary(Library):
    def __init__(self, object, *args, **kwargs):
        super().__init__(library=object.library, *args, **kwargs)


