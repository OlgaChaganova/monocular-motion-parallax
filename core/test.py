import typing as tp

from services.animation import DynamicAnimation
from services.parallax import Parallax


def test_rotataion(num_tests: int, config_path: str, true_rotation: tp.Literal['clockwise', 'counterclockwise']):
    true_answers = 0
    for _ in range(num_tests):
        dynamic_animation = DynamicAnimation(config_path=config_path)
        raw_images = dynamic_animation.make_animation()
        parallax = Parallax(frames=raw_images)
        direction = parallax.get_rotation_direction()
        if direction == true_rotation:
            true_answers += 1
    return true_answers / num_tests


if __name__ == '__main__':
    num_tests = 20
    test_clockwise_acc = test_rotataion(
        num_tests, config_path='../configs/test_config_clockwise.yml', true_rotation='clockwise',
    )

    test_counterclockwise_acc = test_rotataion(
        num_tests, config_path='../configs/test_config_clockwise.yml', true_rotation='counterclockwise',
    )

    print(f'Clockwise: accuracy: {test_clockwise_acc}')
    print(f'Counterclockwise: accuracy: {test_counterclockwise_acc}')
