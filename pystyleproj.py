#!venv/bin/python3
"""Checks project for pycodestyle and pydocstyle infractions.

Usage:
    pystyleproj.py [-c|-s|-r|-f] [-d] [-v]

Options:
    -c      Count infractions
    -s      Show source for infractions
    -r      Show source for infractions and compliance sample
    -f      Show first infractions

    -d      Include pydocstyle infractions
    -v      Show verbose infraction detail
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


if __name__ == '__main__':
    args = docopt(__doc__)

    cmds = []
    if args["-c"]:
        cmds.append(make_pyxstyle_command("code", path_here, ["--statistics", "-qq"], verbose=args["-v"]))
    elif args["-s"]:
        cmds.append(make_pyxstyle_command("code", path_here, ["--show-source"], verbose=args["-v"]))
    elif args["-r"]:
        cmds.append(make_pyxstyle_command("code", path_here, ["--show-source", "--show-pep8"], verbose=args["-v"]))
    elif args["-f"]:
        cmds.append(make_pyxstyle_command("code", path_here, ["--first"], verbose=args["-v"]))
    else:
        cmds.append(make_pyxstyle_command("code", path_here, verbose=args["-v"]))

    if args["-d"]:
        # Load excludes from tox.ini
        excludes = ["__pycache__"]
        tox_config = configparser.ConfigParser()
        tox_config.read(str(path_here / "tox.ini"))
        if "pycodestyle" in tox_config:
            if "exclude" in tox_config["pycodestyle"]:
                excludes.extend(tox_config["pycodestyle"]["exclude"].split(","))
                print(f"Excluding {', '.join(excludes)}")

        # Find folders and files at top level
        folders = (x for x in path_here.iterdir() if x.is_dir() and x.name not in excludes)
        things = list(itertools.chain(path_here.glob("*.py"), folders))
        for thing in things:
            if args["-c"]:
                cmds.append(make_pyxstyle_command("doc", thing, ["--count"], verbose=args["-v"]))
            else:
                cmds.append(make_pyxstyle_command("doc", thing, verbose=args["-v"]))

    for cmd in cmds:
        print(f">>> {' '.join(arg for arg in cmd)}")
        try:
            subprocess.run(cmd)
        except FileNotFoundError as e:
            raise Exception(f"No '{cmd[0]}'") from e
