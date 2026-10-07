# Two-Way Task Sync Reliability Proof

Self-directed proof by **Povilas Brand** for a Craft.do ↔ Todoist-style bidirectional sync.

This is **not** a claim that I previously delivered Craft/Todoist work for a client. It is a small deterministic proof of the failure-prone part of the requested job: state mapping and safe re-runs.

## What it demonstrates
- stable ID mapping instead of title-based matching
- duplicate prevention after a pair is registered
- Craft → Todoist completion propagation
- Todoist → Craft completion propagation
- no-op behavior when both sides are already in the same state
- mapping-collision rejection
- repair path when a mapped counterpart cannot be loaded
- same-title tasks remain distinct when IDs differ

## Intended n8n boundary
The deterministic core maps cleanly to n8n:
1. **Craft poll** every 10–30 minutes.
2. Normalize Craft task/block data.
3. Look up persistent mapping keyed by Craft ID.
4. If unmapped, create Todoist task and persist both IDs.
5. If mapped, compare completion state before writing.
6. Todoist event/webhook path performs the symmetric state comparison.
7. External calls use explicit error branches, retry/backoff, and a repair queue.
8. A pause/maintenance flag prevents writes during troubleshooting.
9. Logs record source ID, target ID, requested action, result, and retry state.

## Tests
```bash
python3 -m unittest -v test_sync_core.py
```

The tests use synthetic IDs/data and require no credentials.

## Before a live build
I would verify against current API docs and the buyer's redacted/sample payloads:
- exact Craft task/block type and stable ID
- Craft completion read/write semantics
- Todoist event payloads and completion/reopen constraints
- where the mapping should persist in n8n Cloud
- exact in-scope fields/subtasks/reopen behavior

No production credential is needed for this proof.
