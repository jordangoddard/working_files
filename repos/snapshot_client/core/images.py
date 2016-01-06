from .base.images import Image as Image_base

class Image(Image_base):

    #PUT YOUR CODE HERE

    def __str__(self):
        return ("%s > %s > %s.%s" (self.name, self.filepath, self.width, self.height))


