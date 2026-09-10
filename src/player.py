import math

import pygame

from config import PLAYER_BULLET_SPEED, PLAYER_DAMAGE, PLAYER_FIRE_COOLDOWN, PLAYER_INVULNERABILITY, PLAYER_MAX_HP, PLAYER_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from src.projectiles import PlayerBullet
from src.utils import get_asset_path, load_image


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 18
        self.speed = PLAYER_SPEED
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.damage = PLAYER_DAMAGE
        self.fire_cooldown = PLAYER_FIRE_COOLDOWN
        self.fire_timer = 0.0
        self.invulnerable_timer = 0.0
        self.angle = 0.0
        self.image = load_image(get_asset_path("Sprites", "Player", "player.png"), size=(48, 48))
        self.damaged_flash = 0.0

    def update(self, dt, mouse_pos, keys):
        move_x = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        move_y = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if move_x or move_y:
            length = math.hypot(move_x, move_y)
            self.x += (move_x / length) * self.speed * dt
            self.y += (move_y / length) * self.speed * dt
        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))

        self.angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)
        self.fire_timer = max(0.0, self.fire_timer - dt)
        self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
        self.damaged_flash = max(0.0, self.damaged_flash - dt)

    def shoot(self, bullets):
        if self.fire_timer > 0:
            return
        self.fire_timer = self.fire_cooldown
        bullet = PlayerBullet(self.x, self.y, self.angle)
        bullet.x += math.cos(self.angle) * 20
        bullet.y += math.sin(self.angle) * 20
        bullets.append(bullet)

    def take_damage(self, amount):
        if self.invulnerable_timer > 0:
            return False
        self.hp -= amount
        self.invulnerable_timer = PLAYER_INVULNERABILITY
        self.damaged_flash = 0.25
        return True

    def draw(self, surface):
        if self.image:
            rotated = pygame.transform.rotate(self.image, math.degrees(-self.angle) - 90)
            rect = rotated.get_rect(center=(self.x, self.y))
            surface.blit(rotated, rect)
        else:
            pygame.draw.circle(surface, (80, 180, 255), (int(self.x), int(self.y)), self.radius)
            pygame.draw.line(surface, (180, 220, 255), (self.x, self.y), (self.x + math.cos(self.angle) * 20, self.y + math.sin(self.angle) * 20), 4)

        if self.damaged_flash > 0:
            flash = pygame.Surface((self.radius * 2 + 8, self.radius * 2 + 8), pygame.SRCALPHA)
            pygame.draw.circle(flash, (255, 255, 255, 100), (self.radius + 4, self.radius + 4), self.radius + 4)
            surface.blit(flash, (self.x - self.radius - 4, self.y - self.radius - 4))
