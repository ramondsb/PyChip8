#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from chip8 import Chip8


class Emulator:

    def __init__(self, file):
        print("Loading from \"{}\"".format(file))
        self.chip8 = Chip8()
        self.rom = self.load_from_file(file)


    def run(self):
        self.chip8.load_rom(self.rom)
        self.chip8.run()
        # self.draw_screen(self.chip8.display)
        #while(self.chip8.is_running()):
          # chip8.display_state()
          # Draw display
          # handle_keypress()


    def load_from_file(self, file):
        with open(file, "rb") as file:
            return file.read()


    def handle_keypress():
        # TODO
        pass


    def draw_screen(self, screen):
        for line in screen:
            print(line)


def main(filepath):
    emu = Emulator(filepath)
    emu.run();

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    main(args.file)
