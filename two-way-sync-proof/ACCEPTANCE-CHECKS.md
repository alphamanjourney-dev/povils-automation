# Proposed v1 Acceptance Checks

For a bounded first milestone:

1. New in-scope Craft task creates exactly one Todoist task.
2. Re-running the Craft poll does not create a duplicate.
3. Todoist task contains an agreed Craft backlink/identifier.
4. Craft-side completion propagates to the mapped Todoist task.
5. Todoist-side completion propagates to the mapped Craft task.
6. Replayed completion events do not bounce indefinitely between systems.
7. Same-title tasks with different source IDs remain distinct.
8. Temporary API failure is retried with a bounded policy and surfaced if still failing.
9. Missing mapped counterpart is sent to a repair path rather than silently recreated.
10. Owner can pause writes while still inspecting logs.
11. Workflow export and concise handover notes are delivered.
12. No secret is written into logs or committed to source control.
