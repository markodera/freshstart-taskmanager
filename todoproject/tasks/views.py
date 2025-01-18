from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Q
from .models import Task
from .forms import TaskForm

class TaskUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure users can only access their own tasks"""
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        # Filter by status
        status_filter = self.request.GET.get('status')
        if status_filter == 'completed':
            queryset = queryset.filter(completed=True)
        elif status_filter == 'active':
            queryset = queryset.filter(completed=False)
            
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
            
        # Filter by due date
        due_filter = self.request.GET.get('due')
        if due_filter == 'overdue':
            queryset = queryset.filter(
                due_date__lt=timezone.now().date(),
                completed=False
            )
        elif due_filter == 'today':
            queryset = queryset.filter(due_date=timezone.now().date())
        elif due_filter == 'week':
            queryset = queryset.filter(
                due_date__range=[
                    timezone.now().date(),
                    timezone.now().date() + timezone.timedelta(days=7)
                ]
            )

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset.order_by('due_date', '-priority', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overdue_count'] = Task.objects.filter(
            user=self.request.user,
            completed=False,
            due_date__lt=timezone.now().date()
        ).count()
        return context

class TaskDetailView(TaskUserMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'task': {
                    'id': self.object.id,
                    'title': self.object.title,
                    'priority': self.object.priority,
                    'due_date': self.object.due_date,
                }
            })
        return response

class TaskUpdateView(TaskUserMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

class TaskDeleteView(TaskUserMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return HttpResponseRedirect(success_url)

@login_required
def toggle_task_completion(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        
        return JsonResponse({
            'success': True,
            'completed': task.completed,
            'task_id': task.id
        })
    return JsonResponse({'success': False}, status=400)