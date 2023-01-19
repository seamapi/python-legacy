from seamapi import Seam
import time
import requests


def run_salto_factory(seam: Seam):
    seam.make_request(
        "POST",
        "/internal/scenarios/factories/load",
        json={
            "factory_name": "create_salto_devices",
            "input": {"num": 3},
            "sync": True,
        },
    )
