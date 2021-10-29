import unittest

import udonarium

class TestFileToHashMaker(unittest.TestCase):
    def test_read(self):
        hash_maker = udonarium.FileToHashMaker()

        hashed_name = hash_maker.make_from_file("tests/data/rect890.png")
        self.assertEqual("885b78ed0eb2588873f44aa8c1bc378a101bc5390f78f29ba04b0d3897603b0a",
                        hashed_name)

class TestDeckNode():
    def __init__():
        pass