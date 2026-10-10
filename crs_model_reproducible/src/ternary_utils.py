import numpy as np

SQRT3_2 = np.sqrt(3) / 2

def bary_to_xy(rC, rR, rS):
    """Barycentric (C top, R bottom-left, S bottom-right) -> Cartesian for plotting."""
    x = 0.5 * (2 * rS + rC) / (rC + rR + rS)
    y = SQRT3_2 * rC / (rC + rR + rS)
    return x, y

def simplex_grid(n):
    """Generate a triangular grid of (rC, rR, rS) with rC+rR+rS=1, resolution n."""
    pts = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            k = n - i - j
            pts.append((i / n, j / n, k / n))
    return np.array(pts)  # columns: C, R, S
