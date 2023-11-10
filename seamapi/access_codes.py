import time
from datetime import datetime, timezone, timedelta
from seamapi.types import (
    AbstractUnmanagedAccessCodes,
    UnmanagedAccessCode,
    WaitForAccessCodeFailedException,
    AbstractAccessCodes,
    AccessCode,
    AccessCodeId,
    ActionAttempt,
    Device,
    DeviceId,
    AbstractSeam as Seam,
)
from typing import List, Optional, Union, Any
import requests
from seamapi.utils.convert_to_id import to_access_code_id, to_device_id
from seamapi.utils.report_error import report_error


class AccessCodes(AbstractAccessCodes):
    """
    A class used to retrieve access code data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(device, access_codes=None)
        Gets a list of access codes for a device
    get(access_code=None, device=None)
        Gets a certain access code of a device
    create(device, name=None, code=None, starts_at=None, ends_at=None, attempt_for_offline_device=None, wait_for_code=None, timeout=None, allow_external_modification=None, prefer_native_scheduling=None, use_backup_access_code_pool=None)
        Creates an access code on a device
    create_multiple(devices, name=None, code=None, starts_at=None, ends_at=None)
        Creates multiple access codes across devices
    update(access_code, device=None, name=None, code=None, starts_at=None, ends_at=None, type=None, allow_external_modification=None)
        Updates an access code on a device
    delete(access_code, device=None)
        Deletes an access code on a device
    pull_backup_access_code(access_code)
        Pulls a backup access code.
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
        self.unmanaged = UnmanagedAccessCodes(seam)

    @report_error
    def list(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        access_codes: Optional[Union[List[AccessCode], List[AccessCodeId]]] = None,
    ) -> List[AccessCode]:
        """Gets a list of access codes for a device.

        Parameters
        ----------
        device : Union[DeviceId, Device], optional
            Device id or Device to list access codes for
        access_codes : Union[List[AccessCode], List[AccessCodeId]], optional
            Access Code IDs or Access Codes to filter access_codes by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of access codes for a device.
        """

        params = {}
        if device:
            params["device_id"] = to_device_id(device)
        if access_codes:
            params["access_code_ids"] = [to_access_code_id(ac) for ac in access_codes]

        res = self.seam.make_request(
            "GET",
            "/access_codes/list",
            params=params,
        )
        res_access_codes = res["access_codes"]

        return [AccessCode.from_dict(ac) for ac in res_access_codes]

    @report_error
    def get(
        self,
        access_code: Optional[Union[AccessCodeId, AccessCode]] = None,
        device: Optional[Union[DeviceId, AccessCode]] = None,
    ) -> AccessCode:
        """Gets a certain access code for a device.

        Parameters
        ----------
        access_code : AccessCodeId or AccessCode, optional
            Access code id or AccessCode to get latest version of
        device : DeviceId or Device, optional
            Device id or Device to get an access code for

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            AccessCode
        """

        params = {}
        if access_code:
            params["access_code_id"] = to_access_code_id(access_code)
        if device:
            params["device_id"] = to_device_id(device)

        res = self.seam.make_request(
            "GET",
            "/access_codes/get",
            params=params,
        )

        return AccessCode.from_dict(res["access_code"])

    @report_error
    def create(
        self,
        device: Union[DeviceId, Device],
        name: Optional[str] = None,
        code: Optional[str] = None,
        type: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        common_code_key: Optional[str] = None,
        attempt_for_offline_device: Optional[bool] = True,
        wait_for_code: Optional[bool] = False,
        timeout: Optional[int] = 300,
        allow_external_modification: Optional[bool] = None,
        prefer_native_scheduling: Optional[bool] = None,
        use_backup_access_code_pool: Optional[bool] = None,
        use_offline_access_code: Optional[bool] = None,
        is_offline_access_code: Optional[bool] = None,
        is_one_time_use: Optional[bool] = None,
        max_time_rounding: Optional[str] = None,
    ) -> AccessCode:
        """Creates an access code on a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to create an access code for
        name : str, optional
            Access code name
        code : str, optional
            Access code value
        type : str, optional
            Access code type eg. ongoing or time_bound
        starts_at : str, optional
            Time when access code becomes effective
        ends_at : str, optional
            Time when access code ceases to be effective
        attempt_for_offline_device : bool, optional
            If the device status is offline,
            attempt to set the access code anyway.
        wait_for_code : bool, optional
            Poll the access code until the code is known.
        timeout : int, optional:
            Maximum polling time in seconds.
        allow_external_modification : bool, optional:
            Allow external modifications of the access code e.g. through the lock provider's app. False by default.
        prefer_native_scheduling : bool, optional:
            Where possible, prefer lock provider's native access code scheduling. True by default.
        use_backup_access_code_pool : bool, optional:
            Activate backup access code pool. False by default.
        use_offline_access_code : bool, optional:
            Use offline access code. False by default.
        is_offline_access_code : bool, optional:
            Is offline access code. False by default.
        is_one_time_use : bool, optional:
            Is one time use. For offline access codes only. False by default.
        max_time_rounding : str, optional:
            Accepts 1day, 1d, 1hour and 1h. For offline access codes only. "1hour" by default.

        Raises
        ------
        Exception
            If the API request wasn't successful.
        WaitForAccessCodeFailedException
            If waiting for code aborts due to error or timeout.

        Returns
        ------
            AccessCode
        """

        device_id = to_device_id(device)
        create_payload = {"device_id": device_id}
        if name is not None:
            create_payload["name"] = name
        if code is not None:
            create_payload["code"] = code
        if starts_at is not None:
            create_payload["starts_at"] = starts_at
        if ends_at is not None:
            create_payload["ends_at"] = ends_at
        if common_code_key is not None:
            create_payload["common_code_key"] = common_code_key
        if type is not None:
            create_payload["type"] = type
        if attempt_for_offline_device is not None:
            create_payload["attempt_for_offline_device"] = attempt_for_offline_device
        if allow_external_modification is not None:
            create_payload["allow_external_modification"] = allow_external_modification
        if prefer_native_scheduling is not None:
            create_payload["prefer_native_scheduling"] = prefer_native_scheduling
        if use_backup_access_code_pool is not None:
            create_payload["use_backup_access_code_pool"] = use_backup_access_code_pool
        if use_offline_access_code is not None:
            create_payload["use_offline_access_code"] = use_offline_access_code
        if is_offline_access_code is not None:
            create_payload["is_offline_access_code"] = is_offline_access_code
        if is_one_time_use is not None:
            create_payload["is_one_time_use"] = is_one_time_use
        if max_time_rounding is not None:
            create_payload["max_time_rounding"] = max_time_rounding

        if (
            wait_for_code
            and not is_offline_access_code
            and starts_at is not None
            and datetime.fromisoformat(starts_at)
            > datetime.now() + timedelta(seconds=5)
        ):
            raise RuntimeError("Cannot use wait_for_code with a future time bound code")

        res = self.seam.make_request(
            "POST",
            "/access_codes/create",
            json=create_payload,
        )

        access_code = AccessCode.from_dict(res["access_code"])

        duration = 0
        poll_interval = 0.25
        if wait_for_code:
            while access_code.code is None:
                if access_code.status == "unknown":
                    raise WaitForAccessCodeFailedException(
                        "Access code status returned unknown",
                        access_code_id=access_code.access_code_id,
                    )
                if len(access_code.errors) > 0:
                    raise WaitForAccessCodeFailedException(
                        "Access code returned errors",
                        access_code_id=access_code.access_code_id,
                        errors=access_code.errors,
                    )
                time.sleep(poll_interval)
                duration += poll_interval
                if duration > timeout:
                    raise WaitForAccessCodeFailedException(
                        f"Gave up after waiting the maximum timeout of {timeout} seconds",
                        access_code_id=access_code.access_code_id,
                        errors=access_code.errors,
                    )

                access_code = self.seam.access_codes.get(access_code)

        return access_code

    @report_error
    def create_multiple(
        self,
        devices: Union[List[DeviceId], List[Device]],
        name: Optional[str] = None,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
    ) -> List[AccessCode]:
        """Creates multiple access codes across multiple devices. All access
        codes will have the same code (if possible).

        Parameters
        ----------
        devices : List of DeviceIds or Devices
            Device ids or Devices to create an access code for
        name : str, optional
            Access code name
        code : str, optional
            Access code value
        starts_at : str, optional
            Time when access code becomes effective
        ends_at : str, optional
            Time when access code ceases to be effective

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            AccessCode
        """

        device_ids: List[str] = []
        for device in devices:
            device_ids.append(to_device_id(device))

        create_payload: dict[str, Any] = {"device_ids": device_ids}
        if name is not None:
            create_payload["name"] = name
        if code is not None:
            create_payload["code"] = code
        if starts_at is not None:
            create_payload["starts_at"] = starts_at
        if ends_at is not None:
            create_payload["ends_at"] = ends_at

        res = self.seam.make_request(
            "POST",
            "/access_codes/create_multiple",
            json=create_payload,
        )

        access_codes: List[AccessCode] = []
        for access_code in res["access_codes"]:
            access_codes.append(AccessCode.from_dict(access_code))

        return access_codes

    @report_error
    def update(
        self,
        access_code: Union[AccessCodeId, AccessCode],
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        type: Optional[str] = None,
        allow_external_modification: Optional[bool] = None,
    ) -> AccessCode:
        """Updates an access code on a device.

        Parameters
        ----------
        access_code: AccessCodeId or AccessCode
            Access code id or Access code to update
        device : DeviceId or Device
            New device to move access code to
        name : str, optional
            Access code name
        code : str, optional
            Access code value
        starts_at : str, optional
            Time when access code becomes effective
        ends_at : str, optional
            Time when access code ceases to be effective
        type : str, optional
            Access code type eg. ongoing or time_bound
        allow_external_modification : bool, optional:
            Allow external modifications of the access code e.g. through the lock provider's app. False by default.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            AccessCode
        """

        access_code_id = to_access_code_id(access_code)
        update_payload = {"access_code_id": access_code_id}
        if device is not None:
            update_payload["device_id"] = to_device_id(device)
        if name is not None:
            update_payload["name"] = name
        if code is not None:
            update_payload["code"] = code
        if starts_at is not None:
            update_payload["starts_at"] = starts_at
        if ends_at is not None:
            update_payload["ends_at"] = ends_at
        if type is not None:
            update_payload["type"] = type
        if allow_external_modification is not None:
            update_payload["allow_external_modification"] = allow_external_modification

        res = self.seam.make_request(
            "POST",
            "/access_codes/update",
            json=update_payload,
        )

        action_attempt = self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )
        success_res: Any = action_attempt.result

        return AccessCode.from_dict(success_res["access_code"])

    @report_error
    def delete(
        self,
        access_code: Union[AccessCodeId, AccessCode],
        device: Optional[Union[DeviceId, AccessCode]] = None,
    ) -> ActionAttempt:
        """Deletes an access code on a device.

        Parameters
        ----------
        access_code : AccessCodeId or AccessCode
            Access code id or AccessCode to delete it
        device : DeviceId or Device, optional
            Device id or Device to delete an access code on

        Raises
        ------
        Exception
            If the API request wasn't successful.
        Exception
            If action attempt failed.

        Returns
        ------
            ActionAttempt
        """

        access_code_id = to_access_code_id(access_code)
        create_payload = {"access_code_id": access_code_id}
        if device is not None:
            create_payload["device_id"] = to_device_id(device)

        res = self.seam.make_request(
            "DELETE",
            "/access_codes/delete",
            json=create_payload,
        )

        action_attempt = self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )

        return action_attempt

    @report_error
    def pull_backup_access_code(
        self,
        access_code: Union[AccessCode, AccessCodeId],
    ) -> AccessCode:
        """Pulls a backup access code.

        Parameters
        ----------
        access_code : Union[AccessCode, AccessCodeId]
            Access code ID or AccessCode

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            AccessCode
        """

        res = self.seam.make_request(
            "POST",
            "/access_codes/pull_backup_access_code",
            json={"access_code_id": to_access_code_id(access_code)},
        )

        return AccessCode.from_dict(res["backup_access_code"])


class UnmanagedAccessCodes(AbstractUnmanagedAccessCodes):
    """
    A class used to retrieve unmanaged access code data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    get(device=None, access_code=None, code=None)
        Gets an unmanaged access code
    list(device)
        Gets a list of unmanaged access codes
    convert_to_managed(access_code, allow_external_modification=None)
        Converts an unmanaged access code to a managed one
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
        access_code: Optional[Union[AccessCodeId, AccessCode]] = None,
        device: Optional[Union[DeviceId, Device]] = None,
        code: Optional[str] = None,
    ) -> UnmanagedAccessCode:
        """Gets an unmanaged access code.

        Parameters
        ----------
        access_code : Union[AccessCodeId, UnmanagedAccessCode], optional
            Access Code ID or Access Code
        device : Union[DeviceId, Device], optional
            Device ID or Device
        code : str, optional
            Pin code of an access code

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An unmanaged access code.
        """

        params = {}

        if device:
            params["device_id"] = to_device_id(device)
        if access_code:
            params["access_code_id"] = to_access_code_id(access_code)
        if code:
            params["code"] = code

        res = self.seam.make_request(
            "GET",
            "/access_codes/unmanaged/get",
            params=params,
        )
        json_access_code = res["access_code"]

        return UnmanagedAccessCode.from_dict(json_access_code)

    @report_error
    def list(
        self,
        device: Union[DeviceId, Device],
    ) -> List[UnmanagedAccessCode]:
        """Gets a list of unmanaged access codes.

        Parameters
        ----------
        device : Union[DeviceId, Device], optional
            Device ID or Device

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of unmanaged access codes.
        """

        res = self.seam.make_request(
            "GET",
            "/access_codes/unmanaged/list",
            params={"device_id": to_device_id(device)},
        )
        access_codes = res["access_codes"]

        return [UnmanagedAccessCode.from_dict(ac) for ac in access_codes]

    @report_error
    def convert_to_managed(
        self,
        access_code: Union[AccessCodeId, UnmanagedAccessCode],
        allow_external_modification: Optional[bool] = None,
    ) -> ActionAttempt:
        """Converts an unmanaged access code to a managed one.

        Parameters
        ----------
        access_code : AccessCodeId or UnmanagedAccessCode
            Access Code ID or UnmanagedAccessCode
        allow_external_modification : bool
            Allow external modifications of the access code e.g. through the lock provider's app. False by default.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

        payload = {
            "access_code_id": to_access_code_id(access_code),
        }

        if allow_external_modification is not None:
            payload["allow_external_modification"] = allow_external_modification

        res = self.seam.make_request(
            "POST",
            "/access_codes/unmanaged/convert_to_managed",
            json=payload,
        )

        action_attempt = self.seam.action_attempts.poll_until_ready(
            res["action_attempt"]["action_attempt_id"]
        )

        return action_attempt
