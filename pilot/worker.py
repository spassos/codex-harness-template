"""Run one pilot input on a fresh, authenticated, isolated Linux worker."""

import argparse
import json
import os
import signal
import subprocess
import tempfile
import time
from pathlib import Path

CLI_VERSION = "0.172.0-alpha.2"
MODEL = "gpt-5.4"


def run(task: str, output: Path) -> None:
    project = Path("project").resolve()
    if not project.is_dir() or (project / ".git").exists():
        raise SystemExit("Extract a fresh input archive before each trial.")
    if subprocess.check_output(["codex", "--version"], text=True).strip() != f"codex-cli {CLI_VERSION}":
        raise SystemExit(f"This pilot uses Codex CLI {CLI_VERSION}.")
    prompt = json.loads(Path("tasks.json").read_text())[task]
    output.mkdir(parents=True, exist_ok=False)
    subprocess.run(["make", "bootstrap"], cwd=project, check=True)
    subprocess.run(["make", "audit"], cwd=project, check=True)
    subprocess.run(["git", "add", "-A"], cwd=project, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Pilot",
            "-c",
            "user.email=pilot@example.invalid",
            "commit",
            "-qm",
            "baseline",
        ],
        cwd=project,
        check=True,
    )
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=project, text=True).strip()
    started = time.monotonic()
    with tempfile.TemporaryFile(mode="w+") as trace:
        agent = subprocess.Popen(
            [
                "codex",
                "exec",
                "--ephemeral",
                "--trust",
                "--json",
                "-m",
                MODEL,
                "-s",
                "workspace-write",
                "-c",
                'model_reasoning_effort="medium"',
                "-c",
                "sandbox_workspace_write.network_access=false",
                "-o",
                str(output / "response.txt"),
                prompt,
            ],
            cwd=project,
            stdin=subprocess.DEVNULL,
            stdout=trace,
            start_new_session=True,
        )
        try:
            outcome = "success" if agent.wait(timeout=900) == 0 else "failure"
        except subprocess.TimeoutExpired:
            os.killpg(agent.pid, signal.SIGKILL)
            agent.wait()
            outcome = "timeout"
        elapsed = round(time.monotonic() - started)
        trace.seek(0)
        usage = None
        for line in trace:
            event = json.loads(line)
            if event.get("type") == "turn.completed":
                usage = event.get("usage")
    (output / "usage.json").write_text(json.dumps(usage))
    (output / "metrics.json").write_text(
        json.dumps(
            {"bootstrap": "success", "agent": outcome, "seconds": elapsed, "interventions_given": 0},
        )
    )
    subprocess.run(["git", "add", "--intent-to-add", "."], cwd=project, check=True)
    with (output / "change.patch").open("wb") as diff:
        subprocess.run(["git", "diff", "--binary", base], cwd=project, stdout=diff, check=True)
    if outcome != "success":
        raise SystemExit(f"Trial ended with {outcome}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=["note", "warning"])
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.task, args.output.resolve())
