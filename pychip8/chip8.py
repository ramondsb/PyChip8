class Chip8:

    def __init__(self):
        self.memory = 4096 * [int("0x00", 16)]
        self.pc = int("0x200", 16)
        self.stack = 16 * [int("0x00", 16)]
        self.sp = 0
        self.i = int("0x00", 16)
        self.registers = 16 * [int("0x00", 16)]
        self.delay_timer = int("0x00", 16)
        self.sound_timer = int("0x00", 16)
        self.keypad = 16 * [int("0x00", 16)]
        self.display = 64 * [32 * [int("0x00", 16)]]


    def cycle(self):
        opcode = self.fetch_opcode()

        self.decode_opcode(opcode)

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer == 0:
            #TODO: Integrate sound system
            print("beep")


    def fetch_opcode(self):
        msb = self.memory[self.pc]
        lsb = self.memory[self.pc + 1]

        #print("msb: {}, lsb: {}".format(msb, lsb))

        return ((msb << 8) | (lsb))


    def decode_opcode(self, opcode):
        opcode = opcode & 0xffff
        print("opcode", hex(opcode))

        def opcode_0x00XX(opcode):
            g2 = {
                0x00e0: self.opcode_00E0,
                0x00ee: self.opcode_00EE
            }
            op = (opcode & int('0x00FF', 16))
            g2[op](opcode)

        g1 = {
                0x1000: self.opcode_0x1NNN,
                0x2000: self.opcode_0x2NNN,
                0x3000: self.opcode_0x3XNN,
                0xa000: self.opcode_0xAXXX,
                0x0000: opcode_0x00XX
        }

        op = (opcode & int('0xF000', 16))
        #print("op: {}".format(hex(op)))

        g1[op](opcode)


    def load_rom(self, bytes):
        bytes = list(bytes)
        for i in range(len(bytes)):
            self.memory[i + 512] = bytes[i]


    def run(self):
        self.cycle()


    def opcode_0x1NNN(self, opcode):
        print("Executing opcode 1NNN")
        """Jumps to address NNN"""
        address = opcode & 0x0FFF
        self.pc = address


    def opcode_0x2NNN(self, opcode):
        print("Executing opcode 2NNN")
        """Calls subroutine at NNN"""
        address = opcode & 0x0FFF
        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = address


    def opcode_0x3XNN(self, opcode):
        print("Executing opcode 3XNN")
        """Skips the next instruction if VX equals NN"""
        x = opcode & 0x0F00
        nn = opcode & 0x00FF

        vx = self.registers[x]
        if vx == nn:
            self.pc += 2


    def sys_address2(self, opcode):
        print("sys_address2")


    def opcode_00E0(self, opcode):
        """Clear screen"""
        print("clear screen")
        self.display = 64 * [32 * [int("0x00", 16)]]
        self.pc += 2
        # TODO: Set draw flag


    def opcode_0xAXXX(self, opcode):
        print("Executing opcode AXXX")
        address = opcode & 0x0FFF
        self.i = address 
        self.pc += 2


    def opcode_00EE(self, opcode):
        print("Executing opcode 00EE")
