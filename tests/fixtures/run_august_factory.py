from seamapi import Seam
import time
import requests


def run_august_factory(seam: Seam):
    factory_res = requests.post(
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
    time.sleep(0.2)
