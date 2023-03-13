# pyudon

[ユドナリウム](https://github.com/TK11235/udonarium)のアーカイブファイルをPythonから作成、編集するためのAPIです。
The Udonarium API to create archived files on Python.

## Description

ユドナリウムのアーカイブ機能は本来セッションの途中状況などを保存するために使われますが、本ライブラリはセッション開始時にランダムにオブジェクトを配置したい場合などを想定して、ゲーム内オブジェクトをコード上で扱いzipファイルとして生成できるようにしたものです。
開発途中のため、最低限の機能しかありません。(ボード、カード、山札、駒の生成及び一部の操作)
気が向いたらそのほかの機能が追加されるかもしれません。

## Install

setup.pyがあるディレクトリで以下を叩いてください。

```bash
$ python -m pip install .
```

## Sample

インストール後、以下を叩くとtemp/ディレクトリにサンプルzipがダンプされます。

```bash
$ mkdir temp/
$ python sample.py temp/
```

## Usage

gameモジュールにあるもので基本的にはすべて完結します。

以下が簡単な使用例です。
"TestCharacter"という名前の駒を1体生成し、テーブル上に配置します。

```python
from pyudon import Character, Game, Table, DefaultBackgroudImage

# テーブル生成
table_image = DefaultBackgroudImage()
table = Table("FirstTable", table_image)

# ゲーム生成
game = Game(table)

# キャラクター生成
character = Character("TestCharacter")
# キャラクターをゲームに追加
game.add_character(character, x=0, y=0)

# Zipファイル作成
game.create_zip("temp/archive.zip")
```

"sample.py"内でその他のオブジェクトも一通り生成しているので、覗いてみてください。

## License

[MIT License](https://github.com/alfa0112/pyudon/blob/master/LICENSE)
