#!/usr/bin/python3

import sys

def getchar():
    print("\ngetchar: ", end='')
    sys.stdout.flush()
    c = input()[0]
    return ord(c)

def putchar(c: int):
    print(chr(c), end="")

class Machine:
    src = ""
    ip = 0
    ptr = 0
    loop = 0
    buf = [0] * 1000

    getchar_handler = None
    putchar_handler = None

    def __init__(self, getchar_handler=None, putchar_handler=None):
        if getchar_handler == None:
            self.getchar_handler = getchar
        else:
            self.getchar_handler = getchar_handler
        if putchar_handler == None:
            self.putchar_handler = putchar
        else:
            self.putchar_handler = putchar_handler

    def reset(self):
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
        if len(self.src) == 0:
            return False
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
            self.putchar_handler(self.get_buf())
        elif i == ',':
            self.set_buf(self.getchar_handler())
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
        else:
            return False

        self.ip += 1
        return True

    def run(self, src):
        self.src = src
        print("src: ", src)
        while self.ip < len(self.src):
            if not self.run_step():
                break

if __name__ == '__main__':
    print("usage> ./bf.py src")
    bf = Machine()
    bf.run(sys.argv[1])
    #bf.run("+[>,.<]")
