from seamapi.types import (
    AbstractConnectWebviews,
    ConnectWebview,
    AbstractSeam as Seam,
    AcceptedProvider,
    ConnectWebviewId,
)
import requests
from typing import List, Optional, Union
from seamapi.utils.convert_to_id import to_connect_webview_id


class ConnectWebviews(AbstractConnectWebviews):
    """
    A class used to retrieve connect webview data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list()
        Gets a list of connect webviews
    get(connect_webview)
        Gets a connect webview
    create(
      accepted_providers, custom_redirect_url=None, device_selection_mode==None
    )
        Creates a connect webview
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
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
            A list of connect webviews
        """

        res = requests.get(
            f"{self.seam.api_url}/connect_webviews/list",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webviews = res.json()["connect_webviews"]
        return [
            ConnectWebview(**json_webview)
            for json_webview in json_webviews
        ]

    def get(
        self, connect_webview: Union[ConnectWebviewId, ConnectWebview]
    ) -> ConnectWebview:
        """Gets a connect webview.

        Parameters
        ----------
        connect_webview_id : ConnectWebviewId or ConnectWebview
            Connect webview id or ConnectWebview to get latest version of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ConnectWebview
        """

        connect_webview_id = to_connect_webview_id(connect_webview)
        res = requests.get(
            f"{self.seam.api_url}/connect_webviews/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"connect_webview_id": connect_webview_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_webview = res.json()["connect_webview"]
        return ConnectWebview(**json_webview)

    def create(
        self,
        accepted_providers: List[AcceptedProvider],
        custom_redirect_url: Optional[str] = None,
        device_selection_mode: Optional[str] = None,
    ) -> ConnectWebview:
        """Creates a connect webview.

        Parameters
        ----------
        accepted_providers : list[AcceptedProvider]
            A list of accepted providers e.g. august or noiseaware
        custom_redirect_url : str, optional
            Custom redirect url
        device_selection_mode : str, optional
            Selection mode: 'none', 'single' or 'multiple'

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ConnectWebview
        """

        create_payload = {"accepted_providers": accepted_providers}
        if custom_redirect_url is not None:
            create_payload["custom_redirect_url"] = custom_redirect_url
        if device_selection_mode is not None:
            create_payload["device_selection_mode"] = device_selection_mode
        res = requests.post(
            f"{self.seam.api_url}/connect_webviews/create",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json=create_payload,
        )
        if not res.ok:
            raise Exception(res.text)
        json_webview = res.json()["connect_webview"]
        return ConnectWebview(**json_webview)
