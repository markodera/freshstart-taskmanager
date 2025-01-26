from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from .tokens import account_activation_token
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView, PasswordChangeView

User = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "authentication/signup_form.html"
    success_url = reverse_lazy("authentication:login")

    def form_valid(self, form):
        try:
            self.object = form.save()
            form.send_activation_email(self.request, self.object)
            messages.success(
                self.request,
                "Please check your email to activate your account."
            )
            return redirect(self.success_url)
        except Exception as e:
            messages.error(
                self.request,
                "There was an error sending the activation email. Please try again."
            )
            return self.form_invalid(form)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect("authentication:login")
    else:
        messages.error(request, "Invalid activation link!")
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
