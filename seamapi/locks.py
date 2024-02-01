from seamapi.types import AbstractLocks, AbstractSeam as Seam, Device, ActionAttempt
from typing import Optional, Any


class Locks(AbstractLocks):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(self, device_id: Optional[Any] = None, name: Optional[Any] = None):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if name is not None:
            json_payload["name"] = name

        res = self.seam.make_request("POST", "/locks/get", json=json_payload)

        return Device.from_dict(res["device"])

    def list(
        self,
        connected_account_id: Optional[Any] = None,
        connected_account_ids: Optional[Any] = None,
        connect_webview_id: Optional[Any] = None,
        device_types: Optional[Any] = None,
        manufacturer: Optional[Any] = None,
        device_ids: Optional[Any] = None,
        limit: Optional[Any] = None,
        created_before: Optional[Any] = None,
        user_identifier_key: Optional[Any] = None,
        custom_metadata_has: Optional[Any] = None,
    ):
        json_payload = {}

        if connected_account_id is not None:
            json_payload["connected_account_id"] = connected_account_id
        if connected_account_ids is not None:
            json_payload["connected_account_ids"] = connected_account_ids
        if connect_webview_id is not None:
            json_payload["connect_webview_id"] = connect_webview_id
        if device_types is not None:
            json_payload["device_types"] = device_types
        if manufacturer is not None:
            json_payload["manufacturer"] = manufacturer
        if device_ids is not None:
            json_payload["device_ids"] = device_ids
        if limit is not None:
            json_payload["limit"] = limit
        if created_before is not None:
            json_payload["created_before"] = created_before
        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key
        if custom_metadata_has is not None:
            json_payload["custom_metadata_has"] = custom_metadata_has

        res = self.seam.make_request("POST", "/locks/list", json=json_payload)

        return [Device.from_dict(item) for item in res["devices"]]

    def lock_door(
        self,
        device_id: Any,
        sync: Optional[Any] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if sync is not None:
            json_payload["sync"] = sync

        res = self.seam.make_request("POST", "/locks/lock_door", json=json_payload)

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(res["action_attempt"])

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )

        return updated_action_attempt

    def unlock_door(
        self,
        device_id: Any,
        sync: Optional[Any] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if sync is not None:
            json_payload["sync"] = sync

        res = self.seam.make_request("POST", "/locks/unlock_door", json=json_payload)

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(res["action_attempt"])

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )

        return updated_action_attempt
