from seamapi import Seam
from tests.fixtures.run_nest_factory import run_nest_factory
import datetime

def add_month_to_date(date: datetime.date, months: int) -> datetime.date:
    return datetime.datetime(date.year + int(date.month / 12), ((date.month % 12) + months), 1)

def test_climate_setting_schedules(seam: Seam):
    run_nest_factory(seam)

    thermostat = seam.thermostats.list()[0]

    base_date = datetime.date.today()

    schedule_starts_at = add_month_to_date(base_date, months=1).isoformat()
    schedule_ends_at = add_month_to_date(base_date, months=2).isoformat()

    # Test Create
    climate_setting_schedule = seam.thermostats.climate_setting_schedules.create(
        device=thermostat,
        name="Vacation Setting",
        schedule_starts_at=schedule_starts_at,
        schedule_ends_at=schedule_ends_at,
        schedule_type="time_bound",
        automatic_heating_enabled=True,
        automatic_cooling_enabled=True,
        heating_set_point_fahrenheit=40,
        cooling_set_point_fahrenheit=80,
        manual_override_allowed=True,
    )

    assert climate_setting_schedule.name == "Vacation Setting"

    # Test List
    climate_setting_schedules = seam.thermostats.climate_setting_schedules.list(device=thermostat)
    assert len(climate_setting_schedules) == 1

    # Test Update
    updated_climate_setting_schedule = seam.thermostats.climate_setting_schedules.update(
        climate_setting_schedule=climate_setting_schedule,
        name="Vacation Setting 2",
    )

    assert updated_climate_setting_schedule.name == "Vacation Setting 2"

    # Test Get
    climate_setting_schedule = seam.thermostats.climate_setting_schedules.get(
        climate_setting_schedule=climate_setting_schedule,
    )

    assert climate_setting_schedule.name == "Vacation Setting 2"

    # Test Delete
    result = seam.thermostats.climate_setting_schedules.delete(
        climate_setting_schedule=climate_setting_schedule,
    )

    assert result == None
