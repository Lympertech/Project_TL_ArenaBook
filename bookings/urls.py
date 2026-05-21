from django.urls import path

from . import views


app_name = "bookings"

urlpatterns = [
    path("my/", views.my_bookings, name="my_bookings"),
    path("create/", views.create_booking, name="create_booking"),
    path("<int:booking_id>/modify/", views.modify_booking, name="modify_booking"),
    path("<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
    path(
        "fields/<int:field_id>/availability/",
        views.field_availability,
        name="field_availability",
    ),
]
