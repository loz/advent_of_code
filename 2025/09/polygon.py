from typing import List, Tuple

def is_rect_inside_polygon(
    rect: Tuple[int, int, int, int],           # (x1, y1, x2, y2)  top-left → bottom-right
    polygon: List[Tuple[int, int]]             # closed or not – works either way
) -> bool:
    """
    Returns True if the axis-aligned rectangle is completely inside
    or touching the polygon (inclusive of boundary).
    Pure Python, integer only, no dependencies.
    """
    x1, y1, x2, y2 = rect
    if x1 >= x2 or y1 >= y2:
        return False

    # Ensure polygon is treated as closed
    poly = polygon if polygon[0] == polygon[-1] else polygon + [polygon[0]]
    n = len(poly) - 1  # last point == first

    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    # 1. All four corners must be inside or on boundary
    if not all(_point_in_poly_inclusive(c, poly, n) for c in corners):
        return False

    # 2. No polygon edge may PROPERLY cross any rectangle edge
    rect_edges = [
        ((x1, y1), (x2, y1)),
        ((x2, y1), (x2, y2)),
        ((x2, y2), (x1, y2)),
        ((x1, y2), (x1, y1)),
    ]

    for i in range(n):
        a = poly[i]
        b = poly[i + 1]
        for c, d in rect_edges:
            if _edges_cross_proper(a, b, c, d):
                return False

    return True


# ─────────────────────────────────────────────────────────────────────────────
# Robust inclusive point-in-polygon (handles boundary perfectly)
# ─────────────────────────────────────────────────────────────────────────────
def _point_in_poly_inclusive(pt: Tuple[int, int], poly: List[Tuple[int, int]], n: int) -> bool:
    x, y = pt

    # 1. Quick boundary check: vertex or on edge
    for i in range(n):
        a = poly[i]
        b = poly[i + 1]

        if pt == a or pt == b:
            return True

        # Bounding box early skip
        if not (min(a[0], b[0]) <= x <= max(a[0], b[0]) and
                min(a[1], b[1]) <= y <= max(a[1], b[1])):
            continue

        # Horizontal or vertical edge
        if a[1] == b[1] == y or a[0] == b[0] == x:
            return True

        # General on-segment test (cross product == 0 and dot in range)
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        cross = dx * (y - a[1]) - dy * (x - a[0])
        if cross != 0:
            continue
        dot = dx * (x - a[0]) + dy * (y - a[1])
        if 0 <= dot <= dx*dx + dy*dy:
            return True

    # 2. Ray-casting (count crossings to the right)
    inside = False
    j = n - 1
    for i in range(n):
        a = poly[i]
        b = poly[j]
        if ((a[1] > y) != (b[1] > y)) and \
           (x < a[0] + (b[0] - a[0]) * (y - a[1]) // (b[1] - a[1] + (b[1] == a[1]))):
            inside = not inside
        j = i
    return inside


# ─────────────────────────────────────────────────────────────────────────────
# Proper edge crossing (ignores touching at endpoints → inclusive)
# ─────────────────────────────────────────────────────────────────────────────
def _edges_cross_proper(a1, a2, b1, b2):
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    different1 = ccw(a1, b1, b2) != ccw(a2, b1, b2)
    different2 = ccw(a1, a2, b1) != ccw(a1, a2, b2)
    if not (different1 and different2):
        return False

    # If they only touch at endpoint → not a "proper" cross → allowed
    if a1 in (b1, b2) or a2 in (b1, b2) or b1 in (a1, a2) or b2 in (a1, a2):
        return False

    return True
