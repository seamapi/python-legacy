import os

from .routes import Routes
import requests
from importlib.metadata import version
from typing import Optional, cast
from .types import AbstractSeam, SeamAPIException


class Seam(AbstractSeam):
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
            "User-Agent": "Python SDK v"
            + version("seamapi")
            + " (https://github.com/seamapi/python)",
        }
        response = requests.request(method, url, headers=headers, **kwargs)

        parsed_response = response.json()

        if response.status_code != 200:
            error_message = (
                parsed_response["error"]
                if isinstance(parsed_response, dict)
                else parsed_response
            )
            raise SeamAPIException(
                response.status_code,
                response.headers.get("seam-request-id", None),
                error_message,
            )
        ## TODO automatically paginate if kwargs["auto_paginate"] is True

        return parsed_response
