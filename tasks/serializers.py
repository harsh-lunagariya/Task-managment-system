from rest_framework import serializers

from .models import Task, TaskComment
from projects.models import Project
from workspaces.models import WorkspaceMembership
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = [
            "id",
            "task",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "task",
            "created_at",
        ]

    def validate(self, attrs):

        user = self.context["request"].user
        task = self.context["task"]

        if not WorkspaceMembership.objects.filter(
            workspace=task.project.workspace,
            user=user,
        ).exists():
            raise serializers.ValidationError(
                "You are not a member of this workspace."
            )
        
        return attrs
    
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        validated_data["task"] = self.context["task"]
        return super().create(validated_data)
    
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        required = False,
        allow_null=True
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    comments = TaskCommentSerializer(
        many=True,
        read_only=True
    )
        
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "status_display",
            "assigned_to",
            "created_at",
            "updated_at",
            "comments"
        ]
        read_only_fields = [
            "id",
            "project",
            "comments"
            "created_at",
            "updated_at",
        ]

    def validate_assigned_to(self, user):
        """
        Change inrtoduced:
        - assigned user must belong to same workspace
        """
        # PUT/PATCH
        if self.instance:
            project = self.instance.project
        # POST
        else:
            project = self.context["project"]

        if not WorkspaceMembership.objects.filter(
            workspace=project.workspace,
            user=user
        ).exists():
            raise serializers.ValidationError(
                "Assigned user must belong to same workspace."
            )

        return user
    
    def create(self, validated_data):
        """
        created_by is forced from request.user
        """
        validated_data["created_by"] = self.context["request"].user
        validated_data["project"] = self.context["project"]
        return super().create(validated_data)
