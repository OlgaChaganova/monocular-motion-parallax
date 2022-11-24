import typing as tp
from time import time

import numpy as np
from omegaconf import OmegaConf
from matplotlib import pyplot as plt
from matplotlib import animation
from tqdm import tqdm
from cylinder import Cylinder


class DynamicAnimation(object):
    def __init__(self, config_path: str = '../config.yml'):
        self._config = OmegaConf.load(config_path)
        self._config_cyl1 = self._config['cylinders']['cylinder_1']
        self._config_cyl2 = self._config['cylinders']['cylinder_2']
        self._config_anim = self._config['animation']

        self.cylinder1 = Cylinder(rho=self._config_cyl1['rho'], z=self._config_cyl1['z'])
        self.cylinder1.generate_points(points_cnt=self._config_cyl1['points_cnt'])

        self.cylinder2 = Cylinder(rho=self._config_cyl2['rho'], z=self._config_cyl2['z'])
        self.cylinder2.generate_points(points_cnt=self._config_cyl2['points_cnt'])

    @classmethod
    def _get_points(cls, cylinder: Cylinder, config: dict) -> tp.Tuple[np.array, np.array, str]:
        projected_coords = cylinder.project_2d()
        return projected_coords[:, 0], projected_coords[:, 1], config['color']

    def _make_frames(self, ax, frame_cnt: int) -> list:
        frames = []
        for _ in tqdm(range(frame_cnt)):
            self.cylinder1.rotate(direction=self._config_cyl1['direction'], delta_phi=self._config_anim['delta_phi'])
            self.cylinder2.rotate(direction=self._config_cyl2['direction'], delta_phi=self._config_anim['delta_phi'])
            xx1, yy1, color1 = self._get_points(self.cylinder1, self._config_cyl1)
            xx2, yy2, color2 = self._get_points(self.cylinder2, self._config_cyl2)
            scene1 = ax.scatter(xx1, yy1, c=color1, alpha=0.7)
            scene2 = ax.scatter(xx2, yy2, c=color2, alpha=0.7)
            frames.append([scene1, scene2])
        return frames

    def make_animation(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.axis('off')
        frames = self._make_frames(ax, frame_cnt=360)
        anim = animation.ArtistAnimation(fig, frames, interval=20, blit=True, repeat=True)
        anim.save(self._config_anim['save_path'], fps=self._config_anim['fps'], writer='pillow')


if __name__ == '__main__':
    dynamic_animation = DynamicAnimation()
    start_time = time()
    dynamic_animation.make_animation()
    end_time = time()
    print(f'Generation time: {end_time - start_time}')
