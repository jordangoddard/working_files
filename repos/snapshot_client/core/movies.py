from .base.movies import Movie as Movie_base

class Movie(Movie_base):

    #PUT YOUR CODE HERE

    """
    This is a stand-in class that needs to be replaced - placeholder for now
    """
    def __str__(self):
        return "%s - movie" % self.asset.code

    def play(self):
        """
        Play the movie - get RV info from the show preferences
        :return:
        """
        # rv_info = self.playblast.asset.show.preferences.rv_info
        pass
        
    


