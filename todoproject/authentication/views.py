from django.shortcuts import redirect
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
)
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "authentication/signup_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        form.send_activation_email(self.request, self.object)
        return response


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect("authentication:login")
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("authentication:signup")


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


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "authentication/password_change_form.html"
    form_class = CustomPasswordChangeForm
