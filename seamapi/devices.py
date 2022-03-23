from seamapi.types import AbstractDevices, Device, DeviceId, AbstractSeam as Seam
from typing import List, Union, Optional
import requests


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class Devices(AbstractDevices):
    """
    A class used to retreive device data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
        Initial seam class

    Methods
    -------
    list(connected_account=None, connect_webview=None, device_type=None)
        Gets a list of devices
    get(device=None, name=None)
        Gets a device
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
        device_type: Optional[str] = None,
    ) -> List[Device]:
        """Gets a list of devices.

        Parameters
        ----------
        connected_account : str, optional
            Connected account id
        connect_webview : str, optional
            Connect webview id
        device_type : str, optional
            A device type e.g. august_lock

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of devices.
        """

        params = {}
        if connected_account:
            params["connected_account_id"] = connected_account
        if connect_webview:
            params["connect_webview_id"] = connect_webview
        if device_type:
            params["device_type"] = device_type
        res = requests.get(
            f"{self.seam.api_url}/devices/list",
            params=params,
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        devices = res.json()["devices"]
        return [Device.from_dict(d) for d in devices]

    def get(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
    ) -> Device:
        """Gets a device.

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
            A device dict.
        """

        params = {}
        if device:
            params["device_id"] = to_device_id(device)
        if name:
            params["name"] = name
        res = requests.get(
            f"{self.seam.api_url}/devices/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params=params,
        )
        if not res.ok:
            raise Exception(res.text)
        json_device = res.json()["device"]
        return Device.from_dict(json_device)
