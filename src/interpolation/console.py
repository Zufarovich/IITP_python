# src/interpolation/console.py
import click
import numpy as np

from interpolation import __version__
from interpolation.bilinear_interp import bilinear_interpolation
from interpolation.bilinear_interp import visualize

@click.command()
def blt():
    """
    This script tests bilinear interpolation
    """

    x_points = np.array((1, 2))
    y_points = np.array((1, 2))
    values = np.array([[1, 2], [3, 4]])

    res = bilinear_interpolation(x_points, y_points, values)

    click.echo(res(0, 0))

@click.command()
def graph():
    """
    This script builds a graph of interpolation
    """

    x_points = np.array((1, 2))
    y_points = np.array((1, 2))
    values = np.array([[5, 2], [-1, 4]])

    res = bilinear_interpolation(x_points, y_points, values)
    visualize(x_points, y_points, 1000, res)

@click.group()
@click.version_option(version=__version__)
def cli():
    pass

cli.add_command(blt)
cli.add_command(graph)

if __name__ == '__main__':
    cli()