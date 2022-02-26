from itertools import product

class OctreeNode:
    def __init__(self):
        self.children = set()

    def push(self, minimum, supremum, point):
        if isinstance(self.children, set):
            self.children.add(point)
            self.update_depth(minimum, supremum)
            return
        x, y, z = point
        x0, y0, z0 = minimum
        x2, y2, z2 = supremum
        x1, y1, z1 = ((x0 + x2) // 2 for x0, x2 in zip(minimum, supremum))
        child = (int(x >= x1), int(y >= y1), int(z >= z1))
        x0, y0, z0 = [x0, x1][child[0]], [y0, y1][child[1]], [z0, z1][child[2]]
        x2, y2, z2 = [x1, x2][child[0]], [y1, y2][child[1]], [z1, z2][child[2]]
        self.children[child].push((x0, y0, z0), (x2, y2, z2), (x, y, z))

    def update_depth(self, minimum, supremum):
        if len(self.children) <= 8:
            return
        points = self.children
        self.children = {p : OctreeNode() for p in product(range(2), repeat=3)}
        for point in points:
            self.push(minimum, supremum, point)
