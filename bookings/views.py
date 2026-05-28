from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date

from accounts.decorators import user_required
from facilities.models import Facility, Field
from facilities.services import get_available_slots


@user_required
def my_bookings(request):
    return HttpResponse("My Bookings placeholder. Booking management logic will be added later.")


@user_required
def create_booking(request):
    return HttpResponse("UC-04 Create Pending Booking")


@user_required
def modify_booking(request, booking_id):
    return HttpResponse(f"UC-06 Modify Confirmed Booking {booking_id}")


@user_required
def cancel_booking(request, booking_id):
    return HttpResponse(f"UC-07 Cancel Confirmed Booking {booking_id}")


@user_required
def field_availability(request, field_id):
    field = get_object_or_404(
        Field.objects.select_related("facility"),
        id=field_id,
        facility__status=Facility.Status.ACTIVE,
    )
    date_value = request.GET.get("date", "").strip()
    selected_date = parse_date(date_value) if date_value else None
    invalid_date = bool(date_value and selected_date is None)
    available_slots = [] if invalid_date else get_available_slots(field, selected_date)

    return render(
        request,
        "bookings/field_availability.html",
        {
            "field": field,
            "date_value": date_value,
            "selected_date": selected_date,
            "invalid_date": invalid_date,
            "available_slots": available_slots,
        },
    )
