from django.urls import path
from .views import ActivityLogViewSet

activity_list = ActivityLogViewSet.as_view({
    "get": "list",
})

urlpatterns = [
    path(
        "workspaces/<uuid:workspace_id>/activity/",
        activity_list,
        name="workspace-activity"
    ),
]
