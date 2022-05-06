from .image import Image

__all__ = ["dithering"]
DITHERING_METHODS = {}
dithering_method = lambda name: lambda f: DITHERING_METHODS.setdefault(name, f)


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
