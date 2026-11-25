"""Command-line entry point for generating a service and its project-scoped Codex setup."""

import argparse
import keyword
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from copier import run_copy
from copier.errors import CopierError

TEMPLATE = "https://github.com/spassos/codex-harness-template.git"


def mcp_server(value: str) -> tuple[str, str]:
    name, _, url = value.partition("=")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise argparse.ArgumentTypeError(
            "use NAME=HTTPS_URL with a server name containing letters, digits, - or _"
        )
    try:
        endpoint = urlsplit(url)
        valid = endpoint.scheme == "https" and endpoint.hostname and endpoint.username is None
        # Only endpoints suitable for committing to project configuration are supported.
        valid = (
            valid
            and not endpoint.query
            and not endpoint.fragment
            and not any(c.isspace() or not c.isprintable() for c in url)
        )
        _ = endpoint.port
    except ValueError:
        valid = False
    if not valid:
        raise argparse.ArgumentTypeError("use an HTTPS endpoint URL without credentials, query or fragment")
    return name, url


def main() -> int:
    parser = argparse.ArgumentParser(prog="codex-scaffold", description=__doc__)
    parser.add_argument("destination", type=Path, help="new directory, e.g. orders-api")
    parser.add_argument("--name", help="project display name (default: directory name)")
    parser.add_argument("--description", help="one-line service description")
    parser.add_argument("--author", help="owning person or team")
    parser.add_argument("--python", choices=["3.12", "3.13", "3.14"], help="service Python version")
    parser.add_argument("--postgres", action="store_true", help="include PostgreSQL and migrations")
    parser.add_argument("--redis", action="store_true", help="include Redis")
    parser.add_argument("--broker", choices=["none", "kafka", "rabbit"], default="none")
    parser.add_argument(
        "--mcp",
        action="append",
        type=mcp_server,
        default=[],
        metavar="NAME=HTTPS_URL",
        help="register a project MCP server (repeatable)",
    )
    parser.add_argument("--template", type=Path, help="use a local template checkout")
    parser.add_argument(
        "--ref", help="template Git revision (default: main upstream, HEAD for a local checkout)"
    )
    args = parser.parse_args()
    path = args.destination.expanduser().absolute()
    slug = path.name.lower().replace("_", "-").replace(" ", "-")
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", slug) or keyword.iskeyword(slug.replace("-", "_")):
        parser.error("choose a directory name that can be used as a Python package, e.g. orders-api")
    servers = dict(args.mcp)
    if len(servers) != len(args.mcp):
        parser.error("each MCP server must have a unique name")
    answers = {
        "project_name": args.name if args.name is not None else path.name,
        "project_slug": slug,
        "use_postgres": args.postgres,
        "use_redis": args.redis,
        "event_broker": args.broker,
        "mcp_servers": servers,
    }
    for key, value in (
        ("description", args.description),
        ("author_name", args.author),
        ("python_version", args.python),
    ):
        if value is not None:
            answers[key] = value

    source = str(args.template.expanduser().resolve()) if args.template else TEMPLATE
    revision = args.ref or ("HEAD" if args.template else "main")
    try:
        if path.exists() or path.is_symlink():
            parser.error("destination already exists; choose a new directory")
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=path.parent) as temp:
            project = Path(temp) / "project"
            run_copy(source, project, vcs_ref=revision, data=answers, defaults=True, unsafe=False, quiet=True)
            subprocess.run(["uv", "lock"], cwd=project, check=True)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=project, check=True)
            project.rename(path)
    except (CopierError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"codex-scaffold: {exc}", file=sys.stderr)
        return 1

    print(f"Created {path}. Open this directory in Codex. See README.md for startup and test commands.")
    return 0
