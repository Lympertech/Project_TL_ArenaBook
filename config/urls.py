from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("facilities/", include("facilities.urls")),
    path("bookings/", include("bookings.urls")),
    path("payments/", include("payments.urls")),
]
