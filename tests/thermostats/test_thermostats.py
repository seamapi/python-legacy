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

    assert (
        thermostat.properties.current_climate_setting.hvac_mode_setting
        == "heatcool"
    )
    seam.thermostats.set_mode(device=thermostat, hvac_mode_setting="cool")
    updated_thermostat = seam.thermostats.get(thermostat.device_id)
    assert (
        updated_thermostat.properties.current_climate_setting.hvac_mode_setting
        == "cool"
    )

    seam.thermostats.set_cooling_set_point(
        device=thermostat, cooling_set_point_fahrenheit=74
    )
    updated_thermostat = seam.thermostats.get(thermostat)
    assert (
        updated_thermostat.properties.current_climate_setting.cooling_set_point_fahrenheit
        == 74
    )
