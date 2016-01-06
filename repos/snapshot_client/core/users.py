from .base.users import User as User_base

class User(User_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s - %s" %(self.username, self.email)
        
    def __repr__(self):
        return self.__str__()
        
    pass


