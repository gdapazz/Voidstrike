from dataclasses import dataclass

from src.guns import GUNS


@dataclass(frozen=True)
class Powerup:
    name: str
    description: str
    kind: str
    duration: float = 0.0
    weapon_name: str = ""


POWERUPS = (
    Powerup("Rapidfire", "Firerate x2 e auto fire por 15s", "rapidfire", 15.0),
    Powerup("The Flash", "Velocidade de movimento x3 por 25s", "flash", 25.0),
    Powerup("Red Cross", "Recupera 5 HP por segundo durante 15s", "red_cross", 15.0),
    Powerup("Salvation", "Aumenta a vida total em 50% permanentemente", "salvation"),
    *(Powerup(gun.name, f"Desbloqueia a {gun.name}", "weapon", weapon_name=gun.name) for gun in GUNS[1:]),
)

WEAPON_POWERUPS = tuple(powerup for powerup in POWERUPS if powerup.kind == "weapon")
