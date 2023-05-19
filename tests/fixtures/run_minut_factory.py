from seamapi import Seam


def run_minut_factory(seam: Seam):
    seam.make_request(
        "POST",
        "/internal/scenarios/factories/load",
        json={
            "factory_name": "create_minut_devices",
            "input": {
                "devicesConfig": [
                    {
                        "sound_level_high": {
                            "value": 60,
                            "duration_seconds": 600,
                            "notifications": [],
                        },
                        "sound_level_high_quiet_hours": {
                            "value": 60,
                            "duration_seconds": 600,
                            "notifications": [],
                            "enabled": True,
                            "starts_at": "20:00",
                            "ends_at": "08:00",
                        },
                    }
                ]
            },
        },
    )
