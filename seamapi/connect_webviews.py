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
from seamapi.utils.report_error import report_error


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
      accepted_providers, custom_redirect_url=None, custom_redirect_failure_url=None, device_selection_mode=None, provider_category=None, custom_metadata=None, automatically_manage_new_devices=None, wait_for_device_creation=None
    )
        Creates a connect webview
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

    @report_error
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

        res = self.seam.make_request(
            "GET",
            "/connect_webviews/list",
        )
        json_webviews = res["connect_webviews"]

        return [
            ConnectWebview.from_dict(json_webview)
            for json_webview in json_webviews
        ]

    @report_error
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
        res = self.seam.make_request(
            "GET",
            "/connect_webviews/get",
            params={"connect_webview_id": connect_webview_id},
        )
        json_webview = res["connect_webview"]

        return ConnectWebview.from_dict(json_webview)

    @report_error
    def create(
        self,
        accepted_providers: Optional[List[AcceptedProvider]] = None,
        provider_category: Optional[str] = None,
        custom_redirect_url: Optional[str] = None,
        custom_redirect_failure_url: Optional[str] = None,
        device_selection_mode: Optional[str] = None,
        custom_metadata: Optional[dict] = None,
        automatically_manage_new_devices: Optional[bool] = None,
        wait_for_device_creation: Optional[bool] = None,
    ) -> ConnectWebview:
        """Creates a connect webview.

        Parameters
        ----------
        provider_category : str, optional
            Provider category e.g. stable
        accepted_providers : list[AcceptedProvider], optional
            A list of accepted providers e.g. august or noiseaware
        custom_redirect_url : str, optional
            Custom redirect url
        custom_redirect_failure_url : str, optional
            Custom redirect failure url
        device_selection_mode : str, optional
            Selection mode: 'none', 'single' or 'multiple'
        custom_metadata : dict, optional
        automatically_manage_new_devices : bool, optional
            Defaults to true, whether newly added devices should appear as a Managed Device
        wait_for_device_creation : bool, optional
            Wait until your connected account and devices are synced

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ConnectWebview
        """

        create_payload = {}

        if accepted_providers is None and provider_category is None:
            raise Exception(
                "Must provide either accepted_providers or category"
            )

        if accepted_providers is not None:
            create_payload["accepted_providers"] = accepted_providers
        if provider_category is not None:
            create_payload["provider_category"] = provider_category
        if custom_redirect_url is not None:
            create_payload["custom_redirect_url"] = custom_redirect_url
        if custom_redirect_failure_url is not None:
            create_payload[
                "custom_redirect_failure_url"
            ] = custom_redirect_failure_url
        if device_selection_mode is not None:
            create_payload["device_selection_mode"] = device_selection_mode
        if custom_metadata is not None:
            create_payload["custom_metadata"] = custom_metadata
        if automatically_manage_new_devices is not None:
            create_payload[
                "automatically_manage_new_devices"
            ] = automatically_manage_new_devices
        if wait_for_device_creation is not None:
            create_payload[
                "wait_for_device_creation"
            ] = wait_for_device_creation

        res = self.seam.make_request(
            "POST",
            "/connect_webviews/create",
            json=create_payload,
        )
        json_webview = res["connect_webview"]

        return ConnectWebview.from_dict(json_webview)
