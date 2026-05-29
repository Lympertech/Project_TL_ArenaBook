from django.utils import timezone

from bookings.models import Booking
from .models import Payment


def process_mock_payment(booking, payment_result="success"):
    if payment_result == "success":
        payment_status = Payment.Status.SUCCESSFUL
    else:
        payment_status = Payment.Status.FAILED

    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_cost,
        status=payment_status,
        payment_type=Payment.PaymentType.INITIAL,
        payment_date=timezone.now(),
    )

    if payment_result == "success":
        booking.status = Booking.Status.CONFIRMED
        booking.save()

    return payment
