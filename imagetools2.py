def invert_y(array):
    return list(reversed(array))


def traspose(array):
    return [
        [array[y][x] for y in range(len(array))] for x in range(len(array[0]))
    ]


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


class Image:
    def __init__(self, pixels, size=None):
        if size is None:
            size = len(pixels)
            pixels = traspose(invert_y(pixels))
        self.size = size
        self.pixels = pixels

    def show(self):
        for y in range(self.size - 1, -1, -1):
            for x in range(self.size):
                r, g, b = self[x, y]
                print(end=colored(r, g, b, "#"))
            print()

    def __getitem__(self, indexes):
        x, y = indexes
        return self.pixels[x][y]
