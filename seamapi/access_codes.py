from seamapi.types import (
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


def to_access_code_id(access_code: Union[AccessCodeId, AccessCode]) -> str:
    if isinstance(access_code, str):
        return access_code
    return access_code.access_code_id


def to_device_id(device: Union[DeviceId, Device]) -> str:
    if isinstance(device, str):
        return device
    return device.device_id


class AccessCodes(AbstractAccessCodes):
    """
    A class used to retreive access code data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
        Initial seam class

    Methods
    -------
    list(device)
        Gets a list of access codes for a device
    get(access_code)
        Gets a certain access code of a device
    create(device, name, code=None, starts_at=None, ends_at=None)
        Creates an access code on a device
    delete(access_code)
        Deletes an access code on a device
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

    def list(self, device: Union[DeviceId, Device]) -> List[AccessCode]:
        """Gets a list of access codes for a device.

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
            A list of access codes for a device.
        """

        device_id = to_device_id(device)
        res = requests.get(
            f"{self.seam.api_url}/access_codes/list?device_id={device_id}",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)
        access_codes = res.json()["access_codes"]
        return [AccessCode.from_dict(ac) for ac in access_codes]

    def get(self, access_code: Union[AccessCodeId, AccessCode]) -> AccessCode:
        """Gets a certain access code of a device.

        Parameters
        ----------
        access_code : str or dict
            Access code id or access code dict

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An access code dict.
        """

        access_code_id = to_access_code_id(access_code)
        res = requests.get(
            f"{self.seam.api_url}/access_codes/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"access_code_id": access_code_id},
        )
        if not res.ok:
            raise Exception(res.text)
        return AccessCode.from_dict(res.json()["access_code"])

    def create(
        self,
        device: Union[DeviceId, Device],
        name: str,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
    ) -> AccessCode:
        """Creates an access code on a device.

        Parameters
        ----------
        device : str or dict
            Device id or device dict
        name : str
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
            An access code dict.
        """

        device_id = to_device_id(device)
        create_payload = {"device_id": device_id, "name": name}
        if code is not None:
            create_payload["code"] = code
        if starts_at is not None:
            create_payload["starts_at"] = starts_at
        if ends_at is not None:
            create_payload["ends_at"] = ends_at
        res = requests.post(
            f"{self.seam.api_url}/access_codes/create",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json=create_payload,
        )
        if not res.ok:
            raise Exception(res.text)
        action_attempt = self.seam.action_attempts.poll_until_ready(
            res.json()["action_attempt"]["action_attempt_id"]
        )
        success_res: Any = action_attempt.result
        return AccessCode.from_dict(success_res["access_code"])

    def delete(self, access_code: Union[AccessCodeId, AccessCode]) -> ActionAttempt:
        """Deletes an access code on a device.

        Parameters
        ----------
        access_code : str or dict
            Access code id or access code dict

        Raises
        ------
        Exception
            If the API request wasn't successful.
        Exception
            If action attempt failed.

        Returns
        ------
            An access code dict.
        """

        access_code_id = to_access_code_id(access_code)
        res = requests.delete(
            (f"{self.seam.api_url}/access_codes/delete"),
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            json={"access_code_id": access_code_id},
        )
        if not res.ok:
            raise Exception(res.text)
        action_attempt = self.seam.action_attempts.poll_until_ready(
            res.json()["action_attempt"]["action_attempt_id"]
        )
        if action_attempt.status == "error" and action_attempt.error:
            raise Exception(
                f"{action_attempt.error.type}: {action_attempt.error.message}"
            )
        return action_attempt
