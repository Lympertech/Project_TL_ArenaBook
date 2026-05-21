from django.http import HttpResponse


def register(request):
    return HttpResponse("UC-01 Register User")


def login_view(request):
    return HttpResponse("Login placeholder. Authentication logic will be added later.")


def logout_view(request):
    return HttpResponse("Logout placeholder. Authentication logic will be added later.")
