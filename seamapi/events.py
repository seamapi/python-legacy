from seamapi.types import (
    Event,
    AbstractEvents,
    AbstractSeam as Seam,
)
from typing import List, Optional
import requests


class Events(AbstractEvents):
    """
    A class to interact with events through the Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(since, device_id=None, device_ids=None, event_type=None, event_types=None)
        Gets a list of events
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

    def list(
        self,
        since: str,
        device_id: Optional[str] = None,
        device_ids: Optional[list] = None,
        event_type: Optional[str] = None,
        event_types: Optional[list] = None
    ) -> List[Event]:
        """Gets a list of events.

        Parameters
        ----------
			since : str
				ISO 8601 timestamp of the earliest event to return
			device_id : Optional[str]
				Device ID to filter events by
			device_ids : Optional[list]
				Device IDs to filter events by
			event_type : Optional[str]
				Event type to filter events by
			event_types : Optional[list]
				Event types to filter events by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of events.
        """
        if not since:
            raise Exception("'since' is required")

        params = {
            "since": since,
        }

        arguments = {
            "device_id": device_id,
            "device_ids": device_ids,
            "event_type": event_type,
            "event_types": event_types
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = requests.get(
            f"{self.seam.api_url}/events/list",
            params=params,
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)

        events = res.json()["events"]
        return events

    def get(
        self,
        event_id: Optional[str] = None,
        event_type: Optional[str] = None,
        device_id: Optional[str] = None
    ) -> Event:
        """Get an Event.

        Parameters
        ----------
            event_id : Optional[str]
                Event ID to filter events by
            event_type : Optional[str]
                Event type to filter events by
            device_id : Optional[str]
                Device ID to filter events by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An event or None.
        """
        params = {}

        arguments = {
            "event_id": event_id,
            "event_type": event_type,
            "device_id": device_id
        }

        for name in arguments:
            if arguments[name]:
                params.update({ name: arguments[name] })

        res = requests.get(
            f"{self.seam.api_url}/events/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params=params,
        )
        
        if not res.ok:
            raise Exception(res.text)

        if not res.json().get("event", None):
            return None

        return res.json()["event"]