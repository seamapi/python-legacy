from seamapi.types import AbstractCredentialsAcs, AbstractSeam as Seam
from typing import Optional, Any


class CredentialsAcs(AbstractCredentialsAcs):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def assign(self, acs_user_id: Any, acs_credential_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/assign", json=json_payload)

        return None

    def create(
        self,
        acs_user_id: Any,
        access_method: Any,
        code: Optional[Any] = None,
        is_multi_phone_sync_credential: Optional[Any] = None,
        external_type: Optional[Any] = None,
        visionline_metadata: Optional[Any] = None,
        starts_at: Optional[Any] = None,
        ends_at: Optional[Any] = None,
    ):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if access_method is not None:
            json_payload["access_method"] = access_method
        if code is not None:
            json_payload["code"] = code
        if is_multi_phone_sync_credential is not None:
            json_payload[
                "is_multi_phone_sync_credential"
            ] = is_multi_phone_sync_credential
        if external_type is not None:
            json_payload["external_type"] = external_type
        if visionline_metadata is not None:
            json_payload["visionline_metadata"] = visionline_metadata
        if starts_at is not None:
            json_payload["starts_at"] = starts_at
        if ends_at is not None:
            json_payload["ends_at"] = ends_at

        self.seam.make_request("POST", "/acs/credentials/create", json=json_payload)

        return None

    def delete(self, acs_credential_id: Any):
        json_payload = {}

        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/delete", json=json_payload)

        return None

    def get(self, acs_credential_id: Any):
        json_payload = {}

        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/get", json=json_payload)

        return None

    def list(
        self,
        acs_user_id: Optional[Any] = None,
        acs_system_id: Optional[Any] = None,
        user_identity_id: Optional[Any] = None,
    ):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if acs_system_id is not None:
            json_payload["acs_system_id"] = acs_system_id
        if user_identity_id is not None:
            json_payload["user_identity_id"] = user_identity_id

        self.seam.make_request("POST", "/acs/credentials/list", json=json_payload)

        return None

    def unassign(self, acs_user_id: Any, acs_credential_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/unassign", json=json_payload)

        return None

    def update(self, acs_credential_id: Any, code: Any):
        json_payload = {}

        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id
        if code is not None:
            json_payload["code"] = code

        self.seam.make_request("POST", "/acs/credentials/update", json=json_payload)

        return None
