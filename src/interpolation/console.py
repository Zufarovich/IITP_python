# src/interpolation/console.py
from pathlib import Path

import click
import numpy as np

from interpolation import __version__
from interpolation.bilinear_interp import visualize
from interpolation.image_process import process_interpolation


@click.command()
@click.argument("SOURCE")
@click.argument("OUTPUT")
@click.argument("WIDTH")
@click.argument("HEIGHT")
@click.option(
    "--force", "-f", is_flag=True, help="Overwriting output file without asking"
)
def image_interpolate(source, output, width, height, force):
    """
    This script interpolates image from SOURCE to OUTPUT

    OUTPUT image will have size WIDTH*HEIGHT
    """
    source = Path(source)
    output = Path(output)

    if not source.exists():
        raise ValueError(
            click.style(f"Input image not found: {source}", fg="red", bold=True)
        )

    if output.exists() and not force:
        msg = click.style(f'File "{output}" exists! Overwrite? [y/n]: ', fg="yellow")
        if input(msg).lower() != "y":
            click.secho("Cancelled", fg="red")
            return -1
    else:
        output.touch()

    return process_interpolation(source, output, int(width), int(height))


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


cli.add_command(image_interpolate)

if __name__ == "__main__":
    cli()
