from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from accounts.decorators import user_required
from facilities.models import Facility, Field, Slot
from facilities.services import get_available_slots
from .models import Booking
from .services import calculate_booking_cost, create_pending_booking


@user_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("field__facility", "slot")
        .order_by("-created_at")
    )
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@user_required
def create_booking(request):
    slot_id = request.POST.get("slot_id") if request.method == "POST" else request.GET.get("slot_id")
    if not slot_id:
        messages.error(request, "Please select an available slot before creating a booking.")
        return redirect("facilities:search")

    slot = get_object_or_404(
        Slot.objects.select_related("field__facility"),
        id=slot_id,
        field__facility__status=Facility.Status.ACTIVE,
    )
    price = calculate_booking_cost(slot)
    error_message = None

    if request.method == "POST":
        try:
            booking = create_pending_booking(request.user, slot)
        except ValidationError as error:
            error_message = error.messages[0]
            messages.error(request, error_message)
        else:
            messages.success(request, "Pending booking created. Please complete payment.")
            return redirect("payments:pay_booking", booking_id=booking.id)

    return render(
        request,
        "bookings/create_booking.html",
        {
            "slot": slot,
            "price": price,
            "error_message": error_message,
        },
    )


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
