"""Render the template for representative answer sets and run the generated project's gates.

Fast checks always run; the full `make check` (Docker for testcontainers) runs with --full.
"""

import os
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest
from copier import run_copy

ROOT = Path(__file__).parents[1]

SCENARIOS = {
    "full-kafka": {"use_postgres": True, "use_redis": True, "event_broker": "kafka"},
    "minimal": {"use_postgres": False, "use_redis": False, "event_broker": "none"},
    "postgres-rabbit": {"use_postgres": True, "use_redis": False, "event_broker": "rabbit"},
    "redis-only": {"use_postgres": False, "use_redis": True, "event_broker": "none"},
}


def render(destination: Path, answers: dict[str, object]) -> Path:
    run_copy(
        str(ROOT),
        destination,
        data={"project_name": "Acme Orders", **answers},
        defaults=True,
        unsafe=False,
        vcs_ref="HEAD",
        quiet=True,
    )
    return destination


def sh(cwd: Path, *command: str) -> None:
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    subprocess.run(command, cwd=cwd, check=True, env=env)


@pytest.fixture(params=sorted(SCENARIOS))
def project(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    return render(tmp_path / request.param, SCENARIOS[request.param])


def test_renders_expected_layout(project: Path) -> None:
    answers = SCENARIOS[project.name]
    package = project / "src" / "acme_orders"

    assert (package / "adapters" / "postgres.py").exists() is answers["use_postgres"]
    assert (project / "migrations").exists() is answers["use_postgres"]
    assert (package / "adapters" / "redis_cache.py").exists() is answers["use_redis"]
    assert (package / "entrypoints" / "worker.py").exists() is (answers["event_broker"] != "none")
    for path in ["AGENTS.md", ".codex/config.toml", ".agents/skills/implement/SKILL.md"]:
        assert (project / path).is_file(), path
    tomllib.loads((project / "pyproject.toml").read_text())
    tomllib.loads((project / ".codex/config.toml").read_text())
    for agent in (project / ".codex/agents").glob("*.toml"):
        assert {"name", "description", "developer_instructions"} <= tomllib.loads(agent.read_text()).keys()
    leftovers = [p for p in project.rglob("*") if "{{" in p.name or p.suffix == ".jinja"]
    assert not leftovers


@pytest.mark.slow
def test_generated_project_passes_its_own_gates(project: Path) -> None:
    if shutil.which("docker") is None:
        pytest.skip("Docker is required for integration tests")
    sh(project, "git", "init", "-q", "-b", "main")
    sh(project, "uv", "sync", "--all-groups", "-q")
    sh(project, "make", "check")
