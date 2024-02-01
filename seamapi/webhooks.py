from seamapi.types import AbstractWebhooks, AbstractSeam as Seam, Webhook
from typing import Optional, Any


class Webhooks(AbstractWebhooks):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def create(self, url: Any, event_types: Optional[Any] = None):
        json_payload = {}

        if url is not None:
            json_payload["url"] = url
        if event_types is not None:
            json_payload["event_types"] = event_types

        res = self.seam.make_request("POST", "/webhooks/create", json=json_payload)

        return Webhook.from_dict(res["webhook"])

    def delete(self, webhook_id: Any):
        json_payload = {}

        if webhook_id is not None:
            json_payload["webhook_id"] = webhook_id

        self.seam.make_request("POST", "/webhooks/delete", json=json_payload)

        return None

    def get(self, webhook_id: Any):
        json_payload = {}

        if webhook_id is not None:
            json_payload["webhook_id"] = webhook_id

        res = self.seam.make_request("POST", "/webhooks/get", json=json_payload)

        return Webhook.from_dict(res["webhook"])

    def list(
        self,
    ):
        json_payload = {}

        res = self.seam.make_request("POST", "/webhooks/list", json=json_payload)

        return [Webhook.from_dict(item) for item in res["webhooks"]]
