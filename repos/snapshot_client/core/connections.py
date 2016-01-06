from .base.connections import Connector as Connector_base

class Connector(Connector_base):

    #PUT YOUR CODE HERE

    class __Connector(Connector_base.__Connector):
        def __init__(self, *args, **kwargs):
            Connector_base.__Connector.__init__(self, *args, **kwargs)

        instance = None
        def __new__(cls, *args, **kwargs):
            if not Connector.instance:
                Connector.instance = Connector.__Connector(*args, **kwargs)
            return Connector.instance

        def __getattr__(self, name):
            return getattr(self.instance, name)

        def __setattr__(self, name):
            return setattr(self.instance, name)

