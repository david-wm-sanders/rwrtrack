import subprocess
from pathlib import Path


# Run pep8 --exclude=venv --show-source .\source.py
files = ["rwrtrack.py", "stats.py", "sums.py"]
for f in files:
    p = Path(__file__).parent / Path(f)
    try:
        subprocess.check_output(["pep8", "--exclude=venv",
                                 "--show-source", str(p)])
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"))