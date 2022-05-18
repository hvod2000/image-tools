from importlib import import_module
Image = import_module("." + __package__, __package__).Image
__all__ = ["to_tree", "from_tree"]


class Quadtree:
    def __init__(self, colors, tiles, size):
        self.colors = colors
        self.tiles = tiles
        self.size = size

    def __repr__(self):
        return f"Quadtree({repr(self.tree)}, {repr(self.size)})"


def to_tree(image):
    pixels, w = image.pixels, min(image.size)
    colors = list(sorted({pixels[x][y] for y in range(w) for x in range(w)}))
    tiles = {(i, i, i, i): i for i in range(len(colors))}
    color2ind = {color: i for i, color in enumerate(colors)}
    tilemap = [[color2ind[pixels[x][y]] for x in range(w)] for y in range(w)]
    for k in range(w.bit_length() - 1):
        new_tilemap = [[None] * w for _ in range(w)]
        for x in range(0, w >> k, 2):
            for y in range(0, w >> k, 2):
                tile = (
                    tilemap[x][y],
                    tilemap[x + 1][y],
                    tilemap[x][y + 1],
                    tilemap[x + 1][y + 1],
                )
                if tile not in tiles:
                    tiles[tile] = len(tiles)
                new_tilemap[x // 2][y // 2] = tiles[tile]
        tilemap = new_tilemap
    assert tilemap[0][0] == len(tiles) - 1
    return Quadtree(colors, list(tiles)[len(colors) :], w)


def from_tree(tree):
    colors, tiles, size = tree.colors, tree.tiles, tree.size
    tiles = [(i, i, i, i) for i in range(len(colors))] + tiles
    result = [[None] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            ind = -1
            for k in range(size.bit_length() - 2, -1, -1):
                ind = tiles[ind][((x >> k) & 1) + 2 * ((y >> k) & 1)]
            result[y][x] = colors[ind]
    return Image(result, (len(result), len(result)))
