---
name: review
description: Review the current change against its spec, conventions, security and Definition of Done, using the reviewer and security_auditor subagents in parallel, then fix blocking findings. Use for "review", "revisão", "code review", "security review", or before opening/merging a PR.
---

# Review

1. Run `make check`. Red → fix first; reviewing a red build wastes time.
2. Spawn in parallel and wait for both:
   - `reviewer` — spec coverage, correctness, design, tests.
   - `security_auditor` — dependencies (`make audit` output), OWASP API Top 10, secrets, CI/container.
3. Checklist (the reviewers use it too):
   - [ ] Every AC of the spec has a test that would fail without the change.
   - [ ] Layering respected (`make arch`); domain/application framework-free; wiring only in `container.py`.
   - [ ] Inputs validated at the edge; domain errors mapped to correct status codes; no stack traces leaked.
   - [ ] Every network call has a timeout; retries only on idempotent operations; consumers idempotent.
   - [ ] No secrets/PII in code, logs, fixtures; settings via `Settings`/`SecretStr`.
   - [ ] Migrations reversible or expand/contract; API/event contracts backward compatible or versioned.
   - [ ] Logs are structured with meaningful event names; readiness covers new dependencies.
   - [ ] Clean code: small functions, clear names, no dead/commented code, no needless abstraction.
   - [ ] Docs updated (spec contracts, ADRs, README/AGENTS.md if commands changed).
4. Fix every **Blocking** finding (re-run `make check`); answer suggestions explicitly (fix or why not).
5. Next: `$ship`.
