from seamapi.types import (
    AbstractLocks,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
from typing import List, Union, Optional
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class Locks(AbstractLocks):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self, connected_account: Optional[str] = None) -> List[Device]:
        res = requests.post(
            f"{self.seam.api_url}/locks/list",
            params={"connected_account_id": connected_account},
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_locks = res.json()["devices"]
        return [Device.from_dict(d) for d in json_locks]

    def get(self, device: Union[DeviceId, Device]) -> Device:
        device_id = to_device_id(device)
        res = requests.post(
            f"{self.seam.api_url}/locks/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"device_id": device_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_lock = res.json()["device"]
        return Device.from_dict(json_lock)

    def lock_door(self, device: Union[DeviceId, Device]) -> None:
        device_id = to_device_id(device)
        res = requests.post(
            f"{self.seam.api_url}/locks/lock_door",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"device_id": device_id},
        )
        if not res.ok:
            raise Exception(res.text)

    def unlock_door(self, device: Union[DeviceId, Device]) -> None:
        device_id = to_device_id(device)
        res = requests.post(
            f"{self.seam.api_url}/locks/unlock_door",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"device_id": device_id},
        )
        if not res.ok:
            raise Exception(res.text)
