from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Voidstrike"

PLAYER_SPEED = 340
PLAYER_MAX_HP = 100
PLAYER_DAMAGE = 20
PLAYER_FIRE_COOLDOWN = 0.18
PLAYER_BULLET_SPEED = 760
PLAYER_BULLET_RADIUS = 4
PLAYER_INVULNERABILITY = 0.7

ENEMY_SPAWN_MARGIN = 140
MAX_STAR_COUNT = 140

DEFAULT_SETTINGS = {
    "music_volume": 0.55,
    "sfx_volume": 0.75,
    "fullscreen": False,
}

WAVE_CONFIG_PATH = ROOT_DIR / "data" / "waves.json"
SETTINGS_PATH = ROOT_DIR / "data" / "settings.json"
