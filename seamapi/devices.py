from seamapi.types import (
    AbstractDevices,
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    AbstractSeam as Seam,
    DeviceType,
)
from typing import List, Union, Optional
import requests
from seamapi.utils.convert_to_id import (
    to_connect_webview_id,
    to_connected_account_id,
    to_device_id,
)


class Devices(AbstractDevices):
    """
    A class used to retreive device data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
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
        seam : Seam
          Intial seam class
        """

        self.seam = seam

    def list(
        self,
        connected_account: Union[ConnectedAccountId, ConnectedAccount] = None,
        connect_webview: Union[ConnectWebviewId, ConnectWebview] = None,
        device_type: Optional[DeviceType] = None,
    ) -> List[Device]:
        """Gets a list of devices.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount, optional
            Connected account id or ConnectedAccount to get devices associated with
        connect_webview : ConnectWebviewId or ConnectWebview, optional
            Connect webview id or ConnectWebview to get devices associated with
        device_type : DeviceType, optional
            Device type e.g. august_lock

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
            params["connected_account_id"] = to_connected_account_id(
                connected_account
            )
        if connect_webview:
            params[
                "connect_webview_id"
            ] =  to_connect_webview_id(connect_webview)
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
        device : DeviceId or Device, optional
            Device id or Device to get the state of
        name : str, optional
            Device name

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Device
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
