# n8n Workflow QA / Stress-Test Checklist

Self-directed proof asset by **Povilas Brand**. This is a methodology/demo, not a claim of prior client delivery.

## Review order
1. Trigger and input contract: required/optional input, webhook response behavior.
2. External dependencies: HTTP/API/AI/DB/comms nodes; timeouts, retries, rate limits, malformed responses.
3. Error routing: fallible-node error paths plus a workflow-level Error Workflow for unattended automation.
4. Data validation: missing fields, wrong types, invalid JSON, oversized payloads.
5. Idempotency: replayed webhooks, retries, double submissions, duplicate CRM rows/messages.
6. AI behavior: invalid structured output, untrusted-input prompt injection, empty output, refusal, timeout, rate limit.
7. Edge cases: 4xx, 429, 5xx, timeout, expired credential, zero-result branch, partial success.
8. Observability: execution history, useful errors, correlation/context, alerts.
9. Recovery: retry transient failures; fail clearly on permanent failures; make replay safe.
10. Client-demo readiness: no dead branches, stale test data, exposed secrets, or hidden failure behind a success response.

## High-value stress cases
- missing or malformed caller input
- upstream 400 / 429 / 500 / 503
- timeout
- empty or invalid model JSON
- duplicate inbound event
- concurrent events
- revoked credential
- downstream partial success
- error alert channel failure

## Evidence record for each issue
- exact node / branch
- reproduction input
- observed result
- expected result
- severity
- proposed fix
- retest result

## Paid-trial deliverable shape
- short executive summary
- prioritized defect list
- edge-case test matrix
- fixes applied or recommended
- before/after execution evidence
- remaining risks and assumptions
