import math
import random

import pygame

from config import ENEMY_SPAWN_MARGIN, SCREEN_HEIGHT, SCREEN_WIDTH
from src.projectiles import EnemyBullet
from src.utils import angle_to, get_asset_path, load_image, normalize


class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.name = "Enemy"
        self.radius = 16
        self.speed = 90
        self.max_hp = 30
        self.hp = self.max_hp
        self.damage = 10
        self.fire_cooldown = 2.0
        self.fire_timer = random.uniform(0.5, 1.5)
        self.color = (255, 120, 120)
        self.image = None
        self.alive = True
        self.invulnerable = 0.0
        self.is_boss = False

    def update(self, dt, player, bullets):
        if not self.alive:
            return
        self.fire_timer -= dt
        self.invulnerable = max(0.0, self.invulnerable - dt)

    def draw(self, surface):
        if self.image:
            rect = self.image.get_rect(center=(self.x, self.y))
            surface.blit(self.image, rect)
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def take_damage(self, amount):
        if self.invulnerable > 0:
            return False
        self.hp -= amount
        self.invulnerable = 0.12
        if self.hp <= 0:
            self.alive = False
        return True


class BasicEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "basic")
        self.name = "Basic Enemy"
        self.radius = 16
        self.speed = 90
        self.max_hp = 35
        self.hp = self.max_hp
        self.damage = 10
        self.color = (255, 140, 140)
        self.image = load_image(get_asset_path("Sprites", "Inimigos", "basic_enemy.png"), size=(32, 32))

    def update(self, dt, player, bullets):
        super().update(dt, player, bullets)
        if player is None:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += (dx / dist) * self.speed * dt
        self.y += (dy / dist) * self.speed * dt


class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "fast")
        self.name = "Fast Enemy"
        self.radius = 12
        self.speed = 180
        self.max_hp = 20
        self.hp = self.max_hp
        self.damage = 8
        self.color = (255, 210, 90)
        self.image = load_image(get_asset_path("Sprites", "Inimigos", "fast_enemy.png"), size=(26, 26))

    def update(self, dt, player, bullets):
        super().update(dt, player, bullets)
        if player is None:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += (dx / dist) * self.speed * dt
        self.y += (dy / dist) * self.speed * dt


class ShooterEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "shooter")
        self.name = "Shooter Enemy"
        self.radius = 18
        self.speed = 78
        self.max_hp = 55
        self.hp = self.max_hp
        self.damage = 12
        self.color = (150, 130, 255)
        self.image = load_image(get_asset_path("Sprites", "Inimigos", "shooter_enemy.png"), size=(34, 34))

    def update(self, dt, player, bullets):
        super().update(dt, player, bullets)
        if player is None:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1, math.hypot(dx, dy))
        desired_distance = 220
        if dist < desired_distance:
            self.x -= (dx / dist) * self.speed * dt * 0.8
            self.y -= (dy / dist) * self.speed * dt * 0.8
        elif dist > desired_distance + 40:
            self.x += (dx / dist) * self.speed * dt * 0.6
            self.y += (dy / dist) * self.speed * dt * 0.6

        if self.fire_timer <= 0:
            angle = math.atan2(player.y - self.y, player.x - self.x)
            bullets.append(EnemyBullet(self.x, self.y, angle, speed=250, damage=9))
            self.fire_timer = 2.0


class TankEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "tank")
        self.name = "Tank Enemy"
        self.radius = 28
        self.speed = 55
        self.max_hp = 120
        self.hp = self.max_hp
        self.damage = 18
        self.color = (130, 180, 160)
        self.image = load_image(get_asset_path("Sprites", "Inimigos", "tank_enemy.png"), size=(52, 52))

    def update(self, dt, player, bullets):
        super().update(dt, player, bullets)
        if player is None:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += (dx / dist) * self.speed * dt * 0.65
        self.y += (dy / dist) * self.speed * dt * 0.65


class EliteEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "elite")
        self.name = "Elite Enemy"
        self.radius = 22
        self.speed = 130
        self.max_hp = 90
        self.hp = self.max_hp
        self.damage = 16
        self.color = (190, 100, 210)
        self.image = load_image(get_asset_path("Sprites", "Inimigos", "elite_enemy.png"), size=(42, 42))

    def update(self, dt, player, bullets):
        super().update(dt, player, bullets)
        if player is None:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += (dx / dist) * self.speed * dt
        self.y += (dy / dist) * self.speed * dt
        if self.fire_timer <= 0:
            for offset in (-0.4, 0, 0.4):
                angle = math.atan2(player.y - self.y, player.x - self.x) + offset
                bullets.append(EnemyBullet(self.x, self.y, angle, speed=280, damage=12))
            self.fire_timer = 1.6


def enemy_from_type(enemy_type, x, y):
    mapping = {
        "basic": BasicEnemy,
        "fast": FastEnemy,
        "shooter": ShooterEnemy,
        "tank": TankEnemy,
        "elite": EliteEnemy,
    }
    enemy_cls = mapping.get(enemy_type, BasicEnemy)
    return enemy_cls(x, y)
