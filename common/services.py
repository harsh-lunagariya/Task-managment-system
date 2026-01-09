from .models import ActivityLog

def log_activity(
        *,
        actor,
        workspace,
        action,
        object_type,
        object_id,
        message
):
    ActivityLog.objects.create(
        actor=actor,
        workspace=workspace,
        action=action,
        object_type=object_type,
        object_id=object_id,
        message=message,
    )