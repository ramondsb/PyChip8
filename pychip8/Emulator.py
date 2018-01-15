#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chip8 import Chip8


class Emulator:

    def __init__(self):
        self.chip8 = Chip8()


    def read_rom(filename):
        pass


    def run(self):
        self.chip8.load_rom(b'\x10\x00\x2B\xFF')
        self.chip8.run()
        #while(self.chip8.is_running()):
          # chip8.display_state()
          # Draw display


if __name__ == "__main__":
    emu = Emulator()
    emu.run();
