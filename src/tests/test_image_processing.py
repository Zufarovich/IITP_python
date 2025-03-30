from pathlib import Path

import cv2
import pytest
import numpy as np

from interpolation.image_process import process_interpolation


def test_invalid_input():
    with pytest.raises(ValueError):
        process_interpolation(Path("bad path"), Path("bad path"), 100, 100)


@pytest.fixture(scope="class")
def start_test_interpolation(request):
    input_path = Path("./src/tests/lantern.jpeg")
    input = cv2.imread(input_path)

    output = process_interpolation(input_path, Path("./src/tests/lantern_interpolated.jpeg")
                                   , input.shape[1], input.shape[0])
    scaled  = process_interpolation(input_path, Path("./src/tests/lantern_interpolated2.jpeg")
                                   , int(input.shape[1]*1.5), int(input.shape[0]*1.5))
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
        src = cv2.imread(Path("./src/tests/lantern.jpeg"))
        assert np.any(self.test_image - src)

    def test_output(self):
        assert self.img_path.exists()

    def test_scaled_output(self):
        new_size = (int(self.src_size[0]*1.5), int(self.src_size[1]*1.5), 3)
        assert self.scaled.shape == new_size