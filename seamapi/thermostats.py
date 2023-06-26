from seamapi.types import (
    AbstractThermostats,
    ActionAttempt,
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
from typing import List, Union, Optional
from seamapi.utils.convert_to_id import (
    to_connect_webview_id,
    to_connected_account_id,
    to_device_id,
)
from seamapi.utils.report_error import report_error
from .climate_setting_schedules import ClimateSettingSchedules


class Thermostats(AbstractThermostats):
    """
    A class used to interact with Thermostats

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(connected_account=None, connect_webview=None, device_type=None, device_ids=None)
        Gets a list of devices
    get(device=None, name=None)
        Gets a device
    update(device, name=None, properties=None, location=None)
        Updates a device
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
        self.climate_setting_schedules = ClimateSettingSchedules(
            seam=self.seam
        )

    @report_error
    def list(
        self,
        connected_account: Union[ConnectedAccountId, ConnectedAccount] = None,
        connect_webview: Union[ConnectWebviewId, ConnectWebview] = None,
        device_ids: Optional[list] = None,
    ) -> List[Device]:
        """Gets a list of Thermostats.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount, optional
            Connected account id or ConnectedAccount to get thermostats associated with
        connect_webview : ConnectWebviewId or ConnectWebview, optional
            Connect webview id or ConnectWebview to get thermostats associated with
        device_ids : Optional[list]
            Device IDs to filter thermostats by

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
            params["connect_webview_id"] = to_connect_webview_id(
                connect_webview
            )
        if device_ids is not None:
            params["device_ids"] = [to_device_id(d) for d in device_ids]

        res = self.seam.make_request(
            "GET",
            "/thermostats/list",
            params=params,
        )
        thermostats = res["thermostats"]

        return [Device.from_dict(d) for d in thermostats]

    @report_error
    def get(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
    ) -> Device:
        """Gets a Thermostat.

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

        res = self.seam.make_request("GET", "/thermostats/get", params=params)
        json_thermostat = res["thermostat"]
        return Device.from_dict(json_thermostat)

    @report_error
    def update(
        self,
        device: Union[DeviceId, Device],
        default_climate_setting: dict,
    ) -> bool:
        """Updates a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        name : str, optional
            New device name
        default_climate_setting : dict, optional
            New thermostat settings

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Boolean
        """

        if not device:
            raise Exception("device is required")

        update_payload = {
            "device_id": to_device_id(device),
        }

        update_payload["default_climate_setting"] = default_climate_setting

        self.seam.make_request(
            "POST",
            "/thermostats/update",
            json=update_payload,
        )

        return True
