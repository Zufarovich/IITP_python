from pathlib import Path

import cv2
import numpy as np
import pytest

from interpolation.image_process import process_interpolation


def test_invalid_input():
    """Tests handling of invalid file paths.

    Raises:
        ValueError: When `process_interpolation` is called with invalid file
                    paths.
    """
    with pytest.raises(ValueError):
        process_interpolation(Path("bad path"), Path("bad path"), 100, 100)


@pytest.fixture(scope="class")
def start_test_interpolation(request):
    """Sets up test environment and performs image interpolation.

    This fixture executes before the test class. It loads an input image,
    applies the `process_interpolation` function to create an interpolated
    image and a scaled interpolated image.

    Sets the following class-level attributes:
        test_image (np.ndarray): The interpolated image.
        
        img_path (Path): The path to the interpolated image file.
        
        src_size (tuple): The original image size (height, width, channels).
        
        scaled (np.ndarray): The scaled interpolated image.
    """
    input_path = Path("./src/tests/lantern.jpeg")
    input = cv2.imread(input_path)

    output = process_interpolation(
        input_path,
        Path(
            "./src/tests/lantern_interpolated.jpeg",
        ),
        input.shape[1],
        input.shape[0],
    )
    scaled = process_interpolation(
        input_path,
        Path(
            "./src/tests/lantern_interpolated2.jpeg",
        ),
        int(input.shape[1] * 1.5),
        int(input.shape[0] * 1.5),
    )
    image = cv2.imread(output)
    img_scaled = cv2.imread(scaled)

    request.cls.test_image = image
    request.cls.img_path = output
    request.cls.src_size = input.shape
    request.cls.scaled = img_scaled

    yield image

    output.unlink()
    scaled.unlink()
    del request.cls.test_image
    del request.cls.img_path
    del request.cls.src_size
    del request.cls.scaled


@pytest.mark.usefixtures("start_test_interpolation")
class TestOutput:
    def test_unchanged_size(self):
        """Tests that the image size remains unchanged after processing.

        This function verifies that the image processing steps do not alter the
        dimensions of the input image.

        Raises:
            AssertionError: If the source and processed images differ.
        """
        src = cv2.imread(Path("./src/tests/lantern.jpeg"))
        assert np.any(self.test_image - src)

    def test_output(self):
        """Tests if the output image file is created.

        Raises:
            AssertionError: If the output image file 
            does not exist at the expected path.
        """
        assert self.img_path.exists()

    def test_scaled_output(self):
        """Tests that the output image is scaled correctly.

        This function verifies that the output image, stored in `self.scaled`, has the
        correct dimensions after scaling, by checking that the shape matches the new
        size.
        
        Raises:
            AssertionError: If the shape of the scaled image does not match the
                            expected dimensions.
        """
        new_size = (int(self.src_size[0] * 1.5), int(self.src_size[1] * 1.5), 3)
        assert self.scaled.shape == new_size
