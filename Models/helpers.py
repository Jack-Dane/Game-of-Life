
def iterateGrid(func):
    def inner(object, update=False):
        for x in range(object.rows):
            for y in range(object.columns):
                func(object, x, y)
        if update:
            object.notifyObservers()

    return inner
