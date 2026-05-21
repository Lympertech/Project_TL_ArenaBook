from django.urls import path

from . import views


app_name = "facilities"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("<int:facility_id>/", views.detail, name="detail"),
    path("manager/", views.manager_dashboard_view, name="manager_dashboard"),
    path("manager/new/", views.submit_facility_view, name="manager_new"),
    path("manager/<int:facility_id>/rules/", views.manage_booking_rules_view, name="manage_rules"),
    path(
        "manager/<int:facility_id>/cancellation-policy/",
        views.manage_cancellation_policy_view,
        name="manage_cancellation_policy",
    ),
    path("manager/<int:facility_id>/fields/", views.manage_fields_view, name="manage_fields"),
    path(
        "manager/fields/<int:field_id>/slots/",
        views.manage_field_slots,
        name="manage_field_slots",
    ),
    path(
        "manager/fields/<int:field_id>/unavailability/",
        views.manage_unavailability,
        name="manage_unavailability",
    ),
    path("admin-panel/pending/", views.pending_facilities_view, name="admin_pending"),
]
