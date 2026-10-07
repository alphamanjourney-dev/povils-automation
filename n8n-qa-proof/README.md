# n8n QA Proof

Self-directed QA proof by **Povilas Brand** for exported n8n workflows.

Includes:
- practical stress-test checklist
- static workflow JSON audit script
- unit tests for common failure conditions

This is portfolio proof of QA/reliability methodology, not a claim of prior n8n client work.

Run:
```bash
python3 -m unittest -v test_n8n_workflow_audit.py
python3 n8n_workflow_audit.py workflow.json
```
