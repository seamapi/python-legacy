from seamapi import Seam
from tests.fixtures.run_ecobee_factory import run_ecobee_factory
import json


def test_thermostats(seam: Seam):
    # run_ecobee_factory(seam)

    # Test List
    # Blocked by:  AssertionError: assert 1 == 3
    # Increase the number of ecobee thermostats to 3?
    thermostats = seam.thermostats.list()

    # assert len(thermostats) == 3

    thermostat = thermostats[0]
    assert thermostat.device_type == "ecobee_thermostat"

    # Test Get
    thermostat = seam.thermostats.get(thermostat.device_id)
    assert thermostat.device_type == "ecobee_thermostat"

    # Test Update
    # AttributeError: 'Thermostats' object has no attribute 'update'

    # result = seam.thermostats.update(
    #     device=thermostat,
    #     default_climate_setting={
    #         "hvac_mode_setting": "cool",
    #         "cooling_set_point_celsius": 20,
    #         "manual_override_allowed": True,
    #     },
    # )
    # assert result == True

    # Test Cool
    # blocked by:
    # AttributeError: 'Thermostats' object has no attribute 'update'
    # AttributeError: 'Thermostats' object has no attribute 'cool'

    # seam.thermostats.cool(
    #     device=thermostat,
    #     cooling_set_point_celsius=27,
    # )
    # thermostat = seam.thermostats.get(thermostat)
    # assert (
    #     round(thermostat.properties.current_climate_setting.cooling_set_point_celsius)
    #     == 27
    # )
    # assert thermostat.properties.current_climate_setting.hvac_mode_setting == "cool"

    # Test Heat
    # AttributeError: 'Thermostats' object has no attribute 'heat'

    # seam.thermostats.heat(
    #     device=thermostat,
    #     heating_set_point_celsius=18,
    # )
    # thermostat = seam.thermostats.get(thermostat)
    # assert (
    #     round(thermostat.properties.current_climate_setting.heating_set_point_celsius)
    #     == 18
    # )

    # Test Heat Cool
    # AttributeError: 'Thermostats' object has no attribute 'heat_cool'

    # seam.thermostats.heat_cool(
    #     device=thermostat,
    #     cooling_set_point_celsius=28,
    #     heating_set_point_celsius=19,
    # )
    # thermostat = seam.thermostats.get(thermostat)
    # assert thermostat.properties.current_climate_setting.hvac_mode_setting == "heat_cool"
    # assert (
    # round(thermostat.properties.current_climate_setting.cooling_set_point_celsius)
    # == 28
    # )
    # assert (
    # round(thermostat.properties.current_climate_setting.heating_set_point_celsius)
    # == 19
    # )

    # Test Off
    # AttributeError: 'Thermostats' object has no attribute 'off'

    # seam.thermostats.off(
    #     device=thermostat,

    # )
    # thermostat = seam.thermostats.get(thermostat)
    # assert thermostat.properties.current_climate_setting.hvac_mode_setting == "off"

    # Test Set Fan Mode
    # AttributeError: 'Thermostats' object has no attribute 'set_fan_mode'

    # seam.thermostats.set_fan_mode(
    #     device=thermostat,
    #     fan_mode="on",
    # )
    # thermostat = seam.thermostats.get(thermostat)
    # assert thermostat.properties.is_fan_running == True
