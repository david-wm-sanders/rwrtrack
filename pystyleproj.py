#!venv/bin/python3
"""Checks project for pycodestyle and pydocstyle infractions.

Usage:
    pystyleproj.py [-c|-s|-r|-f] [-d] [-n] [-v]

Options:
    -c     Count infractions
    -s     Show source for infractions
    -r     Show source and remediation sample for infractions
    -f     Show first infractions of each type

    -d     Include pydocstyle infractions
    -n     Include SLOC analysis

    -v     Verbose output from py{code,doc}style
"""
import configparser
import itertools
import platform
import subprocess
from pathlib import Path

from docopt import docopt


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


def _find_analysis_paths(root_p, excludes):
    """Find folders and files at top level that are not excluded."""
    folders = (x for x in root_p.iterdir() if x.is_dir() and x.name not in excludes)
    return list(itertools.chain(path_here.glob("*.py"), folders))


if __name__ == '__main__':
    args = docopt(__doc__)

    tox_p = path_here / "tox.ini"
    excludes = _load_exclusions(tox_p)
    analysis_paths = _find_analysis_paths(path_here, excludes)
    print(f"Excluding {', '.join(excludes)}")
    cmds = []

    # Create the pycodestyle command
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

    # If "-d" option specified, create the pydocstyle command
    if args["-d"]:
        for analysis_path in analysis_paths:
            pydocstyle_opts = ["--count"] if args["-c"] else None
            cmds.append(make_pyxstyle_command("doc", analysis_path, pydocstyle_opts, verbose=args["-v"]))

    for cmd in cmds:
        print(f">>> {' '.join(cmd)}")
        try:
            subprocess.run(cmd)
        except FileNotFoundError as e:
            raise Exception(f"No '{cmd[0]}'") from e

    # If "-n" option specified, do a SLOC analysis
    if args["-n"]:
        print("Performing SLOC analysis...")
        py_files = []
        for analysis_path in analysis_paths:
            if analysis_path.is_file():
                py_files.append(analysis_path)
            elif analysis_path.is_dir():
                py_files.extend(analysis_path.rglob("*.py"))

        total_blank, total_docstring, total_comment, total_code = 0, 0, 0, 0
        for py_file in py_files:
            blank, docstring, comment, code = 0, 0, 0, 0
            with py_file.open("r", encoding="utf-8") as f:
                docstring_mode = False
                for i, line in enumerate(f, 1):
                    # If the line is just whitespace, consider it to be a blank line
                    if line.isspace():
                        blank += 1
                        continue
                    # Strip leading whitespace from the line for remaining checks
                    line = line.strip()
                    # Process docstrings
                    if line.startswith("\"\"\"") or docstring_mode:
                        # print(f"{str(i).zfill(3)}: {repr(line)}")
                        if not docstring_mode:
                            # If find == rfind then there is only one """ in the line, so enter docstring_mode
                            if line.find("\"\"\"") == line.rfind("\"\"\""):
                                docstring_mode = True
                        else:
                            # If """ is in the line when in docstring_mode it must be the end, so exit docstring_mode
                            if "\"\"\"" in line:
                                docstring_mode = False
                        docstring += 1
                        continue
                    # If the line starts with a #, consider it to be a comment line
                    if line.startswith("#"):
                        comment += 1
                        continue
                    code += 1

            total_blank += blank
            total_docstring += docstring
            total_comment += comment
            total_code += code

            if args["-v"]:
                print(f"{py_file}: {blank} blank, {docstring} docstring, {comment} comment, {code} code")

        print(f"Lines: {total_blank} blank, {total_docstring} docstring, {total_comment} comment, {total_code} code")
