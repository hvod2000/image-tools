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

    def __iter__(self):
        pixels = self.content.load()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield (x, y, pixels[x, y])
