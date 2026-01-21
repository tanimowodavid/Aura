from django.conf import settings
from django.db import models


class FinancialProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="financial_profile"
    )

    estimated_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    primary_goal = models.CharField(
        max_length=255
    )


    # Flexible, AI-friendly context
    financial_context = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FinanceHistory(models.Model):
    profile = models.ForeignKey(FinancialProfile, on_delete=models.CASCADE, related_name='history')
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True) # The "Time" axis for your graph

    class Meta:
        ordering = ['timestamp']



class CheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="checkins"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Snapshot of financial state at check-in time
    estimated_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # User-reported updates during the session
    user_update = models.JSONField(
        help_text="What the user said during this check-in",
        default=dict,
        blank=True
    )

    # Aura’s interpretation + summary
    summary = models.TextField(
        help_text="Aura’s concise summary of the check-in"
    )

    # Actionable advice given by Aura
    advice = models.TextField(
        help_text="Guidance Aura gave the user"
    )

    # Main focus until next check-in
    focus_until_next = models.CharField(
        max_length=255,
        help_text="Single primary financial focus"
    )

    # Aura’s confidence level about the data
    confidence_score = models.PositiveSmallIntegerField(
        help_text="0–100 confidence in data accuracy",
        default=80
    )

    # Optional metadata (flags, risk signals, etc.)
    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"CheckIn({self.user}, {self.created_at.date()})"

