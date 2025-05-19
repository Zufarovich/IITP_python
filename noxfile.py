
import nox
import nox_poetry
import pytest
from nox import Session

package = "interpolation"
nox.options.sessions = ["ruff_check", "formatter", "tests", "documentation"]
locations = ["src/interpolation"]

@nox_poetry.session(python="3.12")
def ruff_check(session: Session):
    session.install('ruff')
    session.run('ruff','check', '--fix')

@nox_poetry.session(python="3.12")
def formatter(session: Session) -> None:
    """Run ruff code formatter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)

@nox_poetry.session(python="3.12", reuse_venv=True)
def tests(session: Session) -> None:
    """Run pytest with coverage."""
    session.install(".")
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov")
    
@nox_poetry.session(python="3.12", reuse_venv=True)
def documentation(session: Session) -> None:
    """Run documentation."""
    session.install(".") 
    
    session.install(
        "sphinx", 
        "sphinx_rtd_theme", 
        "sphinx_click",
        "myst_parser"
    )
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")