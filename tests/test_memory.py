#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from pychip8.memory import Memory

class TestMemory(unittest.TestCase):

    def test_set_memory_data(self):
        dump_data = bytes(b'\xFF\x0A\x2C\x3D')
        mem = Memory()
        mem.set_data(dump_data)


    def test_next_opcode(self):
        dump_data = bytes(b'\xFF\x0A\x2C\x3D')
        mem = Memory()
        mem.set_data(dump_data)

        opcode = int.from_bytes(dump_data[0:2], byteorder='big')
        self.assertEqual(opcode, mem.read_opcode(0))

        opcode = int.from_bytes(dump_data[2:], byteorder='big')
        self.assertEqual(opcode, mem.read_opcode(2))


if __name__ == '__main__':
        unittest.main()


