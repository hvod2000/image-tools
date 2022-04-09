__all__ = ["show"]


def str_column(lower, upper):
    r0, g0, b0 = lower
    r1, g1, b1 = upper
    result = "\033[38;2;{};{};{}m".format(r1, g1, b1)
    result += "\033[48;2;{};{};{}m".format(r0, g0, b0)
    result += "▀"
    result += "\033[0m"
    return result


def show(image):
    for y in range((image.size - 1) // 2 * 2 - 1, -1, -2):
        for x in range(image.size):
            print(end=str_column(image[x, y], image[x, y + 1]))
        print()
