from django.http import HttpResponse

from accounts.decorators import user_required


@user_required
def pay_booking(request, booking_id):
    return HttpResponse(f"UC-05 Pay Pending Booking {booking_id}")
