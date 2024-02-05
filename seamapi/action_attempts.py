from seamapi.types import AbstractActionAttempts, AbstractSeam as Seam, ActionAttempt
from typing import Optional, Any

import time


class ActionAttempts(AbstractActionAttempts):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(self, action_attempt_id: Any):
        json_payload = {}

        if action_attempt_id is not None:
            json_payload["action_attempt_id"] = action_attempt_id

        res = self.seam.make_request("POST", "/action_attempts/get", json=json_payload)

        return ActionAttempt.from_dict(res["action_attempt"])

    def list(self, action_attempt_ids: Any):
        json_payload = {}

        if action_attempt_ids is not None:
            json_payload["action_attempt_ids"] = action_attempt_ids

        res = self.seam.make_request("POST", "/action_attempts/list", json=json_payload)

        return [ActionAttempt.from_dict(item) for item in res["action_attempts"]]

    def poll_until_ready(self, action_attempt_id: str) -> ActionAttempt:
        seam = self.seam
        time_waiting = 0.0

        action_attempt = seam.action_attempts.get(action_attempt_id)

        while action_attempt.status == "pending":
            action_attempt = seam.action_attempts.get(action_attempt.action_attempt_id)

            if time_waiting > 20.0:
                raise Exception("Timed out waiting for action attempt to be ready")

            time.sleep(0.4)  # Sleep for 0.4 seconds
            time_waiting += 0.4

        if action_attempt.status == "failed":
            raise Exception(f"Action Attempt failed: {action_attempt.error.message}")

        return action_attempt
