from django import forms

from .models import BookingRules, CancellationPolicy, Facility, Field


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ("name", "location", "description")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class BookingRulesForm(forms.ModelForm):
    class Meta:
        model = BookingRules
        fields = (
            "price_amount",
            "day_type",
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
