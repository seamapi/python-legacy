from seamapi.types import (
    AbstractConnectedAccounts,
    ConnectedAccount,
    AbstractSeam as Seam,
)
import requests
from typing import List, Optional


class ConnectedAccounts(AbstractConnectedAccounts):
    """
    A class used to retreive connected account data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
        Initial seam class

    Methods
    -------
    list()
        Gets a list of connected accounts
    get(connected_account_id)
        Gets a connected account
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : dict
          Intial seam class
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
        """Gets a connected account.

        Parameters
        ----------
        connected_account_id : str
            Connected account id

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A connected account dict.
        """

        res = requests.get(
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
