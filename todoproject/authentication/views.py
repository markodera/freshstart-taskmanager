from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task

# Create your views here.


# def signup(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("authentication:dashboard")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "authentication/signup.html", {"form": form})
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "authentication/signup_form.html"
    success_url = reverse_lazy("tasks:task_list")


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("tasks:task_list")

# logout view
def logout_view(request):
    logout(request)
    return redirect("authentication:login")
