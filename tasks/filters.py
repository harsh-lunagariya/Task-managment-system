import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name="status")
    assigned_to = django_filters.UUIDFilter(field_name="assigned_to_id")

    class Meta:
        model = Task
        fields = ["status", "assigned_to"]