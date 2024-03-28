from seamapi.types import AbstractAcsEntrances, AbstractSeam as Seam
from typing import Optional, Any, List, Dict, Union


class AcsEntrances(AbstractAcsEntrances):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(self, *, acs_entrance_id: str) -> None:
        json_payload = {}

        if acs_entrance_id is not None:
            json_payload["acs_entrance_id"] = acs_entrance_id

        self.seam.make_request("POST", "/acs/entrances/get", json=json_payload)

        return None

    def grant_access(self, *, acs_entrance_id: str, acs_user_id: str) -> None:
        json_payload = {}

        if acs_entrance_id is not None:
            json_payload["acs_entrance_id"] = acs_entrance_id
        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request("POST", "/acs/entrances/grant_access", json=json_payload)

        return None

    def list(
        self,
        *,
        acs_system_id: Optional[str] = None,
        acs_credential_id: Optional[str] = None
    ) -> None:
        json_payload = {}

        if acs_system_id is not None:
            json_payload["acs_system_id"] = acs_system_id
        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/entrances/list", json=json_payload)

        return None

    def list_credentials_with_access(
        self, *, acs_entrance_id: str, include_if: Optional[List[str]] = None
    ) -> None:
        json_payload = {}

        if acs_entrance_id is not None:
            json_payload["acs_entrance_id"] = acs_entrance_id
        if include_if is not None:
            json_payload["include_if"] = include_if

        self.seam.make_request(
            "POST", "/acs/entrances/list_credentials_with_access", json=json_payload
        )

        return None