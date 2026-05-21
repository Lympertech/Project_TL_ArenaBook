from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .decorators import user_required
from .forms import RegisterForm
from .models import User


def role_redirect(user):
    if user.role == User.Role.FACILITY_MANAGER:
        return redirect("facilities:manager_dashboard")
    if user.role == User.Role.SYSTEM_ADMIN:
        return redirect("facilities:admin_pending")
    return redirect("accounts:user_dashboard")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return role_redirect(user)
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return role_redirect(user)
    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def dashboard_redirect_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    return role_redirect(request.user)


@user_required
def user_dashboard_view(request):
    return render(request, "accounts/user_dashboard.html")


register = register_view
