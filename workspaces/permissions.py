from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import WorkspaceMembership
from .constants import WorkspaceRole

class WorkspacePermission(BasePermission):
    def has_object_permission(self, request, view, obj):        
        try:
            membership = WorkspaceMembership.objects.get(
                user = request.user,
                workspace = obj
            )
        except WorkspaceMembership.DoesNotExist:
            return False
        
        # Read access -> any member
        if request.method in SAFE_METHODS:
            return True
        
        # Update -> ADMIN or OWNER
        if request.method in ["PUT", "PATCH"]:
            return membership.role in (
                WorkspaceRole.OWNER,
                WorkspaceRole.ADMIN,
            )
        
        # Delete -> OWNER only
        if request.method == "DELETE":
            return membership.role == WorkspaceRole.OWNER
        
        return False
    
class WorkspaceMemberPermission(BasePermission):
    # OWNER / ADMIN can manage member
    def has_permission(self, request, view):
        workspace = view.get_workspace()
        try:
            membership = WorkspaceMembership.objects.get(
                workspace=workspace,
                user=request.user,
            )
        except WorkspaceMembership.DoesNotExist:
            return False
        
        return membership.role in (
            WorkspaceRole.OWNER,
            WorkspaceRole.ADMIN,
        )