from rest_framework import serializers

from .models import Project
from workspaces.models import WorkspaceMembership
from workspaces.constants import WorkspaceRole
from tasks.serializers import TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = Project
        fields = [
            "id",
            "workspace",
            "name",
            "slug",
            "created_at",
            "updated_at",
            "tasks",
        ]
        read_only_fields = [
            "id",
            "slug",
            "tasks",
            "created_at",
            "updated_at",
        ]

    def validate_workspace(self, workspace):

        user = self.context["request"].user

        if not WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=user
        ):
            raise serializers.ValidationError(
                "You are not a memberof this workspace."
            )
        
        return workspace
    
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)