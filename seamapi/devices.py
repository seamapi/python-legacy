from seamapi.types import AbstractDevices, Device, DeviceId, AbstractSeam as Seam
from typing import List, Union
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class Devices(AbstractDevices):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self) -> List[Device]:
        res = requests.get(
            f"{self.seam.api_url}/devices/list",
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
