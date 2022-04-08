def square2tree(pixels):
    pixels = [line.copy() for line in pixels]
    w = len(pixels)
    real_colors = list(
        sorted({pixels[x][y] for y in range(w) for x in range(w)})
    )
    colors = {color: i for i, color in enumerate(real_colors)}
    for y in range(w):
        for x in range(w):
            pixels[x][y] = colors[pixels[x][y]]
    colors = {(i, i, i, i): i for i, color in enumerate(real_colors)}
    for _ in range(1, w.bit_length()):
        new_image = [[None] * w for _ in range(w)]
        for y in range(0, w, 2):
            for x in range(0, w, 2):
                color = (
                    pixels[x][y],
                    pixels[x + 1][y],
                    pixels[x][y + 1],
                    pixels[x + 1][y + 1],
                )
                if color not in colors:
                    colors[color] = len(colors)
                new_image[x // 2][y // 2] = colors[color]
        pixels = new_image

    tree = [color for color, _ in colors.items()]
    tree = [col for _, col in sorted((i, color) for color, i in colors.items())]
    return real_colors, tree, pixels[0][0]
