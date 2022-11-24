import typing as tp
from time import time

import numpy as np
from omegaconf import OmegaConf
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

from cylinder import Cylinder


class DynamicAnimation(object):
    def __init__(self, config_path: str = '../config.yml'):
        self._config = OmegaConf.load(config_path)
        self._config_cyl = self._config['cylinders']
        self._config_anim = self._config['animation']

        self.cylinder1 = Cylinder(rho=self._config_cyl['cylinder_1']['rho'], z=self._config_cyl['cylinder_1']['z'])
        self.cylinder1.generate_points(points_cnt=self._config_cyl['cylinder_1']['points_cnt'])

        self.cylinder2 = Cylinder(rho=self._config_cyl['cylinder_2']['rho'], z=self._config_cyl['cylinder_2']['z'])
        self.cylinder2.generate_points(points_cnt=self._config_cyl['cylinder_2']['points_cnt'])

    @classmethod
    def _get_points(cls, cylinder: Cylinder, config: dict) -> tp.Tuple[np.array, np.array, np.array, str]:
        cartesian_coords = cylinder.cylindrical2cartesian(cylinder.points)
        xx = cartesian_coords[:, 0]
        yy = cartesian_coords[:, 1]
        zz = cartesian_coords[:, 2]
        return xx, yy, zz, config['color']

    def make_animation(self):
        def init():
            ax.scatter(xx1, yy1, zz1, marker='o', s=20, c=color1, alpha=0.7)
            ax.scatter(xx2, yy2, zz2, marker='o', s=20, c=color2, alpha=0.7)
            return fig,

        def animate(i):
            start_time = time()
            ax = Axes3D(fig, elev=self._config_anim['elev'])
            ax.dist = self._config_anim['dist']
            ax.axis('off')
            self.cylinder1.rotate(direction='counterclockwise', delta_phi=self._config_anim['delta_phi'])
            self.cylinder2.rotate(direction='clockwise', delta_phi=self._config_anim['delta_phi'])
            xx1, yy1, zz1, color1 = self._get_points(self.cylinder1, self._config_cyl['cylinder_1'])
            xx2, yy2, zz2, color2 = self._get_points(self.cylinder2, self._config_cyl['cylinder_2'])
            ax.scatter(xx1, yy1, zz1, marker='o', s=20, c=color1, alpha=0.7)
            ax.scatter(xx2, yy2, zz2, marker='o', s=20, c=color2, alpha=0.7)
            # print(f'# {i} time: {time() - start_time}')
            return fig,

        # Create a figure and a 3D Axes
        fig = plt.figure(figsize=(7, 7))
        ax = Axes3D(fig, elev=self._config_anim['elev'])
        ax.dist = self._config_anim['dist']
        ax.axis('off')
        xx1, yy1, zz1, color1 = self._get_points(self.cylinder1, self._config_cyl['cylinder_1'])
        xx2, yy2, zz2, color2 = self._get_points(self.cylinder2, self._config_cyl['cylinder_2'])

        anim = animation.FuncAnimation(
            fig,
            animate,
            init_func=init,
            frames=(360 // self._config_anim['delta_phi']),
            interval=1,
            blit=True,
        )
        anim.save(self._config_anim['save_path'], fps=self._config_anim['fps'])


if __name__ == '__main__':
    dynamic_animation = DynamicAnimation()
    start_time = time()
    dynamic_animation.make_animation()
    end_time = time()
    print(f'Generation time: {end_time - start_time}')
