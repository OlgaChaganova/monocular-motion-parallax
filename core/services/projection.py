import numpy as np


def linear_projection(coords: np.array, new_min: float, new_max: float) -> np.array:
    """Линейно отображает отрезок в другой"""
    old_min = coords.min()
    old_max = coords.max()
    c = (new_max - new_min) / (old_max - old_min)
    return c * coords - c * old_min + new_min
