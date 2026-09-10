# Voidstrike

Voidstrike is a top-down 2D space shooter built with Pygame.

## Requisitos

- Python 3.10+
- Pygame

## Instalação

```bash
python -m pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Controles

- WASD ou setas: movimentação
- Mouse: mira
- Botão esquerdo: disparar
- ESC: pausar

## Assets e música

- Coloque os sprites em pastas dentro de `Sprites/`
- Coloque os efeitos sonoros em `Sons/`
- Coloque a música principal em `Músicas/Under_Heavy_Fire.mp3`
- O jogo verificará o caminho automaticamente e avisará no console caso a música não exista

## Alterar dificuldade das waves

Edite o arquivo `data/waves.json`.

Exemplo:

```json
{
  "1": { "enemies": { "basic": 8 } },
  "2": { "enemies": { "basic": 10, "fast": 3 } },
  "5": { "boss": "boss_01" }
}
```

## Adicionar novos inimigos e bosses

- Crie a classe em `src/enemies.py` ou `src/bosses.py`
- Registre o tipo em `src/waves.py`
- Adicione o sprite na pasta correspondente dentro de `Sprites/`

## Estrutura principal

- `src/game.py`: loop principal do jogo
- `src/player.py`: nave do jogador
- `src/enemies.py`: inimigos
- `src/bosses.py`: bosses
- `src/projectiles.py`: projéteis
- `src/waves.py`: sistema de ondas
- `src/ui.py`: menu, HUD e telas
- `src/audio.py`: música e Efeitos sonoros
- `data/waves.json`: configuração das ondas
- `data/settings.json`: configurações salvas pelo jogador
