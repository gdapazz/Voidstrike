import math

import pygame

if __package__:
    from ._bootstrap import ensure_project_root
else:
    from _bootstrap import ensure_project_root

ensure_project_root()

from config import PLAYER_BULLET_SPEED, PLAYER_DAMAGE, PLAYER_FIRE_COOLDOWN, PLAYER_INVULNERABILITY, PLAYER_MAX_HP, PLAYER_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from src.guns import PISTOL, Gun
from src.projectiles import PlayerBullet
from src.utils import get_asset_path, load_image


class Player:
    DASH_SPEED = 900
    DASH_DURATION = 0.16
    DASH_COOLDOWN = 2.00

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 18
        self.speed = PLAYER_SPEED
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.dash_direction_x = 0.0
        self.dash_direction_y = 0.0
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.guns = {PISTOL.name: PISTOL}
        self.weapon = PISTOL
        self.rapidfire_timer = 0.0
        self.flash_timer = 0.0
        self.red_cross_timer = 0.0
        self.trigger_held = False
        self.fire_timer = 0.0
        self.invulnerable_timer = 0.0
        self.angle = 0.0
        self.image = load_image(get_asset_path("Sprites", "Player", "player.png"), size=(48, 48))
        self.damaged_flash = 0.0

    def update(self, dt, mouse_pos, keys):
        move_x = int(pygame.K_d in keys or pygame.K_RIGHT in keys) - int(pygame.K_a in keys or pygame.K_LEFT in keys)
        move_y = int(pygame.K_s in keys or pygame.K_DOWN in keys) - int(pygame.K_w in keys or pygame.K_UP in keys)
        speed_multiplier = 3.0 if self.flash_timer > 0 else 1.0
        normal_dt = dt

        if self.dash_timer > 0:
            dash_dt = min(dt, self.dash_timer)
            self.x += self.dash_direction_x * self.DASH_SPEED * dash_dt
            self.y += self.dash_direction_y * self.DASH_SPEED * dash_dt
            self.dash_timer = max(0.0, self.dash_timer - dash_dt)
            self.velocity_x = self.dash_direction_x * self.speed * speed_multiplier
            self.velocity_y = self.dash_direction_y * self.speed * speed_multiplier
            normal_dt -= dash_dt

        if move_x or move_y:
            length = math.hypot(move_x, move_y)
            target_velocity_x = (move_x / length) * self.speed * speed_multiplier
            target_velocity_y = (move_y / length) * self.speed * speed_multiplier
        else:
            target_velocity_x = 0.0
            target_velocity_y = 0.0

        if normal_dt > 0:
            self.velocity_x = target_velocity_x
            self.velocity_y = target_velocity_y
            self.x += self.velocity_x * normal_dt
            self.y += self.velocity_y * normal_dt

        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))
        if self.x in (self.radius, SCREEN_WIDTH - self.radius):
            self.velocity_x = 0.0
        if self.y in (self.radius, SCREEN_HEIGHT - self.radius):
            self.velocity_y = 0.0

        self.angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)
        self.fire_timer = max(0.0, self.fire_timer - dt)
        self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
        self.damaged_flash = max(0.0, self.damaged_flash - dt)
        self.rapidfire_timer = max(0.0, self.rapidfire_timer - dt)
        self.flash_timer = max(0.0, self.flash_timer - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        if self.red_cross_timer > 0:
            previous_timer = self.red_cross_timer
            self.red_cross_timer = max(0.0, self.red_cross_timer - dt)
            self.hp = min(self.max_hp, self.hp + (5.0 * (previous_timer - self.red_cross_timer)))

    def start_dash(self, keys):
        if self.dash_cooldown > 0 or self.dash_timer > 0:
            return False

        move_x = int(pygame.K_d in keys or pygame.K_RIGHT in keys) - int(pygame.K_a in keys or pygame.K_LEFT in keys)
        move_y = int(pygame.K_s in keys or pygame.K_DOWN in keys) - int(pygame.K_w in keys or pygame.K_UP in keys)
        if move_x == 0 and move_y == 0:
            move_x = self.velocity_x
            move_y = self.velocity_y

        length = math.hypot(move_x, move_y)
        if length == 0:
            return False

        self.dash_direction_x = move_x / length
        self.dash_direction_y = move_y / length
        self.dash_timer = self.DASH_DURATION
        self.dash_cooldown = self.DASH_COOLDOWN
        return True

    def shoot(self, bullets):
        if self.weapon.fire_mode == "single" and self.trigger_held and self.rapidfire_timer <= 0:
            return False
        if self.fire_timer > 0:
            return False
        fire_rate_multiplier = 2.0 if self.rapidfire_timer > 0 else 1.0
        self.fire_timer = self.weapon.cooldown / fire_rate_multiplier
        for offset in self.weapon.angle_offsets:
            shot_angle = self.angle + offset
            bullet = PlayerBullet(self.x, self.y, shot_angle, damage=self.weapon.damage)
            bullet.x += math.cos(shot_angle) * 20
            bullet.y += math.sin(shot_angle) * 20
            bullets.append(bullet)
        self.trigger_held = True
        return True

    def release_trigger(self):
        self.trigger_held = False

    def unlock_gun(self, gun: Gun):
        if gun.name in self.guns:
            return False
        self.guns[gun.name] = gun
        self.weapon = gun
        return True

    def equip_gun(self, gun_name):
        if gun_name in self.guns:
            self.weapon = self.guns[gun_name]
            return True
        return False

    def apply_powerup(self, powerup):
        if powerup.kind == "rapidfire":
            self.rapidfire_timer = powerup.duration
        elif powerup.kind == "flash":
            self.flash_timer = powerup.duration
        elif powerup.kind == "red_cross":
            self.red_cross_timer = powerup.duration
        elif powerup.kind == "salvation":
            self.max_hp *= 1.5
            self.hp = min(self.hp, self.max_hp)
        elif powerup.kind == "weapon":
            from src.guns import GUN_BY_NAME
            self.unlock_gun(GUN_BY_NAME[powerup.weapon_name])

    def take_damage(self, amount):
        if self.invulnerable_timer > 0:
            return False
        self.hp -= amount
        self.invulnerable_timer = PLAYER_INVULNERABILITY
        self.damaged_flash = 0.25
        return True

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

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
