import typing as tp


class Parallax(object):
    def __init__(self, frames: list):
        self._frames = frames

    def get_rotation_direction(self) -> tp.Literal['clockwise', 'counterclockwise']:
        frames = self._frames
        return 'clockwise'

    def estimate_angular_speed(self) -> float:
        ...

    def track_point(self):
        ...



