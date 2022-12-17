import typing as tp

import cv2
import numpy as np


ERROR_MESSAGE_ROTATION = 'Cannot find direction due to lack of information. Try to increase number of points'


class Parallax(object):
    def __init__(self, frames: list):
        self._frames = frames

    def get_rotation_direction(self) -> tp.Literal['clockwise', 'counterclockwise', ERROR_MESSAGE_ROTATION]:
        frames = self._frames
        frame_start = frames[0]
        frame_next = frames[5]
        points_start = list(zip(*np.where(frame_start == 1)))
        points_next = list(zip(*np.where(frame_next == 1)))
        # print(frame_start.shape, frame_start.dtype)
        # cv2.imshow('start', cv2.cvtColor(frame_start.astype('uint8'), cv2.COLOR_GRAY2BGR))
        # cv2.imshow('next', cv2.cvtColor(frame_next.astype('uint8'), cv2.COLOR_GRAY2BGR))
        # cv2.waitKey(0)

        delta_xs = []
        for point_start, point_next in zip(points_start, points_next):
            y_start, x_start = point_start
            y_next, x_next = point_next
            delta_xs.append(x_next - x_start)

        delta_xs = sorted(delta_xs)  # from max abs(negative) to max positive
        # print(delta_xs)
        delta_x_neg = delta_xs[0]
        delta_x_pos = delta_xs[-1]

        if delta_x_neg * delta_x_pos > 0 or np.allclose(abs(delta_x_neg), delta_x_pos):
            return ERROR_MESSAGE_ROTATION
        else:
            if abs(delta_x_neg) > delta_x_pos:
                return 'clockwise'
            else:
                return 'counterclockwise'

    def estimate_angular_speed(self) -> float:
        ...

    def track_point(self):
        ...



