"""
BUG: setuptoolsのバグ？で__version__を他のファイルからインポートしようとするとサブモジュールのインポート処理で失敗する
ひとまず__version__を__init__.py内で宣言することで回避
"""
# from ._version import __version__
__version__ = "0.2.0"

from .data import DefaultBackgroudImage, Image
from .game import (Card, CardState, Character, CharacterDetailSection,
                   CharacterNote, CharacterResource, Deck, Dice, DiceType,
                   Game, OnBoardCard, OnBoardCharacter, OnBoardDeck, Table,
                   TableBackgroundFilter, TableGridColor, TableGridType)

__all__ = ["DefaultBackgroudImage", "Image", "Card", "CardState", "Character", "CharacterDetailSection",
           "CharacterNote", "CharacterResource", "Deck", "Dice", "DiceType", "Game", "OnBoardCard", "OnBoardCharacter",
           "OnBoardDeck", "Table", "TableBackgroundFilter", "TableGridColor", "TableGridType"]
