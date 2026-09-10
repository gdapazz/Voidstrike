import math
import os
import random
import sys

import pygame

from config import DEFAULT_SETTINGS, FPS, ROOT_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from src.audio import AudioManager
from src.bosses import BossOne, BossTwo
from src.enemies import enemy_from_type
from src.particles import ParticleSystem
from src.player import Player
from src.settings import SettingsManager
from src.ui import Button, UI
from src.utils import get_asset_path, load_image
from src.waves import WaveSystem


class Game:
    def __init__(self, smoke_test=False):
        self.smoke_test = smoke_test
        if smoke_test:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error as exc:
            print(f"[Audio] Mixer indisponivel; efeitos e musica serao ignorados: {exc}")

        self.smoke_test = smoke_test
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.dt = 0.0

        self.settings = SettingsManager()
        self.audio = AudioManager()
        self.audio.set_volume(self.settings.music_volume, self.settings.sfx_volume)

        self.wave_system = WaveSystem()
        self.ui = UI(self)
        self.particles = ParticleSystem()
        self.score = 0
        self.wave_number = 1
        self.current_boss = None
        self.boss_alert_start = 0

        self.player = None
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.stars = [
            {
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "size": random.randint(1, 3),
                "speed": random.uniform(12, 80),
                "alpha": random.randint(80, 255),
            }
            for _ in range(160)
        ]

        self.menu_buttons = [
            Button(560, 260, 180, 52, "PLAY", self.start_game),
            Button(560, 330, 180, 52, "SETTINGS", self.show_settings),
            Button(560, 400, 180, 52, "QUIT", self.quit_game),
        ]

        self.pause_buttons = [
            Button(560, 260, 180, 52, "RESUME", self.resume_game),
            Button(560, 330, 180, 52, "SETTINGS", self.show_settings),
            Button(560, 400, 180, 52, "MAIN MENU", self.return_to_menu),
        ]

        self.game_over_buttons = [
            Button(500, 360, 220, 52, "RESTART", self.start_game),
            Button(560, 430, 180, 52, "MENU", self.return_to_menu),
        ]

        self.settings_buttons = [
            Button(500, 220, 220, 52, "MUSIC +", lambda: self.adjust_music(0.1)),
            Button(760, 220, 220, 52, "MUSIC -", lambda: self.adjust_music(-0.1)),
            Button(500, 310, 220, 52, "SFX +", lambda: self.adjust_sfx(0.1)),
            Button(760, 310, 220, 52, "SFX -", lambda: self.adjust_sfx(-0.1)),
            Button(500, 400, 220, 52, "FULLSCREEN", self.toggle_fullscreen),
            Button(760, 400, 220, 52, "BACK", self.back_from_settings),
        ]

        self.settings_state = None
        self.wave_delay = 0.0
        self.wave_spawn_queue = []
        self.wave_started = False
        self.boss_wave = False
        self.wave_intro_timer = 0.0
        self.current_wave_label = ""

        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_down = False

    def reset_run(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.current_boss = None
        self.score = 0
        self.wave_number = 1
        self.wave_spawn_queue = self.wave_system.get_enemy_queue(self.wave_number)
        self.wave_delay = 1.0
        self.wave_started = False
        self.wave_intro_timer = 1.4
        self.current_wave_label = "Wave 1"
        self.boss_wave = False

    def start_game(self):
        self.reset_run()
        self.state = "playing"
        self.audio.start_music()

    def resume_game(self):
        self.state = "playing"

    def return_to_menu(self):
        self.state = "menu"
        self.audio.stop_music()
        self.player = None

    def quit_game(self):
        self.running = False

    def show_settings(self):
        self.settings_state = self.state
        self.state = "settings"

    def back_from_settings(self):
        self.state = self.settings_state or "menu"
        self.settings_state = None

    def toggle_fullscreen(self):
        self.settings.fullscreen = not self.settings.fullscreen
        flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

    def adjust_music(self, amount):
        value = max(0.0, min(1.0, self.settings.music_volume + amount))
        self.settings.music_volume = value
        self.audio.set_volume(value, self.settings.sfx_volume)

    def adjust_sfx(self, amount):
        value = max(0.0, min(1.0, self.settings.sfx_volume + amount))
        self.settings.sfx_volume = value
        self.audio.set_volume(self.settings.music_volume, value)

    def spawn_enemy(self, enemy_type):
        margin = 140
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x = random.randint(0, SCREEN_WIDTH)
            y = -margin
        elif edge == "bottom":
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + margin
        elif edge == "left":
            x = -margin
            y = random.randint(0, SCREEN_HEIGHT)
        else:
            x = SCREEN_WIDTH + margin
            y = random.randint(0, SCREEN_HEIGHT)

        enemy = enemy_from_type(enemy_type, x, y)
        self.enemies.append(enemy)

    def spawn_boss(self, boss_name):
        if boss_name == "boss_02":
            boss = BossTwo(SCREEN_WIDTH // 2, -120)
        else:
            boss = BossOne(SCREEN_WIDTH // 2, -120)
        self.current_boss = boss
        self.boss_wave = True
        self.boss_alert_start = pygame.time.get_ticks()
        self.current_wave_label = boss.name

    def start_next_wave(self):
        self.wave_number += 1
        self.wave_started = False
        self.wave_delay = 1.8
        self.wave_spawn_queue = self.wave_system.get_enemy_queue(self.wave_number)
        self.current_wave_label = f"Wave {self.wave_number}"
        self.boss_wave = False
        self.current_boss = None

    def begin_wave(self):
        if self.state != "playing":
            return

        boss_name = self.wave_system.boss_for_wave(self.wave_number)
        if boss_name:
            self.spawn_boss(boss_name)
            self.boss_wave = True
            self.wave_started = True
            self.wave_delay = 0.0
            return

        self.wave_spawn_queue = self.wave_system.get_enemy_queue(self.wave_number)
        self.wave_started = True
        self.wave_delay = 0.0

    def advance_wave(self):
        if self.current_boss and self.current_boss.alive:
            return
        if self.current_boss and not self.current_boss.alive:
            self.current_boss = None
            self.score += 250
        if self.enemies:
            return
        if len(self.player_bullets) == 0 and len(self.enemy_bullets) == 0 and not self.boss_wave:
            self.start_next_wave()
            self.begin_wave()
        elif not self.wave_started and not self.boss_wave:
            self.begin_wave()

    def enemies_remaining(self):
        active = len(self.enemies)
        if self.current_boss is not None and self.current_boss.alive:
            active += 1
        return active

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
                if self.state == "menu":
                    for btn in self.menu_buttons:
                        btn.handle_click(self.mouse_pos, True)
                elif self.state == "pause":
                    for btn in self.pause_buttons:
                        btn.handle_click(self.mouse_pos, True)
                elif self.state == "game_over":
                    for btn in self.game_over_buttons:
                        btn.handle_click(self.mouse_pos, True)
                elif self.state == "settings":
                    for btn in self.settings_buttons:
                        btn.handle_click(self.mouse_pos, True)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state == "playing":
                    self.state = "pause"
                elif self.state == "pause":
                    self.state = "playing"

        self.mouse_pos = pygame.mouse.get_pos()
        if self.state == "playing":
            if self.player is not None and self.mouse_down:
                if self.player.shoot(self.player_bullets):
                    self.audio.play_sfx("GunshotSoundEffect.mp3")

    def update(self):
        self.dt = self.clock.tick(FPS) / 1000.0
        self.handle_input()

        if self.state == "menu":
            return
        if self.state == "settings":
            return
        if self.state == "game_over":
            return
        if self.state == "pause":
            return

        for star in self.stars:
            star["y"] += star["speed"] * self.dt
            if star["y"] > SCREEN_HEIGHT:
                star["y"] = -5
                star["x"] = random.randint(0, SCREEN_WIDTH)

        self.particles.update(self.dt)

        if self.player is not None:
            self.player.update(self.dt, self.mouse_pos, pygame.key.get_pressed())
            if self.mouse_down:
                if self.player.shoot(self.player_bullets):
                    self.audio.play_sfx("GunshotSoundEffect.mp3")

        if self.current_boss is not None and self.current_boss.alive:
            self.current_boss.update(self.dt, self.player, self.enemy_bullets)

        if not self.wave_started and self.wave_delay <= 0:
            self.begin_wave()
        elif self.wave_delay > 0:
            self.wave_delay -= self.dt

        if self.wave_started and not self.boss_wave and self.wave_spawn_queue:
            if len(self.enemies) < 7:
                self.spawn_enemy(self.wave_spawn_queue.pop(0))

        for enemy in list(self.enemies):
            enemy.update(self.dt, self.player, self.enemy_bullets)
            if not enemy.alive:
                self.score += 25
                self.particles.add_explosion(enemy.x, enemy.y, (255, 150, 120), 18)
                self.enemies.remove(enemy)
                continue

            if self.player is not None:
                if math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < enemy.radius + self.player.radius:
                    if self.player.take_damage(enemy.damage):
                        self.particles.add_hit(self.player.x, self.player.y, (255, 255, 255), 14)

        for bullet in list(self.player_bullets):
            bullet.update(self.dt)
            if not bullet.active:
                self.player_bullets.remove(bullet)
                continue

            for enemy in list(self.enemies):
                if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) < bullet.radius + enemy.radius:
                    if enemy.take_damage(bullet.damage):
                        bullet.active = False
                        self.particles.add_hit(enemy.x, enemy.y, (170, 220, 255), 10)
                        if not enemy.alive:
                            self.score += 30
                            self.particles.add_explosion(enemy.x, enemy.y, (255, 160, 100), 20)
                    break

            if bullet.active and self.current_boss is not None and self.current_boss.alive:
                if math.hypot(bullet.x - self.current_boss.x, bullet.y - self.current_boss.y) < bullet.radius + self.current_boss.radius:
                    self.current_boss.take_damage(bullet.damage)
                    bullet.active = False
                    self.particles.add_hit(self.current_boss.x, self.current_boss.y, (255, 160, 180), 12)
                    if not self.current_boss.alive:
                        self.score += 500
                        self.particles.add_explosion(self.current_boss.x, self.current_boss.y, (250, 120, 120), 60)

        for bullet in list(self.enemy_bullets):
            bullet.update(self.dt)
            if not bullet.active:
                self.enemy_bullets.remove(bullet)
                continue
            if self.player is not None and math.hypot(bullet.x - self.player.x, bullet.y - self.player.y) < bullet.radius + self.player.radius:
                if self.player.take_damage(bullet.damage):
                    self.particles.add_hit(self.player.x, self.player.y, (255, 120, 120), 15)
                bullet.active = False

        if self.current_boss is not None and self.current_boss.alive:
            if self.current_boss.hp <= 0:
                self.current_boss.alive = False
                self.score += 500
                self.current_boss = None
                self.boss_wave = False
                self.state = "playing"

        if self.current_boss is not None and not self.current_boss.alive:
            self.current_boss = None
            self.boss_wave = False

        if self.player is not None and self.player.hp <= 0:
            self.player.hp = 0
            self.state = "game_over"
            self.audio.stop_music()
            self.audio.play_sfx("GameOverSoundEffect.mp3")

        if self.current_boss is None and not self.boss_wave and self.wave_started and not self.wave_spawn_queue and len(self.enemies) == 0:
            self.wave_number += 1
            self.wave_started = False
            self.wave_delay = 2.0
            self.current_wave_label = f"Wave {self.wave_number}"

    def draw(self):
        self.screen.fill((8, 10, 18))

        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255, star["alpha"]), (int(star["x"]), int(star["y"])), star["size"])

        if self.state == "menu":
            self.ui.draw_menu(self.screen)
            for btn in self.menu_buttons:
                btn.draw(self.screen, self.mouse_pos)
        elif self.state == "settings":
            self.ui.draw_menu(self.screen, "SETTINGS")
            for btn in self.settings_buttons:
                btn.draw(self.screen, self.mouse_pos)
            volume_text = self.ui.font.render(f"Music Volume: {self.settings.music_volume:.2f}", True, (255, 255, 255))
            sfx_text = self.ui.font.render(f"SFX Volume: {self.settings.sfx_volume:.2f}", True, (255, 255, 255))
            self.screen.blit(volume_text, (520, 170))
            self.screen.blit(sfx_text, (520, 260))
        elif self.state == "pause":
            self.ui.draw_pause_overlay(self.screen)
            for btn in self.pause_buttons:
                btn.draw(self.screen, self.mouse_pos)
        elif self.state == "game_over":
            self.ui.draw_game_over(self.screen, self.score, self.wave_number)
            for btn in self.game_over_buttons:
                btn.draw(self.screen, self.mouse_pos)
        else:
            if self.player is not None:
                self.player.draw(self.screen)

            for bullet in self.player_bullets:
                bullet.draw(self.screen)
            for bullet in self.enemy_bullets:
                bullet.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)

            if self.current_boss is not None:
                self.current_boss.draw(self.screen)

            self.particles.draw(self.screen)
            self.ui.draw_hud(self.screen)

            if self.current_boss is not None and self.current_boss.alive:
                self.ui.draw_boss_alert(self.screen, self.current_boss.name)

            wave_text = self.ui.font.render(self.current_wave_label, True, (255, 230, 140))
            self.screen.blit(wave_text, (SCREEN_WIDTH // 2 - 60, 50))

        pygame.display.flip()

    def run(self):
        if self.smoke_test:
            self.start_game()
            for _ in range(30):
                self.update()
                self.draw()
            print("[Smoke test] Voidstrike startup validated successfully.")
            pygame.quit()
            return

        while self.running:
            self.update()
            self.draw()
        pygame.quit()
        sys.exit(0)
