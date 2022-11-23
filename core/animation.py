import typing as tp

import numpy as np
from omegaconf import OmegaConf
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

from cylinder import Cylinder


class DynamicAnimation(object):
    def __init__(self):
        self._config = OmegaConf.load('../config.yml')
        self._config_cyl = self._config['cylinders']
        self._config_anim = self._config['animation']

    @classmethod
    def _generate_points(cls, config: dict) -> tp.Tuple[np.array, np.array, np.array, str]:
        cylinder = Cylinder(
            rho=config['rho'],
            z=config['z'],
        )
        cylinder.generate_random_points(points_cnt=config['points_cnt'])
        xx = cylinder.points[:, 0]
        yy = cylinder.points[:, 1]
        zz = cylinder.points[:, 2]
        return xx, yy, zz, config['color']

    def make_animation(self):
        def init():
            ax.scatter(xx1, yy1, zz1, marker='o', s=20, c=color1, alpha=0.7)
            ax.scatter(xx2, yy2, zz2, marker='o', s=20, c=color2, alpha=0.7)
            return fig,

        def animate(i):
            ax.view_init(azim=(dest_coeff * i))
            ax.dist = self._config_anim['dist']
            return fig,

        xx1, yy1, zz1, color1 = self._generate_points(self._config_cyl['cylinder_1'])
        xx2, yy2, zz2, color2 = self._generate_points(self._config_cyl['cylinder_2'])
        dest_coeff = 1 if self._config_anim['direction'] == 'counterclockwise' else -1  # TODO: not working as expected

        # Create a figure and a 3D Axes
        fig = plt.figure(figsize=(7, 7))
        ax = Axes3D(fig, elev=self._config_anim['elev'])
        ax.dist = self._config_anim['dist']
        ax.axis('off')

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=360, interval=1, blit=True)

        anim.save(self._config_anim['save_path'], fps=self._config_anim['fps'])


if __name__ == '__main__':
    dynamic_animation = DynamicAnimation()
    dynamic_animation.make_animation()
