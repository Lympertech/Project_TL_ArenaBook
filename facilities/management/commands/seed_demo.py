from datetime import datetime, timedelta, time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from facilities.models import (
    BookingRules,
    CancellationPolicy,
    Facility,
    Field,
    Slot,
)


class Command(BaseCommand):
    help = "Create demo ArenaBook users, facility, field, rules, policy, and slots."

    def handle(self, *args, **options):
        User = get_user_model()
        password = "password123"

        user = self.upsert_user(
            User,
            username="user",
            email="user@arenabook.local",
            password=password,
            role=User.Role.USER,
        )
        manager = self.upsert_user(
            User,
            username="manager",
            email="manager@arenabook.local",
            password=password,
            role=User.Role.FACILITY_MANAGER,
        )
        sysadmin = self.upsert_user(
            User,
            username="sysadmin",
            email="sysadmin@arenabook.local",
            password=password,
            role=User.Role.SYSTEM_ADMIN,
            is_staff=True,
        )

        facility, _ = Facility.objects.get_or_create(
            name="Arena Patras",
            defaults={
                "location": "Patras",
                "description": "Demo sports facility",
                "manager": manager,
                "status": Facility.Status.ACTIVE,
            },
        )
        facility.location = "Patras"
        facility.description = "Demo sports facility"
        facility.manager = manager
        facility.status = Facility.Status.ACTIVE
        facility.save()

        field, _ = Field.objects.get_or_create(
            facility=facility,
            name="Court 1",
            defaults={
                "sport_type": "Football",
                "surface_type": "Synthetic grass",
            },
        )
        field.sport_type = "Football"
        field.surface_type = "Synthetic grass"
        field.save()

        BookingRules.objects.update_or_create(
            facility=facility,
            defaults={
                "price_amount": Decimal("30.00"),
                "max_duration_minutes": 120,
                "min_notice_hours": 0,
                "modification_limit": 1,
            },
        )

        CancellationPolicy.objects.update_or_create(
            facility=facility,
            defaults={
                "cancellation_deadline_hours": 24,
                "refund_percentage": 100,
            },
        )

        slot_date = timezone.localdate() + timedelta(days=1)
        for start_hour in (18, 20):
            start_datetime = self.make_aware_datetime(slot_date, time(start_hour, 0))
            end_datetime = start_datetime + timedelta(hours=2)
            Slot.objects.get_or_create(
                field=field,
                start_datetime=start_datetime,
                defaults={"end_datetime": end_datetime},
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data ready: user, manager, sysadmin, Arena Patras, Court 1, rules, policy, and slots."
            )
        )

    def upsert_user(self, User, username, email, password, role, is_staff=False):
        user, _ = User.objects.get_or_create(username=username)
        user.email = email
        user.role = role
        user.account_status = "active"
        user.is_staff = is_staff
        user.set_password(password)
        user.save()
        return user

    def make_aware_datetime(self, date_value, time_value):
        naive_datetime = datetime.combine(date_value, time_value)
        if timezone.is_aware(naive_datetime):
            return naive_datetime
        return timezone.make_aware(naive_datetime, timezone.get_current_timezone())
