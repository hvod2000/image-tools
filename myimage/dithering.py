from contextlib import suppress
from random import choices, randint, shuffle
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


def random_threshold_map():
    m = list(range(256))
    shuffle(m)
    return [[m[y * 16 + x] for x in range(16)] for y in range(16)]


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


@dithering_method("JJN")
def Jarvis_Judice_Nink_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 24) // 48
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error * 7
            with suppress(IndexError):
                result[x + 2, y + 0] += error * 5
            with suppress(IndexError):
                result[x - 2, y - 1] += error * 3
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 5
            with suppress(IndexError):
                result[x + 0, y - 1] += error * 7
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 5
            with suppress(IndexError):
                result[x + 2, y - 1] += error * 3
            with suppress(IndexError):
                result[x - 2, y - 2] += error * 1
            with suppress(IndexError):
                result[x - 1, y - 2] += error * 3
            with suppress(IndexError):
                result[x + 0, y - 2] += error * 5
            with suppress(IndexError):
                result[x + 1, y - 2] += error * 3
            with suppress(IndexError):
                result[x + 2, y - 2] += error * 1
    return Image(result, (width, height))


@dithering_method("Stucki")
def Stucki_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 21) // 42
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error * 8
            with suppress(IndexError):
                result[x + 2, y + 0] += error * 4
            with suppress(IndexError):
                result[x - 2, y - 1] += error * 2
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 4
            with suppress(IndexError):
                result[x + 0, y - 1] += error * 8
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 4
            with suppress(IndexError):
                result[x + 2, y - 1] += error * 2
            with suppress(IndexError):
                result[x - 2, y - 2] += error * 1
            with suppress(IndexError):
                result[x - 1, y - 2] += error * 2
            with suppress(IndexError):
                result[x + 0, y - 2] += error * 4
            with suppress(IndexError):
                result[x + 1, y - 2] += error * 2
            with suppress(IndexError):
                result[x + 2, y - 2] += error * 1
    return Image(result, (width, height))


@dithering_method("Stevenson-Arce")
def Stevenson_Arce_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 100) // 200
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 2, y + 0] += error * 32
            with suppress(IndexError):
                result[x - 3, y - 1] += error * 12
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 26
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 30
            with suppress(IndexError):
                result[x + 3, y - 1] += error * 16
            with suppress(IndexError):
                result[x - 2, y - 2] += error * 12
            with suppress(IndexError):
                result[x - 0, y - 2] += error * 26
            with suppress(IndexError):
                result[x + 2, y - 2] += error * 12
            with suppress(IndexError):
                result[x - 3, y - 3] += error * 5
            with suppress(IndexError):
                result[x - 1, y - 3] += error * 12
            with suppress(IndexError):
                result[x + 1, y - 3] += error * 12
            with suppress(IndexError):
                result[x + 3, y - 3] += error * 5
    return Image(result, (width, height))


@dithering_method("Atkinson")
def Atkinson_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 4) // 8
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error
            with suppress(IndexError):
                result[x + 2, y + 0] += error
            # with suppress(IndexError): result[x - 2, y - 1] += error
            with suppress(IndexError):
                result[x - 1, y - 1] += error
            with suppress(IndexError):
                result[x + 0, y - 1] += error
            with suppress(IndexError):
                result[x + 1, y - 1] += error
            # with suppress(IndexError): result[x + 2, y - 1] += error
            # with suppress(IndexError): result[x - 2, y - 2] += error
            # with suppress(IndexError): result[x - 1, y - 2] += error
            with suppress(IndexError):
                result[x + 0, y - 2] += error
            # with suppress(IndexError): result[x + 1, y - 2] += error
            # with suppress(IndexError): result[x + 2, y - 2] += error
    return Image(result, (width, height))


@dithering_method("Burkes")
def Burkes_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 16) // 32
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error * 8
            with suppress(IndexError):
                result[x + 2, y + 0] += error * 4
            with suppress(IndexError):
                result[x - 2, y - 1] += error * 2
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 4
            with suppress(IndexError):
                result[x + 0, y - 1] += error * 8
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 4
            with suppress(IndexError):
                result[x + 2, y - 1] += error * 2
    return Image(result, (width, height))


@dithering_method("Sierra-3")
def Sierra_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 16) // 32
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error * 5
            with suppress(IndexError):
                result[x + 2, y + 0] += error * 3
            with suppress(IndexError):
                result[x - 2, y - 1] += error * 2
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 4
            with suppress(IndexError):
                result[x + 0, y - 1] += error * 5
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 4
            with suppress(IndexError):
                result[x + 2, y - 1] += error * 2
            with suppress(IndexError):
                result[x - 2, y - 2] += error * 0
            with suppress(IndexError):
                result[x - 1, y - 2] += error * 2
            with suppress(IndexError):
                result[x + 0, y - 2] += error * 3
            with suppress(IndexError):
                result[x + 1, y - 2] += error * 2
            with suppress(IndexError):
                result[x + 2, y - 2] += error * 0
    return Image(result, (width, height))


