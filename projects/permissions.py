from rest_framework.permissions import BasePermission, SAFE_METHODS
from workspaces.models import WorkspaceMembership
from workspaces.constants import WorkspaceRole

class ProjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            membership = WorkspaceMembership.objects.get(
                workspace=obj.workspace,
                user=request.user,
            )
        except WorkspaceMembership.DoesNotExist:
            return False
        
        # read by any member
        if request.method in SAFE_METHODS:
            return True
        
        # Write by ADMIN or OWNER
        return membership.role in (
            WorkspaceRole.ADMIN,
            WorkspaceRole.OWNER,
        )