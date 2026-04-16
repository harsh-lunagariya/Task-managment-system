from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from projects.models import Project
from workspaces.models import WorkspaceMembership
from common.services import log_activity
from common.constants import ActivityAction

from .models import Task, TaskComment
from .serializers import TaskSerializer, TaskCommentSerializer
from .permissions import TaskPermission, TaskCommentPermission
from .filters import TaskFilter

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = TaskFilter
    ordering_fields = [
        "created_at",
        "updated_at",
        "status",
    ]
    ordering = ["-created_at"]

    def get_project(self):
        """
        - project resolved from URL
        - workspace membership enforced once
        """
        if not hasattr(self, "_project"):
            project_id = self.kwargs["project_id"]

            project = get_object_or_404(Project, id=project_id)

            if not WorkspaceMembership.objects.filter(
                workspace=project.workspace,
                user=self.request.user,
            ).exists():
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Not a workspace member.")
            
            self._project = project

        return self._project
    
    def get_queryset(self):
        qs = Task.objects.filter(
            project=self.get_project()
        )

        if self.action in ("retrieve", "list"):
            qs = qs.select_related(
                "assigned_to",
                "created_by",
            ).prefetch_related(
                "comments"
            )
        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context
    
    def perform_create(self, serializer):
        task = serializer.save(
            project=self.get_project(),
            created_by=self.request.user
        )

        log_activity(
            actor=self.request.user,
            workspace=task.project.workspace,
            action=ActivityAction.TASK_CREATED,
            object_type="Task",
            object_id=task.id,
            message=(
                f"{self.request.user.email} created task "
                f"'{task.title}'"
            )
        )

    def perform_update(self, serializer):
        old_task = self.get_object()

        old_status = old_task.status
        old_assigned_to = old_task.assigned_to

        task = serializer.save()

        # status change
        if old_status != task.status:
            log_activity(
                actor=self.request.user,
                workspace=task.project.workspace,
                action=ActivityAction.TASK_STATUS_CHANGED,
                object_type="Task",
                object_id=task.id,
                message=(
                    f"{self.request.user.email} changed status of task "
                    f"'{task.title}' from "
                    f"{old_task.get_status_display()} to "
                    f"{task.get_status_display()}"
                )
            )

        # assignment change
        if old_assigned_to != task.assigned_to:
            assignee = (
                # it assign email if task is assigned to some one other wise
                # unassigned
                task.assigned_to.email
                if task.assigned_to else "unassigned"
            )

            log_activity(
                actor=self.request.user,
                workspace=task.project.workspace,
                action=ActivityAction.TASK_ASSIGNED,
                object_type="Task",
                object_id=task.id,
                message=(
                    f"{self.request.user.email} assigned task "
                    f"'{task.title}' to {assignee}"
                )
            )

    
class TaskCommentViewSet(ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated, TaskCommentPermission]

    def get_task(self):
        if not hasattr(self,"_task"):
            task_id = self.kwargs["task_id"]
            task = get_object_or_404(Task, id=task_id)

            if not WorkspaceMembership.objects.filter(
                workspace=task.project.workspace,
                user=self.request.user,
            ).exists():
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Not a workspace member.")
            
            self._task = task

        return self._task
    
    def get_queryset(self):
        qs = TaskComment.objects.filter(
            task=self.get_task()
        )
        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["task"] = self.get_task()
        return context

    def perform_create(self, serializer):
        comment = serializer.save(
            author=self.request.user,
            task=self.get_task()
        )

        log_activity(
            actor=self.request.user,
            workspace=comment.task.project.workspace,
            action=ActivityAction.COMMENT_ADDED,
            object_type="Task",
            object_id=comment.task.id,
            message=(
                f"{self.request.user.email} commented on "
                f"task '{comment.task.title}'"
            )
        )