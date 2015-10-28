__author__ = 'Jeff.Bell'

def proc():
    print("Hello Blender.")

def proc_with_param(value):
    """

    :param value:
    """
    print(value)


def proc_with_optional_value(value="Default Value"):
    """

    :param value:
    """
    print(value)

def proc_with_values(not_optional, optional=None):
    """

    :param value:
    """
    print(not_optional, optional)

def proc_with_return():
    return "Something"

