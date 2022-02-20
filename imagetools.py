import PIL.Image, PIL.ImageDraw

class Image:
    def __init__(self, content, palette=None):
        self.size = content.size
        self.content = content

    @staticmethod
    def load(path):
        return Image(PIL.Image.open(path))

    def save(self, path, file_format='PNG'):
        self.content.save(path, file_format)

    def resize(self, size):
        result = PIL.Image.new('RGB', size)
        draw = PIL.ImageDraw.Draw(result)
        old_pixels = self.content.load()
        for y in range(result.size[1]):
            y_old = round(y * self.size[1] / result.size[1])
            for x in range(result.size[0]):
                x_old = round(x * self.size[0] / result.size[0])
                draw.point((x, y), old_pixels[x_old, y_old])
        return Image(result)

    def __iter__(self):
        pixels = self.content.load()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield (x, y, pixels[x, y])
