from seamapi.types import (
    NoiseThreshold,
    AbstractNoiseThresholds,
    AbstractSeam as Seam,
    ActionAttempt,
    ActionAttemptError,
)
from typing import List, Optional
import requests

from seamapi.utils.report_error import report_error


class NoiseThresholds(AbstractNoiseThresholds):
    """
    A class to interact with noise thresholds through the Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(device_id)
        Gets a list of noise thresholds of a noise-monitoring device
    create(device_id, starts_daily_at, ends_daily_at, sync=None, noise_threshold_decibels=None, noise_threshold_nrs=None)
        Creates a noise threshold on a noise-monitoring device
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Intial seam class
        """
        self.seam = seam

    @report_error
    def list(
        self,
        device_id: str,
    ) -> List[NoiseThreshold]:
        """Gets a list of noise thresholds.

        Parameters
        ----------
        device_id : str
            Device ID of a device to list noise thresholds of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of noise thresholds.
        """
        res = self.seam.make_request(
            "GET",
            "/noise_sensors/noise_thresholds/list",
            params={"device_id": device_id},
        )

        return res["noise_thresholds"]

    @report_error
    def create(
        self,
        device_id: str,
        starts_daily_at: str,
        ends_daily_at: str,
        sync: Optional[bool] = None,
        noise_threshold_decibels: Optional[float] = None,
        noise_threshold_nrs: Optional[float] = None,
    ) -> List[NoiseThreshold]:
        """Creates a noise threshold.

        Parameters
        ----------
        device_id : str
            Device ID of a device to list noise thresholds of
        sync: Optional[bool]
            Should wait for action attempt to resolve
        starts_daily_at: str,
            Time when noise threshold becomes active
        ends_daily_at: str,
            Time when noise threshold becomes inactive
        noise_threshold_decibels: Optional[float],
            The noise level in decibels
        noise_threshold_nrs: Optional[float],
            Noise Level in Noiseaware Noise Risk Score (NRS)
        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """
        params = {
            "device_id": device_id,
            "starts_daily_at": starts_daily_at,
            "ends_daily_at": ends_daily_at,
        }

        arguments = {
            "sync": sync,
            "noise_threshold_decibels": noise_threshold_decibels,
            "noise_threshold_nrs": noise_threshold_nrs,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "POST",
            "/noise_sensors/noise_thresholds/create",
            params={"device_id": device_id},
        )

        json_aa = res["action_attempt"]
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

    @report_error
    def delete(self, noise_threshold_id):
        raise NotImplementedError()

    @report_error
    def update(self, noise_threshold_id):
        raise NotImplementedError()
