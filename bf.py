#!/usr/bin/python3

import sys

class Machine:
    src = ""
    ip = 0
    ptr = 0
    loop = 0
    buf = [0] * 100
    def insn(self):
        return self.src[self.ip]
    def get_buf(self):
        return self.buf[self.ptr]
    def set_buf(self, data: int):
        self.buf[self.ptr] = data
    def run_step(self):
        i = self.insn()
        #print("insn: ", i, "(", self.ip, ")")
        if i == '>':
            self.ptr += 1
        elif i == '<':
            self.ptr -= 1
        elif i == '+':
            self.buf[self.ptr] += 1
        elif i == '-':
            self.buf[self.ptr] -= 1
        elif i == '.':
            print(chr(self.buf[self.ptr]), end="")
        elif i == ',':
            print("\ngetchar: ", end='')
            sys.stdout.flush()
            c = input()[0]
            self.set_buf(ord(c))
        elif i == '[':
            if(self.get_buf() == 0):
                self.ip += 1
                while self.loop > 0 or self.insn() != ']':
                    print("loop", self.loop)
                    if self.insn() == '[':
                        self.loop += 1
                    elif self.insn() == ']':
                        self.loop -= 1
                    self.ip += 1
        elif i == ']':
            if(self.get_buf() != 0):
                self.ip -= 1
                while self.loop > 0 or self.insn() != '[':
                    if self.insn() == ']':
                        self.loop += 1
                    elif self.insn() == '[':
                        self.loop -= 1
                    self.ip -= 1
                self.ip -= 1


        self.ip += 1

    def run(self, src):
        self.src = src
        print("src: ", src)
        while self.ip < len(self.src):
            self.run_step()

if __name__ == '__main__':
    print("usage> ./bf.py src")
    bf = Machine()
    bf.run(sys.argv[1])
    #bf.run("+[>,.<]")
