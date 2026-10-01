import math
import random
from functools import lru_cache
from pathlib import Path

import pygame

if __package__:
    from ._bootstrap import ensure_project_root
else:
    from _bootstrap import ensure_project_root

ensure_project_root()

from config import ROOT_DIR


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def normalize(vec):
    length = math.hypot(vec[0], vec[1])
    if length == 0:
        return (0.0, 0.0)
    return (vec[0] / length, vec[1] / length)


def angle_to(target, source):
    return math.atan2(target[1] - source[1], target[0] - source[0])


def get_asset_path(*parts):
    relative = Path(*parts)
    return str(ROOT_DIR / relative)


@lru_cache(maxsize=256)
def _load_image_cached(path, size, colorkey, alpha):
    try:
        image = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
        if size:
            image = pygame.transform.scale(image, size)
        if colorkey is not None:
            image.set_colork_key(colorkey)
        return image
    except Exception:
        return None


def load_image(path, size=None, colorkey=None, alpha=True):
    cache_size = tuple(size) if size is not None else None
    cache_colorkey = tuple(colorkey) if colorkey is not None else None
    return _load_image_cached(str(path), cache_size, cache_colorkey, alpha)


def random_choice_weighted(items):
    return random.choice(items)


def lerp(a, b, t):
    return a + (b - a) * t
