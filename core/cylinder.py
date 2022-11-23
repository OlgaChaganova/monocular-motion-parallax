import typing as tp

import numpy as np


class Cylinder(object):
    def __init__(self, rho: int | float, z: tp.Tuple[int, int] | tp.Tuple[float, float]):
        assert z[0] < z[1], 'Min z-coordinate must be lower than max z-coordinate'
        self._rho = rho
        self._z = z
        self.points = np.array([])

    def generate_random_points(self, points_cnt: int) -> None:
        """
        Generate random points.

        Parameters
        ----------
        points_cnt : int
            Number of points to be generated.

        Returns
        -------
        np.array
            Array with (x, y, z) coordinates placed at the row. Shape: (points_cnt, 3).
        """

        phis = np.random.uniform(low=0, high=(2 * np.pi), size=points_cnt)
        zs = np.random.uniform(low=self._z[0], high=self._z[1], size=points_cnt)
        xs = self._rho * np.cos(phis)
        ys = self._rho * np.sin(phis)
        self.points = np.column_stack([xs, ys, zs])


if __name__ == '__main__':
    cylinder = Cylinder(rho=5, z=(-5, 5))
    print(cylinder.generate_random_points(points_cnt=50).shape)
