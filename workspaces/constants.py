class WorkspaceRole:
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

    CHOICES = (
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (MEMBER, "Member"),
    )