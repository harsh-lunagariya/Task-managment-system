from django.contrib import admin
from .models import Project
from workspaces.models import WorkspaceMembership

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "workspace", "created_by"]

    def save_model(self, request, obj, form, change):
        if not WorkspaceMembership.objects.filter(
            workspace=obj.workspace,
            user=obj.created_by,
        ).exists():
            raise ValueError(
                "Project creator must belongs to the workspace."
            )
        super().save_model(request, obj, form, change)