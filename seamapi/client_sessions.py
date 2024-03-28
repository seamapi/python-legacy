from seamapi.types import AbstractClientSessions, AbstractSeam as Seam, ClientSession
from typing import Optional, Any, List, Dict, Union


class ClientSessions(AbstractClientSessions):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def create(
        self,
        *,
        user_identifier_key: Optional[str] = None,
        connect_webview_ids: Optional[List[str]] = None,
        connected_account_ids: Optional[List[str]] = None,
        user_identity_ids: Optional[List[str]] = None,
        expires_at: Optional[str] = None
    ) -> ClientSession:
        json_payload = {}

        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key
        if connect_webview_ids is not None:
            json_payload["connect_webview_ids"] = connect_webview_ids
        if connected_account_ids is not None:
            json_payload["connected_account_ids"] = connected_account_ids
        if user_identity_ids is not None:
            json_payload["user_identity_ids"] = user_identity_ids
        if expires_at is not None:
            json_payload["expires_at"] = expires_at

        res = self.seam.make_request(
            "POST", "/client_sessions/create", json=json_payload
        )

        return ClientSession.from_dict(res["client_session"])

    def delete(self, *, client_session_id: str) -> None:
        json_payload = {}

        if client_session_id is not None:
            json_payload["client_session_id"] = client_session_id

        self.seam.make_request("POST", "/client_sessions/delete", json=json_payload)

        return None

    def get(
        self,
        *,
        client_session_id: Optional[str] = None,
        user_identifier_key: Optional[str] = None
    ) -> ClientSession:
        json_payload = {}

        if client_session_id is not None:
            json_payload["client_session_id"] = client_session_id
        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key

        res = self.seam.make_request("POST", "/client_sessions/get", json=json_payload)

        return ClientSession.from_dict(res["client_session"])

    def get_or_create(
        self,
        *,
        user_identifier_key: Optional[str] = None,
        connect_webview_ids: Optional[List[str]] = None,
        connected_account_ids: Optional[List[str]] = None,
        user_identity_ids: Optional[List[str]] = None,
        expires_at: Optional[str] = None
    ) -> ClientSession:
        json_payload = {}

        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key
        if connect_webview_ids is not None:
            json_payload["connect_webview_ids"] = connect_webview_ids
        if connected_account_ids is not None:
            json_payload["connected_account_ids"] = connected_account_ids
        if user_identity_ids is not None:
            json_payload["user_identity_ids"] = user_identity_ids
        if expires_at is not None:
            json_payload["expires_at"] = expires_at

        res = self.seam.make_request(
            "POST", "/client_sessions/get_or_create", json=json_payload
        )

        return ClientSession.from_dict(res["client_session"])

    def grant_access(
        self,
        *,
        client_session_id: Optional[str] = None,
        user_identifier_key: Optional[str] = None,
        connected_account_ids: Optional[List[str]] = None,
        connect_webview_ids: Optional[List[str]] = None,
        user_identity_ids: Optional[List[str]] = None
    ) -> None:
        json_payload = {}

        if client_session_id is not None:
            json_payload["client_session_id"] = client_session_id
        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key
        if connected_account_ids is not None:
            json_payload["connected_account_ids"] = connected_account_ids
        if connect_webview_ids is not None:
            json_payload["connect_webview_ids"] = connect_webview_ids
        if user_identity_ids is not None:
            json_payload["user_identity_ids"] = user_identity_ids

        self.seam.make_request(
            "POST", "/client_sessions/grant_access", json=json_payload
        )

        return None

    def list(
        self,
        *,
        client_session_id: Optional[str] = None,
        user_identifier_key: Optional[str] = None,
        connect_webview_id: Optional[str] = None,
        without_user_identifier_key: Optional[bool] = None,
        user_identity_id: Optional[str] = None
    ) -> List[ClientSession]:
        json_payload = {}

        if client_session_id is not None:
            json_payload["client_session_id"] = client_session_id
        if user_identifier_key is not None:
            json_payload["user_identifier_key"] = user_identifier_key
        if connect_webview_id is not None:
            json_payload["connect_webview_id"] = connect_webview_id
        if without_user_identifier_key is not None:
            json_payload["without_user_identifier_key"] = without_user_identifier_key
        if user_identity_id is not None:
            json_payload["user_identity_id"] = user_identity_id

        res = self.seam.make_request("POST", "/client_sessions/list", json=json_payload)

        return [ClientSession.from_dict(item) for item in res["client_sessions"]]

    def revoke(self, *, client_session_id: str) -> None:
        json_payload = {}

        if client_session_id is not None:
            json_payload["client_session_id"] = client_session_id

        self.seam.make_request("POST", "/client_sessions/revoke", json=json_payload)

        return None