import typing as tp

import numpy as np


class Cylinder(object):
    """Cylinder class."""

    def __init__(self, rho: int | float, z: tp.Tuple[int, int] | tp.Tuple[float, float]):
        """
        Initialize Cylinder.

        Parameters
        ----------
        rho : int | float
            Radius.

        z : tp.Tuple[int, int] | tp.Tuple[float, float]
            Tuple with (z_min, z_max) coordinates.
        """
        assert z[0] < z[1], 'Min z-coordinate must be lower than max z-coordinate'
        self._rho = rho
        self._z = z
        self.points = np.array([])

    def generate_points(self, points_cnt: int):
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
        self.points = np.column_stack([phis, zs])

    def cylindrical2cartesian(self, points: np.array) -> np.array:
        """
        Move from cylindrical (rho, phi, z) to cartesian (x, y, z) coordinate system.

        Parameters
        ----------
        points : np.array
            Points of the cylinder in cylindrical coordinate system (phi, z). Shape: [points_cnt, 2].

        Returns
        -------
        np.array
            Points in cartesian (x, y, z) coordinate system. Shape: [points_cnt, 3]
        """
        phis, zs = points[:, 0], points[:, 1]
        xs = self._rho * np.cos(phis)
        ys = self._rho * np.sin(phis)
        return np.column_stack([xs, ys, zs])

    def rotate(
        self,
        direction: tp.Literal['clockwise', 'counterclockwise'],
        delta_phi: float = 1,
    ) -> None:
        """
        Rotate the cylinder.

        Parameters
        ----------
        direction : tp.Literal['clockwise', 'counterclockwise']
            Direction of the rotation.

        delta_phi : float
            Delta of the phi angle.
        """
        assert direction in ['clockwise', 'counterclockwise'], \
            'Direction must be one of the following: clockwise, counterclockwise'
        if direction == 'clockwise':
            self.points[:, 0] -= delta_phi * np.pi / 180
        else:
            self.points[:, 0] += delta_phi * np.pi / 180

    def project_2d(self) -> np.array:
        """
        Project 3D points (x, y, z) to 2D (x, y).

        Returns
        -------
        np.array
            Points in 2D-cartesian (x, y) coordinate system. Shape: [points_cnt, 2]
        """
        points = self.points
        points = self.cylindrical2cartesian(points)
        xs, ys, zs = points[:, 0], points[:, 1], points[:, 2]
        return np.column_stack([xs, zs])
