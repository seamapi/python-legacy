from seamapi.types import (
    AbstractLocks,
    ActionAttempt,
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
import time
from typing import List, Union, Optional, cast
import requests
from seamapi.utils.convert_to_id import (
    to_connect_webview_id,
    to_connected_account_id,
    to_device_id,
)
from seamapi.utils.report_error import report_error


class Locks(AbstractLocks):
    """
    A class used to retreive lock data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(connected_account=None, connect_webview=None)
        Gets a list of locks
    get(device=None, name=None)
        Gets a lock
    lock_door(device)
        Locks a lock
    unlock_door(device)
        Unlocks a lock
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

    @report_error
    def list(
        self,
        connected_account: Optional[
            Union[ConnectedAccountId, ConnectedAccount]
        ] = None,
        connect_webview: Optional[
            Union[ConnectWebviewId, ConnectWebview]
        ] = None,
    ) -> List[Device]:
        """Gets a list of locks.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount, optional
            Connected account id or ConnectedAccount to get locks associated with
        connect_webview : ConnectWebviewId or ConnectWebview, optional
            Connect webview id or ConnectWebview to get locks associated with

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of locks.
        """

        params = {}
        if connected_account:
            params["connected_account_id"] = to_connected_account_id(
                connected_account
            )
        if connect_webview:
            params["connect_webview_id"] = to_connect_webview_id(
                connect_webview
            )

        res = self.seam.make_request(
            "GET",
            "/locks/list",
            params=params,
        )
        json_locks = res["devices"]

        return [Device.from_dict(d) for d in json_locks]

    @report_error
    def get(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
    ) -> Device:
        """Gets a lock.

        Parameters
        ----------
        device : DeviceId or Device, optional
            Device id or Device to get the latest state of
        name : str, optional
            Device name

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A lock dict.
        """

        params = {}
        if device:
            params["device_id"] = to_device_id(device)
        if name:
            params["name"] = name

        res = self.seam.make_request(
            "GET",
            "/locks/get",
            params=params,
        )
        json_lock = res["device"]

        return Device.from_dict(json_lock)

    @report_error
    def lock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        """Locks a lock.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to be locked

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        device_id = to_device_id(device)
        res = self.seam.make_request(
            "POST",
            "/locks/lock_door",
            json={"device_id": device_id},
        )

        return self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )

    @report_error
    def unlock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        """Unlocks a lock.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to be locked

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        device_id = to_device_id(device)
        res = self.seam.make_request(
            "POST",
            "/locks/unlock_door",
            json={"device_id": device_id},
        )

        return self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )
