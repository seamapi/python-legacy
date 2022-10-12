import os

from seamapi.utils.get_sentry_dsn import get_sentry_dsn
from .routes import Routes
import requests
import sentry_sdk
import pkg_resources
from typing import Optional, cast
from .types import AbstractSeam, SeamAPIException


class Seam(AbstractSeam):
    """
    Initial Seam class used to interact with Seam API

    ...

    Attributes
    ----------
    api_key : str
        API key (default None)
    api_url : str
        API url (default None)
    workspaces : Workspaces
        Workspaces class
    connected_accounts : ConnectedAccounts
        Connected accounts class
    connect_webviews : ConnectWebviews
        Connect webviews class
    devices : Devices
        Devices class
    events : Events
        Events class
    locks : Locks
        Locks class
    access_codes : AccessCodes
        Access codes class
    action_attempts : ActionAttempts
        Action attempts class
    """

    api_key: str
    api_url: str = "https://connect.getseam.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        should_report_exceptions: Optional[bool] = False,
    ):
        """
        Parameters
        ----------
        api_key : str, optional
          API key
        api_url : str, optional
          API url
        should_report_exceptions : bool, optional
          Defaults to False. If true, thrown exceptions will be reported to Seam.
        """
        Routes.__init__(self)

        if api_key is None:
            api_key = os.environ.get("SEAM_API_KEY", None)
        if api_key is None:
            raise Exception(
                "SEAM_API_KEY not found in environment, and api_key not provided"
            )
        if api_url is None:
            api_url = os.environ.get("SEAM_API_URL", self.api_url)
        self.api_key = api_key
        self.api_url = cast(str, api_url)
        self.should_report_exceptions = should_report_exceptions

        if self.should_report_exceptions:
            self.sentry_client = sentry_sdk.Hub(sentry_sdk.Client(
                dsn=get_sentry_dsn(),
            ))
            self.sentry_client.scope.set_context("sdk_info", {
                "repository": "https://github.com/seamapi/python",
                "version": pkg_resources.get_distribution("seamapi").version,
                "endpoint": self.api_url,
            })

    def make_request(self, method: str, path: str, **kwargs):
        """
        Makes a request to the API

        Parameters
        ----------
        method : str
          Request method
        path : str
          Request path
        **kwargs
          Keyword arguments passed to requests.request
        """

        url = self.api_url + path
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "Python SDK v" + pkg_resources.get_distribution("seamapi").version + " (https://github.com/seamapi/python)",
        }
        response = requests.request(method, url, headers=headers, **kwargs)

        if self.should_report_exceptions and response.status_code:
            # Add breadcrumb
            self.sentry_client.add_breadcrumb(
                category="http",
                level="info",
                data={
                    "method": method,
                    "url": url,
                    "status_code": response.status_code,
                    "request_id": response.headers.get("seam-request-id", "unknown"),
                },
            )


        parsed_response = response.json()

        if response.status_code != 200:
            raise SeamAPIException(
                response.status_code,
                response.headers["seam-request-id"],
                parsed_response["error"],
            )

        return parsed_response
