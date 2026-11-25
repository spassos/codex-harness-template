import ast
import subprocess
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_cli_records_options_in_generated_project(tmp_path: Path) -> None:
    project = tmp_path / "catalog"
    subprocess.run(
        [
            "codex-scaffold",
            str(project),
            "--template",
            str(ROOT),
            "--name",
            'Catalog "API"',
            "--description",
            'Team """A""" service',
            "--postgres",
            "--broker",
            "rabbit",
            "--mcp",
            "docs=https://docs.example.com/mcp",
            "--mcp",
            "tracker=https://tracker.example.com/mcp",
        ],
        check=True,
    )
    metadata = tomllib.loads((project / "pyproject.toml").read_text())
    assert metadata["project"]["description"] == 'Team """A""" service'
    ast.parse((project / "src/catalog/__init__.py").read_text())
    ast.parse((project / "src/catalog/entrypoints/http/app.py").read_text())
    assert (project / "migrations").is_dir()
    assert (project / "src/catalog/entrypoints/worker.py").is_file()
    config = tomllib.loads((project / ".codex/config.toml").read_text())
    assert config["mcp_servers"] == {
        "docs": {"url": "https://docs.example.com/mcp"},
        "tracker": {"url": "https://tracker.example.com/mcp"},
    }


@pytest.mark.parametrize("case", ["existing", "invalid-mcp", "duplicate-mcp"])
def test_cli_rejects_invalid_request_without_modifying_destination(tmp_path: Path, case: str) -> None:
    project = tmp_path / "orders"
    flags = []
    if case == "existing":
        project.mkdir()
        (project / "keep.txt").write_text("keep")
    elif case == "invalid-mcp":
        flags = ["--mcp", "docs=https://user:password@example.com"]
    else:
        flags = ["--mcp", "docs=https://example.com", "--mcp", "docs=https://example.org"]
    result = subprocess.run(["codex-scaffold", str(project), *flags], capture_output=True, check=False)
    assert result.returncode != 0
    if case == "existing":
        assert list(project.iterdir()) == [project / "keep.txt"]
        assert (project / "keep.txt").read_text() == "keep"
    else:
        assert not project.exists()
