from seamapi.types import (
    AbstractSeam as Seam,
    AbstractWorkspaces,
    Workspace,
    WorkspaceId,
    ResetSandBoxResponse,
)
from typing import Optional, List, Union

from seamapi.utils.convert_to_id import to_workspace_id
from seamapi.utils.report_error import report_error


class Workspaces(AbstractWorkspaces):
    """
    A class used to retrieve workspace data
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

    @report_error
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
        res = self.seam.make_request(
            "GET",
            "/workspaces/list",
            params={"workspace_id": workspace_id},
        )
        return res["workspaces"]

    @report_error
    def get(
        self
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
        res = self.seam.make_request(
            "GET",
            "/workspaces/get",
        )
        return Workspace(
            workspace_id=res["workspace"]["workspace_id"],
            name=res["workspace"]["name"],
            is_sandbox=res["workspace"]["is_sandbox"],
        )

    @report_error
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
        self.seam.make_request(
            "POST",
            "/workspaces/reset_sandbox",
        )

        return ResetSandBoxResponse(
            message="Successfully reset workspace sandbox",
            ok=True,
        )
