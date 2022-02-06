import math
import random


class RGB:
    r = 0
    g = 0
    b = 0

    colors = [
        [(0xF5, 0x22, 0x2D), "red"],
        [(0xFA, 0x54, 0x1C), "volcano"],
        [(0xFA, 0x8C, 0x16), "orange"],
        # [(0xFA, 0xAD, 0x14), "gold"],
        [(0xFA, 0xDB, 0x14), "yellow"],
        # [(0xA0, 0xD9, 0x11), "lime"],
        [(0x52, 0xC4, 0x1A), "green"],
        [(0x13, 0xC2, 0xC2), "cyan"],
        [(0x18, 0x90, 0xFF), "blue"],
        # [(0x2F, 0x54, 0xEB), "geekblue"],
        [(0x72, 0x2E, 0xD1), "purple"],
        [(0xEB, 0x2F, 0x96), "magenta"]
        # [(0x66, 0x66, 0x66), "grey"]
    ]

    def __init__(self, orig=None):
        if orig is None:
            return
        else:
            self.set(orig[0], orig[1], orig[2])

    def __eq__(self, other):
        if isinstance(other, RGB):
            return (self.r == other.r) and (self.g == other.g) and (self.b == other.b)
        return False

    def randomize(self):
        self.r = random.randrange(255)
        self.g = random.randrange(255)
        self.b = random.randrange(255)

    def randomFromPalette(self):
        index = random.randrange(len(self.colors))
        self.r = self.colors[index][0][0]
        self.g = self.colors[index][0][1]
        self.b = self.colors[index][0][2]
        print("{0}".format(self.colors[index][1]))

    def set(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def get(self):
        return (self.r, self.g, self.b)

    def dump(self):
        print((self.r, self.g, self.b))

    def brighten(self):
        brightnessIncrement = 255 - max(self.r, self.g, self.b)
        self.r += brightnessIncrement
        self.b += brightnessIncrement
        self.g += brightnessIncrement

    def darken(self):
        darknessDecrement = min(self.r, self.g, self.b)
        self.r -= darknessDecrement
        self.b -= darknessDecrement
        self.g -= darknessDecrement

    def multiply(self, scale_factor):
        self.r = int(float(self.r) * scale_factor)
        self.g = int(float(self.g) * scale_factor)
        self.b = int(float(self.b) * scale_factor)
