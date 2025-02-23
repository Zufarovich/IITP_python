import numpy as np
import matplotlib.pyplot as plt

def bilinear_interpolation(x_points: np.array, y_points: np.array, values: np.array):
    assert x_points.shape == (2,), "x_points должен быть массивом размера (2,)"
    assert y_points.shape == (2,), "y_points должен быть массивом размера (2,)"
    assert values.shape == (2, 2), "values должен быть массивом размера (2, 2)"

    denumerator = (x_points[1] - x_points[0]) * (y_points[1] - y_points[0])

    assert denumerator, "в x_points и y_points должны содержаться разные точки"

    def interpolant(x: np.float64, y: np.float64):

        x_x1 = x - x_points[0]
        x_x2 = x - x_points[1]
        y_y1 = y - y_points[0]
        y_y2 = y - y_points[1] 

        result = (
            values[0][0] * (-x_x2) * (-y_y2) +
            values[1][0] * x_x1 * (-y_y2) +
            values[0][1] * (-x_x2) * y_y1 +
            values[1][1] * x_x1 * y_y1
        ) / denumerator

        return result

    return interpolant

def visualize(x_points: np.array, y_points: np.array, num_points: int, interpolant):
    assert x_points.shape == (2,), "x_points должен быть массивом размера (2,)"
    assert y_points.shape == (2,), "y_points должен быть массивом размера (2,)"

    x_points = np.linspace(x_points[0], x_points[1], num_points)
    y_points = np.linspace(y_points[0], y_points[1], num_points)

    grid_x, grid_y = np.meshgrid(x_points, y_points)

    grid_z = np.vectorize(lambda x, y: interpolant(x, y))(grid_x, grid_y)

    plt.figure(figsize=(8, 6))
    cp = plt.contourf(grid_x, grid_y, grid_z, cmap='viridis')
    plt.colorbar(cp)
    plt.title("Bilinear Interpolation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()