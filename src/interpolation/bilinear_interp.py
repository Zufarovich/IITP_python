import matplotlib.pyplot as plt
import numpy as np


def bilinear_interpolation(
    x_points: np.array, y_points: np.array, values: np.array, x: np.array, y: np.array
):
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


def visualize(
    x_points: np.array, y_points: np.array, num_points: int, values: np.array
):
    assert x_points.shape == (2,), "x_points must be an array of shape (2,)"
    assert y_points.shape == (2,), "y_points must be an array of shape (2,)"
    assert values.shape == (2, 2), "values must be convertible to 2x2 array"

    x_grid = np.linspace(x_points[0], x_points[1], num_points)
    y_grid = np.linspace(y_points[0], y_points[1], num_points)
    grid_x, grid_y = np.meshgrid(x_grid, y_grid)

    grid_z = bilinear_interpolation(
        x_points=x_points, y_points=y_points, values=values, x=grid_x, y=grid_y
    )

    plt.figure(figsize=(8, 6))
    cp = plt.contourf(grid_x, grid_y, grid_z, levels=20, cmap="viridis")
    plt.colorbar(cp, label="Interpolated Value")
    plt.title("Bilinear Interpolation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()
