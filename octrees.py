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

    def get_preleafs(self):
        if isinstance(self.children, set):
            return
        if all(isinstance(c.children, set) for c in self.children):
            yield self
            return
        for child in self.children:
            yield from child.get_preleafs()

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


from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
    z: int
    def __add__(u, v):
        return Point(*(x + y for x, y in zip(u, v)))
    def __sub__(u, v):
        return Point(*(x - y for x, y in zip(u, v)))
    def __floordiv__(u, alpha):
        return Point(*(x // alpha for x in u))
    def __iter__(self):
        yield from (self.x, self.y, self.z)

import enum
class Nodes(enum.Enum):
    empty = 1
    inner = 2
    leaf = 3

import arenas
class OctreeDict:
    def __init__(self, minimum, supremum):
        self.minimum = Point(*minimum)
        self.supremum = Point(*supremum)
        self.inodes = arenas.Arena()
        self.leafs = arenas.Arena()
        self.root = [Nodes.empty, None]

    def __setitem__(self, p, value):
        if not isinstance(p, Point):
            p = Point(*p)
        x0, x2 = self.minimum, self.supremum
        node = self.root
        while node[0] is not Nodes.empty:
            x1 = (x2 + x0) // 2
            child = tuple(int(x >= y) for x, y in zip(p, x1))
            if node[0] is Nodes.leaf:
                if self.leafs[node[1]][0] == p:
                    self.leafs[node[1]][1] = value
                    return
                node[0] = Nodes.inner
                leaf1 = node[1]
                p1 = self.leafs[leaf1][0]
                child1 = tuple(int(x >= y) for x, y in zip(p1, x1))
                node[1] = self.inodes.push({child1: [Nodes.leaf, leaf1]})
            children = self.inodes[node[1]]
            if child not in children:
                children[child] = [Nodes.empty, None]
            x0 = Point(*([y0, y1][b] for y0, y1, b in zip(x0, x1, child)))
            x2 = Point(*([y0, y1][b] for y0, y1, b in zip(x1, x2, child)))
            node = children[child]
        node[0] = Nodes.leaf
        node[1] = self.leafs.push([p, value])

    def __contains__(self, p):
        if not isinstance(p, Point):
            p = Point(*p)
        x0, x2 = self.minimum, self.supremum
        node = self.root
        while node[0] is Nodes.inner:
            x1 = (x2 + x0) // 2
            child = tuple(int(x >= y) for x, y in zip(p, x1))
            children = self.inodes[node[1]]
            if child not in children:
                children[child] = [Nodes.empty, None]
            node = children[child]
        return node[0] is Nodes.leaf

    def __iter__(self):
        for leaf in self.leafs:
            yield leaf
