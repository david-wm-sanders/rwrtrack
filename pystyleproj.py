#!venv/bin/python3
"""Checks project for pycodestyle and pydocstyle infractions.

Usage:
    pystyleproj.py [-c|-s|-r|-f] [-d] [-v]

Options:
    -c     Count infractions
    -s     Show source for infractions
    -r     Show source and remediation sample for infractions
    -f     Show first infractions of each type

    -d     Include pydocstyle infractions
    -v     Verbose output from py{code,doc}style
"""
import configparser
import itertools
import platform
import subprocess
from pathlib import Path

from docopt import docopt


# TODO: If no venv: make venv and just install pycodestyle
path_here = Path(__file__).parent / Path(".")


def pyxstyle_path(x, venv_dir="venv"):
    """Calculate the path to py{x}style in the venv directory relative to project root."""
    extension = ".exe" if platform.system() == "Windows" else ""
    bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
    return [str(path_here / f"{venv_dir}/{bin_dir}/py{x}style{extension}")]


def make_pyxstyle_command(x, p, opts=None, verbose=False):
    """Calculate the py{x}style command required to elicit behaviour desired by opts."""
    opts = opts if opts else []
    verbose = ["-v"] if verbose else []
    return list(itertools.chain(pyxstyle_path(x), opts, verbose, [str(p)]))


def _load_exclusions(tox_p):
    """Load pycodestyle exclude list from tox.ini at tox_p."""
    # Load excludes from tox.ini
    excludes = ["__pycache__"]
    tox_config = configparser.ConfigParser()
    tox_config.read(tox_p)
    if "pycodestyle" in tox_config:
        if "exclude" in tox_config["pycodestyle"]:
            excludes.extend(tox_config["pycodestyle"]["exclude"].split(","))
    return excludes


def _find_things(root_p, excludes):
    """Find folders and files at top level that are not excluded."""
    folders = (x for x in root_p.iterdir() if x.is_dir() and x.name not in excludes)
    return list(itertools.chain(path_here.glob("*.py"), folders))


if __name__ == '__main__':
    args = docopt(__doc__)

    tox_p = path_here / "tox.ini"
    excludes = _load_exclusions(tox_p)
    print(f"Excluding {', '.join(excludes)}")

    cmds = []

    if args["-c"]:
        pycodestyle_opts = ["--statistics", "-qq"]
    elif args["-s"]:
        pycodestyle_opts = ["--show-source"]
    elif args["-r"]:
        pycodestyle_opts = ["--show-source", "--show-pep8"]
    elif args["-f"]:
        pycodestyle_opts = ["--first"]
    else:
        pycodestyle_opts = None

    cmds.append(make_pyxstyle_command("code", path_here, pycodestyle_opts, verbose=args["-v"]))

    if args["-d"]:
        things = _find_things(path_here, excludes)
        for thing in things:
            pydocstyle_opts = ["--count"] if args["-c"] else None
            cmds.append(make_pyxstyle_command("doc", thing, pydocstyle_opts, verbose=args["-v"]))

    for cmd in cmds:
        print(f">>> {' '.join(arg for arg in cmd)}")
        try:
            subprocess.run(cmd)
        except FileNotFoundError as e:
            raise Exception(f"No '{cmd[0]}'") from e
