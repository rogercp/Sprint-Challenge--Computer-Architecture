import sys 
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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        ADD = 0b10100000
        AND = 0b10101000
        POP = 0b01000110
        LD  = 0b10000011
        MOD = 0b10100100
        PUSH = 0b01000101
        CMP = 0b10100111
        CALL = 0b01010000
        RET = 0b00010001
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101

        while self.pc < len(self.ram):

            command = self.ram[self.pc]
            num_operands = (command & 0b11000000) >> 6

            if num_operands == 1:
                operand_a = self.ram_read(self.pc + 1)
            elif num_operands == 2:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

            if command == HLT:
                self.halt()
            elif command == LDI:
                self.reg[operand_a] = operand_b
            elif command == PRN:
                print(self.reg[operand_a])
            elif command == MUL:
                self.alu("MUL", operand_a, operand_b)
                print(self.reg[operand_a])
            elif command == ADD:
                self.alu("ADD", operand_a, operand_b)
            elif command == AND:
                self.alu("AND", operand_a, operand_b)
            elif command == LD:
                self.reg[operand_a] = self.reg[operand_b]
            elif command == MOD:
                self.alu("MOD", operand_a, operand_b)
            elif command == POP:
                value = self.ram[self.reg[self.sp]]
                self.reg[operand_a] = value
                self.reg[self.sp] += 1
            elif command == PUSH:
                self.reg[self.sp] -= 1
                value = self.reg[operand_a]
                self.ram[self.reg[self.sp]] = value  
            elif command == CMP:
                self.alu("CMP", operand_a, operand_b)

            if command == CALL:
                return_addr = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_addr
                regnum = self.ram[self.pc + 1]
                subroutine_addr = self.reg[regnum]
                self.pc = subroutine_addr
                
            elif command == RET:
                return_addr = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
                self.pc = return_addr
            elif command == JMP:
                self.pc = self.reg[operand_a]
            elif command == JNE:
                if self.fl[self.e] == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += num_operands + 1
            elif command == JEQ:
                if self.fl[self.e] == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += num_operands + 1
            else:
                self.pc += num_operands + 1