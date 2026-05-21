from django.http import HttpResponse


def pay_booking(request, booking_id):
    return HttpResponse(f"UC-05 Pay Pending Booking {booking_id}")
