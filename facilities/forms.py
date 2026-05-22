from django import forms

from .models import (
    BookingRules,
    CancellationPolicy,
    Facility,
    Field,
    Slot,
    TemporaryUnavailability,
)


EUROPEAN_DATETIME_FORMAT = "%d/%m/%Y %H:%M"
DATETIME_INPUT_FORMATS = [EUROPEAN_DATETIME_FORMAT]
DATETIME_WIDGET_ATTRS = {
    "placeholder": "dd/mm/yyyy HH:MM",
}
DATETIME_ERROR_MESSAGES = {
    "invalid": "Use European format: dd/mm/yyyy HH:MM.",
}


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ("name", "location", "description")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class BookingRulesForm(forms.ModelForm):
    price_amount = forms.DecimalField(
        label="Price amount (€)",
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
    )
    start_time = forms.TimeField(label="Start time")
    end_time = forms.TimeField(label="End time")
    min_notice_hours = forms.IntegerField(label="Minimum notice before booking (hours)")
    max_duration_minutes = forms.IntegerField(label="Maximum booking duration (minutes)")
    modification_limit = forms.IntegerField(label="Maximum booking modifications")

    class Meta:
        model = BookingRules
        fields = (
            "price_amount",
            "start_time",
            "end_time",
            "min_notice_hours",
            "max_duration_minutes",
            "modification_limit",
        )
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }


class CancellationPolicyForm(forms.ModelForm):
    class Meta:
        model = CancellationPolicy
        fields = ("cancellation_deadline_hours", "refund_percentage")


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ("name", "sport_type", "surface_type")


class SlotForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        label="Start datetime (dd/mm/yyyy HH:MM)",
        input_formats=DATETIME_INPUT_FORMATS,
        error_messages=DATETIME_ERROR_MESSAGES,
        widget=forms.DateTimeInput(
            attrs=DATETIME_WIDGET_ATTRS,
            format=EUROPEAN_DATETIME_FORMAT,
        ),
    )
    end_datetime = forms.DateTimeField(
        label="End datetime (dd/mm/yyyy HH:MM)",
        input_formats=DATETIME_INPUT_FORMATS,
        error_messages=DATETIME_ERROR_MESSAGES,
        widget=forms.DateTimeInput(
            attrs=DATETIME_WIDGET_ATTRS,
            format=EUROPEAN_DATETIME_FORMAT,
        ),
    )

    class Meta:
        model = Slot
        fields = ("start_datetime", "end_datetime")


class TemporaryUnavailabilityForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        label="Start datetime (dd/mm/yyyy HH:MM)",
        input_formats=DATETIME_INPUT_FORMATS,
        error_messages=DATETIME_ERROR_MESSAGES,
        widget=forms.DateTimeInput(
            attrs=DATETIME_WIDGET_ATTRS,
            format=EUROPEAN_DATETIME_FORMAT,
        ),
    )
    end_datetime = forms.DateTimeField(
        label="End datetime (dd/mm/yyyy HH:MM)",
        input_formats=DATETIME_INPUT_FORMATS,
        error_messages=DATETIME_ERROR_MESSAGES,
        widget=forms.DateTimeInput(
            attrs=DATETIME_WIDGET_ATTRS,
            format=EUROPEAN_DATETIME_FORMAT,
        ),
    )

    class Meta:
        model = TemporaryUnavailability
        fields = ("start_datetime", "end_datetime", "reason")
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 3}),
        }
