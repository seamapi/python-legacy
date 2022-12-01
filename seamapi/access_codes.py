import time
from datetime import datetime, timezone, timedelta
from seamapi.types import (
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
    A class used to retreive access code data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(device)
        Gets a list of access codes for a device
    get(access_code=None, device=None)
        Gets a certain access code of a device
    create(device, name=None, code=None, starts_at=None, ends_at=None)
        Creates an access code on a device
    delete(access_code, device=None)
        Deletes an access code on a device
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
    def list(self, device: Union[DeviceId, Device]) -> List[AccessCode]:
        """Gets a list of access codes for a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to list access codes for

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of access codes for a device.
        """

        device_id = to_device_id(device)
        res = self.seam.make_request(
            "GET",
            "/access_codes/list",
            params={"device_id": device_id},
        )
        access_codes = res["access_codes"]

        return [AccessCode.from_dict(ac) for ac in access_codes]

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
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        common_code_key: Optional[str] = None,
        attempt_for_offline_device: Optional[bool] = True,
        wait_for_code: Optional[bool] = False,
        timeout: Optional[int] = 300,
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
        if attempt_for_offline_device is not None:
            create_payload["attempt_for_offline_device"] = attempt_for_offline_device

        if (wait_for_code
            and starts_at is not None
            and datetime.fromisoformat(starts_at) > datetime.now() + timedelta(seconds=5)
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
            while (access_code.code is None):
                if (access_code.status == "unknown"):
                    raise WaitForAccessCodeFailedException(
                        "Access code status returned unknown",
                        access_code_id=access_code.access_code_id
                    )
                if (len(access_code.errors) > 0):
                    raise WaitForAccessCodeFailedException(
                        "Access code returned errors",
                        access_code_id=access_code.access_code_id,
                        errors=access_code.errors
                    )
                time.sleep(poll_interval)
                duration += poll_interval
                if (duration > timeout):
                    raise WaitForAccessCodeFailedException(
                        f"Gave up after waiting the maximum timeout of {timeout} seconds",
                        access_code_id=access_code.access_code_id,
                        errors=access_code.errors
                    )

                access_code = access_codes.get(access_code)

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
