from seamapi.types import AbstractDevices, Device, DeviceId
from typing import List, Union


class ConnectWebviews(AbstractDevices):
    def list(self) -> List[Device]:
        raise NotImplementedError

    def get(self, device: Union[DeviceId, Device]) -> Device:
        raise NotImplementedError
