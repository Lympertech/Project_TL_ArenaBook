from django.http import HttpResponse


def search(request):
    return HttpResponse("UC-02 Search Facility")


def detail(request, facility_id):
    return HttpResponse(f"Facility detail placeholder for facility {facility_id}.")


def manager_dashboard(request):
    return HttpResponse("Facility manager placeholder. Business logic will be added later.")


def manager_new(request):
    return HttpResponse("UC-10 Submit Facility")


def manage_rules(request, facility_id):
    return HttpResponse(f"UC-08 Manage Booking Rules for facility {facility_id}")


def manage_cancellation_policy(request, facility_id):
    return HttpResponse(f"UC-09 Manage Cancellation Policy for facility {facility_id}")


def manage_fields(request, facility_id):
    return HttpResponse(f"UC-11 Create or Update Field for facility {facility_id}")


def manage_field_slots(request, field_id):
    return HttpResponse(f"UC-12 Create or Update Field Slots for field {field_id}")


def manage_unavailability(request, field_id):
    return HttpResponse(f"UC-13 Declare Temporary Field Unavailability for field {field_id}")


def admin_pending(request):
    return HttpResponse("UC-14 Approve Facility Submission")
