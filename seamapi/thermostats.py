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
    DeviceType,
)
from typing import List, Union, Optional
from seamapi.utils.parse_list_device_params import parse_list_device_params
from seamapi.utils.convert_to_id import (
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
        Gets a list of devices.

    get(device=None, name=None)
        Gets a device.

    update(device, name=None, properties=None, location=None)
        Updates a device.

    cool(device, cooling_set_point_celsius=None, cooling_set_point_fahrenheit=None, wait_for_action_attempt=True)
        Sets the the thermostat mode to cool with the provided set point.

    heat(device, cooling_set_point_celsius=None, cooling_set_point_fahrenheit=None, wait_for_action_attempt=True)
        Sets the the thermostat mode to heat with the provided set point.

    heat_cool(device, heating_set_point_celsius=None, heating_set_point_fahrenheit=None, cooling_set_point_celsius=None, cooling_set_point_fahrenheit=None, wait_for_action_attempt=True)
        Sets the thermostat mode to heat_cool with the provided set points.

    off(device, wait_for_action_attempt=True)
        Sets the the thermostat mode to off.

    set_fan_mode(device, fan_mode, wait_for_action_attempt=True)
        Sets the fan mode on the device.
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
        connected_accounts: List[
            Union[ConnectedAccountId, ConnectedAccount]
        ] = None,
        connect_webview: Union[ConnectWebviewId, ConnectWebview] = None,
        device_type: Optional[DeviceType] = None,
        device_types: Optional[List[DeviceType]] = None,
        device_ids: Optional[List[Union[DeviceId, Device]]] = None,
        manufacturer: Optional[str] = None,
        limit: Optional[float] = None,
        created_before: Optional[str] = None,
    ) -> List[Device]:
        """Gets a list of Thermostats.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount, optional
            Connected account id or ConnectedAccount to get devices associated with
        connected_accounts : ConnectedAccountId(s) or ConnectedAccount(s), optional
            Connected account ids or ConnectedAccount(s) to get devices associated with
        connect_webview : ConnectWebviewId or ConnectWebview, optional
            Connect webview id or ConnectWebview to get devices associated with
        device_type : DeviceType, optional
            Device type e.g. august_lock
        device_types : List[DeviceType], optional
            List of device types e.g. august_lock
        device_ids : List[Union[DeviceId, Device]], optional
            Device IDs to filter devices by
        manufacturer : str, optional
            Manufacturer name to filter devices by e.g. august, schlage
        limit : str, optional
            Limit the number of devices returned
        created_before : str, optional
            If specified, only devices created before this date will be returned

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of devices.
        """

        params = parse_list_device_params(
            connected_account,
            connected_accounts,
            connect_webview,
            device_type,
            device_types,
            device_ids,
            manufacturer,
            limit,
            created_before,
        )

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

    @report_error
    def cool(
        self,
        device: Union[DeviceId, Device],
        cooling_set_point_celsius: Optional[float] = None,
        cooling_set_point_fahrenheit: Optional[float] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        """Sets the the thermostat mode to cool with the provided set point.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        cooling_set_point_celsius : float, optional
            Cooling set point in celsius
        cooling_set_point_fahrenheit : float, optional
            Cooling set point in fahrenheit
        wait_for_action_attempt: bool, optional
            Should wait for action attempt to resolve

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        if not device:
            raise Exception("device is required")

        params = {
            "device_id": to_device_id(device),
        }

        arguments = {
            "cooling_set_point_celsius": cooling_set_point_celsius,
            "cooling_set_point_fahrenheit": cooling_set_point_fahrenheit,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "POST",
            "/thermostats/cool",
            json=params,
        )
        action_attempt = res["action_attempt"]

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(action_attempt)

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            action_attempt["action_attempt_id"]
        )

        return updated_action_attempt

    @report_error
    def heat(
        self,
        device: Union[DeviceId, Device],
        heating_set_point_celsius: Optional[float] = None,
        heating_set_point_fahrenheit: Optional[float] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        """Sets the the thermostat mode to heat with the provided set point.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        heating_set_point_celsius : float, optional
            Heating set point in celsius
        heating_set_point_fahrenheit : float, optional
            Heating set point in fahrenheit
        wait_for_action_attempt: bool, optional
            Should wait for action attempt to resolve

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        if not device:
            raise Exception("device is required")

        params = {
            "device_id": to_device_id(device),
        }

        arguments = {
            "heating_set_point_celsius": heating_set_point_celsius,
            "heating_set_point_fahrenheit": heating_set_point_fahrenheit,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "POST",
            "/thermostats/heat",
            json=params,
        )
        action_attempt = res["action_attempt"]

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(action_attempt)

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            action_attempt["action_attempt_id"]
        )

        return updated_action_attempt

    @report_error
    def heat_cool(
        self,
        device: Union[DeviceId, Device],
        cooling_set_point_fahrenheit: Optional[float] = None,
        cooling_set_point_celsius: Optional[float] = None,
        heating_set_point_fahrenheit: Optional[float] = None,
        heating_set_point_celsius: Optional[float] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        """Sets the thermostat mode to heat_cool with the provided set points.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        cooling_set_point_celsius : float, optional
            Cooling set point in celsius
        cooling_set_point_fahrenheit : float, optional
            Cooling set point in fahrenheit
        heating_set_point_celsius : float, optional
            Heating set point in celsius
        heating_set_point_fahrenheit : float, optional
            Heating set point in fahrenheit
        wait_for_action_attempt: bool, optional
            Should wait for action attempt to resolve

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        if not device:
            raise Exception("device is required")

        params = {
            "device_id": to_device_id(device),
        }

        arguments = {
            "cooling_set_point_celsius": cooling_set_point_celsius,
            "cooling_set_point_fahrenheit": cooling_set_point_fahrenheit,
            "heating_set_point_celsius": heating_set_point_celsius,
            "heating_set_point_fahrenheit": heating_set_point_fahrenheit,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "POST",
            "/thermostats/heat_cool",
            json=params,
        )
        action_attempt = res["action_attempt"]

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(action_attempt)

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            action_attempt["action_attempt_id"]
        )

        return updated_action_attempt

    @report_error
    def off(
        self,
        device: Union[DeviceId, Device],
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        """Sets the thermostat mode to heat_cool with the provided set points.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        wait_for_action_attempt: bool, optional
            Should wait for action attempt to resolve

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        if not device:
            raise Exception("device is required")

        res = self.seam.make_request(
            "POST",
            "/thermostats/off",
            json={
                "device_id": to_device_id(device),
            },
        )
        action_attempt = res["action_attempt"]

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(action_attempt)

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            action_attempt["action_attempt_id"]
        )

        return updated_action_attempt

    @report_error
    def set_fan_mode(
        self,
        device: Union[DeviceId, Device],
        fan_mode: str,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        """Sets the thermostat mode to heat_cool with the provided set points.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        fan_mode : str
            Fan mode of the thermostat: "auto" or "on"
        wait_for_action_attempt: bool, optional
            Should wait for action attempt to resolve

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        if not device:
            raise Exception("device is required")
        if not fan_mode:
            raise Exception("fan_mode is required")

        res = self.seam.make_request(
            "POST",
            "/thermostats/set_fan_mode",
            json={
                "device_id": to_device_id(device),
                "fan_mode": fan_mode
            },
        )
        action_attempt = res["action_attempt"]

        if not wait_for_action_attempt:
            return ActionAttempt.from_dict(action_attempt)

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            action_attempt["action_attempt_id"]
        )

        return updated_action_attempt
