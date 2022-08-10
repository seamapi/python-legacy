from seamapi.types import (
    AbstractConnectedAccounts,
    ConnectedAccount,
    AbstractSeam as Seam,
    ConnectedAccountId,
)

import requests
from typing import Any, Dict, List, Union
from seamapi.utils.convert_to_id import to_connected_account_id


class ConnectedAccounts(AbstractConnectedAccounts):
    """
    A class used to retrieve connected account data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list()
        Gets a list of connected accounts
    get(connected_account)
        Gets a connected account
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Initial seam class
        """

        self.seam = seam

    def list(self) -> List[ConnectedAccount]:
        """Gets a list of connected accounts.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of connected accounts.
        """

        res = requests.get(
            f"{self.seam.api_url}/connected_accounts/list",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_accounts: List[Dict[str, Any]] = res.json()["connected_accounts"]
        return [
            ConnectedAccount(
                connected_account_id=json_account["connected_account_id"],
                created_at=json_account["created_at"],
                user_identifier=json_account["user_identifier"],
                account_type=json_account["account_type"],
                errors=json_account.get("errors", []),
            )
            for json_account in json_accounts
        ]

    def get(
        self,
        connected_account: Union[ConnectedAccountId, ConnectedAccount],
    ) -> ConnectedAccount:
        """Gets a connected account.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount
            Connected account id or ConnectedAccount to get the latest version of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ConnectedAccount
        """

        connected_account_id = to_connected_account_id(connected_account)
        res = requests.get(
            f"{self.seam.api_url}/connected_accounts/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"connected_account_id": connected_account_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_account: Dict[str, Any] = res.json()["connected_account"]
        return ConnectedAccount(
            connected_account_id=json_account["connected_account_id"],
            created_at=json_account["created_at"],
            user_identifier=json_account["user_identifier"],
            account_type=json_account["account_type"],
            errors=json_account.get("errors", []),
        )
