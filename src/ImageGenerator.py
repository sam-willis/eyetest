import random
import string
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
from collections import defaultdict
from math import ceil

WORD_SITE = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"


class ImageGenerator:
    def __init__(self, width=1920, height=1200):
        response = requests.get(WORD_SITE)
        self.words = response.content.splitlines()
        self.random = random.SystemRandom()
        self.msgs = []
        self.positions = []
        self.width = width
        self.height = height
        self.nx = self.width // 10
        self.ny = self.height // 10
        self.size_lookup = defaultdict(lambda: 16)

    def generate_word_image(self):
        random_word = str(self.random.choice(self.words))[2:-1]
        return self.generate_image(random_word)

    def generate_char_image(self):
        random_char = self.random.choice(string.ascii_lowercase)
        return self.generate_image(random_char)

    def generate_image(self, msg):
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(msg)
        x, y = (self.random.randrange(self.width - 2 * w),
                self.random.randrange(self.height - 2 * h))
        size = self.size_lookup[(x // self.nx, y // self.ny)]
        draw.text((x, y), msg, (255, 255, 255), font=self.get_font(size))
        self.msgs.append(msg)
        self.positions.append((x, y), )
        return img

    def update(self, msg_guess):
        x, y = self.positions[-1]
        if msg_guess == self.msgs[-1]:
            print("correct")
            self.size_lookup[(x // self.nx, y // self.ny)] = ceil(
                self.size_lookup[(x // self.nx, y // self.ny)] / 2)
        else:
            print("failed")
            self.size_lookup[(x // self.nx, y // self.ny)] = ceil(
                self.size_lookup[(x // self.nx, y // self.ny)] * 2)

    def get_font(self, size=10):
        return ImageFont.truetype("Inconsolata-g.ttf", size)

    def print_results(self):
        for key, value in self.size_lookup.items():
            print('At {}: font size is {}'.format(key, value))
