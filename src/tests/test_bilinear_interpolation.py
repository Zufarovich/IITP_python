import numpy as np
import pytest

from interpolation.bilinear_interp import bilinear_interpolation


@pytest.fixture(scope="module")
def interpolation_data():
    return {
        "x_points": np.array([0, 1]),
        "y_points": np.array([0, 1]),
        "values": np.array([[10, 20], [30, 40]]),
    }


def test_basic_interpolation(interpolation_data):
    result = bilinear_interpolation(
        interpolation_data["x_points"],
        interpolation_data["y_points"],
        interpolation_data["values"],
        0.5,
        0.5,
    )
    assert np.isclose(result, 25)  # (10+20+30+40)/4


def test_corner_points(interpolation_data):
    data = interpolation_data
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 0, 0)
        == 10
    )
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 1, 0)
        == 30
    )
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 0, 1)
        == 20
    )
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 1, 1)
        == 40
    )


def test_linear_interpolation():
    x_points = np.array([0, 1])
    y_points = np.array([0, 1])
    values = np.array([[10, 10], [20, 20]])

    x = np.linspace(0, 1, 5)
    y = np.array([0.5] * 5)

    result = bilinear_interpolation(x_points, y_points, values, x, y)
    expected = np.linspace(10, 20, 5)
    assert np.allclose(result, expected)


def test_vectorized_operation():
    x_points = np.array([0, 1])
    y_points = np.array([0, 1])
    values = np.array([[1, 2], [3, 4]])

    x = np.array([0, 0.5, 1])
    y = np.array([0, 0.5, 1])

    result = bilinear_interpolation(x_points, y_points, values, x, y)
    expected = np.array([1, 2.5, 4])
    assert np.allclose(result, expected)


def test_zero_area():
    with pytest.raises(AssertionError, match="x_points and y_points should contain different points"):
        bilinear_interpolation(np.array([0,0]), np.array([0,1]), np.eye(2), 0.5, 0.5)


def test_invalid_input_shapes():
    with pytest.raises(AssertionError) as excinfo:
        bilinear_interpolation(np.array([0]), np.array([0, 1]), np.eye(2), 0.5, 0.5)
    assert "x_points must be an array of shape (2,)" in str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        bilinear_interpolation(np.array([0, 1]), np.array([0]), np.eye(2), 0.5, 0.5)
    assert "y_points must be an array of shape (2,)" in str(excinfo.value)
