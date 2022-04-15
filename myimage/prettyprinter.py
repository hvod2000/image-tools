__all__ = ["show"]


def str_column(lower, upper):
    upper = "" if upper is None else "\033[48;2;{};{};{}m".format(*upper)
    lower = "" if lower is None else "\033[38;2;{};{};{}m".format(*lower)
    return upper + lower + "▄" + "\033[0m"


def show(image):
    width, height = image.size
    for y in range((height + 1) // 2 * 2 - 1, 0, -2):
        for x in range(width):
            print(end=str_column(image.get(x, y - 1), image.get(x, y)))
        print()
