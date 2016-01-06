from .base.nodes import Action as Action_base

class Action(Action_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s" % self.name
    pass


from .base.nodes import Camera as Camera_base

class Camera(Camera_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s > %smm" % (self.name, self.focal_length)
    pass


from .base.nodes import Group as Group_base

class Group(Group_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s" % self.name

    pass


from .base.nodes import Material as Material_base

class Material(Material_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s" % self.name
    pass


from .base.nodes import Scene as Scene_base

class Scene(Scene_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s" % self.name
    pass


from .base.nodes import World as World_base

class World(World_base):

    #PUT YOUR CODE HERE
    def __str__(self):
        return "%s" % self.name
    pass


