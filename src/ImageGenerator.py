import random
import string
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

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
        self.segment_lookup = {}
        self.build_segments()

    def generate_word_image(self, size=16):
        random_word = str(self.random.choice(self.words))[2:-1]
        return self.generate_image(random_word, size)

    def generate_char_image(self, size=16):
        random_char = self.random.choice(string.ascii_lowercase)
        return self.generate_image(random_char, size)

    def generate_image(self, msg, size):
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(msg)
        position = (self.random.randrange(self.width - 2 * w),
                    self.random.randrange(self.height - 2 * h))
        draw.text(position, msg, (255, 255, 255), font=self.get_font(size))
        self.msgs.append(msg)
        self.positions.append(msg)
        return img

    def update(self, msg_guess):
        if msg_guess == self.msgs[-1]:
            print("correct")
        else:
            print("failed")

    def get_font(self, size=10):
        return ImageFont.truetype("Inconsolata-g.ttf", size)

    def build_segments(self):
        np.linspace(0, self.width, 10)
        np.linspace(0, self.height, 10)
