import pandas as pd
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



def load_globals(filepath):
    """
    This function reads input data from various Excel sheets and parses it into
    structured components used throughout the slope stability analysis framework.
    It handles circular and non-circular failure surface data, reinforcement, piezometric
    lines, and distributed loads.

    Validation is enforced to ensure required geometry and material information is present:
    - Circular failure surface: must contain at least one valid row with Xo and Yo
    - Non-circular failure surface: required if no circular data is provided
    - Profile lines: must contain at least one valid set, and each line must have ≥ 2 points
    - Materials: must match the number of profile lines
    - Piezometric line: only included if it contains ≥ 2 valid rows
    - Distributed loads and reinforcement: each block must contain ≥ 2 valid entries

    Raises:
        ValueError: if required inputs are missing or inconsistent.

    Returns:
        dict: Parsed and validated global data structure for analysis
    """

    xls = pd.ExcelFile(filepath)
    globals_data = {}

    # === STATIC GLOBALS ===
    main_df = xls.parse('main', header=None)

    try:
        gamma_water = float(main_df.iloc[15, 3])  # Excel row 16, column D
        tcrack_depth = float(main_df.iloc[16, 3])  # Excel row 17, column D
        tcrack_water = float(main_df.iloc[17, 3])  # Excel row 18, column D
        k_seismic = float(main_df.iloc[18, 3])  # Excel row 19, column D
    except Exception as e:
        raise ValueError(f"Error reading static global values from 'main' tab: {e}")


    # === PROFILE LINES ===
    profile_df = xls.parse('profile', header=None)
    profile_lines = []

    profile_data_blocks = [
        {"header_row": 2, "data_start": 3, "data_end": 18},
        {"header_row": 20, "data_start": 21, "data_end": 36}
    ]
    profile_block_width = 3

    for block in profile_data_blocks:
        for col in range(0, profile_df.shape[1], profile_block_width):
            x_col, y_col = col, col + 1
            try:
                x_header = str(profile_df.iloc[block["header_row"], x_col]).strip().lower()
                y_header = str(profile_df.iloc[block["header_row"], y_col]).strip().lower()
            except:
                continue
            if x_header != 'x' or y_header != 'y':
                continue
            data = profile_df.iloc[block["data_start"]:block["data_end"], [x_col, y_col]]
            data = data.dropna(how='all')
            if data.empty:
                continue
            if data.iloc[0].isna().any():
                continue
            coords = data.dropna().apply(lambda r: (float(r.iloc[0]), float(r.iloc[1])), axis=1).tolist()
            if len(coords) == 1:
                raise ValueError("Each profile line must contain at least two points.")
            if coords:
                profile_lines.append(coords)

    # === BUILD GROUND SURFACE FROM PROFILE LINES ===

    ground_surface = build_ground_surface(profile_lines)

    # === BUILD TENSILE CRACK LINE ===

    tcrack_surface = None
    if tcrack_depth > 0:
        tcrack_surface = LineString([(x, y - tcrack_depth) for (x, y) in ground_surface.coords])

    # === MATERIALS (Optimized Parsing) ===
    mat_df = xls.parse('mat', header=2)
    materials = []

    for _, row in mat_df.iterrows():
        gamma = row.get('g')
        option = str(row.get('option', '')).strip().lower()
        piezo = row.get('Piezo', 1.0)

        if pd.isna(gamma) or option not in ('mc', 'cp'):
            continue

        try:
            gamma = float(gamma)
            piezo = float(piezo) if pd.notna(piezo) else 1.0
        except:
            continue

        if option == 'mc':
            c = row.get('c')
            phi = row.get('f')
            if pd.isna(c) or pd.isna(phi):
                continue
            try:
                c = float(c)
                phi = float(phi)
            except:
                continue
            cp = 0
            r_elev = 0

        elif option == 'cp':
            cp = row.get('cp')
            r_elev = row.get('r-elev')
            if pd.isna(cp) or pd.isna(r_elev):
                continue
            try:
                cp = float(cp)
                r_elev = float(r_elev)
            except:
                continue
            c = 0
            phi = 0

        materials.append({
            "gamma": gamma,
            "option": option,
            "c": c,
            "phi": phi,
            "cp": cp,
            "r_elev": r_elev,
            "piezo": piezo,
            "sigma_gamma": float(row.get('s(g)', 0) or 0),
            "sigma_c": float(row.get('s(c)', 0) or 0),
            "sigma_phi": float(row.get('s(f)', 0) or 0),
            "sigma_cp": float(row.get('s(cp)', 0) or 0),
        })

    # === PIEZOMETRIC LINE ===
    piezo_df = xls.parse('piezo')
    piezo_data = piezo_df.iloc[2:].dropna(how='all')
    piezo_line = []

    if len(piezo_data) >= 2:
        try:
            piezo_data = piezo_data.dropna(subset=[piezo_data.columns[0], piezo_data.columns[1]], how='any')
            if len(piezo_data) < 2:
                raise ValueError("Piezometric line must contain at least two points.")
            piezo_line = piezo_data.apply(lambda row: (float(row.iloc[0]), float(row.iloc[1])), axis=1).tolist()
        except Exception:
            raise ValueError("Invalid piezometric line format.")
    elif len(piezo_data) == 1:
        raise ValueError("Piezometric line must contain at least two points.")

    # === DISTRIBUTED LOADS ===
    dload_df = xls.parse('dloads', header=None)
    dloads = []
    dload_data_blocks = [
        {"start_row": 3, "end_row": 13},
        {"start_row": 16, "end_row": 26}
    ]
    dload_block_starts = [1, 5, 9, 13]

    for block in dload_data_blocks:
        for col in dload_block_starts:
            section = dload_df.iloc[block["start_row"]:block["end_row"], col:col + 3]
            section = section.dropna(how='all')
            section = section.dropna(subset=[col, col + 1], how='any')
            if len(section) >= 2:
                try:
                    block_points = section.apply(
                        lambda row: {
                            "X": float(row.iloc[0]),
                            "Y": float(row.iloc[1]),
                            "Normal": float(row.iloc[2])
                        }, axis=1).tolist()
                    dloads.append(block_points)
                except:
                    raise ValueError("Invalid data format in distributed load block.")
            elif len(section) == 1:
                raise ValueError("Each distributed load block must contain at least two points.")

    # === CIRCLES ===

    # Read the first 3 rows to get the max depth
    raw_df = xls.parse('circles', header=None)  # No header, get full sheet
    max_depth = float(raw_df.iloc[1, 2])  # Excel C2 = row 1, column 2

    # Read the circles data starting from row 4 (index 3)
    circles_df = xls.parse('circles', header=3)
    raw = circles_df.dropna(subset=['Xo', 'Yo'], how='any')
    circles = []
    for _, row in raw.iterrows():
        Xo = row['Xo']
        Yo = row['Yo']
        Option = row.get('Option', None)
        Depth = row.get('Depth', None)
        Xi = row.get('Xi', None)
        Yi = row.get('Yi', None)
        R = row.get('R', None)
        # For each circle, fill in the radius and depth values depending on the circle option
        if Option == 'Depth':
            R = Yo - Depth
        elif Option == 'Intercept':
            R = ((Xi - Xo) ** 2 + (Yi - Yo) ** 2) ** 0.5
            Depth = Yo - R
        elif Option == 'Radius':
            Depth = Yo - R
        else:
            raise ValueError(f"Unknown option '{Option}' for circles.")
        circle = {
            "Xo": Xo,
            "Yo": Yo,
            "Depth": Depth,
            "R": R,
        }
        circles.append(circle)

    # === NON-CIRCULAR SURFACES ===
    noncirc_df = xls.parse('non-circ')
    non_circ = list(noncirc_df.iloc[1:].dropna(subset=['Unnamed: 0']).apply(
        lambda row: {
            "X": float(row['Unnamed: 0']),
            "Y": float(row['Unnamed: 1']),
            "Movement": row['Unnamed: 2']
        }, axis=1))

    # === REINFORCEMENT LINES ===
    reinforce_df = xls.parse('reinforce', header=None)
    reinforce_lines = []
    reinforce_data_blocks = [
        {"start_row": 3, "end_row": 13},
        {"start_row": 16, "end_row": 26},
        {"start_row": 29, "end_row": 39}
    ]
    reinforce_block_starts = [1, 6, 11, 16]

    for block in reinforce_data_blocks:
        for col in reinforce_block_starts:
            section = reinforce_df.iloc[block["start_row"]:block["end_row"], col:col + 4]
            section = section.dropna(how='all')
            section = section.dropna(subset=[col, col + 1], how='any')
            if len(section) >= 2:
                try:
                    line_points = section.apply(
                        lambda row: {
                            "X": float(row.iloc[0]),
                            "Y": float(row.iloc[1]),
                            "FL": float(row.iloc[2]),
                            "FT": float(row.iloc[3])
                        }, axis=1).tolist()
                    reinforce_lines.append(line_points)
                except:
                    raise ValueError("Invalid data format in reinforcement block.")
            elif len(section) == 1:
                raise ValueError("Each reinforcement line must contain at least two points.")

    # === VALIDATION ===
    circular = len(circles) > 0
    if not circular and len(non_circ) == 0:
        raise ValueError("Input must include either circular or non-circular surface data.")
    if not profile_lines:
        raise ValueError("Profile lines sheet is empty or invalid.")
    if not materials:
        raise ValueError("Materials sheet is empty.")
    if len(materials) != len(profile_lines):
        raise ValueError("Each profile line must have a corresponding material.")

    # Add everything to globals_data
    globals_data["gamma_water"] = gamma_water
    globals_data["tcrack_depth"] = tcrack_depth
    globals_data["tcrack_water"] = tcrack_water
    globals_data["k_seismic"] = k_seismic
    globals_data["profile_lines"] = profile_lines
    globals_data["ground_surface"] = ground_surface
    globals_data["tcrack_surface"] = tcrack_surface
    globals_data["materials"] = materials
    globals_data["piezo_line"] = piezo_line
    globals_data["circular"] = circular # True if circles are present
    globals_data["max_depth"] = max_depth
    globals_data["circles"] = circles
    globals_data["non_circ"] = non_circ
    globals_data["dloads"] = dloads
    globals_data["reinforce_lines"] = reinforce_lines

    return globals_data