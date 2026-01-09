from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware, datetime

from workspaces.models import Workspace, WorkspaceMembership

from .models import ActivityLog
from .serializers import ActivitySerializer

class ActivityLogViewSet(ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["action", "object_type", "actor"]

    def get_workspace(self):
        if not hasattr(self, "_workspace"):
            self._workspace = get_object_or_404(
                Workspace,
                id=self.kwargs["workspace_id"],
                memberships__user=self.request.user,
            )
        return self._workspace
    
    def get_queryset(self):
        qs = ActivityLog.objects.filter(
            workspace=self.get_workspace()
        )

        # date filtering
        from_date = self.request.query_params.get("from")
        to_date = self.request.query_params.get("to")

        if from_date:
            from_date = parse_date(from_date)
            if from_date:
                qs = qs.filter(
                    created_at__date__gte=from_date
                )
        
        if to_date:
            to_date = parse_date(to_date)
            if to_date:
                qs = qs.filter(
                    created_at__date__lte=to_date
                )
        
        return qs