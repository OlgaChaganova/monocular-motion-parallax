from time import time

from animation import DynamicAnimation


if __name__ == '__main__':
    dynamic_animation = DynamicAnimation()
    start_time = time()
    dynamic_animation.make_animation()
    end_time = time()
    print(f'Generation time: {end_time - start_time}')