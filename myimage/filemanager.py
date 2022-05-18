from importlib import import_module

import PIL.Image
import PIL.ImageDraw

Image = import_module("." + __package__, __package__).Image
__all__ = ["load", "save"]


def invert_y(array):
    return list(reversed(array))


def transpose(array):
    return [[array[y][x] for y in range(len(array))] for x in range(len(array[0]))]


def load(path):
    image = PIL.Image.open(path).convert("RGB")
    size = image.size
    pixes = image.load()
    result = []
    for y in range(size[1]):
        result.append([pixes[x, y] for x in range(size[0])])
    return Image(transpose(invert_y(result)), size)


def save(image, path):
    size = image.size
    result = PIL.Image.new("RGB", size)
    draw = PIL.ImageDraw.Draw(result)
    for y in range(result.size[1]):
        for x in range(result.size[0]):
            draw.point((x, y), image[x][size[1] - 1 - y])
    result.save(path)
