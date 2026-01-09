from django.urls import path
from .views import TaskViewSet, TaskCommentViewSet

task_list = TaskViewSet.as_view({
    "get": "list",
    "post": "create",
})

task_detail = TaskViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

comment_list = TaskCommentViewSet.as_view({
    "get": "list",
    "post": "create",
})

comment_detail = TaskCommentViewSet.as_view({
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
})



urlpatterns = [
    path(
        "projects/<uuid:project_id>/tasks/",
        task_list,
        name="task-list",
    ),
    path(
        "projects/<uuid:project_id>/tasks/<uuid:pk>/",
        task_detail,
        name="task-detail",
    ),

    path(
        "tasks/<uuid:task_id>/comments/",
        comment_list,
        name="task-comment-list",
    ),
    path(
        "tasks/<uuid:task_id>/comments/<uuid:pk>/",
        comment_detail,
        name="task-comment-detail"
    ),
]

