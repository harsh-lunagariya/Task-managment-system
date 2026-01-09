from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model

from workspaces.models import Workspace, WorkspaceMembership
from workspaces.constants import WorkspaceRole
from projects.models import Project
from tasks.models import Task
from tasks.views import TaskViewSet

User = get_user_model()

class TaskPermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.owner = User.objects.create_user(
            email="owner@test.com",
            password="pass123"
        )
        self.member = User.objects.create_user(
            email="member@test.com",
            password="pass123"
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            created_by=self.owner
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.owner,
            role=WorkspaceRole.OWNER
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.member,
            role=WorkspaceRole.MEMBER
        )

        self.project = Project.objects.create(
            workspace = self.workspace,
            name="Backend1",
            created_by=self.owner
        )

        self.task = Task.objects.create(
            project=self.project,
            title="Setup DB",
            created_by = self.owner
        )

    def test_owner_can_assign_task(self):
        request = self.factory.patch(
            f"/api/projects/{self.project.id}/tasks/{self.task.id}/",
            {"assigned_to":self.member.id},
            format="json"
        )

        force_authenticate(request, user=self.owner)

        view = TaskViewSet.as_view({"patch":"partial_update"})
        response = view(
            request,
            project_id = self.project.id,
            pk=self.task.id
        )

        print("RESPONSE DATA:", response.data)

        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.assigned_to, self.member)