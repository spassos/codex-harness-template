"""Freeze one generated API, produce the two inputs and randomize the 12 run IDs."""

import argparse
import json
import os
import random
import shutil
import subprocess
import tarfile
import tempfile
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination: Path, revision: str) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    sha = subprocess.check_output(
        ["git", "rev-parse", "--verify", revision + "^{commit}"], cwd=ROOT, text=True
    ).strip()
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "project"
        subprocess.run(
            [
                "uv",
                "run",
                "--locked",
                "copier",
                "copy",
                "--quiet",
                "--defaults",
                f"--vcs-ref={sha}",
                "-d",
                "project_name=Pilot API",
                str(ROOT),
                str(project),
            ],
            cwd=ROOT,
            check=True,
        )
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        subprocess.run(["uv", "lock"], cwd=project, env=env, check=True)
        for arm in ["guided", "baseline"]:
            if arm == "baseline":
                (project / "AGENTS.md").unlink()
                shutil.rmtree(project / ".agents")
                shutil.rmtree(project / ".codex/agents")
            with tarfile.open(destination / f"{arm}.tar", "w") as archive:
                archive.add(project, arcname="project")
                archive.add(ROOT / "pilot/tasks.json", arcname="tasks.json")
                archive.add(ROOT / "pilot/usage.py", arcname="usage.py")
                archive.add(ROOT / "pilot/worker.py", arcname="worker.py")

    tasks = json.loads((ROOT / "pilot/tasks.json").read_text())
    assignments = list(product(tasks, ("guided", "baseline"), range(1, 4)))
    random.SystemRandom().shuffle(assignments)
    rows = [
        {"id": f"run-{i:02d}", "task": task, "arm": arm, "repeat": repeat}
        for i, (task, arm, repeat) in enumerate(assignments, 1)
    ]
    (destination / "matrix.json").write_text(json.dumps({"include": rows}) + "\n")
    (destination / "revision.txt").write_text(sha + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--revision", default="HEAD")
    args = parser.parse_args()
    prepare(args.destination.resolve(), args.revision)
