import argparse
import datetime
from pathlib import Path

from pyudon import Game, Deck


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    # ゲーム生成
    game = Game()

    # デッキ生成
    deck = Deck()

    # デッキ追加
    # game.add_deck(deck)

    # Zipファイル作成
    now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    zip_path = args.output_dir / f"{now}.zip"
    game.create_zip(zip_path)


if __name__ == "__main__":
    main()
