from django.conf import settings
from django.db import models

from facilities.models import Field, Slot


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="bookings",
        on_delete=models.CASCADE,
    )
    field = models.ForeignKey(
        Field,
        related_name="bookings",
        on_delete=models.PROTECT,
    )
    slot = models.ForeignKey(
        Slot,
        related_name="bookings",
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Booking {self.id} - {self.user}"
