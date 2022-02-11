from seamapi.types import (
    AbstractConnectedAccounts,
    ConnectedAccount,
    AbstractSeam as Seam,
)
import requests
from typing import List, Optional


class ConnectedAccounts(AbstractConnectedAccounts):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def list(self) -> List[ConnectedAccount]:
        res = requests.post(
            f"{self.seam.api_url}/connected_accounts/list",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_accounts = res.json()["connected_accounts"]
        return [
            ConnectedAccount(
                connected_account_id=json_account["connected_account_id"],
                created_at=json_account["created_at"],
                user_identifier=json_account["user_identifier"],
                account_type=json_account["account_type"],
            )
            for json_account in json_accounts
        ]

    def get(self, connected_account_id: str) -> ConnectedAccount:
        res = requests.post(
            f"{self.seam.api_url}/connected_accounts/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"connected_account_id": connected_account_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_account = res.json()["connected_account"]
        return ConnectedAccount(
                connected_account_id=json_account["connected_account_id"],
                created_at=json_account["created_at"],
                user_identifier=json_account["user_identifier"],
                account_type=json_account["account_type"],
            )
