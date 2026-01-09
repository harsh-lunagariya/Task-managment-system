from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer
from .permissions import ProjectPermission

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        qs = Project.objects.filter(
            workspace__memberships__user = self.request.user
        ).distinct()

        if self.action == "retrieve":
            qs = qs.prefetch_related(
                "tasks_comments"
            )
            
        return qs