from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("<int:pk>/update/", views.UpdateTaskView.as_view(), name="task_update"),
    path("<int:pk>/delete/", views.DeleteTaskView.as_view(), name="task_delete"),
]
