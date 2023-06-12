from typing import List, Optional, Union

from seamapi.types import AbstractClimateSettingSchedules
from seamapi.types import AbstractSeam as Seam
from seamapi.types import (ClimateSettingSchedule,
                           ClimateSettingScheduleId, Device, DeviceId)
from seamapi.utils.convert_to_id import (to_climate_setting_schedule_id,
                                         to_device_id)
from seamapi.utils.report_error import report_error

class ClimateSettingSchedules(AbstractClimateSettingSchedules):
    """
    A class used to interact with Climate Setting Schedules for Thermostats

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(device=Union[DeviceId, Device])
        Gets a list of climate setting schedules for a device
    get(climate_setting_schedule: Union[ClimateSettingScheduleId, ClimateSettingSchedule])
        Gets a climate setting schedule
    create(
        device,
        device: Union[DeviceId, Device],
        schedule_starts_at: str,
        schedule_ends_at: str,
        manual_override_allowed: bool,
        name: Optional[str],
        automatic_heating_enabled: Optional[bool],
        automatic_cooling_enabled: Optional[bool],
        hvac_mode_setting: Optional[str],
        cooling_set_point_celsius: Optional[float],
        heating_set_point_celsius: Optional[float],
        cooling_set_point_fahrenheit: Optional[float],
        heating_set_point_fahrenheit: Optional[float],
        schedule_type: Optional[str],
    )
        Creates a climate setting schedule for a Device
    update(
        climate_setting_schedule,
        self,
        climate_setting_schedule: Union[str, ClimateSettingSchedule],
        schedule_starts_at: Optional[str],
        schedule_ends_at: Optional[str],
        name: Optional[str],
        automatic_heating_enabled: Optional[bool],
        automatic_cooling_enabled: Optional[bool],
        hvac_mode_setting: Optional[str],
        cooling_set_point_celsius: Optional[float],
        heating_set_point_celsius: Optional[float],
        cooling_set_point_fahrenheit: Optional[float],
        heating_set_point_fahrenheit: Optional[float],
        manual_override_allowed: Optional[bool],
        schedule_type: Optional[str],
    )
        Updates a climate setting schedule
    delete(climate_setting_schedule)
        Deletes a climate setting schedule
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
    def list(
        self,
        device: Union[DeviceId, Device],
    ) -> List[ClimateSettingSchedule]:
        """Gets a list of Climate Setting Schedules.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to get the climate setting schedules of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of climate setting schedules.
        """
        device_id = to_device_id(device)

        res = self.seam.make_request(
            "GET",
            "/thermostats/climate_setting_schedules/list",
            params={
                "device_id": device_id
            },
        )
        climate_setting_schedules = res["climate_setting_schedules"]

        return [ClimateSettingSchedule.from_dict(d) for d in climate_setting_schedules]

    @report_error
    def get(
        self,
        climate_setting_schedule: Union[ClimateSettingScheduleId, ClimateSettingSchedule]
    ) -> ClimateSettingSchedule:
        """Gets a Climate Setting Schedule.

        Parameters
        ----------
        climate_setting_schedule : Id or ClimateSettingSchedule
            Id or ClimateSettingSchedule to get the state of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ClimateSettingSchedule
        """

        climate_setting_schedule_id = to_climate_setting_schedule_id(climate_setting_schedule)

        res = self.seam.make_request("GET", "/thermostats/climate_setting_schedules/get", params={
            "climate_setting_schedule_id": climate_setting_schedule_id
        })
        json_response = res["climate_setting_schedule"]
        return ClimateSettingSchedule.from_dict(json_response)

    @report_error
    def create(
        self,
        device: Union[DeviceId, Device],
        schedule_starts_at: str,
        schedule_ends_at: str,
        manual_override_allowed: bool,
        name: Optional[str] = None,
        automatic_heating_enabled: Optional[bool] = None,
        automatic_cooling_enabled: Optional[bool] = None,
        hvac_mode_setting: Optional[str] = None,
        cooling_set_point_celsius: Optional[float] = None,
        heating_set_point_celsius: Optional[float] = None,
        cooling_set_point_fahrenheit: Optional[float] = None,
        heating_set_point_fahrenheit: Optional[float] = None,
        schedule_type: Optional[str] = None,
    ) -> ClimateSettingSchedule:
        """Creates a Climate Setting Schedule.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to create the climate setting schedule for
        properties : ClimateSettingScheduleBase
            Properties to update

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Boolean
        """
        device_id = to_device_id(device)

        params = climate_setting_params(
            automatic_heating_enabled,
            automatic_cooling_enabled,
            hvac_mode_setting,
            cooling_set_point_celsius,
            heating_set_point_celsius,
            cooling_set_point_fahrenheit,
            heating_set_point_fahrenheit,
            manual_override_allowed,
            schedule_type,
            name,
            schedule_starts_at,
            schedule_ends_at,
        )

        params["device_id"] = device_id

        res = self.seam.make_request(
            "POST",
            "/thermostats/climate_setting_schedules/create",
            json=params
        )
        json_response = res["climate_setting_schedule"]
        return ClimateSettingSchedule.from_dict(json_response)

    @report_error
    def update(
        self,
        climate_setting_schedule: Union[str, ClimateSettingSchedule],
        schedule_starts_at: Optional[str] = None,
        schedule_ends_at: Optional[str] = None,
        name: Optional[str] = None,
        automatic_heating_enabled: Optional[bool] = None,
        automatic_cooling_enabled: Optional[bool] = None,
        hvac_mode_setting: Optional[str] = None,
        cooling_set_point_celsius: Optional[float] = None,
        heating_set_point_celsius: Optional[float] = None,
        cooling_set_point_fahrenheit: Optional[float] = None,
        heating_set_point_fahrenheit: Optional[float] = None,
        manual_override_allowed: Optional[bool] = None,
        schedule_type: Optional[str] = None,
    ) -> ClimateSettingSchedule:
        """Updates a Climate Setting Schedule.

        Parameters
        ----------
        climate_setting_schedule : ClimateSettingScheduleId or ClimateSettingSchedule
            ClimateSettingSchedule to update
        properties : ClimateSettingScheduleBase
            Properties to update

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Boolean
        """

        climate_setting_schedule_id = to_climate_setting_schedule_id(climate_setting_schedule)

        params = climate_setting_params(
            automatic_heating_enabled,
            automatic_cooling_enabled,
            hvac_mode_setting,
            cooling_set_point_celsius,
            heating_set_point_celsius,
            cooling_set_point_fahrenheit,
            heating_set_point_fahrenheit,
            manual_override_allowed,
            schedule_type,
            name,
            schedule_starts_at,
            schedule_ends_at,
        )

        params["climate_setting_schedule_id"] = climate_setting_schedule_id

        res = self.seam.make_request(
            "POST",
            "/thermostats/climate_setting_schedules/update",
            json=params,
        )

        json_response = res["climate_setting_schedule"]
        return ClimateSettingSchedule.from_dict(json_response)

    @report_error
    def delete(
        self,
        climate_setting_schedule: Union[ClimateSettingScheduleId, ClimateSettingSchedule]
    ) -> None:
        """Deletes a climate setting schedule.

        Parameters
        ----------
        climate_setting_schedule : Id or ClimateSettingSchedule
            Id or ClimateSettingSchedule to delete

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            None
        """

        climate_setting_schedule_id = to_climate_setting_schedule_id(climate_setting_schedule)

        delete_payload = {
            "climate_setting_schedule_id": climate_setting_schedule_id
        }

        self.seam.make_request(
            "DELETE",
            "/thermostats/climate_setting_schedules/delete",
            json=delete_payload,
        )

        return None

def climate_setting_params(
    automatic_heating_enabled: Optional[bool] = None,
    automatic_cooling_enabled: Optional[bool] = None,
    hvac_mode_setting: Optional[str] = None,
    cooling_set_point_celsius: Optional[float] = None,
    heating_set_point_celsius: Optional[float] = None,
    cooling_set_point_fahrenheit: Optional[float] = None,
    heating_set_point_fahrenheit: Optional[float] = None,
    manual_override_allowed: Optional[bool] = None,
    schedule_type: Optional[str] = None,
    name: Optional[str] = None,
    schedule_starts_at: Optional[str] = None,
    schedule_ends_at: Optional[str] = None,
):
    params = {}

    if automatic_heating_enabled is not None:
        params["automatic_heating_enabled"] = automatic_heating_enabled
    if automatic_cooling_enabled is not None:
        params["automatic_cooling_enabled"] = automatic_cooling_enabled
    if hvac_mode_setting is not None:
        params["hvac_mode_setting"] = hvac_mode_setting
    if cooling_set_point_celsius is not None:
        params["cooling_set_point_celsius"] = cooling_set_point_celsius
    if heating_set_point_celsius is not None:
        params["heating_set_point_celsius"] = heating_set_point_celsius
    if cooling_set_point_fahrenheit is not None:
        params["cooling_set_point_fahrenheit"] = cooling_set_point_fahrenheit
    if heating_set_point_fahrenheit is not None:
        params["heating_set_point_fahrenheit"] = heating_set_point_fahrenheit
    if manual_override_allowed is not None:
        params["manual_override_allowed"] = manual_override_allowed
    if schedule_type is not None:
        params["schedule_type"] = schedule_type
    if name is not None:
        params["name"] = name
    if schedule_starts_at is not None:
        params["schedule_starts_at"] = schedule_starts_at
    if schedule_ends_at is not None:
        params["schedule_ends_at"] = schedule_ends_at

    return params
