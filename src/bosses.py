import math
import random

import pygame

from src.projectiles import EnemyBullet
from src.utils import get_asset_path, load_image


class Boss:
    def __init__(self, name, x, y, max_hp, image_name):
        self.name = name
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
        self.radius = 70
        self.speed = 70
        self.fire_timer = 0.8
        self.phase = 1
        self.image = load_image(get_asset_path("Sprites", "Bosses", image_name), size=(180, 180))
        self.alive = True
        self.start_timer = 0.0
        self.entering = True

    def update(self, dt, player, bullets):
        if not self.alive:
            return
        self.fire_timer -= dt
        self.start_timer += dt

        if player is not None:
            dx = player.x - self.x
            dy = player.y - self.y
            dist = max(1, math.hypot(dx, dy))
            if dist > 180:
                self.x += (dx / dist) * self.speed * dt
                self.y += (dy / dist) * self.speed * dt
            else:
                self.x -= (dx / dist) * self.speed * dt * 0.25
                self.y -= (dy / dist) * self.speed * dt * 0.25

        if self.hp < self.max_hp * 0.6:
            self.phase = 2
        if self.hp < self.max_hp * 0.3:
            self.phase = 3

        if self.fire_timer <= 0:
            if self.phase == 1:
                self.attack_phase_one(bullets, player)
            elif self.phase == 2:
                self.attack_phase_two(bullets, player)
            else:
                self.attack_phase_three(bullets, player)
            self.fire_timer = 1.2 if self.phase == 1 else 0.8 if self.phase == 2 else 0.52

    def attack_phase_one(self, bullets, player):
        if player is None:
            return
        for i in range(5):
            angle = math.atan2(player.y - self.y, player.x - self.x) + (i - 2) * 0.22
            bullets.append(EnemyBullet(self.x, self.y, angle, speed=260, damage=12))

    def attack_phase_two(self, bullets, player):
        if player is None:
            return
        for i in range(8):
            angle = (i / 8) * math.tau + (self.start_timer * 0.8)
            bullets.append(EnemyBullet(self.x, self.y, angle, speed=300, damage=14))

    def attack_phase_three(self, bullets, player):
        if player is None:
            return
        for i in range(12):
            angle = math.atan2(player.y - self.y, player.x - self.x) + (i - 6) * 0.18
            bullets.append(EnemyBullet(self.x, self.y, angle, speed=350, damage=16))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def draw(self, surface):
        if self.image:
            rotated = pygame.transform.rotate(self.image, math.degrees(self.start_timer * 0.8))
            rect = rotated.get_rect(center=(self.x, self.y))
            surface.blit(rotated, rect)
        else:
            pygame.draw.circle(surface, (200, 80, 90), (int(self.x), int(self.y)), self.radius)


class BossOne(Boss):
    def __init__(self, x, y):
        super().__init__("Boss: Vanguard", x, y, 400, "boss_01.png")


class BossTwo(Boss):
    def __init__(self, x, y):
        super().__init__("Boss: Eclipse", x, y, 520, "boss_02.png")
