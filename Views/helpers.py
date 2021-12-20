
class NoScreenAssignedException(Exception):
    pass


def ensureScreen(func):
    def inner(object, *args):
        if object.screen is not None:
            return func(object, *args)
        raise NoScreenAssignedException()

    return inner
