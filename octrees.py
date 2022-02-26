from itertools import product

class OctreeNode:
    def __init__(self):
        self.children = set()

    def find_node(self, minimum, supremum, point):
        if isinstance(self.children, set):
            return self
        x, y, z = point
        x0, y0, z0 = minimum
        x2, y2, z2 = supremum
        x1, y1, z1 = ((x0 + x2) // 2 for x0, x2 in zip(minimum, supremum))
        child = (int(x >= x1), int(y >= y1), int(z >= z1))
        x0, y0, z0 = [x0, x1][child[0]], [y0, y1][child[1]], [z0, z1][child[2]]
        x2, y2, z2 = [x1, x2][child[0]], [y1, y2][child[1]], [z1, z2][child[2]]
        return self.children[child].find_node((x0, y0, z0), (x2, y2, z2), point)

    def push(self, minimum, supremum, point):
        node = self.find_node(minimum, supremum, point)
        node.children.add(point)
        node.update_depth(minimum, supremum)

    def update_depth(self, minimum, supremum):
        if len(self.children) <= 8:
            return
        points = self.children
        self.children = {p : OctreeNode() for p in product(range(2), repeat=3)}
        for point in points:
            self.push(minimum, supremum, point)

    def contains(self, minimum, supremum, point):
        node = self.find_node(minimum, supremum, point)
        return point in node.children

    def __iter__(self):
        if isinstance(self.children, set):
            yield from self.children
        else:
            for child in self.children.values():
                yield from child

class Octree:
    def __init__(self, minimum, supremum, points=()):
        self.root = OctreeNode()
        self.minimum = minimum
        self.supremum = supremum
        for point in points:
            self.push(point)

    def push(self, p):
        self.root.push(self.minimum, self.supremum, p)

    def __contains__(self, p):
        return self.root.contains(self.minimum, self.supremum, p)

    def __iter__(self):
        yield from self.root
