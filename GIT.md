# Git facts — GMSUD

Inspected locally: 2026-10-30. Remote refs were not refreshed during this audit.

Only main is recorded as a long-lived branch in this checkout. No separate integration branch is configured. Use a scoped task branch and inspect release effects before integration; do not invent staging/dev. Production and publication triggers remain to be verified for the task.

Shared procedure and Rikki's integration/shipping authorisation: `~/.agents/workflows/git.md`. This file owns local facts, not another copy of the workflow. Verify current triggers before release.
