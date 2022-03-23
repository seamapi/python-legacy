from seamapi.types import (
    AbstractLocks,
    ActionAttempt,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
import time
from typing import List, Union, Optional, cast
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class Locks(AbstractLocks):
    """
    A class used to retreive lock data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
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
        seam : dict
          Intial seam class
        """

        self.seam = seam

    def list(
        self,
        connected_account: Optional[str] = None,
        connect_webview: Optional[str] = None,
    ) -> List[Device]:
        """Gets a list of locks.

        Parameters
        ----------
        connected_account : str, optional
            Connected account id
        connect_webview : str, optional
            Connect webview id

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
            params["connected_account_id"] = connected_account
        if connect_webview:
            params["connect_webview_id"] = connect_webview

        res = requests.post(
            f"{self.seam.api_url}/locks/list",
            params=params,
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
        device : str or dict, optional
            Device id or device dict
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
        res = requests.post(
            f"{self.seam.api_url}/locks/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params=params,
        )
        if not res.ok:
            raise Exception(res.text)
        json_lock = res.json()["device"]
        return Device.from_dict(json_lock)

    def lock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        """Locks a lock.

        Parameters
        ----------
        device : str or dict
            Device id or device dict

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An action attempt dict.
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
        device : str or dict
            Device id or device dict

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An action attempt dict.
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
