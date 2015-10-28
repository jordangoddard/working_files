__author__ = 'Jeff.Bell'
from core.movies import Movie
from core.log import Log

class Playblast(object):
    """
    This is a stand-in class that needs to be replaced - placeholder for now
    """
    def __init__(self, asset):
        self.asset = asset
        self.log = Log()

    def __str__(self):
        return "%s - playblast" % asset.code

    def execute(self):
        """
        Do playblast here
        :return:
        """
        self.log.info("Playblasting %s" % self.asset.code)


    @property
    def movie(self):
        return Movie(self)
