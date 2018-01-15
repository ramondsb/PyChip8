from memory import Memory

class Chip8:

    def __init__(self):
        self.memory = Memory()
        self.running = False
        self.pc = 0


    def cycle(self):
        opcode =  self.memory.read_opcode(self.pc)
        self.decode(opcode)
        self.pc += 2



    def decode(self, opcode):
        # First group of instruction with forma x000
        g1 = {
                0x1000: self.sys_address,
                0x2000: self.sys_address2
        }
        op = (opcode & int.from_bytes(b'\xF0\x00', byteorder='big'))

        g1[op](opcode)


    def load_rom(self, bytes):
        self.memory.set_data(bytes)

    def sys_address(self, opcode):
        print("sys_address")


    def sys_address2(self, opcode):
        print("sys_address2")


    def run(self):
        self.running = True
        self.cycle()
        self.cycle()


    def stop(self):
        self.running= False


    def is_running(self):
        return self.running
