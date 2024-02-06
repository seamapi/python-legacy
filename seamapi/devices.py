from seamapi.types import AbstractDevices, AbstractSeam as Seam, Device, DeviceProvider
from typing import Optional, Any
from seamapi.devices_unmanaged import DevicesUnmanaged


class Devices(AbstractDevices):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam
        self._unmanaged = DevicesUnmanaged(seam=seam)

    @property
    def unmanaged(self) -> DevicesUnmanaged:
        return self._unmanaged

    def delete(self, device_id: Any):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id

        self.seam.make_request("POST", "/devices/delete", json=json_payload)

        return None

    def get(self, device_id: Optional[Any] = None, name: Optional[Any] = None):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if name is not None:
            json_payload["name"] = name

        res = self.seam.make_request("POST", "/devices/get", json=json_payload)

        return Device.from_dict(res["device"])

    def list(
        self,
        connected_account_id: Optional[Any] = None,
        connected_account_ids: Optional[Any] = None,
        connect_webview_id: Optional[Any] = None,
        device_type: Optional[Any] = None,
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
        if device_type is not None:
            json_payload["device_type"] = device_type
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

        res = self.seam.make_request("POST", "/devices/list", json=json_payload)

        return [Device.from_dict(item) for item in res["devices"]]

    def list_device_providers(self, provider_category: Optional[Any] = None):
        json_payload = {}

        if provider_category is not None:
            json_payload["provider_category"] = provider_category

        res = self.seam.make_request(
            "POST", "/devices/list_device_providers", json=json_payload
        )

        return [DeviceProvider.from_dict(item) for item in res["device_providers"]]

    def update(
        self,
        device_id: Any,
        properties: Optional[Any] = None,
        name: Optional[Any] = None,
        is_managed: Optional[Any] = None,
        custom_metadata: Optional[Any] = None,
    ):
        json_payload = {}

        if device_id is not None:
            json_payload["device_id"] = device_id
        if properties is not None:
            json_payload["properties"] = properties
        if name is not None:
            json_payload["name"] = name
        if is_managed is not None:
            json_payload["is_managed"] = is_managed
        if custom_metadata is not None:
            json_payload["custom_metadata"] = custom_metadata

        self.seam.make_request("POST", "/devices/update", json=json_payload)

        return None
