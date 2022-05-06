from contextlib import suppress
from random import choices, randint
from .array2d import Array2d
from .image import Image

__all__ = ["dithering"]
DITHERING_METHODS = {}
dithering_method = lambda name: lambda f: DITHERING_METHODS.setdefault(name, f)


def ilog(number, base=2):
    result = 0
    y = 1
    while number > y:
        result += 1
        y *= base
    return result


def bits(number, bit_length=None):
    bit_length = number.bit_length() if bit_length is None else bit_length
    bits = bin(number)[2:].rjust(bit_length, "0")
    return map(int, bits)


def threshold(x, y, lvl):
    b = [x * 2 + y for x, y in zip(bits(x ^ y, lvl), bits(y, lvl))]
    return sum(x * 4 ** i for i, x in enumerate(b))


def generate_threshold_map(lvl):
    line = list(range(2 ** lvl))
    return [[threshold(x, y, lvl) for x in line] for y in line]


def gray(color):
    return (max(color) + min(color)) // 2
    return sum(color) // 3


def dithering(image, method):
    return DITHERING_METHODS[method](image)


@dithering_method("logic")
def zero_dithering(image):
    width, height = image.size
    result = [[None] * height for x in range(width)]
    for y in range(height):
        for x in range(width):
            color = gray(image[x, y])
            target_color = (color >= 128) * 255
            result[x][y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("random")
def random_dithering(image):
    width, height = image.size
    result = [[None] * height for x in range(width)]
    for y in range(height):
        for x in range(width):
            color = gray(image[x, y])
            target_color = choices((255, 0), (color, 255 - color))[0]
            result[x][y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("randomshift")
def randomshift_dithering(image):
    width, height = image.size
    result = [[None] * height for x in range(width)]
    for y in range(height):
        for x in range(width):
            color = gray(image[x, y])
            target_color = (color + randint(-128, 128) >= 128) * 255
            result[x][y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("linear")
def linear_dithering(image):
    width, height = image.size
    result = [[None] * height for x in range(width)]
    for y in range(height):
        error = 0
        for x in range(width):
            color = gray(image[x, y]) + error
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x][y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("FS")
def Floyd_Steinberg_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + result[x][y]
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y - 0] += error * 7 / 16
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 3 / 16
            with suppress(IndexError):
                result[x + 0, y - 1] += error * 5 / 16
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 1 / 16
    return Image(result, (width, height))