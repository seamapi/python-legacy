from seamapi.types import (
    AbstractConnectedAccounts,
    AbstractSeam as Seam,
    ConnectedAccount,
)
from typing import Optional, Any


class ConnectedAccounts(AbstractConnectedAccounts):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def delete(
        self, connected_account_id: Optional[Any] = None, sync: Optional[Any] = None
    ):
        json_payload = {}
        if connected_account_id is not None:
            json_payload["connected_account_id"] = connected_account_id
        if sync is not None:
            json_payload["sync"] = sync
        res = self.seam.make_request(
            "POST", "/connected_accounts/delete", json=json_payload
        )
        return None.from_dict(res[""])

    def get(self, connected_account_id: Any, email: Optional[Any] = None):
        json_payload = {}
        if connected_account_id is not None:
            json_payload["connected_account_id"] = connected_account_id
        if email is not None:
            json_payload["email"] = email
        res = self.seam.make_request(
            "POST", "/connected_accounts/get", json=json_payload
        )
        return ConnectedAccount.from_dict(res["connected_account"])

    def list(
        self,
    ):
        json_payload = {}
        res = self.seam.make_request(
            "POST", "/connected_accounts/list", json=json_payload
        )
        return [ConnectedAccount.from_dict(item) for item in res["connected_accounts"]]

    def update(
        self,
        connected_account_id: Optional[Any] = None,
        automatically_manage_new_devices: Optional[Any] = None,
    ):
        json_payload = {}
        if connected_account_id is not None:
            json_payload["connected_account_id"] = connected_account_id
        if automatically_manage_new_devices is not None:
            json_payload[
                "automatically_manage_new_devices"
            ] = automatically_manage_new_devices
        res = self.seam.make_request(
            "POST", "/connected_accounts/update", json=json_payload
        )
        return ConnectedAccount.from_dict(res["connected_account"])
