from seamapi import Seam
import time
import requests


def run_august_factory(seam: Seam):
    requests.post(
        f"{seam.api_url}/internal/scenarios/factories/load",
        json={
            "factory_name": "create_august_devices",
            "input": {"num": 1},
            "sync": True,
        },
        headers={
            "Authorization": f"Bearer {seam.api_key}",
        },
    )

    # TODO remove when sync is supported in /internal/scenarios/factories/load
    time.sleep(0.2)
