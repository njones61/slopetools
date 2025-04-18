from shapely.geometry import LineString, Point

def build_ground_surface(profile_lines):
    """
    Constructs the topmost ground surface LineString from a set of profile lines.

    The function:
    1. Collects all (x, y) points from the input profile lines.
    2. Keeps the highest y-value for each unique x-coordinate.
    3. Filters these points by ensuring they are not exceeded in elevation by any other profile line at the same x.
    4. Returns a LineString representing the visible ground surface.

    Parameters:
        profile_lines (list of list of tuple): A list of profile lines, each represented
            as a list of (x, y) coordinate tuples.

    Returns:
        shapely.geometry.LineString: A LineString of the top surface, or an empty LineString
        if fewer than two valid points are found.

    Notes:
        - Excludes points that would result in extrapolation during line intersection checks.
        - Ensures the result reflects the outermost (visible) surface in multi-layered profiles.
    """

    # Step 1: Gather all points and sort by x, then by descending y
    all_points = sorted(set(pt for line in profile_lines for pt in line), key=lambda p: (p[0], -p[1]))

    # Step 2: Keep only the highest y for each x
    top_candidates = {}
    for x, y in all_points:
        if x not in top_candidates or y > top_candidates[x]:
            top_candidates[x] = y

    # Step 3: For each top candidate, check that it's higher than all other lines
    top_surface_points = []
    for x, y in sorted(top_candidates.items()):
        keep = True
        for other_line in profile_lines:
            line = LineString(other_line)
            if line.length == 0:
                continue
            proj = line.project(Point(x, 0))
            if proj == 0 or proj == line.length:
                continue  # avoid extrapolation
            ipt = line.interpolate(proj)
            if ipt.y > y + 1e-6:
                keep = False
                break
        if keep:
            top_surface_points.append((x, y))

    return LineString(top_surface_points) if len(top_surface_points) >= 2 else LineString([])
