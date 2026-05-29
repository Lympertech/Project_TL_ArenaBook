from decimal import Decimal

from django.core.exceptions import ValidationError

from accounts.models import User
from facilities.models import BookingRules, Facility, TemporaryUnavailability
from .models import Booking


def is_slot_available_for_booking(slot, user=None, exclude_booking_id=None):
    if not slot:
        return False
    if slot.field.facility.status != Facility.Status.ACTIVE:
        return False

    confirmed_bookings = Booking.objects.filter(
        field=slot.field,
        status=Booking.Status.CONFIRMED,
        slot__start_datetime__lt=slot.end_datetime,
        slot__end_datetime__gt=slot.start_datetime,
    )
    if exclude_booking_id:
        confirmed_bookings = confirmed_bookings.exclude(id=exclude_booking_id)
    if confirmed_bookings.exists():
        return False

    if TemporaryUnavailability.objects.filter(
        field=slot.field,
        start_datetime__lt=slot.end_datetime,
        end_datetime__gt=slot.start_datetime,
    ).exists():
        return False

    if user:
        pending_bookings = Booking.objects.filter(
            user=user,
            slot=slot,
            status=Booking.Status.PENDING,
        )
        if exclude_booking_id:
            pending_bookings = pending_bookings.exclude(id=exclude_booking_id)
        if pending_bookings.exists():
            return False

    return True


def calculate_booking_cost(slot):
    try:
        return BookingRules.objects.get(facility=slot.field.facility).price_amount
    except BookingRules.DoesNotExist:
        return Decimal("0.00")


def create_pending_booking(user, slot):
    if user.role != User.Role.USER:
        raise ValidationError("Only normal users can create bookings.")
    if not is_slot_available_for_booking(slot, user=user):
        raise ValidationError("This slot is no longer available.")

    return Booking.objects.create(
        user=user,
        field=slot.field,
        slot=slot,
        status=Booking.Status.PENDING,
        total_cost=calculate_booking_cost(slot),
    )


def validate_pending_booking_for_payment(booking, user):
    if booking.user != user:
        raise ValidationError("You cannot pay for this booking.")
    if booking.status != Booking.Status.PENDING:
        raise ValidationError("Booking is not pending.")
    if not is_slot_available_for_booking(
        booking.slot,
        user=user,
        exclude_booking_id=booking.id,
    ):
        raise ValidationError("This slot is no longer available.")
    return True
