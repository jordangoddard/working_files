__author__ = 'Jeff.Bell'


class MyClass(object):
    def __init__(self):
        pass

class BaseFile(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def __str__(self):
        return self.filepath

    def filesize(self):
        return "The filesize"

class ImageClass(BaseFile):

    def resolution(self):
        return "640 x 480"
