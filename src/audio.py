import os
import random
import sys
from pathlib import Path

import pygame

if __package__:
    from ._bootstrap import ensure_project_root
else:
    from _bootstrap import ensure_project_root

ensure_project_root()

from config import DEFAULT_SETTINGS, ROOT_DIR


class AudioManager:
    def __init__(self):
        self.music_directory = ROOT_DIR / "Music" / "PlayMusic"
        self.music_path = None
        self.music_volume = DEFAULT_SETTINGS["music_volume"]
        self.sfx_volume = DEFAULT_SETTINGS["sfx_volume"]
        self.music_started = False
        self.music_paused = False
        self.music_channel = None
        self.last_error = None
        self.track_sequence = 0
        self.current_track_name = ""

    def set_volume(self, music_volume=None, sfx_volume=None):
        if music_volume is not None:
            self.music_volume = music_volume
        if sfx_volume is not None:
            self.sfx_volume = sfx_volume
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.set_volume(self.music_volume)

    def start_music(self):
        if pygame.mixer.get_init() is None:
            return
        music_files = sorted(
            path for path in self.music_directory.iterdir()
            if path.is_file() and path.suffix.lower() in {".mp3", ".ogg", ".wav"}
        ) if self.music_directory.exists() else []
        if not music_files:
            print("[Audio] Nenhuma música encontrada em Music/PlayMusic")
            return

        available_files = [path for path in music_files if path != self.music_path]
        next_track = random.choice(available_files or music_files)
        try:
            pygame.mixer.music.load(str(next_track))
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play()
            self.music_path = next_track
            self.music_started = True
            self.music_paused = False
            self.track_sequence += 1
            self.current_track_name = next_track.stem.replace("_", " ").replace("-", " ").strip()
        except Exception as exc:  # pragma: no cover - runtime validation
            self.last_error = exc
            print(f"[Audio] Não foi possível carregar a música: {exc}")

    def update_music(self):
        if self.music_started and not self.music_paused and pygame.mixer.get_init() is not None and not pygame.mixer.music.get_busy():
            self.start_music()

    def pause_music(self):
        if self.music_started and not self.music_paused and pygame.mixer.get_init() is not None:
            pygame.mixer.music.pause()
            self.music_paused = True

    def resume_music(self):
        if self.music_started and self.music_paused and pygame.mixer.get_init() is not None:
            pygame.mixer.music.unpause()
            self.music_paused = False

    def stop_music(self):
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()
        self.music_started = False
        self.music_paused = False

    def play_sfx(self, path, loops=0):
        if pygame.mixer.get_init() is None:
            return None
        sound_path = ROOT_DIR / "Sons" / path
        if not sound_path.exists():
            return None
        try:
            sound = pygame.mixer.Sound(str(sound_path))
            sound.set_volume(self.sfx_volume)
            sound.play(loops=loops)
            return sound
        except Exception as exc:
            print(f"[Audio] Falha ao tocar efeito sonoro {path}: {exc}")
            return None
