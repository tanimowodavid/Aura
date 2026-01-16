from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    CHECK_IN_CHOICES = [
        ("daily", "Daily"),
        ("twice_weekly", "Twice Weekly"),
        ("weekly", "Weekly"),
        ("biweekly", "Biweekly"),
        ("monthly", "Monthly"),
    ]
    is_onboarded = models.BooleanField(default=False)
    check_in_frequency = models.CharField(
        max_length=20,
        choices=CHECK_IN_CHOICES,
        default="weekly"
    )

    next_check_in_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
