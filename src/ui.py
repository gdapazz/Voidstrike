import math

import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Button:
    def __init__(self, x, y, w, h, text, callback, text_color=(255, 255, 255), bg_color=(27, 33, 60), hover_color=(44, 69, 102), outline=(90, 130, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.outline = outline

    def draw(self, surface, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, self.outline, self.rect, 2, border_radius=12)
        font = pygame.font.SysFont("arial", 28, bold=True)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_click(self, mouse_pos, click):
        if click and self.rect.collidepoint(mouse_pos):
            self.callback()


class UI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("arial", 22)
        self.big_font = pygame.font.SysFont("arial", 52, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)

    def draw_hud(self, surface):
        player = self.game.player
        if not player:
            return

        hp_ratio = max(0, min(1, player.hp / player.max_hp))
        bar_width = 220
        bar_height = 18
        bar_x = 20
        bar_y = 20
        pygame.draw.rect(surface, (35, 45, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=9)
        pygame.draw.rect(surface, (80, 220, 130), (bar_x, bar_y, bar_width * hp_ratio, bar_height), border_radius=9)
        hp_text = self.font.render(f"HP: {int(player.hp)} / {int(player.max_hp)}", True, (255, 255, 255))
        surface.blit(hp_text, (bar_x, bar_y + 24))

        score_text = self.font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        surface.blit(score_text, (SCREEN_WIDTH - 180, 20))

        wave_text = self.font.render(f"Wave: {self.game.wave_number}", True, (255, 255, 255))
        surface.blit(wave_text, (SCREEN_WIDTH // 2 - 60, 20))

        remaining = self.game.enemies_remaining()
        enemies_text = self.font.render(f"Enemies: {remaining}", True, (255, 255, 255))
        surface.blit(enemies_text, (SCREEN_WIDTH - 200, 52))

        if self.game.current_boss:
            boss = self.game.current_boss
            boss_name = boss.name
            name_text = self.font.render(boss_name, True, (255, 255, 255))
            surface.blit(name_text, (SCREEN_WIDTH // 2 - 70, 60))
            boss_bar_w = 360
            boss_bar_h = 16
            boss_x = SCREEN_WIDTH // 2 - boss_bar_w // 2
            boss_y = 90
            pygame.draw.rect(surface, (35, 45, 60), (boss_x, boss_y, boss_bar_w, boss_bar_h), border_radius=8)
            pygame.draw.rect(surface, (220, 65, 65), (boss_x, boss_y, boss_bar_w * max(0, min(1, boss.hp / boss.max_hp)), boss_bar_h), border_radius=8)

    def draw_menu(self, surface, title="VOIDSTRIKE"):
        surface.fill((8, 12, 22))
        title_text = self.big_font.render(title, True, (130, 200, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        surface.blit(title_text, title_rect)

        subtitle = self.font.render("WASD / Arrows = Move   Mouse = Aim   LMB = Shoot   ESC = Pause", True, (200, 220, 255))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 170))
        surface.blit(subtitle, subtitle_rect)

    def draw_pause_overlay(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 18, 180))
        surface.blit(overlay, (0, 0))
        pause_title = self.big_font.render("PAUSED", True, (255, 255, 255))
        surface.blit(pause_title, pause_title.get_rect(center=(SCREEN_WIDTH // 2, 220)))

    def draw_game_over(self, surface, score, wave):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 9, 14, 220))
        surface.blit(overlay, (0, 0))
        title = self.big_font.render("GAME OVER", True, (255, 100, 100))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 180)))
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        surface.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 250)))
        wave_text = self.font.render(f"Wave Reached: {wave}", True, (255, 255, 255))
        surface.blit(wave_text, wave_text.get_rect(center=(SCREEN_WIDTH // 2, 290)))

    def draw_boss_alert(self, surface, text):
        if not text:
            return
        label = self.big_font.render(text, True, (255, 215, 120))
        rect = label.get_rect(center=(SCREEN_WIDTH // 2, 120))
        alpha = max(0, 255 - ((pygame.time.get_ticks() - self.game.boss_alert_start) / 1000) * 255)
        label.set_alpha(max(0, int(alpha)))
        surface.blit(label, rect)
