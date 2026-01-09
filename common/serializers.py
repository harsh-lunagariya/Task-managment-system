from rest_framework import serializers
from .models import ActivityLog


class ActivitySerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(
        source="actor.email",
        read_only=True
    )

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "actor_email",
            "action",
            "object_type",
            "object_id",
            "message",
            "created_at",
        ]