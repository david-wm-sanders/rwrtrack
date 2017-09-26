import subprocess
from pathlib import Path


# Run pep8 --exclude=venv --show-source .\source.py
files = ["stats.py", "get_stats.py", "sums.py", "analysis.py", "ranking.py"]
for f in files:
    p = Path(__file__).parent / Path(f)
    subprocess.run(["pep8", "--exclude=venv","--show-source", str(p)])
