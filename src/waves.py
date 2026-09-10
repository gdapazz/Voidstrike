import json
import random
from pathlib import Path

from config import ROOT_DIR, WAVE_CONFIG_PATH


class WaveSystem:
    def __init__(self):
        self.config_path = WAVE_CONFIG_PATH
        self.wave_data = self.load()
        self.current_wave = 1

    def load(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            return {"1": {"enemies": {"basic": 5}}}

    def get_wave_config(self, wave_number):
        index = str(wave_number)
        if not index in self.wave_data:
            base = {"enemies": {"basic": 8 + wave_number * 2, "fast": 2 + wave_number, "shooter": 2 + wave_number // 2}} if wave_number % 5 else {"boss": "boss_01"}
            return base
        return self.wave_data[index]

    def get_enemy_queue(self, wave_number):
        config = self.get_wave_config(wave_number)
        queue = []
        if "boss" in config:
            return queue
        enemies = config.get("enemies", {})
        for enemy_name, count in enemies.items():
            for _ in range(int(count)):
                queue.append(enemy_name)
        random.shuffle(queue)
        return queue

    def boss_for_wave(self, wave_number):
        config = self.get_wave_config(wave_number)
        if "boss" in config:
            if config["boss"] == "boss_02":
                return "boss_02"
            return "boss_01"
        return None

    def next_wave(self):
        self.current_wave += 1
        return self.current_wave

    def reset(self):
        self.current_wave = 1
