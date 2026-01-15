from .models import BalanceSnapshot
from .models import Income, Expense, Goal
from django.db.models import Sum

# Get current balance
def get_current_balance(user):
    snapshot = (
        BalanceSnapshot.objects
        .filter(user=user)
        .order_by("-date")
        .first()
    )
    return snapshot.amount if snapshot else None


# Total expenses in a date range
def get_total_expenses(user, start_date, end_date):
    return (
        Expense.objects
        .filter(user=user, date__range=(start_date, end_date))
        .aggregate(total=Sum("amount"))["total"] or 0
    )


# Total income in a date range
def get_total_income(user, start_date, end_date):
    return (
        Income.objects
        .filter(user=user, date__range=(start_date, end_date))
        .aggregate(total=Sum("amount"))["total"] or 0
    )


# Expenses by category (dashboard + Aura insight)
def expenses_by_category(user, start_date, end_date):
    return (
        Expense.objects
        .filter(user=user, date__range=(start_date, end_date))
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )


# Goal progress
def get_active_goals(user):
    return Goal.objects.filter(user=user, is_active=True)
