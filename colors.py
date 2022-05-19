from fractions import Fraction


def str2mat(txt):
    mat = [r.split(",") for r in txt.strip().split("\n")]
    return [[Fraction(c.replace(" ", "")) for c in r] for r in mat]


rgb2xyz_matrix = str2mat(
    """
    33786752 / 81924984, 29295110 / 81924984,  14783675 / 81924984
    8710647 / 40962492,  29295110 / 40962492,  2956735 / 40962492
    4751262 / 245774952, 29295110 / 245774952, 233582065 / 245774952
"""
)
xyz2rgb_matrix = str2mat(
    """
    4277208 / 1319795,    -2028932 / 1319795,   -658032 / 1319795
    -70985202 / 73237775, 137391598 / 73237775, 3043398 / 73237775
    164508 / 2956735,     -603196 / 2956735,    3125652 / 2956735
"""
)


def matmul(m, x):
    return tuple(sum(a * b for a, b in zip(r, x)) for r in m)


rgb2xyz = lambda r, g, b: matmul(rgb2xyz_matrix, (r, g, b))
xyz2rgb = lambda x, y, z: matmul(xyz2rgb_matrix, (x, y, z))
