from seamapi.types import AbstractDevices, Device, DeviceId, AbstractSeam as Seam
from typing import List, Union
import requests


class Devices(AbstractDevices):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self) -> List[Device]:
        raise NotImplementedError

    def get(self, device: Union[DeviceId, Device]) -> Device:
        raise NotImplementedError
