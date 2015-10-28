__author__ = 'Jeff.Bell'

import shelve

class DataPersistCache(object):
    def __init__(
            self,
            url=None,
            data=None,
            previous_operation=None,
            filepath="C:/temp/",
            filename="data_persist.cache",
            function="SAVE"):

        self.url = url
        self.data = data
        self.previous_operation = previous_operation
        self.filepath = filepath
        self.filename = filename
        self.file = "%s/%s" % (self.filepath, self.filename)

        if function == "SAVE":
            self.save()
        elif function == "LOAD":
            self.load()

    def _create_cache_dir(self):
        import os
        if not os.path.exists(self.filepath):
            print("Creating cache directory: %s" % self.filepath)
            os.makedirs(self.filepath, mode=0o777)

    def save(self):
        print("Opening %s to save data cache" % (self.file))
        self._create_cache_dir()
        outf = shelve.open(self.file)
        outf['data_persist_cache'] = self
        outf.close()

    def load(self):
        print("Opening %s to load data cache" % self.file)
        try:
            inputf = shelve.open(self.file)
            cached_data = inputf['data_persist_cache']
            self.data = cached_data.data
            self.url = cached_data.url
            self.previous_operation = cached_data.previous_operation
        except KeyError:
            print("KeyError when attempting to load cache")
            return None
        finally:
            print("Loaded cached data")
            inputf.close()


# Example of inheritance, and calling the
class InheritanceExampleCache(DataPersistCache):
    def __init__(self, url="blah", extra_data="Extra Data!", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.extra_data = extra_data

    def print_this(self):
        print(self.extra_data, self.url)
