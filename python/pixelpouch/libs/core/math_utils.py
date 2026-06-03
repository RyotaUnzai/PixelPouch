import math


def extract_trs_from_matrix(matrix: tuple[float, ...]) -> tuple[float, ...]:
    """
    Extract Translation, Rotation (Euler XYZ), Scale
    from Houdini packedfulltransform (column-major 4x4, flat 16-tuple)

    Matrix layout (column-major):
    [0  4  8  12]
    [1  5  9  13]
    [2  6  10 14]
    [3  7  11 15]
    """
    # --- Scale ---
    sx = math.sqrt(matrix[0] ** 2 + matrix[1] ** 2 + matrix[2] ** 2)
    sy = math.sqrt(matrix[4] ** 2 + matrix[5] ** 2 + matrix[6] ** 2)
    sz = math.sqrt(matrix[8] ** 2 + matrix[9] ** 2 + matrix[10] ** 2)

    # --- Normalized rotation matrix ---
    r00, r10, r20 = matrix[0] / sx, matrix[1] / sx, matrix[2] / sx
    r01, r11, r21 = matrix[4] / sy, matrix[5] / sy, matrix[6] / sy
    r02, r12, r22 = matrix[8] / sz, matrix[9] / sz, matrix[10] / sz

    # --- Euler XYZ extraction ---
    if abs(r20) < 0.9999:
        ry = math.asin(-r20)
        rx = math.atan2(r21, r22)
        rz = math.atan2(r10, r00)
    else:
        # Gimbal lock
        ry = math.pi / 2 if r20 < 0 else -math.pi / 2
        rx = math.atan2(-r12, r11)
        rz = 0.0

    # --- Translation (last column in column-major) ---
    tx = matrix[12]
    ty = matrix[13]
    tz = matrix[14]

    return (
        tx,
        ty,
        tz,
        math.degrees(rx),
        math.degrees(ry),
        math.degrees(rz),
        sx,
        sy,
        sz,
    )
