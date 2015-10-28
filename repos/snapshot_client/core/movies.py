__author__ = 'Jeff.Bell'

class Movie(object):
    """
    This is a stand-in class that needs to be replaced - placeholder for now
    """
    def __init__(self, playblast):
        self.playblast = playblast

    def __str__(self):
        return "%s - movie" % playblast.asset.code

    def play(self):
        """
        Play the movie - get RV info from the show preferences
        :return:
        """
        # rv_info = self.playblast.asset.show.preferences.rv_info
        pass
