from django.contrib import admin

from .models import (
    BookingRules,
    CancellationPolicy,
    Facility,
    Field,
    Slot,
    TemporaryUnavailability,
)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "manager", "status")


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", "facility", "sport_type", "surface_type")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("field", "start_datetime", "end_datetime")


@admin.register(BookingRules)
class BookingRulesAdmin(admin.ModelAdmin):
    list_display = (
        "facility",
        "price_amount",
        "day_type",
        "start_time",
        "end_time",
    )


@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = (
        "facility",
        "cancellation_deadline_hours",
        "refund_percentage",
    )


@admin.register(TemporaryUnavailability)
class TemporaryUnavailabilityAdmin(admin.ModelAdmin):
    list_display = ("field", "start_datetime", "end_datetime")
