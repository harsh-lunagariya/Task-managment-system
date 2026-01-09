from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from common.services import log_activity
from common.constants import ActivityAction

from .models import Workspace, WorkspaceMembership
from .serializers import WorkspaceSerializer, WorkspaceDetailSerializer, WorkspaceMembershipSerializer
from .permissions import WorkspacePermission, WorkspaceMemberPermission
from .constants import WorkspaceRole

class WorkspaceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, WorkspacePermission]

    def get_queryset(self):
        qs = Workspace.objects.filter(
            memberships__user = self.request.user
        ).distinct()

        if self.action == "retrieve":
            qs = qs.prefetch_related(
                "projects__tasks__comments"
            )
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorkspaceDetailSerializer
        return WorkspaceSerializer

class WorkspaceMembershipViewSet(ModelViewSet):
    serializer_class = WorkspaceMembershipSerializer
    permission_classes = [IsAuthenticated, WorkspaceMemberPermission]

    def get_workspace(self):
        if not hasattr(self, "_workspace"):
            workspace_id = self.kwargs["workspace_id"]
            self._workspace = get_object_or_404(
                Workspace,
                id=workspace_id
            )
        return self._workspace
    
    def get_queryset(self):
        return WorkspaceMembership.objects.filter(
            workspace=self.get_workspace()
        ).select_related(
            "user"
        )
    
    def perform_create(self, serializer):
        workspace  = self.get_workspace()

        # prevent dupclicate membership
        if WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=serializer.validated_data["user"],
        ).exists():
            raise ValidationError("User already a member.")
        
        membership = serializer.save(workspace=workspace)

        log_activity(
            actor=self.request.user,
            workspace=membership.workspace,
            action=ActivityAction.MEMBER_ADDED,
            object_type="WorkspaceMembership",
            object_id=membership.id,
            message=(
                f"{membership.user.email} was added to "
                f"workspace '{membership.workspace.name}' "
                f"as {membership.role}"
            )
        )
    
    def perform_update(self, serializer):
        old_membership = self.get_workspace()
        old_role = old_membership.role

        membership = serializer.save()

        if old_role != membership.role:
            log_activity(
                actor=self.request.user,
                workspace=membership.workspace,
                action=ActivityAction.MEMBER_ROLE_CHANGED,
                object_type="WorkspaceMembership",
                object_id=membership.id,
                message=(
                    f"{membership.user.email}'s role changed "
                    f"from {old_role} to {membership.role} "
                    f"in workspace '{membership.workspace.name}'"
                )
            )
        

    def perform_destroy(self, instance):
        # prevent removing OWNER
        if instance.role == WorkspaceRole.OWNER:
            raise ValidationError("Owner cannot be removed.")
        instance.delete()