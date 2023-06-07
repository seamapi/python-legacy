from seamapi import Seam
from tests.fixtures.run_nest_factory import run_nest_factory

def test_thermostats(seam: Seam):
    run_nest_factory(seam)

    # Test List
    thermostats = seam.thermostats.list()

    print(thermostats)
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
        }
    )

    assert result == True

    # Test Delete
    result = seam.thermostats.delete(thermostat)
    assert result == None

    thermostats = seam.thermostats.list()
    assert len(thermostats) == 2
