from seamapi.types import (
    AbstractAccessCodes,
    AccessCode,
    AccessCodeId,
    ActionAttempt,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
from typing import List, Optional, Union
import requests


def to_access_code_id(
    access_code: Union[AccessCodeId, AccessCode]
) -> str:
    if isinstance(access_code, str):
        return access_code
    return access_code.access_code_id


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

    def create(
        self,
        device: Union[DeviceId, Device],
        name: str,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
    ) -> None:
        device_id = to_device_id(device)
        create_payload = {
            "device_id": device_id,
            "name": name
        }
        if code is not None:
            create_payload["code"] = code
        if starts_at is not None:
            create_payload["starts_at"] = starts_at
        if ends_at is not None:
            create_payload["ends_at"] = ends_at
        res = requests.post(
            f"{self.seam.api_url}/access_codes/create",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json=create_payload,
        )
        if not res.ok:
            raise Exception(res.text)
        return res.json()

    def delete(
        self,
        access_code: Union[AccessCodeId, AccessCode]
    ) -> ActionAttempt:
        access_code_id = to_access_code_id(access_code)
        res = requests.delete(
            (
                f"{self.seam.api_url}/access_codes/delete?"
                f"access_code_id={access_code_id}"
            ),
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        action_attempt = res.json()
        return action_attempt
