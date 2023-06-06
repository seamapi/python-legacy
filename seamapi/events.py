from seamapi.types import (
    AccessCode,
    ConnectedAccount,
    Device,
    Event,
    AbstractEvents,
    AbstractSeam as Seam,
)
from typing import List, Optional, Union
import requests
from seamapi.utils.convert_to_id import (
    to_access_code_id,
    to_connected_account_id,
    to_device_id,
    to_event_id,
)

from seamapi.utils.report_error import report_error


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
    list(since=None, between=None, device_id=None, device_ids=None, access_code_id=None, access_code_ids=None, event_type=None, event_types=None, connected_account_id=None)
        Gets a list of events

    get(device_id=None, event_id=None, event_type=None)
        Gets an event
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

    @report_error
    def list(
        self,
        since: Optional[str] = None,
        between: Optional[list] = None,
        device_id: Union[str, Device] = None,
        device_ids: Optional[list] = None,
        access_code_id: Union[str, AccessCode] = None,
        access_code_ids: Optional[list] = None,
        event_type: Optional[str] = None,
        event_types: Optional[list] = None,
        connected_account_id: Union[str, ConnectedAccount] = None,
    ) -> List[Event]:
        """Gets a list of events.

        Parameters
        ----------
        since : Optional[str]
            ISO 8601 timestamp of the earliest event to return
        between : Optional[list]
            List of two ISO 8601 timestamps to specify a date range for filtering events
        device_id : Union[str, Device]
            Device ID or Device to filter events by
        device_ids : Optional[list]
            Device IDs to filter events by
        access_code_id : Union[str, AccessCode]
            Access Code ID or AccessCode to filter events by
        access_code_ids : Optional[list]
            Access Code IDs to filter events by
        event_type : Optional[str]
            Event type to filter events by
        event_types : Optional[list]
            Event types to filter events by
        connected_account_id : Union[str, ConnectedAccount]
            Connected Account ID or ConnectedAccount to filter events by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of events.
        """
        device_id = to_device_id(device_id) if device_id else None
        access_code_id = (
            to_access_code_id(access_code_id) if access_code_id else None
        )
        connected_account_id = (
            to_connected_account_id(connected_account_id)
            if connected_account_id
            else None
        )

        params = {}
        arguments = {
            "since": since,
            "between": between,
            "device_id": device_id,
            "device_ids": device_ids,
            "access_code_id": access_code_id,
            "access_code_ids": access_code_ids,
            "event_type": event_type,
            "event_types": event_types,
            "connected_account_id": connected_account_id,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "GET",
            "/events/list",
            params=params,
        )

        return res["events"]

    @report_error
    def get(
        self,
        event_id: Union[str, Event] = None,
        event_type: Optional[str] = None,
        device_id: Union[str, Device] = None,
    ) -> Event:
        """Get an Event.

        Parameters
        ----------
            event_id : Union[str, Event]
                Event ID or Event to filter events by
            event_type : Optional[str]
                Event type to filter events by
            device_id : Union[str, Device]
                Device ID or Device to filter events by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An event or None.
        """
        device_id = to_device_id(device_id) if device_id else None
        event_id = to_event_id(event_id) if event_id else None

        params = {}
        arguments = {
            "event_id": event_id,
            "event_type": event_type,
            "device_id": device_id,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "GET",
            "/events/get",
            params=params,
        )

        return res.get("event", None)
