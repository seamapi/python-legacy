from seamapi.types import AbstractNetworks, AbstractSeam as Seam
from typing import Optional, Any


class Networks(AbstractNetworks):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(self, network_id: Any):
        json_payload = {}

        if network_id is not None:
            json_payload["network_id"] = network_id

        self.seam.make_request("POST", "/networks/get", json=json_payload)

        return None

    def list(
        self,
    ):
        json_payload = {}

        self.seam.make_request("POST", "/networks/list", json=json_payload)

        return None
