def hilbert(level):
    path, rules = "A", {"A": "+BF-AFA-FB+", "B": "-AF+BFB+FA-"}
    for _ in range(level):
        path = "".join(rules.get(ch, ch) for ch in path)
    pos, drn = (0, 0), (1, 0)
    yield pos
    for cmd in path:
        match cmd:
            case rotation if rotation in "+-":
                drn = (
                    (-drn[1], drn[0]) if rotation == "+" else (drn[1], -drn[0])
                )
            case "F":
                pos = tuple(map(sum, zip(pos, drn)))
                yield pos
