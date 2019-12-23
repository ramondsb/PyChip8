import random


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
        self.display = (64 * 32) * [int("0x00", 16)]


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

        def opcode_0x8NNN(opcode):
            g = {
                0x0000: self.opcode_0x8XY0,
                0x0001: self.opcode_0x8XY1,
                0x0002: self.opcode_0x8XY2,
                0x0003: self.opcode_0x8XY3,
                0x0004: self.opcode_0x8XY4,
                0x0005: self.opcode_0x8XY5,
                0x0006: self.opcode_0x8XY6,
                0x0007: self.opcode_0x8XY7,
                0x000E: self.opcode_0x8XYE,
            }
            op = (opcode & int('0x000F', 16))
            g[op](opcode)

        g1 = {
                0x1000: self.opcode_0x1NNN,
                0x2000: self.opcode_0x2NNN,
                0x3000: self.opcode_0x3XNN,
                0x4000: self.opcode_0x4XNN,
                0x5000: self.opcode_0x5XY0,
                0x6000: self.opcode_0x6XNN,
                0x7000: self.opcode_0x7XNN,
                0x8000: opcode_0x8NNN,
                0x9000: self.opcode_0x9XY0,
                0xa000: self.opcode_0xAXXX,
                0xb000: self.opcode_0xBXXX,
                0xc000: self.opcode_0xCXNN,
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
        x = (opcode & 0x0F00) >> 8
        nn = opcode & 0x00FF

        vx = self.registers[x]
        if vx == nn:
            self.pc += 4
        else:
            self.pc += 2


    def opcode_0x4XNN(self, opcode):
        print("Executing opcode 4XNN")
        """Skips the next instruction if VX doesn't equal NN"""
        x = (opcode & 0x0F00) >> 8
        nn = opcode & 0x00FF

        vx = self.registers[x]
        if vx != nn:
            self.pc += 4
        else:
            self.pc += 2


    def opcode_0x5XY0(self, opcode):
        print("Executing opcode 5XYN")
        """Skips the next instruction if VX equals VY"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]
        if vx == vy:
            self.pc += 4
        else:
            self.pc += 2


    def opcode_0x6XNN(self, opcode):
        print("Executing opcode 6XNN")
        """Sets VX to NN"""
        x = (opcode & 0x0F00) >> 8
        nn = opcode & 0x00FF

        self.registers[x] = nn
        self.pc += 2


    def opcode_0x7XNN(self, opcode):
        print("Executing opcode 7XNN")
        """Adds NN to VX"""
        x = (opcode & 0x0F00) >> 8
        nn = opcode & 0x00FF

        self.registers[x] += nn
        self.pc += 2


    def opcode_0x8XY0(self, opcode):
        print("Executing opcode 8XY0")
        """Sets VX to the value of VY"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vy = self.registers[y]
        self.registers[x] = vy
        self.pc += 2


    def opcode_0x8XY1(self, opcode):
        print("Executing opcode 8XY1")
        """Sets VX to VX or VY"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]
        self.registers[x] = vx | vy
        self.pc += 2


    def opcode_0x8XY2(self, opcode):
        print("Executing opcode 8XY2")
        """Sets VX to VX and VY"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]
        self.registers[x] = vx & vy
        self.pc += 2


    def opcode_0x8XY3(self, opcode):
        print("Executing opcode 8XY3")
        """Sets VX to VX xor VY"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]
        self.registers[x] = vx ^ vy
        self.pc += 2


    def opcode_0x8XY4(self, opcode):
        print("Executing opcode 8XY4")
        """Adds VY to VX and set carry flag"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]

        sum = vx + vy

        self.registers[x] = (sum & 0xFFFF)

        if (vx + vy) > 255:
            self.registers[15] = 0x0001 # VF = 1
        else:
            self.registers[15] = 0x0000 # VF = 0
        self.pc += 2


    def opcode_0x8XY5(self, opcode):
        print("Executing opcode 8XY5")
        """VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't. """
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]

        sub = vx - vy

        self.registers[x] = (sub & 0xFFFF)

        if vx > vy:
            self.registers[15] = 0x0001 # VF = 1
        else:
            self.registers[15] = 0x0000 # VF = 0
        self.pc += 2


    def opcode_0x8XY6(self, opcode):
        print("Executing opcode 8XY6")
        """Stores the least significant bit of VX in VF and then shifts VX to the right by 1(Vx is divided by 2)"""
        x = (opcode & 0x0F00) >> 8

        vx = self.registers[x]

        least_significant_bit = vx & 0x0001

        self.registers[x] = vx >> 1

        # Set VF to the least significant bit
        self.registers[15] = least_significant_bit

        self.pc += 2


    def opcode_0x8XY7(self, opcode):
        print("Executing opcode 8XY5")
        """VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't. """
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]

        sub = vy - vx

        self.registers[x] = (sub & 0xFFFF)

        if vy > vx:
            self.registers[15] = 0x0001 # VF = 1
        else:
            self.registers[15] = 0x0000 # VF = 0
        self.pc += 2


    def opcode_0x8XYE(self, opcode):
        print("Executing opcode 8XYE")
        """Stores the most significant bit of VX in VF and then shifts VX to the left by 1 (Vx is multiplied by 2)"""
        x = (opcode & 0x0F00) >> 8

        vx = self.registers[x]

        msb = 1 << (16 - 1)

        most_significant_bit = vx & msb

        self.registers[x] = vx << 1

        # Set VF to the most significant bit
        self.registers[15] = most_significant_bit

        self.pc += 2


    def opcode_0x9XY0(self, opcode):
        print("Executing opcode 9XY0")
        """Skips the next instruction if VX doesn't equal VY"""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        print("x: {}, y: {}".format(hex(x), hex(y)))

        vx = self.registers[x]
        vy = self.registers[y]

        if vx != vy:
            self.pc += 4
        else:
            self.pc += 2


    def sys_address2(self, opcode):
        print("sys_address2")


    def opcode_00E0(self, opcode):
        """Clear screen"""
        print("clear screen")
        self.display = (64 * 32) * [int("0x00", 16)]
        self.pc += 2
        # TODO: Set draw flag


    def opcode_0xAXXX(self, opcode):
        print("Executing opcode AXXX")
        address = opcode & 0x0FFF
        self.i = address 
        self.pc += 2


    def opcode_0xBXXX(self, opcode):
        print("Executing opcode BXXX")
        """Jumps to the address XXX plus V0"""
        address = opcode & 0x0FFF
        v0 = self.registers[0]
        self.pc = address + v0


    def opcode_0xCXNN(self, opcode):
        print("Executing opcode CXNN")
        """Sets VX to the result of a bitwise AND operation on a random number"""
        x = (opcode & 0x0F00) >> 8
        nn = opcode & 0x00FF
        random_number = random.randrange(0, 256)

        self.registers[x] = random_number & nn

        self.pc += 2


    def opcode_00EE(self, opcode):
        print("Executing opcode 00EE")
