
def iterateGrid(func):
    def inner(object, update=False):
        for y in range(object.rows):
            for x in range(object.columns):
                func(object, x, y)
        if update:
            object.notifyObservers()

    return inner
