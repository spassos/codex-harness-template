---
name: ship
description: Deliver a reviewed change to production — branch, Conventional Commit PR, CI gates, merge, release-please, CD to staging and production with post-deploy verification and rollback. Use for "ship", "deploy", "release", "abrir PR", "subir para produção", "entregar".
---

# Ship → production verified

1. Branch `feat/NNN-<slug>` (or `fix/...`). `make check` green locally.
2. Open a PR with `.github/pull_request_template.md` filled in; title in Conventional Commits
   (`feat(items): ...`) — it becomes the squash commit and drives the version bump.
3. CI must be green: quality (ruff, mypy, import-linter), tests + coverage, security (pip-audit,
   gitleaks, zizmor), image build + Trivy, PR title. Optional Codex review comment
   (`codex-review.yml`). Address findings; never re-run hoping for a different result.
4. Human approval → squash merge to `main`.
5. CD (`cd.yml`) runs automatically: CI again → image pushed to GHCR with provenance attestation →
   **staging** deploy → `scripts/smoke.py` proves `/health/live` reports the commit SHA and
   `/health/ready` is 200 → **production** (GitHub Environment approval) → same verification →
   automatic `scripts/deploy.sh rollback` if verification fails.
6. Watch the run (`gh run watch` or the Actions tab). Done = production smoke test green.
   Then check the PRD metrics/logs for the feature and update the spec status to `Shipped`.
7. release-please keeps a release PR with the CHANGELOG; merging it tags a semantic version.

Incident? Roll back first (`scripts/deploy.sh rollback` or revert commit → CD), investigate after.
