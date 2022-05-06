class Array2d:
    def __init__(self, iterable):
        array = [list(row) for row in iterable]
        self.size = (len(array), len(array[0]))
        self.content = array

    def __getitem__(self, indexes):
        match indexes:
            case int(x) if 0 <= x < self.size[0]:
                return self.content[x]
            case (x, y) if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
                return self.content[x][y]
            case _:
                raise IndexError(repr(indexes))

    def __setitem__(self, indexes, value):
        x, y = indexes
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            self.content[x][y] = value

    def __repr__(self):
        return f"{__class__}(self.content)"
