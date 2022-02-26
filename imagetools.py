import PIL.Image, PIL.ImageDraw
from math import inf, dist
from kmeans_clustering import kmeans

def number2hex(number, size=2):
    return hex(number)[2:].rjust(2, '0')

def color2hex(color):
    return ''.join(map(number2hex, color))

class Image:
    def __init__(self, content, palette=None):
        self.size = content.size
        self.content = content
        self.palette = palette

    @staticmethod
    def load(path):
        return Image(PIL.Image.open(path))

    def save(self, path, file_format="PNG"):
        self.content.save(path, file_format)

    def resize(self, size):
        result = PIL.Image.new("RGB", size)
        draw = PIL.ImageDraw.Draw(result)
        old_pixels = self.content.load()
        for y in range(result.size[1]):
            y_old = round(y * self.size[1] / result.size[1])
            for x in range(result.size[0]):
                x_old = round(x * self.size[0] / result.size[0])
                draw.point((x, y), old_pixels[x_old, y_old])
        return Image(result, self.palette)

    def pixelize(self, size, radius=3):
        result = PIL.Image.new("RGB", size)
        draw = PIL.ImageDraw.Draw(result)
        old_pixels = self.content.load()
        radius = min(radius, min(int(self.size[i] / result.size[i] / 2 - 0.5) for i in range(2)))
        for y in range(result.size[1]):
            y_old = int((y + 0.5) * self.size[1] / result.size[1])
            for x in range(result.size[0]):
                x_old = int((x + 0.5) * self.size[0] / result.size[0] + 0.5)
                colors = []
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        colors.append(old_pixels[x_old + dx, y_old + dy])
                new_color = tuple(round(sum(c[i] for c in colors) / len(colors)) for i in range(len(colors[0])))
                draw.point((x, y), new_color)
        return Image(result, self.palette)

    def smooth_resize(self, size):
        return pixelize(self, size)

    def apply_the_palette(self, palette):
        result = PIL.Image.new("RGB", self.size)
        draw = PIL.ImageDraw.Draw(result)
        old_pixels = self.content.load()
        for y in range(result.size[1]):
            for x in range(result.size[0]):
                pixel = old_pixels[x, y]
                closest_color = None
                min_dist = inf
                for color_name, color in palette.items():
                    current_dist = dist(pixel, color)
                    if current_dist < min_dist:
                        closest_color = color_name
                        min_dist = current_dist
                draw.point((x, y), palette[closest_color])
        return Image(result, palette)

    def create_palette_using_kmeans(self, palette_size):
        import random
        colors = []
        pixels = self.content.load()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                colors.append(pixels[x, y])
        random.shuffle(colors)
        return {f'color{number}': color for number, color in enumerate(tuple(max(min(round(x), 255), 0) for x in color) for color in kmeans(colors, palette_size))}

    def create_palette(self, palette_size = None):
        if palette_size:
            return self.create_palette_using_kmeans(palette_size)
        colors = set()
        pixels = self.content.load()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                colors.add(pixels[x, y])
        return {f'color{i}':c for i, c in enumerate(colors)}

    def to_css(self):
        assert self.palette
        colors = list(sorted(self.palette.items()))
        result = []
        for color_name, color in colors:
            result.append(f'table.pixelart *.{color_name} ' + '{')
            result.append(f'\tbackground-color: #{color2hex(color)};')
            result.append('}')
        return '\n'.join(result)

    def to_html(self):
        assert self.palette
        color2name = {rgb: color_name for color_name, rgb in self.palette.items()}
        pixels = self.content.load()
        result = ['<table class=pixelart>']
        for y in range(self.size[1]):
            row_color = color2name[pixels[0, y]]
            result.append(f'\t<tr class="{row_color}">')
            for x in range(self.size[0]):
                color = color2name[pixels[x, y]]
                if color != row_color:
                    result.append(f'\t\t<td class="{color}" />')
                else:
                    result.append(f'\t\t<td/>')
            result.append('\t</tr>')
        result.append('</table>')
        return '\n'.join(result)

    def __iter__(self):
        pixels = self.content.load()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield (x, y, pixels[x, y])
