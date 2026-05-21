from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import facility_manager_required, system_admin_required
from .forms import (
    BookingRulesForm,
    CancellationPolicyForm,
    FacilityForm,
    FieldForm,
)
from .models import BookingRules, CancellationPolicy, Facility, Field


def search(request):
    return HttpResponse("UC-02 Search Facility")


def detail(request, facility_id):
    return HttpResponse(f"Facility detail placeholder for facility {facility_id}.")


@facility_manager_required
def manager_dashboard_view(request):
    facilities = Facility.objects.filter(manager=request.user).order_by("name")
    return render(
        request,
        "facilities/manager_dashboard.html",
        {"facilities": facilities},
    )


@facility_manager_required
def submit_facility_view(request):
    if request.method == "POST":
        form = FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.manager = request.user
            facility.status = Facility.Status.PENDING
            facility.save()
            return redirect("facilities:manager_dashboard")
    else:
        form = FacilityForm()
    return render(request, "facilities/submit_facility.html", {"form": form})


@facility_manager_required
def manage_booking_rules_view(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id, manager=request.user)
    rules, _ = BookingRules.objects.get_or_create(facility=facility)
    if request.method == "POST":
        form = BookingRulesForm(request.POST, instance=rules)
        if form.is_valid():
            form.save()
            return redirect("facilities:manager_dashboard")
    else:
        form = BookingRulesForm(instance=rules)
    return render(
        request,
        "facilities/manage_booking_rules.html",
        {"facility": facility, "form": form},
    )


@facility_manager_required
def manage_cancellation_policy_view(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id, manager=request.user)
    policy, _ = CancellationPolicy.objects.get_or_create(facility=facility)
    if request.method == "POST":
        form = CancellationPolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect("facilities:manager_dashboard")
    else:
        form = CancellationPolicyForm(instance=policy)
    return render(
        request,
        "facilities/manage_cancellation_policy.html",
        {"facility": facility, "form": form},
    )


@facility_manager_required
def manage_fields_view(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id, manager=request.user)
    editing_field = None

    edit_field_id = request.GET.get("edit")
    if edit_field_id:
        editing_field = get_object_or_404(Field, id=edit_field_id, facility=facility)

    if request.method == "POST":
        field_id = request.POST.get("field_id")
        if field_id:
            editing_field = get_object_or_404(Field, id=field_id, facility=facility)
        form = FieldForm(request.POST, instance=editing_field)
        if form.is_valid():
            field_name = form.cleaned_data["name"]
            duplicate = Field.objects.filter(facility=facility, name__iexact=field_name)
            if editing_field:
                duplicate = duplicate.exclude(id=editing_field.id)
            if duplicate.exists():
                form.add_error("name", "A field with this name already exists for this facility.")
            else:
                field = form.save(commit=False)
                field.facility = facility
                field.save()
                return redirect("facilities:manage_fields", facility_id=facility.id)
    else:
        form = FieldForm(instance=editing_field)

    fields = facility.fields.order_by("name")
    return render(
        request,
        "facilities/manage_fields.html",
        {
            "facility": facility,
            "fields": fields,
            "form": form,
            "editing_field": editing_field,
        },
    )


@facility_manager_required
def manage_field_slots(request, field_id):
    return HttpResponse(f"UC-12 Create or Update Field Slots for field {field_id}")


@facility_manager_required
def manage_unavailability(request, field_id):
    return HttpResponse(f"UC-13 Declare Temporary Field Unavailability for field {field_id}")


@system_admin_required
def pending_facilities_view(request):
    if request.method == "POST":
        facility = get_object_or_404(
            Facility,
            id=request.POST.get("facility_id"),
            status=Facility.Status.PENDING,
        )
        action = request.POST.get("action")
        if action == "approve":
            facility.status = Facility.Status.ACTIVE
            facility.save()
        elif action == "reject":
            facility.status = Facility.Status.REJECTED
            facility.save()
        return redirect("facilities:admin_pending")

    pending_facilities = (
        Facility.objects.filter(status=Facility.Status.PENDING)
        .select_related("manager")
        .order_by("name")
    )
    return render(
        request,
        "facilities/pending_facilities.html",
        {
            "title": "UC-14 Approve Facility Submission",
            "pending_facilities": pending_facilities,
        },
    )


manager_dashboard = manager_dashboard_view
manager_new = submit_facility_view
manage_rules = manage_booking_rules_view
manage_cancellation_policy = manage_cancellation_policy_view
manage_fields = manage_fields_view
admin_pending = pending_facilities_view
