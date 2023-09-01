from seamapi import Seam
from tests.fixtures.run_nest_factory import run_nest_factory


def test_thermostats(seam: Seam):
    run_nest_factory(seam)

    # Test List
    thermostats = seam.thermostats.list()

    assert len(thermostats) == 3

    thermostat = thermostats[0]

    assert thermostat.device_type == "nest_thermostat"

    # Test Get
    thermostat = seam.thermostats.get(thermostat.device_id)
    assert thermostat.device_type == "nest_thermostat"

    # Test Update
    result = seam.thermostats.update(
        device=thermostat,
        default_climate_setting={
            "hvac_mode_setting": "cool",
            "cooling_set_point_celsius": 20,
            "manual_override_allowed": True,
        },
    )
    assert result == True

    # Test Cool
    seam.thermostats.cool(
        device=thermostat,
        cooling_set_point_celsius=27,
    )
    thermostat = seam.thermostats.get(thermostat)
    assert (
        round(thermostat.properties.current_climate_setting.cooling_set_point_celsius)
        == 27
    )
    assert thermostat.properties.current_climate_setting.hvac_mode_setting == "cool"

    # Test Heat
    seam.thermostats.heat(
        device=thermostat,
        heating_set_point_celsius=18,
    )
    thermostat = seam.thermostats.get(thermostat)
    assert (
        round(thermostat.properties.current_climate_setting.heating_set_point_celsius)
        == 27
    )

    # Test Heat Cool
    seam.thermostats.heat_cool(
        device=thermostat,
        cooling_set_point_celsius=28,
        heating_set_point_celsius=19,
    )
    thermostat = seam.thermostats.get(thermostat)
    assert thermostat.properties.current_climate_setting.hvac_mode_setting == "heat_cool"

    # Test Off
    seam.thermostats.off(
        device=thermostat,

    )
    thermostat = seam.thermostats.get(thermostat)
    assert thermostat.properties.current_climate_setting.hvac_mode_setting == "off"

    # Test Set Fan Mode
    seam.thermostats.off(
        device=thermostat,
        fan_mode="on",
    )
    thermostat = seam.thermostats.get(thermostat)
    assert thermostat.properties.is_fan_running == True
