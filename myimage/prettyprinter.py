__all__ = ["show"]

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


def show(image):
    for y in range(image.size - 1, -1, -1):
        for x in range(image.size):
            r, g, b = image[x, y]
            print(end=colored(r, g, b, "#"))
        print()
