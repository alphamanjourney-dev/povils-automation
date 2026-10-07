import unittest
from n8n_workflow_audit import audit

class AuditTests(unittest.TestCase):
    def test_flags_unattended_http_workflow(self):
        wf={"nodes":[
            {"name":"Webhook","type":"n8n-nodes-base.webhook"},
            {"name":"Call API","type":"n8n-nodes-base.httpRequest","retryOnFail":False}
        ],"connections":{},"settings":{}}
        codes={i["code"] for i in audit(wf)}
        self.assertIn("NO_ERROR_WORKFLOW",codes)
        self.assertIn("WEBHOOK_NO_RESPOND_NODE",codes)
        self.assertIn("NO_RETRY",codes)

    def test_flags_unwired_error_output(self):
        wf={"nodes":[
            {"name":"Schedule","type":"n8n-nodes-base.scheduleTrigger"},
            {"name":"Call API","type":"n8n-nodes-base.httpRequest","retryOnFail":True,"onError":"continueErrorOutput"}
        ],"connections":{"Call API":{"main":[[{"node":"Done","type":"main","index":0}]]}},"settings":{"errorWorkflow":"error-handler-id"}}
        codes={i["code"] for i in audit(wf)}
        self.assertIn("UNWIRED_ERROR_OUTPUT",codes)
        self.assertNotIn("NO_ERROR_WORKFLOW",codes)

    def test_cleaner_webhook_shape(self):
        wf={"nodes":[
            {"name":"Webhook","type":"n8n-nodes-base.webhook"},
            {"name":"Call API","type":"n8n-nodes-base.httpRequest","retryOnFail":True,"onError":"continueErrorOutput"},
            {"name":"Respond","type":"n8n-nodes-base.respondToWebhook"},
            {"name":"Handle Error","type":"n8n-nodes-base.set"}
        ],"connections":{"Call API":{"main":[
            [{"node":"Respond","type":"main","index":0}],
            [{"node":"Handle Error","type":"main","index":0}]
        ]}},"settings":{"errorWorkflow":"error-handler-id"}}
        codes={i["code"] for i in audit(wf)}
        self.assertNotIn("NO_ERROR_WORKFLOW",codes)
        self.assertNotIn("WEBHOOK_NO_RESPOND_NODE",codes)
        self.assertNotIn("NO_RETRY",codes)
        self.assertNotIn("UNWIRED_ERROR_OUTPUT",codes)

if __name__=="__main__": unittest.main()
