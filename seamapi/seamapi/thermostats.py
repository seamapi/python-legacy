from seamapi.types import AbstractThermostats, AbstractSeam as Seam, Device
from typing import Optional, Any


class Thermostats(AbstractThermostats):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def cool(
        self,
        device_id: Optional[Any] = None,
        cooling_set_point_celsius: Optional[Any] = None,
        cooling_set_point_fahrenheit: Optional[Any] = None,
        sync: Optional[Any] = None,
    ):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if cooling_set_point_celsius is not None:
            json_payload["cooling_set_point_celsius"] = cooling_set_point_celsius
        if cooling_set_point_fahrenheit is not None:
            json_payload["cooling_set_point_fahrenheit"] = cooling_set_point_fahrenheit
        if sync is not None:
            json_payload["sync"] = sync
        res = self.seam.make_request("POST", "/thermostats/cool", json=json_payload)
        return None.from_dict(res[""])

    def get(self, device_id: Optional[Any] = None, name: Optional[Any] = None):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if name is not None:
            json_payload["name"] = name
        res = self.seam.make_request("POST", "/thermostats/get", json=json_payload)
        return Device.from_dict(res["thermostat"])

    def heat(
        self,
        device_id: Optional[Any] = None,
        heating_set_point_celsius: Optional[Any] = None,
        heating_set_point_fahrenheit: Optional[Any] = None,
        sync: Optional[Any] = None,
    ):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if heating_set_point_celsius is not None:
            json_payload["heating_set_point_celsius"] = heating_set_point_celsius
        if heating_set_point_fahrenheit is not None:
            json_payload["heating_set_point_fahrenheit"] = heating_set_point_fahrenheit
        if sync is not None:
            json_payload["sync"] = sync
        res = self.seam.make_request("POST", "/thermostats/heat", json=json_payload)
        return None.from_dict(res[""])

    def heat_cool(
        self,
        device_id: Optional[Any] = None,
        heating_set_point_celsius: Optional[Any] = None,
        heating_set_point_fahrenheit: Optional[Any] = None,
        cooling_set_point_celsius: Optional[Any] = None,
        cooling_set_point_fahrenheit: Optional[Any] = None,
        sync: Optional[Any] = None,
    ):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if heating_set_point_celsius is not None:
            json_payload["heating_set_point_celsius"] = heating_set_point_celsius
        if heating_set_point_fahrenheit is not None:
            json_payload["heating_set_point_fahrenheit"] = heating_set_point_fahrenheit
        if cooling_set_point_celsius is not None:
            json_payload["cooling_set_point_celsius"] = cooling_set_point_celsius
        if cooling_set_point_fahrenheit is not None:
            json_payload["cooling_set_point_fahrenheit"] = cooling_set_point_fahrenheit
        if sync is not None:
            json_payload["sync"] = sync
        res = self.seam.make_request(
            "POST", "/thermostats/heat_cool", json=json_payload
        )
        return None.from_dict(res[""])

    def list(
        self,
        connected_account_id: Optional[Any] = None,
        connected_account_ids: Optional[Any] = None,
        connect_webview_id: Optional[Any] = None,
        device_types: Optional[Any] = None,
        manufacturer: Optional[Any] = None,
        device_ids: Optional[Any] = None,
        limit: Optional[Any] = None,
        created_before: Optional[Any] = None,
        user_identifier_key: Optional[Any] = None,
    ):
        json_payload = {}
        if connected_account_id is not None:
            json_payload["connected_account_id"] = connected_account_id
        if connected_account_ids is not None:
            json_payload["connected_account_ids"] = connected_account_ids
        if connect_webview_id is not None:
            json_payload["connect_webview_id"] = connect_webview_id
        if device_types is not None:
            json_payload["device_types"] = device_types
        if manufacturer is not None:
            json_payload["manufacturer"] = manufacturer
        if device_ids is not None:
            json_payload["device_ids"] = device_ids
        if limit is not None:
            json_payload["limit"] = limit
        if created_before is not None:
            json_payload["created_before"] = created_before
        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key
        res = self.seam.make_request("POST", "/thermostats/list", json=json_payload)
        return [Device.from_dict(item) for item in res["thermostats"]]

    def off(self, device_id: Optional[Any] = None, sync: Optional[Any] = None):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if sync is not None:
            json_payload["sync"] = sync
        res = self.seam.make_request("POST", "/thermostats/off", json=json_payload)
        return None.from_dict(res[""])

    def set_fan_mode(
        self,
        device_id: Optional[Any] = None,
        fan_mode: Optional[Any] = None,
        fan_mode_setting: Optional[Any] = None,
        sync: Optional[Any] = None,
    ):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if fan_mode is not None:
            json_payload["fan_mode"] = fan_mode
        if fan_mode_setting is not None:
            json_payload["fan_mode_setting"] = fan_mode_setting
        if sync is not None:
            json_payload["sync"] = sync
        res = self.seam.make_request(
            "POST", "/thermostats/set_fan_mode", json=json_payload
        )
        return None.from_dict(res[""])

    def update(
        self,
        device_id: Optional[Any] = None,
        default_climate_setting: Optional[Any] = None,
    ):
        json_payload = {}
        if device_id is not None:
            json_payload["device_id"] = device_id
        if default_climate_setting is not None:
            json_payload["default_climate_setting"] = default_climate_setting
        res = self.seam.make_request("POST", "/thermostats/update", json=json_payload)
        return None.from_dict(res[""])
