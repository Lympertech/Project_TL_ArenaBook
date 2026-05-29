from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from accounts.decorators import user_required
from facilities.models import Facility, Field, Slot
from facilities.services import get_available_slots
from .models import Booking
from .services import (
    calculate_booking_cost,
    calculate_refund_amount,
    cancel_confirmed_booking,
    create_pending_booking,
    get_available_slots_for_modification,
    modify_confirmed_booking,
)


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
    booking = get_object_or_404(
        Booking.objects.select_related("field__facility", "slot", "user"),
        id=booking_id,
        user=request.user,
    )
    if booking.status != Booking.Status.CONFIRMED:
        messages.error(request, "Only confirmed bookings can be modified.")
        return redirect("bookings:my_bookings")

    error_message = None

    if request.method == "POST":
        new_slot_id = request.POST.get("new_slot_id")
        new_slot = None
        if new_slot_id:
            try:
                new_slot = (
                    Slot.objects.select_related("field__facility")
                    .filter(id=new_slot_id, field=booking.field)
                    .first()
                )
            except (TypeError, ValueError):
                new_slot = None
        if not new_slot:
            error_message = "Please select a valid slot."
            messages.error(request, error_message)
        else:
            try:
                modify_confirmed_booking(booking, new_slot, request.user)
            except ValidationError as error:
                error_message = error.messages[0]
                messages.error(request, error_message)
            else:
                messages.success(request, "Booking modified.")
                return redirect("bookings:my_bookings")

    available_slots = get_available_slots_for_modification(booking)
    return render(
        request,
        "bookings/modify_booking.html",
        {
            "booking": booking,
            "available_slots": available_slots,
            "error_message": error_message,
        },
    )


@user_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("field__facility", "slot", "user"),
        id=booking_id,
        user=request.user,
    )
    if booking.status != Booking.Status.CONFIRMED:
        messages.error(request, "Only confirmed bookings can be cancelled.")
        return redirect("bookings:my_bookings")

    policy = getattr(booking.field.facility, "cancellation_policy", None)
    error_message = None
    refund_amount = None
    can_cancel = True

    try:
        refund_amount = calculate_refund_amount(booking)
    except ValidationError as error:
        error_message = error.messages[0]
        can_cancel = False

    if request.method == "POST":
        if not can_cancel:
            messages.error(request, error_message)
        else:
            try:
                booking, refund_amount = cancel_confirmed_booking(booking, request.user)
            except ValidationError as error:
                error_message = error.messages[0]
                messages.error(request, error_message)
                can_cancel = False
            else:
                messages.success(
                    request,
                    f"Booking cancelled and refund processed: {refund_amount}.",
                )
                return redirect("bookings:my_bookings")

    return render(
        request,
        "bookings/cancel_booking.html",
        {
            "booking": booking,
            "policy": policy,
            "refund_amount": refund_amount,
            "refund_amount_available": refund_amount is not None,
            "can_cancel": can_cancel,
            "error_message": error_message,
        },
    )


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
