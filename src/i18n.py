TRANSLATIONS = {
    "english": {
        "play": "PLAY", "settings": "SETTINGS", "tutorial": "TUTORIAL", "quit": "QUIT",
        "back": "BACK", "resume": "RESUME", "main_menu": "MAIN MENU", "restart": "RESTART",
        "menu": "MENU", "language": "LANGUAGE", "music_up": "MUSIC +", "music_down": "MUSIC -",
        "sfx_up": "SFX +", "sfx_down": "SFX -", "fullscreen": "FULLSCREEN", "paused": "PAUSED",
        "choose_powerup": "CHOOSE POWERUP", "music_volume": "Music Volume", "sfx_volume": "SFX Volume",
        "score": "Score", "wave": "Wave", "enemies": "Enemies", "weapon": "Weapon", "damage": "Damage",
        "game_over": "GAME OVER", "final_score": "Final Score", "wave_reached": "Wave Reached",
        "movement": "MOVEMENT", "aim": "AIM", "shooting": "SHOOTING", "weapons": "WEAPONS",
        "powerups": "POWERUPS", "pause": "PAUSE", "move_help": "WASD or arrow keys",
        "aim_help": "Move the mouse to aim", "shoot_help": "Hold the left mouse button to shoot",
        "weapons_help": "Use 1 to 4 to switch unlocked weapons", "powerups_help": "Choose an upgrade every 10 kills",
        "pause_help": "Press ESC to pause the game", "choose_help": "or click",
    },
    "portugues": {
        "play": "JOGAR", "settings": "CONFIGURACOES", "tutorial": "TUTORIAL", "quit": "SAIR",
        "back": "VOLTAR", "resume": "CONTINUAR", "main_menu": "MENU PRINCIPAL", "restart": "REINICIAR",
        "menu": "MENU", "language": "IDIOMA", "music_up": "MUSICA +", "music_down": "MUSICA -",
        "sfx_up": "SFX +", "sfx_down": "SFX -", "fullscreen": "TELA CHEIA", "paused": "PAUSADO",
        "choose_powerup": "ESCOLHA UM POWERUP", "music_volume": "Volume da musica", "sfx_volume": "Volume dos efeitos",
        "score": "Pontos", "wave": "Onda", "enemies": "Inimigos", "weapon": "Arma", "damage": "Dano",
        "game_over": "FIM DE JOGO", "final_score": "Pontuacao final", "wave_reached": "Onda alcancada",
        "movement": "MOVIMENTO", "aim": "MIRA", "shooting": "DISPARO", "weapons": "ARMAS",
        "powerups": "POWERUPS", "pause": "PAUSA", "move_help": "WASD ou teclas direcionais",
        "aim_help": "Mova o mouse para mirar", "shoot_help": "Segure o botao esquerdo para atirar",
        "weapons_help": "Use 1 a 4 para trocar armas desbloqueadas", "powerups_help": "Escolha uma melhoria a cada 10 mortes",
        "pause_help": "Pressione ESC para pausar o jogo", "choose_help": "ou clique",
    },
    "espanol": {
        "play": "JUGAR", "settings": "AJUSTES", "tutorial": "TUTORIAL", "quit": "SALIR",
        "back": "VOLVER", "resume": "CONTINUAR", "main_menu": "MENU PRINCIPAL", "restart": "REINICIAR",
        "menu": "MENU", "language": "IDIOMA", "music_up": "MUSICA +", "music_down": "MUSICA -",
        "sfx_up": "SFX +", "sfx_down": "SFX -", "fullscreen": "PANTALLA COMPLETA", "paused": "PAUSADO",
        "choose_powerup": "ELIGE UN POWERUP", "music_volume": "Volumen de musica", "sfx_volume": "Volumen de efectos",
        "score": "Puntuacion", "wave": "Oleada", "enemies": "Enemigos", "weapon": "Arma", "damage": "Dano",
        "game_over": "FIN DEL JUEGO", "final_score": "Puntuacion final", "wave_reached": "Oleada alcanzada",
        "movement": "MOVIMIENTO", "aim": "MIRA", "shooting": "DISPARO", "weapons": "ARMAS",
        "powerups": "POWERUPS", "pause": "PAUSA", "move_help": "WASD o flechas direccionales",
        "aim_help": "Mueve el raton para apuntar", "shoot_help": "Manten pulsado el boton izquierdo para disparar",
        "weapons_help": "Usa 1 a 4 para cambiar armas desbloqueadas", "powerups_help": "Elige una mejora cada 10 muertes",
        "pause_help": "Pulsa ESC para pausar el juego", "choose_help": "o haz clic",
    },
}


LANGUAGE_NAMES = ("english", "portugues", "espanol")


def translate(language, key):
    return TRANSLATIONS.get(language, TRANSLATIONS["english"]).get(key, key)