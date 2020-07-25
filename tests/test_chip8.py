import unittest

from pychip8 import chip8


class TestChip8(unittest.TestCase):
    def setUp(self):
        self.chip = chip8.Chip8()
        self.state = {
            "memory": [0x0000, 0x0001, 0x0001, 0x0000],
            "pc": 0
        }


    def test_fetch_opcode(self):

        opcode = self.chip.fetch_opcode(self.state)

        self.assertEqual(opcode, 1)

        self.state["pc"] = 2
        opcode = self.chip.fetch_opcode(self.state)

        self.assertEqual(opcode, 256)


if __name__ ==  "__main__":
    unittest.main()