@dithering_method("Sierra-2")
def tworow_Sierra_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 8) // 16
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error * 4
            with suppress(IndexError):
                result[x + 2, y + 0] += error * 3
            with suppress(IndexError):
                result[x - 2, y - 1] += error * 1
            with suppress(IndexError):
                result[x - 1, y - 1] += error * 2
            with suppress(IndexError):
                result[x + 0, y - 1] += error * 3
            with suppress(IndexError):
                result[x + 1, y - 1] += error * 2
            with suppress(IndexError):
                result[x + 2, y - 1] += error * 1
            with suppress(IndexError):
                result[x - 2, y - 2] += error * 0
            with suppress(IndexError):
                result[x - 1, y - 2] += error * 0
            with suppress(IndexError):
                result[x + 0, y - 2] += error * 0
            with suppress(IndexError):
                result[x + 1, y - 2] += error * 0
            with suppress(IndexError):
                result[x + 2, y - 2] += error * 0
    return Image(result, (width, height))


@dithering_method("Sierra-1")
def Sierra_lite_dithering(image):
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) + (result[x, y] + 2) // 4
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            with suppress(IndexError):
                result[x + 1, y + 0] += error * 2
            with suppress(IndexError):
                result[x - 1, y - 1] += error
            with suppress(IndexError):
                result[x + 0, y - 1] += error
    return Image(result, (width, height))


@dithering_method("ordered-2")
def dithering_by_threshold_map_2(image):
    threshold_map = [[0, 2], [3, 1]]
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) / 256 * len(threshold_map) ** 2
            target_color = (color > threshold_map[x % 2][y % 2]) * 255
            result[x, y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("ordered-4")
def dithering_by_threshold_map_4(image):
    threshold_map = [
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5],
    ]
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) / 256 * len(threshold_map) ** 2
            target_color = (color > threshold_map[x % 4][y % 4]) * 255
            result[x, y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("ordered-8")
def dithering_by_threshold_map_8(image):
    threshold_map = [
        [0, 48, 12, 60, 3, 51, 15, 63],
        [32, 16, 44, 28, 35, 19, 47, 31],
        [8, 56, 4, 52, 11, 59, 7, 55],
        [40, 24, 36, 20, 43, 27, 39, 23],
        [2, 50, 14, 62, 1, 49, 13, 61],
        [34, 18, 46, 30, 33, 17, 45, 29],
        [10, 58, 6, 54, 9, 57, 5, 53],
        [42, 26, 38, 22, 41, 25, 37, 21],
    ]
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) / 256 * len(threshold_map) ** 2
            target_color = (color > threshold_map[x % 8][y % 8]) * 255
            result[x, y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("ordered-16")
def dithering_by_threshold_map_16(image):
    threshold_map = generate_threshold_map(4)
    width, height = image.size
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = gray(image[x, y]) / 256 * len(threshold_map) ** 2
            target_color = (color > threshold_map[x % 16][y % 16]) * 255
            result[x, y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("randompattern")
def randompattern_dithering(image):
    width, height = image.size
    threshold_maps = (width + 15) // 16 * ((height + 15) // 16)
    threshold_maps = [random_threshold_map() for _ in range(threshold_maps)]
    result = Array2d([[0] * height for x in range(width)])
    for y in range(height - 1, -1, -1):
        for x in range(width):
            threshold_map = threshold_maps[x // 16 + (y // 16) * 16]
            color = gray(image[x, y]) / 256 * len(threshold_map) ** 2
            target_color = (color > threshold_map[x % 16][y % 16]) * 255
            result[x, y] = (target_color,) * 3
    return Image(result, (width, height))


@dithering_method("recursive")
def recursive_error_propagation_dithering(image):
    def rec(x, y, lvl, error):
        if lvl == -1:
            try:
                color = gray(image[x, y]) + error
            except IndexError:
                return error
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            return error
        error = rec(x, y, lvl - 1, error)
        error = rec(x + 2 ** lvl, y, lvl - 1, error)
        error = rec(x + 2 ** lvl, y + 2 ** lvl, lvl - 1, error)
        error = rec(x, y + 2 ** lvl, lvl - 1, error)
        return error

    width, height = image.size
    result = Array2d((image[x, y] for y in range(height)) for x in range(width))
    rec(0, 0, max(ilog(width), ilog(height)), 0)
    return Image(result, (width, height))


@dithering_method("recursive-2")
def recursive_two_row_error_propagation_dithering(image):
    def rec(x, y, lvl, error):
        if lvl == -1:
            try:
                color = gray(image[x, y]) + error
            except IndexError:
                return error
            target_color = (color >= 128) * 255
            error = color - target_color
            result[x, y] = (target_color,) * 3
            return error
        err1 = rec(x, y, lvl - 1, error)
        err2 = rec(x + 2 ** lvl, y, lvl - 1, err1 // 2)
        err3 = rec(x, y + 2 ** lvl, lvl - 1, err1 // 2)
        err4 = rec(x + 2 ** lvl, y + 2 ** lvl, lvl - 1, err2 + err3)
        return err4

    width, height = image.size
    result = Array2d((image[x, y] for y in range(height)) for x in range(width))
    rec(0, 0, max(ilog(width), ilog(height)), 0)
    return Image(result, (width, height))
