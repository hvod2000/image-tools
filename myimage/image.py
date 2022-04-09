class Image:
    def __init__(self, pixels, size):
        self.size = size
        self.pixels = pixels

    def __getitem__(self, indexes):
        x, y = indexes
        return self.pixels[x][y]

    def __repr__(self):
        return f"{__class__}(self.pixels, self.size)"
