from seamapi.types import (
    AbstractDevicesUnmanaged,
    AbstractSeam as Seam,
    UnmanagedDevice,
)
from typing import Optional, Any


class DevicesUnmanaged(AbstractDevicesUnmanaged):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(self, device_id: Optional[Any] = None, name: Optional[Any] = None):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if name is not None:
            json_payload["name"] = name

        res = self.seam.make_request(
            "POST", "/devices/unmanaged/get", json=json_payload
        )

        return UnmanagedDevice.from_dict(res["device"])

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

        res = self.seam.make_request(
            "POST", "/devices/unmanaged/list", json=json_payload
        )

        return [UnmanagedDevice.from_dict(item) for item in res["devices"]]

    def update(self, device_id: Any, is_managed: Any):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if is_managed is not None:
            json_payload["is_managed"] = is_managed

        self.seam.make_request("POST", "/devices/unmanaged/update", json=json_payload)

        return None
