from django.contrib import admin
from .models import Task, TaskComment
from workspaces.models import WorkspaceMembership

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "assigned_to", "status"]

    def save_model(self, request, obj, form, change):
        if obj.assigned_to:
            workspace = obj.project.workspace
            if not WorkspaceMembership.objects.filter(
                workspace=workspace,
                user=obj.assigned_to
            ).exists():
                raise ValueError(
                    "Assigned user must belongs to the same workspace."
                )
        super().save_model(request, obj, form, change)

admin.site.register(TaskComment)
