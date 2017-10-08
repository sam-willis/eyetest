import dill as pickle
from collections import defaultdict


class ScoreKeeper:
    def __init__(self,
                 width,
                 height,
                 horz_buckets=2,
                 vert_buckets=2,
                 saveFile="save.obj"):
        self.horz_buckets = horz_buckets
        self.vert_buckets = vert_buckets
        self.nx = width // horz_buckets
        self.ny = height // vert_buckets
        self.saveFile = saveFile
        try:
            self.load()
        except FileNotFoundError:
            self.coordinate_lookup = defaultdict(lambda: Rows(self))

    def __getitem__(self, key):
        x, y = key
        return self.coordinate_lookup[(x // self.nx, y // self.ny)]

    def save(self):
        with open(self.saveFile, mode='wb') as file:
            pickle.dump(self.coordinate_lookup, file)

    def load(self):
        with open(self.saveFile, mode='rb') as file:
            self.coordinate_lookup = pickle.load(file)


class Rows:
    def __init__(self, scoreKeeper):
        self.lastGuess = False
        self.rows = []
        self.fontsizes = set()
        self.sc = scoreKeeper

    def update(self, letter, guess, fontsize):
        self.fontsizes.add(fontsize)
        self.rows.append(Row(letter, guess, fontsize))
        if letter == guess:
            self.lastGuess = True
        else:
            self.lastGuess = False
        self.sc.save()

    def __iter__(self):
        return self.rows.__iter__()


class Row:
    def __init__(self, letter, guess, fontsize):
        self.letter = letter
        self.guess = guess
        self.fontsize = fontsize
