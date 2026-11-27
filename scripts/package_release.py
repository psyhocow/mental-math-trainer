"""Package a PyInstaller build as a downloadable release archive."""

import platform
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ARTIFACTS = ROOT / "artifacts"


def main() -> None:
    target = sys.argv[1]
    ARTIFACTS.mkdir(exist_ok=True)
    if platform.system() == "Darwin":
        app = DIST / "MentalMathTrainer.app"
        archive = ARTIFACTS / f"MentalMathTrainer-{target}.zip"
        subprocess.run(
            ["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", str(app), str(archive)],
            check=True,
        )
    else:
        archive_base = ARTIFACTS / f"MentalMathTrainer-{target}"
        shutil.make_archive(str(archive_base), "zip", root_dir=DIST, base_dir="MentalMathTrainer")


if __name__ == "__main__":
    main()
