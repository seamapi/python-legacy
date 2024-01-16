from seamapi.types import (
    AbstractCredentialProvisioningAutomationsAcs,
    AbstractSeam as Seam,
)
from typing import Optional, Any


class CredentialProvisioningAutomationsAcs(
    AbstractCredentialProvisioningAutomationsAcs
):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def launch(
        self,
        user_identity_id: Optional[Any] = None,
        credential_manager_acs_system_id: Optional[Any] = None,
        acs_credential_pool_id: Optional[Any] = None,
        create_credential_manager_user: Optional[Any] = None,
        credential_manager_acs_user_id: Optional[Any] = None,
    ):
        json_payload = {}
        if user_identity_id is not None:
            json_payload["user_identity_id"] = user_identity_id
        if credential_manager_acs_system_id is not None:
            json_payload[
                "credential_manager_acs_system_id"
            ] = credential_manager_acs_system_id
        if acs_credential_pool_id is not None:
            json_payload["acs_credential_pool_id"] = acs_credential_pool_id
        if create_credential_manager_user is not None:
            json_payload[
                "create_credential_manager_user"
            ] = create_credential_manager_user
        if credential_manager_acs_user_id is not None:
            json_payload[
                "credential_manager_acs_user_id"
            ] = credential_manager_acs_user_id
        res = self.seam.make_request(
            "POST", "/acs/credential_provisioning_automations/launch", json=json_payload
        )
        return None.from_dict(res[""])
