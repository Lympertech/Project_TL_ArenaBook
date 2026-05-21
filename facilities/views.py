from django.http import HttpResponse
from django.shortcuts import render

from accounts.decorators import facility_manager_required, system_admin_required


def search(request):
    return HttpResponse("UC-02 Search Facility")


def detail(request, facility_id):
    return HttpResponse(f"Facility detail placeholder for facility {facility_id}.")


@facility_manager_required
def manager_dashboard(request):
    return render(request, "facilities/manager_dashboard.html")


@facility_manager_required
def manager_new(request):
    return HttpResponse("UC-10 Submit Facility")


@facility_manager_required
def manage_rules(request, facility_id):
    return HttpResponse(f"UC-08 Manage Booking Rules for facility {facility_id}")


@facility_manager_required
def manage_cancellation_policy(request, facility_id):
    return HttpResponse(f"UC-09 Manage Cancellation Policy for facility {facility_id}")


@facility_manager_required
def manage_fields(request, facility_id):
    return HttpResponse(f"UC-11 Create or Update Field for facility {facility_id}")


@facility_manager_required
def manage_field_slots(request, field_id):
    return HttpResponse(f"UC-12 Create or Update Field Slots for field {field_id}")


@facility_manager_required
def manage_unavailability(request, field_id):
    return HttpResponse(f"UC-13 Declare Temporary Field Unavailability for field {field_id}")


@system_admin_required
def admin_pending(request):
    return render(
        request,
        "facilities/pending_facilities.html",
        {"title": "UC-14 Approve Facility Submission"},
    )


manager_dashboard_view = manager_dashboard
pending_facilities_view = admin_pending
