from django.core.exceptions import ValidationError

from bookings.models import Booking
from .models import Slot, TemporaryUnavailability


def validate_time_range(start_datetime, end_datetime):
    if start_datetime >= end_datetime:
        raise ValidationError("Start date and time must be before end date and time.")


def slot_overlaps_existing_slots(field, start_datetime, end_datetime, exclude_slot_id=None):
    slots = Slot.objects.filter(
        field=field,
        start_datetime__lt=end_datetime,
        end_datetime__gt=start_datetime,
    )
    if exclude_slot_id:
        slots = slots.exclude(id=exclude_slot_id)
    return slots.exists()


def slot_conflicts_with_confirmed_bookings(
    field,
    start_datetime,
    end_datetime,
    exclude_slot_id=None,
):
    bookings = Booking.objects.filter(
        field=field,
        status=Booking.Status.CONFIRMED,
        slot__start_datetime__lt=end_datetime,
        slot__end_datetime__gt=start_datetime,
    )
    if exclude_slot_id:
        bookings = bookings.exclude(slot_id=exclude_slot_id)
    return bookings.exists()


def duplicate_temporary_unavailability(
    field,
    start_datetime,
    end_datetime,
    exclude_id=None,
):
    unavailabilities = TemporaryUnavailability.objects.filter(
        field=field,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    if exclude_id:
        unavailabilities = unavailabilities.exclude(id=exclude_id)
    return unavailabilities.exists()


def unavailability_conflicts_with_confirmed_bookings(
    field,
    start_datetime,
    end_datetime,
):
    return Booking.objects.filter(
        field=field,
        status=Booking.Status.CONFIRMED,
        slot__start_datetime__lt=end_datetime,
        slot__end_datetime__gt=start_datetime,
    ).exists()
