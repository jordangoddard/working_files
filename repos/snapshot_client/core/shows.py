from .base.shows import Preferences as Preferences_base

class Preferences(Preferences_base):

    #PUT YOUR CODE HERE

    pass


from .base.shows import Show as Show_base

class Show(Show_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s" % self.code

    def __repr__(self):
        return self.__str__()
        
    pass


