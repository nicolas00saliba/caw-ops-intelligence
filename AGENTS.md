# AGENTS.md

## Review policy

Review every pull request for correctness, regressions, broken interfaces, and missing tests before style suggestions.

Verify changed behavior against current tests and the repository setup. Historical reports are not evidence for the current change.

Prefer small, actionable findings with file and line context. Avoid speculative warnings without a concrete failure mode.

The local Automatic Code Review gate remains independent. This GitHub-integrated Codex review is a second review layer, not a replacement for local tests or human approval.
