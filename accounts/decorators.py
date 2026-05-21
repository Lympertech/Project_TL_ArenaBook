from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

from .models import User


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role != required_role:
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


user_required = role_required(User.Role.USER)
facility_manager_required = role_required(User.Role.FACILITY_MANAGER)
system_admin_required = role_required(User.Role.SYSTEM_ADMIN)
