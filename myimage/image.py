from .array2d import Array2d

class Image:
    def __init__(self, pixels, size):
        if not isinstance(pixels, Array2d):
            pixels = Array2d(pixels)
        self.size = size
        self.pixels = pixels

    def get(self, x, y, default=None):
        try:
            return self.pixels[x][y]
        except Exception:
            return default

    def __getitem__(self, indexes):
        return self.pixels[indexes]

    def __setitem__(self, indexes, value):
        x, y = indexes
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            self.pixels[x][y] = value

    def __repr__(self):
        return f"{__class__}(self.pixels, self.size)"
