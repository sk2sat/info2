#!/bin/python3

import math
import random
import enum
import pyxel
import bf

@enum.unique
class Phase(enum.Enum):
    GAME = 0
    OVER = 1

class Char:
    c = None
    dt = 0.0
    pos = [0, 0]
    vel = [0, 0]

    def gen():
        lst = "><+-.,[]"
        c = lst[random.randint(0, len(lst)-1)]
        return c

    def __init__(self):
        self.init()

    def init(self, x=0, y=0, speed=40.0):
        self.c = Char.gen()
        self.dt = 1.0 / pyxel.DEFAULT_FPS
        self.pos = [x, y]
        angle = math.radians(random.randint(40, 140))
        self.vel = [speed*math.cos(angle), speed*math.sin(angle)]

    def update(self):
        self.pos[0] += self.vel[0] * self.dt
        self.pos[1] += self.vel[1] * self.dt


class App:
    phase = Phase.GAME
    char = None
    pad = [0, 0]
    bf = None
    insn = ""
    output = ""

    def __init__(self):
        self.init()

    def init(self):
        self.phase = Phase.GAME
        self.char = [Char(), Char(), Char(), Char(), Char()]
        self.pad = [100, 200-20]
        self.bf = bf.Machine(None, self.putchar)
        self.insn = ""
        self.output = ""

    def update(self):
        if pyxel.btn(pyxel.KEY_END):
            self.init()
        elif pyxel.btn(pyxel.KEY_ENTER):
            self.bf.run(self.bf.src)
        elif pyxel.btnr(pyxel.KEY_BACKSPACE):
            self.bf.src = self.bf.src[:-1]
        self.pad[0] = pyxel.mouse_x

        for c in self.char:
            c.update()
            p = c.pos
            if p[1] > 200-15:
                if self.pad[0] < p[0] and p[0] < self.pad[0]+40:
                    self.insn = c.c
                    self.bf.src += self.insn
                    #if self.bf.run_step():
                    #    pass
                    #else:
                    #    self.bf.reset()
                    #    self.output = ""
                c.init(random.randint(10, 200-10))

    def draw(self):
        pyxel.cls(7)

        for c in self.char:
            pyxel.text(c.pos[0], c.pos[1], c.c, pyxel.COLOR_BROWN)

        pyxel.rect(self.pad[0], self.pad[1], 40, 5, pyxel.COLOR_PINK)
        pyxel.rect(0, 200-15, 200, 3, pyxel.COLOR_GRAY)
        pyxel.text(2, 200-9, "src: "+self.bf.src, pyxel.COLOR_BLACK)
        pyxel.text(100, 200-9, "output: "+self.output, pyxel.COLOR_BLACK)

    def run(self):
        pyxel.init(200,200)
        pyxel.run(self.update, self.draw)

    def putchar(self, c: int):
        self.output += chr(c)

app = App()
app.run()
