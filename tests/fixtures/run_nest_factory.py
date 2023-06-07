from seamapi import Seam

def run_nest_factory(seam: Seam):
    seam.make_request(
        "POST",
        "/internal/scenarios/factories/load",
        json={
            "factory_name": "create_nest_devices",
            "input": {"num": 2},
            "sync": True,
        },
    )
