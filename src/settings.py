import json
from pathlib import Path

from config import DEFAULT_SETTINGS, SETTINGS_PATH


class SettingsManager:
    def __init__(self, path=SETTINGS_PATH):
        self.path = Path(path)
        self.settings = dict(DEFAULT_SETTINGS)
        self.load()

    def load(self):
        if not self.path.exists():
            self.save()
            return
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            self.settings.update(loaded)
        except Exception:
            self.settings = dict(DEFAULT_SETTINGS)
            self.save()

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(self.settings, handle, indent=2)

    def update(self, **kwargs):
        self.settings.update(kwargs)
        self.save()

    @property
    def music_volume(self):
        return self.settings.get("music_volume", DEFAULT_SETTINGS["music_volume"])

    @music_volume.setter
    def music_volume(self, value):
        self.settings["music_volume"] = value
        self.save()

    @property
    def sfx_volume(self):
        return self.settings.get("sfx_volume", DEFAULT_SETTINGS["sfx_volume"])

    @sfx_volume.setter
    def sfx_volume(self, value):
        self.settings["sfx_volume"] = value
        self.save()

    @property
    def fullscreen(self):
        return self.settings.get("fullscreen", DEFAULT_SETTINGS["fullscreen"])

    @fullscreen.setter
    def fullscreen(self, value):
        self.settings["fullscreen"] = value
        self.save()
