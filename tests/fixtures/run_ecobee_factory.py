from seamapi import Seam

def run_ecobee_factory(seam: Seam):
    seam.make_request(
        "POST",
        "/internal/scenarios/factories/load",
        json={
            "factory_name": "create_ecobee_devices",
            "input": {"num": 2},
            "sync": True,
        },
    )
