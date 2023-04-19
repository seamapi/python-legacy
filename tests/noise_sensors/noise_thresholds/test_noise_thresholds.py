from seamapi import Seam
from seamapi.types import SeamAPIException
from tests.fixtures.run_minut_factory import run_minut_factory


def test_noise_thresholds(seam: Seam):
    run_minut_factory(seam)

    device = seam.devices.list()[0]

    def get_minut_device_noise_thresholds():
        return seam.noise_sensors.noise_thresholds.list(
            device_id=device.device_id
        )

    noise_thresholds = get_minut_device_noise_thresholds()
    assert len(noise_thresholds) == 2

    quiet_hours_threshold = next(
        (nt for nt in noise_thresholds if nt["name"] == "builtin_quiet_hours"),
        None,
    )
    seam.noise_sensors.noise_thresholds.delete(
        device_id=device.device_id,
        noise_threshold_id=quiet_hours_threshold.noise_threshold_id,
    )
    noise_thresholds = get_minut_device_noise_thresholds()
    assert len(noise_thresholds) == 1

    seam.noise_sensors.noise_thresholds.create(
        device_id=device.device_id,
        starts_daily_at="20:00",
        ends_daily_at="08:00",
        noise_threshold_decibels=75,
    )
    noise_thresholds = get_minut_device_noise_thresholds()
    assert len(noise_thresholds) == 2
