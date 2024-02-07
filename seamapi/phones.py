from seamapi.types import AbstractPhones, AbstractSeam as Seam, Phone
from typing import Optional, Any
from seamapi.phones_simulate import PhonesSimulate


class Phones(AbstractPhones):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam
        self._simulate = PhonesSimulate(seam=seam)

    @property
    def simulate(self) -> PhonesSimulate:
        return self._simulate

    def list(self, owner_user_identity_id: Optional[Any] = None):
        json_payload = {}

        if owner_user_identity_id is not None:
            json_payload["owner_user_identity_id"] = owner_user_identity_id

        res = self.seam.make_request("POST", "/phones/list", json=json_payload)

        return [Phone.from_dict(item) for item in res["phones"]]
