from seamapi.types import (
    AbstractSeam as Seam,
    AbstractWorkspaces,
    Workspace,
    WorkspaceId,
    ResetSandBoxResponse,
)
from typing import Optional, List, Union
import requests

from seamapi.utils.convert_to_id import to_workspace_id


class Workspaces(AbstractWorkspaces):
    """
    A class used to retreive workspace data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(workspace=None)
        Gets a list of workspaces
    get(workspace=None)
        Gets a workspace
    reset_sandbox()
        Resets workspace sandbox
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
        workspace: Optional[Union[WorkspaceId, Workspace]] = None,
    ) -> List[Workspace]:
        """Gets a list of workspaces.

        Parameters
        ----------
        workspace : WorkspaceId or Workspace, optional
            Workspace id or Workspace to get latest version of

        Raises
        ------
        Exception
            If workspaces weren't found.
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Workspace
        """

        workspace_id = None if workspace is None else to_workspace_id(workspace)
        res = requests.get(
            f"{self.seam.api_url}/workspaces/list",
            params={"workspace_id": workspace_id},
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if res.status_code == 404:
            raise Exception("workspaces not found")  # TODO custom exception
        if res.status_code != 200:
            raise Exception(res.text)
        res_json = res.json()
        return res_json["workspaces"]

    def get(
        self,
        workspace: Optional[Union[WorkspaceId, Workspace]] = None,
    ) -> Workspace:
        """Gets a workspace.

        Parameters
        ----------
        workspace : WorkspaceId or Workspace, optional
            Workspace id or Workspace to get latest version of

        Raises
        ------
        Exception
            If the workspace wasn't found.
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Workspace
        """
        workspace_id = None if workspace is None else to_workspace_id(workspace)
        res = requests.get(
            f"{self.seam.api_url}/workspaces/get",
            params={"workspace_id": workspace_id},
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if res.status_code == 404:
            raise Exception("workspace not found")  # TODO custom exception
        if res.status_code != 200:
            raise Exception(res.text)
        res_json = res.json()
        return Workspace(
            workspace_id=res_json["workspace"]["workspace_id"],
            name=res_json["workspace"]["name"],
            is_sandbox=res_json["workspace"]["is_sandbox"],
        )

    def reset_sandbox(self) -> None:
        """Resets workspace sandbox.

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ResetSandBoxResponse
        """

        res = requests.post(
            f"{self.seam.api_url}/workspaces/reset_sandbox",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
        )
        if not res.ok:
            raise Exception(res.text)

        return ResetSandBoxResponse(
            message="Successfully reset workspace sandbox",
            ok=True,
        )
