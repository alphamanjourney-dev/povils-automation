#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

NETWORK_HINTS=("httprequest","openai","anthropic","slack","gmail","discord","twilio","postgres","mysql","salesforce","hubspot","telegram","microsoftsql","mongodb","redis","s3","google")
UNATTENDED_HINTS=("webhook","scheduletrigger","cron","formtrigger","rabbitmq","kafka","queue")
RESPOND_HINT="respondtowebhook"

def norm(s): return (s or "").replace(" ","").replace("-","").replace("_","").lower()

def audit(workflow):
    issues=[]
    nodes=workflow.get("nodes") or []
    if not nodes:
        return [{"severity":"HIGH","code":"NO_NODES","message":"Workflow contains no nodes."}]
    names=[n.get("name","") for n in nodes]
    for name in sorted({n for n in names if n and names.count(n)>1}):
        issues.append({"severity":"MEDIUM","code":"DUPLICATE_NODE_NAME","node":name,"message":"Duplicate node names make debugging and connection review harder."})
    types=[norm(n.get("type")) for n in nodes]
    has_unattended=any(any(h in t for h in UNATTENDED_HINTS) for t in types)
    has_webhook=any("webhook" in t and RESPOND_HINT not in t for t in types)
    has_respond=any(RESPOND_HINT in t for t in types)
    settings=workflow.get("settings") or {}
    if has_unattended and not settings.get("errorWorkflow"):
        issues.append({"severity":"HIGH","code":"NO_ERROR_WORKFLOW","message":"Unattended workflow has no workflow-level errorWorkflow configured."})
    if has_webhook and not has_respond:
        issues.append({"severity":"HIGH","code":"WEBHOOK_NO_RESPOND_NODE","message":"Webhook workflow has no Respond to Webhook node; verify response behavior and failure paths."})
    connections=workflow.get("connections") or {}
    for n in nodes:
        name=n.get("name") or "<unnamed>"
        t=norm(n.get("type"))
        if not any(h in t for h in NETWORK_HINTS): continue
        if not n.get("retryOnFail",False):
            issues.append({"severity":"MEDIUM","code":"NO_RETRY","node":name,"message":"External/network node has retryOnFail disabled or absent."})
        on_error=n.get("onError")
        if on_error=="continueRegularOutput":
            issues.append({"severity":"HIGH","code":"SILENT_CONTINUE","node":name,"message":"Node continues on regular output after error; downstream logic may treat failure as success."})
        if on_error=="continueErrorOutput":
            main=((connections.get(name) or {}).get("main") or [])
            if len(main)<2 or not main[1]:
                issues.append({"severity":"HIGH","code":"UNWIRED_ERROR_OUTPUT","node":name,"message":"Node is configured for error output but no second/error branch is connected."})
    return issues

def main():
    ap=argparse.ArgumentParser(description="Static QA checks for exported n8n workflow JSON.")
    ap.add_argument("workflow")
    args=ap.parse_args()
    data=json.loads(Path(args.workflow).read_text())
    issues=audit(data)
    print(json.dumps({"issue_count":len(issues),"issues":issues},indent=2))
    return 1 if any(i["severity"]=="HIGH" for i in issues) else 0

if __name__=="__main__": sys.exit(main())
