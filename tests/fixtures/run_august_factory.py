from seamapi import Seam
import time
import requests


def run_august_factory(seam: Seam):
    seam.make_request(
        "POST",
        "/internal/scenarios/factories/load",
        json={
            "factory_name": "create_august_devices",
            "input": {"num": 2},
            "sync": True,
        },
    )
