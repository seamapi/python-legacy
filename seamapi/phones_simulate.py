from seamapi.types import AbstractPhonesSimulate, AbstractSeam as Seam, Phone
from typing import Optional, Any


class PhonesSimulate(AbstractPhonesSimulate):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def create_sandbox_phone(
        self,
        assa_abloy_credential_service_acs_system_id: Any,
        user_identity_id: Any,
        custom_sdk_installation_id: Optional[Any] = None,
        phone_metadata: Optional[Any] = None,
        assa_abloy_metadata: Optional[Any] = None,
    ):
        json_payload = {}

        if assa_abloy_credential_service_acs_system_id is not None:
            json_payload[
                "assa_abloy_credential_service_acs_system_id"
            ] = assa_abloy_credential_service_acs_system_id
        if user_identity_id is not None:
            json_payload["user_identity_id"] = user_identity_id
        if custom_sdk_installation_id is not None:
            json_payload["custom_sdk_installation_id"] = custom_sdk_installation_id
        if phone_metadata is not None:
            json_payload["phone_metadata"] = phone_metadata
        if assa_abloy_metadata is not None:
            json_payload["assa_abloy_metadata"] = assa_abloy_metadata

        res = self.seam.make_request(
            "POST", "/phones/simulate/create_sandbox_phone", json=json_payload
        )

        return Phone.from_dict(res["phone"])
