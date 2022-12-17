from services.animation import DynamicAnimation
from services.parallax import Parallax


if __name__ == '__main__':
    dynamic_animation = DynamicAnimation()

    # 1. make animation
    raw_images = dynamic_animation.make_animation()

    # 2. track point

    # 3. estimate angular speed and rotation direction
    parallax = Parallax(frames=raw_images)

    angular_speed = parallax.estimate_angular_speed()
    print(f'Estimated angular speed: {angular_speed}')

    direction = parallax.get_rotation_direction()
    print(f'Direction of rotation: {direction}')
