import sus 
import re

class CPU:
    def __init__(self):
        self.ram = [0] * 256 
        self.reg = [0] * 8 
        self.pc = 0 
        self.sp = 7 
        self.reg[self.sp] = 244 
        self.e = 7 
        self.fl = [0] * 8

    def load(self):

        address = 0

        if len(sys.argv) != 2:
            print("Pass a filename argument when calling this file")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split("#", 1)[0]
                    if num.strip() != "":
                        self.ram_write(address, int(num, 2))
                        address += 1

        except FileNotFoundError:
            print("file not found")
            sys.exit(2)

    def halt(self):
        print('Halting the program')
        sys.exit(1)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op_code, reg_a, reg_b):
        """ALU operations."""

        if op_code == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op_code == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op_code == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op_code == "DEC":
            self.reg[reg_a] -= 1
        elif op_code == "INC":
            self.reg[reg_a] += 1
        elif op_code == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[self.e] = 1
            else:
                self.fl[self.e] = 0
        elif op_code == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op_code == "DIV":
            if self.reg[reg_b] != 0:
                self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]
            else:
                self.halt()
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):