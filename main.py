import argparse

from src.game import Game


def main() -> None:
    parser = argparse.ArgumentParser(description="Voidstrike 2D shooter")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Run a short headless startup validation and exit.",
    )
    args = parser.parse_args()

    game = Game(smoke_test=args.smoke_test)
    game.run()


if __name__ == "__main__":
    main()
