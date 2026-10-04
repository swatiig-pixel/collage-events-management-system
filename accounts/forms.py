from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import StudentProfile

class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        )
    )

    usn = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your USN",
            }
        )
    )

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
            }
        )
    )

    branch = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your branch",
            }
        )
    )

    semester = forms.IntegerField(
        min_value=1,
        max_value=8,
        required=True,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your semester",
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "usn",
            "branch",
            "semester",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Choose a username",
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your email",
        })

        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your full name",
        })

        self.fields["usn"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your USN",
        })

        self.fields["branch"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your branch",
        })

        self.fields["semester"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your semester",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Create a password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm your password",
        })

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        self.order_fields([
            "username",
            "email",
            "name",
            "usn",
            "branch",
            "semester",
            "password1",
            "password2",
        ])

    def save(self, commit=True):

        user = super().save(commit=commit)

        if commit:

            StudentProfile.objects.create(
                user=user,
                name=self.cleaned_data["name"],
                usn=self.cleaned_data["usn"],
                branch=self.cleaned_data["branch"],
                semester=self.cleaned_data["semester"],
            )

        return user

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        )
    )
