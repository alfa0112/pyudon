import argparse
import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import pandas as pd

from .hyper_bloom import HyperBloomGame, HyperBloomDataXML, CardImageTable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images", type=Path)
    parser.add_argument("card_image_table", type=Path,
                        help="The csv file with correspondence between card names and images.")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--bg-img", type=Path,
                        help="The image file to be set to background of the game.")
    args = parser.parse_args()

    # カード定義読み込み
    card_image_table_df = pd.read_csv(args.card_image_table)    
    card_image_table = CardImageTable(args.images,
                                    card_image_table_df)

    # ゲーム生成
    hb_game = HyperBloomGame(card_image_table, args.bg_img)
    hb_game.create_random_field()

    # Zipファイル作成
    now = datetime.datetime.now()
    zip_path = args.output_dir / now.strftime("hb_%y%m%d_%H%M%S.zip")
    hb_game.create_zip(zip_path)


if __name__ == "__main__":
    main()