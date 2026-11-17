---
name: implement
description: Implement an approved plan task by task with TDD, clean code and the hexagonal layering, keeping `make check` green. Use for "implement", "implementar", "codar", "fix", or when executing tasks from docs/specs/NNN-*/plan.md.
---

# Implement (TDD loop)

Precondition: an approved `spec.md` + `plan.md`. Bug fix without a spec? Write a failing test that
reproduces it first, then follow the same loop.

For **each** unchecked task in `plan.md`, in order:

1. **Red** — write the tests for the task's acceptance criteria (or delegate to the
   `test_engineer` subagent). Run `make test-unit` and see them fail for the right reason.
2. **Green** — write the minimum code to pass, inside the right layer:
   - business rule → `domain/`; orchestration → `application/` through ports;
   - I/O → `adapters/` (new external system? follow `$integrate`);
   - HTTP/consumer → `entrypoints/` (pydantic schemas there, map domain errors to status codes);
   - wiring → `container.py` only.
3. **Refactor** — remove duplication, name things after the domain, keep functions small. No
   speculative abstractions, no dead code, no commented-out code.
4. **Gate** — `make fmt && make check`. Fix root causes; never suppress a rule or lower coverage.
5. Tick the task in `plan.md` and commit: `git commit -m "feat(<scope>): <what> (NNN T<n>)"`.

Before handing off: every AC has a passing test, `make check` is green, docs touched by the change
(README, spec contracts, ADRs) are updated. Next: `$review`.
