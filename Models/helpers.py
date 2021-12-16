
def iterateGrid(func):
    def inner(object):
        for x in range(object.rows):
            for y in range(object.columns):
                func(object, x, y)
    return inner
