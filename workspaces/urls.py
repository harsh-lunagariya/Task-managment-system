from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, WorkspaceMembershipViewSet
from django.urls import path

router = DefaultRouter()
router.register(r"workspaces", WorkspaceViewSet, basename="workspace")

urlpatterns = router.urls


member_list = WorkspaceMembershipViewSet.as_view({
    "get": "list",
    "post": "create",
})
member_detail = WorkspaceMembershipViewSet.as_view({
    "delete": "destroy",
    "patch": "partial_update",
})

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/members/",
        member_list,
        name="workspace-member-list"
    ),
    path(
        "workspaces/<uuid:workspace_id>/members/<uuid:pk>/",
        member_detail,
        name="workspace-member-detail"
    ),
]