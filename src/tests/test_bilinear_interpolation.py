import numpy as np
import pytest

from interpolation.bilinear_interp import bilinear_interpolation


@pytest.fixture(scope="module")
def interpolation_data():
    """This function generates data for test

    Returns:
       Dict that contains x_points, y_points and values in this corners.
    """
    return {
        "x_points": np.array([0, 1]),
        "y_points": np.array([0, 1]),
        "values": np.array([[10, 20], [30, 40]]),
    }


def test_basic_interpolation(interpolation_data):
    """Tests interpolation in the center of a rectangle

    This function tests the bilinear interpolation method by evaluating
    it at the exact center of a defined rectangular grid. It asserts that
    the result of the interpolation is close to the average of the four corner values.

    Args:
        interpolation_data (dict): A dictionary containing the data necessary for
                                    bilinear interpolation. This dictionary should have
                                    the following keys:

            'x_points' (np.ndarray): A 1D numpy array of x-coordinates.

            'y_points' (np.ndarray): A 1D numpy array of y-coordinates.

            'values' (np.ndarray): A 2D numpy array of values defined at the grid.
                                    values[i, j] corresponds to the value at
                                    (x_points[j], y_points[i]).

    Raises:
        AssertionError: If the interpolated value is not close to the expected
                        value, indicating an issue with the bilinear interpolation
                        implementation.
    """
    result = bilinear_interpolation(
        interpolation_data["x_points"],
        interpolation_data["y_points"],
        interpolation_data["values"],
        0.5,
        0.5,
    )
    assert np.isclose(result, np.sum(interpolation_data["values"])/4)


def test_corner_points(interpolation_data):
    """Tests bilinear interpolation at the corner points of a rectangle.

    This function verifies the bilinear interpolation implementation by evaluating
    it at each of the four corner points of the rectangular grid defined by
    the input `interpolation_data`.

    Args:
        interpolation_data (dict): A dictionary containing the data necessary for
                                    bilinear interpolation. This dictionary should have
                                    the following keys:

            'x_points' (np.ndarray): A 1D numpy array of x-coordinates of the grid.

            'y_points' (np.ndarray): A 1D numpy array of y-coordinates of the grid.

            'values' (np.ndarray): A 2D numpy array of values defined at the grid.
                                    values[i, j] corresponds to the value at
                                    (x_points[j], y_points[i]).

    Raises:
        AssertionError: If the interpolated value at any of the corner points
                        does not match the expected value, indicating a problem
                        with the bilinear interpolation implementation or input data.
    """
    data = interpolation_data
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 0, 0)
        == interpolation_data["values"][0, 0]
    )
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 1, 0)
        == interpolation_data["values"][1, 0]
    )
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 0, 1)
        == interpolation_data["values"][0, 1]
    )
    assert (
        bilinear_interpolation(data["x_points"], data["y_points"], data["values"], 1, 1)
        == interpolation_data["values"][1, 1]
    )


def test_linear_interpolation():
    """Tests bilinear interpolation produces a linear gradient along a line.

    This function verifies that bilinear interpolation, when applied along a
    horizontal line (y = 0.5) within a rectangular grid, results in a linear
    gradient of values.

    Raises:
        AssertionError: If the interpolated values deviate significantly
                           from the expected linear gradient.
    """
    x_points = np.array([0, 1])
    y_points = np.array([0, 1])
    values = np.array([[10, 10], [20, 20]])

    x = np.linspace(0, 1, 5)
    y = np.array([0.5] * 5)

    result = bilinear_interpolation(x_points, y_points, values, x, y)
    expected = np.linspace(10, 20, 5)
    assert np.allclose(result, expected)


def test_vectorized_operation():
    """Tests bilinear interpolation with vectorized inputs.

    This function verifies that the bilinear_interpolation function correctly
    handles vectorized inputs for x and y coordinates, producing a corresponding
    array of interpolated values.

    Raises:
        AssertionError: If the interpolated values deviate significantly from
                        the expected values.
    """
    x_points = np.array([0, 1])
    y_points = np.array([0, 1])
    values = np.array([[1, 2], [3, 4]])

    x = np.array([0, 0.5, 1])
    y = np.array([0, 0.5, 1])

    result = bilinear_interpolation(x_points, y_points, values, x, y)
    expected = np.array([1, 2.5, 4])
    assert np.allclose(result, expected)


def test_zero_area():
    """Tests behavior when the interpolation area is zero.

    This function verifies that the bilinear_interpolation function raises an
    AssertionError when the input contains same points.
    """
    with pytest.raises(
        AssertionError, match="x_points and y_points should contain different points"
    ):
        bilinear_interpolation(np.array([0, 0]), np.array([0, 1]), np.eye(2), 0.5, 0.5)


def test_invalid_input_shapes():
    """Tests handling of invalid input shapes for coordinate arrays.

    This function verifies that the bilinear_interpolation function raises an
    AssertionError when the input x_points or y_points arrays have incorrect shapes 

    Raises:
        AssertionError: When x_points or y_points have incorrect shapes.
    """
    with pytest.raises(AssertionError) as excinfo:
        bilinear_interpolation(np.array([0]), np.array([0, 1]), np.eye(2), 0.5, 0.5)
    assert "x_points must be an array of shape (2,)" in str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        bilinear_interpolation(np.array([0, 1]), np.array([0]), np.eye(2), 0.5, 0.5)
    assert "y_points must be an array of shape (2,)" in str(excinfo.value)
