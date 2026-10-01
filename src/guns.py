from dataclasses import dataclass


@dataclass(frozen=True)
class Gun:
    name: str
    fire_rate: float
    bullets: int
    fire_mode: str
    damage: int
    angle_offsets: tuple = (0.0,)

    @property
    def cooldown(self):
        return 1.0 / self.fire_rate


PISTOL = Gun("Pistola", 5.0, 1, "single", 10)
SMG = Gun("SMG", 8.0, 1, "auto", 7)
SHOTGUN = Gun("Shotgun", 2.0, 3, "single", 15, (-0.785398, 0.0, 0.785398))
SNIPER = Gun("Sniper", 0.5, 1, "single", 30)

GUNS = (PISTOL, SMG, SHOTGUN, SNIPER)
GUN_BY_NAME = {gun.name: gun for gun in GUNS}
