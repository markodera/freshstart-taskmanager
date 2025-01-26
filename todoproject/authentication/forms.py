from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from .models import CustomUser
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import account_activation_token
from django.conf import settings


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Email",
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Username",
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm password",
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def send_activation_email(self, request, user):  # Changed signature to include request
        try:
            subject = "Activate your Fresh Start account"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
            activation_url = f"{protocol}://{domain}/auth/activate/{uid}/{token}/"
            
            email_body = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'activation_url': activation_url,
            })
            
            email = EmailMessage(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            
        except Exception as e:
            user.is_active = True
            user.save()
            raise forms.ValidationError(f"Error sending activation email: {str(e)}")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Username",
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
    )

    class Meta:
        model = CustomUser
        fields = ("username", "password")


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].help_text = " "
        self.fields["new_password2"].help_text = (
            "<span style='color:white;'>Enter the same password as before, for verification.</span>"
        )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].help_text = " "
        self.fields["new_password2"].help_text = (
            "<span style='color:white;'>Enter the same password as before, for verification.</span>"
        )
