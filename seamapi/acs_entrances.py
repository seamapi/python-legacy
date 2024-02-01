from seamapi.types import AbstractEntrancesAcs, AbstractSeam as Seam
from typing import Optional, Any


class EntrancesAcs(AbstractEntrancesAcs):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(self, acs_entrance_id: Any):
        json_payload = {}

        if acs_entrance_id is not None:
            json_payload["acs_entrance_id"] = acs_entrance_id

        self.seam.make_request("POST", "/acs/entrances/get", json=json_payload)

        return None

    def grant_access(self, acs_entrance_id: Any, acs_user_id: Any):
        json_payload = {}

        if acs_entrance_id is not None:
            json_payload["acs_entrance_id"] = acs_entrance_id
        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request("POST", "/acs/entrances/grant_access", json=json_payload)

        return None

    def list(
        self,
        acs_system_id: Optional[Any] = None,
        acs_credential_id: Optional[Any] = None,
    ):
        json_payload = {}

        if acs_system_id is not None:
            json_payload["acs_system_id"] = acs_system_id
        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/entrances/list", json=json_payload)

        return None

    def list_credentials_with_access(
        self,
        acs_entrance_id: Optional[Any] = None,
        acs_entrance_ids: Optional[Any] = None,
        include_if: Optional[Any] = None,
    ):
        json_payload = {}

        if acs_entrance_id is not None:
            json_payload["acs_entrance_id"] = acs_entrance_id
        if acs_entrance_ids is not None:
            json_payload["acs_entrance_ids"] = acs_entrance_ids
        if include_if is not None:
            json_payload["include_if"] = include_if

        self.seam.make_request(
            "POST", "/acs/entrances/list_credentials_with_access", json=json_payload
        )

        return None
