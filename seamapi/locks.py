from seamapi.types import (
    AbstractLocks,
    Device,
    DeviceId,
    ActionAttempt,
    AbstractSeam as Seam,
)
from typing import List, Union
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class Locks(AbstractLocks):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self) -> List[Device]:
        raise NotImplementedError

    def get(self, device: Union[DeviceId, Device]) -> Device:
        device_id = to_device_id(device)
        raise NotImplementedError

    def lock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        device_id = to_device_id(device)
        raise NotImplementedError

    def unlock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        device_id = to_device_id(device)
        raise NotImplementedError
