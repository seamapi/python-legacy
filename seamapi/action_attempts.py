from seamapi.types import (
    AbstractActionAttempts,
    ActionAttemptError,
    ActionAttempt,
    AbstractSeam as Seam,
    ActionAttemptId,
)
import time
import requests
from typing import Union


def to_action_attempt_id(action_attempt: Union[ActionAttemptId, ActionAttempt]) -> str:
    if isinstance(action_attempt, str):
        return action_attempt
    return action_attempt.action_attempt_id


class ActionAttempts(AbstractActionAttempts):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def get(
        self, action_attempt: Union[ActionAttemptId, ActionAttempt]
    ) -> ActionAttempt:
        action_attempt_id = to_action_attempt_id(action_attempt)
        res = requests.get(
            f"{self.seam.api_url}/action_attempts/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"action_attempt_id": action_attempt_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_aa = res.json()["action_attempt"]
        error = None
        if "error" in json_aa and json_aa["error"] is not None:
            error = ActionAttemptError(
                type=json_aa["error"]["type"],
                message=json_aa["error"]["message"],
            )
        return ActionAttempt(
            action_attempt_id=json_aa["action_attempt_id"],
            status=json_aa["status"],
            action_type=json_aa["action_type"],
            result=json_aa["result"],
            error=error,
        )

    def poll_until_ready(
        self, action_attempt: Union[ActionAttemptId, ActionAttempt]
    ) -> ActionAttempt:
        updated_action_attempt = None
        while (
            updated_action_attempt is None or updated_action_attempt.status == "pending"
        ):
            updated_action_attempt = self.get(action_attempt)
            time.sleep(0.25)
        return updated_action_attempt
