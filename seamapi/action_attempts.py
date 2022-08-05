from seamapi.types import (
    AbstractActionAttempts,
    ActionAttemptError,
    ActionAttempt,
    AbstractSeam as Seam,
    ActionAttemptFailedException,
    ActionAttemptId,
)
import time
import requests
from typing import Union
from seamapi.utils.convert_to_id import to_action_attempt_id


class ActionAttempts(AbstractActionAttempts):
    """
    A class used to retrieve action attempt data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    get(action_attempt)
        Gets data about an action attempt
    poll_until_ready(action_attempt)
        Polls an action attempt until its status is 'success' or 'error'
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Initial seam class
        """

        self.seam = seam

    def get(
        self, action_attempt: Union[ActionAttemptId, ActionAttempt]
    ) -> ActionAttempt:
        """Gets data about an action attempt.

        Parameters
        ----------
        action_attempt : ActionAttemptId or ActionAttempt
            Action attempt id or ActionAttempt to get latest state of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """

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
        self,
        action_attempt: Union[ActionAttemptId, ActionAttempt],
        should_raise: bool = True,
    ) -> ActionAttempt:
        """
        Polls an action attempt until its status is 'success' or 'error'.

        Parameters
        ----------
        action_attempt : ActionAttemptId or ActionAttempt
            Action attempt id or ActionAttempt to be polled

        Returns
        ------
            ActionAttempt
        """

        updated_action_attempt = None
        while (
            updated_action_attempt is None or updated_action_attempt.status == "pending"
        ):
            updated_action_attempt = self.get(action_attempt)
            time.sleep(0.25)

        if updated_action_attempt.status == "error" and should_raise:
            error_type = None
            error_message = None
            if updated_action_attempt.error is not None:
                error_type = updated_action_attempt.error.type
                error_message = updated_action_attempt.error.message
            raise ActionAttemptFailedException(
                action_attempt_id=updated_action_attempt.action_attempt_id,
                action_type=updated_action_attempt.action_type,
                error_type=error_type,
                error_message=error_message,
            )

        return updated_action_attempt
