#!/bin/python3

import math
import random
import enum
import base64
import bz2
import pyxel
import bf

@enum.unique
class Phase(enum.Enum):
    LOAD = 0
    GAME = 1
    OVER = 2

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
        self.phase = Phase.LOAD
        self.char = [Char(), Char(), Char(), Char(), Char()]
        self.pad = [100, 200-20]
        self.bf = bf.Machine(None, self.putchar)
        self.insn = ""
        self.output = ""

    def update(self):
        if self.phase == Phase.LOAD:
            if pyxel.btnr(pyxel.KEY_R):
                sb64 = "QlpoOTFBWSZTWdq2ejwAA6jaAH/4AAsABQAKUAR4eKmdVQO6jjvCUxE0hUJ6mCU9FJqeimgAk9VSmjEMANqg0AABU1UiaaaDaTdu2pZbLEtbKICU0TbUxIrLYSU0JEtrGSjZtJk0SrQyy0RiUlYktNRILNNSZNRkLa0pJE1qVE2GHLNyNrFtibaY1mWbQ1sgsmLQybZw4ykpbUqhhta42W4gSZmlBsUCLSkpFJFLWWZum2CuK1WRSDSIUSQoYZITE0hZlNmEUkSEqVKFUVVOoe+53HXzZwfEcyzLXkHRFRw8aFavWOJrifHTXzdWPzg+9Zor7m7PiTteW+atIIIu5XjPXkqnJ011cT3BIwYPHnlmCSQa8Rm2cLxLjNbqSVtYSZ5SmpNJFhW7U5cic31TuSNno4ayxLXuPKY8p+nqd25HBsN9bomtuVHkg+btxcik1SNx1PNTSRWNCM5dqi33FsvGIYy4pCanSF4zRQNX4VRVU/uI99fkwWAhl58K2Wfw/P1zvO+b2jzl13a7eyjvb/5NCFF4M0t1BnJ5GounEt2Gerik4e52ck21va8ZuxdW707uTG00+rPXmeDxNfl1PmN/T7i7BkXCRXxxc+3yZ0dx9px73JvMi+VQUcs3LPB/qtjOWegmta2axGmTay2NNYtZvckoTSyaKgtIpWKptbcCZbTWzRZim1M1mlLTVlwEiGYJsBGNaQym2ZY20m0Yo2ixYtpNaI3rX5pb2T1lMcoUpSQsi1SPIIqatpTOxfc62/VPQiiXDpW4yk9AzSU2itYq6wmNhS1ksGkIIKihEcsJVsdYIhopSt8CG3pT1olMSHzCK8gQHxdyRThQkNq2ejw="
                self.bf.run(bz2.decompress(base64.b64decode(sb64.encode())).decode())
                exec(self.output)
                self.init()
                self.phase = Phase.GAME
            elif pyxel.btnr(pyxel.KEY_SPACE):
                self.phase = Phase.GAME
        elif self.phase == Phase.GAME:
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
                    c.init(random.randint(10, 200-10))

    def draw(self):
        pyxel.cls(7)

        if self.phase == Phase.LOAD:
            pyxel.text(65, 100, "Rain of Brainf*ck", pyxel.COLOR_PURPLE)
            pyxel.text(70, 130, "Install Rust: R", pyxel.COLOR_GRAY)
            pyxel.text(65, 140, "Start f*ck: Space", pyxel.COLOR_GRAY)
        elif self.phase == Phase.GAME:
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

if __name__ == '__main__':
    app = App()
    app.run()
