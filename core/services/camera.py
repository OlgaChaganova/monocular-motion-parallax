class Camera(object):
    def __init__(self, distance: int | float):
        self._distance = distance

    @property
    def distance(self):
        return self._distance