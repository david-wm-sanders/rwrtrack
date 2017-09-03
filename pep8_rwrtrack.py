import subprocess
from pathlib import Path


# Run pep8 --exclude=venv --show-source .\rwrtrack.py
rwrtrack_path = Path(__file__).parent / Path("rwrtrack.py")
try:
    subprocess.check_output(["pep8", "--exclude=venv",
                             "--show-source", str(rwrtrack_path)])
except subprocess.CalledProcessError as e:
    print(e.output.decode("utf-8"))
