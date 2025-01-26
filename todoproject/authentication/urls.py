from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomSetPasswordForm

app_name = "authentication"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path(
        "login/",
        views.CustomLoginView.as_view(),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path(
        "password_change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/password_reset_form.html",
            email_template_name="authentication/password_reset_email.html",
            success_url="/auth/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
            success_url="/auth/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
