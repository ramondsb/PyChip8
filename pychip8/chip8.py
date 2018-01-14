from memory import Memory

class Chip8:

    def __init__(self):
        self.memory = Memory()
        self.running = False
        self.pc = 0


    def cycle(self):
        # Read opcode
          opcode =  self.memory.read_next_opcode(self.pc)
        # Find operation to execute
          self.decode(opcode)


    def decode(self, opcode):
        if (opcode &  int.from_bytes(b'\xF0\x00', byteorder='big')) == 0x1000:
            print("1")
        elif opcode & int.from_bytes(b'\xF0\x00', byteorder='big') == 0x2000:
            print("2")
        else:
            print("other")


    def run(self):
        self.running = True
        self.cycle()


    def stop(self):
        self.running= False


    def is_running(self):
        return self.running
