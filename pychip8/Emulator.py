#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chip8 import Chip8


class Emulator:

    def __init__(self):
        self.chip8 = Chip8()
        self.rom = ["0x00", "0xE0", "0xA1","0x23", "0x10", "0x00", "0x2B", "0xFF"]


    def run(self):
        self.chip8.load_rom(self.rom)
        self.chip8.run()
        # self.draw_screen(self.chip8.display)
        #while(self.chip8.is_running()):
          # chip8.display_state()
          # Draw display
          # handle_keypress()


    def handle_keypress():
        # TODO
        pass


    def draw_screen(self, screen):
        for line in screen:
            print(line)


if __name__ == "__main__":
    emu = Emulator()
    emu.run();
