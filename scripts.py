import sys
import subprocess
from pathlib import Path
from typing import Any

current_module = __import__(__name__)

BASE_DIR = Path(__file__).resolve().parent
DJ_MANAGE_PYFILE = BASE_DIR / "manage.py"
POETRY_PYTHON = ["poetry", "run", "python"]


def manage():
    subprocess.run(POETRY_PYTHON + [DJ_MANAGE_PYFILE] + sys.argv[1:])


def runserver():
    subprocess.run(POETRY_PYTHON + [DJ_MANAGE_PYFILE, "runserver"])


def runserver_plus():
    subprocess.run(POETRY_PYTHON + [DJ_MANAGE_PYFILE, "runserver_plus"])


def default(name):
    name = name.replace("_", "-")

    subprocess.run(POETRY_PYTHON + ["-m", name] + sys.argv[1:])


def __getattr__(name: str) -> Any:
    attrs = set(dir(current_module))

    if name not in attrs:
        return lambda: default(name)
