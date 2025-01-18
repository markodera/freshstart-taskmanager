from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),  # Add this line
    path("logout/", views.logout_view, name="logout"),
]