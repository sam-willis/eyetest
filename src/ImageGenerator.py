import random
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import GaussianProcess
import pickle


class ImageGenerator:
    def __init__(self, width=400, height=300):
        self.random = random.SystemRandom()
        self.width = width
        self.height = height
        self.msg = None
        self.position = None
        self.fontsize = None
        try:
            with open("x", 'rb') as f:
                self.rows = pickle.load(f)
        except FileNotFoundError:
            self.rows = []
        self.distribution = GaussianProcess.GP(self.rows)

    def generate_char_image(self):
        random_char = self.random.choice(string.ascii_lowercase)
        return self.generate_image(random_char)

    def generate_image(self, msg):
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        self.draw_msg(draw, msg)
        self.draw_centerpoint(draw)
        return img

    def draw_centerpoint(self, draw, size=10):
        p1 = ((self.width - size) // 2, (self.height - size) // 2)
        p2 = ((self.width + size) // 2, (self.height + size) // 2)
        draw.ellipse((p1, p2), fill=(255, 255, 255, 255))

    def draw_msg(self, draw, msg):
        while True:
            x, y = (self.random.randrange(self.width),
                    self.random.randrange(self.height))
            self.msg = msg
            self.position = (x, y)
            self.fontsize = self.distribution.draw(self.position)
            w, h = draw.textsize(msg, font=self.get_font())

            xc = x - w // 2
            yc = y - h // 2

            if self.width - w > xc and xc > 0 and self.height - h > yc and yc > 0:
                break

        draw.text((xc, yc), msg, (255, 255, 255), font=self.get_font())

    def update(self, msg_guess):
        if all((self.msg, self.position, self.fontsize)):
            self.rows.append(
                (self.position, self.msg, msg_guess, self.fontsize), )
            with open("x", 'wb') as f:
                pickle.dump(self.rows, f)
            self.distribution.update(self.position, self.msg, msg_guess,
                                     self.fontsize)
        else:
            raise Exception("update called before generate_image")

    def get_font(self):
        return ImageFont.truetype("Inconsolata-g.ttf", self.fontsize)

    def print_results(self):
        self.distribution.plot()
