import math

import pygame

from config import ROOT_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class Button:
    def __init__(self, x, y, w, h, text, callback, text_color=(255, 255, 255), bg_color=(27, 33, 60), hover_color=(44, 69, 102), outline=(90, 130, 255), text_only=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.outline = outline
        self.text_only = text_only

    def draw(self, surface, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        if not self.text_only:
            color = self.hover_color if hovered else self.bg_color
            pygame.draw.rect(surface, color, self.rect, border_radius=12)
            pygame.draw.rect(surface, self.outline, self.rect, 2, border_radius=12)
        font_size = 36 if self.text_only else 28
        if self.text_only and hovered:
            font_size = int(font_size * 1.5)
        font = pygame.font.SysFont("arial", font_size, bold=True)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(midleft=self.rect.midleft) if self.text_only else text.get_rect(center=self.rect.center)
        if self.text_only:
            shadow = font.render(self.text, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(midleft=(self.rect.left + 3, self.rect.centery + 3))
            surface.blit(shadow, shadow_rect)
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
        self.menu_background = self._load_menu_background()

    def _load_menu_background(self):
        candidates = (
            ROOT_DIR / "Sprites" / "Menu" / "Main menu Wallpaper.png",
            ROOT_DIR / "Main menu Wallpaper.png",
            ROOT_DIR / "Main menu Wallpaper.jpg",
            ROOT_DIR / "Sprites" / "Main menu Wallpaper.png",
            ROOT_DIR / "Sprites" / "Main menu Wallpaper.jpg",
            ROOT_DIR / "Sprites" / "Main_menu_Wallpaper.png",
            ROOT_DIR / "Sprites" / "main_menu_wallpaper.png",
        )
        for path in candidates:
            if path.exists():
                try:
                    return pygame.image.load(str(path)).convert()
                except pygame.error:
                    pass
        return None

    def draw_menu_background(self, surface):
        if self.menu_background:
            image_ratio = self.menu_background.get_width() / self.menu_background.get_height()
            screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
            if image_ratio > screen_ratio:
                height = SCREEN_HEIGHT
                width = int(height * image_ratio)
            else:
                width = SCREEN_WIDTH
                height = int(width / image_ratio)
            scaled = pygame.transform.smoothscale(self.menu_background, (width, height))
            rect = scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(scaled, rect)
        else:
            surface.fill((8, 12, 22))

        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 35))
        surface.blit(shade, (0, 0))

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

        score_text = self.font.render(f"{self.game.text('score')}: {self.game.score}", True, (255, 255, 255))
        surface.blit(score_text, (SCREEN_WIDTH - 180, 20))

        wave_text = self.font.render(f"{self.game.text('wave')}: {self.game.wave_number}", True, (255, 255, 255))
        surface.blit(wave_text, (SCREEN_WIDTH // 2 - 60, 20))

        remaining = self.game.enemies_remaining()
        enemies_text = self.font.render(f"{self.game.text('enemies')}: {remaining}", True, (255, 255, 255))
        surface.blit(enemies_text, (SCREEN_WIDTH - 200, 52))

        weapon_text = self.font.render(
            f"{self.game.text('weapon')}: {player.weapon.name} | {self.game.text('damage')}: {player.weapon.damage}",
            True,
            (255, 230, 140),
        )
        surface.blit(weapon_text, (20, SCREEN_HEIGHT - 38))

        effect_text = []
        if player.rapidfire_timer > 0:
            effect_text.append(f"Rapidfire {player.rapidfire_timer:.1f}s")
        if player.flash_timer > 0:
            effect_text.append(f"The Flash {player.flash_timer:.1f}s")
        if player.red_cross_timer > 0:
            effect_text.append(f"Red Cross {player.red_cross_timer:.1f}s")
        if effect_text:
            effects = self.small_font.render(" | ".join(effect_text), True, (150, 255, 170))
            surface.blit(effects, (20, SCREEN_HEIGHT - 64))

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

    def draw_menu(self, surface, title=None):
        self.draw_menu_background(surface)
        if title is None:
            return
        title_font = pygame.font.SysFont("arial", 68, bold=True)
        title_text = title_font.render(title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        shadow = title_font.render(title, True, (0, 0, 0))
        surface.blit(shadow, shadow.get_rect(center=(title_rect.centerx + 4, title_rect.centery + 4)))
        surface.blit(title_text, title_rect)

    def draw_tutorial(self, surface):
        self.draw_menu_background(surface)
        title = pygame.font.SysFont("arial", 58, bold=True).render(self.game.text("tutorial"), True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 90)))
        panel = pygame.Surface((650, 430), pygame.SRCALPHA)
        panel.fill((5, 10, 25, 205))
        surface.blit(panel, panel.get_rect(center=(SCREEN_WIDTH // 2, 375)))
        lines = (
            (self.game.text("movement"), self.game.text("move_help")),
            (self.game.text("aim"), self.game.text("aim_help")),
            (self.game.text("shooting"), self.game.text("shoot_help")),
            (self.game.text("weapons"), self.game.text("weapons_help")),
            (self.game.text("powerups"), self.game.text("powerups_help")),
            (self.game.text("pause"), self.game.text("pause_help")),
        )
        for index, (heading, detail) in enumerate(lines):
            y = 190 + index * 52
            heading_text = self.font.render(heading, True, (255, 220, 120))
            detail_text = self.font.render(detail, True, (255, 255, 255))
            surface.blit(heading_text, (350, y))
            surface.blit(detail_text, (560, y))

    def draw_pause_overlay(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 18, 180))
        surface.blit(overlay, (0, 0))
        pause_title = self.big_font.render(self.game.text("paused"), True, (255, 255, 255))
        surface.blit(pause_title, pause_title.get_rect(center=(SCREEN_WIDTH // 2, 220)))

    def draw_powerup_choices(self, surface, choices):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 22, 235))
        surface.blit(overlay, (0, 0))
        title = self.big_font.render(self.game.text("choose_powerup"), True, (255, 230, 140))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 110)))
        for index, choice in enumerate(choices):
            rect = pygame.Rect(90 + index * 390, 220, 350, 220)
            color = (44, 69, 102) if rect.collidepoint(self.game.mouse_pos) else (27, 33, 60)
            pygame.draw.rect(surface, color, rect, border_radius=12)
            pygame.draw.rect(surface, (120, 180, 255), rect, 2, border_radius=12)
            name = self.font.render(choice.name, True, (255, 255, 255))
            surface.blit(name, name.get_rect(center=(rect.centerx, rect.y + 55)))
            lines = [choice.description[i:i + 29] for i in range(0, len(choice.description), 29)]
            for line_index, line in enumerate(lines):
                description = self.small_font.render(line, True, (210, 220, 240))
                surface.blit(description, description.get_rect(center=(rect.centerx, rect.y + 105 + line_index * 24)))
            prompt = self.small_font.render(f"{index + 1} {self.game.text('choose_help')}", True, (255, 230, 140))
            surface.blit(prompt, prompt.get_rect(center=(rect.centerx, rect.bottom - 28)))

    def draw_game_over(self, surface, score, wave):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 9, 14, 220))
        surface.blit(overlay, (0, 0))
        title = self.big_font.render(self.game.text("game_over"), True, (255, 100, 100))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 180)))
        score_text = self.font.render(f"{self.game.text('final_score')}: {score}", True, (255, 255, 255))
        surface.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 250)))
        wave_text = self.font.render(f"{self.game.text('wave_reached')}: {wave}", True, (255, 255, 255))
        surface.blit(wave_text, wave_text.get_rect(center=(SCREEN_WIDTH // 2, 290)))

    def draw_settings_values(self, surface):
        music_text = self.font.render(
            f"{self.game.text('music_volume')}: {self.game.settings.music_volume:.2f}",
            True,
            (255, 255, 255),
        )
        sfx_text = self.font.render(
            f"{self.game.text('sfx_volume')}: {self.game.settings.sfx_volume:.2f}",
            True,
            (255, 255, 255),
        )
        surface.blit(music_text, (580, 230))
        surface.blit(sfx_text, (580, 310))

    def draw_boss_alert(self, surface, text):
        if not text:
            return
        label = self.big_font.render(text, True, (255, 215, 120))
        rect = label.get_rect(center=(SCREEN_WIDTH // 2, 120))
        alpha = max(0, 255 - ((pygame.time.get_ticks() - self.game.boss_alert_start) / 1000) * 255)
        label.set_alpha(max(0, int(alpha)))
        surface.blit(label, rect)
