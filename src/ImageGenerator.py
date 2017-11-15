import random
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import GaussianProcess
import pickle
from math import pi, sqrt, sin, cos, floor, atan, acos, asin


class ImageGenerator:
    def __init__(self, width=400, height=300):
        self.random = random.SystemRandom()
        self.width = width
        self.height = height
        self.maxA = atan(height / width)
        self.centerpoint_radius = 5
        self.msg = None
        self.position = None
        self.fontsize = None
        self.savefile_data = "rows_{}_{}.pickle".format(width, height)
        self.savefile_bound = "bound_{}_{}.pickle".format(width, height)
        try:
            with open(self.savefile_data, 'rb') as f:
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

    def draw_centerpoint(self, draw):
        p1 = ((self.width // 2 - self.centerpoint_radius),
              (self.height // 2 - self.centerpoint_radius))
        p2 = ((self.width // 2 + self.centerpoint_radius),
              (self.height // 2 + self.centerpoint_radius))
        draw.ellipse((p1, p2), fill=(255, 255, 255, 255))

    def draw_msg(self, draw, msg):
        while True:
            theta = self.random.uniform(-pi, pi)
            r = self.get_r(theta)
            x = int(self.width / 2 + r * cos(theta))
            y = int(self.height / 2 + r * sin(theta))
            self.msg = msg
            self.position = (r, theta)
            self.fontsize = self.distribution.draw(r)
            w, h = draw.textsize(msg, font=self.get_font())

            xc = x - w // 2
            yc = y - h // 2

            if self.width - w > xc and xc > 0 and self.height - h > yc and yc > 0:
                break

        draw.text((xc, yc), msg, (255, 255, 255), font=self.get_font())

    def get_r(self, theta):
        if (pi - self.maxA > theta and theta > self.maxA) or (
                2 * pi - self.maxA > theta and theta > pi + self.maxA):
            maxR = floor(abs(self.width / (2 * cos(theta))))
        else:
            maxR = floor(abs(self.height / (2 * sin(theta))))
        return self.random.randint(self.centerpoint_radius * 2, maxR)

    def update(self, msg_guess):
        if all((self.msg, self.position, self.fontsize)):
            self.rows.append(
                (self.position, self.msg, msg_guess, self.fontsize), )
            with open(self.savefile_data, 'wb') as f:
                pickle.dump(self.rows, f)

            with open(self.savefile_bound, 'wb') as f:
                try:
                    pickle.dump(self.distribution.get_bound(), f)
                except AssertionError:
                    pass

            self.distribution.update(self.position, self.msg, msg_guess,
                                     self.fontsize)
        else:
            raise Exception("update called before generate_image")

    def get_font(self):
        return ImageFont.truetype("Inconsolata-g.ttf", self.fontsize)

    def print_results(self):
        self.distribution.plot()
