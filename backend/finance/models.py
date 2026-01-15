from django.db import models
from django.conf import settings
from base.models import TimeStampedModel

# Create your models here.
class BalanceSnapshot(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.amount} on {self.date}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_expense = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Income(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="incomes")
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Income {self.amount} - {self.user.email}"


class Expense(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="incomes")
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Expense {self.amount} - {self.user.email}"
    

class Goal(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_length=12, decimal_places=2)
    current_amount = models.DecimalField(max_length=12, decimal_places=2)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.user.email})"


class CheckIn(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scheduled_for = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    user_feedback = models.CharField(
        max_length=20,
        choices=[
            ("helpful", "Helpful"),
            ("neutral", "Neutral"),
            ("confusing", "Confusing"),
        ],
        blank=True
    )

    def __str__(self):
        return f"Check-in for {self.user.email}"
