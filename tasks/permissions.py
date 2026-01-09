from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Task, TaskComment
from workspaces.models import WorkspaceMembership
from workspaces.constants import WorkspaceRole

class TaskPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        workspace = obj.project.workspace

        try:
            membership = WorkspaceMembership.objects.get(
                workspace = workspace,
                user=user,
            )
        except WorkspaceMembership.DoesNotExist:
            return False
        
        # Read access any workspace member
        if request.method in SAFE_METHODS:
            return True
        
        # Admin Owner full access
        if membership.role in (
            WorkspaceRole.OWNER,
            WorkspaceRole.ADMIN,            
        ):
            return True
        
        if (
            obj.assign_to == user.id
            and request.method in ("PUT", "PATCH")
        ):
            allowed_fields = {"status"}
            incoming_fields = set(request.data.keys())
            return incoming_fields.issubset(allowed_fields)
        
        return False
    

class TaskCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        workspace = obj.task.project.workspace

        if not WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=user,
        ).exists():
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return obj.author_id == user.id

