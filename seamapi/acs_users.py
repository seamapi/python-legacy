from seamapi.types import AbstractUsersAcs, AbstractSeam as Seam
from typing import Optional, Any


class UsersAcs(AbstractUsersAcs):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def create(
        self,
        acs_system_id: Any,
        acs_access_group_ids: Optional[Any] = None,
        user_identity_id: Optional[Any] = None,
        access_schedule: Optional[Any] = None,
        full_name: Optional[Any] = None,
        email: Optional[Any] = None,
        phone_number: Optional[Any] = None,
        email_address: Optional[Any] = None,
    ):
        json_payload = {}

        if acs_system_id is not None:
            json_payload["acs_system_id"] = acs_system_id
        if acs_access_group_ids is not None:
            json_payload["acs_access_group_ids"] = acs_access_group_ids
        if user_identity_id is not None:
            json_payload["user_identity_id"] = user_identity_id
        if access_schedule is not None:
            json_payload["access_schedule"] = access_schedule
        if full_name is not None:
            json_payload["full_name"] = full_name
        if email is not None:
            json_payload["email"] = email
        if phone_number is not None:
            json_payload["phone_number"] = phone_number
        if email_address is not None:
            json_payload["email_address"] = email_address

        self.seam.make_request("POST", "/acs/users/create", json=json_payload)

        return None

    def delete(self, acs_user_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request("POST", "/acs/users/delete", json=json_payload)

        return None

    def get(self, acs_user_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request("POST", "/acs/users/get", json=json_payload)

        return None

    def list(
        self,
        user_identity_id: Optional[Any] = None,
        user_identity_phone_number: Optional[Any] = None,
        user_identity_email_address: Optional[Any] = None,
        acs_system_id: Optional[Any] = None,
    ):
        json_payload = {}

        if user_identity_id is not None:
            json_payload["user_identity_id"] = user_identity_id
        if user_identity_phone_number is not None:
            json_payload["user_identity_phone_number"] = user_identity_phone_number
        if user_identity_email_address is not None:
            json_payload["user_identity_email_address"] = user_identity_email_address
        if acs_system_id is not None:
            json_payload["acs_system_id"] = acs_system_id

        self.seam.make_request("POST", "/acs/users/list", json=json_payload)

        return None

    def list_accessible_entrances(self, acs_user_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request(
            "POST", "/acs/users/list_accessible_entrances", json=json_payload
        )

        return None

    def suspend(self, acs_user_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request("POST", "/acs/users/suspend", json=json_payload)

        return None

    def unsuspend(self, acs_user_id: Any):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id

        self.seam.make_request("POST", "/acs/users/unsuspend", json=json_payload)

        return None

    def update(
        self,
        acs_user_id: Any,
        access_schedule: Optional[Any] = None,
        full_name: Optional[Any] = None,
        email: Optional[Any] = None,
        phone_number: Optional[Any] = None,
        email_address: Optional[Any] = None,
        hid_acs_system_id: Optional[Any] = None,
    ):
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if access_schedule is not None:
            json_payload["access_schedule"] = access_schedule
        if full_name is not None:
            json_payload["full_name"] = full_name
        if email is not None:
            json_payload["email"] = email
        if phone_number is not None:
            json_payload["phone_number"] = phone_number
        if email_address is not None:
            json_payload["email_address"] = email_address
        if hid_acs_system_id is not None:
            json_payload["hid_acs_system_id"] = hid_acs_system_id

        self.seam.make_request("POST", "/acs/users/update", json=json_payload)

        return None
