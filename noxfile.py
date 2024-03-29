import nox
from nox.sessions import Session

locations = "pyfilemovr", "run.py", "noxfile.py"
python_versions = ["3.9"]
nox.options.sessions = "lint", "mypy"


@nox.session(python=python_versions)
def lint(session: Session) -> None:
    """Lint code using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=python_versions)
def black(session: Session) -> None:
    """Format code using black."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=python_versions)
def mypy(session: Session) -> None:
    """Check typing with mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)
