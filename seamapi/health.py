from seamapi.types import AbstractHealth, AbstractSeam as Seam
from typing import Optional, Any


class Health(AbstractHealth):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get_service_health(self, service: Optional[Any] = None):
        json_payload = {}
        if service is not None:
            json_payload["service"] = service
        res = self.seam.make_request(
            "POST", "/health/get_service_health", json=json_payload
        )
        return None
