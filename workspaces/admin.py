from django.contrib import admin
from .models import Workspace, WorkspaceMembership
from .constants import WorkspaceRole

# Register your models here.

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display = ("workspace", "user", "role", "joined_at")
    list_filter = ("role",)
    search_fields = ("workspace__name", "user__email")

    def has_delete_permission(self, request, obj = None):
        if obj and obj.role == WorkspaceRole.OWNER:
            return False
        return super().has_delete_permission(request, obj)