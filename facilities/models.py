from datetime import time

from django.conf import settings
from django.db import models


class Facility(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        REJECTED = "REJECTED", "Rejected"

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_facilities",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return self.name


class Field(models.Model):
    facility = models.ForeignKey(
        Facility,
        related_name="fields",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    sport_type = models.CharField(max_length=100)
    surface_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.facility.name} - {self.name}"


class Slot(models.Model):
    field = models.ForeignKey(
        Field,
        related_name="slots",
        on_delete=models.CASCADE,
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.field} ({self.start_datetime} - {self.end_datetime})"


class BookingRules(models.Model):
    facility = models.OneToOneField(
        Facility,
        related_name="booking_rules",
        on_delete=models.CASCADE,
    )
    price_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    day_type = models.CharField(max_length=30, default="ALL")
    start_time = models.TimeField(default=time(0, 0))
    end_time = models.TimeField(default=time(23, 59))
    min_notice_hours = models.PositiveIntegerField(default=0)
    max_duration_minutes = models.PositiveIntegerField(default=120)
    modification_limit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Booking rules for {self.facility.name}"


class CancellationPolicy(models.Model):
    facility = models.OneToOneField(
        Facility,
        related_name="cancellation_policy",
        on_delete=models.CASCADE,
    )
    cancellation_deadline_hours = models.PositiveIntegerField(default=24)
    refund_percentage = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Cancellation policy for {self.facility.name}"


class TemporaryUnavailability(models.Model):
    field = models.ForeignKey(
        Field,
        related_name="temporary_unavailabilities",
        on_delete=models.CASCADE,
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField(blank=True)

    def __str__(self):
        return f"Temporary unavailability for {self.field}"
