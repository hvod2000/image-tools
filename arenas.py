class Arena:
    def __init__(self):
        self.counter = 0
        self.content = {}

    def push(self, value):
        ind = self.counter
        self.content[ind] = value
        self.counter += 1
        return ind

    def __getitem__(self, ind):
        return self.content[ind]

    def __setitem__(self, ind, value):
        self.content[ind] = value

    def __len__(self):
        return len(self.content)

    def __delitem__(self, ind):
        del self.content[ind]
