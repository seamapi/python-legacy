from seamapi.types import (
    AbstractAccessCodes,
    AccessCode,
    AccessCodeId,
    ActionAttempt,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
from typing import List, Optional, Union, Any
import requests


def to_access_code_id(access_code: Union[AccessCodeId, AccessCode]) -> str:
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

    def get(self, access_code: Union[AccessCodeId, AccessCode]) -> AccessCode:
        access_code_id = to_access_code_id(access_code)
        res = requests.get(
            f"{self.seam.api_url}/access_codes/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"access_code_id": access_code_id},
        )
        if not res.ok:
            raise Exception(res.text)
        return AccessCode.from_dict(res.json()["access_code"])

    def create(
        self,
        device: Union[DeviceId, Device],
        name: str,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
    ) -> AccessCode:
        device_id = to_device_id(device)
        create_payload = {"device_id": device_id, "name": name}
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
        action_attempt = self.seam.action_attempts.poll_until_ready(
            res.json()["action_attempt"]["action_attempt_id"]
        )
        success_res: Any = action_attempt.result
        return AccessCode.from_dict(success_res["access_code"])

    def delete(self, access_code: Union[AccessCodeId, AccessCode]) -> ActionAttempt:
        access_code_id = to_access_code_id(access_code)
        res = requests.delete(
            (f"{self.seam.api_url}/access_codes/delete"),
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"access_code_id": access_code_id},
        )
        if not res.ok:
            raise Exception(res.text)
        action_attempt = self.seam.action_attempts.poll_until_ready(
            res.json()["action_attempt"]["action_attempt_id"]
        )
        if action_attempt.status == "error" and action_attempt.error:
            raise Exception(
                f"{action_attempt.error.type}: {action_attempt.error.message}"
            )
        return action_attempt
