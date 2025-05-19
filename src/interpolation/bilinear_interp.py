import numpy as np


def bilinear_interpolation(
    x_points: np.ndarray,
    y_points: np.ndarray,
    values: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    """Bilinear interpolation for points (x,y) on a rectangular grid.

    Computes weighted sum of values at four corners using bilinear
    interpolation formula.

    Args:
        x_points: Array of shape (2,) with x-coordinates of corners.

        y_points: Array of shape (2,) with y-coordinates of corners.

        values: Array of values at corners.

        x: X-coordinates of points to interpolate.

        y: Y-coordinates of points to interpolate.

    Returns:
        np.array: Interpolated values for points (x, y).
        The output shape matches the input shapes of x and y.

    Raises:
        AssertionError:
            - x_points or y_points don't have shape (2,)
            - x_points or y_points contain identical values
    """
    assert x_points.shape == (2,), "x_points must be an array of shape (2,)"
    assert y_points.shape == (2,), "y_points must be an array of shape (2,)"

    denumerator = (x_points[1] - x_points[0]) * (y_points[1] - y_points[0])
    assert denumerator != 0, "x_points and y_points should contain different points"

    x_x1 = x - x_points[0]
    x_x2 = x - x_points[1]
    y_y1 = y - y_points[0]
    y_y2 = y - y_points[1]

    w_a = (-x_x2) * (-y_y2)
    w_b = x_x1 * (-y_y2)
    w_c = (-x_x2) * y_y1
    w_d = x_x1 * y_y1

    return (
        values[..., 0, 0] * w_a
        + values[..., 1, 0] * w_b
        + values[..., 0, 1] * w_c
        + values[..., 1, 1] * w_d
    ) / denumerator
