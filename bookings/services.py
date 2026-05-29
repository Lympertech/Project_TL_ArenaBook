from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import User
from facilities.models import (
    BookingRules,
    CancellationPolicy,
    Facility,
    Slot,
    TemporaryUnavailability,
)
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


def get_available_slots_for_modification(booking):
    if booking.status != Booking.Status.CONFIRMED:
        raise ValidationError("Only confirmed bookings can be modified.")

    slots = (
        Slot.objects.filter(field=booking.field)
        .exclude(id=booking.slot_id)
        .select_related("field__facility")
        .order_by("start_datetime")
    )
    return [
        slot
        for slot in slots
        if is_slot_available_for_booking(slot, exclude_booking_id=booking.id)
    ]


def validate_booking_modification(booking, new_slot, user):
    if booking.user_id != user.id:
        raise ValidationError("You cannot modify this booking.")
    if booking.status != Booking.Status.CONFIRMED:
        raise ValidationError("Only confirmed bookings can be modified.")
    if new_slot.field_id != booking.field_id:
        raise ValidationError("The new slot must belong to the same field.")
    if new_slot.field.facility.status != Facility.Status.ACTIVE:
        raise ValidationError("This facility is not active.")

    try:
        rules = BookingRules.objects.get(facility=booking.field.facility)
    except BookingRules.DoesNotExist:
        rules = None
    if rules and rules.modification_limit == 0:
        raise ValidationError("This booking cannot be modified under the facility rules.")

    if not is_slot_available_for_booking(
        new_slot,
        exclude_booking_id=booking.id,
    ):
        raise ValidationError("The selected slot is no longer available.")
    return True


def modify_confirmed_booking(booking, new_slot, user):
    validate_booking_modification(booking, new_slot, user)
    booking.field = new_slot.field
    booking.slot = new_slot
    booking.status = Booking.Status.CONFIRMED
    booking.total_cost = calculate_booking_cost(new_slot)
    booking.save()
    return booking


def calculate_refund_amount(booking):
    try:
        policy = CancellationPolicy.objects.get(facility=booking.field.facility)
    except CancellationPolicy.DoesNotExist:
        return Decimal("0.00")

    cancellation_deadline = booking.slot.start_datetime - timedelta(
        hours=policy.cancellation_deadline_hours
    )
    if timezone.now() >= cancellation_deadline:
        raise ValidationError("Cancellation deadline has passed.")

    refund = (
        booking.total_cost
        * Decimal(policy.refund_percentage)
        / Decimal("100")
    )
    return refund.quantize(Decimal("0.01"))


def cancel_confirmed_booking(booking, user):
    if booking.user_id != user.id:
        raise ValidationError("You cannot cancel this booking.")
    if booking.status != Booking.Status.CONFIRMED:
        raise ValidationError("Only confirmed bookings can be cancelled.")

    refund_amount = calculate_refund_amount(booking)
    if refund_amount > Decimal("0.00"):
        from payments.models import Payment

        Payment.objects.create(
            booking=booking,
            amount=refund_amount,
            status=Payment.Status.REFUNDED,
            payment_type=Payment.PaymentType.REFUND,
            payment_date=timezone.now(),
        )

    booking.status = Booking.Status.CANCELLED
    booking.save()
    return booking, refund_amount
