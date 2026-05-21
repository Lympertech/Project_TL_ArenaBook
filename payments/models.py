from django.db import models

from bookings.models import Booking


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        FAILED = "FAILED", "Failed"
        REFUND_PENDING = "REFUND_PENDING", "Refund Pending"
        REFUNDED = "REFUNDED", "Refunded"

    class PaymentType(models.TextChoices):
        INITIAL = "INITIAL", "Initial"
        ADDITIONAL = "ADDITIONAL", "Additional"
        REFUND = "REFUND", "Refund"

    booking = models.ForeignKey(
        Booking,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.INITIAL,
    )

    def __str__(self):
        return f"Payment {self.id} for booking {self.booking_id}"
