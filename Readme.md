## 🔐 AUTH APIs (accounts)

| Method | Endpoint               | Purpose                       |
| ------ | ---------------------- | ----------------------------- |
| POST   | `api/auth/token/`         | Obtain access & refresh token |
| POST   | `api/auth/token/refresh/` | Refresh access token          |

> Users are created via Django Admin only.



## 🏢 WORKSPACE APIs

### Workspace CRUD

| Method | Endpoint                      | Description                      |
| ------ | ----------------------------- | -------------------------------- |
| POST   | `api/workspaces/`                | Create workspace                 |
| GET    | `api/workspaces/`                | List user workspaces             |
| GET    | `api/workspaces/{workspace_id}/` | Retrieve workspace               |
| PATCH  | `api/workspaces/{workspace_id}/` | Update workspace (ADMIN / OWNER) |
| DELETE | `api/workspaces/{workspace_id}/` | Delete workspace (OWNER only)    |


### Workspace Member Management

| Method | Endpoint                                              | Description                |
| ------ | ----------------------------------------------------- | -------------------------- |
| GET    | `api/workspaces/{workspace_id}/members/`                 | List workspace members     |
| POST   | `api/workspaces/{workspace_id}/members/`                 | Add member (ADMIN / OWNER) |
| PATCH  | `api/workspaces/{workspace_id}/members/{membership_id}/` | Change member role         |
| DELETE | `api/workspaces/{workspace_id}/members/{membership_id}/` | Remove member              |


**Rules**
* OWNER role cannot be assigned or removed
* MEMBER cannot manage members


## 📁 PROJECT APIs

| Method | Endpoint                  | Description                      |
| ------ | ------------------------- | -------------------------------- |
| POST   | `api/projects/`              | Create project (ADMIN / OWNER)   |
| GET    | `api/projects/`              | List projects (workspace-scoped) |
| GET    | `api/projects/{project_id}/` | Retrieve project                 |
| PATCH  | `api/projects/{project_id}/` | Update project (ADMIN / OWNER)   |
| DELETE | `api/projects/{project_id}/` | Delete project (ADMIN / OWNER)   |


## 📝 TASK APIs (Nested under Project)

| Method | Endpoint                                  | Description   |
| ------ | ----------------------------------------- | ------------- |
| POST   | `api/projects/{project_id}/tasks/`           | Create task   |
| GET    | `api/projects/{project_id}/tasks/`           | List tasks    |
| GET    | `api/projects/{project_id}/tasks/{task_id}/` | Retrieve task |
| PATCH  | `api/projects/{project_id}/tasks/{task_id}/` | Update task   |
| DELETE | `api/projects/{project_id}/tasks/{task_id}/` | Delete task   |

**Task Rules**

* MEMBER → read-only
* ADMIN / OWNER → full access
* Assigned user → status update only


## 💬 TASK COMMENT APIs (Nested under Task)

| Method | Endpoint                                  | Description                  |
| ------ | ----------------------------------------- | ---------------------------- |
| POST   | `api/tasks/{task_id}/comments/`              | Add comment                  |
| GET    | `api/tasks/{task_id}/comments/`              | List comments                |
| GET    | `api/tasks/{task_id}/comments/{comment_id}/` | Retrieve comment             |
| PATCH  | `api/tasks/{task_id}/comments/{comment_id}/` | Edit comment (author only)   |
| DELETE | `api/tasks/{task_id}/comments/{comment_id}/` | Delete comment (author only) |


## 🔎 FILTERING PARAMETERS

| Query Key     | Type    | Description                   | Example                    |
| ------------- | ------- | ----------------------------- | -------------------------- |
| `status`      | Integer | Filter tasks by status        | `?status=1`                |
| `assigned_to` | UUID    | Filter tasks by assigned user | `?assigned_to=<user_uuid>` |

### Status Values

| Value | Meaning     |
| ----- | ----------- |
| 1     | TODO        |
| 2     | IN_PROGRESS |
| 3     | DONE        |



## 🔃 ORDERING PARAMETERS

| Query Key              | Description            | Example                 |
| ---------------------- | ---------------------- | ----------------------- |
| `ordering=created_at`  | Oldest first           | `?ordering=created_at`  |
| `ordering=-created_at` | Newest first (default) | `?ordering=-created_at` |
| `ordering=updated_at`  | Order by last update   | `?ordering=updated_at`  |
| `ordering=status`      | Order by status        | `?ordering=status`      |



## 🔀 COMBINED ORDERING

| Use Case        | Example                        |
| --------------- | ------------------------------ |
| Status → newest | `?ordering=status,-created_at` |
| Status → oldest | `?ordering=status,created_at`  |



## 📌 QUICK BLOCK

```
/api/projects/{project_id}/tasks/?status=2
/api/projects/{project_id}/tasks/?assigned_to=<uuid>
/api/projects/{project_id}/tasks/?ordering=-created_at
/api/projects/{project_id}/tasks/?ordering=status,-created_at
```

