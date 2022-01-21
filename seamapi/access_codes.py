from seamapi.types import (
    AbstractAccessCodes,
    AccessCode,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
from typing import List, Union
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class AccessCodes(AbstractAccessCodes):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self, device: Union[DeviceId, Device]) -> List[AccessCode]:
        device_id = to_device_id(device)
        res = requests.get(
            f"{self.seam.api_url}/access_codes/list?device_id={device_id}",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        access_codes = res.json()["access_codes"]
        return [AccessCode.from_dict(ac) for ac in access_codes]

    def create(self, device: Union[DeviceId, Device], name: str, code: str) -> None:
        device_id = to_device_id(device)
        res = requests.post(
            f"{self.seam.api_url}/access_codes/create",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={
                "device_id": device_id,
                "name": name,
                "code": code,
            },
        )
        if not res.ok:
            raise Exception(res.text)
