from seamapi.types import AbstractEvents, AbstractSeam as Seam, Event
from typing import Optional, Any


class Events(AbstractEvents):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(
        self,
        event_id: Any,
        event_type: Optional[Any] = None,
        device_id: Optional[Any] = None,
    ):
        json_payload = {}
        if event_id is not None:
            json_payload["event_id"] = event_id
        if event_type is not None:
            json_payload["event_type"] = event_type
        if device_id is not None:
            json_payload["device_id"] = device_id
        res = self.seam.make_request("POST", "/events/get", json=json_payload)
        return Event.from_dict(res["event"])

    def list(
        self,
        since: Optional[Any] = None,
        between: Optional[Any] = None,
        device_id: Optional[Any] = None,
        device_ids: Optional[Any] = None,
        access_code_id: Optional[Any] = None,
        access_code_ids: Optional[Any] = None,
        event_type: Optional[Any] = None,
        event_types: Optional[Any] = None,
        connected_account_id: Optional[Any] = None,
    ):
        json_payload = {}
        if since is not None:
            json_payload["since"] = since
        if between is not None:
            json_payload["between"] = between
        if device_id is not None:
            json_payload["device_id"] = device_id
        if device_ids is not None:
            json_payload["device_ids"] = device_ids
        if access_code_id is not None:
            json_payload["access_code_id"] = access_code_id
        if access_code_ids is not None:
            json_payload["access_code_ids"] = access_code_ids
        if event_type is not None:
            json_payload["event_type"] = event_type
        if event_types is not None:
            json_payload["event_types"] = event_types
        if connected_account_id is not None:
            json_payload["connected_account_id"] = connected_account_id
        res = self.seam.make_request("POST", "/events/list", json=json_payload)
        return [Event.from_dict(item) for item in res["events"]]
