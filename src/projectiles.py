import math

import pygame

from config import ROOT_DIR
from src.utils import get_asset_path, load_image


class Projectile:
    def __init__(self, x, y, angle, speed, damage, owner, radius=5, color=(255, 255, 255), image_path=None):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.owner = owner
        self.radius = radius
        self.color = color
        self.image = None
        if image_path:
            self.image = load_image(get_asset_path("Sprites", "Projectiles", image_path), size=(max(int(radius * 3), 10), max(int(radius * 3), 10)))
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.active = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < -50 or self.x > 2000 or self.y < -50 or self.y > 2000:
            self.active = False

    def draw(self, surface):
        if self.image:
            rect = self.image.get_rect(center=(self.x, self.y))
            surface.blit(self.image, rect)
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class PlayerBullet(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(
            x,
            y,
            angle,
            760,
            20,
            "player",
            radius=4,
            color=(120, 220, 255),
            image_path="player_bullet.png",
        )


class EnemyBullet(Projectile):
    def __init__(self, x, y, angle, speed=340, damage=12):
        super().__init__(
            x,
            y,
            angle,
            speed,
            damage,
            "enemy",
            radius=6,
            color=(255, 120, 120),
            image_path="enemy_bullet.png",
        )
