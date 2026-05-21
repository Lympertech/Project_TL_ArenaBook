from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=(
            (User.Role.USER, "User"),
            (User.Role.FACILITY_MANAGER, "Facility Manager"),
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user
