from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import user_required
from bookings.models import Booking
from bookings.services import validate_pending_booking_for_payment
from .services import process_mock_payment


@user_required
def pay_booking(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("field__facility", "slot", "user"),
        id=booking_id,
        user=request.user,
    )
    error_message = None

    if booking.status != Booking.Status.PENDING:
        messages.error(request, "Booking is not pending.")
        return redirect("bookings:my_bookings")

    if request.method == "POST":
        payment_result = request.POST.get("payment_result")
        if payment_result not in {"success", "failed"}:
            error_message = "Invalid payment action."
            messages.error(request, error_message)
        else:
            try:
                validate_pending_booking_for_payment(booking, request.user)
            except ValidationError as error:
                error_message = error.messages[0]
                messages.error(request, error_message)
            else:
                process_mock_payment(booking, payment_result)
                if payment_result == "success":
                    messages.success(request, "Payment successful. Booking confirmed.")
                    return redirect("bookings:my_bookings")
                error_message = "Payment failed. The booking remains pending."
                messages.error(request, error_message)

    return render(
        request,
        "payments/pay_booking.html",
        {
            "booking": booking,
            "error_message": error_message,
        },
    )
