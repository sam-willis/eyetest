import random
import string
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from database import ScoreKeeper


def score_function(rows):
    from collections import Counter
    correct = Counter()
    total = Counter()
    for row in rows:
        if row.letter == row.guess:
            correct[row.fontsize] += 1
        total[row.fontsize] += 1
    try:
        return min(k for k, v in total.items() if correct[k] / v > 0.5)
    except ValueError as e:
        try:
            return max(rows.fontsizes) * 2
        except ValueError as e:
            return 64


class ImageGenerator:
    def __init__(self, width=400, height=300):
        self.random = random.SystemRandom()
        self.width = width
        self.height = height
        self.sc = ScoreKeeper(width, height)
        self.msg = None
        self.position = None
        self.fontsize = None

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
            rows = self.sc[(x, y)]
            self.msg = msg
            self.position = (x, y)
            if rows.lastGuess:
                self.fontsize = score_function(rows) // 2
            else:
                self.fontsize = score_function(rows) * 2
            w, h = draw.textsize(msg, font=self.get_font())

            xc = x - w // 2
            yc = y - h // 2

            if self.width - w > xc and xc > 0 and self.height - h > yc and yc > 0:
                break

        draw.text((xc, yc), msg, (255, 255, 255), font=self.get_font())

    def update(self, msg_guess):
        if all((self.msg, self.position, self.fontsize)):
            self.sc[self.position].update(self.msg, msg_guess, self.fontsize)
        else:
            raise Exception("update called before generate_image")

    def get_font(self):
        return ImageFont.truetype("Inconsolata-g.ttf", self.fontsize)

    def print_results(self):
        for y in range(self.sc.vert_buckets):
            values = []
            for x in range(self.sc.horz_buckets):
                rows = self.sc.coordinate_lookup[x, y]
                values.append(str(score_function(rows)))
            print("\t".join(values))
