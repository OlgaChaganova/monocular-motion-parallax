import typing as tp
from time import time

import numpy as np
from omegaconf import OmegaConf
from matplotlib import pyplot as plt
from matplotlib import animation
from tqdm import tqdm

from .cylinder import Cylinder
from .projection import linear_projection


class DynamicAnimation(object):
    """Animation class."""

    def __init__(self, config_path: str = '../config.yml'):
        """
        Initialize DynamicAnimation class.

        Parameters
        ----------
        config_path : str
            Path to config.
        """
        self._config = OmegaConf.load(config_path)
        self._config_cyl1 = self._config['cylinders']['cylinder_1']
        self._config_cyl2 = self._config['cylinders']['cylinder_2']
        self._config_anim = self._config['animation']
        self._config_cam = self._config['camera']

        self.cylinder1 = Cylinder(rho=self._config_cyl1['rho'], z=self._config_cyl1['z'])
        self.cylinder1.generate_points(points_cnt=self._config_cyl1['points_cnt'])

        self.cylinder2 = Cylinder(rho=self._config_cyl2['rho'], z=self._config_cyl2['z'])
        self.cylinder2.generate_points(points_cnt=self._config_cyl2['points_cnt'])

    def make_animation(self) -> list:
        """Make animation with cylinders."""
        start_time = time()
        fig = plt.figure(figsize=(5, 5))
        plt.gray()
        ax = fig.add_subplot(111)
        ax.axis('off')
        frame_cnt = round(360 // self._config_anim['delta_phi'])
        frames = self._make_frames(ax, frame_cnt=frame_cnt)
        anim = animation.ArtistAnimation(fig, frames, interval=20, blit=True, repeat=True)
        print(f'Total generation time: {round(time() - start_time, 3)} s')
        if self._config_anim['save']:
            anim.save(self._config_anim['save_path'], fps=self._config_anim['fps'], writer='pillow')
        plt.show()
        return frames

    def _get_points(self, cylinder1: Cylinder, cylinder2: Cylinder) -> tp.Tuple[np.array, np.array, np.array, np.array]:
        """Get points in correct format for 2d projection. One point is one pixel on the image."""
        width = self._config_anim['frame_width']

        projected_coords1 = cylinder1.project_2d(self._config_cam['distance'])
        projected_coords2 = cylinder2.project_2d(self._config_cam['distance'])
        x_proj1, y_proj1 = projected_coords1[:, 0], projected_coords1[:, 1]
        x_proj2, y_proj2 = projected_coords2[:, 0], projected_coords2[:, 1]

        # concatenate arrays to save their structure on the image
        # if we scale coordinates separately, position structure of the cylinders will be broken
        x_proj = np.hstack([x_proj1, x_proj2])
        y_proj = np.hstack([y_proj1, y_proj2])
        points_cnt1 = x_proj1.shape[0]

        # get point coordinates in the image
        image_shape = self._config_anim['image_shape']

        # add width // 2 to get frame on the final image
        x_scaled = (np.clip(linear_projection(x_proj, 0, image_shape[1]), 0, image_shape[1] - 1) + width // 2).astype(np.int32)
        y_scaled = (np.clip(linear_projection(y_proj, 0, image_shape[0]), 0, image_shape[0] - 1) + width // 2).astype(np.int32)
        return x_scaled[:points_cnt1], y_scaled[:points_cnt1], x_scaled[points_cnt1:], y_scaled[points_cnt1:]

    def _draw_points(self, x_coords: np.array, y_coords: np.array, point_size: int) -> np.array:
        width = self._config_anim['frame_width']
        image_shape = self._config_anim['image_shape']
        image_shape = (image_shape[0] + width, image_shape[1] + width)
        image = np.zeros(image_shape, dtype=np.float16)
        for x, y in zip(x_coords, y_coords):
            image[(y - point_size // 2):(y + point_size // 2), (x - point_size // 2):(x + point_size // 2)] = 0.5
            image[y, x] = 1  # central pixel of the point
        return image

    def _make_frames(self, ax, frame_cnt: int) -> list:
        """Make frames for animation."""
        frames = []
        for _ in tqdm(range(frame_cnt)):
            self.cylinder1.rotate(direction=self._config_cyl1['direction'], delta_phi=self._config_anim['delta_phi'])
            self.cylinder2.rotate(direction=self._config_cyl2['direction'], delta_phi=self._config_anim['delta_phi'])
            xx1, yy1, xx2, yy2 = self._get_points(self.cylinder1, self.cylinder2)
            image1 = self._draw_points(xx1, yy1, self._config_cyl1['point_size'])
            image2 = self._draw_points(xx2, yy2, self._config_cyl2['point_size'])
            scene1 = ax.imshow(image1 + image2)  # adding image of 1st cylinder with image of the 2nd cylinder
            frames.append([scene1])
        return frames
