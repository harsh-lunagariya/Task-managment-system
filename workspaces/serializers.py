from rest_framework import serializers
from .models import Workspace, WorkspaceMembership
from .constants import WorkspaceRole
from projects.serializers import ProjectSerializer

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
    
    def create(self, validated_data):
        user = self.context["request"].user

        workspace = Workspace.objects.create(
            name = validated_data["name"],
            created_by = user,
        )

        WorkspaceMembership.objects.create(
            workspace=workspace,
            user=user,
            role=WorkspaceRole.OWNER,
        )

        return workspace

class WorkspaceDetailSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(
        many=True,
        read_only=True,
    )
    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "created_at",
            "projects",
        ]


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMembership
        fields = [
            "id",
            "workspace",
            "user",
            "role",
            "joined_at",
        ]
        read_only_fields = [
            "id",
            "workspace",
            "joined_at",
        ]

    def validate_role(self, role):
        # Prevent OWNER role assignment
        if role not in (
            WorkspaceRole.MEMBER,
            WorkspaceRole.ADMIN,
        ):
            raise serializers.ValidationError(
                "Only MEMBER or ADMIN roles can be assigned."
            )
        return role
    

