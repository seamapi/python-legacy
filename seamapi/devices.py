from seamapi.types import AbstractDevices, Device, DeviceId, AbstractSeam as Seam
from typing import List, Union, Optional
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class Devices(AbstractDevices):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(
        self,
        connected_account: Optional[str] = None,
        connect_webview: Optional[str] = None,
    ) -> List[Device]:
        params = {}
        if connected_account:
            params["connected_account_id"] = connected_account
        if connect_webview:
            params["connect_webview_id"] = connect_webview
        res = requests.get(
            f"{self.seam.api_url}/devices/list",
            params=params,
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        devices = res.json()["devices"]
        return [Device.from_dict(d) for d in devices]

    def get(self, device: Union[DeviceId, Device]) -> Device:
        device_id = to_device_id(device)
        res = requests.get(
            f"{self.seam.api_url}/devices/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"device_id": device_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_device = res.json()["device"]
        return Device.from_dict(json_device)
