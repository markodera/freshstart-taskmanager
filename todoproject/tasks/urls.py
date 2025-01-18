from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # List and Create
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    
    # Read, Update, Delete
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # Ajax endpoints
    path('task/<int:pk>/toggle/', views.toggle_task_completion, name='task_toggle'),
    
    # Filtered views
    path('tasks/priority/<str:priority>/', views.TaskListView.as_view(), name='task_list_by_priority'),
    path('tasks/due/<str:due_filter>/', views.TaskListView.as_view(), name='task_list_by_due'),
    path('tasks/status/<str:status>/', views.TaskListView.as_view(), name='task_list_by_status'),
]