from seamapi.types import (
    AbstractDevices,
    AbstractUnmanagedDevices,
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    UnmanagedDevice,
    AbstractSeam as Seam,
    DeviceType,
)
from typing import Any, List, Union, Optional, Dict
from seamapi.utils.parse_list_device_params import parse_list_device_params
from seamapi.utils.convert_to_id import (
    to_device_id,
)
from seamapi.utils.report_error import report_error


class Devices(AbstractDevices):
    """
    A class used to retrieve device data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(connected_account=None, connected_accounts=None, connect_webview=None, device_type=None, device_ids=None, manufacturer=None)
        Gets a list of devices
    get(device=None, name=None)
        Gets a device
    update(device, name=None, properties=None, location=None)
        Updates a device
    list_device_providers(provider_category=None):
        Gets a list of device providers
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
        self.unmanaged = UnmanagedDevices(seam)

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
        """Gets a list of devices.

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
        device_ids : Optional[List[Union[DeviceId, Device]]]
            Device IDs to filter devices by
        manufacturer : Optional[str]
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
            "/devices/list",
            params=params,
        )
        devices = res["devices"]

        return [Device.from_dict(d) for d in devices]

    @report_error
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
        res = self.seam.make_request("GET", "/devices/get", params=params)
        json_device = res["device"]
        return Device.from_dict(json_device)

    @report_error
    def update(
        self,
        device: Union[DeviceId, Device],
        name: Optional[str] = None,
        properties: Optional[dict] = None,
        location: Optional[dict] = None,
        is_managed: Optional[bool] = None,
    ) -> bool:
        """Updates a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        name : str, optional
            New device name
        properties : dict, optional
            New device properties
        location : str, optional
            New device location
        is_managed : bool, optional
            The managed state of the device

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
        if name:
            update_payload["name"] = name
        if properties:
            update_payload["properties"] = properties
        if location:
            update_payload["location"] = location
        if is_managed is not None:
            update_payload["is_managed"] = is_managed

        self.seam.make_request(
            "POST",
            "/devices/update",
            json=update_payload,
        )

        return True

    @report_error
    def delete(self, device: Union[DeviceId, Device]) -> bool:
        """Deletes a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to delete

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

        delete_payload = {"device_id": to_device_id(device)}
        self.seam.make_request(
            "DELETE",
            "/devices/delete",
            json=delete_payload,
        )

        return True

    @report_error
    def list_device_providers(
        self, provider_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of device providers

        Parameters
        ----------
        provider_category : Optional[str]
            Provider category to filter by eg. stable

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            List of device providers
        """
        params = {}

        if provider_category:
            params["provider_category"] = provider_category

        res = self.seam.make_request(
            "GET",
            "/devices/list_device_providers",
            params=params,
        )

        return res["device_providers"]


class UnmanagedDevices(AbstractUnmanagedDevices):
    """
    A class used to retrieve unmanaged device data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    get(device=None, name=None)
        Gets an unmanaged device
    list(connected_account=None, connected_accounts=None, connect_webview=None, device_type=None, device_ids=None, manufacturer=None)
        Gets a list of unmanaged devices
    update(device, is_managed)
        Updates an unmanaged device
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
    def get(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
    ) -> UnmanagedDevice:
        """Gets an unmanaged devices.

        Parameters
        ----------
        device : Union[DeviceId, Device], optional
            Device ID or Device
        name : str, optional
            Device name

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An unmanaged device.
        """

        params = {}

        if device:
            params["device_id"] = to_device_id(device)
        if name:
            params["name"] = name

        res = self.seam.make_request(
            "GET",
            "/devices/unmanaged/get",
            params=params,
        )
        json_device = res["device"]

        return UnmanagedDevice.from_dict(json_device)

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
    ) -> List[UnmanagedDevice]:
        """Gets a list of unmanaged devices.

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
            A list of unmanaged devices.
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
            "/devices/unmanaged/list",
            params=params,
        )
        devices = res["devices"]

        return [UnmanagedDevice.from_dict(d) for d in devices]

    @report_error
    def update(
        self,
        device: Union[DeviceId, UnmanagedDevice],
        is_managed: bool,
    ) -> bool:
        """Updates a device transitioning it from an unmanaged state to a managed one.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        is_managed : bool
            The managed state of the device

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

        self.seam.make_request(
            "POST",
            "/devices/unmanaged/update",
            json={
                "device_id": to_device_id(device),
                "is_managed": is_managed,
            },
        )

        return True
