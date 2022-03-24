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

        create_payload = {}
        if connected_account:
            create_payload["connected_account_id"] = to_connected_account_id(
                connected_account
            )
        if connect_webview:
            create_payload["connect_webview_id"] = to_connect_webview_id(
                connect_webview
            )

        res = requests.post(
            f"{self.seam.api_url}/locks/list",
            json=create_payload,
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        json_locks = res.json()["devices"]
        return [Device.from_dict(d) for d in json_locks]

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

        create_payload = {}
        if device:
            create_payload["device_id"] = to_device_id(device)
        if name:
            create_payload["name"] = name
        res = requests.post(
            f"{self.seam.api_url}/locks/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json=create_payload,
        )
        if not res.ok:
            raise Exception(res.text)
        json_lock = res.json()["device"]
        return Device.from_dict(json_lock)

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
        res = requests.post(
            f"{self.seam.api_url}/locks/lock_door",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"device_id": device_id},
        )
        if not res.ok:
            raise Exception(res.text)
        return self.seam.action_attempts.poll_until_ready(
            res.json()["action_attempt"]["action_attempt_id"]
        )

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
        res = requests.post(
            f"{self.seam.api_url}/locks/unlock_door",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"device_id": device_id},
        )
        if not res.ok:
            raise Exception(res.text)
        return self.seam.action_attempts.poll_until_ready(
            res.json()["action_attempt"]["action_attempt_id"]
        )
