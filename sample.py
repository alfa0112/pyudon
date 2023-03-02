import argparse
import datetime
from pathlib import Path

from pyudon import (Card, CardState, Character, CharacterDetailSection,
                    CharacterNote, CharacterResource, Deck,
                    DefaultBackgroudImage, Game, Image, Table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    # テーブル生成
    table_image = DefaultBackgroudImage()
    table = Table("FirstTable", table_image)

    # ゲーム生成
    game = Game(table)

    # キャラクター生成
    character = Character(
        "TestCharacter",
        size=1
    )
    # resourceをキャラクターに追加
    character_resources = CharacterDetailSection("resource")
    character_resources.add_resource(CharacterResource("HP", 50, 100))
    character_resources.add_resource(CharacterResource("MP", 50, 100))
    character.add_detail_section(character_resources)
    # informationをキャラクターに追加
    character_info = CharacterDetailSection("information")
    character_info.add_note(CharacterNote(
        "Description", "This is a test character."))
    character_info.add_note(CharacterNote("Memo", "Memo for user usage."))
    character.add_detail_section(character_info)
    # キャラクターをゲームに追加
    game.add_character(character, 0, 0)

    # カード生成
    with open("tests/data/card_top.png", "rb") as f:
        top_image = Image(f.read())
    with open("tests/data/card_bottom.png", "rb") as f:
        bottom_image = Image(f.read())
    # カードをゲームに追加
    game.add_card(Card("TestLittleCard", top_image,
                  bottom_image, size=1), 100, 0)
    game.add_card(Card("TestLargeCard", top_image,
                  bottom_image, size=4), 200, 0)
    game.add_card(Card("TestTopCard", top_image,
                  bottom_image, state=CardState.TOP), 300, 0)
    game.add_card(Card("TestButtomCard", top_image,
                  bottom_image, state=CardState.BOTTOM), 400, 0)

    # デッキ生成
    deck = Deck("TestDeck")
    # カードをデッキに追加
    deck.add_card(Card("TestCardInDeck", top_image, bottom_image))
    card_in_deck = Card("TestCardInDeck", top_image, bottom_image)
    deck.add_cards([card_in_deck, card_in_deck, card_in_deck])
    # デッキをゲームに追加
    game.add_deck(deck, 0, 100)

    # Zipファイル作成
    now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    zip_path = args.output_dir / f"{now}.zip"
    game.create_zip(zip_path)


if __name__ == "__main__":
    main()
