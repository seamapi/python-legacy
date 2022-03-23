from seamapi.types import (
    AbstractConnectWebviews,
    ConnectWebview,
    AbstractSeam as Seam,
    AcceptedProvider,
)
import requests
from typing import List, Optional


class ConnectWebviews(AbstractConnectWebviews):
    """
    A class used to retreive connect webview data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
        Initial seam class

    Methods
    -------
    list()
        Gets a list of connect webviews
    get(connect_webview_id)
        Gets a connect webview
    create(accepted_providers)
        Creates a connect webview
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

    def list(self) -> List[ConnectWebview]:
        """Gets a list of connect webviews.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of connect webviews.
        """

        res = requests.post(
            f"{self.seam.api_url}/connect_webviews/list",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webviews = res.json()["connect_webviews"]
        return [
            ConnectWebview(
                connect_webview_id=json_webview["connect_webview_id"],
                status=json_webview["status"],
                url=json_webview["url"],
                login_successful=json_webview["login_successful"],
                connected_account_id=json_webview["connected_account_id"],
            )
            for json_webview in json_webviews
        ]

    def get(self, connect_webview_id: str) -> ConnectWebview:
        """Gets a connect webview.

        Parameters
        ----------
        connect_webview_id : str
            Connect webview id

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A connect webview dict.
        """

        res = requests.get(
            f"{self.seam.api_url}/connect_webviews/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"connect_webview_id": connect_webview_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webview = res.json()["connect_webview"]
        return ConnectWebview(
            connect_webview_id=json_webview["connect_webview_id"],
            status=json_webview["status"],
            url=json_webview["url"],
            login_successful=json_webview["login_successful"],
            connected_account_id=json_webview["connected_account_id"],
        )

    def create(
        self, accepted_providers: Optional[List[AcceptedProvider]] = []
    ) -> ConnectWebview:
        """Creates a connect webview.

        Parameters
        ----------
        accepted_providers : list, optional
            A list of accepted providers e.g. august or noiseaware

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A connect webview dict.
        """

        res = requests.post(
            f"{self.seam.api_url}/connect_webviews/create",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"accepted_providers": accepted_providers},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webview = res.json()["connect_webview"]
        return ConnectWebview(
            connect_webview_id=json_webview["connect_webview_id"],
            status=json_webview["status"],
            url=json_webview["url"],
            login_successful=json_webview["login_successful"],
            connected_account_id=None,
        )
