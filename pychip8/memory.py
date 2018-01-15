class Memory:

    def __init__(self):
        # Initialize with 4kB
        self.mem = bytearray(4096);


    def set_address(self):
        pass


    def set_data(self, bytes):
        self.mem = bytearray(bytes)


    def read_address(self, address):
        pass

    def read_opcode(self, pc):

        msb = self.mem[pc]
        lsb = self.mem[pc + 1]

        return ((msb << 8) | (lsb))

