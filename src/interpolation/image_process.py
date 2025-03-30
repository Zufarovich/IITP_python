import pathlib as Path

import click
import cv2
import numpy as np

from interpolation.bilinear_interp import bilinear_interpolation


def process_interpolation(source: Path, output: Path, width: int, height: int):
    img = cv2.imread(source)
    if img is None:
        raise ValueError(click.style(f"Failed to load image: {source}", fg="red"))

    src_h, src_w = img.shape[:2]

    x_coords = np.linspace(0, src_w - 1, width)
    y_coords = np.linspace(0, src_h - 1, height)
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    x0 = np.floor(x_grid).astype(int)
    x1 = np.minimum(x0 + 1, src_w - 1)
    y0 = np.floor(y_grid).astype(int)
    y1 = np.minimum(y0 + 1, src_h - 1)

    result = np.empty((height, width, 3), dtype=np.uint8)

    for color in range(3):
        channel = img[:, :, color]

        Ia = channel[y0, x0]
        Ib = channel[y0, x1]
        Ic = channel[y1, x0]
        Id = channel[y1, x1]

        values = np.stack(
            [np.stack([Ia, Ib], axis=-1), np.stack([Ic, Id], axis=-1)], axis=-1
        )

        x_norm = x_grid - x0
        y_norm = y_grid - y0

        interpolated = bilinear_interpolation(
            x_points=np.array([0, 1]),
            y_points=np.array([0, 1]),
            values=values,
            x=x_norm,
            y=y_norm,
        )

        result[:, :, color] = np.clip(interpolated, 0, 255).astype(np.uint8)

    cv2.imwrite(output, result)

    return output
