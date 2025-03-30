# IITP_python

This project currently implements **bilinear interpolation**.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Zufarovich/IITP_python.git
   cd IITP_python
   ```

2. **Install dependencies using Poetry**:
   ```sh
   poetry install
   ```

## Usage

Run the interpolation CLI with:
```sh
poetry run interpolation
```

To see available commands, use:
```sh
poetry run interpolation --help
```

Select the required command inside `cli/`.

## Example

To perform bilinear interpolation on an image, use the following command:

```sh
poetry run interpolation image-interpolate lantern.jpeg lantern1.jpeg 500 1000 -f
```

### Explanation:

| Parameter                        | Description |
|----------------------------------|------------|
| **`poetry run`**                 | Runs a script defined in `pyproject.toml` using Poetry. |
| **`interpolation`**              | The main command for running interpolation-related tasks. |
| **`image-interpolate`**          | A specific subcommand for performing bilinear image interpolation. |
| **`image.jpeg`**                 | The input image file that will be resized. |
| **`interpolated_image.jpeg`**    | The output file where the interpolated image will be saved. |
| **`500`**                        | The target width (in pixels) for the output image. |
| **`1000`**                       | The target height (in pixels) for the output image. |
| **`-f`**                         | Forces overwriting of the output file if it already exists. |

This command resizes `image.jpeg` to `500x1000` pixels using bilinear interpolation and saves the result as `interpolated_image.jpeg`.
