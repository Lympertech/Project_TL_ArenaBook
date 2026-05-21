from django.http import HttpResponse

from accounts.decorators import user_required


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
    return HttpResponse(f"UC-03 View Field Availability for field {field_id}")
